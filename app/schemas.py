from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class TaskBase(BaseModel):
    title: str
    description: Optional[str] = None
    status: str = "todo"

class TaskCreate(TaskBase):
    session_id: str

class TaskUpdate(TaskBase):
    pass

class TaskResponse(TaskBase):
    id: int
    session_id: str
    created_at: datetime

    model_config = {"from_attributes": True}