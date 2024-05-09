from pydantic import BaseModel

from src.schemas.image import Image


class Session(BaseModel):
    id: int
    images_uploaded: int
    images: list[Image]
