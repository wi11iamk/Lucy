from __future__ import annotations

import datetime as dt
import json

from sqlalchemy import (
    Boolean,
    Column,
    DateTime,
    Float,
    ForeignKey,
    Integer,
    JSON,
    String,
    UniqueConstraint,
)

# from sqlalchemy.dialects.sqlite import JSON
from sqlalchemy.orm import relationship, declarative_base
from sqlalchemy.types import TypeDecorator

Base = declarative_base()


class Vector(TypeDecorator):
    """Stores list[float] as JSON string, returns list on load."""

    impl = String
    cache_ok = True

    def process_bind_param(self, value, dialect):
        return json.dumps(value) if value is not None else None

    def process_result_value(self, value, dialect):
        return json.loads(value) if value is not None else None


class Interaction(Base):
    __tablename__ = "interaction"

    id = Column(Integer, primary_key=True)
    timestamp = Column(DateTime, default=dt.datetime.utcnow, index=True)
    user_id = Column(String, nullable=False)
    user_input = Column(String, nullable=False)
    llm_response = Column(String, nullable=False)
    emotion_scores = Column(JSON, nullable=False)
    safety_flag = Column(Boolean, default=False)
    cognitive_score = Column(Float)  # nullable


class RateLimitWindow(Base):
    __tablename__ = "rate_limit_window"

    user_id = Column(String, primary_key=True)
    request_cnt = Column(Integer, default=0)
    window_end = Column(DateTime)  # nullable


# ---------- profile tables ----------


class BioFact(Base):
    __tablename__ = "bio_fact"

    key = Column(String, primary_key=True)
    value = Column(String)


class LifelineEvent(Base):
    __tablename__ = "lifeline_event"

    id = Column(Integer, primary_key=True)
    date = Column(String, index=True)
    description = Column(String)


class Patient(Base):
    __tablename__ = "patient"

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(String, unique=True, nullable=False)

    # back-reference used in tests
    interests = relationship(
        "Interest",
        back_populates="patient",
        cascade="all, delete-orphan",
    )


class Interest(Base):
    __tablename__ = "interest"

    id = Column(Integer, primary_key=True, autoincrement=True)

    patient_id = Column(
        Integer, ForeignKey("patient.id", ondelete="CASCADE"), nullable=False
    )
    tag = Column(String, nullable=False, index=True)
    weight = Column(Float, default=1.0)

    # store vector as TEXT (JSON) – our Vector type handles (de)serialization
    embedding = Column(Vector, nullable=False)

    # ✅ **make this NULL-able** so inserts without a timestamp succeed
    last_used = Column(DateTime, nullable=True)

    patient = relationship("Patient", back_populates="interests")

    __table_args__ = (UniqueConstraint("patient_id", "tag", name="uix_patient_tag"),)


class CarePlan(Base):
    __tablename__ = "care_plan"

    id = Column(Integer, primary_key=True)
    trigger = Column(String)
    intervention_uri = Column(String)
    kind = Column(String)  # music | video | breathing


class AllowedMedia(Base):
    __tablename__ = "allowed_media"

    uri = Column(String, primary_key=True)
    label = Column(String)
