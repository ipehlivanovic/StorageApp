import pytest
from sqlalchemy import create_engine, inspect, text
from sqlalchemy.orm import sessionmaker
from app.models import Base, Item


@pytest.fixture(scope="function", autouse=True)
def setup_database():
    """Create a fresh in-memory database for each test."""
    # ✅ Create a brand new in-memory engine - NOT the real one!
    test_engine = create_engine(
        "sqlite:///:memory:",
        connect_args={"check_same_thread": False}
    )
    
    # ✅ Create tables in memory using the blueprint
    Base.metadata.create_all(bind=test_engine)
    
    # ✅ Store the engine so tests can access it
    pytest.test_engine = test_engine
    
    yield
    
    # ✅ No drop_all needed - in-memory database auto-destroys!
    # The database disappears when the connection closes

def test_database_connection():
    """Test that we can connect to the database."""
    try:
        TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=pytest.test_engine)
        db = TestingSessionLocal()
        db.execute(text("SELECT 1"))
        db.close()
        assert True
    except Exception as e:
        pytest.fail(f"Database connection failed: {e}")


def test_tables_created():
    """Test that the 'items' table exists."""
    inspector = inspect(pytest.test_engine)
    tables = inspector.get_table_names()
    assert "items" in tables, "'items' table not found in database"


def test_item_table_columns():
    """Test that the 'items' table has the correct columns."""
    inspector = inspect(pytest.test_engine)
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
