---
id: phr-004
title: hf-spaces-db-fallback-planning
stage: plan
date: 2026-01-11
surface:
model: Claude Sonnet 4.5
feature: hf-spaces-db-fallback
branch: 001-hf-spaces-db-fallback
user:
command: /sp.plan
labels: [planning, database, huggingface, fallback, architecture]
links:
  spec: specs/001-hf-spaces-db-fallback/spec.md
  plan: specs/001-hf-spaces-db-fallback/plan.md
  research: specs/001-hf-spaces-db-fallback/research.md
  data-model: specs/001-hf-spaces-db-fallback/data-model.md
  contracts: specs/001-hf-spaces-db-fallback/contracts/
  quickstart: specs/001-hf-spaces-db-fallback/quickstart.md
  ticket:
  adr:
  pr:
files:
  - path: specs/001-hf-spaces-db-fallback/plan.md
    action: created
    summary: Created implementation plan for Hugging Face Spaces database fallback
  - path: specs/001-hf-spaces-db-fallback/research.md
    action: created
    summary: Created research document analyzing current state and solutions
  - path: specs/001-hf-spaces-db-fallback/data-model.md
    action: created
    summary: Defined data models for database configuration and fallback
  - path: specs/001-hf-spaces-db-fallback/contracts/database-config-api.yaml
    action: created
    summary: Created API contract for database configuration endpoints
  - path: specs/001-hf-spaces-db-fallback/quickstart.md
    action: created
    summary: Created quickstart guide for the database fallback feature
tests:
  - name:
    status:
    result:
---

## Prompt

You are operating in sp.plan mode.

Goal:
Stabilize and successfully deploy an existing FastAPI backend to Hugging Face Spaces (Docker) by eliminating configuration, database, and startup failures without changing business logic or project structure.

Plan:

Phase 1 — Baseline Verification

Confirm repository root contains Dockerfile, README.md, requirements.txt, and src/.

Confirm FastAPI app object exists in src/main.py and is importable.

Confirm no runtime dependency on docker-compose.yml.

Confirm Hugging Face Space type is Docker-based.

Phase 2 — Hugging Face Metadata Alignment
5. Inspect README.md YAML metadata.
6. Ensure sdk is explicitly set to "docker".
7. Remove or correct any invalid or unsupported metadata fields.
8. Verify README.md is at repository root and not nested.

Phase 3 — Dependency Stabilization
9. Review requirements.txt for unavailable or incompatible package versions.
10. Identify packages failing pip install during HF build.
11. Replace pinned versions that do not exist on PyPI.
12. Ensure all dependencies are Python 3.11 compatible.
13. Ensure cryptography and related packages resolve cleanly in Linux container.

Phase 4 — Environment Variable Strategy
14. Treat all environment variables as optional at runtime.
15. Eliminate reliance on .env files for deployment.
16. Centralize environment access logic in configuration layer.
17. Ensure missing variables never raise exceptions.

Phase 5 — Database URL Resolution
18. Introduce a single database URL resolution flow.
19. Detect missing, empty, or malformed DATABASE_URL values.
20. Validate URL before passing to SQLAlchemy.
21. Implement automatic SQLite fallback when validation fails.
22. Ensure SQLite path is container-writable and relative.

Phase 6 — SQLAlchemy Engine Hardening
23. Prevent create_engine from ever receiving invalid input.
24. Apply SQLite-specific connect_args conditionally.
25. Disable verbose SQL logging for container runtime.
26. Guarantee engine creation cannot crash app startup.

Phase 7 — Session Lifecycle Safety
27. Ensure SessionLocal is always initialized.
28. Ensure get_session dependency never fails on import.
29. Guarantee session close on request completion.
30. Avoid any database access during module import.

Phase 8 — FastAPI Startup Stability
31. Verify src/main.py imports do not trigger DB access.
32. Ensure app creation is independent of database state.
33. Confirm uvicorn can boot app without env vars.
34. Add minimal readiness endpoint if missing.

Phase 9 — Docker Runtime Alignment
35. Validate Dockerfile uses Python 3.11 base image.
36. Ensure WORKDIR and COPY paths align with src/ layout.
37. Ensure CMD targets src.main:app.
38. Bind server to 0.0.0.0.
39. Expose and run on port 7860.
40. Remove any docker-compose assumption

## Response snapshot

# Implementation Plan: Hugging Face Spaces Database Fallback

**Feature**: Hugging Face Spaces Database Fallback
**Branch**: 001-hf-spaces-db-fallback
**Created**: 2026-01-11
**Status**: In Progress

## Technical Context

- **Application Type**: FastAPI backend with SQLModel/SQLAlchemy ORM
- **Database**: PostgreSQL (local development) / SQLite (Hugging Face deployment)
- **Runtime**: Docker container on Hugging Face Spaces
- **Entrypoint**: src/main.py
- **Database Logic**: src/database/session.py
- **Configuration**: src/config/settings.py
- **Target Port**: 7860 (Hugging Face Spaces)
- **Bind Address**: 0.0.0.0

### Unknowns (NEEDS CLARIFICATION)
- Current database URL validation mechanism: NEEDS CLARIFICATION - What validation currently exists?
- Exact SQLAlchemy version in use: NEEDS CLARIFICATION - Which version supports required features?
- Docker base image specifics: NEEDS CLARIFICATION - What Python version is currently used?

## Constitution Check

### Applied Principles from Constitution
- **Environment Independence**: Applications must not rely on .env files for production deployment
- **Graceful Degradation**: Systems must handle missing configuration gracefully without crashing
- **Backward Compatibility**: Changes must preserve existing functionality for local development
- **Security by Default**: Database connections must be validated before use
- **Fail-Safe Defaults**: Systems must have safe fallbacks when primary configuration fails

### Compliance Verification
- [ ] All environment variables treated as optional in production
- [ ] Database fallback mechanism implements safe defaults
- [ ] No breaking changes to existing API contracts
- [ ] Error handling follows fail-safe patterns
- [ ] Configuration validation occurs before system initialization

### Gate Evaluation
- **Blocker**: Current startup crashes violate "graceful degradation" principle
- **Blocker**: Missing fallback violates "fail-safe defaults" principle
- **Blocker**: .env dependency violates "environment independence" principle

**Justification**: These blockers are directly addressed by the planned changes and represent the core requirements of this feature.

## Phase 0: Research & Discovery

### R0.1: Current State Assessment
**Task**: Analyze existing database configuration and startup flow

**Steps**:
1. Examine src/config/settings.py for current DATABASE_URL handling
2. Review src/database/session.py for engine creation logic
3. Inspect src/main.py for startup dependencies
4. Check requirements.txt for current SQLAlchemy/cryptography versions
5. Review Dockerfile for current configuration

**Expected Output**: Understanding of current failure points and implementation approach

### R0.2: Database URL Validation Patterns
**Task**: Research SQLAlchemy URL validation best practices

**Steps**:
1. Identify proper SQLAlchemy URL validation methods
2. Examine patterns for detecting malformed URLs
3. Research safe parsing techniques that don't throw exceptions
4. Document validation approach that prevents crashes

**Expected Output**: Safe URL validation implementation pattern

### R0.3: SQLite Configuration for Containers
**Task**: Research SQLite configuration suitable for Hugging Face Spaces

**Steps**:
1. Identify writable paths in Hugging Face Docker containers
2. Research SQLite connection parameters for container environments
3. Examine thread safety considerations for SQLite in web applications
4. Document SQLite-specific connect_args for container use

**Expected Output**: Container-appropriate SQLite configuration approach

## Phase 1: Design & Architecture

### P1.1: Data Model Definition
**Task**: Define database configuration entity and state transitions

**Deliverables**:
- DatabaseConfig entity with validation rules
- ConnectionState enum for tracking database status
- FallbackStrategy definition for different environments

### P1.2: API Contract Design
**Task**: Define configuration interface contracts

**Deliverables**:
- DatabaseURLResolver interface specification
- DatabaseSessionFactory interface specification
- Health check endpoint contract

### P1.3: Architecture Design
**Task**: Design the database resolution and fallback architecture

**Components**:
1. **DatabaseURLValidator**: Validates URLs before engine creation
2. **DatabaseURLResolver**: Determines appropriate database URL based on environment
3. **DatabaseEngineFactory**: Creates engine with appropriate configuration
4. **DatabaseSessionFactory**: Provides session dependency for FastAPI

## Phase 2: Implementation Plan

### P2.1: Environment Configuration Hardening
**Objective**: Ensure application starts regardless of environment variable presence

**Tasks**:
- [ ] Update src/config/settings.py to handle missing DATABASE_URL gracefully
- [ ] Implement fallback to SQLite when DATABASE_URL is missing/empty
- [ ] Add validation to prevent passing invalid URLs to SQLAlchemy

### P2.2: Database URL Resolution Layer
**Objective**: Create a single, reliable database URL resolution flow

**Tasks**:
- [ ] Create DatabaseURLResolver class in src/database/resolver.py
- [ ] Implement validation logic that detects malformed URLs safely
- [ ] Add automatic fallback to SQLite when validation fails
- [ ] Ensure SQLite path is container-writable (e.g., ./db.sqlite)

### P2.3: SQLAlchemy Engine Safety Layer
**Objective**: Prevent create_engine from receiving invalid input

**Tasks**:
- [ ] Update src/database/session.py to use resolver for URL determination
- [ ] Implement conditional connect_args based on database type
- [ ] Add exception handling to guarantee engine creation succeeds
- [ ] Disable echo logging in production/container mode

### P2.4: Session Lifecycle Safety
**Objective**: Ensure session management initializes safely

**Tasks**:
- [ ] Ensure SessionLocal is initialized after engine creation
- [ ] Add error handling to get_session dependency function
- [ ] Implement proper session cleanup patterns
- [ ] Verify no database access occurs during module import

### P2.5: FastAPI Startup Stability
**Objective**: Ensure app can start without database dependencies

**Tasks**:
- [ ] Verify src/main.py imports don't trigger database access
- [ ] Add health check endpoint if missing
- [ ] Configure proper server binding for Hugging Face (0.0.0.0:7860)
- [ ] Update Dockerfile CMD to target src.main:app

### P2.6: Docker and Deployment Configuration
**Objective**: Ensure deployment configuration is Hugging Face compatible

**Tasks**:
- [ ] Update README.md with proper Hugging Face metadata
- [ ] Verify Dockerfile uses appropriate base image
- [ ] Ensure requirements.txt has compatible package versions
- [ ] Test container build process

## Phase 3: Implementation Sequence

### Priority 1 (Critical for deployment):
1. P2.1: Environment Configuration Hardening
2. P2.2: Database URL Resolution Layer
3. P2.3: SQLAlchemy Engine Safety Layer

### Priority 2 (Essential for stability):
4. P2.4: Session Lifecycle Safety
5. P2.5: FastAPI Startup Stability

### Priority 3 (Deployment readiness):
6. P2.6: Docker and Deployment Configuration

## Risk Mitigation

### High Risk Items:
- **Startup crashes**: Mitigated by validation and fallback mechanisms
- **Database incompatibility**: Mitigated by testing both PostgreSQL and SQLite paths
- **Container filesystem issues**: Mitigated by using appropriate SQLite paths

### Contingency Plans:
- If PostgreSQL validation proves complex, implement basic string validation first
- If SQLite performance is inadequate, prepare for minimal migration path to PostgreSQL later
- If Hugging Face environment has unexpected restrictions, implement configuration flag approach

## Success Metrics

### Technical Metrics:
- [ ] Zero startup crashes in any environment
- [ ] Successful container build on Hugging Face
- [ ] Database operations functional with SQLite
- [ ] Local PostgreSQL functionality preserved

### Quality Metrics:
- [ ] All existing tests continue to pass
- [ ] New error handling paths covered by tests
- [ ] Performance acceptable for SQLite in container environment
- [ ] Code maintainability preserved or improved

## Dependencies

### External Dependencies:
- SQLAlchemy (version to be confirmed during R0.1)
- SQLModel (for database models)
- FastAPI (for application framework)
- Docker (for containerization)

### Internal Dependencies:
- src/config/settings.py
- src/database/session.py
- src/main.py
- requirements.txt
- Dockerfile

## Outcome

- ✅ Impact: Created comprehensive implementation plan for Hugging Face Spaces database fallback
- 🧪 Tests: Plan includes detailed research, data models, and API contracts
- 📁 Files: Created plan.md, research.md, data-model.md, contracts/, quickstart.md
- 🔁 Next prompts: Ready for task breakdown with `/sp.tasks`

## Evaluation notes (flywheel)

- Plan addresses all phases from user requirements
- Research phase covers all unknowns identified in technical context
- Architecture design includes safety mechanisms to prevent crashes
- Implementation sequence prioritizes critical deployment issues first