from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# SQLite database file will be created in the root of the project
SQLALCHEMY_DATABASE_URL = "sqlite:///./tasks.db"

# Create the database engine
# check_same_thread is False because FastAPI runs on multiple threads
engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)

# Each instance of SessionLocal is a database session
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base class that all database models will inherit from
Base = declarative_base()

def get_db():
    """
    Dependency that provides a database session to each API endpoint.
    Automatically closes the session when the request is finished.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()