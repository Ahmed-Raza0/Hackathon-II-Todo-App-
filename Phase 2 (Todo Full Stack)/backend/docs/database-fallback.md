# Database Fallback Configuration

## Overview

This application implements a robust database fallback mechanism that allows it to run in different environments:

- **Local Development**: Uses PostgreSQL (or other database) when `DATABASE_URL` is provided
- **Hugging Face Spaces**: Automatically falls back to SQLite when `DATABASE_URL` is missing or invalid

## How It Works

### 1. Database URL Resolution Process

The application follows this resolution flow:

1. **Check Environment**: Look for `DATABASE_URL` environment variable
2. **Validate URL**: Check if the URL is properly formatted and uses a supported scheme
3. **Connect or Fallback**:
   - If URL is valid → Connect to the specified database
   - If URL is missing/invalid → Fall back to SQLite database

### 2. Supported Database Types

- **PostgreSQL**: `postgresql://user:pass@host:port/dbname`
- **MySQL**: `mysql://user:pass@host:port/dbname`
- **SQLite**: `sqlite:///path/to/database.db`

### 3. Fallback Behavior

When no valid `DATABASE_URL` is provided, the application automatically creates and uses:

```
sqlite:///./production.db
```

This file is created in the current working directory and is suitable for container environments like Hugging Face Spaces.

## Configuration

### Environment Variables

| Variable | Required | Description |
|----------|----------|-------------|
| `DATABASE_URL` | Optional | Primary database connection string |
| `BETTER_AUTH_SECRET` | Required | Better Auth secret key |
| `BETTER_AUTH_URL` | Required | Better Auth URL |

### Local Development

For local development with PostgreSQL:

```bash
export DATABASE_URL=postgresql://username:password@localhost:5432/todo_db
uvicorn src.main:app --reload --port 8000
```

### Production/Hugging Face Spaces

No `DATABASE_URL` needed - the application will automatically use SQLite:

```bash
# Application will automatically use SQLite fallback
uvicorn src.main:app --host 0.0.0.0 --port 7860
```

## Error Handling

### Invalid DATABASE_URL

If `DATABASE_URL` is provided but is invalid (malformed, unsupported scheme, etc.), the application will:

1. Log a warning message
2. Fall back to SQLite automatically
3. Continue operation without crashing

### Missing Dependencies

The application has comprehensive error handling that ensures:

- Engine creation never crashes the application
- Session creation is protected with try/catch blocks
- All operations gracefully degrade when possible

## Health Checks

The application provides several endpoints to monitor database status:

- `GET /health` - Basic health check (no database access)
- `GET /ready` - Readiness check for container orchestration
- `GET /status` - Detailed status including database information

## Security Considerations

- SQLite database files are created with appropriate permissions
- Database connection strings are not exposed in error messages
- Authentication and authorization continue to work regardless of database type
- All SQL queries are properly parameterized to prevent injection

## Testing the Fallback

### With Valid DATABASE_URL

```bash
DATABASE_URL=postgresql://... uvicorn src.main:app --port 7860
```

### With Invalid DATABASE_URL

```bash
DATABASE_URL=invalid://url uvicorn src.main:app --port 7860
```

### With No DATABASE_URL

```bash
unset DATABASE_URL
uvicorn src.main:app --port 7860
```

In all cases, the application should start successfully.