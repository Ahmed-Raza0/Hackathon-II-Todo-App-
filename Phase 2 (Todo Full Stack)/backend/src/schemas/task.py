from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class TaskBase(BaseModel):
    title: str
    description: Optional[str] = None
    status: str = "pending"


class CreateTaskRequest(TaskBase):
    title: str


class UpdateTaskRequest(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None


class TaskResponse(TaskBase):
    id: str
    user_id: str
    created_at: datetime
    updated_at: datetime