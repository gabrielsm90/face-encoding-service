import pytest

from fastapi.testclient import TestClient

from src.app import app


@pytest.fixture
def client():
    return TestClient(app)


def test_root_endpoint_returns_200_status_code_and_welcome_message(client):
    response = client.get("/")

    assert response.status_code == 200
    assert response.json() == {"message": "Welcome to Veriff's Face Encoding Service!"}


def test_health_endpoint_returns_200_status_code_and_proper_content(client):
    response = client.get("/health")

    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_invalid_endpoint_returns_404_status_code(client):
    response = client.get("/invalid-path")

    assert response.status_code == 404
