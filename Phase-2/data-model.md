# Data Model - Hackathon II Todo App

## Entities

### User Entity
- **Primary Key**: `id: UUID` (auto-generated)
- **Attributes**:
  - `email: string` (unique, required, valid email format)
  - `username: string` (unique, required, 3-50 characters)
  - `full_name: string` (optional)
  - `hashed_password: string` (required, BCrypt hashed)
  - `is_active: boolean` (default: true)
  - `created_at: datetime` (auto-generated)
  - `updated_at: datetime` (auto-generated)

- **Relationships**:
  - One-to-many with Task (user.tasks)

### Task Entity
- **Primary Key**: `id: UUID` (auto-generated)
- **Attributes**:
  - `user_id: UUID` (foreign key to User, required)
  - `title: string` (required, 1-200 characters)
  - `description: string` (optional, max 1000 characters)
  - `status: enum` (values: 'pending', 'in-progress', 'completed'; default: 'pending')
  - `priority: enum` (values: 'low', 'medium', 'high'; default: 'medium')
  - `due_date: datetime` (optional)
  - `completed_at: datetime` (optional)
  - `created_at: datetime` (auto-generated)
  - `updated_at: datetime` (auto-generated)

- **Relationships**:
  - Many-to-one with User (task.owner)

## Validation Rules

### User Validation
- Email: Must be valid email format
- Username: 3-50 alphanumeric characters plus underscores/hyphens
- Password: Minimum 6 characters (hashed before storage)
- All fields required unless noted as optional

### Task Validation
- Title: 1-200 characters
- Description: Max 1000 characters
- Status: Must be one of allowed values
- Priority: Must be one of allowed values
- Due date: Must be future date if provided

## Indexes

### Required Indexes
- `idx_users_email` on users(email)
- `idx_users_username` on users(username)
- `idx_tasks_user_id` on tasks(user_id)
- `idx_tasks_status` on tasks(status)
- `idx_tasks_priority` on tasks(priority)
- `idx_tasks_created_at` on tasks(created_at DESC)
- `idx_tasks_due_date` on tasks(due_date)

## Constraints

### Foreign Key Constraints
- `tasks.user_id` references `users.id` with CASCADE delete

### Check Constraints
- Task title length: 1-200 characters
- Task description length: <= 1000 characters
- Valid status values: 'pending', 'in-progress', 'completed'
- Valid priority values: 'low', 'medium', 'high'

## SQLModel Definitions

### User Model
```python
from sqlmodel import SQLModel, Field, Relationship
from typing import Optional, List
import uuid
from datetime import datetime

class UserBase(SQLModel):
    email: str = Field(unique=True, index=True)
    username: str = Field(unique=True, index=True)
    full_name: Optional[str] = Field(default=None)

class User(UserBase, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    hashed_password: str
    is_active: bool = Field(default=True)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    tasks: List["Task"] = Relationship(back_populates="owner")
```

### Task Model
```python
from sqlmodel import SQLModel, Field, Relationship
from typing import Optional
import uuid
from datetime import datetime
from enum import Enum

class TaskStatus(str, Enum):
    pending = "pending"
    in_progress = "in-progress"
    completed = "completed"

class TaskPriority(str, Enum):
    low = "low"
    medium = "medium"
    high = "high"

class TaskBase(SQLModel):
    title: str
    description: Optional[str] = None
    status: TaskStatus = Field(default=TaskStatus.pending)
    priority: TaskPriority = Field(default=TaskPriority.medium)
    due_date: Optional[datetime] = None

class Task(TaskBase, table=True):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    user_id: uuid.UUID = Field(foreign_key="user.id")

    completed_at: Optional[datetime] = None
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    owner: "User" = Relationship(back_populates="tasks")
```