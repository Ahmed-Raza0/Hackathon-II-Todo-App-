"""MCP Tools for Task Operations"""

from typing import Dict, Any, List
from services.task_service import TaskService
from models import Task
from sqlmodel import Session


class TaskMCPTools:
    """Collection of MCP tools for task operations"""

    @staticmethod
    def add_task(session: Session, user_id: str, title: str, description: str = None) -> Dict[str, Any]:
        """Create a new task"""
        try:
            task = Task(
                user_id=user_id,
                title=title,
                description=description,
                completed=False
            )
            created_task = TaskService.create_task(session, task)
            return {
                "success": True,
                "task": {
                    "id": created_task.id,
                    "title": created_task.title,
                    "description": created_task.description,
                    "completed": created_task.completed
                }
            }
        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }

    @staticmethod
    def list_tasks(session: Session, user_id: str, status: str = "all") -> Dict[str, Any]:
        """List user's tasks with optional status filter"""
        try:
            tasks = TaskService.get_tasks_by_user(session, user_id)

            if status != "all":
                if status == "pending":
                    tasks = [t for t in tasks if not t.completed]
                elif status == "completed":
                    tasks = [t for t in tasks if t.completed]

            task_list = [
                {
                    "id": t.id,
                    "title": t.title,
                    "description": t.description,
                    "completed": t.completed
                }
                for t in tasks
            ]

            return {
                "success": True,
                "tasks": task_list,
                "count": len(task_list)
            }
        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }

    @staticmethod
    def complete_task(session: Session, user_id: str, task_id: int, completed: bool = True) -> Dict[str, Any]:
        """Mark a task as complete or pending"""
        try:
            # First get the task to check if it belongs to the user
            task = TaskService.get_task_by_id(session, task_id, user_id)
            if not task:
                return {
                    "success": False,
                    "error": "Task not found or doesn't belong to user"
                }

            updated_task = TaskService.toggle_task_completion(session, task_id, user_id, completed)
            if updated_task:
                return {
                    "success": True,
                    "task": {
                        "id": updated_task.id,
                        "title": updated_task.title,
                        "description": updated_task.description,
                        "completed": updated_task.completed
                    }
                }
            else:
                return {
                    "success": False,
                    "error": "Failed to update task"
                }
        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }

    @staticmethod
    def update_task(session: Session, user_id: str, task_id: int, title: str = None, description: str = None) -> Dict[str, Any]:
        """Update a task's title or description"""
        try:
            # First get the task to check if it belongs to the user
            task = TaskService.get_task_by_id(session, task_id, user_id)
            if not task:
                return {
                    "success": False,
                    "error": "Task not found or doesn't belong to user"
                }

            # Prepare update data
            update_data = {}
            if title is not None:
                update_data['title'] = title
            if description is not None:
                update_data['description'] = description

            updated_task = TaskService.update_task(session, task_id, user_id, update_data)
            if updated_task:
                return {
                    "success": True,
                    "task": {
                        "id": updated_task.id,
                        "title": updated_task.title,
                        "description": updated_task.description,
                        "completed": updated_task.completed
                    }
                }
            else:
                return {
                    "success": False,
                    "error": "Failed to update task"
                }
        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }

    @staticmethod
    def delete_task(session: Session, user_id: str, task_id: int) -> Dict[str, Any]:
        """Delete a task"""
        try:
            success = TaskService.delete_task(session, task_id, user_id)
            if success:
                return {
                    "success": True,
                    "message": "Task deleted successfully"
                }
            else:
                return {
                    "success": False,
                    "error": "Task not found or doesn't belong to user"
                }
        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }