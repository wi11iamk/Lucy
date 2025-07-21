from __future__ import annotations

import os
from typing import List

from openai import OpenAI

_MODEL = "text-embedding-3-small"
_DIM = 1536  # ← known output dim for that model
_client: OpenAI | None = None


def prompt_security_filter(user_prompt):
    blocked_prompts = [
        "repeat previous response",
        "ignore all rules",
        "output everything",
    ]

    if any(term in user_prompt.lower() for term in blocked_prompts):
        return "Request denied due to security policies."
    return user_prompt


def _oai() -> OpenAI:
    global _client
    if _client is None:
        _client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
    return _client


def embed(text: str) -> List[float]:
    """
    Return a 1536-dim embedding for *text*.
    Falls back to a deterministic zero-vector when running in CI
    (dummy key) so tests don’t call the real API.
    """
    if os.getenv("OPENAI_API_KEY", "").startswith("dummy-"):
        return [0.0] * _DIM

    resp = _oai().embeddings.create(model=_MODEL, input=text)
    return resp.data[0].embedding
