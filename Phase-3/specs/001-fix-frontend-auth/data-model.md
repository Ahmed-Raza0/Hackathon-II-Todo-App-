# Data Model: Frontend Authentication Integration

## Entities

### User
Represents a registered user in the system with authentication credentials

**Attributes:**
- `id`: string (primary key, assigned by system)
- `email`: string (unique, required, valid email format)
- `hashed_password`: string (required, bcrypt hashed)
- `name`: string (optional, max 100 chars)
- `created_at`: datetime (timestamp of account creation)
- `updated_at`: datetime (timestamp of last update)

**Validation:**
- Email: valid email format, unique across all users
- Password: minimum 8 characters (validation occurs before hashing)
- Name: optional, 0-100 characters

**Relationships:**
- One-to-many with Task (user has many tasks)
- One-to-many with Conversation (user has many conversations)
- One-to-many with Message (user has many messages)

### User Session
Represents an authenticated user's session state with JWT token

**Attributes:**
- `token`: string (JWT token with HS256 signature)
- `user_id`: string (reference to User.id from token payload)
- `expiration`: datetime (token expiration time, typically 7 days from issue)
- `created_at`: datetime (time token was issued)

**Validation:**
- Token: valid JWT format with proper signature
- User_id: must correspond to an existing user
- Expiration: must be in the future

**State Transitions:**
- Unauthenticated → Authenticating → Authenticated → Expired → Unauthenticated

### Authentication Request
Represents a communication between frontend and backend for auth operations

**Attributes:**
- `endpoint`: string (e.g., "/api/auth/signup", "/api/auth/login")
- `method`: enum (POST, GET)
- `headers`: object (includes Authorization header when applicable)
- `payload_format`: object (email, password for login; email, password, name for signup)
- `response_handling`: object (how frontend processes backend responses)

**Validation:**
- Endpoint: must be valid auth endpoint
- Method: must be allowed for the endpoint
- Payload: must conform to endpoint's schema

### User Credentials
Represents authentication data submitted by user

**Attributes:**
- `email`: string (required, valid email format)
- `password`: string (required, min 8 chars, max 100 chars)
- `name`: string (optional, for signup only, max 100 chars)
- `validation_rules`: object (format, length, strength requirements)

**Validation:**
- Email: must be valid email format
- Password: must be 8-100 characters with sufficient complexity
- Name: if provided, must be 1-100 characters

## Database Schema Mapping

### Users Table
```
users
├── id (string, PK, not null)
├── email (string, unique, not null)
├── hashed_password (string, not null)
├── name (string, nullable)
├── created_at (datetime, default now)
└── updated_at (datetime, default now)
```

**Indexes:**
- `users.email` - for authentication lookups

### Session Storage (Conceptual - handled by JWT)
- JWT tokens stored in localStorage on frontend
- Backend validates tokens statelessly using signature verification
- No persistent session records in database (stateless as per constitution)

## API Contract Mapping

### Authentication Endpoints
- POST `/api/auth/signup` → Creates User record, returns JWT token
- POST `/api/auth/login` → Validates User credentials, returns JWT token
- GET `/api/auth/me` → Validates JWT, returns User information
- POST `/api/auth/logout` → Invalidates session (optional)

### Protected Endpoints
- All `/api/{user_id}/**` endpoints → Require valid JWT in Authorization header
- GET `/api/{user_id}/tasks` → Validates JWT and filters by user_id
- POST `/api/{user_id}/tasks` → Validates JWT and associates with user_id
- PUT `/api/{user_id}/tasks/{id}` → Validates JWT and user ownership
- DELETE `/api/{user_id}/tasks/{id}` → Validates JWT and user ownership

## Business Rules
1. Users must authenticate before accessing protected resources
2. Passwords must be hashed before storage using bcrypt
3. JWT tokens must include proper expiration times
4. All authenticated requests must include valid JWT in Authorization header
5. Users can only access their own data based on user_id from JWT
6. Authentication failures should return appropriate error messages without revealing user existence
7. Session tokens must persist across page refreshes and navigation
8. Expired tokens must result in automatic logout or re-authentication requirement