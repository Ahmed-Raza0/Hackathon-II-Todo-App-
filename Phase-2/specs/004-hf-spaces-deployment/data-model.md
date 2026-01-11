# Data Model: FastAPI Backend for Hugging Face Spaces

## Entity Overview

The backend application manages Todo tasks with associated user data. The data model consists of:

## Core Entities

### Task
**Description**: Represents a single todo task created by a user

**Fields**:
- `id`: String (Primary Key) - Unique identifier for the task
- `title`: String - Title/description of the task
- `description`: String (Optional) - Detailed description of the task
- `status`: String - Status of the task (e.g., "pending", "completed")
- `user_id`: String - ID of the user who owns the task
- `created_at`: DateTime - Timestamp when task was created
- `updated_at`: DateTime - Timestamp when task was last updated

**Validation Rules**:
- `title` must not be empty
- `status` must be one of predefined values (pending, completed)
- `user_id` must exist and be valid

**Relationships**:
- Belongs to a single User (via user_id foreign key)

### User (Implicit)
**Description**: Represents a user who can create and manage tasks

**Fields**:
- `id`: String (Primary Key) - Unique identifier for the user
- `email`: String - User's email address
- `username`: String - User's username
- `created_at`: DateTime - Timestamp when user was created

**Note**: User entity is primarily managed by authentication system but referenced by tasks via user_id.

## Database Configuration

### Environment-Specific Settings

The application supports different database engines based on the deployment environment:

#### Hugging Face Spaces (Production)
- **Engine**: SQLite
- **Connection String**: `sqlite:///./test.db`
- **Features**: File-based storage, single-user access
- **Considerations**: Limited concurrency, file persistence in container

#### Local Development
- **Engine**: PostgreSQL or MySQL (configurable)
- **Connection String**: Environment variable configurable
- **Features**: Full ACID compliance, multi-user support
- **Considerations**: Requires external database server

## API Endpoints Data Flow

### Task Operations

#### GET /api/{user_id}/tasks
- **Request**: User ID path parameter
- **Response**: Array of Task objects
- **Filters**: Optional status parameter

#### POST /api/{user_id}/tasks
- **Request**: User ID path parameter + Task creation data
- **Response**: Created Task object
- **Validation**: Title required, valid status values

#### GET /api/{user_id}/tasks/{task_id}
- **Request**: User ID and Task ID path parameters
- **Response**: Single Task object
- **Validation**: Task must belong to user

#### PUT /api/{user_id}/tasks/{task_id}
- **Request**: User ID, Task ID path parameters + Task update data
- **Response**: Updated Task object
- **Validation**: Task must belong to user

#### DELETE /api/{user_id}/tasks/{task_id}
- **Request**: User ID and Task ID path parameters
- **Response**: 204 No Content
- **Validation**: Task must belong to user

#### PATCH /api/{user_id}/tasks/{task_id}/complete
- **Request**: User ID and Task ID path parameters
- **Response**: Updated Task object
- **Behavior**: Toggles completion status

## Data Validation

### Task Creation
- Title field is required and cannot be empty
- Status field must be one of allowed values
- User ID must match the authenticated user

### Task Updates
- Only the owner can modify their tasks
- Validation rules apply to updated fields
- Updated timestamp is automatically set

## Migration Strategy

### Alembic Configuration
- Support for both SQLite and PostgreSQL/MySQL
- Environment-specific migration scripts
- Automatic schema evolution handling

### Database Initialization
- Create tables if they don't exist
- Apply pending migrations on startup
- Handle database version compatibility