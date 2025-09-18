# tests/test_auth.py
import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.database import Base, engine

# Setup test client
client = TestClient(app)

# Fixture to create a fresh test DB
@pytest.fixture(autouse=True, scope="module")
def setup_db():
    # Drop all tables if they exist, then create fresh tables
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)


def test_register_user():
    response = client.post(
        "/api/auth/register",  # matches main.py route
        json={"username": "testuser", "password": "testpass"}
    )
    assert response.status_code == 200
    data = response.json()
    assert data["username"] == "testuser"
    assert "id" in data


def test_login_user():
    response = client.post(
        "/api/auth/login",  # matches main.py route
        json={"username": "testuser", "password": "testpass"}  # JSON payload for FastAPI
    )
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"
