from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlmodel import select, desc
from typing import Any, List
import uuid

from models.task import Task, TaskCreate, TaskUpdate, TaskRead, TaskStatus
from models.user import User
from database import get_session
from utils.auth import get_current_user

router = APIRouter(prefix="/tasks", tags=["tasks"])

@router.get("/", response_model=List[TaskRead])
def read_tasks(
    current_user: User = Depends(get_current_user),
    session: Session = Depends(get_session),
    skip: int = 0,
    limit: int = 100
) -> Any:
    """
    Retrieve tasks for the current user.
    """
    tasks = session.exec(
        select(Task)
        .where(Task.user_id == current_user.id)
        .offset(skip)
        .limit(limit)
        .order_by(desc(Task.created_at))
    ).all()
    return tasks

@router.post("/", response_model=TaskRead)
def create_task(
    task: TaskCreate,
    current_user: User = Depends(get_current_user),
    session: Session = Depends(get_session)
) -> Any:
    """
    Create a new task for the current user.
    """
    db_task = Task(
        title=task.title,
        description=task.description,
        status=task.status if task.status else TaskStatus.pending,
        priority=task.priority if task.priority else TaskPriority.medium,
        due_date=task.due_date,
        user_id=current_user.id
    )
    session.add(db_task)
    session.commit()
    session.refresh(db_task)
    return db_task

@router.get("/{task_id}", response_model=TaskRead)
def read_task(
    task_id: uuid.UUID,
    current_user: User = Depends(get_current_user),
    session: Session = Depends(get_session)
) -> Any:
    """
    Get a specific task by ID.
    """
    task = session.exec(
        select(Task).where(Task.id == task_id).where(Task.user_id == current_user.id)
    ).first()

    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    return task

@router.put("/{task_id}", response_model=TaskRead)
def update_task(
    task_id: uuid.UUID,
    task_update: TaskUpdate,
    current_user: User = Depends(get_current_user),
    session: Session = Depends(get_session)
) -> Any:
    """
    Update a specific task by ID.
    """
    task = session.exec(
        select(Task).where(Task.id == task_id).where(Task.user_id == current_user.id)
    ).first()

    if not task:
        raise HTTPException(status_code=404, detail="Task not found")

    # Update task attributes
    update_data = task_update.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(task, field, value)

    # If status is changed to completed, set completed_at
    if task_update.status == TaskStatus.completed and task.status != TaskStatus.completed:
        from datetime import datetime
        task.completed_at = datetime.utcnow()

    # Update the updated_at timestamp
    from datetime import datetime
    task.updated_at = datetime.utcnow()

    session.add(task)
    session.commit()
    session.refresh(task)
    return task

@router.delete("/{task_id}")
def delete_task(
    task_id: uuid.UUID,
    current_user: User = Depends(get_current_user),
    session: Session = Depends(get_session)
) -> Any:
    """
    Delete a specific task by ID.
    """
    task = session.exec(
        select(Task).where(Task.id == task_id).where(Task.user_id == current_user.id)
    ).first()

    if not task:
        raise HTTPException(status_code=404, detail="Task not found")

    session.delete(task)
    session.commit()
    return {"message": "Task deleted successfully"}