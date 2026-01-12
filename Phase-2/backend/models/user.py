from sqlmodel import SQLModel, Field, Relationship
from typing import TYPE_CHECKING, Optional, List
import uuid
from datetime import datetime
from pydantic import validator
import bcrypt

if TYPE_CHECKING:
    from models.task import Task

class UserBase(SQLModel):
    email: str = Field(unique=True, index=True)
    username: str = Field(unique=True, index=True)
    full_name: Optional[str] = Field(default=None)

class User(UserBase, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    email: str = Field(unique=True, index=True)
    username: str = Field(unique=True, index=True)
    full_name: Optional[str] = Field(default=None)
    hashed_password: str
    is_active: bool = Field(default=True)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    # Relationship to tasks
    tasks: List["Task"] = Relationship(back_populates="owner", sa_relationship_kwargs={"lazy": "select"})

    def verify_password(self, plain_password: str) -> bool:
        password_bytes = plain_password.encode('utf-8')[:72]
        return bcrypt.checkpw(password_bytes, self.hashed_password.encode('utf-8'))

class UserCreate(UserBase):
    password: str

    @validator('password')
    def validate_password(cls, v):
        if len(v) < 6:
            raise ValueError('Password must be at least 6 characters long')
        return v

class UserRead(UserBase):
    id: uuid.UUID
    created_at: datetime
    updated_at: datetime

class UserUpdate(SQLModel):
    email: Optional[str] = None
    username: Optional[str] = None
    full_name: Optional[str] = None

class UserLogin(SQLModel):
    email: str
    password: str

def get_password_hash(password: str) -> str:
    """Hash a password using bcrypt with automatic salt generation."""
    # Truncate to 72 bytes (bcrypt limitation)
    password_bytes = password.encode('utf-8')[:72]
    salt = bcrypt.gensalt()
    return bcrypt.hashpw(password_bytes, salt).decode('utf-8')

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify a password against a hash."""
    password_bytes = plain_password.encode('utf-8')[:72]
    return bcrypt.checkpw(password_bytes, hashed_password.encode('utf-8'))