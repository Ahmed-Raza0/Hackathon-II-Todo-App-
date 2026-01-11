# Deployment Guide: Todo Backend on Hugging Face Spaces

## Overview

This guide describes how to deploy the Todo Backend application to Hugging Face Spaces using the Docker SDK.

## Prerequisites

- A Hugging Face account
- Git repository with the backend code
- Docker SDK enabled on your Hugging Face Space

## Deployment Steps

### 1. Prepare Your Repository

Ensure your repository contains:

```
├── Dockerfile
├── README.md (with Hugging Face metadata)
├── requirements.txt
├── src/
│   ├── main.py
│   ├── config/
│   ├── database/
│   └── api/
├── docs/
└── alembic/
```

### 2. Verify Hugging Face Metadata

Ensure your `README.md` contains the proper Hugging Face configuration:

```yaml
---
title: "Todo App Backend"
emoji: "📝"
colorFrom: "blue"
colorTo: "green"
sdk: "docker"
sdk_version: "latest"
app_file: "src/main.py"
pinned: false
---
```

### 3. Configure the Dockerfile

Your Dockerfile should:

- Use Python 3.11 base image
- Expose port 7860
- Run on 0.0.0.0:7860
- Copy all necessary application files

### 4. Create Your Hugging Face Space

1. Go to [huggingface.co/spaces](https://huggingface.co/spaces)
2. Click "Create new Space"
3. Select your repository or import from GitHub
4. Choose "Docker" as the SDK
5. Select the appropriate hardware

### 5. Push Your Code

```bash
git add .
git commit -m "Deploy to Hugging Face Spaces with database fallback"
git push origin main
```

## Application Behavior on Hugging Face

### Automatic Configuration

When deployed to Hugging Face Spaces, the application automatically:

- Falls back to SQLite database (no DATABASE_URL needed)
- Runs on port 7860 (as required by Hugging Face)
- Binds to 0.0.0.0 for external access
- Disables SQL logging for cleaner logs
- Handles all startup errors gracefully

### Database Configuration

- **No DATABASE_URL provided** → Uses SQLite (`sqlite:///./production.db`)
- **Invalid DATABASE_URL provided** → Falls back to SQLite with warning
- **Valid DATABASE_URL provided** → Uses specified database

### Environment Variables

The application does not require any environment variables for basic operation, but you can still provide:

- `BETTER_AUTH_SECRET` - Required for authentication
- `BETTER_AUTH_URL` - Required for authentication

## Monitoring and Health Checks

### Health Endpoints

- `GET /health` - Basic health status
- `GET /ready` - Container readiness
- `GET /status` - Detailed status including database info

### Expected Responses

**Health Check:**
```json
{
  "status": "healthy"
}
```

**Status Check:**
```json
{
  "status": "healthy",
  "database_type": "sqlite",
  "database_url_preview": "sqlite://***",
  "fallback_active": true,
  "timestamp": "2026-01-11T09:30:00.000000"
}
```

## Troubleshooting

### Common Issues

1. **Build Fails**
   - Check that all dependencies in requirements.txt are available
   - Verify Dockerfile syntax
   - Ensure no missing files

2. **Container Won't Start**
   - Check logs for database URL resolution messages
   - Verify that the application binds to port 7860
   - Confirm that the CMD instruction in Dockerfile is correct

3. **Database Issues**
   - The application should automatically fall back to SQLite
   - Check that the SQLite database file is writable
   - Look for "falling back to SQLite" messages in logs

### Logs to Monitor

Look for these messages in the Hugging Face Space logs:

```
Falling back to SQLite database: sqlite:///./production.db
App imported successfully
INFO:     Application startup complete.
```

## Local Development vs. Hugging Face

| Environment | Database | Configuration | Port |
|-------------|----------|---------------|------|
| Local | PostgreSQL (if DATABASE_URL set) | Manual setup | 8000 |
| Hugging Face | SQLite (automatic fallback) | Automatic | 7860 |

## Best Practices

1. **Test Locally First**: Test the Docker build locally before pushing to Hugging Face
2. **Monitor Logs**: Watch the space logs during initial deployment
3. **Environment Variables**: Set required auth variables in Space Secrets if needed
4. **Database Migration**: For SQLite, schema changes are handled automatically by SQLModel
5. **Health Checks**: Use the `/status` endpoint to verify database configuration

## Scaling Considerations

- SQLite is sufficient for small to medium workloads
- For heavy write loads, consider adding a PostgreSQL database later
- The fallback mechanism allows easy migration from SQLite to PostgreSQL

## Rollback Plan

If deployment issues occur:

1. Check the application logs in Hugging Face Space
2. Verify that the Docker image builds successfully
3. Test the same configuration locally
4. Revert to a previous working commit if needed