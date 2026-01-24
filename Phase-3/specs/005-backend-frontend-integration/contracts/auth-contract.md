# API Contract: Authentication Endpoints

## Authentication Endpoints

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

**Error Responses:**
- 401: Invalid credentials
- 400: Invalid request format

### POST /api/auth/signup
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

**Error Responses:**
- 400: Invalid request format or weak password
- 409: Email already exists

### GET /api/auth/me
Get current user information

**Headers:**
```
Authorization: Bearer {jwt_token}
```

**Response (200 OK):**
```json
{
  "user_id": "user_123456789",
  "email": "user@example.com",
  "name": "John Doe"
}
```

**Error Responses:**
- 401: Invalid or expired token

### POST /api/auth/logout
Logout from the application

**Headers:**
```
Authorization: Bearer {jwt_token}
```

**Response (200 OK):**
```json
{
  "success": true,
  "message": "Logged out successfully"
}
```

**Error Responses:**
- 401: Invalid or expired token