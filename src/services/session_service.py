from src.repositories.session_repository import SessionRepository
from src.schemas.image import Image
from src.schemas.session import Session

session_repository = SessionRepository()


def create_session() -> Session:
    created_session_db = session_repository.create_session()

    return Session(
        id=created_session_db.id,
        status=created_session_db.status,
        images=created_session_db.images,
        images_uploaded=len(created_session_db.images),
    )


def get_session(session_id: int) -> Session:
    session_db = session_repository.get_session_by_id(session_id)

    images = [
        Image(
            id=image_db.id, session_id=session_id, file_name=image_db.file_name, face_encodings=image_db.face_encodings
        )
        for image_db in session_db.images
    ]

    return Session(id=session_db.id, status=session_db.status, images=images, images_uploaded=len(session_db.images))
