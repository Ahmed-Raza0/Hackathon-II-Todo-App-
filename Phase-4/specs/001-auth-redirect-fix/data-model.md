# Data Model: Auth Redirect Fix

## Entities

### User Session
Represents an authenticated user's session state with JWT token and browser cookies

**Attributes:**
- `user_id`: string (subject from JWT token, foreign key to User)
- `token`: string (JWT token stored in httpOnly cookie)
- `expiration`: datetime (token expiration time)
- `created_at`: datetime (session creation timestamp)

**Relationships:**
- One-to-many with Task (session user has many tasks)
- One-to-many with Conversation (session user has many conversations)
- One-to-many with Message (session user has many messages)

**Validation:**
- user_id must be valid UUID format
- token must be valid JWT format
- expiration must be in the future
- created_at must be before expiration

**State Transitions:**
- Active (valid token) → Expired (token expired) → Inactive (session cleared)

### Authentication Request
Represents an authentication attempt from frontend to backend

**Attributes:**
- `email`: string (user's email address)
- `password`: string (user's password, min 8 chars)
- `callback_url`: string (destination after successful auth, default: "/dashboard")
- `credentials_handling`: string (how credentials are included in requests, default: "include")

**Relationships:**
- Many-to-one with User Session (many requests may relate to one session)

**Validation:**
- Email must be valid email format
- Password must be 8-100 characters
- Callback URL must be a valid path in the application
- Credentials handling must be one of: "include", "same-origin", "omit"

## Database Schema Mapping

### Session Storage (Conceptual - handled by Better Auth)
- Session data stored in httpOnly cookies
- JWT tokens validated server-side
- No persistent session records in database (stateless as per constitution)

### Authentication Log (For debugging/tracking if needed)
- `id`: integer (primary key)
- `user_id`: string (foreign key to User)
- `action`: enum('login', 'logout', 'signup', 'refresh')
- `timestamp`: datetime (when action occurred)
- `success`: boolean (whether action succeeded)
- `error_message`: string (if action failed)

## API Contract Mapping

### Authentication Endpoints
- POST `/api/auth/login` → Creates User Session with JWT token
- POST `/api/auth/signup` → Creates User and Session with JWT token
- GET `/api/auth/me` → Validates User Session and returns user info
- POST `/api/auth/logout` → Destroys User Session

### Protected Endpoints
- All `/api/{user_id}/**` endpoints → Require valid User Session
- GET `/api/{user_id}/tasks` → Validates session and filters by user_id
- POST `/api/{user_id}/tasks` → Validates session and associates with user_id
- PUT `/api/{user_id}/tasks/{id}` → Validates session and user ownership
- DELETE `/api/{user_id}/tasks/{id}` → Validates session and user ownership

## Business Rules
1. Sessions must be validated on every protected endpoint
2. User IDs in URL must match the authenticated user's ID from JWT
3. Sessions expire automatically after set duration
4. Failed authentication attempts should not reveal user existence
5. All authentication-related data transmission must be encrypted