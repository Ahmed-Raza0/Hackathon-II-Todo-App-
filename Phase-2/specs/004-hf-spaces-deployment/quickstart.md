# Quick Start Guide: FastAPI Backend for Hugging Face Spaces

## Overview

This guide provides instructions to set up, develop, and deploy the FastAPI backend for the Todo application to Hugging Face Spaces using Docker.

## Prerequisites

- Python 3.8+
- Docker and Docker Compose
- Git
- Hugging Face Account (for deployment)

## Local Development Setup

### 1. Clone the Repository

```bash
git clone <your-repo-url>
cd <repo-directory>
```

### 2. Set Up Virtual Environment (Optional but Recommended)

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 3. Install Dependencies

```bash
cd backend  # Navigate to the backend directory
pip install -r requirements.txt
```

### 4. Set Up Environment Variables

Create a `.env` file in the backend directory:

```bash
DATABASE_URL=sqlite:///./test.db
BETTER_AUTH_SECRET=your-secret-key
BETTER_AUTH_URL=http://localhost:8000
```

### 5. Run Database Migrations

```bash
# Navigate to the alembic directory
cd alembic
alembic upgrade head
```

### 6. Start the Development Server

```bash
cd src
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

The server will start at `http://localhost:8000`.

## Running with Docker (Local Testing)

### 1. Build the Docker Image

```bash
docker build -t todo-backend .
```

### 2. Run the Container

```bash
docker run -p 8000:8000 -e PORT=8000 todo-backend
```

## Running with Docker Compose (Local Development)

### 1. Create a docker-compose.yml file:

```yaml
version: '3.8'

services:
  backend:
    build: .
    ports:
      - "8000:8000"
    environment:
      - PORT=8000
      - DATABASE_URL=sqlite:///./test.db
    volumes:
      - ./data:/app/data  # For SQLite persistence
    restart: unless-stopped
```

### 2. Start Services

```bash
docker-compose up -d
```

## API Endpoints

Once running, the following endpoints will be available:

- `GET /` - Root endpoint
- `GET /health` - Health check
- `GET /api/{user_id}/tasks` - Get user's tasks
- `POST /api/{user_id}/tasks` - Create a new task
- `GET /api/{user_id}/tasks/{task_id}` - Get a specific task
- `PUT /api/{user_id}/tasks/{task_id}` - Update a task
- `DELETE /api/{user_id}/tasks/{task_id}` - Delete a task
- `PATCH /api/{user_id}/tasks/{task_id}/complete` - Toggle task completion

## Testing the API

### Using curl

```bash
# Health check
curl http://localhost:8000/health

# Get tasks for user (example)
curl http://localhost:8000/api/user123/tasks
```

### Using Python requests

```python
import requests

# Health check
response = requests.get("http://localhost:8000/health")
print(response.json())
```

## Deploying to Hugging Face Spaces

### 1. Prepare Your Repository

1. Ensure your repository has:
   - `Dockerfile` in the root
   - `docker-compose.yml` (optional for local development)
   - `README.md` with proper Hugging Face YAML metadata
   - `requirements.txt` with compatible dependencies
   - Source code in the correct structure

2. Update `README.md` with Hugging Face metadata:

```yaml
---
title: Todo Backend
emoji: 🚀
colorFrom: purple
colorTo: blue
sdk: docker
app_file: src/main.py
pinned: false
license: mit
---

# Todo Backend
```

### 2. Create Hugging Face Space

1. Go to [huggingface.co/spaces](https://huggingface.co/spaces)
2. Click "Create new Space"
3. Select your repository or connect to GitHub
4. Choose "Docker" as SDK
5. Configure your hardware requirements

### 3. Monitor Deployment

Check the "Logs" tab in your Space to monitor the build and deployment process.

## Troubleshooting

### Common Issues

#### Docker Build Failures
- Check that `requirements.txt` is compatible with Hugging Face environment
- Ensure all dependencies can be installed via pip
- Verify base image compatibility

#### Port Binding Issues
- Ensure the application binds to `0.0.0.0` and uses the `$PORT` environment variable
- Check that the Dockerfile exposes the correct port

#### Database Connection Issues
- Verify that SQLite file path is writable in container
- For PostgreSQL/MySQL, ensure connection string format is correct
- Check that database migrations are applied

#### Environment Variables Not Loading
- Ensure environment variables are set correctly in container
- Verify that .env files are loaded in Docker environment

### Useful Commands

```bash
# Check running containers
docker ps

# View container logs
docker logs <container-id>

# Execute commands in running container
docker exec -it <container-id> /bin/bash

# Check environment variables in container
docker run --rm -it <image-name> env
```

## Environment Variables

The application uses the following environment variables:

- `DATABASE_URL`: Database connection string (defaults to SQLite)
- `BETTER_AUTH_SECRET`: Secret key for authentication
- `BETTER_AUTH_URL`: Authentication service URL
- `PORT`: Port number (used in Hugging Face Spaces)

## Next Steps

1. Implement proper error handling
2. Add logging configuration
3. Set up monitoring and metrics
4. Configure automated testing
5. Implement CI/CD pipeline