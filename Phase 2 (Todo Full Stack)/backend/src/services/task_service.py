from sqlmodel import Session, select
from ..models.task import Task, TaskRead
from ..schemas.task import CreateTaskRequest, UpdateTaskRequest
from ..utils.exceptions import TaskNotFoundException, UnauthorizedAccessException
from typing import List, Optional
from datetime import datetime


class TaskService:
    @staticmethod
    def create_task(session: Session, user_id: str, task_data: CreateTaskRequest) -> Task:
        """
        Create a new task for a user.
        """
        task = Task(
            title=task_data.title,
            description=task_data.description,
            status=task_data.status,
            user_id=user_id
        )
        session.add(task)
        session.commit()
        session.refresh(task)
        return task

    @staticmethod
    def get_tasks_by_user(
        session: Session,
        user_id: str,
        status_filter: Optional[str] = None
    ) -> List[Task]:
        """
        Get all tasks for a user, with optional status filtering.
        """
        query = select(Task).where(Task.user_id == user_id)

        if status_filter and status_filter != "all":
            query = query.where(Task.status == status_filter)

        tasks = session.exec(query).all()
        return tasks

    @staticmethod
    def get_task_by_id_and_user(session: Session, task_id: str, user_id: str) -> Task:
        """
        Get a specific task by ID for a user.
        """
        statement = select(Task).where(Task.id == task_id, Task.user_id == user_id)
        task = session.exec(statement).first()
        if not task:
            raise TaskNotFoundException(task_id)
        return task

    @staticmethod
    def update_task_by_id(
        session: Session,
        task_id: str,
        user_id: str,
        task_data: UpdateTaskRequest
    ) -> Task:
        """
        Update a task by ID for a user.
        """
        task = TaskService.get_task_by_id_and_user(session, task_id, user_id)

        # Update fields if provided
        if task_data.title is not None:
            task.title = task_data.title
        if task_data.description is not None:
            task.description = task_data.description

        task.updated_at = datetime.utcnow()
        session.add(task)
        session.commit()
        session.refresh(task)
        return task

    @staticmethod
    def delete_task_by_id(session: Session, task_id: str, user_id: str) -> bool:
        """
        Delete a task by ID for a user.
        """
        task = TaskService.get_task_by_id_and_user(session, task_id, user_id)
        session.delete(task)
        session.commit()
        return True

    @staticmethod
    def toggle_task_completion(session: Session, task_id: str, user_id: str) -> Task:
        """
        Toggle the completion status of a task (idempotent behavior).
        """
        task = TaskService.get_task_by_id_and_user(session, task_id, user_id)

        # Toggle status: if pending -> completed, if completed -> pending
        if task.status == "completed":
            task.status = "pending"
        else:
            task.status = "completed"

        task.updated_at = datetime.utcnow()
        session.add(task)
        session.commit()
        session.refresh(task)
        return task