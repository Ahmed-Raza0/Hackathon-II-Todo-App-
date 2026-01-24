# API Contract: Authentication Endpoints

## Authentication Endpoints

### POST /api/auth/login
Login existing user with email and password

**Request:**
```json
{
  "email": "user@example.com",
  "password": "securePassword123",
  "callbackUrl": "/dashboard"
}
```

**Response (200 OK):**
```json
{
  "user_id": "user_123456789",
  "email": "user@example.com",
  "name": "John Doe",
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer",
  "expires_in": 2592000
}
```

**Response (401 Unauthorized):**
```json
{
  "error": "Unauthorized",
  "message": "Invalid email or password"
}
```

### POST /api/auth/signup
Create new user account with email, password, and name

**Request:**
```json
{
  "email": "user@example.com",
  "password": "securePassword123",
  "name": "John Doe",
  "callbackUrl": "/dashboard"
}
```

**Response (201 Created):**
```json
{
  "user_id": "user_123456789",
  "email": "user@example.com",
  "name": "John Doe",
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer",
  "expires_in": 2592000
}
```

**Response (400 Bad Request):**
```json
{
  "error": "Bad Request",
  "message": "Invalid request parameters",
  "details": {
    "field": "email",
    "reason": "Email already exists"
  }
}
```

### GET /api/auth/me
Get current authenticated user information

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

**Response (401 Unauthorized):**
```json
{
  "error": "Unauthorized",
  "message": "Invalid or expired token"
}
```

### POST /api/auth/logout
Logout current user and invalidate session

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

**Response (401 Unauthorized):**
```json
{
  "error": "Unauthorized",
  "message": "Invalid or expired token"
}
```

## Protected Task Endpoints (Require Authentication)

### GET /api/{user_id}/tasks
Get all tasks for the authenticated user

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
Content-Type: application/json
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

### PUT /api/{user_id}/tasks/{id}
Update an existing task

**Headers:**
```
Authorization: Bearer {jwt_token}
Content-Type: application/json
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
Content-Type: application/json
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

## Common Error Responses

### 401 Unauthorized
```json
{
  "error": "Unauthorized",
  "message": "Invalid or missing JWT token"
}
```

### 403 Forbidden
```json
{
  "error": "Forbidden",
  "message": "Access denied - user does not have permission to perform this action"
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

- All authentication endpoints must validate JWT tokens
- User ID in URL path must match authenticated user ID from JWT
- All sensitive data must be transmitted over HTTPS
- Passwords must never be returned in API responses
- Authentication tokens must have limited expiration times
- Rate limiting should be applied to prevent brute force attacks