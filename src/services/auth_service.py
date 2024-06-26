import os

import jwt

from datetime import timedelta, datetime
from typing import Optional, Any

from jwt import InvalidSignatureError, DecodeError
from passlib.context import CryptContext

from src.exceptions import UserAlreadyExistsException
from src.repositories.auth_repository import AuthRepository
from src.schemas.user import UserCreate


ACCESS_TOKEN_EXPIRE_MINUTES = 30
ALGORITHM = "HS256"


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

auth_repository = AuthRepository()


def register_user(username: str, password: str) -> None:
    user = auth_repository.get_user(username)
    if user is not None:
        raise UserAlreadyExistsException()
    hashed_password = pwd_context.hash(password)
    user = UserCreate(username=username, password=hashed_password)
    auth_repository.create_user(user)


def verify_token(token: str) -> Optional[dict[str, Any]]:
    try:
        return jwt.decode(token, _get_secret_key(), algorithms=[ALGORITHM])
    except (InvalidSignatureError, DecodeError):
        return None


def login(username: str, password: str) -> Optional[str]:
    if _authenticate_user(username, password):
        return _create_access_token({"sub": username})
    return None


def _authenticate_user(username: str, password: str) -> bool:
    user = auth_repository.get_user(username)
    if not user:
        return False
    return _verify_password(password, str(user.hashed_password))


def _verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


def _create_access_token(data: dict[str, Any]) -> str:
    to_encode = data.copy()
    expire = datetime.now() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, _get_secret_key(), algorithm=ALGORITHM)
    return encoded_jwt


def _get_secret_key() -> Optional[str]:
    return os.getenv("JWT_ENCODING_SECRET_KEY")
