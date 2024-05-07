from pydantic import BaseModel


class Image(BaseModel):
    id: int
    session_id: int
    file_name: str
