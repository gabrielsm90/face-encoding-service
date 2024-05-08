import pytest
from src.repositories.session_repository import SessionRepository
from src.schemas.session import SessionStatus
from src.db import engine, SessionLocal, Base


@pytest.fixture(scope="module")
def test_db():
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()

    yield db

    db.close()


def test_create_new_session(test_db):
    repo = SessionRepository()

    created_session = repo.create_session()

    assert created_session is not None
    assert created_session.status == SessionStatus.STARTED
    assert created_session.id > 0


def test_get_session_summary(test_db):
    repo = SessionRepository()

    created_session = repo.create_session()
    fetched_session = repo.get_session_by_id(created_session.id)

    assert created_session == fetched_session
