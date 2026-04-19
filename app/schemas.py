from pydantic import BaseModel, field_validator
from datetime import datetime
from typing import Optional

class TaskBase(BaseModel):
    """Shared fields used across all task schemas."""
    title: str
    description: Optional[str] = None
    status: str = "todo"

    @field_validator("status")
    @classmethod
    def validate_status(cls, v):
        """Ensure status is either 'todo' or 'done'."""
        if v not in ("todo", "done"):
            raise ValueError("status must be 'todo' or 'done'")
        return v

class TaskCreate(TaskBase):
    """Schema for creating a new task. Requires a session_id."""
    session_id: str

class TaskUpdate(TaskBase):
    """Schema for updating an existing task."""
    pass

class TaskResponse(TaskBase):
    """Schema for returning task data in API responses."""
    id: int
    session_id: str
    created_at: datetime

    model_config = {"from_attributes": True}