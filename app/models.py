from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.sql import func
from app.database import Base

class Task(Base):
    """
    Represents a task in the database.
    Each task belongs to a session, allowing multi-user isolation.
    """
    __tablename__ = "tasks"

    id = Column(Integer, primary_key=True, index=True)  # Auto-incrementing unique ID
    session_id = Column(String, nullable=False, index=True)  # Links task to a user session
    title = Column(String, nullable=False)  # Required task title
    description = Column(String, nullable=True)  # Optional task description
    status = Column(String, default="todo")  # Either "todo" or "done"
    created_at = Column(DateTime(timezone=True), server_default=func.now())  # Auto-set on creation