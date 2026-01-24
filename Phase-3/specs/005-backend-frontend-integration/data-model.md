# Data Model: Backend-Frontend Integration

## Entities

### User Session
Represents an authenticated user's session state for API communication

**Attributes:**
- `token`: string (JWT token)
- `user_id`: string (identifier from JWT claims)
- `expiration`: timestamp (token expiration time)

**Validation:**
- Token must be valid JWT format
- User_id must match the authenticated user
- Expiration must be in the future

### API Request
Represents a communication between frontend and backend with authentication context

**Attributes:**
- `endpoint`: string (API endpoint path)
- `method`: enum(GET, POST, PUT, DELETE, PATCH)
- `headers`: object (HTTP headers including Authorization)
- `body`: object (request payload, optional)
- `authenticated_user_id`: string (extracted from JWT, if authenticated)

**Validation:**
- Endpoint must be valid API path
- Method must be one of allowed HTTP methods
- Headers must include valid JWT if endpoint requires authentication
- Body must conform to endpoint's schema if required

## Database Schema Mapping

### User Session (Conceptual - actual handled by Better Auth)
- Stored in JWT format in client-side storage
- Verified server-side using python-jose
- Contains user_id claim for authorization

### Task Entity (Already defined in backend models)
- `id`: integer (primary key)
- `user_id`: string (foreign key to user)
- `title`: string (1-200 chars)
- `description`: string (optional, max 1000 chars)
- `completed`: boolean (default false)
- `created_at`: timestamp
- `updated_at`: timestamp

## API Contract Mapping

### Authentication Endpoints
- `/api/auth/login` → Creates JWT token with user_id
- `/api/auth/signup` → Creates user and returns JWT token
- `/api/auth/me` → Validates JWT and returns user info

### Task Endpoints
- `/api/{user_id}/tasks` → Requires JWT, filters by user_id
- `/api/{user_id}/tasks/{id}` → Requires JWT, validates user owns task

## State Transition Diagrams

### API Request Processing
```
Incoming Request → JWT Validation → User Context Extraction → Business Logic → Response
                              ↓
                         Invalid Token → 401 Unauthorized Response
```

### Authentication Flow
```
User Request → No Token → Redirect to Login
              ↓
        Has Token → Validate Token → Valid → Proceed with Request
                                    ↓
                                  Invalid → Redirect to Login
```

## Business Rules
1. All API requests to protected endpoints must include valid JWT
2. JWT validation must occur before processing request
3. User context must be extracted from JWT for authorization
4. Requests must be filtered by authenticated user's context
5. Error responses must include appropriate HTTP status codes