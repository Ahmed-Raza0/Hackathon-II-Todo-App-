---
id: 1-backend-specification
title: Backend Specification for Todo Full-Stack Web Application
stage: spec
date_iso: 2026-01-09
surface: agent
model: Claude Sonnet 4.5
feature: backend-specification
branch: 003-backend-specification
user: Claude Code User
command: /sp.specify
labels: ["backend", "specification", "api", "security"]
links:
  spec: "specs/003-backend-specification/spec.md"
  ticket: null
  adr: null
  pr: null
files_yaml:
  - "specs/003-backend-specification/spec.md"
  - "specs/003-backend-specification/checklists/requirements.md"
tests_yaml: []
prompt_text: |

  You are Claude, operating in **sp.specify mode**.

  Your task is to **SPECIFY (NOT IMPLEMENT)** the COMPLETE BACKEND
  for **Hackathon II – Phase 2: Todo Full-Stack Web Application**.

  This backend MUST be:

  * Production-ready
  * Secure
  * Fully integrated with the existing frontend
  * Fully compliant with provided specifications
  * Error-proof and hackathon-ready

  ────────────────────────────────────
  SECTION 1 — BACKEND SCOPE (STRICT)
  ────────────────────────────────────

  You are specifying ONLY:

  * Backend architecture
  * API contracts
  * Authentication verification flow
  * Database interaction rules
  * Request/response behavior
  * Error handling rules

  You MUST NOT:

  * Implement frontend logic
  * Redesign UI behavior
  * Add Phase III features (AI / chatbot)
  * Invent endpoints outside the provided spec
  * Add background jobs or async workers

  ────────────────────────────────────
  SECTION 2 — BACKEND TECHNOLOGY STACK (FIXED)
  ────────────────────────────────────

  * Python FastAPI
  * SQLModel (ORM)
  * Neon Serverless PostgreSQL
  * JWT verification compatible with Better Auth
  * Environment-based configuration

  ────────────────────────────────────
  SECTION 3 — ENVIRONMENT CONFIGURATION (REFERENCED)

  Backend MUST rely on environment variables:

  * BETTER_AUTH_SECRET
  * BETTER_AUTH_URL
  * DATABASE_URL (Neon PostgreSQL URI)

  Rules:

  * Secrets MUST NOT be hardcoded
  * Backend assumes env values are valid
  * Backend uses the SAME JWT secret as frontend

  ────────────────────────────────────
  SECTION 4 — AUTHENTICATION & SECURITY MODEL
  ────────────────────────────────────

  Authentication Rules:

  * Backend does NOT manage login or signup
  * Backend ONLY verifies JWT issued by Better Auth
  * JWT is received via:
    Authorization: Bearer <token>

  Verification Flow:

  1. Extract JWT from request header
  2. Verify signature using BETTER_AUTH_SECRET
  3. Decode payload to retrieve:

     * user_id
     * email (if present)
  4. Reject request if:

     * Token missing
     * Token invalid
     * Token expired

  ────────────────────────────────────
  SECTION 5 — API ENDPOINT SPECIFICATION
  ────────────────────────────────────

  Base Path:

  * /api

  Endpoints (Phase II ONLY):

  1. GET /api/{user_id}/tasks

     * Lists all tasks belonging to authenticated user
     * Supports optional filtering:

       * status (all | pending | completed)

  2. POST /api/{user_id}/tasks

     * Creates a new task
     * Title required
     * Task must be owned by authenticated user

  3. GET /api/{user_id}/tasks/{task_id}

     * Returns task details
     * Only if task belongs to authenticated user

  4. PUT /api/{user_id}/tasks/{task_id}

     * Updates task title and/or description
     * Ownership enforced

  5. DELETE /api/{user_id}/tasks/{task_id}

     * Deletes task permanently
     * Ownership enforced

  6. PATCH /api/{user_id}/tasks/{task_id}/complete

     * Toggles completed state
     * Idempotent behavior

  Rules:

  * All endpoints return JSON
  * All endpoints enforce user isolation
  * Unauthorized access returns 401
  * Forbidden access returns 403
  * Every API request MUST be authenticated
  * user_id from token MUST match requested user context
  * Backend NEVER trusts client-provided user_id blindly

  ────────────────────────────────────
  SECTION 6 — DATABASE INTERACTION RULES
  ────────────────────────────────────

  Database:

  * Neon Serverless PostgreSQL
  * SQLModel for ORM

  Data Rules:

  * Tasks are always filtered by user_id
  * Backend never returns tasks belonging to other users
  * Timestamps handled consistently
  * No soft deletes unless explicitly required

  ────────────────────────────────────
  SECTION 7 — ERROR HANDLING CONTRACT
  ────────────────────────────────────

  Error Response Rules:

  * Use standard HTTP status codes
  * Always return structured JSON errors
  * Never expose stack traces or secrets

  Common Errors:

  * 400 → Invalid input
  * 401 → Missing/invalid JWT
  * 403 → User mismatch
  * 404 → Task not found
  * 500 → Internal error (generic message)

  ────────────────────────────────────
  SECTION 8 — BACKEND–FRONTEND INTEGRATION
  ────────────────────────────────────

  Integration Rules:

  * Backend expects JWT from frontend automatically
  * Backend responses are frontend-friendly
  * Backend never redirects
  * Backend never renders HTML

  Frontend Assumptions:

  * Frontend attaches Authorization header
  * Frontend handles all UI state
  * Backend only returns data or errors

  ────────────────────────────────────
  SECTION 9 — PROJECT STRUCTURE (LOGICAL)
  ────────────────────────────────────

  Backend should be logically organized into:

  * App entry point
  * Config / env loader
  * Auth verification middleware
  * Task routes
  * Database session handling
  * Models and schemas

  (No code required — structure only)

  ────────────────────────────────────
  FINAL RULE
  ────────────────────────────────────

  This is a **SPECIFICATION ONLY** task.

  Do NOT write implementation code.
  Do NOT assume frontend logic.
  Do NOT exceed Phase II scope.

  The backend must be:

  * Secure
  * Deterministic
  * Frontend-compatible
  * Hackathon-ready

response_text: |
  Created complete backend specification for Todo Full-Stack Web Application.
  The specification includes:
  - User scenarios for secure task management, task status management, and task filtering
  - Functional requirements covering JWT authentication, user isolation, API endpoints, error handling
  - Key entities (Task, User, Authentication Token)
  - Success criteria with measurable outcomes
  - Edge cases for security and error handling
  The specification ensures user isolation, security, and compliance with the provided requirements.
  All implementation details were avoided, focusing on user value and business needs.
outcome: |
  Successfully created a comprehensive backend specification that meets all requirements.
  The specification is ready for the planning phase and includes all necessary functional
  requirements, user scenarios, and success criteria without implementation details.
evaluation: |
  The specification meets all quality criteria:
  - No implementation details leaked into the spec
  - All requirements are testable and unambiguous
  - Success criteria are measurable and technology-agnostic
  - User scenarios cover primary flows
  - Edge cases and security requirements properly addressed
---
