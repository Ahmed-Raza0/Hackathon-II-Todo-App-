"""Task entity model for Todo CLI Core application.

This module defines the Task dataclass with all required attributes and
display formatting functionality.
"""

from dataclasses import dataclass
from datetime import datetime


@dataclass
class Task:
    """Represents a single task in the todo list.

    Attributes:
        id: Unique identifier for the task (positive integer, sequential).
        title: Task title (1-200 characters, non-empty).
        description: Optional task description (max 1000 characters).
        is_complete: Completion status (True = complete, False = incomplete).
        created_at: Timestamp when task was created (ISO 8601 format).
        updated_at: Timestamp when task was last modified (ISO 8601 format).
    """

    id: int
    title: str
    description: str | None
    is_complete: bool
    created_at: datetime
    updated_at: datetime

    def to_display(self) -> str:
        """Format task for console display per Principle 6 specification.

        Returns:
            Formatted string with task ID, checkbox, title, timestamp, and description.

        Example output:
            ID: 1 | [X] Buy groceries | Created: 2025-12-27 10:30
                Description: Milk, eggs, bread
        """
        checkbox = "[X]" if self.is_complete else "[ ]"
        created_str = self.created_at.strftime("%Y-%m-%d %H:%M")
        result = f"ID: {self.id} | {checkbox} {self.title} | Created: {created_str}"

        if self.description:
            result += f"\n    Description: {self.description}"

        return result
