from typing import Any

from src.schemas.user import UserCreate
from src.db import SessionLocal
from src.models.user import User


class AuthRepository:
    def __init__(self, db: Any = SessionLocal()):
        self.db = db

    def create_user(self, user: UserCreate) -> User:
        db_user = User(username=user.username, hashed_password=user.password)
        self.db.add(db_user)
        self.db.commit()
        self.db.refresh(db_user)
        return db_user

    def get_user(self, username: str) -> User:
        return self.db.query(User).filter(User.username == username).first()
