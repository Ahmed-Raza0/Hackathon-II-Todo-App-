# Data Model: Hugging Face Spaces Database Fallback

**Feature**: Hugging Face Spaces Database Fallback
**Date**: 2026-01-11
**Version**: 1.0

## Overview

This document defines the data structures and entities required for implementing the database fallback mechanism for Hugging Face Spaces deployment while maintaining PostgreSQL compatibility for local development.

## Core Entities

### DatabaseConfig
**Description**: Configuration entity that encapsulates database connection settings and fallback strategy

**Fields**:
- `primary_url` (string, optional): The primary database URL (e.g., PostgreSQL, MySQL)
- `fallback_url` (string): The fallback database URL (e.g., SQLite)
- `driver` (string): The database driver type (postgresql, mysql, sqlite)
- `host` (string, optional): Database host for primary connections
- `port` (integer, optional): Database port for primary connections
- `username` (string, optional): Database username for primary connections
- `password` (string, optional): Database password for primary connections
- `database_name` (string, optional): Database name for primary connections
- `is_fallback_active` (boolean): Flag indicating if fallback mode is active
- `validation_errors` (array[string]): List of validation errors if any occurred

**Validation Rules**:
- `fallback_url` must always be a valid SQLite connection string
- If `primary_url` is provided, it must have a valid database URL format
- `driver` must be one of: 'postgresql', 'mysql', 'sqlite'
- When `is_fallback_active` is true, all primary connection fields should be ignored

### DatabaseConnectionState
**Description**: Enumerates the possible states of database connection

**Values**:
- `DISCONNECTED`: No database connection attempted
- `CONNECTING_PRIMARY`: Attempting to connect to primary database
- `CONNECTING_FALLBACK`: Attempting to connect to fallback database
- `PRIMARY_CONNECTED`: Successfully connected to primary database
- `FALLBACK_CONNECTED`: Successfully connected to fallback database
- `CONNECTION_ERROR`: Both primary and fallback connections failed

### FallbackStrategy
**Description**: Defines the strategy for handling database connection failures

**Fields**:
- `enable_fallback` (boolean): Whether fallback mechanism is enabled
- `fallback_timeout` (integer): Timeout in seconds before attempting fallback
- `max_retries_primary` (integer): Number of retries for primary connection
- `retry_delay_ms` (integer): Delay in milliseconds between retry attempts
- `fallback_conditions` (array[string]): Conditions that trigger fallback

**Validation Rules**:
- `fallback_timeout` must be greater than 0
- `max_retries_primary` must be between 0 and 5
- `retry_delay_ms` must be between 100 and 5000

## Relationship Models

### DatabaseSessionContext
**Description**: Context object that holds the current database session state

**Fields**:
- `connection_state` (DatabaseConnectionState): Current state of the connection
- `engine` (object): The SQLAlchemy engine instance
- `session_factory` (object): The session factory for creating sessions
- `last_connection_attempt` (datetime): Timestamp of last connection attempt
- `connection_attempts_count` (integer): Number of connection attempts made
- `active_sessions` (integer): Number of currently active sessions

## State Transitions

### Database Connection Lifecycle

1. **Initialization** → `DISCONNECTED`
   - Application starts, no connection attempt made yet

2. `DISCONNECTED` → `CONNECTING_PRIMARY`
   - Database initialization requested with primary URL available

3. `DISCONNECTED` → `CONNECTING_FALLBACK`
   - Database initialization requested but no primary URL available

4. `CONNECTING_PRIMARY` → `PRIMARY_CONNECTED`
   - Primary database connection successful

5. `CONNECTING_PRIMARY` → `CONNECTING_FALLBACK`
   - Primary connection failed, fallback activated

6. `CONNECTING_FALLBACK` → `FALLBACK_CONNECTED`
   - Fallback database connection successful

7. `CONNECTING_FALLBACK` → `CONNECTION_ERROR`
   - Both primary and fallback connections failed

8. `PRIMARY_CONNECTED` → `CONNECTING_FALLBACK`
   - Primary connection lost, attempting fallback

## Configuration Schema

### DatabaseSettings
**Description**: Settings object that combines environment variables and fallback logic

**Structure**:
```
{
  "database_url": "string (from environment)",
  "fallback_database_url": "sqlite:///./production.db",
  "database_validation_enabled": "boolean (default: true)",
  "connection_timeout": "integer (default: 30)",
  "pool_size": "integer (default: 5)",
  "pool_max_overflow": "integer (default: 10)",
  "echo_sql": "boolean (default: false in production)",
  "sqlite_check_same_thread": "boolean (default: false)"
}
```

## Validation Rules

### URL Validation
- Primary URL must have a valid scheme (postgresql://, mysql://, etc.)
- Fallback URL must be a valid SQLite path (sqlite:///path/to/db)
- URLs must be properly encoded and not contain unsafe characters
- Empty or whitespace-only URLs are treated as invalid

### Environment Validation
- Environment variables are treated as optional in container environments
- Missing environment variables trigger fallback to default values
- Invalid environment variable values trigger fallback to safe defaults
- Validation errors are logged but do not cause application crashes

## Constraints

### Thread Safety
- SQLite connections must have `check_same_thread=False` in web applications
- Connection pools must be appropriately sized for container resources
- Session factories must be thread-safe for concurrent request handling

### File System Access
- SQLite database files must be in writable locations in container
- Database file paths must be relative to avoid permission issues
- Multiple processes must be able to access SQLite files safely

### Error Handling
- All database operations must have comprehensive error handling
- Failed operations must not crash the application
- Error states must be recoverable without restart
- Logging must be informative but not excessive

## Backwards Compatibility

### Existing API Contracts
- All existing database operations must continue to function
- Entity models must remain unchanged
- Query interfaces must remain consistent
- Transaction management must maintain current behavior

### Migration Path
- Existing PostgreSQL configurations continue to work
- New fallback logic does not interfere with primary paths
- Configuration keys remain the same for existing deployments
- Upgrade process requires no code changes to business logic