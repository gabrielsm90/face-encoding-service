from enum import Enum
from pydantic import BaseModel


class SessionStatus(str, Enum):
    STARTED = "STARTED"
    PROCESSING = "PROCESSING"
    COMPLETED = "COMPLETED"


class Session(BaseModel):
    id: int
    status: SessionStatus
    images_uploaded: int
