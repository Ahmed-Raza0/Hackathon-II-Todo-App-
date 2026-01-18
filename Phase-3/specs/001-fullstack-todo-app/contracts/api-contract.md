# API Contracts: Full-Stack Todo Web App

**Feature**: 001-fullstack-todo-app
**Date**: 2026-01-16
**Status**: Approved

## Authentication Contract

### JWT Token Format
- Header: `Authorization: Bearer <jwt_token>`
- Token payload includes: `user_id`, `exp`, `iat`
- Token must be validated on all protected endpoints

### Authentication Failures
- Invalid/expired token → `401 Unauthorized`
- Missing token → `401 Unauthorized`
- Token user_id mismatch with resource owner → `403 Forbidden`

## API Endpoints

### Task Operations

#### Create Task
```
POST /api/tasks
```

**Headers**:
- `Authorization: Bearer <token>`

**Request Body**:
```json
{
  "title": "string (1-200 chars)",
  "description": "string (optional)"
}
```

**Success Response (201)**:
```json
{
  "id": "UUID",
  "title": "string",
  "description": "string or null",
  "completed": false,
  "user_id": "UUID",
  "created_at": "datetime",
  "updated_at": "datetime"
}
```

**Error Responses**:
- `400 Bad Request`: Invalid input (title too long/empty)
- `401 Unauthorized`: Invalid/missing JWT
- `500 Internal Server Error`: Database error

---

#### List Tasks
```
GET /api/tasks
```

**Headers**:
- `Authorization: Bearer <token>`

**Query Parameters**:
- `completed`: boolean (optional filter)
- `limit`: integer (optional, default 50)
- `offset`: integer (optional, default 0)

**Success Response (200)**:
```json
{
  "tasks": [
    {
      "id": "UUID",
      "title": "string",
      "description": "string or null",
      "completed": "boolean",
      "user_id": "UUID",
      "created_at": "datetime",
      "updated_at": "datetime"
    }
  ],
  "total": "integer",
  "limit": "integer",
  "offset": "integer"
}
```

**Error Responses**:
- `401 Unauthorized`: Invalid/missing JWT
- `500 Internal Server Error`: Database error

---

#### Get Task
```
GET /api/tasks/{task_id}
```

**Headers**:
- `Authorization: Bearer <token>`

**Success Response (200)**:
```json
{
  "id": "UUID",
  "title": "string",
  "description": "string or null",
  "completed": "boolean",
  "user_id": "UUID",
  "created_at": "datetime",
  "updated_at": "datetime"
}
```

**Error Responses**:
- `401 Unauthorized`: Invalid/missing JWT
- `403 Forbidden`: Task doesn't belong to user
- `404 Not Found`: Task doesn't exist
- `500 Internal Server Error`: Database error

---

#### Update Task
```
PUT /api/tasks/{task_id}
```

**Headers**:
- `Authorization: Bearer <token>`

**Request Body**:
```json
{
  "title": "string (1-200 chars)",
  "description": "string (optional)",
  "completed": "boolean"
}
```

**Success Response (200)**:
```json
{
  "id": "UUID",
  "title": "string",
  "description": "string or null",
  "completed": "boolean",
  "user_id": "UUID",
  "created_at": "datetime",
  "updated_at": "datetime"
}
```

**Error Responses**:
- `400 Bad Request`: Invalid input
- `401 Unauthorized`: Invalid/missing JWT
- `403 Forbidden`: Task doesn't belong to user
- `404 Not Found`: Task doesn't exist
- `500 Internal Server Error`: Database error

---

#### Complete Task
```
PATCH /api/tasks/{task_id}/complete
```

**Headers**:
- `Authorization: Bearer <token>`

**Request Body**:
```json
{
  "completed": true
}
```

**Success Response (200)**:
```json
{
  "id": "UUID",
  "title": "string",
  "description": "string or null",
  "completed": true,
  "user_id": "UUID",
  "created_at": "datetime",
  "updated_at": "datetime"
}
```

**Error Responses**:
- `400 Bad Request`: Invalid input
- `401 Unauthorized`: Invalid/missing JWT
- `403 Forbidden`: Task doesn't belong to user
- `404 Not Found`: Task doesn't exist
- `500 Internal Server Error`: Database error

---

#### Delete Task
```
DELETE /api/tasks/{task_id}
```

**Headers**:
- `Authorization: Bearer <token>`

**Success Response (204)**: No content

**Error Responses**:
- `401 Unauthorized`: Invalid/missing JWT
- `403 Forbidden`: Task doesn't belong to user
- `404 Not Found`: Task doesn't exist
- `500 Internal Server Error`: Database error

---

## Error Response Format

All errors follow this standard format:

```json
{
  "error": "Descriptive error message",
  "code": "ERROR_CODE",
  "timestamp": "ISO 8601 datetime"
}
```

**Common Error Codes**:
- `AUTHENTICATION_FAILED`: Invalid or missing JWT
- `AUTHORIZATION_FAILED`: User not authorized for resource
- `VALIDATION_ERROR`: Request validation failed
- `RESOURCE_NOT_FOUND`: Requested resource doesn't exist
- `INTERNAL_ERROR`: Unexpected server error