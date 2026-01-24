---
id: 1
title: Fix Better Auth Redirects
stage: spec
date_iso: 2026-01-20
surface: agent
model: qwen-2.5-72b-instruct
feature: 001-auth-redirect-fix
branch: 001-auth-redirect-fix
user: Claude
command: sp.specify
labels: ["auth", "redirect", "better-auth", "frontend", "backend", "security"]
links:
  spec: /mnt/d/Hackathon II (Todo App)/specs/001-auth-redirect-fix/spec.md
  plan: null
  ticket: null
  adr: null
  pr: null
files:
  - specs/001-auth-redirect-fix/spec.md
  - specs/001-auth-redirect-fix/checklists/requirements.md
  - history/prompts/001-auth-redirect-fix/001-fix-better-auth-redirects.spec.prompt.md
tests: []
---

# Fix Better Auth Redirects

## Summary

Created comprehensive specification for fixing Better Auth signup and login redirect issues. The specification defines requirements for proper authentication flow, session management, and error handling to prevent redirects to `/api/auth/error` and ensure proper redirects to `/dashboard` upon successful authentication.

## Prompt Text

```
# sp.specify.auth-redirect-fix.md
Title

Fix Better Auth Signup & Login Redirect to /api/auth/error

Problem Statement (Observed)

When a user attempts to sign up or log in, the application redirects to:

/api/auth/error


Instead of:

/dashboard (success)

or a meaningful auth error page

This indicates Better Auth is failing during its internal callback phase.

Root Causes (Locked)

One or more of the following MUST be true (these are known Better Auth failure points):

1️⃣ BETTER_AUTH_SECRET mismatch or missing

Frontend and backend must share the same secret

If missing → Better Auth throws and redirects to /api/auth/error

2️⃣ Missing or incorrect Better Auth handler route

/api/auth/[...betterauth]/route.ts not configured correctly

App Router mismatch

3️⃣ Invalid callback / base URL

NEXT_PUBLIC_BETTER_AUTH_URL not set

Defaulting to invalid origin

4️⃣ Cookies blocked due to CORS / credentials

Backend not allowing credentials

Frontend fetch missing credentials: "include"

5️⃣ Missing user persistence adapter

Better Auth session created but user not stored

Redirect fails post-auth

Expected Correct Behavior
Signup Flow

User submits signup form

Better Auth creates user + session

JWT + cookies issued

Redirect → /dashboard

Login Flow

User submits credentials

Session restored

Redirect → /dashboard

Failure Case

User stays on /login

Error message shown

❌ NO redirect to /api/auth/error

Required Environment Variables (MANDATORY)
Frontend .env.local
BETTER_AUTH_SECRET=super-long-random-secret
NEXT_PUBLIC_BETTER_AUTH_URL=http://localhost:3000
NEXT_PUBLIC_API_URL=http://localhost:8000

Backend .env
BETTER_AUTH_SECRET=super-long-random-secret
DATABASE_URL=postgresql+psycopg2://...


⚠️ Secret MUST be identical in both services

Required Route Structure (Next.js App Router)
frontend/
└── app/
    └── api/
        └── auth/
            └── [...betterauth]/
                └── route.ts   ✅ REQUIRED

route.ts Contract

Must export GET and POST

Must use Better Auth handler directly

No custom logic allowed here

Redirect Configuration (Locked)
Signup
signUp({
  email,
  password,
  callbackUrl: "/dashboard"
})

Login
signIn({
  email,
  password,
  callbackUrl: "/dashboard"
})


❌ Do NOT rely on defaults

CORS & Cookies Contract
Backend (FastAPI)

allow_credentials=True

allow_origins=["http://localhost:3000"]

Frontend (fetch / auth client)
credentials: "include"


Without this → session cookie never reaches browser.

Validation Checklist (Must Pass All)

 Signup does NOT redirect to /api/auth/error

 Login redirects to /dashboard

 Cookies visible in browser devtools

 Refresh keeps user logged in

 Backend receives JWT correctly

Out of Scope (Explicit)

❌ UI styling

❌ Chatbot

❌ MCP

❌ Role-based auth

This spec is ONLY for fixing signup/login redirect failure.
```

## Response Text

Successfully created the feature specification for fixing Better Auth signup and login redirect issues. The specification includes:

1. **User Scenarios & Testing**: Defined 3 user stories covering successful authentication flow, error handling, and session persistence
2. **Functional Requirements**: Created 10 detailed requirements addressing the core authentication redirect problems
3. **Key Entities**: Defined User Session and Authentication Request entities
4. **Success Criteria**: Established 7 measurable outcomes with specific metrics
5. **Quality Checklist**: Created requirements checklist confirming all validation items passed

The specification addresses all root causes mentioned in the user input:
- BETTER_AUTH_SECRET configuration and synchronization
- Proper route structure for Better Auth handler
- CORS and credential handling
- Correct redirect configuration
- Session persistence requirements

All requirements are technology-agnostic, testable, and focused on user value rather than implementation details. The specification is ready for the planning phase.

## Outcome

The specification is complete and ready for the next phase (`/sp.plan`). It clearly defines the problem of redirects to `/api/auth/error` and establishes requirements to fix the authentication flow to properly redirect to `/dashboard` upon success. The spec includes comprehensive user scenarios, functional requirements, and success criteria to guide implementation.