from sqlmodel import SQLModel, Field
from typing import Optional
from datetime import datetime
import uuid


class TaskBase(SQLModel):
    title: str = Field(min_length=1)
    description: Optional[str] = None
    status: str = Field(default="pending")
    user_id: str


class Task(TaskBase, table=True):
    id: Optional[str] = Field(default_factory=lambda: str(uuid.uuid4()), primary_key=True)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)


class TaskRead(TaskBase):
    id: str
    created_at: datetime
    updated_at: datetime