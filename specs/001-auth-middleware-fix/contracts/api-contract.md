# API Contract: Authentication Endpoints

## Overview
This document outlines the public authentication endpoints that should be accessible without JWT tokens.

## Public Authentication Endpoints

### POST /api/auth/signup
Create a new user account.

**Request:**
- Method: POST
- URL: `/api/auth/signup`
- Headers:
  - `Content-Type: application/json`
- Body:
```json
{
  "email": "user@example.com",
  "password": "securePassword123",
  "name": "John Doe"
}
```

**Responses:**
- Success: `201 Created`
```json
{
  "user_id": "user_abc123",
  "email": "user@example.com",
  "name": "John Doe",
  "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
}
```
- Validation Error: `422 Unprocessable Entity`
```json
{
  "detail": "Email is required"
}
```
- Conflict Error: `409 Conflict`
```json
{
  "detail": "User with this email already exists"
}
```

### POST /api/auth/login
Authenticate user and return JWT token.

**Request:**
- Method: POST
- URL: `/api/auth/login`
- Headers:
  - `Content-Type: application/json`
- Body:
```json
{
  "email": "user@example.com",
  "password": "securePassword123"
}
```

**Responses:**
- Success: `200 OK`
```json
{
  "user_id": "user_abc123",
  "email": "user@example.com",
  "name": "John Doe",
  "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
}
```
- Unauthorized: `401 Unauthorized`
```json
{
  "detail": "Invalid email or password"
}
```

### POST /api/auth/logout
Logout user (optional endpoint, mostly for client-side cleanup).

**Request:**
- Method: POST
- URL: `/api/auth/logout`
- Headers:
  - `Authorization: Bearer {token}` (optional)
- Body: None

**Responses:**
- Success: `200 OK`
```json
{
  "message": "Successfully logged out"
}
```

## Protected Endpoints (require JWT)

### GET /api/{user_id}/tasks
Get all tasks for a specific user.

**Request:**
- Method: GET
- URL: `/api/{user_id}/tasks`
- Headers:
  - `Authorization: Bearer {token}`
- Parameters:
  - `status` (optional): Filter by task status (all, pending, completed)

**Responses:**
- Success: `200 OK`
```json
[
  {
    "id": "task_123",
    "title": "Sample Task",
    "description": "Sample Description",
    "completed": false,
    "created_at": "2023-01-01T00:00:00Z",
    "updated_at": "2023-01-01T00:00:00Z"
  }
]
```
- Unauthorized: `401 Unauthorized`
```json
{
  "detail": "Authorization token missing"
}
```
- Forbidden: `403 Forbidden`
```json
{
  "detail": "You are not authorized to access this resource"
}
```

## Middleware Requirements

### Public Route Access
- Authentication not required
- No Authorization header needed
- Should return appropriate responses

### Protected Route Access
- Valid JWT token required in Authorization header
- User ID in JWT must match user_id in path parameter
- Invalid or missing tokens should return 401
- Mismatched user IDs should return 403