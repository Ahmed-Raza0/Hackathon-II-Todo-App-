from sqlmodel import SQLModel, Field, Relationship
from sqlalchemy.dialects.postgresql import UUID
from typing import Optional
import uuid
from datetime import datetime
from .user import User
from sqlalchemy import String


class TaskBase(SQLModel):
    title: str = Field(min_length=1, max_length=200)
    description: Optional[str] = Field(default=None)
    completed: bool = Field(default=False)


class Task(TaskBase, table=True):
    __tablename__ = "tasks"

    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    title: str = Field(sa_column=Column(String(200), nullable=False))
    description: Optional[str] = Field(sa_column=Column(String, nullable=True))
    completed: bool = Field(default=False)
    user_id: uuid.UUID = Field(foreign_key="users.id", nullable=False)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    # Relationship to user
    user: User = Relationship(back_populates="tasks")


class TaskCreate(TaskBase):
    title: str
    pass


class TaskUpdate(SQLModel):
    title: Optional[str] = None
    description: Optional[str] = None
    completed: Optional[bool] = None


class TaskPublic(TaskBase):
    id: uuid.UUID
    user_id: uuid.UUID
    created_at: datetime
    updated_at: datetime


# Add relationship to User model
User.model_rebuild()