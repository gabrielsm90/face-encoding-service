import pytest
from src.repositories.image_repository import ImageRepository
from src.repositories.session_repository import SessionRepository
from src.db import engine, SessionLocal, Base


@pytest.fixture(scope="module")
def test_db():
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()

    yield db

    db.close()


def test_create_new_image(test_db):
    file_name = "my-image.png"

    session_repo = SessionRepository()
    image_repo = ImageRepository()

    created_session = session_repo.create_session()
    created_image = image_repo.create_image(created_session.id, file_name, [[1], [2]])

    assert created_image is not None
