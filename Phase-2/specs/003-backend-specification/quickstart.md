# Quickstart Guide: Backend for Todo Full-Stack Web Application

## Overview
This guide provides essential information to quickly set up and run the backend service for the Todo Full-Stack Web Application.

## Prerequisites
- Python 3.11+
- pip package manager
- Access to Neon Serverless PostgreSQL database
- Better Auth secret for JWT verification

## Setup Instructions

### 1. Clone the Repository
```bash
git clone <repository-url>
cd <repository-directory>
```

### 2. Create Virtual Environment
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Configure Environment Variables
Create a `.env` file based on the example:
```bash
cp .env.example .env
```

Update the `.env` file with your specific configuration:
```env
BETTER_AUTH_SECRET=your_better_auth_secret_here
BETTER_AUTH_URL=https://your-domain.better-auth.com
DATABASE_URL=postgresql://username:password@ep-xxx.us-east-1.aws.neon.tech/dbname
```

### 5. Run the Application
```bash
# For development
uvicorn src.main:app --reload --port 8000

# For production
gunicorn src.main:app -w 4 -k uvicorn.workers.UvicornWorker --bind 0.0.0.0:8000
```

## API Usage

### Authentication
All API endpoints require a valid JWT token in the Authorization header:
```
Authorization: Bearer <jwt_token>
```

### Available Endpoints

#### List User's Tasks
```
GET /api/{user_id}/tasks
```
Optional query parameter: `status` (all, pending, completed)

#### Create New Task
```
POST /api/{user_id}/tasks
Content-Type: application/json

{
  "title": "Task title",
  "description": "Optional description"
}
```

#### Get Specific Task
```
GET /api/{user_id}/tasks/{task_id}
```

#### Update Task
```
PUT /api/{user_id}/tasks/{task_id}
Content-Type: application/json

{
  "title": "Updated title",
  "description": "Updated description"
}
```

#### Delete Task
```
DELETE /api/{user_id}/tasks/{task_id}
```

#### Toggle Task Completion
```
PATCH /api/{user_id}/tasks/{task_id}/complete
```

## Testing

### Run Unit Tests
```bash
pytest tests/unit/
```

### Run Integration Tests
```bash
pytest tests/integration/
```

### Run All Tests
```bash
pytest tests/
```

## Development Commands

### Format Code
```bash
black src/
```

### Lint Code
```bash
flake8 src/
```

### Generate API Documentation
The API documentation is automatically available at `/docs` when running the development server.

## Troubleshooting

### Common Issues
1. **JWT Validation Errors**: Verify that `BETTER_AUTH_SECRET` matches the one used by your frontend authentication
2. **Database Connection Errors**: Check that `DATABASE_URL` is correctly formatted and accessible
3. **User Isolation Failures**: Ensure that the `user_id` in JWT matches the one in the API path

### Enable Debug Logging
Set the LOG_LEVEL environment variable to "debug":
```bash
export LOG_LEVEL=debug
```