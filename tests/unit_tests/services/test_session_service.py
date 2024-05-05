from random import randint
from unittest.mock import patch

from src.models.session import Session
from src.services.session_service import create_session, SessionRepository


@patch.object(SessionRepository, "create_session")
def test_create_session_returns_new_session_with_correct_initial_data(mocked_create_session):
    db_session = Session(status="STARTED", uploaded_images=0, id=randint(1, 1000))
    mocked_create_session.return_value = db_session

    result = create_session()

    assert result.images_uploaded == db_session.uploaded_images
    assert result.status == db_session.status
    assert result.id == db_session.id
