from random import randint
from unittest.mock import patch

import pytest

from src.exceptions import MaxNumberOfImagesException, SessionDoesntExistException
from src.models.image import Image
from src.models.session import Session
from src.schemas.session import SessionStatus
from src.services.image_service import create_image
from src.repositories.image_repository import ImageRepository
from src.repositories.session_repository import SessionRepository
from src.repositories.face_encoding_repository import FaceEncodingRepository


@patch.object(FaceEncodingRepository, "get_face_encodings", return_value=[[1], [2]])
@patch.object(SessionRepository, "get_session_by_id")
@patch.object(ImageRepository, "create_image")
def test_create_image_returns_new_image_with_correct_initial_data(mocked_repo_create_image, mocked_repo_get_session, _):
    file_name = "file_name.png"
    db_session = Image(session_id=123, file_name=file_name, id=randint(1, 1000))
    mocked_repo_create_image.return_value = db_session
    mocked_repo_get_session.return_value = Session(id=123, status=SessionStatus.STARTED)

    result = create_image(123, file_name, b"file content")

    assert result.session_id == db_session.session_id
    assert result.id == db_session.id
    assert result.file_name == db_session.file_name
    assert result.face_encodings == [[1], [2]]


@patch.object(SessionRepository, "get_session_by_id")
@patch.object(ImageRepository, "create_image")
def test_create_image_when_session_has_the_limit_of_images_throws_exception(
    mocked_repo_create_image, mocked_repo_get_session
):
    file_name = "file_name.png"
    db_session = Image(session_id=123, file_name=file_name, id=randint(1, 1000))
    mocked_repo_create_image.return_value = db_session
    mocked_repo_get_session.return_value = Session(
        id=123,
        status=SessionStatus.STARTED,
        images=[
            Image(session_id=123, file_name=file_name, id=randint(1, 10000)),
            Image(session_id=123, file_name=file_name, id=randint(1, 10000)),
            Image(session_id=123, file_name=file_name, id=randint(1, 10000)),
            Image(session_id=123, file_name=file_name, id=randint(1, 10000)),
            Image(session_id=123, file_name=file_name, id=randint(1, 10000)),
        ],
    )

    with pytest.raises(MaxNumberOfImagesException):
        create_image(123, file_name, b"file content")


def test_create_image_when_session_doesnt_exist_raises_exception():
    with pytest.raises(SessionDoesntExistException):
        create_image(123, "file_name.png", b"file content")
