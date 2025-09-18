# tests/test_sweets.py
import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.database import Base, engine

client = TestClient(app)

# Setup fresh DB for sweets tests
@pytest.fixture(autouse=True, scope="module")
def setup_db():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)


def test_create_sweet():
    payload = {"name": "Ladoo", "category": "Indian", "price": 10, "quantity": 50}
    response = client.post("/api/sweets", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "Ladoo"
    assert data["category"] == "Indian"
    assert "id" in data


def test_list_sweets():
    response = client.get("/api/sweets")
    assert response.status_code == 200
    data = response.json()
    assert len(data) >= 1  # at least the one created
    assert data[0]["name"] == "Ladoo"


def test_get_sweet():
    # Assuming first sweet has ID 1
    response = client.get("/api/sweets/1")
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == 1
    assert data["name"] == "Ladoo"


def test_update_sweet():
    payload = {"name": "Gulab Jamun", "category": "Indian", "price": 12, "quantity": 40}
    response = client.put("/api/sweets/1", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "Gulab Jamun"
    assert data["quantity"] == 40


def test_search_sweets():
    # Search by name
    response = client.get("/api/sweets/search?name=Gulab")
    assert response.status_code == 200
    data = response.json()
    assert len(data) >= 1
    assert "Gulab" in data[0]["name"]

    # Search by category
    response = client.get("/api/sweets/search?category=Indian")
    assert response.status_code == 200
    data = response.json()
    assert len(data) >= 1
    assert data[0]["category"] == "Indian"


def test_delete_sweet():
    response = client.delete("/api/sweets/1")
    assert response.status_code == 200
    data = response.json()
    assert "message" in data
