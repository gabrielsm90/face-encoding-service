from enum import Enum
from pydantic import BaseModel

from src.schemas.image import Image


class SessionStatus(str, Enum):
    STARTED = "STARTED"
    PROCESSING = "PROCESSING"
    COMPLETED = "COMPLETED"


class Session(BaseModel):
    id: int
    status: SessionStatus
    images_uploaded: int
    images: list[Image]
