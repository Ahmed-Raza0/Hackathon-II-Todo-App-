from fastapi import APIRouter, Depends, HTTPException, status, Body, Request
from sqlmodel import Session
from typing import Dict, Any
import logging

from database import get_session
from models import Task, TaskCreate, TaskUpdate
from auth import get_current_user
from services.task_service import TaskService

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/api/tasks")


@router.get("")
def list_tasks(
    session: Session = Depends(get_session),
    current_user: str = Depends(get_current_user)
):
    """Get all tasks for the current user"""
    return TaskService.get_tasks_by_user(session, current_user)


@router.post("")
def create_task(
    task_data: TaskCreate,
    session: Session = Depends(get_session),
    current_user: str = Depends(get_current_user)
):
    """Create a new task for the current user"""
    # Create task with current user's ID
    task = Task(**task_data.model_dump(), user_id=current_user)
    return TaskService.create_task(session, task)


@router.get("/{task_id}")
def get_task(
    task_id: int,
    session: Session = Depends(get_session),
    current_user: str = Depends(get_current_user)
):
    """Get a specific task by ID"""
    task = TaskService.get_task_by_id(session, task_id, current_user)
    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail="Task not found"
        )
    return task


@router.put("/{task_id}")
def update_task(
    task_id: int,
    updated_task: TaskUpdate,
    session: Session = Depends(get_session),
    current_user: str = Depends(get_current_user)
):
    """Update a task"""
    task = TaskService.get_task_by_id(session, task_id, current_user)
    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail="Task not found"
        )

    # Update with the new values
    update_data = updated_task.model_dump(exclude_unset=True)
    updated = TaskService.update_task(session, task_id, current_user, update_data)
    return updated


@router.delete("/{task_id}")
def delete_task(
    task_id: int,
    session: Session = Depends(get_session),
    current_user: str = Depends(get_current_user)
):
    """Delete a task"""
    success = TaskService.delete_task(session, task_id, current_user)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail="Task not found"
        )
    return {"message": "Task deleted successfully"}


@router.patch("/{task_id}/complete")
async def toggle_task_completion(
    task_id: int,
    request: Request,
    session: Session = Depends(get_session),
    current_user: str = Depends(get_current_user)
):
    """Toggle task completion status"""
    try:
        # Get the raw body
        body = await request.json()
        logger.info(f"📦 Received body: {body}")
        logger.info(f"📦 Body type: {type(body)}")
        
        # Extract completed from body
        if "completed" not in body:
            logger.error("❌ 'completed' field missing from body")
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail="'completed' field is required in request body"
            )
        
        completed = body.get("completed")
        logger.info(f"✅ Completed value: {completed}, type: {type(completed)}")
        
        if not isinstance(completed, bool):
            logger.error(f"❌ 'completed' is not boolean: {completed}")
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail="'completed' must be a boolean value"
            )
        
        task = TaskService.toggle_task_completion(
            session, 
            task_id, 
            current_user, 
            completed
        )
        if not task:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, 
                detail="Task not found"
            )
        
        logger.info(f"✅ Task {task_id} completion updated to {completed}")
        return task
        
    except ValueError as e:
        logger.error(f"❌ Invalid JSON: {e}")
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="Invalid JSON in request body"
        )