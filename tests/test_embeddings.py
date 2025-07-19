from db.session import add_interest
from sqlalchemy import select
from db.session import SessionLocal
from db.models import Interest


def test_embedding_vector_saved(monkeypatch):
    # monkeypatch embed() to avoid real API
    from utils import embeddings as emb_mod

    monkeypatch.setattr(emb_mod, "embed", lambda txt: [42.0] * 1536)

    row = add_interest(patient_id=1, tag="loves 1970 World Series")
    assert len(row.embedding) == 1536
    assert row.embedding[0] == 42.0

    # verify persisted
    with SessionLocal() as db:
        vec = db.scalar(select(Interest.embedding).where(Interest.id == row.id))
        assert vec[0] == 42.0
