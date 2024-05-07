from unittest.mock import patch

from src.exceptions import UserAlreadyExistsException


@patch("src.controllers.auth_controller.login", return_value="access-token")
def test_auth_token_endpoint_when_credentials_are_valid_returns_200_status_code_and_access_token(_, client):
    username = "test_user"
    password = "test_password"

    response = client.post("/auth/token", data={"username": username, "password": password})
    response_content = response.json()

    assert response.status_code == 200
    assert response_content.get("access_token") == "access-token"
    assert response_content.get("token_type") == "bearer"


@patch("src.controllers.auth_controller.login", return_value=None)
def test_auth_token_endpoint_when_credentials_are_invalid_returns_401_status_code(_, client):
    username = "invalid_user"
    password = "test_password"

    response = client.post("/auth/token", data={"username": username, "password": password})
    response_content = response.json()

    assert response.status_code == 401
    assert response_content.get("detail") == "Incorrect credentials"


@patch("src.controllers.auth_controller.register_user")
def test_auth_register_endpoint_when_user_name_is_valid_returns_200_status_code_and_success_message(_, client):
    username = "new_user"
    password = "my_new_password"

    response = client.post("/auth/register", data={"username": username, "password": password})
    response_content = response.json()

    assert response.status_code == 200
    assert response_content.get("message") == "User registered successfully"


@patch("src.controllers.auth_controller.register_user", side_effect=UserAlreadyExistsException)
def test_auth_register_endpoint_when_user_name_already_exists_returns_400_with_error_message(_, client):
    username = "existing_user"
    password = "my_password"

    response = client.post("/auth/register", data={"username": username, "password": password})
    response_content = response.json()

    assert response.status_code == 400
    assert response_content.get("detail") == "User already exists"
