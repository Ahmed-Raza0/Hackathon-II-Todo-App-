# Research: Backend for Todo Full-Stack Web Application

## Overview
This research document addresses technical decisions and best practices for implementing the secure backend for the Todo Full-Stack Web Application using Python FastAPI, SQLModel, and Neon Serverless PostgreSQL.

## Decision: FastAPI Framework Choice
**Rationale**: FastAPI is selected as the web framework due to its high performance, automatic API documentation generation (Swagger/OpenAPI), built-in validation with Pydantic, and excellent async support. It's well-suited for building REST APIs and has strong community support.

**Alternatives considered**:
- Flask: More minimal but requires more boilerplate code for validation and documentation
- Django: More heavy-weight with built-in admin, but overkill for a simple API backend
- Express.js: Would require switching to Node.js ecosystem, but we're committed to Python

## Decision: SQLModel for ORM
**Rationale**: SQLModel is chosen as the ORM because it's designed by the same author as FastAPI, offers excellent integration, combines SQLAlchemy's power with Pydantic's validation, and supports both sync and async operations. It's perfect for type-hinted, validated database interactions.

**Alternatives considered**:
- SQLAlchemy Core: More complex setup, less validation integration
- Tortoise ORM: Async-native but less mature than SQLModel
- Peewee: Simpler but lacks advanced features and async support

## Decision: PyJWT for Token Handling
**Rationale**: PyJWT is the standard library for handling JWT tokens in Python. It's well-maintained, widely adopted, and integrates well with FastAPI. Combined with cryptography library for secure signing, it provides robust token handling capabilities.

**Alternatives considered**:
- Authlib: More comprehensive but potentially overkill for simple JWT validation
- python-jose: Another JWT library but PyJWT has better maintenance and community support

## Decision: Neon Serverless PostgreSQL
**Rationale**: Neon is selected as the PostgreSQL provider because it offers serverless scaling, built-in branching capabilities, and seamless integration with modern applications. It provides the reliability of PostgreSQL with cloud-native benefits like automatic scaling and reduced costs during low usage.

**Alternatives considered**:
- Standard PostgreSQL on VM: Requires manual scaling and maintenance
- Supabase: Built on PostgreSQL but adds additional abstraction layer that may not be needed
- SQLite: Simpler but lacks the scalability and advanced features of PostgreSQL

## Decision: Authentication Flow
**Rationale**: The backend will implement JWT token verification by extracting the token from the Authorization header, verifying its signature using the BETTER_AUTH_SECRET, and decoding the user_id to enforce user isolation. This approach ensures that all API requests are authenticated and users can only access their own data.

**Implementation approach**:
- Use FastAPI dependencies for authentication middleware
- Create a get_current_user dependency that validates JWT and extracts user_id
- Apply this dependency to all protected endpoints
- Return 401 for invalid tokens and 403 for user mismatches

## Decision: API Endpoint Structure
**Rationale**: Following REST conventions with user_id in the path to ensure clear ownership semantics while maintaining compatibility with the frontend authentication system. The structure `/api/{user_id}/tasks` makes it explicit that operations are scoped to a particular user.

**Endpoint patterns**:
- GET /api/{user_id}/tasks - List user's tasks with optional status filtering
- POST /api/{user_id}/tasks - Create new task for user
- GET /api/{user_id}/tasks/{task_id} - Get specific task for user
- PUT /api/{user_id}/tasks/{task_id} - Update specific task for user
- DELETE /api/{user_id}/tasks/{task_id} - Delete specific task for user
- PATCH /api/{user_id}/tasks/{task_id}/complete - Toggle completion status

## Decision: Error Handling Strategy
**Rationale**: Consistent error responses are crucial for frontend integration. Using structured JSON responses with standard HTTP status codes ensures predictable behavior and proper error handling on the client side.

**Error response format**:
```json
{
  "error": "Human-readable message",
  "code": "MACHINE_READABLE_CODE",
  "details": {}
}
```

**Standard status codes**:
- 200: Success for GET, PUT, PATCH operations
- 201: Success for POST operations (created)
- 400: Bad request (validation errors)
- 401: Unauthorized (missing/invalid JWT)
- 403: Forbidden (user mismatch)
- 404: Not found (resource doesn't exist)
- 500: Internal server error

## Security Considerations
**JWT Best Practices**:
- Use strong secret (BETTER_AUTH_SECRET) for signing
- Set appropriate expiration times
- Validate token signature server-side
- Never trust client-provided user_id without JWT verification
- Implement proper token refresh mechanisms if needed

**Database Security**:
- Always filter queries by user_id
- Use parameterized queries to prevent SQL injection
- Implement proper connection pooling
- Encrypt sensitive data at rest if needed

## Performance Considerations
**Database Optimization**:
- Proper indexing on user_id and created_at columns
- Connection pooling for database operations
- Async operations to handle concurrent requests efficiently
- Pagination for large result sets (future consideration)

**API Optimization**:
- Efficient query patterns
- Caching for frequently accessed data (future consideration)
- Rate limiting to prevent abuse