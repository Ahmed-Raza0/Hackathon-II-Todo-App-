---
id: 1
title: Create Auth Core Fix Spec
stage: spec
date_iso: 2026-01-20
surface: agent
model: qwen-2.5-72b-instruct
feature: 001-auth-core-fix
branch: 001-auth-core-fix
user: Claude
command: sp.specify
labels: ["spec", "auth", "authentication", "frontend", "backend", "better-auth"]
links:
  spec: /mnt/d/Hackathon II (Todo App)/Phase-3/specs/001-auth-core-fix/spec.md
  plan: null
  ticket: null
  adr: null
  pr: null
files:
  - specs/001-auth-core-fix/spec.md
  - specs/001-auth-core-fix/checklists/requirements.md
  - history/prompts/001-auth-core-fix/001-create-auth-core-fix-spec.spec.prompt.md
tests: []
---

# Create Auth Core Fix Spec

## Summary

Created comprehensive specification for fixing core authentication functionality. This addresses the broken signup and login flows that were redirecting to `/api/auth/error` or failing silently. The spec outlines user stories, functional requirements, and success criteria to ensure proper authentication flow implementation.

## Prompt Text

```
# /sp.specify auth-core-fix

You are working on a full-stack Todo application using:
- Next.js 16+ (App Router)
- Better Auth (frontend authentication)
- FastAPI (backend)
- SQLModel + Neon PostgreSQL
- JWT + Cookies for authentication

## Problem

Signup and login are completely non-functional.

Observed behavior:
- Users cannot successfully sign up or log in
- Application redirects to `/api/auth/error` OR fails silently
- No session is persisted
- No redirect to `/dashboard`
- Authentication blocks all further development

This is a **core authentication failure**, not a UI or styling issue.

---

## Scope (Strict)

### In Scope
- Signup flow
- Login flow
- Session creation
- Cookie/JWT issuance
- Redirect after authentication

### Out of Scope
- Task CRUD
- Chatbot / MCP
- UI styling
- Authorization rules
- Performance optimizations

---

## Root Cause Assumptions (Must Be Verified)

At least one of the following is broken:

1. Better Auth App Router handler is missing or incorrect
   (`app/api/auth/[...betterauth]/route.ts`)
2. `BETTER_AUTH_SECRET` is missing or mismatched between frontend and backend
3. Cookies are not being set due to CORS or missing `credentials: "include"`
4. Redirect relies on defaults instead of explicit `callbackUrl`
5. Backend rejects or never receives JWT

---

## Required Environment Variables

### Frontend (`.env.local`)
```env
BETTER_AUTH_SECRET=dev_super_secret_123
NEXT_PUBLIC_BETTER_AUTH_URL=http://localhost:3000
NEXT_PUBLIC_API_URL=http://localhost:8000
Backend (.env)
env
Copy code
BETTER_AUTH_SECRET=dev_super_secret_123
DATABASE_URL=postgresql+psycopg2://user:pass@neon/db
⚠️ The secret must be identical in both services.

Required Route Contract (Next.js App Router)
Path:

bash
Copy code
app/api/auth/[...betterauth]/route.ts
Requirements:

Must export BOTH GET and POST

Must directly return Better Auth handler

No custom wrappers or logic

If this route is incorrect, authentication will never work.

Signup Flow Specification
User submits email + password

Better Auth creates user

Session cookie is issued

User is redirected to /dashboard

Failure behavior:

User remains on signup page

Error message is shown

❌ No redirect to /api/auth/error

Login Flow Specification
User submits credentials

Session is restored

User is redirected to /dashboard

Redirect Rules (Mandatory)
All auth actions MUST explicitly define:

ts
Copy code
callbackUrl: "/dashboard"
Implicit redirects are forbidden.

Cookie & CORS Contract
Backend (FastAPI)
allow_credentials = true

allow_origins = ["http://localhost:3000"]

Frontend
ts
Copy code
fetch(url, {
  credentials: "include"
})
Without this, cookies will never persist.

Success Criteria (All Required)
Signup creates a user record

Login creates a session cookie

Cookie visible in browser devtools

Refresh keeps user logged in

Redirect always goes to /dashboard

/api/auth/error is never triggered
```

## Response Text

Successfully created the feature specification for the auth core fix with:

1. Four user stories covering registration flow, login flow, session persistence, and protected route access
2. Fifteen functional requirements addressing signup, login, session management, redirects, CORS, and error handling
3. Seven measurable success criteria with specific metrics
4. Two key entities (User Session, User Credentials)
5. Comprehensive edge cases covering token expiration, invalid tokens, and network errors

The specification follows all required sections and is written at a user-focused level without implementation details. All acceptance scenarios are clearly defined with Given/When/Then format, and the scope is clearly bounded as specified.

## Outcome

The specification is complete and ready for the planning phase. It addresses all core authentication issues and provides clear requirements for implementation of signup, login, and session management functionality.