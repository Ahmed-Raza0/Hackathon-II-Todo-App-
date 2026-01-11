---
id: phr-003
title: hf-spaces-db-fallback-spec
stage: spec
date: 2026-01-11
surface:
model: Claude Sonnet 4.5
feature: hf-spaces-db-fallback
branch: 001-hf-spaces-db-fallback
user:
command: /sp.specify
labels: [specification, database, huggingface, fallback, sqlmodel, sqlalchemy]
links:
  spec: specs/001-hf-spaces-db-fallback/spec.md
  ticket:
  adr:
  pr:
files:
  - path: specs/001-hf-spaces-db-fallback/spec.md
    action: created
    summary: Created specification for Hugging Face Spaces database fallback mechanism
  - path: specs/001-hf-spaces-db-fallback/checklists/requirements.md
    action: created
    summary: Created quality checklist for the specification
tests:
  - name:
    status:
    result:
---

## Prompt

You are operating in sp.specify mode.

Context:
This is a FastAPI backend deployed on Hugging Face Spaces using Docker.
Local development works, but deployment crashes at startup with a SQLAlchemy URL parsing error.
The repository structure is fixed and must not be reorganized.

Project structure (authoritative):
Root contains Dockerfile, requirements.txt, alembic, and src/.
Application entrypoint is src/main.py.
Database logic is located in src/database/session.py.
Environment configuration is in src/config/settings.py.

Observed failure:
Application crashes on startup in Hugging Face container logs with:
sqlalchemy.exc.ArgumentError: Could not parse SQLAlchemy URL from given URL string

Constraints:

Hugging Face does NOT load .env files

DATABASE_URL may be missing or empty at runtime

App must never crash during import or startup

SQLite fallback is acceptable for Hugging Face

PostgreSQL compatibility must be preserved for later production use

No changes to API routes, models, schemas, or services

No Ase URL Resolution

Introduce a single, deterministic database URL resolution flow

If DATABASE_URL is missing, empty, or invalid, fallback automatically to SQLite

SQLite database file must be relative and writable inside container

Validation must occur before create_engine is ever called

URL validation must be explicit, not implicit

SQLAlchemy Engine Safety

create_engine must never receive None, empty string, or malformed URL

SQLite-specific connect_args must only apply when SQLite is selected

echo logging must be disabled for production/container runtime

Engine creation must not raise exceptions under any condition

Session Lifecycle Integrity

SessionLocal must always be initialized successfully

get_session dependency must never raise on import

Session cleanup must be guaranteed

FastAPI Startup Stability

Importing src/main.py must not crash even if DATABASE_URL is missing

Uvicorn must be able to boot the app without environment variables

A basic health endpoint should be available for container readiness

Docker Runtime Alignment

Docker CMD must point to src.main:app

Server must bind to 0.0.0.0

Port must be compatible with Hugging Face (7860)

No reliance on docker-compose during Hugging Face runtime

Hugging Face Compatibility Rules

Do not rely on .env or docker-compose.yml

Do not assume persistent volumes

Do not assume Postgres exists

Container must be self-sufficient

Out of scope:

No frontend changes

No authentication changes

No JWT logic changes

No test changes

No Alembic execution

No performance optimizations

Definition of done:

Hugging Face build succeeds

Container starts without crashing

SQLAlchemy error is fully eliminated

App is reachable on Hugging Face Space

Local development remains unaffected

PostgreSQL can be enabled later via environment variable without code changes

Stop condition:
Once the backend boots successfully on Hugging Face with SQLite fallback and no startup errors, stop all work immediately.

## Response snapshot

# Feature Specification: Hugging Face Spaces Database Fallback

**Feature Branch**: `001-hf-spaces-db-fallback`
**Created**: 2026-01-11
**Status**: Draft
**Input**: User description: "You are operating in sp.specify mode.

Context:
This is a FastAPI backend deployed on Hugging Face Spaces using Docker.
Local development works, but deployment crashes at startup with a SQLAlchemy URL parsing error.
The repository structure is fixed and must not be reorganized.

Project structure (authoritative):
Root contains Dockerfile, requirements.txt, alembic, and src/.
Application entrypoint is src/main.py.
Database logic is located in src/database/session.py.
Environment configuration is in src/config/settings.py.

Observed failure:
Application crashes on startup in Hugging Face container logs with:
sqlalchemy.exc.ArgumentError: Could not parse SQLAlchemy URL from given URL string

Constraints:

Hugging Face does NOT load .env files

DATABASE_URL may be missing or empty at runtime

App must never crash during import or startup

SQLite fallback is acceptable for Hugging Face

PostgreSQL compatibility must be preserved for later production use

No changes to API routes, models, schemas, or services

No Ase URL Resolution

Introduce a single, deterministic database URL resolution flow

If DATABASE_URL is missing, empty, or invalid, fallback automatically to SQLite

SQLite database file must be relative and writable inside container

Validation must occur before create_engine is ever called

URL validation must be explicit, not implicit

SQLAlchemy Engine Safety

create_engine must never receive None, empty string, or malformed URL

SQLite-specific connect_args must only apply when SQLite is selected

echo logging must be disabled for production/container runtime

Engine creation must not raise exceptions under any condition

Session Lifecycle Integrity

SessionLocal must always be initialized successfully

get_session dependency must never raise on import

Session cleanup must be guaranteed

FastAPI Startup Stability

Importing src/main.py must not crash even if DATABASE_URL is missing

Uvicorn must be able to boot the app without environment variables

A basic health endpoint should be available for container readiness

Docker Runtime Alignment

Docker CMD must point to src.main:app

Server must bind to 0.0.0.0

Port must be compatible with Hugging Face (7860)

No reliance on docker-compose during Hugging Face runtime

Hugging Face Compatibility Rules

Do not rely on .env or docker-compose.yml

Do not assume persistent volumes

Do not assume Postgres exists

Container must be self-sufficient

Out of scope:

No frontend changes

No authentication changes

No JWT logic changes

No test changes

No Alembic execution

No performance optimizations

Definition of done:

Hugging Face build succeeds

Container starts without crashing

SQLAlchemy error is fully eliminated

App is reachable on Hugging Face Space

Local development remains unaffected

PostgreSQL can be enabled later via environment variable without code changes

Stop condition:
Once the backend boots successfully on Hugging Face with SQLite fallback and no startup errors, stop all work immediately."

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Deploy FastAPI Backend on Hugging Face Spaces (Priority: P1)

As a developer, I want to deploy my FastAPI backend to Hugging Face Spaces so that my application can be accessed by users without startup errors or crashes.

**Why this priority**: This is the core requirement that is currently blocking deployment - the application crashes on startup due to database configuration issues.

**Independent Test**: The backend can be successfully deployed to Hugging Face Spaces and responds to requests without runtime errors, demonstrating that the database connection is established properly.

**Acceptance Scenarios**:

1. **Given** a Hugging Face Space environment with no DATABASE_URL environment variable, **When** the application starts, **Then** it successfully connects to a SQLite database and serves requests without errors
2. **Given** a Hugging Face Space environment with an invalid DATABASE_URL, **When** the application starts, **Then** it falls back to SQLite and continues to operate normally

---

### User Story 2 - Maintain Local Development PostgreSQL Compatibility (Priority: P2)

As a developer, I want to maintain PostgreSQL compatibility for local development so that I can continue working with my preferred database while the production deployment uses SQLite.

**Why this priority**: Preserves existing development workflow while enabling production deployment.

**Independent Test**: The application can connect to PostgreSQL when DATABASE_URL is properly configured in a local environment.

**Acceptance Scenarios**:

1. **Given** a local development environment with a valid PostgreSQL DATABASE_URL, **When** the application starts, **Then** it connects to PostgreSQL and operates normally
2. **Given** a local development environment with no DATABASE_URL, **When** the application starts, **Then** it falls back to SQLite and operates normally

---

### User Story 3 - Ensure Application Stability and Health Checks (Priority: P3)

As a system administrator, I want the application to be stable and provide health endpoints so that Hugging Face Spaces can properly monitor and manage the container.

**Why this priority**: Critical for production reliability and proper container orchestration.

**Independent Test**: The application starts reliably and provides health endpoints that return appropriate status codes.

**Acceptance Scenarios**:

1. **Given** any environment configuration, **When** the application imports and initializes, **Then** it does not crash and can serve health check requests
2. **Given** a container runtime environment, **When** health check endpoints are accessed, **Then** they return appropriate status codes indicating application health

---

### Edge Cases

- What happens when the SQLite database file is not writable in the container?
- How does the system handle malformed DATABASE_URL values?
- What occurs when the database engine creation encounters unexpected errors?
- How does the system behave when the database file path is invalid or inaccessible?

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: System MUST establish a database connection without crashing during application startup
- **FR-002**: System MUST use SQLite as a fallback when DATABASE_URL is missing, empty, or invalid
- **FR-003**: System MUST preserve PostgreSQL connectivity when DATABASE_URL is properly configured
- **FR-004**: System MUST validate database URLs before attempting to create database engines
- **FR-005**: System MUST handle database connection errors gracefully without application crashes
- **FR-006**: System MUST provide health check endpoints that return appropriate status codes
- **FR-007**: System MUST bind to 0.0.0.0:7860 for Hugging Face Spaces compatibility
- **FR-008**: System MUST initialize database session management without raising exceptions on import
- **FR-009**: System MUST apply SQLite-specific connection arguments only when SQLite is selected
- **FR-010**: System MUST disable logging output in production/container runtime

### Key Entities *(include if feature involves data)*

- **Database Connection**: Represents the connection to either PostgreSQL or SQLite, with appropriate configuration based on environment
- **Database Engine**: The SQLAlchemy engine instance that manages database connections and sessions
- **Database Session**: The session factory that provides database sessions for API operations

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: Application starts successfully in Hugging Face Spaces without crashing during import or startup
- **SC-002**: Container builds successfully on Hugging Face Spaces with no build-time errors
- **SC-003**: Database operations function correctly with SQLite in Hugging Face Spaces environment
- **SC-004**: Local development remains unaffected and can still use PostgreSQL when configured
- **SC-005**: PostgreSQL can be enabled via environment variable without requiring code changes
- **SC-006**: Health check endpoints return 200 status codes indicating application readiness
- **SC-007**: Application handles missing or invalid DATABASE_URL without runtime errors

## Outcome

- ✅ Impact: Created comprehensive specification for Hugging Face Spaces database fallback mechanism
- 🧪 Tests: Specification includes testable requirements and acceptance criteria
- 📁 Files: Created spec.md and requirements checklist
- 🔁 Next prompts: Ready for planning phase with `/sp.plan`

## Evaluation notes (flywheel)

- Specification addresses all constraints from user requirements
- Three user stories prioritize deployment stability as highest priority
- Edge cases and error handling properly considered
- Maintains backward compatibility for local development