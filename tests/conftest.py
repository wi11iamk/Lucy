import pathlib
import sys

import pytest
from sqlalchemy import create_engine, event
from sqlalchemy.pool import StaticPool

# make project root importable *before* we import db.*
PROJECT_ROOT = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

from db.models import Base  # noqa: E402

# ------------------------------------------------------------------


@pytest.fixture(scope="session", autouse=True)
def _in_memory_db():
    """Use an in-memory SQLite DB for every test session."""
    engine = create_engine(
        "sqlite+pysqlite:///:memory:",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,  # ⬅️  single shared connection
        future=True,
    )

    # ✨ ensure SQLite enforces foreign-key constraints
    @event.listens_for(engine, "connect")
    def _enable_fk_constraints(dbapi_conn, _):
        dbapi_conn.execute("PRAGMA foreign_keys=ON")

    Base.metadata.drop_all(engine, checkfirst=True)
    Base.metadata.create_all(engine)

    # ── 1. Re-wire the *original* SessionLocal so every old copy uses the new engine.
    import db.session as db_session  # noqa: E402

    db_session.SessionLocal.configure(bind=engine, expire_on_commit=False)
    TestingSessionLocal = db_session.SessionLocal  # alias, for clarity

    db_session.engine = engine

    # ─── take care of any *copies* made with “from db.session import SessionLocal” ───
    import sys
    import types

    for mod in list(sys.modules.values()):
        if not isinstance(mod, types.ModuleType):
            continue
        if hasattr(mod, "SessionLocal") and getattr(mod, "__name__", "").startswith(
            "tests."
        ):
            # overwrite the stale copy held by the test module
            setattr(mod, "SessionLocal", TestingSessionLocal)

    yield
    engine.dispose()
