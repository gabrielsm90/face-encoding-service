import random
from string import ascii_letters

import pytest
from src.repositories.auth_repository import AuthRepository
from src.schemas.user import UserCreate
from src.db import engine, SessionLocal, Base
from src.models.user import User


@pytest.fixture(scope="module")
def test_db():
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()

    yield db

    db.close()


@pytest.fixture
def username():
    return "".join(random.choice(ascii_letters) for _ in range(10))


def test_create_new_user(test_db, username):
    repo = AuthRepository()

    user_create = UserCreate(username=username, password="test_password")
    created_user = repo.create_user(user_create)

    assert created_user is not None
    assert created_user.username == username
    assert created_user.hashed_password == "test_password"


def test_get_existing_user(test_db, username):
    repo = AuthRepository()

    test_user = User(username=username, hashed_password="test_password")
    test_db.add(test_user)
    test_db.commit()

    retrieved_user = repo.get_user(username)

    assert retrieved_user is not None
    assert retrieved_user.username == username
    assert retrieved_user.hashed_password == "test_password"
