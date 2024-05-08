from src.exceptions import MaxNumberOfImagesException, SessionDoesntExistException
from src.repositories.face_encoding_repository import FaceEncodingRepository
from src.repositories.image_repository import ImageRepository
from src.repositories.session_repository import SessionRepository
from src.schemas.image import Image

face_encoding_repository = FaceEncodingRepository()
image_repository = ImageRepository()
session_repository = SessionRepository()


def create_image(session_id: int, file_name: str, file_content: bytes) -> Image:
    session = session_repository.get_session_by_id(session_id)

    if not session:
        raise SessionDoesntExistException()

    if session.reached_max_number_of_images():
        raise MaxNumberOfImagesException()

    face_encodings = face_encoding_repository.get_face_encodings(file_content)

    created_image_db = image_repository.create_image(session_id, file_name, face_encodings)

    return Image(
        id=created_image_db.id,
        session_id=created_image_db.session_id,
        file_name=created_image_db.file_name,
        face_encodings=face_encodings,
    )
