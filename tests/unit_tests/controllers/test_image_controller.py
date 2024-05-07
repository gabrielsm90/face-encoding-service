from unittest.mock import patch

from src.exceptions import SessionDoesntExistException
from src.schemas.image import Image


@patch("src.controllers.image_controller.create_image")
@patch("src.controllers.image_controller.verify_token", return_value=True)
def test_image_upload_endpoint_when_credentials_are_valid_returns_200_status_code_and_proper_content(
    _, mock_create_image, client
):
    image_id = 999
    session_id = 123
    file_name = "test_image.jpg"
    image_file = (file_name, b"dummy_image_content")
    mock_create_image.return_value = Image(id=image_id, session_id=session_id, file_name=file_name)

    response = client.post(
        f"sessions/{session_id}/images", files={"file": image_file}, headers={"Authorization": "Bearer token"}
    )
    response_content = response.json()

    created_session = Image(**response_content)

    assert response.status_code == 200
    assert created_session.file_name == file_name
    assert created_session.id == image_id
    assert created_session.session_id == session_id


def test_start_session_without_token_returns_unauthorized_status_code(client):
    session_id = 123
    file_name = "test_image.jpg"
    image_file = (file_name, b"dummy_image_content")

    response = client.post(f"sessions/{session_id}/images", files={"file": image_file})

    assert response.status_code == 401


def test_start_session_with_invalid_token_returns_unauthorized_status_code(client):
    session_id = 123
    file_name = "test_image.jpg"
    image_file = (file_name, b"dummy_image_content")

    response = client.post(
        f"sessions/{session_id}/images", files={"file": image_file}, headers={"Authorization": "Bearer invalid"}
    )

    assert response.status_code == 401


@patch("src.controllers.image_controller.create_image", side_effect=SessionDoesntExistException())
@patch("src.controllers.image_controller.verify_token", return_value=True)
def test_start_session_with_invalid_session_id_returns_bad_request_status_code(_, __, client):
    session_id = 123
    file_name = "test_image.jpg"
    image_file = (file_name, b"dummy_image_content")

    response = client.post(
        f"sessions/{session_id}/images", files={"file": image_file}, headers={"Authorization": "Bearer invalid"}
    )

    assert response.status_code == 404