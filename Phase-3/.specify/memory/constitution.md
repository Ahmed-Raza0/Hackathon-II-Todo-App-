<!--
Sync Impact Report:
- Version change: 1.0.0 → 1.1.0
- Added sections: Security Requirements, Development Workflow
- Modified principles: All 6 principles updated with specific content from user input
- Templates requiring updates: ⚠ pending review of .specify/templates/plan-template.md, .specify/templates/spec-template.md, .specify/templates/tasks-template.md
- Follow-up TODOs: None
-->
# Hackathon II Todo App Constitution

## Core Principles

### I. Spec-Driven Enforcement
All features must be implemented only after reading the relevant spec in `/specs`; No code may be written outside the plan defined in `sp.plan.md`; Tasks in `sp.tasks.md` must be completed in order; Deviations from specs must be documented and approved.

### II. Security & User Isolation
JWT Mandatory: All API requests require JWT in `Authorization: Bearer <token>` header; User Isolation: All database queries must filter by `user_id` from verified JWT; Unauthorized Access: Requests without valid JWT must return `401 Unauthorized`; No Inline Secrets: All secrets must be stored in `.env` files or environment variables.

### III. Stateless Architecture
No server-side session state; all state persisted in database; Each chat request is independent; conversation persisted in DB; Backend never stores session data in memory.

### IV. Layered Responsibility
Frontend only handles UI and API requests; backend handles all business logic and DB operations; No Direct Frontend Database Access: Frontend cannot query database directly.

### V. Technology Stack Compliance
Only use Neon Serverless PostgreSQL; Only SQLModel for all DB operations; All routes under `/api/`; Use RESTful compliance with proper HTTPException codes.

### VI. Forbidden Practices
Do not access database directly from frontend; Do not skip JWT verification; Do not allow one user to see or modify another user's data; Do not hard-code secrets; Do not implement features before reading and referencing the relevant specs; Do not use any database or ORM other than Neon PostgreSQL + SQLModel; Do not store state in backend memory (stateless enforcement).

## Security Requirements

Authentication Rules:
- Better Auth Issued JWT: Frontend handles login/signup; JWT is sent to backend.
- Backend Verification Only: Backend uses `python-jose` or equivalent to verify JWT; frontend tokens are not trusted for access control.
- User ID Enforcement: The `user_id` in URL must always match the decoded JWT `user_id`.
- Protected Routes: All endpoints under `/api/` are protected unless explicitly stated as public (e.g., login/signup).

Database Rules:
- Database Engine: Only use Neon Serverless PostgreSQL.
- ORM: Only SQLModel for all DB operations.
- Schema Enforcement: `users` table managed by Better Auth; `tasks` table: `id`, `user_id`, `title`, `description`, `completed`, `created_at`, `updated_at`; `conversations` and `messages` for Phase III AI chatbot.
- Indexes: Always index `tasks.user_id` and `tasks.completed` for filtering.
- No Direct Frontend Access: Frontend cannot query database directly.

## Development Workflow

API Rules:
- All routes under `/api/`.
- RESTful Compliance: Use GET, POST, PUT, DELETE, PATCH correctly.
- Request/Response Validation: Use Pydantic models for input/output validation.
- Error Handling: Return proper HTTPException codes (e.g., 404 for not found, 401 for unauthorized).
- Filtering by Authenticated User: Backend must enforce user ownership on every endpoint.

AI & MCP Rules (Phase III):
- Stateless Requests: Each chat request is independent; conversation persisted in DB.
- Agent Must Use MCP Tools: All task operations go through MCP tools (add_task, list_tasks, complete_task, update_task, delete_task).
- No State Leakage: Backend never stores session data in memory.
- Conversation History: All messages stored in DB (`messages`, `conversations`) and fetched per request.
- Agent Behavior: Confirm every user action, handle errors gracefully, enforce task ownership.

## Governance

Amendment Procedure: Changes to this constitution must be documented with clear rationale and reviewed by project maintainers. Any architectural decision that significantly impacts security, data integrity, or system architecture must be recorded in an ADR.

Versioning Policy: MAJOR for backward incompatible governance/principle removals; MINOR for new principles or material expansions; PATCH for clarifications and typo fixes.

Compliance Review: All pull requests must be validated against this constitution. Automated checks should verify that code changes comply with the stated principles, particularly around security, authentication, and data isolation requirements.

**Version**: 1.1.0 | **Ratified**: 2026-01-19 | **Last Amended**: 2026-01-19