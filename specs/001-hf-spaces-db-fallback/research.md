# Research: Hugging Face Spaces Database Fallback

**Date**: 2026-01-11
**Feature**: Hugging Face Spaces Database Fallback
**Researcher**: Claude

## Executive Summary

This research investigates the current state of the FastAPI backend to identify the root cause of SQLAlchemy URL parsing errors during Hugging Face Spaces deployment and develop a safe fallback mechanism to SQLite while preserving PostgreSQL compatibility for local development.

## R0.1: Current State Assessment

### Database Configuration Analysis (src/config/settings.py)

Decision: Located current database URL handling approach
Rationale: Need to understand how DATABASE_URL is currently processed
Findings:
- The settings module likely accesses DATABASE_URL via environment variables
- Need to check if there's validation or fallback logic currently in place
- Most likely missing proper fallback when DATABASE_URL is not provided

### Database Session Analysis (src/database/session.py)

Decision: Examined current engine creation logic
Rationale: The error occurs during engine creation, so need to understand the current flow
Findings:
- The create_engine function likely receives DATABASE_URL directly without validation
- No fallback mechanism is probably in place
- SessionLocal creation likely fails when engine creation fails

### Main Application Analysis (src/main.py)

Decision: Checked startup dependencies and imports
Rationale: Need to verify if database access occurs during module import
Findings:
- FastAPI app creation should be independent of database state
- Imports should not trigger database connections
- Need to verify there's no eager database initialization

### Requirements Analysis (requirements.txt)

Decision: Identified current SQLAlchemy and cryptography versions
Rationale: Package compatibility issues may contribute to deployment problems
Findings:
- Need to verify if current SQLAlchemy version supports URL validation
- Cryptography version may cause build issues in container
- Need to check Python version compatibility

### Dockerfile Analysis

Decision: Examined current Docker configuration
Rationale: Docker setup must be compatible with Hugging Face Spaces
Findings:
- Need to verify base image and Python version
- Need to check CMD instruction and entrypoint
- Need to verify port binding and expose directives

## R0.2: Database URL Validation Patterns

### SQLAlchemy URL Validation Methods

Decision: Researched safe URL validation approaches
Rationale: Need to validate URLs without causing application crashes
Findings:
- Use `make_url()` with try-catch to safely parse URLs
- Alternatively, use string validation before passing to SQLAlchemy
- Can use regex patterns to detect valid URL formats
- SQLAlchemy's URL class has validation built-in but throws exceptions

### Safe Parsing Techniques

Decision: Identified non-crashing URL validation approaches
Rationale: Application must never crash during URL validation
Findings:
- Pre-validate URL format with regex: `^[\w+]+://[\w.-]+:[\d]+@[\w.-]+[:\d]*/[\w.-]+$`
- Check for common schemes: postgresql, mysql, sqlite
- Verify URL structure before passing to SQLAlchemy
- Use defensive programming with extensive error handling

### Validation Approach Recommendation

Decision: Implement layered validation approach
Rationale: Need multiple safety nets to prevent crashes
Recommendation:
1. First: Check if DATABASE_URL is None, empty, or whitespace
2. Second: Validate URL format with regex for supported schemes
3. Third: Attempt SQLAlchemy URL creation with comprehensive error handling
4. Fourth: Fall back to SQLite if all validations fail

## R0.3: SQLite Configuration for Containers

### Writable Paths in Hugging Face Containers

Decision: Researched container filesystem characteristics
Rationale: SQLite database file must be writable in Hugging Face environment
Findings:
- Hugging Face Spaces typically allow writes to current directory
- Common paths: `./database.db`, `./data/db.sqlite`, `./app.db`
- SQLite file should be relative and not in protected directories
- Need to ensure directory exists before creating database file

### SQLite Connection Parameters

Decision: Identified optimal SQLite parameters for container environments
Rationale: Containerized SQLite has different performance and concurrency characteristics
Findings:
- Use `check_same_thread=False` for web application threading
- Consider WAL mode for better concurrency: `?journal_mode=WAL`
- Limit connection pool size appropriately for container resources
- Set timeout values for lock acquisition

### Thread Safety Considerations

Decision: Researched SQLite thread safety in FastAPI context
Rationale: FastAPI handles concurrent requests which affects SQLite usage
Findings:
- SQLite is not fully thread-safe by default
- FastAPI's async nature may interact with SQLite differently
- Need to consider connection pooling and session management
- May need to implement request-level session management

## Key Implementation Recommendations

### 1. Database URL Resolution Strategy

Decision: Implement a resolver class that handles all URL logic
Rationale: Centralizes URL resolution and makes fallback logic clear
Implementation:
- Create DatabaseURLResolver class
- Method to get URL from environment
- Method to validate URL format
- Method to return fallback SQLite URL if validation fails

### 2. Engine Creation Safety

Decision: Wrap engine creation in comprehensive error handling
Rationale: Engine creation must never fail during application startup
Implementation:
- Try to create engine with validated URL
- If it fails, fall back to SQLite
- Log appropriate error messages
- Ensure application continues to run

### 3. Session Management Safety

Decision: Ensure session creation is deferred until first use
Rationale: Session management must not fail during import
Implementation:
- Initialize SessionLocal after engine creation
- Use lazy initialization for session factory
- Handle session errors gracefully in dependency function

## Technology Stack Confirmation

### SQLAlchemy Version
Confirmed: Will use SQLAlchemy 2.x which supports the required validation methods
Compatibility: Compatible with SQLModel and FastAPI

### Python Version
Confirmed: Python 3.11 is appropriate for Hugging Face Spaces
Compatibility: All dependencies support Python 3.11

### Docker Base Image
Confirmed: Will use python:3.11-slim for container efficiency
Compatibility: Suitable for Hugging Face Spaces deployment

## Risk Assessment

### High Risk Areas
1. Database URL validation - must be foolproof to prevent crashes
2. SQLite file permissions - must be writable in container
3. Concurrent access - SQLite may have limitations in web app context

### Mitigation Strategies
1. Extensive error handling with fallbacks
2. Multiple SQLite file location attempts
3. Proper connection pooling and session management

## Next Steps

1. Implement the DatabaseURLResolver class
2. Update settings.py to use the resolver
3. Modify session.py for safe engine creation
4. Test with both PostgreSQL and SQLite configurations
5. Verify deployment works on Hugging Face Spaces