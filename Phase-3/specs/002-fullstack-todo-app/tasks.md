---
description: "Task list template for feature implementation"
---

# Tasks: Full-Stack Todo Application

**Input**: Design documents from `/specs/002-fullstack-todo-app/`
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

- [ ] T001 Create project structure per implementation plan
- [ ] T002 Initialize Python backend project with FastAPI dependencies
- [ ] T003 [P] Configure linting and formatting tools for Python (black, flake8, mypy)
- [ ] T004 [P] Initialize Next.js frontend project with React 19+ dependencies
- [ ] T005 [P] Configure linting and formatting tools for JavaScript/TypeScript (ESLint, Prettier)

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Core infrastructure that MUST be complete before ANY user story can be implemented

**⚠️ CRITICAL**: No user story work can begin until this phase is complete

**Foundation tasks based on research and data model:**

- [X] T006 Setup database schema and SQLModel framework in backend
- [X] T007 [P] Configure environment variables management with python-dotenv
- [ ] T008 [P] Setup Better Auth for user authentication in both frontend and backend
- [X] T009 Create base Task model in backend/src/models/task.py (depends on T006)
- [X] T010 Setup JWT authentication middleware in backend/src/middleware/auth_middleware.py
- [X] T011 Create API base structure with proper error handling in backend/src/api/
- [X] T012 Setup database connection in backend/database.py
- [X] T013 Configure Neon PostgreSQL connection in backend/.env

**Checkpoint**: Foundation ready - user story implementation can now begin in parallel

---

## Phase 3: User Story 1 - Basic Task Management (Priority: P1) 🎯 MVP

**Goal**: Enable users to create, view, update, and delete their personal tasks through a web interface

**Independent Test**: Can be fully tested by creating tasks, viewing them in a list, updating their details, and deleting them. The system should persist these changes and allow users to manage their tasks effectively.

### Implementation for User Story 1

- [X] T014 [P] [US1] Create Task model with validation in backend/src/models/task.py (depends on T009)
- [X] T015 [P] [US1] Create TaskService in backend/src/services/task_service.py for CRUD operations
- [X] T016 [US1] Implement GET /api/{user_id}/tasks endpoint in backend/src/routes/tasks.py (depends on T014, T015)
- [X] T017 [US1] Implement POST /api/{user_id}/tasks endpoint in backend/src/routes/tasks.py (depends on T014, T015)
- [X] T018 [US1] Implement GET /api/{user_id}/tasks/{id} endpoint in backend/src/routes/tasks.py (depends on T014, T015)
- [X] T019 [US1] Implement PUT /api/{user_id}/tasks/{id} endpoint in backend/src/routes/tasks.py (depends on T014, T015)
- [X] T020 [US1] Implement DELETE /api/{user_id}/tasks/{id} endpoint in backend/src/routes/tasks.py (depends on T014, T015)
- [X] T021 [US1] Add validation and error handling to task endpoints (depends on T016-T020)
- [X] T022 [US1] Create API client in frontend/src/lib/api.ts with JWT handling (depends on T008)
- [X] T023 [US1] Create TaskService in frontend/src/services/taskService.ts (depends on T022)
- [X] T024 [US1] Create reusable UI components for tasks in frontend/src/components/ui/
- [X] T025 [US1] Create task management components in frontend/src/components/tasks/ (depends on T024)
- [X] T026 [US1] Implement /app/tasks/page.tsx with task list and CRUD functionality (depends on T023, T025)
- [X] T027 [US1] Add styling for task management page with Tailwind CSS (depends on T026)

**Checkpoint**: At this point, User Story 1 should be fully functional and testable independently

---

## Phase 4: User Story 2 - User Authentication & Security (Priority: P1)

**Goal**: Securely sign up, log in, and isolate user tasks from other users

**Independent Test**: Can be fully tested by creating multiple user accounts, verifying that each user can only see their own tasks and not others'.

### Implementation for User Story 2

- [ ] T028 [P] [US2] Create User model in backend/src/models/user.py (managed by Better Auth)
- [ ] T029 [P] [US2] Create UserService in backend/src/services/auth.py for authentication logic
- [ ] T030 [US2] Implement authentication endpoints in backend/src/routes/auth.py (depends on T029)
- [ ] T031 [US2] Enhance JWT middleware to validate user_id against URL parameter (depends on T010)
- [ ] T032 [US2] Update task endpoints to enforce user_id filtering (depends on T016-T020, T031)
- [ ] T033 [US2] Create authentication components in frontend/src/components/auth/ (depends on T008)
- [ ] T034 [US2] Create authentication context in frontend/src/providers/AuthProvider.tsx (depends on T008)
- [ ] T035 [US2] Create login and signup pages in frontend/app/login/page.tsx and frontend/app/signup/page.tsx (depends on T033)
- [ ] T036 [US2] Update task API calls to ensure JWT token is included (depends on T022)
- [ ] T037 [US2] Add authentication guards to protect task routes (depends on T034)

**Checkpoint**: At this point, User Stories 1 AND 2 should both work independently

---

## Phase 5: User Story 3 - Advanced Task Features (Priority: P2)

**Goal**: Allow users to mark tasks as complete/incomplete and filter tasks by status

**Independent Test**: Can be fully tested by creating tasks, marking them as complete/incomplete, and filtering the task list by status.

### Implementation for User Story 3

- [ ] T038 [P] [US3] Update Task model to include completion status validation (depends on T014)
- [ ] T039 [US3] Implement PATCH /api/{user_id}/tasks/{id}/complete endpoint in backend/src/routes/tasks.py (depends on T038)
- [ ] T040 [US3] Add filtering and sorting capabilities to GET /api/{user_id}/tasks endpoint (depends on T016)
- [ ] T041 [US3] Update TaskService to support completion toggling (depends on T015, T039)
- [ ] T042 [US3] Update frontend task components to support completion toggling (depends on T025)
- [ ] T043 [US3] Add filtering UI to task management page (depends on T026, T042)
- [ ] T044 [US3] Add sorting UI to task management page (depends on T026, T042)

**Checkpoint**: At this point, User Stories 1, 2, and 3 should all work independently

---

## Phase 6: User Story 4 - AI-Powered Chat Assistant (Priority: P3)

**Goal**: Interact with an AI assistant that can help manage tasks through natural language

**Independent Test**: Can be fully tested by sending natural language commands to the AI assistant and verifying that appropriate task operations are performed.

### Implementation for User Story 4

- [X] T045 [P] [US4] Create Conversation model in backend/src/models/conversation.py
- [X] T046 [P] [US4] Create Message model in backend/src/models/message.py
- [X] T047 [P] [US4] Setup MCP server configuration
- [X] T048 [US4] Implement MCP tools: add_task, list_tasks, complete_task, update_task, delete_task (depends on T015)
- [X] T049 [US4] Implement chat endpoint POST /api/{user_id}/chat in backend/src/routes/chat.py (depends on T045, T046, T048)
- [X] T050 [US4] Create chat service in backend/src/services/chat_service.py (depends on T049)
- [X] T051 [US4] Create chat API client in frontend/src/services/chatService.ts (depends on T022)
- [X] T052 [US4] Create chat UI components in frontend/src/components/chat/ (depends on T024)
- [X] T053 [US4] Implement chat interface in frontend/app/chat/page.tsx (depends on T051, T052)
- [X] T054 [US4] Add navigation to chat page in frontend layout (depends on T053)

**Checkpoint**: All user stories should now be independently functional

---

## Phase N: Polish & Cross-Cutting Concerns

**Purpose**: Improvements that affect multiple user stories

- [ ] T055 [P] Documentation updates in docs/
- [ ] T056 Code cleanup and refactoring across frontend and backend
- [ ] T057 Performance optimization across all stories
- [ ] T058 [P] Add comprehensive error handling and logging
- [ ] T059 Security hardening and validation
- [ ] T060 Run quickstart.md validation to ensure setup instructions work

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies - can start immediately
- **Foundational (Phase 2)**: Depends on Setup completion - BLOCKS all user stories
- **User Stories (Phase 3+)**: All depend on Foundational phase completion
  - User stories can then proceed in parallel (if staffed)
  - Or sequentially in priority order (P1 → P2 → P3)
- **Polish (Final Phase)**: Depends on all desired user stories being complete

### User Story Dependencies

- **User Story 1 (P1)**: Can start after Foundational (Phase 2) - No dependencies on other stories
- **User Story 2 (P1)**: Can start after Foundational (Phase 2) - May integrate with US1 but should be independently testable
- **User Story 3 (P2)**: Can start after Foundational (Phase 2) - Integrates with US1/US2 but should be independently testable
- **User Story 4 (P3)**: Can start after Foundational (Phase 2) - Integrates with US1/US2 but should be independently testable

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
3. Complete Phase 3: User Story 1
4. **STOP and VALIDATE**: Test User Story 1 independently
5. Deploy/demo if ready

### Incremental Delivery

1. Complete Setup + Foundational → Foundation ready
2. Add User Story 1 → Test independently → Deploy/Demo (MVP!)
3. Add User Story 2 → Test independently → Deploy/Demo
4. Add User Story 3 → Test independently → Deploy/Demo
5. Add User Story 4 → Test independently → Deploy/Demo
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