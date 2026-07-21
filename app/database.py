import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# Create the engine
DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "sqlite:///./storage.db"  # Default: real database file
)

engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False}
)

# Establish a Local connection
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Create a Base class for the models to inherit
Base = declarative_base()


def get_db():
    """Encapsulate a database session, close when done"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
