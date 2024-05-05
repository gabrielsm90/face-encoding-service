from typing import Any

from src.models.session import Session
from src.db import SessionLocal


class SessionRepository:
    def __init__(self, db: Any = SessionLocal()):
        self.db = db

    def create_session(self) -> Session:
        db_session = Session()
        self.db.add(db_session)
        self.db.commit()
        self.db.refresh(db_session)
        return db_session
