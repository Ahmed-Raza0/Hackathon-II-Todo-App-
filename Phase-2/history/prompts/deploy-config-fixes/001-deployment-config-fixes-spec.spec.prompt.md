---
id: 001
title: deployment-config-fixes-spec
stage: spec
date: 2026-01-10
surface: agent
model: claude-sonnet-4-5-20250929
feature: deploy-config-fixes
branch: 001-deploy-config-fixes
user: Ahmed-Raza0
command: "/sp.specify"
labels: ["deployment", "configuration", "specification", "frontend", "backend"]
links:
  spec: specs/001-deploy-config-fixes/spec.md
  ticket: null
  adr: null
  pr: null
files:
 - specs/001-deploy-config-fixes/spec.md
 - specs/001-deploy-config-fixes/checklists/requirements.md
tests:
 - none
---

## Prompt

You are operating in sp.specify mode.

Your task is to DIAGNOSE, ISOLATE, and FIX deployment, configuration, and integration issues
for a full-stack Todo application built with:

Next.js 16 (App Router) frontend deployed on Vercel

FastAPI backend deployed separately

Shared REST API contract

JWT-based authentication

PostgreSQL database

The application logic is complete.
UI, pages, components, and backend features already exist.

The system is currently NOT production-stable due to configuration and deployment errors.

Your goal is to produce a production-ready, hackathon-safe resolution plan that guarantees:

Successful frontend deployment

Successful backend deployment

Correct frontend–backend communication

Correct Tailwind CSS rendering

Correct environment variable handling

No runtime crashes

You MUST NOT:

Redesign UI

Rewrite business logic

Change database schema

Add features

Refactor architecture beyond configuration fixes

Only configuration, deployment, and integration correctness is allowed.

────────────────────────────────────
CORE CONTEXT (VERY IMPORTANT)
────────────────────────────────────

Frontend:

Built using Next.js 16 App Router

Uses Server Components by default

Uses Tailwind CSS for styling

Deployed on Vercel

Backend is NOT co-located (separate deployment)

Backend:

Built with FastAPI

Uses Uvicorn

Uses JWT authentication

Uses PostgreSQL

Deployed independently (not Vercel)

Current symptoms:

Vercel build succeeds but UI appears unstyled or broken

Tailwind CSS does not apply

API requests fail in production

Backend throws runtime/import/auth errors

Environment variables behave differently locally vs production────────────────────────────────────
FRONTEND (NEXT.JS 16) — REQUIRED DIAGNOSIS & FIXES
────────────────────────────────────

You must diagnose and specify fixes for:

Framework detection:

Confirm Vercel correctly detects Next.js 16 App Router

Confirm correct root directory

Confirm correct build command and output behavior

Ensure no legacy Pages Router assumptions exist

Environment variables (CRITICAL):

Backend API URL must be exposed using NEXT_PUBLIC_ prefix

No server-only env variables used in Client Components

Separate handling for:

Local development

Vercel production

No hardcoded localhost URLs anywhere in frontend code

API communication:

All API requests must resolve to the deployed backend URL

No relative URLs that assume same-origin backend

Clear distinction between:

Server-side fetch (Server Components)

Client-side fetch (Client Components)

Errors must propagate cleanly to UI

Tailwind CSS failure (CRITICAL):
You must identify and resolve:

Missing or incorrect Tailwind installation

Incorrect content paths for App Router (/app directory)

Missing global CSS import in root layout

Missing PostCSS configuration

Vercel build-time CSS purge issues

Any mismatch between dev and production behavior

App Router requirements:

Ensure global styles are imported in the root layout

Ensure no CSS imports inside Server Components incorrectly

Ensure Tailwind classes are not dynamically constructed in a way that breaks purge

Vercel-specific constraints:

Node.js version compatibility

Build cache behavior

Server vs Edge runtime mismatches

Disallowed filesystem or runtime APIs

────────────────────────────────────
BACKEND (FASTAPI) — REQUIRED DIAGNOSIS & FIXES
────────────────────────────────────

You must diagnose and specify fixes for:

Application startup:

Correct module path for Uvicorn

Correct package structure and init files

No import errors

No syntax errors

No reload-only assumptions in production

Environment variables:

Database URI loading

JWT secret loading

CORS origin loading

No reliance on local .env files in production

Clear separation of dev vs prod configuration

Authentication:

JWT validation correctness

Middleware ordering

Health and root endpoints must bypass auth

Auth errors must be explicit and non-crashing

CORS (CRITICAL):

Frontend production domain explicitly allowed

Credentials handling correct

Preflight requests handled

No wildcard misuse in production

Deployment readiness:

Uvicorn production command

Correct port binding

No reload mode

Cloud-host compatible configuration

────────────────────────────────────
FRONTEND–BACKEND INTEGRATION REQUIREMENTS
────────────────────────────────────

You must ensure:

Frontend and backend are fully decoupled

Backend URL is configurable via environment variables

Same API contract works locally and in production

Errors are traceae the system WORK PERFECTLY in production.
No redesign, no new features, no experiments.

The final system must be:

Stable

Predictable

Professional

Hackathon-evaluation ready

Deliver the answer as a senior production engineer preparing the project for final submission.

## Response snapshot

Successfully created a comprehensive specification for fixing deployment, configuration, and integration issues in the full-stack Todo application. Created feature branch '001-deploy-config-fixes' and developed a detailed specification document addressing frontend Tailwind CSS rendering, backend communication, environment variable handling, and production stability requirements.

## Outcome

- ✅ Impact: Created complete specification for deployment configuration fixes addressing all requirements from the user
- 🧪 Tests: none
- 📁 Files: specs/001-deploy-config-fixes/spec.md, specs/001-deploy-config-fixes/checklists/requirements.md
- 🔁 Next prompts: /sp.plan to create implementation plan for the fixes
- 🧠 Reflection: Clear specification with well-defined acceptance criteria and measurable success metrics enables predictable implementation

## Evaluation notes (flywheel)

- Failure modes observed: Script .specify/scripts/bash/create-phr.sh not found, had to create PHR manually
- Graders run and results (PASS/FAIL): PASS - Manual creation followed template correctly
- Prompt variant (if applicable): none
- Next experiment (smallest change to try): Implement automated script to create PHR files