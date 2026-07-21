import time
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)


def test_create_item():
    """Test creating an item via API."""
    response = client.post(
        "/items/",
        json={"name": "Test Item", "quantity": 2.0, "unit": "kg"}
    )
    assert response.status_code == 201
    data = response.json()
    assert data["name"] == "Test Item"
    assert data["quantity"] == 2.0
    assert data["unit"] == "kg"
    assert "id" in data
    assert data["created_at"] is not None
    assert data["updated_at"] is not None


def test_get_items():
    """Test getting all items via API."""
    client.post("/items/", json={"name": "List Test",
                "quantity": 1.0, "unit": "pcs"})

    get_response = client.get("/items/")
    assert get_response.status_code == 200
    data = get_response.json()
    assert isinstance(data, list)
    assert len(data) >= 1


def test_get_item_by_id():
    """Test getting all items via API."""
    create_response = client.post(
        "/items/",
        json={"name": "Get Test", "quantity": 3.0, "unit": "L"}
    )
    item_id = create_response.json()["id"]

    get_response = client.get(f"/items/{item_id}")
    assert get_response.status_code == 200
    data = get_response.json()
    assert data["name"] == "Get Test"
    assert data["quantity"] == 3.0
    assert data["unit"] == "L"
    assert data["created_at"] is not None
    assert data["updated_at"] is not None


def test_get_item_not_found():
    """Test getting a non-existent item returns 404."""
    response = client.get("/items/99999")
    assert response.status_code == 404
    assert "not found" in response.json()["detail"]


def test_update_item():
    """Test updating an item via API."""
    create_response = client.post(
        "/items/",
        json={"name": "Update Test", "quantity": 1.0, "unit": "pcs"}
    )
    item_id = create_response.json()["id"]

    # Give it at least a ms, since it works with in-memory database
    time.sleep(0.001)
    update_response = client.put(
        f"/items/{item_id}",
        json={"name": "Updated Name", "quantity": 5.0}
    )
    assert update_response.status_code == 200
    data = update_response.json()
    assert data["name"] == "Updated Name"
    assert data["quantity"] == 5.0
    assert data["unit"] == "pcs"
    assert data["updated_at"] >= data["created_at"]


def test_delete_item():
    """Test deleting an item via API."""
    create_response = client.post(
        "/items/",
        json={"name": "Delete Test", "quantity": 1.0, "unit": "pcs"}
    )
    item_id = create_response.json()["id"]

    delete_response = client.delete(f"/items/{item_id}")
    assert delete_response.status_code == 204

    get_response = client.get(f"/items/{item_id}")
    assert get_response.status_code == 404


def test_delete_item_not_found():
    """Test deleting a non-existent item returns 404."""
    response = client.delete("/items/99999")
    assert response.status_code == 404
