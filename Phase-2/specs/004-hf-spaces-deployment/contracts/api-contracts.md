# API Contracts: FastAPI Todo Backend

## Overview

This document defines the API contracts for the Todo backend service. The API provides endpoints for managing todo tasks with user-specific access control.

## Base URL

The API endpoints are rooted at `/api/{user_id}/` where `{user_id}` is the authenticated user's identifier.

## Authentication

All endpoints (except health check and root) require JWT authentication via the `Authorization` header:

```
Authorization: Bearer {jwt-token}
```

The user_id in the JWT token must match the user_id in the URL path.

## Common Response Formats

### Success Response
```json
{
  "id": "string",
  "title": "string",
  "description": "string or null",
  "status": "string",
  "user_id": "string",
  "created_at": "ISO 8601 datetime string",
  "updated_at": "ISO 8601 datetime string"
}
```

### Error Response
```json
{
  "detail": "error message string"
}
```

## Endpoints

### Health Check
- **Endpoint**: `GET /health`
- **Authentication**: Not required
- **Description**: Check if the service is running
- **Response**:
  - 200: `{"status": "healthy"}`

### Root Endpoint
- **Endpoint**: `GET /`
- **Authentication**: Not required
- **Description**: Service information
- **Response**:
  - 200: `{"message": "Todo Backend API"}`

### Get User Tasks
- **Endpoint**: `GET /api/{user_id}/tasks`
- **Authentication**: Required
- **Parameters**:
  - Path: `user_id` (string) - User identifier
  - Query (optional): `status` (string) - Filter by status ("all", "pending", "completed")
- **Description**: Retrieve all tasks for a user
- **Response**:
  - 200: Array of Task objects
  - 401: Unauthorized

### Create Task
- **Endpoint**: `POST /api/{user_id}/tasks`
- **Authentication**: Required
- **Parameters**:
  - Path: `user_id` (string) - User identifier
- **Request Body**:
  ```json
  {
    "title": "string",
    "description": "string or null",
    "status": "string (default: 'pending')"
  }
  ```
- **Description**: Create a new task for a user
- **Response**:
  - 201: Created Task object
  - 400: Validation error
  - 401: Unauthorized

### Get Specific Task
- **Endpoint**: `GET /api/{user_id}/tasks/{task_id}`
- **Authentication**: Required
- **Parameters**:
  - Path: `user_id` (string) - User identifier
  - Path: `task_id` (string) - Task identifier
- **Description**: Retrieve a specific task
- **Response**:
  - 200: Task object
  - 401: Unauthorized
  - 404: Task not found

### Update Task
- **Endpoint**: `PUT /api/{user_id}/tasks/{task_id}`
- **Authentication**: Required
- **Parameters**:
  - Path: `user_id` (string) - User identifier
  - Path: `task_id` (string) - Task identifier
- **Request Body**:
  ```json
  {
    "title": "string or null",
    "description": "string or null"
  }
  ```
- **Description**: Update task details
- **Response**:
  - 200: Updated Task object
  - 400: Validation error
  - 401: Unauthorized
  - 404: Task not found

### Delete Task
- **Endpoint**: `DELETE /api/{user_id}/tasks/{task_id}`
- **Authentication**: Required
- **Parameters**:
  - Path: `user_id` (string) - User identifier
  - Path: `task_id` (string) - Task identifier
- **Description**: Permanently delete a task
- **Response**:
  - 204: No content (success)
  - 401: Unauthorized
  - 404: Task not found

### Toggle Task Completion
- **Endpoint**: `PATCH /api/{user_id}/tasks/{task_id}/complete`
- **Authentication**: Required
- **Parameters**:
  - Path: `user_id` (string) - User identifier
  - Path: `task_id` (string) - Task identifier
- **Description**: Toggle the completion status of a task
- **Response**:
  - 200: Updated Task object
  - 401: Unauthorized
  - 404: Task not found

## Error Codes

- 400: Bad Request - Invalid input data
- 401: Unauthorized - Missing or invalid authentication
- 404: Not Found - Requested resource doesn't exist
- 500: Internal Server Error - Unexpected server error

## Data Validation

### Task Object Validation
- `title`: Required, non-empty string
- `status`: Must be one of allowed values (pending, completed)
- `user_id`: Must match the authenticated user

### Path Parameter Validation
- `user_id`: Must match the authenticated user's ID
- `task_id`: Must be a valid task identifier

## Request/Response Examples

### Create Task Request
```json
{
  "title": "Buy groceries",
  "description": "Milk, eggs, bread",
  "status": "pending"
}
```

### Successful Task Response
```json
{
  "id": "task-123",
  "title": "Buy groceries",
  "description": "Milk, eggs, bread",
  "status": "pending",
  "user_id": "user-456",
  "created_at": "2026-01-10T10:00:00Z",
  "updated_at": "2026-01-10T10:00:00Z"
}
```