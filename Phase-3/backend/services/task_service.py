from typing import List, Optional
from sqlmodel import Session, select
from models import Task
from datetime import datetime


class TaskService:
    @staticmethod
    def get_tasks_by_user(session: Session, user_id: str) -> List[Task]:
        """Get all tasks for a specific user"""
        statement = select(Task).where(Task.user_id == user_id)
        return session.exec(statement).all()

    @staticmethod
    def get_task_by_id(session: Session, task_id: int, user_id: str) -> Optional[Task]:
        """Get a specific task by ID for a user"""
        statement = select(Task).where(Task.id == task_id, Task.user_id == user_id)
        return session.exec(statement).first()

    @staticmethod
    def create_task(session: Session, task: Task) -> Task:
        """Create a new task"""
        session.add(task)
        session.commit()
        session.refresh(task)
        return task

    @staticmethod
    def update_task(session: Session, task_id: int, user_id: str, task_data: dict) -> Optional[Task]:
        """Update a task"""
        existing_task = session.exec(
            select(Task).where(Task.id == task_id, Task.user_id == user_id)
        ).first()

        if existing_task:
            for key, value in task_data.items():
                setattr(existing_task, key, value)
            existing_task.updated_at = datetime.utcnow()
            session.add(existing_task)
            session.commit()
            session.refresh(existing_task)
            return existing_task
        return None

    @staticmethod
    def delete_task(session: Session, task_id: int, user_id: str) -> bool:
        """Delete a task"""
        existing_task = session.exec(
            select(Task).where(Task.id == task_id, Task.user_id == user_id)
        ).first()

        if existing_task:
            session.delete(existing_task)
            session.commit()
            return True
        return False

    @staticmethod
    def toggle_task_completion(session: Session, task_id: int, user_id: str, completed: bool) -> Optional[Task]:
        """Toggle task completion status"""
        existing_task = session.exec(
            select(Task).where(Task.id == task_id, Task.user_id == user_id)
        ).first()

        if existing_task:
            existing_task.completed = completed
            existing_task.updated_at = datetime.utcnow()
            session.add(existing_task)
            session.commit()
            session.refresh(existing_task)
            return existing_task
        return None