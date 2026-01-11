# Tasks: Production Deployment Configuration Fix

**Input**: Design documents from `/specs/001-deployment-config-fix/`
**Prerequisites**: plan.md, spec.md, research.md, data-model.md, contracts/api-contracts.md

**Tests**: Tests are NOT requested in the specification. This task list focuses on configuration and deployment fixes only.

**Organization**: Tasks are organized by user story to enable independent implementation and testing of each story.

## Format: `- [ ] [ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1, US2, US3)
- Include exact file paths in descriptions

## Path Conventions

This is a **full-stack application** with separate frontend and backend:

**Frontend (Next.js)**:
- Directory: `frontend/`
- Components: `frontend/components/`
- Pages: `frontend/app/`
- Business logic: `frontend/lib/`
- Configuration: `frontend/` root

**Backend (FastAPI)**:
- Directory: `Todo-backend/`
- Main app: `Todo-backend/main.py`
- Routes: `Todo-backend/src/routes/`
- Models: `Todo-backend/src/models/`
- Business logic: `Todo-backend/src/services/`

---

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Project initialization and environment preparation

- [x] T001 Verify project directory structure matches Next.js 16 App Router pattern
- [x] T002 [P] Locate backend directory and verify FastAPI package structure
- [x] T003 [P] Verify current environment variable configuration in both frontend and backend
- [x] T004 [P] Check current Tailwind CSS configuration files exist (tailwind.config.ts, postcss.config.mjs)
- [x] T005 [P] Verify current API client configuration in frontend
- [x] T006 [P] Check current CORS configuration in backend
- [x] T007 [P] Verify current deployment configuration files (vercel.json, Dockerfile if exists)
- [x] T008 [P] Identify current build process and output structure
- [x] T009 [P] Document current directory structure and file locations
- [x] T010 [P] Set up local environment with correct API base URLs for testing
- [x] T011 [P] Verify existing dependencies are correctly installed
- [x] T012 [P] Test current frontend build process to identify Tailwind issues
- [x] T013 [P] Test current backend startup process to identify runtime errors
- [x] T014 [P] Document current error messages and symptoms
- [x] T015 Create setup verification checklist for deployment testing

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Core configuration fixes that MUST be complete before ANY user story can be implemented

**⚠️ CRITICAL**: No user story work can begin until this phase is complete

- [x] T016 [P] Fix Tailwind CSS content paths in tailwind.config.ts to include App Router structure
- [x] T017 [P] Verify global CSS is properly imported in frontend root layout
- [x] T018 [P] Ensure PostCSS configuration exists and loads correctly in frontend
- [x] T019 [P] Fix backend startup by correcting Uvicorn module path in main.py
- [x] T020 [P] Fix backend import errors and package structure issues
- [x] T021 [P] Configure production-ready Uvicorn startup parameters (no reload, correct port binding)
- [x] T022 [P] Remove hardcoded localhost references from frontend API client
- [x] T023 [P] Ensure NEXT_PUBLIC environment variable prefixes are correctly used in frontend
- [x] T024 [P] Configure backend to read environment variables directly from production environment
- [x] T025 [P] Fix CORS configuration to allow production frontend domain
- [x] T026 [P] Verify Authorization header is allowed in CORS configuration for JWT
- [x] T027 [P] Ensure health/root endpoints bypass authentication middleware
- [x] T028 [P] Fix JWT validation to return structured errors instead of crashing
- [x] T029 [P] Configure proper error response format for API endpoints
- [x] T030 [P] Test basic frontend-backend communication with fixes

**Checkpoint**: Foundational fixes complete - user story implementation can now begin in parallel

---

## Phase 3: User Story 1 - Visual Rendering Fix (Priority: P1) 🎯 MVP

**Goal**: Fix Tailwind CSS rendering so UI appears properly styled in production. All Tailwind classes that work in development also work in production.

**Independent Test**: Deploy frontend to Vercel, verify all styling appears correctly (no unstyled UI elements), confirm Tailwind classes are preserved in production build.

**Dependencies**: Requires Phase 2 (foundational) to be complete

### Implementation for User Story 1

- [ ] T031 [P] [US1] Update tailwind.config.ts content paths to include all App Router directories
- [ ] T032 [P] [US1] Verify Tailwind classes are not being purged incorrectly in production
- [ ] T033 [P] [US1] Test Tailwind build process with production settings locally
- [ ] T034 [P] [US1] Verify all color classes from design system are preserved
- [ ] T035 [P] [US1] Test responsive classes work correctly in production build
- [ ] T036 [P] [US1] Confirm custom theme extensions are preserved in production
- [ ] T037 [P] [US1] Verify dynamic class generation doesn't break Tailwind purging
- [ ] T038 [P] [US1] Test CSS variables are properly applied in production
- [ ] T039 [P] [US1] Validate all component styling matches development appearance
- [ ] T040 [P] [US1] Deploy to Vercel staging and verify styling
- [ ] T041 [P] [US1] Test styling across different screen sizes in production
- [ ] T042 [P] [US1] Verify all interactive states (hover, focus, active) work correctly
- [ ] T043 [P] [US1] Test with disabled JavaScript to ensure CSS-only functionality
- [ ] T044 [P] [US1] Validate accessibility contrast ratios in production
- [ ] T045 [P] [US1] Test Tailwind JIT compilation settings for production
- [ ] T046 [P] [US1] Run visual regression tests if available
- [ ] T047 [US1] Complete visual rendering verification checklist

## Phase 4: User Story 2 - API Communication Fix (Priority: P1)

**Goal**: Fix frontend-backend communication so API requests succeed in production. All API operations work correctly between services.

**Independent Test**: Frontend makes API requests to backend, verify requests succeed with proper CORS handling, authentication tokens are transmitted correctly, responses are processed properly.

**Dependencies**: Requires Phase 2 (foundational) to be complete

### Implementation for User Story 2

- [ ] T048 [P] [US2] Configure frontend API client to use production backend URL
- [ ] T049 [P] [US2] Test GET requests to backend API endpoints
- [ ] T050 [P] [US2] Test POST requests to backend API endpoints
- [ ] T051 [P] [US2] Test PATCH/PUT requests to backend API endpoints
- [ ] T052 [P] [US2] Test DELETE requests to backend API endpoints
- [ ] T053 [P] [US2] Verify JWT tokens are properly attached to requests
- [ ] T054 [P] [US2] Test authentication flow with deployed services
- [ ] T055 [P] [US2] Verify error responses are properly handled
- [ ] T056 [P] [US2] Test preflight OPTIONS requests are handled by CORS
- [ ] T057 [P] [US2] Validate request headers are properly transmitted
- [ ] T058 [P] [US2] Test response parsing and error handling
- [ ] T059 [P] [US2] Verify timeout handling works correctly
- [ ] T060 [P] [US2] Test concurrent API requests don't cause issues
- [ ] T061 [P] [US2] Validate request/response logging for debugging
- [ ] T062 [P] [US2] Test API rate limiting if implemented
- [ ] T063 [US2] Complete API communication verification checklist

## Phase 5: User Story 3 - Environment Configuration Fix (Priority: P1)

**Goal**: Fix environment variable handling so configuration works consistently across local and production environments. All required variables load correctly in each environment.

**Independent Test**: Application runs in local, staging, and production environments, verify correct environment variables are loaded, backend URLs resolve correctly, authentication and database connections work appropriately.

**Dependencies**: Requires Phase 2 (foundational) to be complete

### Implementation for User Story 3

- [ ] T064 [P] [US3] Configure environment-specific backend API URL for frontend
- [ ] T065 [P] [US3] Set up production environment variables for backend (DATABASE_URL, JWT_SECRET)
- [ ] T066 [P] [US3] Configure CORS allowed origins for production domain
- [ ] T067 [P] [US3] Test environment variable loading in different deployment stages
- [ ] T068 [P] [US3] Verify environment-specific configuration doesn't leak between stages
- [ ] T069 [P] [US3] Test fallback configurations when environment variables are missing
- [ ] T070 [P] [US3] Validate environment variable validation and error messages
- [ ] T071 [P] [US3] Configure Vercel environment variables for frontend deployment
- [ ] T072 [P] [US3] Set up cloud hosting environment variables for backend
- [ ] T073 [P] [US3] Test environment variable encryption/security in production
- [ ] T074 [P] [US3] Verify runtime environment detection works correctly
- [ ] T075 [P] [US3] Test configuration reload when environment variables change
- [ ] T076 [P] [US3] Validate environment-specific logging levels
- [ ] T077 [P] [US3] Test configuration validation during startup
- [ ] T078 [P] [US3] Document environment variable requirements and setup process
- [ ] T079 [US3] Complete environment configuration verification checklist

## Phase 6: User Story 4 - Backend Stability Fix (Priority: P2)

**Goal**: Fix backend startup and runtime stability issues. Backend starts without errors and handles requests reliably in production.

**Independent Test**: Backend starts successfully without tracebacks, exposes health endpoints, handles authentication errors gracefully, maintains stable connections.

**Dependencies**: Requires Phase 2 (foundational) to be complete

### Implementation for User Story 4

- [ ] T080 [P] [US4] Fix all import errors and startup crashers in FastAPI application
- [ ] T081 [P] [US4] Validate all API route function signatures follow Python rules
- [ ] T082 [P] [US4] Fix parameter ordering in API route functions
- [ ] T083 [P] [US4] Verify dependency injection parameters don't break function ordering
- [ ] T084 [P] [US4] Test backend startup with production configuration
- [ ] T085 [P] [US4] Verify health check endpoints work without authentication
- [ ] T086 [P] [US4] Test graceful error handling for database connection failures
- [ ] T087 [P] [US4] Validate JWT validation doesn't crash on invalid tokens
- [ ] T088 [P] [US4] Test backend restart resilience and connection recovery
- [ ] T089 [P] [US4] Verify logging works correctly in production environment
- [ ] T090 [P] [US4] Test memory usage and garbage collection in long-running processes
- [ ] T091 [P] [US4] Validate request/response size limits and timeouts
- [ ] T092 [P] [US4] Test concurrent request handling capacity
- [ ] T093 [P] [US4] Verify proper shutdown and cleanup procedures
- [ ] T094 [P] [US4] Test error logging and monitoring integration
- [ ] T095 [US4] Complete backend stability verification checklist

## Phase 7: User Story 5 - Integration Verification (Priority: P2)

**Goal**: Verify full-stack integration works as a cohesive product. All components work together seamlessly in production environment.

**Independent Test**: Deploy both frontend and backend, test complete user workflows, verify error handling consistency, confirm application meets production standards.

**Dependencies**: Requires Phase 2 (foundational) and US1-US4 to be complete

### Implementation for User Story 5

- [ ] T096 [P] [US5] Deploy both frontend and backend to staging environment
- [ ] T097 [P] [US5] Test complete user authentication flow end-to-end
- [ ] T098 [P] [US5] Verify all CRUD operations work across frontend-backend
- [ ] T099 [P] [US5] Test error handling consistency across services
- [ ] T100 [P] [US5] Validate CORS behavior in real browser environment
- [ ] T101 [P] [US5] Test performance under realistic load conditions
- [ ] T102 [P] [US5] Verify security headers and response protection
- [ ] T103 [P] [US5] Test data consistency between frontend and backend
- [ ] T104 [P] [US5] Validate session management and token handling
- [ ] T105 [P] [US5] Test error recovery and retry mechanisms
- [ ] T106 [P] [US5] Verify logging and monitoring integration across services
- [ ] T107 [P] [US5] Test deployment rollback procedures
- [ ] T108 [P] [US5] Validate backup and recovery procedures
- [ ] T109 [P] [US5] Test cross-service debugging and tracing
- [ ] T110 [P] [US5] Verify production monitoring and alerting
- [ ] T111 [US5] Complete integration verification checklist

## Phase 8: Polish & Cross-Cutting Concerns

**Purpose**: Final quality improvements and cross-cutting concerns

- [ ] T112 [P] Add comprehensive error boundaries in frontend for production
- [ ] T113 [P] Implement proper logging and monitoring in backend
- [ ] T114 [P] Add performance monitoring and metrics collection
- [ ] T115 [P] Verify security headers and production best practices
- [ ] T116 [P] Optimize bundle sizes and asset loading
- [ ] T117 [P] Add proper loading states and skeleton screens
- [ ] T118 [P] Implement proper error handling and user feedback
- [ ] T119 [P] Add accessibility improvements and ARIA labels
- [ ] T120 [P] Optimize images and assets for production
- [ ] T121 [P] Add proper caching headers and strategies
- [ ] T122 [P] Verify mobile responsiveness in production
- [ ] T123 [P] Add proper SEO meta tags and social sharing
- [ ] T124 Final production deployment and verification testing
- [ ] T125 Document deployment process and troubleshooting guide

**Checkpoint**: All user stories should now be independently functional and production-ready.

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies - can start immediately
- **Foundational (Phase 2)**: Depends on Setup completion - BLOCKS all user stories
- **User Story 1 (Phase 3)**: Depends on Foundational completion - P1 priority, MVP
- **User Story 2 (Phase 4)**: Depends on Foundational completion - P1 priority
- **User Story 3 (Phase 5)**: Depends on Foundational completion - P1 priority
- **User Story 4 (Phase 6)**: Depends on Foundational completion - P2 priority
- **User Story 5 (Phase 7)**: Depends on Foundational + US1-4 completion - P2 priority
- **Polish (Phase 8)**: Depends on all user stories completion

### Parallel Execution Opportunities

Each user story phase can be worked on in parallel by different developers after Phase 2 completion:
- US1: Visual rendering team
- US2: API communication team
- US3: Environment configuration team
- US4: Backend stability team
- US5: Integration testing team

### Critical Path

The critical path goes through Phase 1 → Phase 2 → US1, US2, US3 (in parallel) → US4 → US5 → Phase 8

---

## Implementation Strategy

### MVP Approach

1. Complete Phase 1 & 2 (Foundational)
2. Complete US1 (Visual Rendering) - enables basic UI verification
3. Complete US2 (API Communication) - enables functionality verification
4. Complete US3 (Environment) - enables multi-environment deployment
5. This delivers a working MVP with proper styling and API communication

### Incremental Delivery

Each user story phase delivers independently testable functionality:
- US1: Styled UI works in production
- US2: API communication works end-to-end
- US3: Environment configuration works properly
- US4: Backend is stable and reliable
- US5: Full integration verified
- Phase 8: Production hardened