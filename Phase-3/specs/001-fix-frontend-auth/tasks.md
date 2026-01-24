---
description: "Task list for auth core fix feature - frontend authentication and dashboard"
---

# Tasks: Auth Core Fix

**Input**: Design documents from `/specs/001-fix-frontend-auth/`
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

- [X] T001 Create project structure per implementation plan in backend/ and frontend/
- [X] T002 [P] Initialize backend with FastAPI dependencies in backend/requirements.txt
- [X] T003 [P] Initialize frontend with Next.js 16+ dependencies in frontend/package.json
- [X] T004 Configure environment variables in backend/.env and frontend/.env.local
- [X] T005 Setup gitignore files for backend and frontend with appropriate patterns

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Core infrastructure that MUST be complete before ANY user story can be implemented

**⚠️ CRITICAL**: No user story work can begin until this phase is complete

**Foundation tasks based on research and data model:**

- [X] T006 Setup database connection in backend/database.py with Neon PostgreSQL
- [X] T007 [P] Configure JWT authentication middleware in backend/middleware/auth_middleware.py
- [X] T008 [P] Create Better Auth integration in both frontend and backend
- [X] T009 Create Task model in backend/models/task.py with proper validation
- [X] T010 Setup CORS middleware in backend/main.py to allow frontend origin
- [X] T011 Create API client in frontend/lib/api.ts with JWT handling
- [X] T012 Setup user session management with token validation

**Checkpoint**: Foundation ready - user story implementation can now begin in parallel

---

## Phase 3: User Story 1 - Registration Flow (Priority: P1) 🎯 MVP

**Goal**: Enable users to create accounts with email, password, and optional name with proper user record creation and session establishment

**Independent Test**: Can be fully tested by navigating to the signup page, entering valid credentials, and verifying successful account creation with redirect to `/dashboard`.

### Implementation for User Story 1

- [X] T013 [P] [US1] Create signup page in frontend/app/signup/page.tsx with form validation
- [X] T014 [P] [US1] Create user registration endpoint POST /api/auth/signup in backend/routes/auth.py
- [X] T015 [US1] Implement user creation logic in backend/services/auth_service.py with password hashing
- [X] T016 [US1] Add client-side validation to signup form with proper error states
- [X] T017 [US1] Implement success redirect to `/dashboard` after registration
- [X] T018 [US1] Add error handling for duplicate email scenarios
- [X] T019 [US1] Create user model in backend/models/user.py with proper validation
- [X] T020 [US1] Update frontend signup form to use Better Auth integration
- [X] T021 [US1] Test complete registration flow with valid credentials

**Checkpoint**: At this point, User Story 1 should be fully functional and testable independently

---

## Phase 4: User Story 2 - Login Flow (Priority: P1)

**Goal**: Enable users to log in with their credentials with proper session restoration and redirect to dashboard

**Independent Test**: Can be fully tested by navigating to the login page, entering valid credentials, and verifying successful authentication with proper session restoration and redirect to `/dashboard`.

### Implementation for User Story 2

- [X] T022 [P] [US2] Create login page in frontend/app/login/page.tsx with form validation
- [X] T023 [US2] Create login endpoint POST /api/auth/login in backend/routes/auth.py
- [X] T024 [US2] Implement authentication logic in backend/services/auth_service.py with credential verification
- [X] T025 [US2] Add client-side validation to login form with proper error states
- [X] T026 [US2] Implement success redirect to `/dashboard` after login
- [X] T027 [US2] Add error handling for invalid credentials
- [X] T028 [US2] Update frontend login form to use Better Auth integration
- [X] T029 [US2] Test complete login flow with valid credentials
- [X] T030 [US2] Test error handling with invalid credentials

**Checkpoint**: At this point, User Story 2 should be fully functional and testable independently

---

## Phase 5: User Story 3 - Session Persistence (Priority: P2)

**Goal**: Maintain user sessions across page refreshes and navigation with proper cookie persistence

**Independent Test**: Can be fully tested by authenticating, refreshing the page, navigating to different routes, and verifying the user remains logged in.

### Implementation for User Story 3

- [X] T031 [P] [US3] Implement session storage using httpOnly cookies in backend/auth.py
- [X] T032 [US3] Create session validation middleware in frontend/middleware.ts
- [X] T033 [US3] Add session refresh mechanism for token expiration handling
- [X] T034 [US3] Implement proper token validation in frontend/lib/api.ts
- [X] T035 [US3] Add automatic logout when session expires
- [X] T036 [US3] Test session persistence across page refreshes
- [X] T037 [US3] Test session persistence across browser tabs/windows
- [X] T038 [US3] Validate that sessions properly clear on logout

**Checkpoint**: At this point, User Story 3 should be fully functional and testable independently

---

## Phase 6: User Story 4 - Protected Route Access (Priority: P2)

**Goal**: Prevent unauthenticated users from accessing protected routes like `/dashboard` with proper redirects to login page

**Independent Test**: Can be fully tested by attempting to access protected routes without authentication and verifying proper redirects to `/login`.

### Implementation for User Story 4

- [X] T039 [P] [US4] Create middleware.ts for route protection in frontend/
- [X] T040 [US4] Implement auth guard for protected routes in middleware.ts
- [X] T041 [US4] Add redirect logic to `/login` for unauthenticated users
- [X] T042 [US4] Create dashboard page in frontend/app/dashboard/page.tsx
- [X] T043 [US4] Add conditional rendering for authenticated users in dashboard page
- [X] T044 [US4] Update landing page in frontend/app/page.tsx with auth redirect logic
- [X] T045 [US4] Test route protection by accessing dashboard without authentication
- [X] T046 [US4] Test route protection by accessing dashboard with authentication
- [X] T047 [US4] Validate that authenticated users are redirected from login to dashboard

**Checkpoint**: At this point, User Story 4 should be fully functional and testable independently

---

## Phase 7: Integration & Validation (Priority: P2)

**Goal**: Ensure all authentication components work together correctly with proper session management and error handling

**Independent Test**: Can be fully tested by completing the full authentication flow (signup → login → dashboard → logout → login) and verifying proper session management throughout.

### Implementation for Integration & Validation

- [X] T048 [US5] Test complete auth flow: signup → login → dashboard → logout → login
- [X] T049 [US5] Verify user isolation (no cross-user data access)
- [X] T050 [US5] Test JWT token handling between frontend and backend
- [X] T051 [US5] Validate CORS configuration for auth requests
- [X] T052 [US5] Test error scenarios: invalid credentials, expired tokens, network errors
- [X] T053 [US5] Run manual auth flow validation to ensure all requirements are met
- [X] T054 [US5] Update API contracts in contracts/ with final endpoint specifications

**Checkpoint**: At this point, the complete authentication flow should be functional and testable

---

## Phase N: Polish & Cross-Cutting Concerns

**Purpose**: Improvements that affect multiple user stories

- [X] T055 [P] Update documentation in docs/ with authentication setup instructions
- [X] T056 Code cleanup and refactoring across auth components
- [X] T057 Performance optimization for authentication flow
- [X] T058 [P] Add comprehensive error handling and logging to auth flow
- [X] T059 Security hardening and validation (password strength, rate limiting)
- [X] T060 Run quickstart.md validation to ensure setup instructions work
- [X] T061 Add loading states to auth forms for better UX
- [X] T062 Add proper accessibility attributes to auth forms

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
3. Complete Phase 3: User Story 1 (Registration Flow)
4. **STOP and VALIDATE**: Test User Story 1 independently
5. Deploy/demo if ready

### Incremental Delivery

1. Complete Setup + Foundational → Foundation ready
2. Add User Story 1 → Test independently → Deploy/Demo (MVP!)
3. Add User Story 2 → Test independently → Deploy/Demo
4. Add User Story 3 → Test independently → Deploy/Demo
5. Add User Story 4 → Test independently → Deploy/Demo
6. Add Integration & Validation → Test complete flow → Deploy/Demo
7. Each story adds value without breaking previous stories

### Parallel Team Strategy

With multiple developers:

1. Team completes Setup + Foundational together
2. Once Foundational is done:
   - Developer A: User Story 1
   - Developer B: User Story 2
   - Developer C: User Story 3
   - Developer D: User Story 4
3. Stories complete and integrate independently

---

## Notes

- [P] tasks = different files, no dependencies
- [US1], [US2], [US3], [US4] labels map task to specific user story for traceability
- Each user story should be independently completable and testable
- Commit after each task or logical group
- Stop at any checkpoint to validate story independently
- Avoid: vague tasks, same file conflicts, cross-story dependencies that break independence