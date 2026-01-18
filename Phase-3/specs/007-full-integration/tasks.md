# SP-FULL-INTEGRATION – Execution Tasks (Backend ↔ Frontend Integration & Build)

This **SP-TASKS** defines the **executable steps** for implementing the **SP-FULL-INTEGRATION** specification to ensure proper backend-frontend integration and build processes.

## Phase 1: Setup

### Goal
Initialize the environment and verify preconditions for integration.

### Independent Test Criteria
- SP-FULL-INTEGRATION specification is accessible
- Backend API is running and reachable
- Frontend development environment is set up
- Environment variables can be configured

### Tasks
- [x] T001 Verify SP-FULL-INTEGRATION specification document exists at specs/007-full-integration/spec.md
- [x] T002 Confirm backend API is running at http://127.0.0.1:8000
- [x] T003 Verify frontend development environment is properly configured

## Phase 2: Foundational

### Goal
Prepare the foundation with required API client and configuration.

### Independent Test Criteria
- API client exists and is properly configured
- Environment variables are set correctly
- CORS is properly configured on backend
- Authentication flow is functional

### Tasks
- [x] T004 [P] Create/verify API client exists at /frontend/src/lib/api.ts
- [x] T005 [P] Confirm NEXT_PUBLIC_API_BASE_URL environment variable is set to http://127.0.0.1:8000
- [x] T006 [P] Verify backend CORS is configured for http://localhost:3000
- [x] T007 [P] Test JWT authentication flow between frontend and backend

## Phase 3: API Integration [US1]

### Goal
Implement proper API communication between frontend and backend.

### Independent Test Criteria
- All API calls use centralized client
- JWT tokens are properly attached to requests
- Error responses are handled appropriately
- API endpoints follow /api/* pattern

### Tasks
- [x] T008 [US1] Verify all API calls go through centralized client in /frontend/src/lib/api.ts
- [x] T009 [US1] Confirm JWT tokens are attached to authenticated requests
- [x] T010 [US1] Test API error handling for different response codes (401, 403, 500)
- [x] T011 [US1] Validate all API endpoints follow /api/* pattern

## Phase 4: Authentication Flow [US2]

### Goal
Ensure JWT authentication works end-to-end between frontend and backend.

### Independent Test Criteria
- Login flow successfully retrieves JWT token
- Token is properly stored and attached to requests
- Logout flow clears token appropriately
- 401 responses trigger proper redirect behavior

### Tasks
- [x] T012 [US2] Test login flow and verify JWT token retrieval
- [x] T013 [US2] Confirm JWT token is stored securely and attached to requests
- [x] T014 [US2] Validate logout flow properly clears authentication tokens
- [x] T015 [US2] Test 401 response handling and redirect to login

## Phase 5: Task Management Integration [US3]

### Goal
Ensure task CRUD operations work properly with backend APIs.

### Independent Test Criteria
- Task creation sends proper POST request to /api/tasks
- Task retrieval sends proper GET request to /api/tasks
- Task updates send proper PUT/PATCH request to /api/tasks/{id}
- Task deletion sends proper DELETE request to /api/tasks/{id}

### Tasks
- [x] T016 [US3] Test task creation flow with POST /api/tasks
- [x] T017 [US3] Test task retrieval flow with GET /api/tasks
- [x] T018 [US3] Test task update flow with PUT/PATCH /api/tasks/{id}
- [x] T019 [US3] Test task deletion flow with DELETE /api/tasks/{id}

## Phase 6: Build & Validation [US4]

### Goal
Ensure production build processes work without errors.

### Independent Test Criteria
- Frontend builds successfully with no TypeScript errors
- Backend compiles without syntax errors
- Environment variables are properly used in build
- All integration points function in built application

### Tasks
- [x] T020 [US4] Run frontend build with `npm run build` and verify no errors
- [x] T021 [US4] Run backend compilation check with `python -m compileall .`
- [x] T022 [US4] Verify environment variables are properly configured in build
- [x] T023 [US4] Test built application functionality

## Phase 7: Quality Assurance [US5]

### Goal
Validate complete integration meets professional standards.

### Independent Test Criteria
- All pages load with proper styling and functionality
- Navigation works correctly between all routes
- Authentication flow works seamlessly
- All API calls succeed with proper responses

### Tasks
- [x] T024 [US5] Test complete user journey from login to task management
- [x] T025 [US5] Verify all navigation links work correctly
- [x] T026 [US5] Confirm header visibility rules (hide on auth pages)
- [x] T027 [US5] Validate error handling across all operations

## Phase 8: Polish & Cross-Cutting Concerns

### Goal
Final validation and ensure all requirements are met.

### Independent Test Criteria
- All SP-FULL-INTEGRATION requirements are satisfied
- Implementation is stable and functional
- No integration violations remain
- Production build succeeds with all features working

### Tasks
- [x] T028 Verify all API calls include JWT tokens as required
- [x] T029 Confirm no hardcoded URLs exist in frontend code
- [x] T030 Validate all pages load with proper styling
- [x] T031 Ensure no CORS violations exist in frontend/backend communication
- [x] T032 Perform final validation that integration works end-to-end
- [x] T033 Update documentation to reflect the integration implementation
- [x] T034 Create summary report of the integration process

## Dependencies

- Task T002 must complete before API integration tasks
- Task T007 must complete before authentication flow validation
- All API configuration tasks must complete before task management testing

## Parallel Execution Examples

- Tasks T004, T005, T006, T007 can run in parallel during foundational phase
- Tasks T016, T017, T018, T019 can run in parallel during task management phase
- Tasks T024, T025, T026, T027 can run in parallel during QA phase

## Implementation Strategy

1. **MVP First**: Complete Phase 1-2 to establish proper API configuration
2. **Incremental Delivery**: Complete API integration (Phase 3) as first deliverable
3. **Complete Implementation**: Finish authentication (Phase 4) and task management (Phase 5)
4. **Final Validation**: Complete build validation (Phase 6) and QA (Phase 7)
5. **Polish**: Complete final validation and documentation (Phase 8)