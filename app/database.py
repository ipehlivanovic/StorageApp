from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# Create the engine
SQLALCHEMY_DATABASE_URL = "sqlite:///./storage.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={
                       "check_same_thread": False})

# Establish a Local connection
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Create a Base class for the models to inherit
Base = declarative_base()

# Encapsulate a database session, close when done


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
