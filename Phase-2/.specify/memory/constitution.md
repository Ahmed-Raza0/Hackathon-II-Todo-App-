<!--
Sync Impact Report:
- Version Change: (initial) → 1.0.0
- Modified Principles: N/A (initial creation)
- Added Sections:
  * Core Principles (7 principles)
  * Technology Stack
  * Development Standards
  * Governance
- Removed Sections: N/A
- Templates Requiring Updates:
  ✅ Updated: None (initial creation, templates reference constitution generically)
- Follow-up TODOs: None
- Rationale: MINOR version (1.0.0) as this is the initial ratified constitution for Phase II
-->

# Hackathon Todo – Phase II Constitution

## Core Principles

### I. User Ownership (NON-NEGOTIABLE)

- Every task belongs to EXACTLY one user
- Users can ONLY:
  - Read their own tasks
  - Modify their own tasks
  - Delete their own tasks
- There is NO concept of:
  - Public tasks
  - Shared tasks
  - Admin override (except infrastructure-level operations)
- Ownership MUST be enforced at:
  - API level (JWT validation + user_id filtering)
  - Query level (database WHERE clauses)
  - Authorization level (middleware checks)

**Rationale**: User data isolation is the foundation of trust. No feature may compromise this boundary. This prevents data leaks, ensures GDPR compliance, and simplifies reasoning about security.

### II. REST API Contract

All APIs MUST:
- Follow RESTful conventions
- Live under `/api/*` namespace
- Require valid JWT authentication
- Return JSON only (no HTML, XML, or mixed responses)
- Use standard HTTP methods semantically (GET=read, POST=create, PUT/PATCH=update, DELETE=remove)
- Return appropriate HTTP status codes (2xx success, 4xx client error, 5xx server error)

Allowed operations ONLY:
- List tasks (GET `/api/tasks`)
- Create task (POST `/api/tasks`)
- Get task (GET `/api/tasks/:id`)
- Update task (PUT/PATCH `/api/tasks/:id`)
- Delete task (DELETE `/api/tasks/:id`)
- Toggle completion (PATCH `/api/tasks/:id/toggle`)

Endpoints behavior MUST match: `@specs/api/rest-endpoints.md`

**Rationale**: Strict REST adherence ensures predictable client integration, simplifies testing, and prevents scope creep. JSON-only responses enable clean frontend state management.

### III. Authentication & Authorization

- JWT-based authentication is MANDATORY for all `/api/*` endpoints
- Tokens MUST include `user_id` claim
- Backend MUST validate:
  - Token signature
  - Token expiration
  - User existence
- Frontend MUST:
  - Store tokens securely (httpOnly cookies preferred, or secure storage with XSS mitigation)
  - Attach tokens to all API requests
  - Handle 401/403 responses (redirect to login)
- NO bypasses, NO temporary hardcoded credentials in production code

**Rationale**: Security-first approach prevents unauthorized access. JWT enables stateless backend scalability while maintaining strong identity verification.

### IV. Phase Boundaries (STRICT)

**In Scope (Phase II)**:
- Web-based UI for task management
- User authentication and registration
- RESTful API backend
- Database persistence
- User-scoped task CRUD operations

**Out of Scope (Phase II)**:
- Chatbot interface (Phase III)
- Task sharing or collaboration
- Mobile native apps
- Real-time sync (WebSockets)
- Admin dashboard
- Analytics or reporting

**Rationale**: Clear scope prevents feature creep. Phases must complete fully before expanding. No assumptions about future phases may leak into current implementation.

### V. Database Schema Integrity

- Schema MUST enforce user ownership via foreign keys
- Tasks table MUST have `user_id` NOT NULL column
- Cascading deletes MUST be defined (delete user → delete user's tasks)
- Indexes MUST exist on:
  - `tasks.user_id` (query performance)
  - `tasks.created_at` (sorting)
- Migrations MUST be versioned and reversible

**Rationale**: Database-level enforcement is the last line of defense. Indexes ensure performance at scale. Reversible migrations enable safe deployments.

### VI. Error Handling & Observability

- All errors MUST be logged with context (user_id, endpoint, timestamp, stack trace)
- API errors MUST return structured JSON:
  ```json
  {
    "error": "Human-readable message",
    "code": "MACHINE_READABLE_CODE",
    "details": {}  // optional, for validation errors
  }
  ```
- Frontend MUST display user-friendly error messages (never raw stack traces)
- Critical errors (auth failures, DB connection loss) MUST trigger alerts

**Rationale**: Structured errors enable debugging without compromising security. User-facing messages prevent confusion. Alerts ensure rapid incident response.

### VII. Simplicity & Pragmatism

- Prefer boring technology (proven frameworks over experimental ones)
- Start with the simplest solution that works
- YAGNI (You Aren't Gonna Need It) applies to all features
- Complexity MUST be justified in writing (ADR or plan.md)
- Refactoring requires tests first

**Rationale**: Premature optimization and over-engineering kill velocity. Simple solutions are easier to debug, test, and hand off. Complexity budget is finite.

## Technology Stack

### Frontend
- Framework: React (or equivalent modern SPA framework)
- State Management: React Context or lightweight state library
- HTTP Client: Fetch API or Axios
- Styling: CSS Modules, Tailwind, or styled-components (consistency required)

### Backend
- Language: Python (FastAPI) or Node.js (Express)
- Database: PostgreSQL (Neon Serverless or equivalent)
- ORM: SQLModel (Python) or Prisma (Node.js)
- Authentication: JWT with secure secret management

### Infrastructure
- Environment Variables: `.env` files for local, secrets manager for production
- Deployment: Containerized (Docker) or serverless (Vercel, Railway, Render)
- Version Control: Git with meaningful commit messages

## Development Standards

### Testing Requirements
- Unit tests for business logic (task validation, auth helpers)
- Integration tests for API endpoints (happy path + error cases)
- Frontend component tests (user interactions)
- Test coverage target: >70% for critical paths

### Code Quality
- Linting enforced (ESLint for JS, Ruff/Black for Python)
- Type safety encouraged (TypeScript preferred for frontend, type hints for Python)
- No commented-out code in main branch
- Meaningful variable names (no single-letter vars except loop counters)

### Git Workflow
- Feature branches from `main`
- Descriptive commit messages (conventional commits preferred)
- Pull requests require:
  - Tests passing
  - No linting errors
  - Clear description of changes
- Squash-merge to keep history clean

### Documentation
- README MUST include:
  - Setup instructions
  - Environment variables required
  - How to run tests
  - API endpoint list (or link to spec)
- Inline comments for non-obvious logic only
- Docstrings for public functions/classes

## Governance

This constitution is the **highest authority** for Phase II development. All code, features, and decisions MUST comply.

### Amendment Process
1. Propose amendment with rationale (via issue or discussion)
2. Document impact on existing code/specs
3. Increment version:
   - MAJOR: Breaking principle changes
   - MINOR: New principles or sections
   - PATCH: Clarifications or typo fixes
4. Update dependent templates and specs
5. Commit with message: `docs: amend constitution to vX.Y.Z (description)`

### Compliance Review
- All PRs MUST verify no constitutional violations
- Spec/plan/tasks artifacts MUST align with principles
- When principles conflict with implementation reality, amend constitution (don't bypass)

### Precedence
- Constitution > Specs > Plans > Tasks > Code comments
- When in doubt, escalate to constitution first
- Silence is NOT consent—ask clarifying questions

**Version**: 1.0.0 | **Ratified**: 2026-01-08 | **Last Amended**: 2026-01-08
