from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship

from src.db import Base


class FaceEncoding(Base):
    __tablename__ = "face_encodings"

    id = Column(Integer, primary_key=True, index=True)
    encoding = Column(String, index=True)

    image_id = Column(Integer, ForeignKey("images.id"))
    image = relationship("Image", back_populates="face_encodings")
