from fastapi.testclient import TestClient
from uuid import UUID

from main import app

client = TestClient(app)


def test_register_user(test_user):
    response = client.post("/api/v1/users/register", json=test_user)
    assert response.status_code == 201
    assert response.json()["username"] == test_user.username

    assert "id" in response.json()
    assert "login" in response.json()
    assert "created_at" in response.json()
    assert "updated_at" in response.json()


def test_get_me():
    response = client.get("/api/v1/users/me")
    assert response.status_code == 200
    assert "login" in response.json()


def test_get_user(test_user):
    user_id = UUID("12345678-1234-5678-1234-567812345678")
    response = client.get(f"/api/v1/users/{user_id}")
    assert response.status_code == 200
    assert response.json()['login'] == test_user.login


def test_update_user(test_user_update):
    user_id = UUID("12345678-1234-5678-1234-567812345678")
    response = client.post(f"/api/v1/users/{user_id}", json=test_user_update)
    assert response.status_code == 200
    assert response.json()["login"] == test_user_update.username


def test_user_login_history():
    user_id = UUID("12345678-1234-5678-1234-567812345678")
    response = client.get(f"/api/v1/users/{user_id}/login_history")
    assert response.status_code == 200
    assert isinstance(response.json(), list)
    assert len(response.json()) >= 0
    assert "timestamp" in response.json()[0]

    if len(response.json()) > 0:
        assert "id" in response.json()[0]
        assert "user_id" in response.json()[0]
        assert "timestamp" in response.json()[0]


def test_register_user_invalid_data():
    invalid_user = {
        "username": "testuser",
        "password": "test"
    }
    response = client.post("/api/v1/users/register", json=invalid_user)
    assert response.status_code == 422


def test_get_user_not_found():
    user_id = UUID("00000000-0000-0000-0000-000000000000")
    response = client.get(f"/api/v1/users/{user_id}")
    assert response.status_code == 404


def test_update_user_not_found(test_user_update):
    user_id = UUID("00000000-0000-0000-0000-000000000000")
    response = client.post(f"/api/v1/users/{user_id}", json=test_user_update)
    assert response.status_code == 404


def test_user_login_history_empty():
    user_id = UUID("12345678-1234-5678-1234-567812345678")
    response = client.get(f"/api/v1/users/{user_id}/login_history")
    assert response.status_code == 200
    assert isinstance(response.json(), list)
    assert len(response.json()) == 0
