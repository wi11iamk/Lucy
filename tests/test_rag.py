from lucy_rag import upsert_interest, fetch_topk
from db.session import SessionLocal


def test_interest_roundtrip():
    with SessionLocal() as db:
        row = upsert_interest("cats", db)
        assert row.tag == "cats"

        upsert_interest("cats", db)
        upsert_interest("1970 World Series", db)
        db.commit()
        top = fetch_topk(db, k=2)
        assert {"cats", "1970 World Series"} <= set(top)
