# Environment Configuration Guide

## Overview

This guide explains how to configure the application for different environments (local development, testing, production, Hugging Face Spaces).

## Environment Variables

### Required Variables (All Environments)

| Variable | Description | Example |
|----------|-------------|---------|
| `BETTER_AUTH_SECRET` | Secret key for Better Auth | `your-super-secret-key` |
| `BETTER_AUTH_URL` | Better Auth URL | `https://your-domain.better-auth.com` |

### Optional Variables

| Variable | Description | Default | Used In |
|----------|-------------|---------|---------|
| `DATABASE_URL` | Database connection string | SQLite fallback | All environments |

## Environment-Specific Configurations

### Local Development (PostgreSQL)

```bash
# .env file for local PostgreSQL development
BETTER_AUTH_SECRET=your_local_secret
BETTER_AUTH_URL=http://localhost:8080
DATABASE_URL=postgresql://username:password@localhost:5432/todo_db
```

**Characteristics:**
- Uses PostgreSQL database
- Full development feature set
- Hot reload enabled
- Detailed logging

### Local Development (SQLite Fallback)

```bash
# .env file for local SQLite development (no DATABASE_URL)
BETTER_AUTH_SECRET=your_local_secret
BETTER_AUTH_URL=http://localhost:8080
# DATABASE_URL is omitted to trigger SQLite fallback
```

**Characteristics:**
- Uses SQLite database
- No external database dependencies
- Good for initial setup/testing
- Portable database file

### Hugging Face Spaces (Production)

The application automatically detects the Hugging Face Spaces environment and:

- Falls back to SQLite if no `DATABASE_URL` is provided
- Disables SQL logging
- Uses port 7860 as required by Hugging Face
- Enables production-level error handling

**No special configuration needed** - the application handles this automatically.

### Testing Environment

For running tests:

```bash
# Use test database
DATABASE_URL=sqlite:///./test.db
BETTER_AUTH_SECRET=test_secret
BETTER_AUTH_URL=http://test.com
```

## Configuration Priority

The application follows this configuration priority:

1. **Environment Variables**: Highest priority
2. **.env file**: Fallback if environment variables not set
3. **Default Values**: Lowest priority, including SQLite fallback

## Database URL Format

### PostgreSQL
```
postgresql://username:password@host:port/database_name
```

### MySQL
```
mysql://username:password@host:port/database_name
```

### SQLite
```
sqlite:///path/to/database.db
```

## Health and Monitoring Endpoints

### Health Check
- `GET /health` - Basic health status
- `GET /ready` - Container readiness (for orchestration)
- `GET /status` - Detailed status including database info

### Response Examples

**Healthy Response:**
```json
{
  "status": "healthy"
}
```

**Detailed Status Response:**
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

1. **Application won't start**
   - Check if required environment variables are set
   - Verify database URL format if provided
   - Look for fallback to SQLite in logs

2. **Database connection errors**
   - Ensure database server is running
   - Verify credentials in DATABASE_URL
   - Check network connectivity

3. **Authentication issues**
   - Verify BETTER_AUTH_SECRET and URL
   - Check if auth service is accessible

### Debugging Tips

- Check application logs for database resolution messages
- Use `/status` endpoint to verify database configuration
- Test with different DATABASE_URL values to confirm fallback behavior