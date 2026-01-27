# API Contract: Todo Application Backend

## Overview
This contract defines the API endpoints for the backend service of the Todo application, which will be deployed in the Kubernetes cluster.

## Base URL
The backend service will be accessible internally within the cluster at:
- `http://backend-service.todo-phase4.svc.cluster.local:8000`

## Endpoints

### Authentication Endpoints

#### POST /api/auth/login
Authenticate a user and return a JWT token.

**Request Body:**
```json
{
  "email": "string",
  "password": "string"
}
```

**Response:**
- 200: Successful login
```json
{
  "token": "jwt-token-string",
  "user": {
    "id": "string",
    "email": "string"
  }
}
```
- 401: Invalid credentials

#### POST /api/auth/register
Register a new user.

**Request Body:**
```json
{
  "email": "string",
  "password": "string",
  "name": "string"
}
```

**Response:**
- 201: User created successfully
- 409: User already exists

### Todo Endpoints

#### GET /api/todos
Retrieve all todos for the authenticated user.

**Headers:**
- Authorization: Bearer {token}

**Response:**
- 200: Array of todo items
```json
[
  {
    "id": "string",
    "title": "string",
    "description": "string",
    "completed": "boolean",
    "user_id": "string",
    "created_at": "timestamp",
    "updated_at": "timestamp"
  }
]
```

#### POST /api/todos
Create a new todo item.

**Headers:**
- Authorization: Bearer {token}

**Request Body:**
```json
{
  "title": "string",
  "description": "string",
  "completed": "boolean"
}
```

**Response:**
- 201: Todo created successfully
- 400: Invalid request body

#### PUT /api/todos/{id}
Update an existing todo item.

**Headers:**
- Authorization: Bearer {token}

**Request Body:**
```json
{
  "title": "string",
  "description": "string",
  "completed": "boolean"
}
```

**Response:**
- 200: Todo updated successfully
- 404: Todo not found

#### DELETE /api/todos/{id}
Delete a todo item.

**Headers:**
- Authorization: Bearer {token}

**Response:**
- 204: Todo deleted successfully
- 404: Todo not found

### Health Check Endpoint

#### GET /
Health check endpoint to verify the backend service is running.

**Response:**
- 200: Service is healthy
```json
{
  "status": "healthy",
  "service": "todo-backend",
  "version": "phase4"
}
```