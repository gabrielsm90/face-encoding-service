from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import relationship

from src.db import Base


class Image(Base):
    __tablename__ = "images"

    id = Column(Integer, primary_key=True, index=True)
    file_name = Column(String, index=True)

    session_id = Column(Integer, ForeignKey("sessions.id"))
    session = relationship("Session", back_populates="images")

    face_encodings = Column(JSONB)
