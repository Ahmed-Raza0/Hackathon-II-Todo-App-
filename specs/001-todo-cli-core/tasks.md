# Tasks: Todo CLI Core

**Input**: Design documents from `/specs/001-todo-cli-core/`
**Prerequisites**: plan.md (required), spec.md (required for user stories), research.md, data-model.md, contracts/

**Tests**: Manual testing for Phase I (17 acceptance scenarios from spec.md)

**Organization**: Tasks are grouped by user story to enable independent implementation and testing of each story.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1, US2, US3)
- Include exact file paths in descriptions

## Path Conventions

- **Single project**: `src/`, `tests/` at repository root
- Paths below assume single project structure from plan.md

---

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Project initialization and basic structure

- [ ] T001 Create project directory structure (src/, tests/, specs/, history/)
- [ ] T002 Initialize Python 3.13+ project with UV (pyproject.toml)
- [ ] T003 [P] Create src/__init__.py package initialization file
- [ ] T004 [P] Create tests/__init__.py package initialization file
- [ ] T005 [P] Create tests/manual_test_plan.md with 17 acceptance scenarios from spec

**Checkpoint**: Project structure ready - code implementation can now begin

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Core infrastructure that MUST be complete before ANY user story can be implemented

**⚠️ CRITICAL**: No user story work can begin until this phase is complete

- [ ] T006 Create Task dataclass model in src/task.py with 6 attributes (id, title, description, is_complete, created_at, updated_at)
- [ ] T007 Implement Task.to_display() method in src/task.py for console formatting per Principle 6
- [ ] T008 Create custom exceptions (InvalidTaskError, TaskNotFoundError) in src/task_manager.py
- [ ] T009 Create TaskManager class skeleton in src/task_manager.py with private state (_tasks dict, _next_id counter)

**Checkpoint**: Foundation ready - user story implementation can now begin in parallel

---

## Phase 3: User Story 1 - Add and View Tasks (Priority: P1) 🎯 MVP

**Goal**: Enable users to add tasks with title/description and view all tasks in a formatted list

**Independent Test**: Launch app, add 2-3 tasks with different titles and descriptions, view task list, verify all tasks appear with correct IDs, titles, completion status, timestamps, and descriptions. For empty list, verify "No tasks found" message.

### Implementation for User Story 1

- [ ] T010 [P] [US1] Implement TaskManager.add_task(title, description) in src/task_manager.py with title/description validation (FR-001, FR-010, FR-011, FR-012)
- [ ] T011 [P] [US1] Implement TaskManager.get_all_tasks() in src/task_manager.py to return tasks in insertion order (FR-005, FR-006)
- [ ] T012 [US1] Create CLI class skeleton in src/cli.py with TaskManager instance and display_menu() method (FR-015)
- [ ] T013 [US1] Implement CLI.add_task_flow() in src/cli.py with input prompts and success/error messages (contracts/cli-menu.md)
- [ ] T014 [US1] Implement CLI.view_tasks_flow() in src/cli.py to display tasks or "No tasks found" (contracts/cli-menu.md)
- [ ] T015 [US1] Implement CLI.get_menu_choice() in src/cli.py with input validation (FR-016, contracts/cli-menu.md)

**Checkpoint**: At this point, User Story 1 should be fully functional - users can add tasks and view the list (MVP complete!)

---

## Phase 4: User Story 2 - Mark Tasks Complete (Priority: P2)

**Goal**: Enable users to toggle task completion status by ID

**Independent Test**: Add 3 tasks (using US1), mark task ID 2 as complete, view list to verify [X] checkbox, mark task ID 2 as incomplete, view list to verify [ ] checkbox. Test with non-existent task ID (999) to verify error handling.

### Implementation for User Story 2

- [ ] T016 [US2] Implement TaskManager.toggle_complete(task_id) in src/task_manager.py with ID validation and status toggle (FR-007, FR-013)
- [ ] T017 [US2] Implement CLI.mark_complete_flow() in src/cli.py with ID prompt, confirmation messages, and error handling (contracts/cli-menu.md)

**Checkpoint**: At this point, User Stories 1 AND 2 should both work independently

---

## Phase 5: User Story 3 - Update Task Details (Priority: P3)

**Goal**: Enable users to modify task title and/or description by ID

**Independent Test**: Add a task "Cal dentist" (typo), update it to "Call dentist" and add description "Schedule annual checkup", view list to verify changes. Test with non-existent task ID (5) and empty title to verify error handling.

### Implementation for User Story 3

- [ ] T018 [US3] Implement TaskManager.update_task(task_id, title, description) in src/task_manager.py with validation and timestamp update (FR-008, FR-004, FR-010, FR-011, FR-012, FR-013)
- [ ] T019 [US3] Implement CLI.update_task_flow() in src/cli.py with ID/title/description prompts and "No changes provided" handling (contracts/cli-menu.md)

**Checkpoint**: At this point, User Stories 1, 2, AND 3 should all work independently

---

## Phase 6: User Story 4 - Delete Unwanted Tasks (Priority: P4)

**Goal**: Enable users to permanently remove tasks by ID with confirmation

**Independent Test**: Add 3 tasks, delete task ID 2 (confirm with 'y'), view list to verify only tasks 1 and 3 remain. Try deleting task ID 2 again to verify error handling. Test cancellation by entering 'n' at confirmation prompt.

### Implementation for User Story 4

- [ ] T020 [US4] Implement TaskManager.delete_task(task_id) in src/task_manager.py with ID validation (FR-009, FR-013)
- [ ] T021 [US4] Implement CLI.delete_task_flow() in src/cli.py with ID prompt, confirmation dialog (y/n), and cancellation handling (contracts/cli-menu.md)

**Checkpoint**: At this point, User Stories 1, 2, 3, AND 4 should all work independently

---

## Phase 7: User Story 5 - Navigate and Exit Safely (Priority: P5)

**Goal**: Provide clear menu navigation and graceful exit (option 6 or Ctrl+C)

**Independent Test**: Launch app, try each menu option (1-6), enter invalid choices (7, "abc"), verify error messages and menu re-display. Select option 6, verify "Goodbye!" message and clean exit. Press Ctrl+C, verify clean exit without stack trace.

### Implementation for User Story 5

- [ ] T022 [P] [US5] Implement CLI.run() main loop in src/cli.py with menu display and choice dispatching (contracts/cli-menu.md)
- [ ] T023 [P] [US5] Implement CLI.exit_application() in src/cli.py to display "Goodbye!" and call sys.exit(0) (FR-018, contracts/cli-menu.md)
- [ ] T024 [US5] Create src/main.py entry point with KeyboardInterrupt handling for graceful Ctrl+C exit (FR-018, research.md decision #4)
- [ ] T025 [US5] Add if __name__ == "__main__" guard to src/main.py to call main() function

**Checkpoint**: All user stories should now be independently functional - full application complete!

---

## Phase 8: Polish & Cross-Cutting Concerns

**Purpose**: Improvements that affect multiple user stories and final validation

- [ ] T026 [P] Add type hints throughout all modules (task.py, task_manager.py, cli.py, main.py) per PEP 484
- [ ] T027 [P] Add docstrings to all public functions and classes per PEP 257
- [ ] T028 [P] Verify error handling completeness across all CLI flows (catch InvalidTaskError, TaskNotFoundError, ValueError)
- [ ] T029 Run manual test plan (tests/manual_test_plan.md) with all 17 acceptance scenarios
- [ ] T030 Test all 9 edge cases from spec.md (title limits, description limits, invalid IDs, etc.)
- [ ] T031 Validate 60-second demo workflow from quickstart.md
- [ ] T032 Code review for PEP 8 compliance (line length, naming, imports)
- [ ] T033 Verify constitution Principle 6 UX format (menu display, task display)

**Final Checkpoint**: Application is demo-ready!

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies - can start immediately
- **Foundational (Phase 2)**: Depends on Setup completion - BLOCKS all user stories
- **User Stories (Phase 3-7)**: All depend on Foundational phase completion
  - User stories can then proceed in parallel (if staffed)
  - Or sequentially in priority order (P1 → P2 → P3 → P4 → P5)
- **Polish (Phase 8)**: Depends on all user stories being complete

### User Story Dependencies

- **User Story 1 (P1)**: Can start after Foundational (Phase 2) - No dependencies on other stories
- **User Story 2 (P2)**: Can start after Foundational (Phase 2) - Uses tasks from US1 for testing but independently testable
- **User Story 3 (P3)**: Can start after Foundational (Phase 2) - Uses tasks from US1 for testing but independently testable
- **User Story 4 (P4)**: Can start after Foundational (Phase 2) - Uses tasks from US1 for testing but independently testable
- **User Story 5 (P5)**: Can start after Foundational (Phase 2) - Integrates all US1-4 flows but independently testable

### Within Each User Story

- Tasks within a story should be completed in order (T010 → T011 → T012 → ...)
- Tasks marked [P] can run in parallel if team capacity allows
- Core implementation before integration
- Story complete before moving to next priority

### Parallel Opportunities

- All Setup tasks (T001-T005) can run in parallel
- Foundation tasks T006-T007 can run in parallel (Task model implementation)
- Foundation tasks T008-T009 can run in parallel (TaskManager skeleton)
- Once Foundational phase completes, User Stories 1-5 can ALL start in parallel (if team capacity allows)
- Within each user story, tasks marked [P] can run in parallel
- Polish phase tasks T026-T028 can run in parallel

---

## Parallel Example: After Foundation Complete

```bash
# Different team members can work on different user stories simultaneously:
Developer A: User Story 1 (T010-T015) → MVP ready
Developer B: User Story 2 (T016-T017) → Mark complete feature ready
Developer C: User Story 3 (T018-T019) → Update feature ready
Developer D: User Story 4 (T020-T021) → Delete feature ready
Developer E: User Story 5 (T022-T025) → Menu and exit ready

# All stories integrate cleanly because they share foundation (Task, TaskManager)
```

---

## Implementation Strategy

### MVP First (User Story 1 Only)

1. Complete Phase 1: Setup (T001-T005)
2. Complete Phase 2: Foundational (T006-T009) - CRITICAL, blocks all stories
3. Complete Phase 3: User Story 1 (T010-T015)
4. **STOP and VALIDATE**: Test User Story 1 independently
   - Launch app, add 2-3 tasks, view list
   - Verify task display format matches Principle 6
   - Test empty list shows "No tasks found"
5. If MVP validates → Deploy/demo or continue to next story

### Incremental Delivery

1. Foundation ready → Add User Story 1 → Test independently → **MVP deployed!**
2. Add User Story 2 → Test independently → Mark complete feature live
3. Add User Story 3 → Test independently → Update feature live
4. Add User Story 4 → Test independently → Delete feature live
5. Add User Story 5 → Test independently → Full navigation live
6. Polish phase → Production-ready

Each story adds value without breaking previous stories!

### Parallel Team Strategy

With 5 developers after Foundational phase:
1. Team completes Setup + Foundational together (T001-T009)
2. Once Foundational is done, split into parallel tracks:
   - **Dev A**: User Story 1 (P1) - MVP priority
   - **Dev B**: User Story 2 (P2) - Depends on US1 for testing only
   - **Dev C**: User Story 3 (P3) - Depends on US1 for testing only
   - **Dev D**: User Story 4 (P4) - Depends on US1 for testing only
   - **Dev E**: User Story 5 (P5) - Integrates all flows
3. Stories complete and merge independently
4. Polish phase runs across all stories

---

## Task Execution Checklist

Before executing tasks:
- [ ] Setup complete (T001-T005)
- [ ] Foundational complete (T006-T009)
- [ ] At least User Story 1 complete for MVP

During execution:
- [ ] Mark tasks complete after finishing each one
- [ ] Commit after each task or logical group
- [ ] Test at each checkpoint
- [ ] Stop at any checkpoint to validate story independently

After execution:
- [ ] All 33 tasks complete
- [ ] All 17 acceptance scenarios pass
- [ ] All 9 edge cases handled
- [ ] 60-second demo workflow validates
- [ ] Code passes PEP 8/257 checks

---

## Notes

- [P] tasks = different files, no dependencies
- [Story] label maps task to specific user story for traceability
- Each user story should be independently completable and testable
- Commit after each task or logical group
- Stop at any checkpoint to validate story independently
- **Tests**: Manual testing for Phase I (automated tests not required per plan.md)
- **File paths**: All paths relative to repository root
- Avoid: vague tasks, same file conflicts, cross-story dependencies that break independence
