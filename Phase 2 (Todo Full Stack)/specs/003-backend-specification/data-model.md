# Data Model: Backend for Todo Full-Stack Web Application

## Overview
This document defines the database schema and data models for the Todo Full-Stack Web Application backend. The models are designed to support the functional requirements while enforcing user isolation and data integrity.

## Task Model

### Fields
- **id** (UUID/Integer): Primary key, auto-generated unique identifier for each task
- **title** (String, NOT NULL): The task title/description, required field
- **description** (Text, nullable): Optional detailed description of the task
- **status** (Enum: pending/completed, default: pending): Current status of the task
- **user_id** (String/UUID, NOT NULL): Foreign key linking to the user who owns the task
- **created_at** (DateTime, default: now): Timestamp when the task was created
- **updated_at** (DateTime, default: now): Timestamp when the task was last updated

### Relationships
- **user_id** references the user identifier from JWT token
- Tasks are strongly associated with a single user and cannot exist without a valid user_id

### Validation Rules
- title must not be empty (length > 0)
- status must be one of: 'pending', 'completed'
- user_id must match the authenticated user's ID from JWT token
- created_at and updated_at are managed automatically by the system

### State Transitions
- Status can transition from 'pending' to 'completed'
- Status can transition from 'completed' to 'pending'
- Status changes are idempotent (changing completed task to completed keeps it completed)

## User Concept (Implicit)

### Fields
- **user_id** (String/UUID): Unique identifier extracted from JWT token
- No explicit User table is required as authentication is handled externally by Better Auth
- User identity is validated through JWT verification

### Validation Rules
- All operations must validate that the user_id from JWT matches the requested user context
- No direct user management operations are supported by this backend
- User authentication is verified through JWT token validation

## Indexing Strategy

### Required Indexes
- **tasks.user_id**: Essential for efficient user-based filtering and enforcing user isolation
- **tasks.created_at**: Important for sorting and pagination of task lists
- **tasks.status**: Beneficial for filtering by status (pending/completed)

### Query Patterns
- `SELECT * FROM tasks WHERE user_id = ?`: Primary query pattern for listing user's tasks
- `SELECT * FROM tasks WHERE user_id = ? AND status = ?`: Filtered query for status-based views
- `SELECT * FROM tasks WHERE user_id = ? AND id = ?`: Individual task retrieval with user verification

## Constraints

### Database-Level Constraints
- Foreign key constraint on user_id (references external user system)
- NOT NULL constraints on critical fields (id, title, user_id)
- Check constraint on status field (must be 'pending' or 'completed')

### Application-Level Constraints
- All queries must filter by user_id to enforce isolation
- User ID from JWT must match the requested user context in API endpoints
- Task ownership cannot be transferred between users

## Security Considerations

### Data Access Controls
- Database queries must always include user_id in WHERE clause
- Direct access to tasks without user_id filtering is prohibited
- Cross-user data access is prevented at both application and database levels

### Privacy Protection
- No personally identifiable information stored in task records
- User identification relies on external authentication system
- Task content is isolated by user_id foreign key relationship