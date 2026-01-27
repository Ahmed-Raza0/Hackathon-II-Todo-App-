# API Contracts: Full-Stack Todo Application

## Authentication Endpoints

### POST /api/auth/register
Register a new user account

**Request:**
```json
{
  "email": "user@example.com",
  "password": "securePassword123",
  "name": "John Doe"
}
```

**Response (201 Created):**
```json
{
  "user_id": "user_123456789",
  "email": "user@example.com",
  "name": "John Doe"
}
```

### POST /api/auth/login
Login to existing account

**Request:**
```json
{
  "email": "user@example.com",
  "password": "securePassword123"
}
```

**Response (200 OK):**
```json
{
  "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "user_id": "user_123456789",
  "expires_in": 604800
}
```

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

### POST /api/{user_id}/tasks
Create a new task for the authenticated user

**Headers:**
```
Authorization: Bearer {jwt_token}
```

**Request:**
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

### PUT /api/{user_id}/tasks/{id}
Update an existing task

**Headers:**
```
Authorization: Bearer {jwt_token}
```

**Request:**
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

### PATCH /api/{user_id}/tasks/{id}/complete
Toggle task completion status

**Headers:**
```
Authorization: Bearer {jwt_token}
```

**Request:**
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

## Chatbot Endpoints

### POST /api/{user_id}/chat
Send a message to the AI assistant and get a response

**Headers:**
```
Authorization: Bearer {jwt_token}
```

**Request:**
```json
{
  "conversation_id": 123, // optional, creates new if not provided
  "message": "Create a task to buy groceries"
}
```

**Response (200 OK):**
```json
{
  "conversation_id": 123,
  "response": "I've created a task for you: 'buy groceries'",
  "tool_calls": [
    {
      "name": "add_task",
      "arguments": {
        "title": "buy groceries",
        "description": ""
      }
    }
  ],
  "timestamp": "2026-01-19T12:00:00Z"
}
```

## Error Responses

### 401 Unauthorized
```json
{
  "error": "Unauthorized",
  "message": "Invalid or missing JWT token"
}
```

### 404 Not Found
```json
{
  "error": "Not Found",
  "message": "The requested resource does not exist"
}
```

### 400 Bad Request
```json
{
  "error": "Bad Request",
  "message": "Invalid request parameters",
  "details": {
    "field": "title",
    "reason": "Title must be between 1 and 200 characters"
  }
}
```

### 500 Internal Server Error
```json
{
  "error": "Internal Server Error",
  "message": "An unexpected error occurred"
}
```

## Security Requirements
- All endpoints (except authentication) require valid JWT in Authorization header
- User ID in URL path must match user ID in JWT
- Users can only access their own resources
- All sensitive data transmitted over HTTPS