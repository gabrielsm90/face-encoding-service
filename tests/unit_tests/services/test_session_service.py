from random import randint
from unittest.mock import patch

from src.models.session import Session
from src.services.session_service import create_session, SessionRepository, get_session


@patch.object(SessionRepository, "create_session")
def test_create_session_returns_new_session_with_correct_initial_data(mocked_create_session):
    db_session = Session(status="STARTED", id=randint(1, 1000))
    mocked_create_session.return_value = db_session

    result = create_session()

    assert result.images_uploaded == 0
    assert result.status == db_session.status
    assert result.id == db_session.id


@patch.object(SessionRepository, "get_session_by_id")
def test_get_session_returns_session_with_correct_data(mocked_get_session):
    db_session = Session(status="STARTED", id=randint(1, 1000))
    mocked_get_session.return_value = db_session

    result = get_session(db_session.id)

    assert result.images_uploaded == 0
    assert result.status == db_session.status
    assert result.id == db_session.id
