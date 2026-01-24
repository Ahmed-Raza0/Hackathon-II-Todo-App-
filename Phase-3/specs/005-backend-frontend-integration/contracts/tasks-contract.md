# API Contract: Task Management Endpoints

## Task Management Endpoints

### GET /api/{user_id}/tasks
Retrieve all tasks for a specific user with optional filtering and sorting

**Headers:**
```
Authorization: Bearer {jwt_token}
```

**Query Parameters:**
- `status`: "all", "pending", "completed" (default: "all")
- `sort`: "created", "title", "due_date" (default: "created")

**Response (200 OK):**
```json
{
  "tasks": [
    {
      "id": 1,
      "user_id": "user_123456789",
      "title": "Buy groceries",
      "description": "Milk, eggs, bread",
      "completed": false,
      "created_at": "2026-01-19T10:00:00Z",
      "updated_at": "2026-01-19T10:00:00Z"
    }
  ],
  "total_count": 1,
  "filters_applied": {
    "status": "all",
    "sort": "created"
  }
}
```

**Error Responses:**
- 401: Invalid or expired JWT token
- 403: User trying to access another user's tasks

### POST /api/{user_id}/tasks
Create a new task for the authenticated user

**Headers:**
```
Authorization: Bearer {jwt_token}
Content-Type: application/json
```

**Request Body:**
```json
{
  "title": "Buy groceries",
  "description": "Milk, eggs, bread"
}
```

**Response (201 Created):**
```json
{
  "id": 1,
  "user_id": "user_123456789",
  "title": "Buy groceries",
  "description": "Milk, eggs, bread",
  "completed": false,
  "created_at": "2026-01-19T10:00:00Z",
  "updated_at": "2026-01-19T10:00:00Z"
}
```

**Validation:**
- title: 1-200 characters
- description: max 1000 characters (optional)

**Error Responses:**
- 401: Invalid or expired JWT token
- 400: Validation errors (invalid title/description)
- 403: User trying to create task for another user

### GET /api/{user_id}/tasks/{id}
Retrieve a specific task by ID

**Headers:**
```
Authorization: Bearer {jwt_token}
```

**Response (200 OK):**
```json
{
  "id": 1,
  "user_id": "user_123456789",
  "title": "Buy groceries",
  "description": "Milk, eggs, bread",
  "completed": false,
  "created_at": "2026-01-19T10:00:00Z",
  "updated_at": "2026-01-19T10:00:00Z"
}
```

**Error Responses:**
- 401: Invalid or expired JWT token
- 403: User trying to access another user's task
- 404: Task not found

### PUT /api/{user_id}/tasks/{id}
Update an existing task

**Headers:**
```
Authorization: Bearer {jwt_token}
Content-Type: application/json
```

**Request Body:**
```json
{
  "title": "Buy groceries and snacks",
  "description": "Milk, eggs, bread, chips"
}
```

**Response (200 OK):**
```json
{
  "id": 1,
  "user_id": "user_123456789",
  "title": "Buy groceries and snacks",
  "description": "Milk, eggs, bread, chips",
  "completed": false,
  "created_at": "2026-01-19T10:00:00Z",
  "updated_at": "2026-01-19T11:00:00Z"
}
```

**Error Responses:**
- 401: Invalid or expired JWT token
- 403: User trying to update another user's task
- 404: Task not found
- 400: Validation errors

### PATCH /api/{user_id}/tasks/{id}/complete
Toggle task completion status

**Headers:**
```
Authorization: Bearer {jwt_token}
Content-Type: application/json
```

**Request Body:**
```json
{
  "completed": true
}
```

**Response (200 OK):**
```json
{
  "id": 1,
  "user_id": "user_123456789",
  "title": "Buy groceries",
  "description": "Milk, eggs, bread",
  "completed": true,
  "created_at": "2026-01-19T10:00:00Z",
  "updated_at": "2026-01-19T11:30:00Z"
}
```

**Error Responses:**
- 401: Invalid or expired JWT token
- 403: User trying to update another user's task
- 404: Task not found

### DELETE /api/{user_id}/tasks/{id}
Delete a task

**Headers:**
```
Authorization: Bearer {jwt_token}
```

**Response (200 OK):**
```json
{
  "success": true,
  "message": "Task deleted successfully"
}
```

**Error Responses:**
- 401: Invalid or expired JWT token
- 403: User trying to delete another user's task
- 404: Task not found