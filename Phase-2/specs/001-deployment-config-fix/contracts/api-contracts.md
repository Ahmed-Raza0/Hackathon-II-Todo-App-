# API Contracts: Production Deployment Configuration

## Overview
This document defines the API contracts that must work consistently across local development and production environments. The contracts remain unchanged from the original specification, but configuration fixes ensure they work properly in production.

## Authentication Endpoints

### POST /api/auth/signup
**Description**: Register a new user account
- **Request Body**:
  ```json
  {
    "email": "string (valid email)",
    "password": "string (min 8 characters)"
  }
  ```
- **Response**: 201 Created
  ```json
  {
    "user": {
      "id": "string",
      "email": "string",
      "createdAt": "ISO date string"
    },
    "token": "JWT string"
  }
  ```
- **Error Responses**: 400 (validation error), 409 (email exists), 500 (server error)
- **Authentication**: None required

### POST /api/auth/login
**Description**: Authenticate existing user
- **Request Body**:
  ```json
  {
    "email": "string (valid email)",
    "password": "string"
  }
  ```
- **Response**: 200 OK
  ```json
  {
    "user": {
      "id": "string",
      "email": "string",
      "createdAt": "ISO date string"
    },
    "token": "JWT string"
  }
  ```
- **Error Responses**: 400 (validation error), 401 (invalid credentials), 500 (server error)
- **Authentication**: None required

### POST /api/auth/logout
**Description**: Log out current user (optional endpoint)
- **Request**: No body required
- **Response**: 200 OK
  ```json
  {}
  ```
- **Error Responses**: 401 (unauthorized), 500 (server error)
- **Authentication**: JWT required

## Task Management Endpoints

### GET /api/tasks
**Description**: Get current user's tasks
- **Request**: No body required
- **Response**: 200 OK
  ```json
  {
    "tasks": [
      {
        "id": "string",
        "title": "string",
        "completed": "boolean",
        "userId": "string",
        "createdAt": "ISO date string",
        "updatedAt": "ISO date string"
      }
    ]
  }
  ```
- **Error Responses**: 401 (unauthorized), 500 (server error)
- **Authentication**: JWT required

### POST /api/tasks
**Description**: Create a new task for current user
- **Request Body**:
  ```json
  {
    "title": "string (1-255 characters)"
  }
  ```
- **Response**: 201 Created
  ```json
  {
    "task": {
      "id": "string",
      "title": "string",
      "completed": "boolean",
      "userId": "string",
      "createdAt": "ISO date string",
      "updatedAt": "ISO date string"
    }
  }
  ```
- **Error Responses**: 400 (validation error), 401 (unauthorized), 500 (server error)
- **Authentication**: JWT required

### GET /api/tasks/{id}
**Description**: Get specific task by ID
- **Parameters**: id (path parameter)
- **Response**: 200 OK
  ```json
  {
    "task": {
      "id": "string",
      "title": "string",
      "completed": "boolean",
      "userId": "string",
      "createdAt": "ISO date string",
      "updatedAt": "ISO date string"
    }
  }
  ```
- **Error Responses**: 401 (unauthorized), 404 (not found), 500 (server error)
- **Authentication**: JWT required

### PATCH /api/tasks/{id}
**Description**: Update task title
- **Parameters**: id (path parameter)
- **Request Body**:
  ```json
  {
    "title": "string (1-255 characters)"
  }
  ```
- **Response**: 200 OK
  ```json
  {
    "task": {
      "id": "string",
      "title": "string",
      "completed": "boolean",
      "userId": "string",
      "createdAt": "ISO date string",
      "updatedAt": "ISO date string"
    }
  }
  ```
- **Error Responses**: 400 (validation error), 401 (unauthorized), 404 (not found), 500 (server error)
- **Authentication**: JWT required

### PATCH /api/tasks/{id}/toggle
**Description**: Toggle task completion status
- **Parameters**: id (path parameter)
- **Response**: 200 OK
  ```json
  {
    "task": {
      "id": "string",
      "title": "string",
      "completed": "boolean",
      "userId": "string",
      "createdAt": "ISO date string",
      "updatedAt": "ISO date string"
    }
  }
  ```
- **Error Responses**: 401 (unauthorized), 404 (not found), 500 (server error)
- **Authentication**: JWT required

### DELETE /api/tasks/{id}
**Description**: Delete specific task
- **Parameters**: id (path parameter)
- **Response**: 204 No Content
- **Error Responses**: 401 (unauthorized), 404 (not found), 500 (server error)
- **Authentication**: JWT required

## Health Check Endpoints

### GET /
**Description**: Root endpoint for health checks
- **Response**: 200 OK
  ```json
  {
    "status": "ok",
    "timestamp": "ISO date string"
  }
  ```
- **Error Responses**: 500 (server error)
- **Authentication**: None required (must bypass auth)

### GET /health
**Description**: Dedicated health check endpoint
- **Response**: 200 OK
  ```json
  {
    "status": "healthy",
    "version": "string",
    "timestamp": "ISO date string"
  }
  ```
- **Error Responses**: 503 (unhealthy), 500 (server error)
- **Authentication**: None required (must bypass auth)

## CORS Policy
- **Allowed Origins**: Production Vercel domain, localhost:3000 (dev)
- **Allowed Methods**: GET, POST, PUT, PATCH, DELETE, OPTIONS
- **Allowed Headers**: Content-Type, Authorization, X-Requested-With
- **Credentials**: Allowed (for JWT cookie support if implemented)

## Error Response Format
All error responses follow this standard format:
```json
{
  "error": "Human-readable error message",
  "code": "MACHINE_READABLE_ERROR_CODE",
  "details": {} // Optional details for validation errors
}
```

## Environment-Specific Configuration
- **Development**:
  - Backend: http://localhost:8000
  - Frontend: http://localhost:3000
  - CORS: Allow all origins (not suitable for production)

- **Production**:
  - Backend: [Configurable via environment variable]
  - Frontend: [Vercel deployment URL]
  - CORS: Allow only production domains