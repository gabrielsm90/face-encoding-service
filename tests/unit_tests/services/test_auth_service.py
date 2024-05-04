from unittest.mock import patch

import jwt
import pytest

from src.exceptions import UserAlreadyExists
from src.models import User
from src.schemas.user import UserCreate
from src.services.auth_service import (
    register_user,
    login,
    verify_token,
    SECRET_KEY,
    ALGORITHM,
    auth_repository,
    pwd_context,
)


@pytest.fixture
def user():
    return User(username="test_user", hashed_password="$2b$12$ICGZngNZaNfhYKx1UQfYf.UkoaXX/O673htEkJSACp4pKSE0mjxua")


# todo parametrize these
@patch.object(auth_repository, "get_user")
def test_login_when_credentials_match_returns_access_token(mocked_get_user, user):
    username = "test_user"
    password = "test_password"
    mocked_get_user.return_value = user

    result = login(username, password)

    assert result is not None


@patch.object(auth_repository, "get_user")
def test_login_when_user_doesnt_exist_returns_none(mocked_get_user):
    username = "invalid_user"
    password = "test_password"
    mocked_get_user.return_value = None

    result = login(username, password)

    assert result is None


@patch.object(auth_repository, "get_user")
def test_login_when_password_is_invalid_returns_none(mocked_get_user, user):
    username = "test_user"
    password = "invalid_password"
    mocked_get_user.return_value = user

    result = login(username, password)

    assert result is None


def test_verify_token_when_token_is_valid_returns_payload():
    to_encode = {"foo": "bar"}
    token = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

    result = verify_token(token)

    assert result == to_encode


def test_verify_token_when_token_is_not_valid_returns_none():
    to_encode = {"foo": "bar"}
    token = jwt.encode(to_encode, "INVALID_SECRET_KEY", algorithm=ALGORITHM)

    result = verify_token(token)

    assert result is None


@patch.object(auth_repository, "get_user")
@patch.object(auth_repository, "create_user")
@patch.object(pwd_context, "hash")
def test_register_user_when_new_username_adds_new_user(mock_hash, mock_create_user, mock_get_user):
    mock_get_user.return_value = None
    mock_hash.return_value = "hashed_password"

    register_user("new_user_name", "new_password")

    mock_create_user.assert_called_once_with(UserCreate(username="new_user_name", password="hashed_password"))


@patch.object(auth_repository, "get_user")
def test_register_user_when_user_exists_throws_exception(_):
    with pytest.raises(UserAlreadyExists):
        register_user("existing_user_name", "new_password")
