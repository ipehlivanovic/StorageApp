import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.models import Base
from app.schemas import ItemCreate, ItemUpdate
from app.crud import create_item, update_item, get_item, get_items, delete_item


@pytest.fixture(scope="function")
def db():
    """Provide a database session for testing."""
    # ✅ Create engine and tables inside the fixture
    engine = create_engine(
        "sqlite:///:memory:",
        connect_args={"check_same_thread": False}
    )
    Base.metadata.create_all(bind=engine)
    
    TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.rollback()
        db.close()


def test_create_item(db):
    """Test creating a new item."""
    item_data = ItemCreate(name="Test Create Item", quantity=1, unit="kg")
    item = create_item(db, item_data)

    assert item.id is not None
    assert item.name == "Test Create Item"
    assert item.quantity == 1
    assert item.unit == "kg"
    assert item.created_at is not None
    assert item.updated_at is not None


def test_get_item(db):
    """Test retrieving an item by ID."""
    item_data = ItemCreate(name="Test Get Item", quantity=2, unit="piece")
    created = create_item(db, item_data)

    retrieved = get_item(db, created.id)

    assert retrieved.id == created.id
    assert retrieved.name == "Test Get Item"


def test_get_item_not_found(db):
    """Test retrieving a non-existent item returns None."""
    item = get_item(db, 9999)

    assert item is None


def test_get_items(db):
    """Test retrieving all items"""
    for i in range(3):
        item_data = ItemCreate(
            name=f"Item {i}", quantity=float(i+1), unit="pcs")
        create_item(db, item_data)

    items = get_items(db)

    assert len(items) >= 3

    # Clean up (delete all test items)
    for item in items:
        if "Item" in item.name:
            db.delete(item)
    db.commit()


def test_update_item(db):
    """Test updating an existing item."""
    item_data = ItemCreate(name="Test Update Item", quantity=1, unit="can")
    update_data = ItemUpdate(name="Updated Data", quantity=3, unit="cans")

    created = create_item(db, item_data)
    updated = update_item(db, created.id, update_data)

    assert updated.name == "Updated Data"
    assert updated.quantity == 3
    assert updated.unit == "cans"
    assert updated.id == created.id


def test_update_item_partial(db):
    """Test updating only some fields of an item."""
    item_data = ItemCreate(name="Test Update Item", quantity=10, unit="bottle")
    update_data = ItemUpdate(name="Partially Updated Data")

    created = create_item(db, item_data)
    updated = update_item(db, created.id, update_data)

    assert updated.name == "Partially Updated Data"
    assert updated.quantity == 10
    assert updated.unit == "bottle"
    assert updated.id == created.id


def test_update_item_not_found(db):
    """Test updating a non-existent item returns None."""
    update_data = ItemUpdate(name="New Name")
    item = update_item(db, 99999, update_data)
    assert item is None


def test_delete_item(db):
    """Test deleting an item."""
    # Create an item
    item_data = ItemCreate(name="Delete Test", quantity=1.0, unit="pcs")
    created = create_item(db, item_data)

    # Delete it
    success = delete_item(db, created.id)
    assert success is True

    # Verify it's gone
    deleted = get_item(db, created.id)
    assert deleted is None


def test_delete_item_not_found(db):
    """Test deleting a non-existent item returns False."""
    success = delete_item(db, 99999)
    assert success is False
