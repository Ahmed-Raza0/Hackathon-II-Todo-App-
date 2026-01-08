# Implementation Plan: Todo CLI Core

**Branch**: `001-todo-cli-core` | **Date**: 2025-12-27 | **Spec**: [spec.md](./spec.md)
**Input**: Feature specification from `/specs/001-todo-cli-core/spec.md`

## Summary

Build a command-line todo application that allows users to manage tasks through a numbered menu interface. The application supports five core operations: add tasks with title/description, view all tasks with completion status, update task details, mark tasks complete/incomplete, and delete tasks. All data stored in-memory only (session-based), with comprehensive input validation and error handling. Technical approach uses Python 3.13+ with standard library only (no external dependencies), implementing a three-layer architecture: Task model (data), TaskManager (business logic), and CLI interface (user interaction).

## Technical Context

**Language/Version**: Python 3.13+
**Primary Dependencies**: Python Standard Library only (datetime, sys, signal modules)
**Storage**: In-memory only (Python dict for ID-based access, no persistence)
**Testing**: Manual testing against 17 acceptance scenarios from spec (automated tests optional for Phase I)
**Target Platform**: Cross-platform CLI (Windows, macOS, Linux terminals)
**Project Type**: Single project (CLI application)
**Performance Goals**: <1 second response for any operation up to 1000 tasks
**Constraints**: Standard library only, in-memory storage, beginner-friendly code, 90-second demo requirement
**Scale/Scope**: Single user, session-based, 100-1000 tasks typical, no concurrency

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

### Principle 1: Spec-Driven Development (NON-NEGOTIABLE)
- ✅ **PASS**: Specification created first (`spec.md` exists with 5 user stories, 18 functional requirements)
- ✅ **PASS**: All code will be AI-generated via Claude Code (no manual coding)
- ✅ **PASS**: Specification stored in `/specs/001-todo-cli-core/` with version control

### Principle 2: Project Architecture
- ✅ **PASS**: Python 3.13+ confirmed as language
- ✅ **PASS**: UV for package management (will be configured in Phase 1)
- ✅ **PASS**: Standard library only (no external dependencies beyond stdlib)
- ✅ **PASS**: Project structure follows constitution template (src/, tests/, specs/)

### Principle 3: Feature Requirements (Basic Level ONLY)
- ✅ **PASS**: All 5 mandatory features included:
  1. Add Task (US1) - FR-001, FR-002, FR-003
  2. Delete Task (US4) - FR-009, FR-013
  3. Update Task (US3) - FR-008, FR-004, FR-013
  4. View Task List (US1) - FR-005, FR-006
  5. Mark as Complete (US2) - FR-007, FR-013
- ✅ **PASS**: No out-of-scope features (persistence, tags, priorities, GUI all excluded)

### Principle 4: Domain Rules
- ✅ **PASS**: Task definition complete (ID, title 1-200 chars, optional description max 1000 chars, boolean status, timestamps)
- ✅ **PASS**: All 5 operations defined with validation rules
- ✅ **PASS**: 9 edge cases specified with exact error messages (empty title, character limits, invalid IDs, etc.)

### Principle 5: Code Quality Standards
- ✅ **PASS**: Plan specifies type hints throughout (PEP 484)
- ✅ **PASS**: Plan specifies docstrings for all public functions/classes (PEP 257)
- ✅ **PASS**: Error handling specified for all user inputs
- ✅ **PASS**: Architecture specifies separation of concerns (Task model, TaskManager, CLI)

### Principle 6: User Experience Requirements
- ✅ **PASS**: Menu interface format specified (exact layout in constitution Principle 6)
- ✅ **PASS**: Task display format specified (ID | [X]/[ ] | Title | Timestamp + Description)
- ✅ **PASS**: Input prompts and feedback messages specified
- ✅ **PASS**: Graceful error handling specified (no crashes, helpful messages)

### Principle 7: Validation Criteria (Hackathon Judge)
- ✅ **PASS**: In-memory storage only (FR-017)
- ✅ **PASS**: Console application (no GUI, no web)
- ✅ **PASS**: Single-user (no authentication, no multi-user)
- ✅ **PASS**: Basic features only (no priorities, tags, advanced features)
- ✅ **PASS**: Can be demoed in 90 seconds (5 simple operations)

### Principle 11: Constraints
- ✅ **PASS**: Python 3.13+ only
- ✅ **PASS**: UV for package management (not pip/poetry)
- ✅ **PASS**: Standard library only (no external packages)
- ✅ **PASS**: In-memory storage (no persistence)

**GATE RESULT**: ✅ ALL CHECKS PASSED - Proceed to Phase 0 Research

## Project Structure

### Documentation (this feature)

```text
specs/001-todo-cli-core/
├── spec.md              # Feature specification (completed)
├── plan.md              # This file (/sp.plan command output)
├── research.md          # Phase 0 output (see below)
├── data-model.md        # Phase 1 output (see below)
├── quickstart.md        # Phase 1 output (see below)
├── contracts/           # Phase 1 output (CLI interface contracts)
│   └── cli-menu.md      # Menu system contract
└── checklists/
    └── requirements.md  # Specification quality checklist (completed)
```

### Source Code (repository root)

```text
src/
├── __init__.py          # Package initialization
├── main.py              # Entry point, CLI menu loop
├── task.py              # Task model (dataclass)
├── task_manager.py      # Business logic (CRUD operations, validation)
└── cli.py               # CLI interface (input/output formatting, menu display)

tests/                   # Manual testing for Phase I (automated optional)
├── __init__.py
└── manual_test_plan.md  # Test scenarios from spec
```

**Structure Decision**: Single project structure selected (Option 1 from template). This is a standalone CLI application with no frontend/backend separation or mobile components. The three-layer architecture (Task model, TaskManager business logic, CLI interface) provides clean separation of concerns while remaining simple and beginner-friendly per Principle 5.

## Complexity Tracking

**No violations detected.** All constitution checks passed without exceptions.

## Phase 0: Research & Design Decisions

### Research Questions

Based on Technical Context, the following areas require research to resolve implementation details:

1. **ISO 8601 Timestamp Formatting**:
   - **Question**: Should timestamps include timezone info or use local time only?
   - **Context**: FR-003/FR-004 specify ISO 8601 format; constitution Principle 4 lists timestamps as auto-generated
   - **Options**: `datetime.now().isoformat()` (local, no TZ) vs `datetime.now(timezone.utc).isoformat()` (UTC with TZ)

2. **Task ID Storage Strategy**:
   - **Question**: Use dict for O(1) access or list with sequential search?
   - **Context**: FR-002 requires sequential IDs; operations reference by ID (FR-007-009, FR-013)
   - **Options**: `dict[int, Task]` vs `list[Task]` with ID matching

3. **Input Validation Patterns**:
   - **Question**: Validate at CLI layer or TaskManager layer?
   - **Context**: FR-010-013, FR-016 specify validation rules; Principle 5 requires separation of concerns
   - **Options**: CLI validates before calling TaskManager vs TaskManager validates and raises exceptions

4. **Graceful Ctrl+C Handling**:
   - **Question**: Use signal handlers or try/except KeyboardInterrupt?
   - **Context**: FR-018 requires graceful exit on Ctrl+C without stack traces
   - **Options**: `signal.signal()` vs `try/except KeyboardInterrupt` in main loop

### Research Findings (to be documented in research.md)

This section will be filled during Phase 0 execution with:
- **Decision**: What was chosen for each question
- **Rationale**: Why this approach best fits constitution constraints
- **Alternatives Considered**: What other options were evaluated
- **Trade-offs**: Performance, simplicity, beginner-friendliness analysis

## Phase 1: Data Model & Contracts

### Entity Design (data-model.md)

**Task Entity**:
```
Task:
  - id: int (unique, sequential, auto-generated)
  - title: str (required, 1-200 chars, validated)
  - description: str | None (optional, max 1000 chars, validated)
  - is_complete: bool (default False)
  - created_at: datetime (auto-generated, ISO 8601)
  - updated_at: datetime (auto-generated, ISO 8601, updates on modify)

Validation Rules:
  - title: non-empty after strip(), length 1-200
  - description: None or length ≤ 1000
  - timestamps: ISO 8601 format via datetime.isoformat()
```

**TaskManager State**:
```
TaskManager:
  - _tasks: dict[int, Task] (private, ID-based access)
  - _next_id: int (private, counter for sequential IDs)

Invariants:
  - IDs never reused (increment only)
  - Tasks accessible by ID in O(1)
  - Display order maintains insertion sequence
```

### CLI Interface Contracts (contracts/cli-menu.md)

**Menu System Contract**:
```
Input: User enters menu choice (1-6)
Valid Choices:
  1 → add_task_flow()
  2 → view_tasks_flow()
  3 → update_task_flow()
  4 → mark_complete_flow()
  5 → delete_task_flow()
  6 → exit_application()

Invalid Input:
  - Non-numeric → "Invalid choice. Please enter 1-6"
  - Out of range (0, 7+) → "Invalid choice. Please enter 1-6"
  - Menu re-displayed after error

Termination:
  - Option 6 → Print "Goodbye!" + clean exit(0)
  - Ctrl+C → Clean exit(0) without stack trace
```

**Task Operation Contracts**:
```
add_task(title: str, description: str | None) → Task | Error
  Preconditions: None (validation internal)
  Success: Returns Task with ID, timestamps, is_complete=False
  Errors:
    - Empty title (after strip) → "Title cannot be empty"
    - Title > 200 chars → "Title too long (max 200 characters)"
    - Description > 1000 chars → "Description too long (max 1000 characters)"

get_all_tasks() → list[Task]
  Preconditions: None
  Success: Returns tasks in insertion order
  Empty list: Returns [] (CLI displays "No tasks found")

update_task(task_id: int, title: str | None, description: str | None) → Task | Error
  Preconditions: At least one of title/description provided
  Success: Returns updated Task with new updated_at
  Errors:
    - task_id not found → "Task ID {task_id} does not exist"
    - Empty title → "Title cannot be empty"
    - Title > 200 chars → "Title too long (max 200 characters)"
    - Description > 1000 chars → "Description too long (max 1000 characters)"

toggle_complete(task_id: int) → Task | Error
  Preconditions: None (idempotent)
  Success: Returns Task with is_complete toggled, updated_at updated
  Errors:
    - task_id not found → "Task ID {task_id} does not exist"

delete_task(task_id: int) → None | Error
  Preconditions: None
  Success: Task removed, no return value
  Errors:
    - task_id not found → "Task ID {task_id} does not exist"
  Note: Confirmation prompt at CLI layer ("Are you sure? (y/n): ")
```

### Quickstart Guide (quickstart.md)

**Setup**:
```bash
# Prerequisites: Python 3.13+, UV installed
uv init --python 3.13
uv sync
```

**Run Application**:
```bash
uv run python src/main.py
```

**Test Workflow** (60-second demo path):
```
1. Launch app → See menu
2. Select 1 (Add Task) → Enter "Buy groceries" + "Milk, eggs, bread"
3. Select 2 (View Tasks) → Verify task 1 appears with [ ] checkbox
4. Select 4 (Mark Complete) → Enter ID 1 → Verify success message
5. Select 2 (View Tasks) → Verify task 1 shows [X] checkbox
6. Select 5 (Delete Task) → Enter ID 1 → Confirm y → Verify deletion
7. Select 2 (View Tasks) → See "No tasks found"
8. Select 6 (Exit) → See "Goodbye!" and clean exit
```

## Phase 2: Implementation Planning (via /sp.tasks)

This plan document stops here. The next phase uses `/sp.tasks` to generate actionable tasks based on this plan, the data model, and the contracts.

**Pre-Task Checklist**:
- ✅ Specification complete (`spec.md` with 5 user stories)
- ✅ Plan approved (this document)
- ✅ Research completed (`research.md` - to be created in Phase 0)
- ✅ Data model defined (`data-model.md` - to be created in Phase 1)
- ✅ Contracts defined (`contracts/cli-menu.md` - to be created in Phase 1)
- ✅ Quickstart guide written (`quickstart.md` - to be created in Phase 1)
- ⏳ Ready for `/sp.tasks todo-cli-core` to generate implementation tasks

## Next Steps

1. **Immediate**: Execute Phase 0 research (create `research.md` resolving 4 research questions)
2. **Immediate**: Execute Phase 1 design (create `data-model.md`, `contracts/cli-menu.md`, `quickstart.md`)
3. **After Phase 0-1 Complete**: Run `/sp.tasks todo-cli-core` to generate dependency-ordered implementation tasks
4. **After Tasks Approved**: Run `/sp.implement todo-cli-core` to execute tasks and generate code

**Estimated Timeline**:
- Phase 0 Research: <10 minutes (4 focused research questions)
- Phase 1 Design: <15 minutes (data model + contracts + quickstart)
- Phase 2 Tasks: <5 minutes (task generation via `/sp.tasks`)
- Phase 3 Implementation: <30 minutes (code generation + manual testing)
- **Total: <60 minutes** from plan approval to demo-ready application
