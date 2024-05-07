from os import path
from random import choice
from string import ascii_letters

import pytest
import requests


@pytest.fixture(scope="module")
def base_url():
    return "http://localhost:8000"


@pytest.fixture
def user_credentials():
    return {"username": "".join(choice(ascii_letters) for _ in range(10)), "password": "testpassword"}


def test_session_journey_happy_path(base_url, user_credentials):

    # Step 1: Register a new user
    registration_response = requests.post(
        f"{base_url}/auth/register",
        data=user_credentials,
        headers={"Content-Type": "application/x-www-form-urlencoded"},
    )
    assert registration_response.status_code == 200

    # Step 2: Login with the registered user credentials to obtain an access token
    login_response = requests.post(f"{base_url}/auth/token", data=user_credentials)
    assert login_response.status_code == 200
    access_token = login_response.json().get("access_token")
    assert access_token is not None

    # Step 3: Use the access token to start a session
    session_response = requests.post(f"{base_url}/sessions", headers={"Authorization": f"Bearer {access_token}"})
    assert session_response.status_code == 200
    session_data = session_response.json()
    assert "id" in session_data
    assert "status" in session_data
    assert session_data["status"] == "STARTED"

    # Step 4: Upload image to session
    file_name = "img1.jpg"
    fixtures_dir = path.join(path.dirname(path.abspath(__file__)), "fixtures")
    file_path = path.join(fixtures_dir, file_name)
    session_id = session_data["id"]
    with open(file_path, "rb") as file:
        image_data = file.read()
    image_file = (file_name, image_data)
    image_response = requests.post(
        f"{base_url}/sessions/{session_id}/images",
        headers={"Authorization": f"Bearer {access_token}"},
        files={"file": image_file},
    )
    image_data = image_response.json()
    assert image_response.status_code == 200
    assert "file_name" in image_data
    assert "id" in image_data
    assert image_data["file_name"] == "img1.jpg"
