# Quickstart Guide: Hugging Face Spaces Database Fallback

**Feature**: Hugging Face Spaces Database Fallback
**Date**: 2026-01-11

## Overview

This guide provides a quick overview of the database fallback mechanism that enables FastAPI backend deployment to Hugging Face Spaces while maintaining PostgreSQL compatibility for local development.

## Key Features

- **Automatic Fallback**: Automatically switches to SQLite when PostgreSQL configuration is missing or invalid
- **Zero Downtime**: Application never crashes during startup regardless of database configuration
- **Environment Agnostic**: Works consistently across local development, testing, and production
- **Backward Compatible**: Existing PostgreSQL configurations continue to work unchanged

## Configuration

### Environment Variables

The system supports the following environment variables:

```bash
# Primary database URL (optional - fallback to SQLite if not provided)
DATABASE_URL=postgresql://user:password@localhost:5432/mydatabase

# These variables are optional and only used if you want to customize the fallback
# FALLBACK_DATABASE_URL=sqlite:///./production.db  # Default fallback location
# DATABASE_TIMEOUT=30                            # Connection timeout in seconds
# DATABASE_POOL_SIZE=5                          # Connection pool size
```

### Default Behavior

If no `DATABASE_URL` is provided:
- The application automatically uses SQLite at `./production.db`
- All database operations continue to work normally
- No application changes required

## Architecture

### Database URL Resolution Flow

```
Start
  ↓
Check DATABASE_URL Environment Variable
  ↓
┌─────────────────┐ ┌──────────────────┐
│ DATABASE_URL    │ │ DATABASE_URL     │
│ Present & Valid │ │ Missing/Invalid  │
└─────────────────┘ └──────────────────┘
        ↓                       ↓
  Connect to Primary      Use Fallback
    Database               SQLite
        ↓                       ↓
   ┌─────────────┐      ┌─────────────┐
   │ Success?    │      │ Success?    │
   └─────────────┘      └─────────────┘
         ↓                   ↓
    ┌─────────┐         ┌─────────┐
    │Healthy  │         │Healthy  │
    │Primary │         │Fallback │
    └─────────┘         └─────────┘
```

### Key Components

1. **DatabaseURLResolver**: Determines which database URL to use based on validation
2. **DatabaseEngineFactory**: Creates SQLAlchemy engines safely with appropriate configuration
3. **DatabaseSessionFactory**: Provides database sessions to FastAPI endpoints
4. **HealthChecker**: Monitors database connection status and reports health

## Deployment to Hugging Face Spaces

### Repository Structure

Your repository should contain:
```
├── Dockerfile
├── README.md (with Hugging Face metadata)
├── requirements.txt
├── src/
│   ├── main.py
│   ├── config/
│   │   └── settings.py
│   └── database/
│       └── session.py
└── alembic/
```

### Hugging Face Configuration

In your `README.md`, include the following metadata:

```yaml
---
title: "Your App Name"
emoji: "🚀"
colorFrom: "blue"
colorTo: "green"
sdk: "docker"
sdk_version: "latest"
app_file: "src/main.py"
pinned: false
---
```

### Docker Configuration

The Dockerfile should:
- Use Python 3.11 base image
- Install dependencies from requirements.txt
- Copy application code to /app directory
- Expose port 7860
- Run the application with: `CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "7860"]`

## Local Development

### With PostgreSQL (Existing Workflow)

```bash
# Set your DATABASE_URL
export DATABASE_URL=postgresql://user:password@localhost:5432/mydatabase

# Run the application normally
uvicorn src.main:app --reload
```

### With SQLite (New Workflow)

```bash
# Don't set DATABASE_URL, or set it to empty
unset DATABASE_URL

# Run the application - it will automatically use SQLite
uvicorn src.main:app --reload
```

## Health Monitoring

### Health Endpoint

Access the health status at `/health` endpoint:

```bash
curl http://localhost:8000/health
```

Response:
```json
{
  "status": "healthy",
  "timestamp": "2026-01-11T09:30:00Z",
  "database_status": "connected",
  "database_type": "sqlite",
  "fallback_active": true
}
```

### Database Configuration Endpoint

View current database configuration:

```bash
curl http://localhost:8000/config/database
```

## Troubleshooting

### Application Won't Start

- Check that `DATABASE_URL` is properly formatted if provided
- Ensure the SQLite database file location is writable
- Verify that all required dependencies are in `requirements.txt`

### Database Operations Fail

- Confirm that the database user has appropriate permissions
- Check that the database server is running and accessible
- Verify that connection limits are not exceeded

### Fallback Isn't Working

- Verify that the fallback database file path is writable
- Check that the application has permission to create the database file
- Review application logs for validation errors

## Best Practices

### For Production

- Monitor the health endpoint to track fallback activation
- Set up alerts for when fallback mode becomes active
- Regularly test both primary and fallback configurations

### For Development

- Test with both PostgreSQL and SQLite configurations
- Verify that all database operations work with both database types
- Use the health endpoint to confirm database connectivity

### For Testing

- Include tests that verify fallback behavior
- Test database operations with both primary and fallback configurations
- Verify that the application handles database errors gracefully