from typing import Any

from src.models.image import Image
from src.db import SessionLocal


class ImageRepository:
    def __init__(self, db: Any = SessionLocal()):
        self.db = db

    def create_image(self, session_id: int, file_name: str, face_encodings: list[list[float]]) -> Image:
        db_image = Image(session_id=session_id, file_name=file_name, face_encodings=face_encodings)
        self.db.add(db_image)
        self.db.commit()
        self.db.refresh(db_image)
        return db_image
