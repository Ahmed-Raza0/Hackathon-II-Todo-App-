from sqlmodel import SQLModel, Field, Column
from sqlalchemy import String
from sqlalchemy.dialects.postgresql import UUID
from typing import Optional
import uuid
from datetime import datetime
from pydantic import BaseModel


class UserBase(SQLModel):
    email: str = Field(unique=True, index=True)
    name: Optional[str] = Field(default=None)


class User(UserBase, table=True):
    __tablename__ = "users"

    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    email: str = Field(unique=True, index=True)
    name: Optional[str] = Field(default=None)
    hashed_password: str = Field(sa_column=Column(String, nullable=False))
    is_active: bool = Field(default=True)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)


class UserCreate(UserBase):
    password: str


class UserUpdate(SQLModel):
    name: Optional[str] = None
    email: Optional[str] = None


class UserPublic(UserBase):
    id: uuid.UUID
    created_at: datetime
    updated_at: datetime