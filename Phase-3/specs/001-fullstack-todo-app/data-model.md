# Data Model: Full-Stack Todo Web App

**Feature**: 001-fullstack-todo-app
**Date**: 2026-01-16
**Status**: Approved

## Entities

### User
**Description**: Represents a registered user with authentication credentials managed by Better Auth
- `id`: UUID (primary key)
- `email`: string (unique, required)
- `name`: string (optional)
- `created_at`: datetime
- `updated_at`: datetime
- `is_active`: boolean (default: true)

**Relationships**: One-to-many with Task (via user_id)

### Task
**Description**: Represents a todo item owned by a specific user, with properties for title, description, completion status, and timestamps
- `id`: UUID (primary key)
- `title`: string (1-200 characters, required)
- `description`: string (optional)
- `completed`: boolean (default: false)
- `user_id`: UUID (foreign key to User.id, required, immutable)
- `created_at`: datetime
- `updated_at`: datetime

**Validation Rules**:
- `title` must be between 1-200 characters
- `user_id` cannot be modified after creation
- `completed` defaults to false
- All tasks must have an owner (user_id required)

**State Transitions**:
- `completed` field can transition from false to true and vice versa

## Database Schema

### Tables
```
users
├── id (UUID, primary key)
├── email (VARCHAR, unique, not null)
├── name (VARCHAR, nullable)
├── created_at (TIMESTAMP, not null)
├── updated_at (TIMESTAMP, not null)
└── is_active (BOOLEAN, not null, default true)

tasks
├── id (UUID, primary key)
├── title (VARCHAR(200), not null)
├── description (TEXT, nullable)
├── completed (BOOLEAN, not null, default false)
├── user_id (UUID, not null, foreign key to users.id)
├── created_at (TIMESTAMP, not null)
└── updated_at (TIMESTAMP, not null)
```

### Constraints
- Foreign key constraint: tasks.user_id references users.id
- Check constraint: length(title) between 1 and 200
- Index on: tasks.user_id for efficient user-based queries

## Relationships
- One User can own many Tasks (one-to-many relationship)
- Each Task must belong to exactly one User
- Referential integrity maintained via foreign key constraint