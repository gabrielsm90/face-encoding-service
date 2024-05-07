from src.exceptions import MaxNumberOfImagesException, SessionDoesntExistException
from src.repositories.image_repository import ImageRepository
from src.repositories.session_repository import SessionRepository
from src.schemas.image import Image

image_repository = ImageRepository()
session_repository = SessionRepository()


def create_image(session_id: int, file_name: str) -> Image:
    session = session_repository.get_session_by_id(session_id)

    if not session:
        raise SessionDoesntExistException()

    if session.reached_max_number_of_images():
        raise MaxNumberOfImagesException()

    created_image_db = image_repository.create_image(session_id, file_name)

    return Image(
        id=created_image_db.id,
        session_id=created_image_db.session_id,
        file_name=created_image_db.file_name,
    )
