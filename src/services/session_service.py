from src.repositories.session_repository import SessionRepository
from src.schemas.session import Session

session_repository = SessionRepository()


def create_session() -> Session:
    created_session_db = session_repository.create_session()

    return Session(
        id=created_session_db.id, status=created_session_db.status, images_uploaded=created_session_db.uploaded_images
    )
