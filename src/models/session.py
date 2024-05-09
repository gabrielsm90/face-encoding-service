from sqlalchemy import Column, Integer
from sqlalchemy.orm import relationship

from src.db import Base


class Session(Base):
    __tablename__ = "sessions"

    id = Column(Integer, primary_key=True)

    images = relationship("Image", back_populates="session")

    def reached_max_number_of_images(self) -> bool:
        return len(self.images) == 5
