import pytest
from unittest.mock import Mock, patch
from datetime import datetime
from app.models.task import Task
from app.schemas.task import CreateTaskRequest, UpdateTaskRequest
from app.services.task_service import TaskService
from app.utils.exceptions import TaskNotFoundException, UnauthorizedAccessException


def test_create_task():
    """Test creating a task."""
    session_mock = Mock()
    user_id = "user123"
    task_data = CreateTaskRequest(title="Test Task", description="Test Description")

    # Create a mock task to return
    mock_task = Task(
        id="task123",
        title="Test Task",
        description="Test Description",
        status="pending",
        user_id=user_id
    )

    with patch.object(session_mock, 'add'), \
         patch.object(session_mock, 'commit'), \
         patch.object(session_mock, 'refresh', side_effect=lambda obj: setattr(obj, 'id', 'task123')):
        result = TaskService.create_task(session_mock, user_id, task_data)

        # Verify the task was created with correct data
        assert result.title == "Test Task"
        assert result.description == "Test Description"
        assert result.user_id == user_id
        assert result.status == "pending"
        assert session_mock.add.called
        assert session_mock.commit.called


def test_get_tasks_by_user():
    """Test getting tasks by user."""
    session_mock = Mock()
    user_id = "user123"

    # Mock tasks to return
    mock_tasks = [
        Task(id="task1", title="Task 1", user_id=user_id, status="pending"),
        Task(id="task2", title="Task 2", user_id=user_id, status="completed")
    ]

    with patch.object(session_mock, 'exec', return_value=Mock()) as exec_mock:
        exec_mock.return_value.all.return_value = mock_tasks

        result = TaskService.get_tasks_by_user(session_mock, user_id)

        # Verify the result
        assert len(result) == 2
        assert result[0].title == "Task 1"
        assert result[1].title == "Task 2"


def test_get_task_by_id_and_user_found():
    """Test getting a task by ID and user when it exists."""
    session_mock = Mock()
    task_id = "task123"
    user_id = "user123"

    mock_task = Task(id=task_id, title="Test Task", user_id=user_id, status="pending")

    with patch.object(session_mock, 'exec', return_value=Mock()) as exec_mock:
        exec_mock.return_value.first.return_value = mock_task

        result = TaskService.get_task_by_id_and_user(session_mock, task_id, user_id)

        assert result.id == task_id
        assert result.user_id == user_id


def test_get_task_by_id_and_user_not_found():
    """Test getting a task by ID and user when it doesn't exist."""
    session_mock = Mock()
    task_id = "task123"
    user_id = "user123"

    with patch.object(session_mock, 'exec', return_value=Mock()) as exec_mock:
        exec_mock.return_value.first.return_value = None

        with pytest.raises(TaskNotFoundException):
            TaskService.get_task_by_id_and_user(session_mock, task_id, user_id)


def test_update_task_by_id():
    """Test updating a task by ID."""
    session_mock = Mock()
    task_id = "task123"
    user_id = "user123"
    update_data = UpdateTaskRequest(title="Updated Title", description="Updated Description")

    original_task = Task(id=task_id, title="Original Title", description="Original Description",
                         user_id=user_id, status="pending")

    with patch('src.services.task_service.TaskService.get_task_by_id_and_user', return_value=original_task):
        result = TaskService.update_task_by_id(session_mock, task_id, user_id, update_data)

        # Verify the task was updated
        assert result.title == "Updated Title"
        assert result.description == "Updated Description"
        assert session_mock.add.called
        assert session_mock.commit.called


def test_delete_task_by_id():
    """Test deleting a task by ID."""
    session_mock = Mock()
    task_id = "task123"
    user_id = "user123"

    mock_task = Task(id=task_id, title="Test Task", user_id=user_id, status="pending")

    with patch('src.services.task_service.TaskService.get_task_by_id_and_user', return_value=mock_task):
        result = TaskService.delete_task_by_id(session_mock, task_id, user_id)

        # Verify the task was deleted
        assert result is True
        session_mock.delete.assert_called_once_with(mock_task)
        assert session_mock.commit.called


def test_toggle_task_completion_pending_to_completed():
    """Test toggling task completion from pending to completed."""
    session_mock = Mock()
    task_id = "task123"
    user_id = "user123"

    original_task = Task(id=task_id, title="Test Task", user_id=user_id, status="pending")

    with patch('src.services.task_service.TaskService.get_task_by_id_and_user', return_value=original_task):
        result = TaskService.toggle_task_completion(session_mock, task_id, user_id)

        # Verify the task status was toggled
        assert result.status == "completed"
        assert session_mock.add.called
        assert session_mock.commit.called


def test_toggle_task_completion_completed_to_pending():
    """Test toggling task completion from completed to pending."""
    session_mock = Mock()
    task_id = "task123"
    user_id = "user123"

    original_task = Task(id=task_id, title="Test Task", user_id=user_id, status="completed")

    with patch('src.services.task_service.TaskService.get_task_by_id_and_user', return_value=original_task):
        result = TaskService.toggle_task_completion(session_mock, task_id, user_id)

        # Verify the task status was toggled
        assert result.status == "pending"
        assert session_mock.add.called
        assert session_mock.commit.called