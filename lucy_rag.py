"""
lucy_rag.py
-----------
Helpers for storing caregiver “interests” (memory cues) and
retrieving the top-k items with time-decay weighting.

Dependencies: sentence-transformers (MiniLM-L6-v2), numpy, SQLAlchemy.
"""

from __future__ import annotations

import datetime as dt
from typing import List

import numpy as np
from sentence_transformers import SentenceTransformer
from sqlalchemy import select, update
from sqlalchemy.orm import Session

from db.models import Interest

_MODEL = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")


# ────────────────────────── internal utils ──────────────────────────
def _vec_to_bytes(vec: np.ndarray) -> bytes:
    return vec.astype("float32").tobytes()


def _bytes_to_vec(buf: bytes) -> np.ndarray:
    return np.frombuffer(buf, dtype="float32")


# ────────────────────────── public API ───────────────────────────────
def upsert_interest(tag: str, session: Session) -> None:
    """Insert or update an Interest row with fresh embedding + timestamp."""
    emb = _vec_to_bytes(_MODEL.encode(tag, normalize_embeddings=True))
    row = session.get(Interest, tag) or Interest(tag=tag)
    row.embedding = emb
    row.last_used = dt.datetime.utcnow()
    session.add(row)


def fetch_topk(session: Session, k: int = 3, half_life_days: int = 30) -> List[str]:
    """Return up to *k* tags sorted by weight × time-decay."""
    now = dt.datetime.utcnow()
    rows = session.execute(select(Interest)).scalars().all()
    scored = []
    for r in rows:
        age = (now - (r.last_used or now)).days
        decay = 0.5 ** (age / half_life_days)
        scored.append((r.tag, r.weight * decay))
    scored.sort(key=lambda x: x[1], reverse=True)
    return [tag for tag, _ in scored[:k]]


def mark_used(tag: str, session: Session) -> None:
    """Update last_used timestamp after an interest is injected into a prompt."""
    session.execute(
        update(Interest)
        .where(Interest.tag == tag)
        .values(last_used=dt.datetime.utcnow())
    )
