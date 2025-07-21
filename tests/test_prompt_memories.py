from lucy_rag import upsert_interest
from db.session import SessionLocal
from response_engine import build_prompt_with_examples


def test_prompt_includes_memories():
    with SessionLocal() as db:
        row = upsert_interest("cats", db)
        assert row.tag == "cats"
        upsert_interest("cats", db)
        db.commit()
    prompt = build_prompt_with_examples("How are you?", {}, [])
    assert "Patient memories:" in prompt and "- cats" in prompt
