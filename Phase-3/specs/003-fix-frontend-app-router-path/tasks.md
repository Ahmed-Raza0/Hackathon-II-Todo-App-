# Tasks: Frontend App Router Path Resolution

**Input**: Design documents from `/specs/003-fix-frontend-app-router-path/`
**Prerequisites**: plan.md (required), spec.md (required for user stories), research.md, data-model.md, quickstart.md

**Tests**: No tests requested in feature specification
**Organization**: Tasks are grouped by user story to enable independent implementation and testing of each story.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1, US2, US3)
- Include exact file paths in descriptions

## Path Conventions

- **Web app**: `backend/`, `frontend/` at repository root

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Project initialization and basic structure

- [X] T001 Create project structure per implementation plan with frontend/src/app directory
- [X] T002 [P] Verify frontend directory exists with proper structure
- [X] T003 [P] Create src directory in frontend if it doesn't exist

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Core infrastructure that MUST be complete before ANY user story can be implemented

**⚠️ CRITICAL**: No user story work can begin until this phase is complete

- [X] T004 Check if forbidden /frontend/app directory exists
- [X] T005 [P] Remove forbidden /frontend/app directory if it exists (per SP-SRC-05)
- [X] T006 [P] Create canonical /frontend/src/app directory structure
- [X] T007 Verify only canonical structure exists after cleanup

**Checkpoint**: Foundation ready - user story implementation can now begin in parallel

---

## Phase 3: User Story 1 - App Router Resolution (Priority: P1) 🎯 MVP

**Goal**: Ensure the Next.js app has a single canonical App Router path so that routing conflicts and 404 errors are eliminated

**Independent Test**: Can be fully tested by running `npm run dev` and navigating to the root URL, verifying the app renders without 404 errors. This delivers the core value of having a functional, predictable frontend routing system.

### Implementation for User Story 1

- [X] T008 [P] [US1] Create layout.tsx file at frontend/src/app/layout.tsx with proper structure
- [X] T009 [US1] Implement the required root layout component in frontend/src/app/layout.tsx per SP-SRC-07
- [X] T010 [P] [US1] Create page.tsx file at frontend/src/app/page.tsx with home component
- [X] T011 [US1] Implement the required home page component in frontend/src/app/page.tsx per SP-SRC-06
- [X] T012 [P] [US1] Create globals.css file at frontend/src/app/globals.css with required styles
- [X] T013 [US1] Test frontend boot with npm run dev command per SP-SRC-08
- [X] T014 [US1] Validate home page renders without 404 errors at http://localhost:3001/

**Checkpoint**: At this point, User Story 1 should be fully functional and testable independently

---

## Phase 4: User Story 2 - Development Workflow (Priority: P2)

**Goal**: Establish standardized project structure so developers know exactly where to place Next.js App Router files

**Independent Test**: Can be tested by verifying the correct directory structure exists and following the SP-SRC-03 standard. This delivers the value of predictable development patterns.

### Implementation for User Story 2

- [X] T015 [P] [US2] Create lib directory at frontend/src/lib/ for shared utilities
- [X] T016 [US2] Update tsconfig.json to support the new structure at frontend/tsconfig.json
- [X] T017 [US2] Update next.config.js to support the canonical structure at frontend/next.config.js
- [X] T018 [US2] Update tailwind.config.ts to reference the new structure at frontend/tailwind.config.ts
- [X] T019 [US2] Validate that new files can be created in canonical location following standards

**Checkpoint**: At this point, User Stories 1 AND 2 should both work independently

---

## Phase 5: User Story 3 - Deployment Consistency (Priority: P3)

**Goal**: Ensure app router structure is consistent so deployments work predictably without routing errors

**Independent Test**: Can be tested by building the application and verifying the build succeeds without router conflicts. This delivers the value of reliable production deployments.

### Implementation for User Story 3

- [X] T020 [P] [US3] Test production build with npm run build command
- [X] T021 [US3] Validate build completes successfully without router conflicts
- [X] T022 [US3] Verify all routes resolve correctly in production build
- [X] T023 [US3] Confirm no 404 errors occur during production testing

**Checkpoint**: All user stories should now be independently functional

---

## Phase 6: Polish & Cross-Cutting Concerns

**Purpose**: Improvements that affect multiple user stories

- [X] T024 [P] Update documentation to reflect the new canonical structure
- [X] T025 Create/verify README.md with proper setup instructions for canonical structure
- [X] T026 [P] Run quickstart.md validation to ensure deployment works as documented
- [X] T027 Verify all SP-SRC requirements are satisfied
- [X] T028 Confirm no manual patches were used (per SP-SRC-05)

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
- **User Story 2 (P2)**: Can start after Foundational (Phase 2) - Independent of other stories
- **User Story 3 (P3)**: Can start after Foundational (Phase 2) - Depends on User Stories 1 & 2

### Within Each User Story

- Implementation tasks follow the sequence: Structure → Dependencies → Implementation → Validation
- Each story complete before moving to next priority

### Parallel Opportunities

- All Setup tasks marked [P] can run in parallel
- All Foundational tasks marked [P] can run in parallel (within Phase 2)
- Once Foundational phase completes, all user stories can start in parallel (if team capacity allows)
- Different user stories can be worked on in parallel by different team members

---

## Parallel Example: User Story 1

```bash
# Launch all implementation tasks for User Story 1 together:
Task: "Create layout.tsx file at frontend/src/app/layout.tsx with proper structure"
Task: "Create page.tsx file at frontend/src/app/page.tsx with home component"
Task: "Create globals.css file at frontend/src/app/globals.css with required styles"
```

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
5. Each story adds value without breaking previous stories

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
- [Story] label maps task to specific user story for traceability
- Each user story should be independently completable and testable
- Commit after each task or logical group
- Stop at any checkpoint to validate story independently
- Avoid: vague tasks, same file conflicts, cross-story dependencies that break independence