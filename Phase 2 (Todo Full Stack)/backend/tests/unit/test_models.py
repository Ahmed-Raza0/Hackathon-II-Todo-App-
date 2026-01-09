import pytest
from datetime import datetime
from app.models.task import Task, TaskBase


def test_task_creation():
    """Test creating a Task instance."""
    task_data = {
        "title": "Test Task",
        "description": "Test Description",
        "status": "pending",
        "user_id": "user123"
    }

    task = Task(**task_data)

    assert task.title == "Test Task"
    assert task.description == "Test Description"
    assert task.status == "pending"
    assert task.user_id == "user123"
    assert task.id is not None  # UUID should be auto-generated
    assert isinstance(task.created_at, datetime)
    assert isinstance(task.updated_at, datetime)


def test_task_base_creation():
    """Test creating a TaskBase instance."""
    task_base_data = {
        "title": "Test Task",
        "description": "Test Description",
        "status": "completed",
        "user_id": "user123"
    }

    task_base = TaskBase(**task_base_data)

    assert task_base.title == "Test Task"
    assert task_base.description == "Test Description"
    assert task_base.status == "completed"
    assert task_base.user_id == "user123"


def test_task_title_required():
    """Test that title is required."""
    with pytest.raises(ValueError):
        TaskBase(title="", description="Test", status="pending", user_id="user123")


def test_task_status_default():
    """Test that status defaults to 'pending'."""
    task_base = TaskBase(title="Test Task", description="Test", user_id="user123")
    assert task_base.status == "pending"