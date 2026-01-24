---
id: 1
title: Update Hackathon Todo App Constitution
stage: constitution
date_iso: 2026-01-19
surface: agent
model: qwen-2.5-72b-instruct
feature: none
branch: main
user: Claude
command: sp.constitution
labels: ["constitution", "hackathon", "todo-app", "security", "architecture"]
links:
  spec: null
  ticket: null
  adr: null
  pr: null
files:
  - .specify/memory/constitution.md
  - history/prompts/constitution/001-update-hackathon-todo-app-constitution.constitution.prompt.md
tests: []
---

# Update Hackathon Todo App Constitution

## Summary

Updated the project constitution to reflect the specific requirements for the Hackathon II Todo App, incorporating security, authentication, database, API, and AI/MCP rules as specified by the user.

## Prompt Text

```
# Hackathon II Todo App - Spec Constitution
**Purpose:** This constitution defines the non-negotiable rules, architectural principles, and enforcement mechanisms for Phase II (Full-Stack Web Application) and Phase III (AI Chatbot) of the Hackathon II Todo App.

---

## 1. Purpose & Scope
- Ensure all features adhere to **Spec-Driven Development** methodology using Spec-Kit Plus and Claude Code.
- Maintain consistency between frontend (Next.js), backend (FastAPI), database (Neon PostgreSQL), authentication (Better Auth), and AI layers (OpenAI Agents + MCP).
- Enforce **security, statelessness, and user isolation** rules across all components.
- All implementation must reference specs in `/specs`.

**In Scope:**
- Task CRUD
- User Authentication (JWT)
- Frontend API integration
- AI-powered chat endpoint
- MCP Tools (add, list, complete, update, delete)
- Database persistence via Neon PostgreSQL

**Out of Scope:**
- Any database access outside backend
- Global state in server
- Skipping Spec-Kit references

---

## 2. Architectural Principles
1. **Monorepo Architecture:** Single CLAUDE.md context, frontend & backend in separate folders.
2. **Stateless Backend:** No server-side session state; all state persisted in database.
3. **Layered Responsibility:** Frontend only handles UI and API requests; backend handles all business logic and DB operations.
4. **Spec-Driven Enforcement:** All features must be implemented **only after reading the relevant spec**.
5. **Atomic Tasks:** Development broken into small, verifiable tasks with dependencies defined in `sp.tasks.md`.

---

## 3. Security Rules
1. **JWT Mandatory:** All API requests require JWT in `Authorization: Bearer <token>` header.
2. **Token Verification:** Backend must verify JWT using shared secret from `BETTER_AUTH_SECRET` environment variable.
3. **User Isolation:** All database queries must filter by `user_id` from verified JWT; user cannot see other users' tasks.
4. **Token Expiry:** JWTs expire automatically (default: 7 days).
5. **Unauthorized Access:** Requests without valid JWT must return `401 Unauthorized`.
6. **No Inline Secrets:** All secrets must be stored in `.env` files or environment variables; never hard-coded.

---

## 4. Authentication Rules
1. **Better Auth Issued JWT:** Frontend handles login/signup; JWT is sent to backend.
2. **Backend Verification Only:** Backend uses `python-jose` or equivalent to verify JWT; frontend tokens are not trusted for access control.
3. **User ID Enforcement:** The `user_id` in URL must always match the decoded JWT `user_id`.
4. **Protected Routes:** All endpoints under `/api/` are protected unless explicitly stated as public (e.g., login/signup).

---

## 5. Database Rules
1. **Database Engine:** Only use Neon Serverless PostgreSQL.
2. **ORM:** Only SQLModel for all DB operations.
3. **Schema Enforcement:**
   - `users` table managed by Better Auth.
   - `tasks` table: `id`, `user_id`, `title`, `description`, `completed`, `created_at`, `updated_at`.
   - `conversations` and `messages` for Phase III AI chatbot.
4. **Indexes:** Always index `tasks.user_id` and `tasks.completed` for filtering.
5. **No Direct Frontend Access:** Frontend cannot query database directly.

---

## 6. API Rules
1. **All routes under `/api/`**.
2. **RESTful Compliance:** Use GET, POST, PUT, DELETE, PATCH correctly.
3. **Request/Response Validation:** Use Pydantic models for input/output validation.
4. **Error Handling:** Return proper HTTPException codes (e.g., 404 for not found, 401 for unauthorized).
5. **Filtering by Authenticated User:** Backend must enforce user ownership on every endpoint.

---

## 7. AI & MCP Rules (Phase III)
1. **Stateless Requests:** Each chat request is independent; conversation persisted in DB.
2. **Agent Must Use MCP Tools:** All task operations go through MCP tools (add_task, list_tasks, complete_task, update_task, delete_task).
3. **No State Leakage:** Backend never stores session data in memory.
4. **Conversation History:** All messages stored in DB (`messages`, `conversations`) and fetched per request.
5. **Agent Behavior:** Confirm every user action, handle errors gracefully, enforce task ownership.

---

## 8. Spec Enforcement Rules
1. All implementations must reference the relevant specs using `@specs/` notation.
2. No code may be written outside the plan defined in `sp.plan.md`.
3. Tasks in `sp.tasks.md` must be completed in order; skipping is forbidden.
4. Any deviation from specs must be documented and approved in the spec files before implementation.

---

## 9. Forbidden Practices
1. Do not access database directly from frontend.
2. do not skip JWT verification.
3. Do not allow one user to see or modify another user's data.
4. Do not hard-code secrets.
5. Do not implement features before reading and referencing the relevant specs.
6. Do not use any database or ORM other than Neon PostgreSQL + SQLModel.
7. Do not store state in backend memory (stateless enforcement).

---

**Bottom Line:**
All developers and AI agents (Claude Code) must strictly adhere to this constitution. It enforces security, statelessness, user isolation, spec-driven methodology, and ensures consistent, production-grade implementation across the full stack.
```

## Response Text

Updated the constitution file at `.specify/memory/constitution.md` with specific principles and rules for the Hackathon II Todo App, including:
- Spec-Driven Enforcement principle
- Security & User Isolation principle
- Stateless Architecture principle
- Layered Responsibility principle
- Technology Stack Compliance principle
- Forbidden Practices principle
- Security Requirements section with authentication and database rules
- Development Workflow section with API and AI/MCP rules
- Governance section with amendment procedures

The constitution now properly reflects the requirements for the full-stack Todo App with Next.js frontend, FastAPI backend, Neon PostgreSQL database, Better Auth authentication, and AI chatbot functionality.

## Outcome

Successfully updated the project constitution to enforce security, statelessness, user isolation, spec-driven methodology, and ensure consistent implementation across the full-stack application.