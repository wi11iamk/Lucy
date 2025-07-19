from sqlalchemy import create_engine, select, update
from sqlalchemy.orm import sessionmaker
from .models import Interest
import datetime as dt
from utils import embed
from db.models import Base

engine = create_engine("sqlite:///lucy.db", future=True, echo=False)
SessionLocal = sessionmaker(bind=engine, expire_on_commit=False)


def init_db() -> None:
    Base.metadata.create_all(bind=engine)


def add_interest(patient_id: int, tag: str, weight: float = 1.0) -> Interest:
    """Insert a brand-new memory and return the row."""
    vec = embed(tag)
    with SessionLocal() as db:
        row = Interest(
            patient_id=patient_id,
            tag=tag,
            weight=weight,
            embedding=vec,
        )
        db.add(row)
        db.commit()
        db.refresh(row)
        return row


def update_interest_embedding(interest_id: int) -> None:
    """Re-embed an existing tag (if edited) and store the new vector."""
    with SessionLocal() as db:
        tag = db.scalar(select(Interest.tag).where(Interest.id == interest_id))
        if tag is None:
            return
        vec = embed(tag)
        db.execute(
            update(Interest)
            .where(Interest.id == interest_id)
            .values(embedding=vec, last_used=dt.datetime.utcnow())
        )
        db.commit()
