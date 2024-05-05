from random import randint
from unittest.mock import patch

from src.schemas.session import Session, SessionStatus


@patch("src.controllers.session_controller.create_session")
@patch("src.controllers.session_controller.verify_token", return_value=True)
def test_start_session_endpoint_returns_200_status_and_correct_data(_, mock_create_session, client):
    session_id = randint(1, 1000)
    mock_create_session.return_value = Session(id=session_id, status=SessionStatus.STARTED, images_uploaded=0)

    response = client.post("/sessions", headers={"Authorization": "Bearer token"})
    response_content = response.json()

    created_session = Session(**response_content)

    assert response.status_code == 200
    assert created_session.status == SessionStatus.STARTED
    assert created_session.images_uploaded == 0
    assert created_session.id == session_id


def test_start_session_without_token_returns_unauthorized_status_code(client):
    response = client.post("/sessions")

    assert response.status_code == 401


def test_start_session_with_invalid_token_returns_unauthorized_status_code(client):
    response = client.post("/sessions", headers={"Authorization": "Bearer invalid"})

    assert response.status_code == 401
