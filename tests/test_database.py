import pytest
from sqlalchemy import inspect, text
from app.database import engine, SessionLocal, Base
from app.models import Item


def test_database_connection():
    """Test that we can connect to the database."""
    try:
        db = SessionLocal()
        db.execute(text("SELECT 1"))
        db.close()
        assert True
    except Exception as e:
        pytest.fail(f"Database connection failed: {e}")


def test_tables_created():
    """Test that the 'items' table exists."""
    inspector = inspect(engine)
    tables = inspector.get_table_names()
    assert "items" in tables, "'items' table not found in database"


def test_item_table_columns():
    """Test that the 'items' table has the correct columns."""
    inspector = inspect(engine)
    columns = inspector.get_columns("items")
    column_names = [col["name"] for col in columns]
    
    expected_columns = ["id", "name", "quantity", "unit", "created_at", "updated_at"]
    
    for expected in expected_columns:
        assert expected in column_names, f"Column '{expected}' not found in 'items' table"
    assert len(column_names) == len(expected_columns), f"Unexpected columns exist in the table"


def test_item_model_attributes():
    """Test that the Item model has the expected attributes."""
    # Check that the model exists
    assert hasattr(Item, "__tablename__"), "Item model missing __tablename__"
    assert Item.__tablename__ == "items", "Item table name should be 'items'"
    
    # Check that the model has the expected columns
    expected_columns = ["id", "name", "quantity", "unit", "created_at", "updated_at"]
    for column in expected_columns:
        assert hasattr(Item, column), f"Item model missing '{column}' attribute"
