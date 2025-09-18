# tests/test_inventory.py
import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.database import Base, engine

client = TestClient(app)

@pytest.fixture(autouse=True, scope="module")
def setup_db():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    # Create one sweet for inventory tests
    client.post("/api/sweets", json={"name": "Rasgulla", "category": "Indian", "price": 15, "quantity": 10})
    yield
    Base.metadata.drop_all(bind=engine)


def test_purchase_sweet():
    response = client.post("/api/sweets/1/purchase")
    assert response.status_code == 200
    data = response.json()
    assert "Purchased Rasgulla" in data["message"]

    # Check quantity decreased
    response = client.get("/api/sweets/1")
    data = response.json()
    assert data["quantity"] == 9


def test_purchase_sweet_out_of_stock():
    # Reduce quantity to 0
    for _ in range(9):
        client.post("/api/sweets/1/purchase")

    response = client.post("/api/sweets/1/purchase")
    assert response.status_code == 400
    data = response.json()
    assert data["detail"] == "Out of stock"


def test_restock_sweet():
    response = client.post("/api/sweets/1/restock", params={"amount": 5})
    assert response.status_code == 200
    data = response.json()
    assert "Restocked Rasgulla" in data["message"]

    # Check quantity increased
    response = client.get("/api/sweets/1")
    data = response.json()
    assert data["quantity"] == 5  # 0 + 5
