from db.models import Base, Interaction
from sqlalchemy import create_engine
from sqlalchemy.orm import Session


def test_interaction_insert():
    engine = create_engine("sqlite:///:memory:", future=True)
    Base.metadata.create_all(engine)
    with Session(engine) as db:
        db.add(
            Interaction(
                user_id="t",
                user_input="hi",
                llm_response="ok",
                emotion_scores={},
                safety_flag=False,
            )
        )
        db.commit()
        assert db.query(Interaction).count() == 1
