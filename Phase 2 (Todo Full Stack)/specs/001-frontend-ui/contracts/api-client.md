# API Client Contract

**Feature**: Frontend UI for Todo Web Application
**Branch**: `001-frontend-ui`
**Date**: 2026-01-08

---

## Overview

This document specifies the contract between the frontend API client and the backend REST API. It defines all HTTP endpoints, request/response formats, error codes, and client-side behavior for consuming the backend API. The frontend MUST NOT make assumptions beyond this contract; all behavior is defined by the backend API specification.

**Constitutional Alignment**:
- ✅ Principle II: REST API Contract - All endpoints follow RESTful conventions under `/api/*`
- ✅ Principle III: Authentication & Authorization - JWT required for all task endpoints
- ✅ Principle I: User Ownership - Backend enforces user_id filtering, frontend respects responses

---

## Base Configuration

### Environment Variables
```bash
NEXT_PUBLIC_API_BASE_URL=http://localhost:8000  # Backend API base URL
```

### Default Headers
All requests include:
```http
Content-Type: application/json
```

### Authenticated Requests
All `/api/tasks*` endpoints require:
```http
Authorization: Bearer <JWT_TOKEN>
```

### Timeout
- Default: **30 seconds** for all requests
- No custom timeouts per endpoint (simplicity)

### Retry Policy
- **Network errors** (timeout, connection refused): Retry max 2 times with exponential backoff (1s, 2s)
- **4xx errors**: NO retry (client error, user action required)
- **5xx errors**: NO retry (server error, backend issue)

---

## Authentication Endpoints

### POST `/api/auth/signup`

Create a new user account and receive JWT token.

**Request**:
```http
POST /api/auth/signup
Content-Type: application/json

{
  "email": "user@example.com",
  "password": "securepassword123"
}
```

**Request Validation** (client-side before sending):
- Email: Must match `/^[^\s@]+@[^\s@]+\.[^\s@]+$/`
- Password: Minimum 8 characters

**Success Response (201 Created)**:
```json
{
  "user": {
    "id": "550e8400-e29b-41d4-a716-446655440000",
    "email": "user@example.com",
    "createdAt": "2026-01-08T10:30:00.000Z"
  },
  "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
}
```

**Error Responses**:

**400 Bad Request** (Validation Error):
```json
{
  "error": "Validation failed",
  "code": "VALIDATION_ERROR",
  "details": {
    "email": ["Invalid email format"],
    "password": ["Password must be at least 8 characters"]
  }
}
```
→ **Frontend Action**: Display field-specific errors inline in signup form

**409 Conflict** (Email Already Exists):
```json
{
  "error": "An account with this email already exists",
  "code": "EMAIL_EXISTS"
}
```
→ **Frontend Action**: Display error below email input: "An account with this email already exists. Try logging in instead."

**500 Internal Server Error**:
```json
{
  "error": "Internal server error",
  "code": "SERVER_ERROR"
}
```
→ **Frontend Action**: Display toast: "Something went wrong. Please try again later."

---

### POST `/api/auth/login`

Authenticate existing user and receive JWT token.

**Request**:
```http
POST /api/auth/login
Content-Type: application/json

{
  "email": "user@example.com",
  "password": "securepassword123"
}
```

**Request Validation** (client-side before sending):
- Email: Must match email format
- Password: Non-empty

**Success Response (200 OK)**:
```json
{
  "user": {
    "id": "550e8400-e29b-41d4-a716-446655440000",
    "email": "user@example.com",
    "createdAt": "2026-01-08T10:30:00.000Z"
  },
  "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
}
```

**Error Responses**:

**400 Bad Request** (Validation Error):
```json
{
  "error": "Validation failed",
  "code": "VALIDATION_ERROR",
  "details": {
    "email": ["Invalid email format"]
  }
}
```
→ **Frontend Action**: Display field-specific errors inline in login form

**401 Unauthorized** (Invalid Credentials):
```json
{
  "error": "Invalid email or password",
  "code": "INVALID_CREDENTIALS"
}
```
→ **Frontend Action**: Display error below form: "Invalid email or password. Please try again."

**500 Internal Server Error**:
```json
{
  "error": "Internal server error",
  "code": "SERVER_ERROR"
}
```
→ **Frontend Action**: Display toast: "Something went wrong. Please try again later."

---

### POST `/api/auth/logout` (Optional)

Logout user and invalidate token (backend may implement token blacklist).

**Request**:
```http
POST /api/auth/logout
Authorization: Bearer <JWT_TOKEN>
```

**Success Response (200 OK)**:
```json
{
  "message": "Logged out successfully"
}
```

**Error Responses**:

**401 Unauthorized** (Invalid/Expired Token):
```json
{
  "error": "Unauthorized",
  "code": "UNAUTHORIZED"
}
```
→ **Frontend Action**: Clear token anyway (already logged out effectively), redirect to login

**Note**: Frontend MUST clear local JWT token regardless of backend response. Backend logout is optional hygiene (blacklisting tokens).

---

## Task Endpoints

All task endpoints require valid JWT in `Authorization` header.

### GET `/api/tasks`

Retrieve all tasks belonging to the authenticated user.

**Request**:
```http
GET /api/tasks
Authorization: Bearer <JWT_TOKEN>
```

**Query Parameters**: None (pagination, filtering, sorting out of scope for Phase II)

**Success Response (200 OK)**:
```json
{
  "tasks": [
    {
      "id": "123e4567-e89b-12d3-a456-426614174000",
      "title": "Buy groceries",
      "completed": false,
      "userId": "550e8400-e29b-41d4-a716-446655440000",
      "createdAt": "2026-01-08T10:00:00.000Z",
      "updatedAt": "2026-01-08T10:00:00.000Z"
    },
    {
      "id": "987fcdeb-51a2-43d8-b567-321987654321",
      "title": "Finish project report",
      "completed": true,
      "userId": "550e8400-e29b-41d4-a716-446655440000",
      "createdAt": "2026-01-07T14:30:00.000Z",
      "updatedAt": "2026-01-08T09:15:00.000Z"
    }
  ]
}
```

**Empty List Response**:
```json
{
  "tasks": []
}
```
→ **Frontend Action**: Display empty state UI with message "No tasks yet. Create your first task to get started!"

**Error Responses**:

**401 Unauthorized** (Missing/Invalid/Expired Token):
```json
{
  "error": "Unauthorized",
  "code": "UNAUTHORIZED"
}
```
→ **Frontend Action**: Clear auth state, redirect to `/login` with message "Session expired, please log in again"

**500 Internal Server Error**:
```json
{
  "error": "Internal server error",
  "code": "SERVER_ERROR"
}
```
→ **Frontend Action**: Display error page with retry button or toast: "Failed to load tasks. Please try again."

---

### POST `/api/tasks`

Create a new task for the authenticated user.

**Request**:
```http
POST /api/tasks
Authorization: Bearer <JWT_TOKEN>
Content-Type: application/json

{
  "title": "Buy groceries"
}
```

**Request Validation** (client-side before sending):
- Title: Non-empty, max 255 characters, trimmed

**Success Response (201 Created)**:
```json
{
  "task": {
    "id": "123e4567-e89b-12d3-a456-426614174000",
    "title": "Buy groceries",
    "completed": false,
    "userId": "550e8400-e29b-41d4-a716-446655440000",
    "createdAt": "2026-01-08T10:00:00.000Z",
    "updatedAt": "2026-01-08T10:00:00.000Z"
  }
}
```

**Error Responses**:

**400 Bad Request** (Validation Error):
```json
{
  "error": "Validation failed",
  "code": "VALIDATION_ERROR",
  "details": {
    "title": ["Title is required", "Title must be less than 255 characters"]
  }
}
```
→ **Frontend Action**: Display error below task input: "Title is required" or "Title must be less than 255 characters"

**401 Unauthorized**:
```json
{
  "error": "Unauthorized",
  "code": "UNAUTHORIZED"
}
```
→ **Frontend Action**: Clear auth state, redirect to login

**500 Internal Server Error**:
```json
{
  "error": "Internal server error",
  "code": "SERVER_ERROR"
}
```
→ **Frontend Action**: Display toast: "Failed to create task. Please try again."

---

### GET `/api/tasks/:id` (Optional)

Retrieve a single task by ID (may not be needed if list fetch provides all tasks).

**Request**:
```http
GET /api/tasks/123e4567-e89b-12d3-a456-426614174000
Authorization: Bearer <JWT_TOKEN>
```

**Success Response (200 OK)**:
```json
{
  "task": {
    "id": "123e4567-e89b-12d3-a456-426614174000",
    "title": "Buy groceries",
    "completed": false,
    "userId": "550e8400-e29b-41d4-a716-446655440000",
    "createdAt": "2026-01-08T10:00:00.000Z",
    "updatedAt": "2026-01-08T10:00:00.000Z"
  }
}
```

**Error Responses**:

**401 Unauthorized**:
```json
{
  "error": "Unauthorized",
  "code": "UNAUTHORIZED"
}
```
→ **Frontend Action**: Redirect to login

**403 Forbidden** (Task belongs to another user):
```json
{
  "error": "Forbidden",
  "code": "FORBIDDEN"
}
```
→ **Frontend Action**: Display toast: "You don't have permission to access this task"

**404 Not Found** (Task does not exist):
```json
{
  "error": "Task not found",
  "code": "NOT_FOUND"
}
```
→ **Frontend Action**: Display toast: "Task not found" or gracefully remove from local state

**500 Internal Server Error**:
```json
{
  "error": "Internal server error",
  "code": "SERVER_ERROR"
}
```
→ **Frontend Action**: Display toast: "Failed to load task. Please try again."

---

### PATCH `/api/tasks/:id`

Update a task's title (completion status updated via separate toggle endpoint).

**Request**:
```http
PATCH /api/tasks/123e4567-e89b-12d3-a456-426614174000
Authorization: Bearer <JWT_TOKEN>
Content-Type: application/json

{
  "title": "Buy groceries and cook dinner"
}
```

**Request Validation** (client-side before sending):
- Title: Non-empty, max 255 characters, trimmed

**Success Response (200 OK)**:
```json
{
  "task": {
    "id": "123e4567-e89b-12d3-a456-426614174000",
    "title": "Buy groceries and cook dinner",
    "completed": false,
    "userId": "550e8400-e29b-41d4-a716-446655440000",
    "createdAt": "2026-01-08T10:00:00.000Z",
    "updatedAt": "2026-01-08T11:00:00.000Z"
  }
}
```

**Error Responses**:

**400 Bad Request** (Validation Error):
```json
{
  "error": "Validation failed",
  "code": "VALIDATION_ERROR",
  "details": {
    "title": ["Title is required"]
  }
}
```
→ **Frontend Action**: Display error in edit form: "Title is required"

**401 Unauthorized**:
```json
{
  "error": "Unauthorized",
  "code": "UNAUTHORIZED"
}
```
→ **Frontend Action**: Redirect to login

**403 Forbidden** (Task belongs to another user):
```json
{
  "error": "Forbidden",
  "code": "FORBIDDEN"
}
```
→ **Frontend Action**: Display toast: "You don't have permission to edit this task"

**404 Not Found** (Task does not exist):
```json
{
  "error": "Task not found",
  "code": "NOT_FOUND"
}
```
→ **Frontend Action**: Display toast: "Task not found" and remove from local state

**500 Internal Server Error**:
```json
{
  "error": "Internal server error",
  "code": "SERVER_ERROR"
}
```
→ **Frontend Action**: Display toast: "Failed to update task. Please try again."

---

### PATCH `/api/tasks/:id/toggle`

Toggle task completion status (completed ↔ incomplete).

**Request**:
```http
PATCH /api/tasks/123e4567-e89b-12d3-a456-426614174000/toggle
Authorization: Bearer <JWT_TOKEN>
```

**Request Body**: None (or empty JSON `{}`)

**Success Response (200 OK)**:
```json
{
  "task": {
    "id": "123e4567-e89b-12d3-a456-426614174000",
    "title": "Buy groceries",
    "completed": true,
    "userId": "550e8400-e29b-41d4-a716-446655440000",
    "createdAt": "2026-01-08T10:00:00.000Z",
    "updatedAt": "2026-01-08T11:00:00.000Z"
  }
}
```

**Behavior**: Backend toggles `completed` field (false → true or true → false) and updates `updatedAt` timestamp.

**Error Responses**:

**401 Unauthorized**:
```json
{
  "error": "Unauthorized",
  "code": "UNAUTHORIZED"
}
```
→ **Frontend Action**: Redirect to login

**403 Forbidden** (Task belongs to another user):
```json
{
  "error": "Forbidden",
  "code": "FORBIDDEN"
}
```
→ **Frontend Action**: Display toast: "You don't have permission to modify this task"

**404 Not Found** (Task does not exist):
```json
{
  "error": "Task not found",
  "code": "NOT_FOUND"
}
```
→ **Frontend Action**: Display toast: "Task not found" and remove from local state

**500 Internal Server Error**:
```json
{
  "error": "Internal server error",
  "code": "SERVER_ERROR"
}
```
→ **Frontend Action**: Display toast: "Failed to update task. Please try again." and rollback optimistic update

---

### DELETE `/api/tasks/:id`

Delete a task permanently.

**Request**:
```http
DELETE /api/tasks/123e4567-e89b-12d3-a456-426614174000
Authorization: Bearer <JWT_TOKEN>
```

**Success Response (204 No Content)**:
```http
HTTP/1.1 204 No Content
```

**Alternative Success Response (200 OK)** (if backend returns message):
```json
{
  "message": "Task deleted successfully"
}
```

**Error Responses**:

**401 Unauthorized**:
```json
{
  "error": "Unauthorized",
  "code": "UNAUTHORIZED"
}
```
→ **Frontend Action**: Redirect to login

**403 Forbidden** (Task belongs to another user):
```json
{
  "error": "Forbidden",
  "code": "FORBIDDEN"
}
```
→ **Frontend Action**: Display toast: "You don't have permission to delete this task"

**404 Not Found** (Task does not exist):
```json
{
  "error": "Task not found",
  "code": "NOT_FOUND"
}
```
→ **Frontend Action**: Silently remove from local state (already "deleted" effectively)

**500 Internal Server Error**:
```json
{
  "error": "Internal server error",
  "code": "SERVER_ERROR"
}
```
→ **Frontend Action**: Display toast: "Failed to delete task. Please try again."

---

## Error Handling Contract

### Client-Side Error Code Mapping

```typescript
const ERROR_MESSAGES: Record<string, string> = {
  VALIDATION_ERROR: "Please check your input and try again.",
  INVALID_CREDENTIALS: "Invalid email or password.",
  EMAIL_EXISTS: "An account with this email already exists.",
  UNAUTHORIZED: "Your session has expired. Please log in again.",
  FORBIDDEN: "You don't have permission to perform this action.",
  NOT_FOUND: "The requested resource was not found.",
  SERVER_ERROR: "Something went wrong. Please try again later.",
  NETWORK_ERROR: "Network error. Please check your connection and try again.",
};
```

### HTTP Status Code Actions

| Status | Action |
|--------|--------|
| 200/201/204 | Success - Update UI with response data |
| 400 | Display field-specific errors from `details` object or generic message |
| 401 | Clear auth state, redirect to `/login` with "Session expired" message |
| 403 | Display toast: "You don't have permission to perform this action" |
| 404 | Display toast: "Resource not found" or gracefully remove from UI |
| 409 | Display inline error: "An account with this email already exists" |
| 500 | Display toast: "Something went wrong. Please try again later." |
| Network Error | Display toast: "Network error. Please check your connection." |

### Retry Strategy

- **Network Errors** (timeout, connection refused): Retry max 2 times with exponential backoff (1s, 2s)
- **4xx Errors**: NO retry (client error, user must correct input or permissions)
- **5xx Errors**: NO retry (server error, backend must fix; retry unlikely to help immediately)

---

## API Client Implementation Contract

### Required Functions

```typescript
// lib/api/client.ts
export async function apiClient<T>(endpoint: string, options?: RequestInit): Promise<T>;

// lib/api/auth.ts
export async function signup(email: string, password: string): Promise<AuthResponse>;
export async function login(email: string, password: string): Promise<AuthResponse>;
export async function logout(): Promise<void>;

// lib/api/tasks.ts
export async function getTasks(): Promise<Task[]>;
export async function createTask(input: CreateTaskInput): Promise<Task>;
export async function updateTask(id: string, input: UpdateTaskInput): Promise<Task>;
export async function toggleTask(id: string): Promise<Task>;
export async function deleteTask(id: string): Promise<void>;
```

### Interceptor Requirements

**Request Interceptor**:
- Automatically attach `Authorization: Bearer <token>` header to all requests
- Get token from Better Auth session or localStorage
- Skip auth header for `/api/auth/login` and `/api/auth/signup` (public endpoints)

**Response Interceptor**:
- Parse JSON response body
- Check for error responses and throw `APIError` with code, status, message, and details
- Handle 401 globally: clear auth state and redirect to `/login`

---

## Testing Contract

### API Client Mock Behavior

For unit tests, mock API client functions with these behaviors:

**Success Cases**:
- `signup()` → Returns `{ user, token }` after 500ms delay
- `login()` → Returns `{ user, token }` after 500ms delay
- `getTasks()` → Returns `tasks` array after 500ms delay
- `createTask()` → Returns new `task` object with generated ID after 500ms delay
- `toggleTask()` → Returns updated `task` with toggled `completed` after 500ms delay
- `deleteTask()` → Resolves (no return value) after 500ms delay

**Error Cases**:
- Invalid credentials → Throw `APIError` with code `INVALID_CREDENTIALS`, status 401
- Email exists → Throw `APIError` with code `EMAIL_EXISTS`, status 409
- Network error → Throw `APIError` with code `NETWORK_ERROR`, status 0
- Server error → Throw `APIError` with code `SERVER_ERROR`, status 500

---

## Next Steps

1. ✅ API contract defined with all endpoints, requests, responses, error codes
2. → Create `quickstart.md` with development setup instructions
3. → Implement API client in `lib/api/` directory during task execution
4. → Write unit tests for API client functions mocking network layer
