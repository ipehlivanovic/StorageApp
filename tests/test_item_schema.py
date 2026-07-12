import pytest
from datetime import datetime
from pydantic import ValidationError
from app.schemas import ItemBase, ItemCreate, ItemUpdate, Item


this_moment = datetime.now()
# --------------------------
# Tests for ItemBase
# --------------------------


def test_item_base_valid():
    """Test that ItemBase works with valid data."""
    item = ItemBase(
        name="Apple",
        quantity=1,
        unit="kg"
    )

    assert item.name == "Apple"
    assert item.quantity == 1.0
    assert item.unit == "kg"


def test_item_base_invalid_empty_name():
    """Test that ItemBase rejects empty name."""
    with pytest.raises(ValidationError) as exc_info:
        ItemBase(name="", quantity=2.0, unit="pcs")
    assert "name" in str(exc_info.value)


def test_item_base_invalid_quantity_value():
    """Test that ItemBase rejects invalid quantity."""
    with pytest.raises(ValidationError) as exc_info:
        ItemBase(name="Tomato", quantity=0, unit="cans")
    assert "quantity" in str(exc_info.value)


def test_item_base_invalid_empty_unit():
    """Test that ItemBase rejects empty unit."""
    with pytest.raises(ValidationError) as exc_info:
        ItemBase(name="Peach", quantity=3, unit="")
    assert "unit" in str(exc_info.value)


def test_item_base_missing_mandatory_name():
    """Test that ItemBase rejects missing name."""
    with pytest.raises(ValidationError) as exc_info:
        ItemBase(quantity=3.5, unit="liters")
    assert "name" in str(exc_info.value)


def test_item_base_missing_mandatory_quantity():
    """Test that ItemBase rejects missing quantity."""
    with pytest.raises(ValidationError) as exc_info:
        ItemBase(name="Pineapple", unit="kg")
    assert "quantity" in str(exc_info.value)


def test_item_base_missing_mandatory_unit():
    """Test that ItemBase rejects missing unit."""
    with pytest.raises(ValidationError) as exc_info:
        ItemBase(name="Watermellon", quantity=1)
    assert "unit" in str(exc_info.value)


# --------------------------
# Tests for ItemCreate
# --------------------------

def test_item_create_valid():
    """Test that ItemCreate works with valid data."""
    item = ItemCreate(
        name="Potato Chips",
        quantity=2,
        unit="bags"
    )

    assert item.name == "Potato Chips"
    assert item.quantity == 2.0
    assert item.unit == "bags"


def test_item_create_invalid_empty_name():
    """Test that ItemCreate rejects empty name."""
    with pytest.raises(ValidationError) as exc_info:
        ItemCreate(name="", quantity=5.0, unit="grams")
    assert "name" in str(exc_info.value)


def test_item_create_invalid_quantity_value():
    """Test that ItemCreate rejects empty unit."""
    with pytest.raises(ValidationError) as exc_info:
        ItemCreate(name="Letuce", quantity=0, unit="piece")
    assert "quantity" in str(exc_info.value)


def test_item_create_invalid_empty_unit():
    """Test that ItemCreate rejects empty unit."""
    with pytest.raises(ValidationError) as exc_info:
        ItemCreate(name="Potato", quantity=4.0, unit="")
    assert "unit" in str(exc_info.value)


def test_item_create_missing_mandatory_name():
    """Test that ItemCreate rejects missing name."""
    with pytest.raises(ValidationError) as exc_info:
        ItemCreate(quantity=6.5, unit="kg")
    assert "name" in str(exc_info.value)


def test_item_create_missing_mandatory_quantity():
    """Test that ItemCreate rejects missing quantity."""
    with pytest.raises(ValidationError) as exc_info:
        ItemCreate(name="Celery", unit="pack")
    assert "quantity" in str(exc_info.value)


def test_item_create_missing_mandatory_unit():
    """Test that ItemCreate rejects missing unit."""
    with pytest.raises(ValidationError) as exc_info:
        ItemCreate(name="Onion", quantity=1)
    assert "unit" in str(exc_info.value)

# --------------------------
# Tests for ItemUpdate
# --------------------------


def test_item_update_valid_all():
    """Test that ItemUpdate works with valid data."""
    item = ItemUpdate(
        name="Juice",
        quantity=1.5,
        unit="l"
    )

    assert item.name == "Juice"
    assert item.quantity == 1.5
    assert item.unit == "l"


def test_item_update_invalid_empty_name():
    """Test that ItemUpdate rejects empty name."""
    with pytest.raises(ValidationError) as exc_info:
        ItemUpdate(name="", quantity=2.0, unit="pcs")
    assert "name" in str(exc_info.value)


def test_item_update_invalid_quantity_value():
    """Test that ItemUpdate rejects invalid quantity."""
    with pytest.raises(ValidationError) as exc_info:
        ItemUpdate(name="Soda", quantity=0, unit="cans")
    assert "quantity" in str(exc_info.value)


def test_item_update_invalid_empty_unit():
    """Test that ItemUpdate rejects empty unit."""
    with pytest.raises(ValidationError) as exc_info:
        ItemUpdate(name="Sunflower oil", quantity=3.0, unit="")
    assert "unit" in str(exc_info.value)


def test_item_update_missing_name():
    """Test that ItemUpdate accepts missing name."""
    item = ItemUpdate(
        quantity=2.0,
        unit="kg"
    )

    assert item.name == None
    assert item.quantity == 2.0
    assert item.unit == "kg"


def test_item_update_missing_quantity():
    """Test that ItemUpdate accepts missing quantity."""
    item = ItemUpdate(
        name="Coconut water",
        unit="ml"
    )

    assert item.name == "Coconut water"
    assert item.quantity == None
    assert item.unit == "ml"


def test_item_update_missing_unit():
    """Test that ItemUpdate accepts missing unit."""
    item = ItemUpdate(
        name="Beer",
        quantity=0.5
    )

    assert item.name == "Beer"
    assert item.quantity == 0.5
    assert item.unit == None


def test_item_update_no_change():
    """Test that ItemUpdate accepts missing information."""
    item = ItemUpdate()

    assert item.name == None
    assert item.quantity == None
    assert item.unit == None

# --------------------------
# Tests for Item
# --------------------------


def test_item_valid():
    """Test that Item works with valid data."""
    item = Item(
        id=1,
        name="Tuna",
        quantity=2.0,
        unit="can",
        created_at=this_moment,
        updated_at=this_moment
    )

    assert item.id == 1
    assert item.name == "Tuna"
    assert item.quantity == 2.0
    assert item.unit == "can"
    assert isinstance(item.created_at, datetime)
    assert item.created_at == this_moment
    assert isinstance(item.updated_at, datetime)
    assert item.updated_at == this_moment


def test_item_invalid_empty_name():
    """Test that Item rejects empty name."""
    with pytest.raises(ValidationError) as exc_info:
        Item(
            id=2,
            name="",
            quantity=2.0,
            unit="pcs",
            created_at=this_moment,
            updated_at=this_moment)
    assert "name" in str(exc_info.value)


def test_item_invalid_quantity_value():
    """Test that Item rejects invalid quantity."""
    with pytest.raises(ValidationError) as exc_info:
        Item(
            id=3,
            name="Jam",
            quantity=0,
            unit="jar",
            created_at=this_moment,
            updated_at=this_moment)
    assert "quantity" in str(exc_info.value)


def test_item_invalid_empty_unit():
    """Test that Item rejects empty unit."""
    with pytest.raises(ValidationError) as exc_info:
        Item(
            id=4,
            name="Gum",
            quantity=10.0,
            unit="",
            created_at=this_moment,
            updated_at=this_moment)
    assert "unit" in str(exc_info.value)


def test_item_missing_mandatory_id():
    """Test that Item rejects missing id."""
    with pytest.raises(ValidationError) as exc_info:
        Item(
            name="Honey",
            quantity=3.0,
            unit="jar",
            created_at=this_moment,
            updated_at=this_moment)
    assert "id" in str(exc_info.value)


def test_item_missing_mandatory_name():
    """Test that Item rejects missing name."""
    with pytest.raises(ValidationError) as exc_info:
        Item(
            id=5,
            quantity=2.0,
            unit="pcs",
            created_at=this_moment,
            updated_at=this_moment)
    assert "name" in str(exc_info.value)


def test_item_missing_mandatory_quantity():
    """Test that Item rejects missing quantity."""
    with pytest.raises(ValidationError) as exc_info:
        Item(
            id=6,
            name="Mustard",
            unit="tube",
            created_at=this_moment,
            updated_at=this_moment)
    assert "quantity" in str(exc_info.value)


def test_item_missing_mandatory_unit():
    """Test that Item rejects missing unit."""
    with pytest.raises(ValidationError) as exc_info:
        Item(
            id=7,
            name="Chicken",
            quantity=2.0,
            created_at=this_moment,
            updated_at=this_moment)
    assert "unit" in str(exc_info.value)


def test_item_missing_mandatory_created_at():
    """Test that Item rejects missing created_at."""
    with pytest.raises(ValidationError) as exc_info:
        Item(
            id=8,
            name="Fish oil",
            quantity=0.5,
            unit="l",
            updated_at=this_moment)
    assert "created_at" in str(exc_info.value)


def test_item_missing_mandatory_updated_at():
    """Test that Item rejects missing updated_at."""
    with pytest.raises(ValidationError) as exc_info:
        Item(
            id=9,
            name="Leek",
            quantity=500,
            unit="grams",
            created_at=this_moment)
    assert "updated_at" in str(exc_info.value)
