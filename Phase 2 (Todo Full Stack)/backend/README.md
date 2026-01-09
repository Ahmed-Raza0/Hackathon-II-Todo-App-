# Todo Backend API

A secure, production-ready backend for the Todo Full-Stack Web Application using Python FastAPI with JWT authentication and Neon Serverless PostgreSQL.

## Features

- Secure JWT-based authentication compatible with Better Auth
- RESTful API endpoints for task management
- User isolation - users can only access their own tasks
- CRUD operations for tasks (Create, Read, Update, Delete)
- Task status management (pending/completed)
- Status filtering capability
- Structured JSON error responses
- Comprehensive error handling

## Tech Stack

- Python 3.11
- FastAPI - web framework with automatic API documentation
- SQLModel - SQL toolkit and ORM combining SQLAlchemy and Pydantic
- PyJWT - JWT token handling
- Neon Serverless PostgreSQL - cloud database
- Uvicorn - ASGI server

## API Endpoints

All endpoints require a valid JWT token in the Authorization header:

```
Authorization: Bearer <jwt_token>
```

### Task Management

- `GET /api/{user_id}/tasks` - List user's tasks with optional status filtering
- `POST /api/{user_id}/tasks` - Create a new task
- `GET /api/{user_id}/tasks/{task_id}` - Get a specific task
- `PUT /api/{user_id}/tasks/{task_id}` - Update a task
- `DELETE /api/{user_id}/tasks/{task_id}` - Delete a task
- `PATCH /api/{user_id}/tasks/{task_id}/complete` - Toggle task completion status

## Environment Variables

Create a `.env` file with the following variables:

```env
BETTER_AUTH_SECRET=your_better_auth_secret_here
BETTER_AUTH_URL=https://your-domain.better-auth.com
DATABASE_URL=postgresql://username:password@localhost:5432/todo_db
```

## Setup and Installation

1. Clone the repository
2. Navigate to the backend directory
3. Create a virtual environment:

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

4. Install dependencies:

```bash
pip install -r requirements.txt
```

5. Set up environment variables in `.env` file

6. Run the application:

```bash
uvicorn src.main:app --reload --port 8000
```

## Running Tests

```bash
# Run all tests
pytest

# Run unit tests
pytest tests/unit/

# Run integration tests
pytest tests/integration/
```

## Docker Deployment

Build and run with Docker Compose:

```bash
docker-compose up --build
```

The API will be available at `http://localhost:8000`.

## Health Check

Check the health of the application at:

```
GET /
GET /health
```

## Error Handling

The API returns structured JSON error responses:

```json
{
  "detail": "Error message"
}
```

Common HTTP status codes:
- 200: Success
- 201: Created
- 204: No Content (successful deletion)
- 400: Bad Request (validation error)
- 401: Unauthorized (invalid/missing JWT)
- 403: Forbidden (user mismatch)
- 404: Not Found (resource doesn't exist)
- 500: Internal Server Error