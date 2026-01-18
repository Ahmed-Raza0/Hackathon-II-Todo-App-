from sqlmodel import Session, select
from fastapi import HTTPException, status
from typing import List, Optional
import uuid
from datetime import datetime
from ..models.task import Task, TaskCreate, TaskUpdate
from ..models.user import User


def create_task(session: Session, task_create: TaskCreate, user_id: uuid.UUID) -> Task:
    """
    Create a new task for a user
    """
    db_task = Task(
        title=task_create.title,
        description=task_create.description,
        completed=task_create.completed,
        user_id=user_id
    )

    session.add(db_task)
    session.commit()
    session.refresh(db_task)

    return db_task


def get_task_by_id(session: Session, task_id: uuid.UUID, user_id: uuid.UUID) -> Optional[Task]:
    """
    Get a task by ID for a specific user
    """
    statement = select(Task).where(Task.id == task_id, Task.user_id == user_id)
    return session.exec(statement).first()


def get_tasks_by_user(session: Session, user_id: uuid.UUID, completed: Optional[bool] = None) -> List[Task]:
    """
    Get all tasks for a specific user
    """
    statement = select(Task).where(Task.user_id == user_id)

    if completed is not None:
        statement = statement.where(Task.completed == completed)

    statement = statement.order_by(Task.created_at.desc())
    return session.exec(statement).all()


def update_task(session: Session, task_id: uuid.UUID, task_update: TaskUpdate, user_id: uuid.UUID) -> Optional[Task]:
    """
    Update a task for a specific user
    """
    statement = select(Task).where(Task.id == task_id, Task.user_id == user_id)
    db_task = session.exec(statement).first()

    if not db_task:
        return None

    # Update fields
    if task_update.title is not None:
        db_task.title = task_update.title
    if task_update.description is not None:
        db_task.description = task_update.description
    if task_update.completed is not None:
        db_task.completed = task_update.completed

    db_task.updated_at = datetime.utcnow()

    session.add(db_task)
    session.commit()
    session.refresh(db_task)

    return db_task


def delete_task(session: Session, task_id: uuid.UUID, user_id: uuid.UUID) -> bool:
    """
    Delete a task for a specific user
    """
    statement = select(Task).where(Task.id == task_id, Task.user_id == user_id)
    db_task = session.exec(statement).first()

    if not db_task:
        return False

    session.delete(db_task)
    session.commit()

    return True


def complete_task(session: Session, task_id: uuid.UUID, user_id: uuid.UUID) -> Optional[Task]:
    """
    Mark a task as completed for a specific user
    """
    statement = select(Task).where(Task.id == task_id, Task.user_id == user_id)
    db_task = session.exec(statement).first()

    if not db_task:
        return None

    db_task.completed = True
    db_task.updated_at = datetime.utcnow()

    session.add(db_task)
    session.commit()
    session.refresh(db_task)

    return db_task