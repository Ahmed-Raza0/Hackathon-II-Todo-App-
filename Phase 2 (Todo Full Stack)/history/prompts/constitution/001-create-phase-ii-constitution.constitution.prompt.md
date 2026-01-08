---
id: 001
title: Create Phase II Constitution
stage: constitution
date: 2026-01-08
surface: agent
model: claude-sonnet-4-5-20250929
feature: none
branch: main
user: user
command: /sp.constitution
labels: ["constitution", "phase-ii", "governance", "principles"]
links:
  spec: null
  ticket: null
  adr: null
  pr: null
files:
  - .specify/memory/constitution.md
tests:
  - N/A (documentation artifact)
---

## Prompt

You are Claude, operating under a **Spec Constitution** for
**Hackathon II – Phase 2: Todo Full-Stack Web Application**.

This document is the **highest authority**.
No assumption, code, feature, or behavior may violate this constitution.

────────────────────────────────────
SECTION 1 — PROJECT IDENTITY
────────────────────────────────────

Project Name: Hackathon Todo
Current Phase: Phase II (Web Application)
Previous Phase: Phase I (Console App) – COMPLETED
Future Phase: Phase III (Chatbot) – OUT OF SCOPE

The goal of Phase II ─────

- Every task belongs to EXACTLY one user
- User can ONLY:
  - Read their own tasks
  - Modify their own tasks
  - Delete their own tasks

There is NO concept of:
- Public tasks
- Shared tasks
- Admin override

Ownership is enforced at:
- API level
- Query level
- Authorization level

────────────────────────────────────
SECTION 8 — API CONSTITUTION
────────────────────────────────────

All APIs:
- Are RESTful
- Live under /api/*
- Require JWT
- Return JSON only

Allowed operations:
- List tasks
- Create task
- Get task
- Update task
- Delete task
- Toggle completion

Endpoints behavior MUST match:
@specs/api/rest-endpoints.md

────────lence is better than assumption.

## Response snapshot

Constitution successfully created at `.specify/memory/constitution.md` (v1.0.0)

**Core Principles Established:**
1. User Ownership (NON-NEGOTIABLE) - strict data isolation per user
2. REST API Contract - RESTful conventions, JWT auth, JSON-only responses
3. Authentication & Authorization - JWT-based with mandatory validation
4. Phase Boundaries (STRICT) - clear in/out scope for Phase II
5. Database Schema Integrity - user_id foreign keys, cascading deletes, indexes
6. Error Handling & Observability - structured logging and error responses
7. Simplicity & Pragmatism - YAGNI, boring tech, justified complexity

**Additional Sections:**
- Technology Stack (React/FastAPI/PostgreSQL recommended)
- Development Standards (testing, code quality, git workflow, docs)
- Governance (amendment process, compliance review, precedence hierarchy)

**Template Consistency:**
- Verified plan-template.md has generic "Constitution Check" section ✅
- Spec and tasks templates have no hard-coded constitution references ✅
- No README found to update (Phase II new project)

**Version Rationale:** 1.0.0 (MINOR) - Initial ratified constitution

## Outcome

- ✅ Impact: Established foundational governance for Phase II development
- 🧪 Tests: N/A (documentation artifact)
- 📁 Files: .specify/memory/constitution.md created
- 🔁 Next prompts: Create feature specs aligned with constitution principles; run /sp.specify for first feature
- 🧠 Reflection: Constitution provides clear boundaries for user ownership, API contracts, and phase scope. All future work must verify compliance with these principles.

## Evaluation notes (flywheel)

- Failure modes observed: None
- Graders run and results (PASS/FAIL): Manual review - PASS
- Prompt variant (if applicable): N/A
- Next experiment (smallest change to try): Test constitution enforcement by creating a spec that violates user ownership principle and verify it gets flagged
