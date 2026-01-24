# Data Model: Frontend & Backend Login/Signup Integration

## Entities

### User Session
Represents an authenticated user's session state with JWT token and browser cookies

**Attributes:**
- `token`: string (JWT token with HS256 signature)
- `user_id`: string (subject from JWT token, foreign key to User)
- `expiration`: datetime (token expiration time, typically 7 days from issue)
- `cookie_settings`: object (httpOnly, secure, sameSite configuration)

**Relationships:**
- One-to-many with Task (session user has many tasks)
- One-to-many with Conversation (session user has many conversations)
- One-to-many with Message (session user has many messages)

**Validation:**
- token must be valid JWT format
- user_id must match authenticated user
- expiration must be in the future
- cookie_settings must include httpOnly for security

**State Transitions:**
- Unauthenticated → Authenticating → Authenticated → Expired → Unauthenticated

### User Credentials
Represents authentication data for signup and login

**Attributes:**
- `email`: string (required, unique, valid email format)
- `password`: string (required, min 8 chars, max 100 chars)
- `name`: string (optional, max 100 chars)

**Relationships:**
- Part of User Session (credentials used to establish session)

**Validation:**
- email must be valid format and unique
- password must be 8-100 characters with appropriate complexity
- name if provided must be 1-100 characters

### Authentication Handler
Represents the Better Auth integration endpoint and middleware

**Attributes:**
- `route_pattern`: string (e.g., `/api/auth/[...betterauth]/route.ts`)
- `http_methods`: array (GET, POST for auth endpoints)
- `middleware_configuration`: object (session validation, JWT verification)

**Relationships:**
- Handles User Session creation and validation
- Manages User Credentials verification

**Validation:**
- route_pattern must match Next.js App Router convention
- http_methods must include both GET and POST for proper functionality
- middleware_configuration must include JWT verification

## Database Schema Mapping

### Session Storage (Conceptual - handled by Better Auth)
- Session data stored in httpOnly cookies
- JWT tokens validated server-side
- No persistent session records in database (stateless as per constitution)

### User Table (Managed by Better Auth)
- `id`: string (primary key, assigned by Better Auth)
- `email`: string (unique index, assigned by Better Auth)
- `name`: string (assigned by Better Auth)
- `created_at`: datetime (assigned by Better Auth)
- `hashed_password`: string (encrypted, assigned by Better Auth)

### Task Table (Already defined in previous specs)
- `id`: integer (primary key)
- `user_id`: string (foreign key to User.id, indexed)
- `title`: string (1-200 chars, not null)
- `description`: text (nullable, max 1000 chars)
- `completed`: boolean (default false)
- `created_at`: datetime (default current timestamp)
- `updated_at`: datetime (default current timestamp)

### Conversation Table (For Phase III AI Chatbot)
- `id`: integer (primary key)
- `user_id`: string (foreign key to User.id, indexed)
- `created_at`: datetime (default current timestamp)
- `updated_at`: datetime (default current timestamp)

### Message Table (For Phase III AI Chatbot)
- `id`: integer (primary key)
- `user_id`: string (foreign key to User.id, indexed)
- `conversation_id`: integer (foreign key to Conversation.id, indexed)
- `role`: enum ('user', 'assistant')
- `content`: text (max 5000 chars)
- `created_at`: datetime (default current timestamp)

## API Contract Mapping

### Authentication Endpoints
- POST `/api/auth/signup` → Creates User Session with JWT token
- POST `/api/auth/login` → Validates User Credentials, restores session
- GET `/api/auth/me` → Validates User Session, returns user info
- POST `/api/auth/logout` → Clears User Session (optional)

### Protected Endpoints
- All `/api/{user_id}/**` endpoints → Require valid User Session
- GET `/api/{user_id}/tasks` → Validates session, filters by user_id
- POST `/api/{user_id}/tasks` → Validates session, associates with user_id
- PUT `/api/{user_id}/tasks/{id}` → Validates session and user ownership
- DELETE `/api/{user_id}/tasks/{id}` → Validates session and user ownership

## Business Rules
1. Sessions must be validated on every protected endpoint
2. User IDs in URL must match the authenticated user's ID from JWT
3. Sessions expire automatically after set duration (7 days)
4. Failed authentication attempts should not reveal user existence
5. All authentication-related data transmission must be encrypted
6. Passwords must be hashed before storage using bcrypt algorithm
7. JWT tokens must include proper expiration times
8. Users can only access their own data based on user_id filtering