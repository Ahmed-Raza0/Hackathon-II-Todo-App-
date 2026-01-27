---
id: 2
title: Auth Core Fix Planning
stage: plan
date_iso: 2026-01-20
surface: agent
model: qwen-2.5-72b-instruct
feature: 001-auth-core-fix
branch: 001-auth-core-fix
user: Claude
command: sp.plan
labels: ["plan", "auth", "frontend", "backend", "authentication", "better-auth", "nextjs", "fastapi"]
links:
  spec: /mnt/d/Hackathon II (Todo App)/Phase-3/specs/001-auth-core-fix/spec.md
  plan: /mnt/d/Hackathon II (Todo App)/Phase-3/specs/001-auth-core-fix/plan.md
  ticket: null
  adr: null
  pr: null
files:
  - specs/001-auth-core-fix/plan.md
  - specs/001-auth-core-fix/research.md
  - specs/001-auth-core-fix/data-model.md
  - specs/001-auth-core-fix/quickstart.md
  - specs/001-auth-core-fix/contracts/auth-contracts.md
  - history/prompts/001-auth-core-fix/002-auth-core-fix-planning.plan.prompt.md
tests: []
---

# Auth Core Fix Planning

## Summary

Completed comprehensive planning for the frontend and backend authentication integration. Created all required design artifacts including research, data model, API contracts, and quickstart guide. The plan is aligned with the feature specification and project constitution, ensuring proper JWT-based authentication flow between frontend and backend.

## Prompt Text

```
# Plan: Frontend & Backend Login/Signup Integration

## Objective
Implement a fully functional authentication system for the Todo App, integrating **FastAPI backend** and **Next.js frontend**, including:

- Signup & Login pages
- JWT-based session management
- Route protection (dashboard, user-specific data)
- Error handling & validation

---

## Phases & Tasks

### Phase 1: Setup (T001-T003)
- **T001 [P]** Initialize frontend env variables (`NEXT_PUBLIC_API_BASE`, `NEXT_PUBLIC_BETTER_AUTH_SECRET`, etc.)
- **T002 [P]** Initialize backend env variables (`DATABASE_URL`, `JWT_SECRET`, `BETTER_AUTH_SECRET`, `CORS_ORIGINS`)
- **T003 [ ]** Verify FastAPI CORS setup for localhost:3000 and localhost:3001

---

### Phase 2: Backend Auth Implementation (T004-T012)
- **T004 [P] [US1]** Create `/api/auth/signup` endpoint in FastAPI
- **T005 [P] [US1]** Implement password hashing & user validation
- **T006 [P] [US1]** Generate JWT token on signup
- **T007 [P] [US2]** Create `/api/auth/login` endpoint
- **T008 [P] [US2]** Validate credentials & generate JWT token on login
- **T009 [ ] [US3]** Implement `/api/auth/me` to verify JWT and return user info
- **T010 [ ] [US3]** Middleware for JWT verification on protected routes
- **T011 [ ] [US4]** Add logout endpoint (optional, clear cookies)
- **T012 [ ] [US4]** Write unit tests for auth endpoints

---

### Phase 3: Frontend Pages & API Integration (T013-T022)
- **T013 [P] [US1]** Create `/signup` page with form (`name`, `email`, `password`)
- **T014 [P] [US1]** POST signup data to `/api/auth/signup`
- **T015 [ ] [US1]** Handle JWT response: store in `httpOnly` cookie / localStorage
- **T016 [P] [US2]** Create `/login` page with form (`email`, `password`)
- **T017 [P] [US2]** POST login data to `/api/auth/login`
- **T018 [ ] [US2]** Handle JWT response: store securely
- **T019 [ ] [US3]** Implement `/dashboard` page with JWT verification
- **T020 [ ] [US3]** Fetch user tasks after JWT verification
- **T021 [ ] [US4]** Redirect unauthenticated users from dashboard/login pages
- **T022 [ ] [US4]** Display error messages for invalid credentials

---

### Phase 4: Integration & Testing (T023-T027)
- **T023 [ ]** Test signup → JWT issued → dashboard accessible
- **T024 [ ]** Test login → JWT issued → dashboard accessible
- **T025 [ ]** Test access without JWT → redirect to login
- **T026 [ ]** Test logout functionality (if implemented)
- **T027 [ ]** Validate cross-origin requests (frontend-backend)

---

## User Story Mapping
- **US1:** Signup functionality
- **US2:** Login functionality
- **US3:** Dashboard access & JWT session management
- **US4:** Route protection & error handling

---

## Notes & Considerations
- JWT algorithm: HS256, expiry: 7 days
- Store JWT in `httpOnly` cookie for security
- Ensure environment variables are correctly loaded in both frontend & backend
- Follow consistent naming for API endpoints (`/api/auth/...`)
- Validate email format, password length, and uniqueness

---

## Deliverables
- Fully functional signup & login pages
- JWT authentication integrated between frontend & backend
- Protected dashboard route with task fetching
- Error messages for invalid credentials
- Documentation for environment variables and setup
```

## Response Text

Successfully completed the implementation planning for the Auth Core Fix feature with all required design artifacts:

1. **Research Document** (`research.md`): Comprehensive analysis of technology decisions including JWT algorithm (HS256), session storage approach (httpOnly cookies), framework choices (Next.js 16+, FastAPI), and authentication library (Better Auth).

2. **Data Model** (`data-model.md`): Detailed entity definitions for User Session, User Credentials, and Authentication Handler with attributes, relationships, validation rules, and state transitions.

3. **API Contracts** (`contracts/auth-contracts.md`): Complete specification of authentication endpoints with request/response formats, headers, validation rules, and error handling.

4. **Quickstart Guide** (`quickstart.md`): Step-by-step setup instructions for both frontend and backend, including environment configuration, running the application, and testing the authentication flows.

5. **Agent Context Update**: Updated CLAUDE.md with new authentication technology stack information.

The plan follows all constitution requirements including:
- JWT authentication with proper token handling
- User isolation with user_id filtering
- Stateless architecture with no server-side session storage
- Layered responsibility with frontend handling UI and backend handling business logic
- Technology stack compliance with Neon PostgreSQL and SQLModel

All components are properly structured for the Next.js App Router and FastAPI backend integration, with proper CORS configuration and security measures.

## Outcome

The implementation plan is complete and all design artifacts have been generated. The frontend and backend authentication integration is ready for the task generation phase. All required contracts, data models, and integration patterns have been specified to ensure proper JWT-based authentication flow between the Next.js frontend and FastAPI backend.