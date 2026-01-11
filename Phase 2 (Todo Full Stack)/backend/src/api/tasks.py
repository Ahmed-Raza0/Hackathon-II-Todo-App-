from fastapi import APIRouter, Depends, HTTPException, status, Path, Query, Request
from sqlmodel import Session
from typing import List, Optional
from ..database.session import get_session
from ..schemas.task import CreateTaskRequest, UpdateTaskRequest, TaskResponse
from ..services.task_service import TaskService
from ..utils.exceptions import TaskNotFoundException, UnauthorizedAccessException, ValidationErrorException

router = APIRouter()


def verify_user_access(request: Request, path_user_id: str):
    """
    Verify that the user_id in the JWT matches the one in the path.
    """
    jwt_user_id = getattr(request.state, 'user_id', None)
    if jwt_user_id != path_user_id:
        raise UnauthorizedAccessException()


@router.get("/tasks", response_model=List[TaskResponse])
def list_user_tasks(
    request: Request,
    user_id: str = Path(..., description="The ID of the user whose tasks to retrieve"),
    status: Optional[str] = Query(None, description="Filter tasks by status (all, pending, completed)"),
    session: Session = Depends(get_session)
):
    """
    List all tasks belonging to the authenticated user with optional status filtering.
    """
    verify_user_access(request, user_id)

    # Validate status parameter if provided
    if status and status not in ["all", "pending", "completed"]:
        raise ValidationErrorException("Status must be one of: all, pending, completed")

    tasks = TaskService.get_tasks_by_user(session, user_id, status)
    return tasks


@router.post("/tasks", response_model=TaskResponse, status_code=status.HTTP_201_CREATED)
def create_task(
    request: Request,
    task_data: CreateTaskRequest,
    user_id: str = Path(..., description="The ID of the user creating the task"),
    session: Session = Depends(get_session)
):
    """
    Create a new task for the authenticated user.
    """
    verify_user_access(request, user_id)

    # Validate that title is not empty
    if not task_data.title or len(task_data.title.strip()) == 0:
        raise ValidationErrorException("Title cannot be empty")

    task = TaskService.create_task(session, user_id, task_data)
    return task


@router.get("/tasks/{task_id}", response_model=TaskResponse)
def get_task(
    request: Request,
    task_id: str = Path(..., description="The ID of the task to retrieve"),
    user_id: str = Path(..., description="The ID of the user"),
    session: Session = Depends(get_session)
):
    """
    Get details of a specific task for the authenticated user.
    """
    verify_user_access(request, user_id)

    task = TaskService.get_task_by_id_and_user(session, task_id, user_id)
    return task


@router.put("/tasks/{task_id}", response_model=TaskResponse)
def update_task(
    request: Request,
    task_data: UpdateTaskRequest,
    task_id: str = Path(..., description="The ID of the task to update"),
    user_id: str = Path(..., description="The ID of the user"),
    session: Session = Depends(get_session)
):

    """
    Update the title and/or description of a task for the authenticated user.
    """
    verify_user_access(request, user_id)

    task = TaskService.update_task_by_id(session, task_id, user_id, task_data)
    return task


@router.delete("/tasks/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_task(
    request: Request,
    task_id: str = Path(..., description="The ID of the task to delete"),
    user_id: str = Path(..., description="The ID of the user"),
    session: Session = Depends(get_session)
):
    """
    Permanently delete a task for the authenticated user.
    """
    verify_user_access(request, user_id)

    TaskService.delete_task_by_id(session, task_id, user_id)
    return


@router.patch("/tasks/{task_id}/complete", response_model=TaskResponse)
def toggle_task_completion(
    request: Request,
    task_id: str = Path(..., description="The ID of the task to update"),
    user_id: str = Path(..., description="The ID of the user"),
    session: Session = Depends(get_session)
):
    """
    Toggle the completion status of a task (idempotent behavior).
    """
    verify_user_access(request, user_id)

    task = TaskService.toggle_task_completion(session, task_id, user_id)
    return task