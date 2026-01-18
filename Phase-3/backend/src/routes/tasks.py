from fastapi import APIRouter, Depends, HTTPException, status
from typing import List, Optional
from uuid import UUID
from sqlmodel import Session

from ..models.task import Task, TaskCreate, TaskUpdate, TaskPublic
from ..models.user import User
from ..services.task_service import (
    create_task,
    get_task_by_id,
    get_tasks_by_user,
    update_task,
    delete_task,
    complete_task
)
from ..dependencies import get_session
from .auth import get_current_user

router = APIRouter()


@router.post("/tasks", response_model=TaskPublic)
def create_task_endpoint(
    task_create: TaskCreate,
    current_user: User = Depends(get_current_user),
    session: Session = Depends(get_session)
):
    """
    Create a new task for the current user
    """
    return create_task(session, task_create, current_user.id)


@router.get("/tasks", response_model=List[TaskPublic])
def read_tasks(
    completed: Optional[bool] = None,
    current_user: User = Depends(get_current_user),
    session: Session = Depends(get_session)
):
    """
    Get all tasks for the current user
    """
    return get_tasks_by_user(session, current_user.id, completed)


@router.get("/tasks/{task_id}", response_model=TaskPublic)
def read_task(
    task_id: UUID,
    current_user: User = Depends(get_current_user),
    session: Session = Depends(get_session)
):
    """
    Get a specific task by ID
    """
    task = get_task_by_id(session, task_id, current_user.id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    return task


@router.put("/tasks/{task_id}", response_model=TaskPublic)
def update_task_endpoint(
    task_id: UUID,
    task_update: TaskUpdate,
    current_user: User = Depends(get_current_user),
    session: Session = Depends(get_session)
):
    """
    Update a specific task
    """
    task = update_task(session, task_id, task_update, current_user.id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    return task


@router.patch("/tasks/{task_id}/complete", response_model=TaskPublic)
def complete_task_endpoint(
    task_id: UUID,
    current_user: User = Depends(get_current_user),
    session: Session = Depends(get_session)
):
    """
    Mark a task as completed
    """
    task = complete_task(session, task_id, current_user.id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    return task


@router.delete("/tasks/{task_id}")
def delete_task_endpoint(
    task_id: UUID,
    current_user: User = Depends(get_current_user),
    session: Session = Depends(get_session)
):
    """
    Delete a specific task
    """
    success = delete_task(session, task_id, current_user.id)
    if not success:
        raise HTTPException(status_code=404, detail="Task not found")
    return {"message": "Task deleted successfully"}