from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

from src.db import Base


class Session(Base):
    __tablename__ = "sessions"

    id = Column(Integer, primary_key=True)
    status = Column(String, default="STARTED")
    uploaded_images = Column(Integer, default=0)

    images = relationship("Image", back_populates="session")
