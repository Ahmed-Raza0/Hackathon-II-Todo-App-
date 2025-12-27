"""CLI interface for Todo CLI Core application.

This module provides the command-line interface for user interaction with
the task management system.
"""

import sys
from src.task_manager import TaskManager, InvalidTaskError, TaskNotFoundError


class CLI:
    """Command-line interface for the Todo application.

    Provides menu display, user input handling, and operation flows for
    all task management features.

    Attributes:
        task_manager: TaskManager instance for business logic.
    """

    def __init__(self) -> None:
        """Initialize CLI with a new TaskManager instance."""
        self.task_manager = TaskManager()

    def display_menu(self) -> None:
        """Display the main menu per Principle 6 specification."""
        print("\n=== Todo App ===")
        print("1. Add Task")
        print("2. View All Tasks")
        print("3. Update Task")
        print("4. Mark Task Complete")
        print("5. Delete Task")
        print("6. Exit")
        print()

    def get_menu_choice(self) -> int | None:
        """Get and validate user menu choice.

        Returns:
            Valid choice (1-6) or None if invalid.
        """
        try:
            choice = int(input("Enter your choice (1-6): "))
            if 1 <= choice <= 6:
                return choice
            else:
                print("Invalid choice. Please enter 1-6")
                return None
        except ValueError:
            print("Invalid choice. Please enter 1-6")
            return None

    def add_task_flow(self) -> None:
        """Handle the Add Task operation flow.

        Prompts user for title and description, creates task, and displays
        success or error message.
        """
        try:
            title = input("Enter task title: ")
            description = input("Enter description (optional): ")

            # Convert empty description to None
            if not description:
                description = None

            task = self.task_manager.add_task(title, description)
            print(f"✓ Task added successfully! (ID: {task.id})")

        except InvalidTaskError as e:
            print(f"✗ Error: {e}")
        except Exception as e:
            print(f"✗ An unexpected error occurred: {e}")

    def view_tasks_flow(self) -> None:
        """Handle the View All Tasks operation flow.

        Displays all tasks using task.to_display() or shows 'No tasks found'
        if the list is empty.
        """
        tasks = self.task_manager.get_all_tasks()

        if not tasks:
            print("No tasks found")
        else:
            for task in tasks:
                print(task.to_display())
                print()  # Blank line between tasks
