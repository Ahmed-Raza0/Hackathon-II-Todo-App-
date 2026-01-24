---
description: "Task list for auth redirect fix feature"
---

# Tasks: Auth Redirect Fix

**Input**: Design documents from `/specs/001-auth-redirect-fix/`
**Prerequisites**: plan.md (required), spec.md (required for user stories), research.md, data-model.md, contracts/

**Tests**: The examples below include test tasks. Tests are OPTIONAL - only include them if explicitly requested in the feature specification.

**Organization**: Tasks are grouped by user story to enable independent implementation and testing of each story.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1, US2, US3)
- Include exact file paths in descriptions

## Path Conventions

- **Single project**: `src/`, `tests/` at repository root
- **Web app**: `backend/src/`, `frontend/src/`
- **Mobile**: `api/src/`, `ios/src/` or `android/src/`
- Paths shown below assume web app - adjust based on plan.md structure

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Project initialization and basic structure

- [ ] T001 Create project structure per implementation plan in backend/ and frontend/
- [ ] T002 [P] Install frontend dependencies: Better Auth client, fetch wrapper, form helpers
- [ ] T003 [P] Install backend dependencies: FastAPI, SQLModel, python-jose, better-auth
- [ ] T004 Configure environment variables in backend/.env and frontend/.env.local
- [ ] T005 Setup gitignore files for backend and frontend with appropriate patterns

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Core infrastructure that MUST be complete before ANY user story can be implemented

**⚠️ CRITICAL**: No user story work can begin until this phase is complete

**Foundation tasks based on research and data model:**

- [ ] T006 Setup database connection in backend/database.py with Neon PostgreSQL
- [ ] T007 [P] Configure JWT authentication middleware in backend/middleware/auth_middleware.py
- [ ] T008 [P] Create Better Auth integration in both frontend and backend
- [ ] T009 Create User and Task models in backend/models/ with proper validation
- [ ] T010 Setup CORS middleware in backend/main.py to allow frontend origin with credentials
- [ ] T011 Create API client in frontend/lib/api.ts with JWT handling
- [ ] T012 Setup user session management with token validation and httpOnly cookies

**Checkpoint**: Foundation ready - user story implementation can now begin in parallel

---

## Phase 3: User Story 1 - Successful Authentication Flow (Priority: P1) 🎯 MVP

**Goal**: Enable users to sign up or log in without encountering redirect errors to `/api/auth/error`

**Independent Test**: Can be fully tested by navigating to the signup/login page, entering valid credentials, and verifying successful authentication with proper redirect to `/dashboard`.

### Implementation for User Story 1

- [ ] T013 [P] [US1] Create `/app/login/page.tsx` with email and password fields
- [ ] T014 [P] [US1] Create `/app/signup/page.tsx` with email, password, and name fields
- [ ] T015 [US1] Implement signup endpoint POST /api/auth/signup in backend/routes/auth.py
- [ ] T016 [US1] Implement login endpoint POST /api/auth/login in backend/routes/auth.py
- [ ] T017 [US1] Implement user verification endpoint GET /api/auth/me in backend/routes/auth.py
- [ ] T018 [US1] Create AuthService in backend/services/auth_service.py for JWT operations
- [ ] T019 [US1] Create AuthProvider in frontend/providers/AuthProvider.tsx for session management
- [ ] T020 [US1] Implement logout functionality in both frontend and backend
- [ ] T021 [US1] Add proper error handling and validation to auth endpoints
- [ ] T022 [US1] Update signup/login forms to redirect to `/dashboard` on success instead of `/api/auth/error`

**Checkpoint**: At this point, User Story 1 should be fully functional and testable independently

---

## Phase 4: User Story 2 - Error Handling (Priority: P1)

**Goal**: When authentication fails, users should receive proper error feedback instead of being redirected to `/api/auth/error`

**Independent Test**: Can be fully tested by attempting to log in with invalid credentials and verifying appropriate error messages are displayed without redirecting to `/api/auth/error`.

### Implementation for User Story 2

- [ ] T023 [US2] Update login endpoint to return proper error messages instead of redirecting to `/api/auth/error`
- [ ] T024 [US2] Update signup endpoint to return proper error messages instead of redirecting to `/api/auth/error`
- [ ] T025 [US2] Implement client-side error display in login form without redirecting to error page
- [ ] T026 [US2] Implement client-side error display in signup form without redirecting to error page
- [ ] T027 [US2] Add validation to prevent weak passwords during signup
- [ ] T028 [US2] Add validation to prevent invalid emails during signup/login
- [ ] T029 [US2] Update auth middleware to handle expired tokens gracefully
- [ ] T030 [US2] Add network error handling for auth API calls

**Checkpoint**: At this point, User Story 2 should be fully functional and testable independently

---

## Phase 5: User Story 3 - Session Persistence (Priority: P2)

**Goal**: After successful authentication, users should maintain their session across page refreshes and navigation

**Independent Test**: Can be fully tested by logging in, refreshing the page, and verifying the user remains authenticated.

### Implementation for User Story 3

- [ ] T031 [US3] Configure httpOnly cookies for JWT storage in Better Auth backend
- [ ] T032 [US3] Implement session validation on frontend using Better Auth hooks
- [ ] T033 [US3] Create session refresh mechanism for token expiration handling
- [ ] T034 [US3] Add session persistence across page refreshes in frontend
- [ ] T035 [US3] Implement proper token expiration checks in API client
- [ ] T036 [US3] Add automatic logout when session expires
- [ ] T037 [US3] Test session persistence across browser tabs and windows
- [ ] T038 [US3] Validate that sessions properly clear on logout

**Checkpoint**: At this point, User Story 3 should be fully functional and testable independently

---

## Phase 6: Integration & Validation (Priority: P2)

**Goal**: Ensure all authentication components work together correctly with proper redirects and error handling

**Independent Test**: Can be fully tested by completing the full authentication flow (signup/login) and verifying proper redirects and session management.

### Implementation for Integration & Validation

- [ ] T039 [US4] Implement middleware.ts to protect `/dashboard` routes and redirect unauthenticated users to `/login`
- [ ] T040 [US4] Create `/app/dashboard/page.tsx` with proper authentication check
- [ ] T041 [US4] Update landing page `/app/page.tsx` with auth-aware routing
- [ ] T042 [US4] Test complete auth flow: signup → login → dashboard → logout → login
- [ ] T043 [US4] Verify that authenticated users are redirected from login/signup to dashboard
- [ ] T044 [US4] Test error scenarios: invalid credentials, expired tokens, network errors
- [ ] T045 [US4] Validate JWT token handling between frontend and backend
- [ ] T046 [US4] Test user isolation (ensure users can't access other users' data)

**Checkpoint**: At this point, the complete authentication flow should be functional and testable

---

## Phase N: Polish & Cross-Cutting Concerns

**Purpose**: Improvements that affect multiple user stories

- [ ] T047 [P] Update documentation in docs/ with authentication setup instructions
- [ ] T048 Code cleanup and refactoring across auth components
- [ ] T049 Performance optimization for authentication flow
- [ ] T050 [P] Add comprehensive error handling and logging to auth flow
- [ ] T051 Security hardening and validation (password strength, rate limiting)
- [ ] T052 Run quickstart.md validation to ensure setup instructions work
- [ ] T053 Update API contracts in contracts/ with final endpoint specifications
- [ ] T054 Create integration tests for the complete auth flow

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies - can start immediately
- **Foundational (Phase 2)**: Depends on Setup completion - BLOCKS all user stories
- **User Stories (Phase 3+)**: All depend on Foundational phase completion
  - User stories can then proceed in parallel (if staffed)
  - Or sequentially in priority order (P1 → P2 → P3)

### User Story Dependencies

- **User Story 1 (P1)**: Can start after Foundational (Phase 2) - No dependencies on other stories
- **User Story 2 (P1)**: Can start after Foundational (Phase 2) - May integrate with US1 but should be independently testable
- **User Story 3 (P2)**: Can start after Foundational (Phase 2) - Integrates with US1/US2 but should be independently testable
- **User Story 4 (P2)**: Can start after Foundational (Phase 2) - Integrates with US1/US2/US3 but should be independently testable

### Within Each User Story

- Models before services
- Services before endpoints
- Core implementation before integration
- Story complete before moving to next priority

### Parallel Opportunities

- All Setup tasks marked [P] can run in parallel
- All Foundational tasks marked [P] can run in parallel (within Phase 2)
- Once Foundational phase completes, all user stories can start in parallel (if team capacity allows)
- Models within a story marked [P] can run in parallel
- Different user stories can be worked on in parallel by different team members

---

## Implementation Strategy

### MVP First (User Story 1 Only)

1. Complete Phase 1: Setup
2. Complete Phase 2: Foundational (CRITICAL - blocks all stories)
3. Complete Phase 3: User Story 1 (Successful Authentication Flow)
4. **STOP and VALIDATE**: Test User Story 1 independently
5. Deploy/demo if ready

### Incremental Delivery

1. Complete Setup + Foundational → Foundation ready
2. Add User Story 1 → Test independently → Deploy/Demo (MVP!)
3. Add User Story 2 → Test independently → Deploy/Demo
4. Add User Story 3 → Test independently → Deploy/Demo
5. Add Integration & Validation → Test complete flow → Deploy/Demo
6. Each story adds value without breaking previous stories

### Parallel Team Strategy

With multiple developers:

1. Team completes Setup + Foundational together
2. Once Foundational is done:
   - Developer A: User Story 1
   - Developer B: User Story 2
   - Developer C: User Story 3
3. Stories complete and integrate independently

---

## Notes

- [P] tasks = different files, no dependencies
- [US1], [US2], [US3], [US4] labels map task to specific user story for traceability
- Each user story should be independently completable and testable
- Commit after each task or logical group
- Stop at any checkpoint to validate story independently
- Avoid: vague tasks, same file conflicts, cross-story dependencies that break independence