# API Contracts: Authentication Endpoints

## Authentication Endpoints

### POST /api/auth/signup
Create a new user account with email, password, and optional name

**Request:**
```json
{
  "email": "user@example.com",
  "password": "securePassword123",
  "name": "John Doe"
}
```

**Headers:**
```
Content-Type: application/json
```

**Response (201 Created):**
```json
{
  "user_id": "user_123456789",
  "email": "user@example.com",
  "name": "John Doe",
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer"
}
```

**Error Responses:**
- 400: Invalid request format or weak password (less than 8 chars)
- 409: Email already exists
- 500: Server error during account creation

### POST /api/auth/login
Authenticate user with email and password, return JWT token

**Request:**
```json
{
  "email": "user@example.com",
  "password": "securePassword123"
}
```

**Headers:**
```
Content-Type: application/json
```

**Response (200 OK):**
```json
{
  "user_id": "user_123456789",
  "email": "user@example.com",
  "name": "John Doe",
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer"
}
```

**Error Responses:**
- 401: Invalid email or password
- 400: Malformed request
- 500: Server error during authentication

### GET /api/auth/me
Verify JWT token and return authenticated user's information

**Headers:**
```
Authorization: Bearer {jwt_token}
```

**Response (200 OK):**
```json
{
  "user_id": "user_123456789",
  "email": "user@example.com",
  "name": "John Doe",
  "created_at": "2026-01-19T10:00:00Z"
}
```

**Error Responses:**
- 401: Invalid or expired token
- 400: Malformed authorization header
- 500: Server error during token validation

### POST /api/auth/logout
Clear user session (optional endpoint)

**Headers:**
```
Authorization: Bearer {jwt_token}
```

**Response (200 OK):**
```json
{
  "success": true,
  "message": "Successfully logged out"
}
```

**Error Responses:**
- 401: Invalid or expired token
- 500: Server error during logout

## Protected Task Endpoints (Require Authentication)

### GET /api/{user_id}/tasks
Retrieve all tasks for the authenticated user with optional filtering and sorting

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
- 401: Invalid or expired token
- 403: User_id in URL doesn't match authenticated user
- 500: Server error during task retrieval

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
- 401: Invalid or expired token
- 400: Validation errors (invalid title/description)
- 403: User_id in URL doesn't match authenticated user
- 500: Server error during task creation

### GET /api/{user_id}/tasks/{id}
Retrieve a specific task by ID for the authenticated user

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
- 401: Invalid or expired token
- 403: User_id in URL doesn't match authenticated user or task doesn't belong to user
- 404: Task not found
- 500: Server error during task retrieval

### PUT /api/{user_id}/tasks/{id}
Update an existing task for the authenticated user

**Headers:**
```
Authorization: Bearer {jwt_token}
Content-Type: application/json
```

**Request Body:**
```json
{
  "title": "Buy groceries and snacks",
  "description": "Milk, eggs, bread, and chips"
}
```

**Response (200 OK):**
```json
{
  "id": 1,
  "user_id": "user_123456789",
  "title": "Buy groceries and snacks",
  "description": "Milk, eggs, bread, and chips",
  "completed": false,
  "created_at": "2026-01-19T10:00:00Z",
  "updated_at": "2026-01-19T11:00:00Z"
}
```

**Error Responses:**
- 401: Invalid or expired token
- 403: User_id in URL doesn't match authenticated user or task doesn't belong to user
- 404: Task not found
- 400: Validation errors
- 500: Server error during task update

### PATCH /api/{user_id}/tasks/{id}/complete
Toggle task completion status for the authenticated user

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
- 401: Invalid or expired token
- 403: User_id in URL doesn't match authenticated user or task doesn't belong to user
- 404: Task not found
- 500: Server error during task update

### DELETE /api/{user_id}/tasks/{id}
Delete a task for the authenticated user

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
- 401: Invalid or expired token
- 403: User_id in URL doesn't match authenticated user or task doesn't belong to user
- 404: Task not found
- 500: Server error during task deletion

## Common Error Responses

### 401 Unauthorized
```json
{
  "detail": "Could not validate credentials"
}
```

### 403 Forbidden
```json
{
  "detail": "Access denied - user does not have permission to perform this action"
}
```

### 404 Not Found
```json
{
  "detail": "The requested resource does not exist"
}
```

### 400 Bad Request
```json
{
  "detail": "Invalid request parameters",
  "errors": [
    {
      "field": "title",
      "reason": "Title must be between 1 and 200 characters"
    }
  ]
}
```

### 500 Internal Server Error
```json
{
  "detail": "An unexpected error occurred"
}
```

## Security Requirements

- All authentication endpoints must validate JWT tokens
- User ID in URL path must match authenticated user ID from JWT
- All sensitive data must be transmitted over HTTPS
- Passwords must never be returned in API responses
- Authentication tokens must have limited expiration times
- Rate limiting should be applied to prevent brute force attacks
- Input validation must be applied to all fields to prevent injection attacks