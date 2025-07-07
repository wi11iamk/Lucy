from __future__ import annotations
import datetime as dt
from sqlalchemy import (
    Column,
    Integer,
    String,
    Float,
    DateTime,
    Boolean,
    JSON,
    LargeBinary,
)
from sqlalchemy.orm import declarative_base

Base = declarative_base()


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
    window_end = Column(DateTime)


# ----- profile tables -----


class BioFact(Base):
    __tablename__ = "bio_fact"
    key = Column(String, primary_key=True)
    value = Column(String)


class LifelineEvent(Base):
    __tablename__ = "lifeline_event"
    id = Column(Integer, primary_key=True)
    date = Column(String, index=True)
    description = Column(String)


class Interest(Base):
    __tablename__ = "interest"
    tag = Column(String, primary_key=True)
    embedding = Column(LargeBinary)  # 384-d vector bytes


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
