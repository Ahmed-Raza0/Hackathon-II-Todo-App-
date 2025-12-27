"""Task management business logic for Todo CLI Core application.

This module provides the TaskManager class for CRUD operations and validation,
along with custom exceptions for error handling.
"""

from datetime import datetime
from src.task import Task


class InvalidTaskError(Exception):
    """Raised when task validation fails (empty title, too long, etc.)."""

    pass


class TaskNotFoundError(Exception):
    """Raised when attempting to access a task that doesn't exist."""

    pass


class TaskManager:
    """Manages task storage, validation, and CRUD operations.

    This class maintains in-memory task storage using a dictionary for O(1)
    lookups and enforces all validation rules defined in the specification.

    Attributes:
        _tasks: Private dictionary mapping task IDs to Task objects.
        _next_id: Private counter for sequential task ID generation.
    """

    def __init__(self) -> None:
        """Initialize TaskManager with empty task storage."""
        self._tasks: dict[int, Task] = {}
        self._next_id: int = 1

    def add_task(self, title: str, description: str | None = None) -> Task:
        """Add a new task with validation.

        Args:
            title: Task title (1-200 characters, required).
            description: Optional task description (max 1000 characters).

        Returns:
            The newly created Task object.

        Raises:
            InvalidTaskError: If validation fails (empty title, too long, etc.).
        """
        # Validate title
        if not title or not title.strip():
            raise InvalidTaskError("Title cannot be empty")

        if len(title) > 200:
            raise InvalidTaskError("Title too long (max 200 characters)")

        # Validate description if provided
        if description is not None and len(description) > 1000:
            raise InvalidTaskError("Description too long (max 1000 characters)")

        # Create new task
        now = datetime.now()
        task = Task(
            id=self._next_id,
            title=title,
            description=description,
            is_complete=False,
            created_at=now,
            updated_at=now,
        )

        # Store task and increment ID counter
        self._tasks[self._next_id] = task
        self._next_id += 1

        return task

    def get_all_tasks(self) -> list[Task]:
        """Get all tasks in insertion order.

        Returns:
            List of all tasks, ordered by ID (insertion order).
        """
        return list(self._tasks.values())
