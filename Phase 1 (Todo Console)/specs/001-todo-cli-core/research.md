# Research & Design Decisions: Todo CLI Core

**Feature**: Todo CLI Core
**Branch**: 001-todo-cli-core
**Date**: 2025-12-27
**Status**: Completed

## Overview

This document resolves technical implementation questions identified during planning. All decisions prioritize simplicity, beginner-friendliness, and compliance with Phase I constitution constraints (Python 3.13+ standard library only, in-memory storage, clean code).

## Research Questions & Resolutions

### 1. ISO 8601 Timestamp Formatting

**Question**: Should timestamps include timezone info or use local time only?

**Context**:
- FR-003/FR-004 specify ISO 8601 format for created_at/updated_at timestamps
- Constitution Principle 8 lists "Locale: Timestamps use system locale; no internationalization required for Phase I"
- Spec Assumption 8: "Timestamps use system locale"

**Options Evaluated**:
1. **Local time without timezone**: `datetime.now().isoformat()` → `"2025-12-27T10:30:45.123456"`
2. **UTC with timezone**: `datetime.now(timezone.utc).isoformat()` → `"2025-12-27T15:30:45.123456+00:00"`

**Decision**: Use **local time without timezone** (`datetime.now().isoformat()`)

**Rationale**:
- **Simplicity**: Beginner-friendly, no timezone concepts to explain
- **Constitution compliance**: Matches Principle 8 assumption ("system locale")
- **Phase I scope**: Single-user, session-based, no persistence - timezone irrelevant
- **Display clarity**: Local time matches user's clock, reducing confusion
- **ISO 8601 compliance**: Format is valid ISO 8601 (timezone optional per spec)

**Alternatives Considered**:
- UTC with timezone: Rejected - adds complexity without benefit for Phase I single-user scenario
- String formatting (`strftime`): Rejected - `.isoformat()` is more Pythonic and automatically ISO 8601 compliant

**Trade-offs**:
- ✅ Simpler code, beginner-friendly
- ✅ Matches user expectations (local time)
- ❌ Not portable across timezones (acceptable for Phase I - no persistence, single session)

**Implementation**:
```python
from datetime import datetime

# In Task creation
created_at = datetime.now()
display_time = created_at.isoformat()  # "2025-12-27T10:30:45.123456"
```

---

### 2. Task ID Storage Strategy

**Question**: Use dict for O(1) access or list with sequential search?

**Context**:
- FR-002 requires sequential integer IDs starting from 1
- Operations (FR-007-009, FR-013) reference tasks by ID
- Spec Success Criterion SC-004: "Application handles 1000 tasks without performance degradation (under 1 second)"

**Options Evaluated**:
1. **Dictionary (dict[int, Task])**: O(1) lookup, no ordering guarantee
2. **List (list[Task])**: O(n) lookup, maintains insertion order

**Decision**: Use **dict[int, Task]** for storage + track insertion order separately

**Rationale**:
- **Performance**: O(1) lookup ensures SC-004 compliance (1000 tasks, <1 second operations)
- **Simplicity**: ID-based access is natural with dict (`tasks[id]` vs `next(t for t in tasks if t.id == id)`)
- **Scalability**: Handles 1000+ tasks efficiently
- **Python 3.7+**: Dicts maintain insertion order (guaranteed in Python 3.13+)

**Alternatives Considered**:
- List with linear search: Rejected - O(n) lookup degrades performance at scale (SC-004 violation at 1000 tasks)
- OrderedDict: Rejected - unnecessary in Python 3.7+, regular dict maintains order
- Both dict + list: Rejected - over-engineering, dict insertion order sufficient

**Trade-offs**:
- ✅ O(1) lookup performance
- ✅ Simple ID-based access
- ✅ Maintains insertion order (Python 3.13+ guaranteed)
- ❌ Slightly more memory than list (acceptable - 1000 tasks is ~100KB)

**Implementation**:
```python
class TaskManager:
    def __init__(self):
        self._tasks: dict[int, Task] = {}  # ID → Task mapping
        self._next_id: int = 1  # Sequential ID counter

    def get_all_tasks(self) -> list[Task]:
        return list(self._tasks.values())  # Maintains insertion order in Python 3.13+
```

---

### 3. Input Validation Patterns

**Question**: Validate at CLI layer or TaskManager layer?

**Context**:
- FR-010-013, FR-016 specify validation rules (title length, empty checks, ID validation)
- Constitution Principle 5: Separation of concerns (Task model, TaskManager, CLI)
- Beginner-friendliness: Clear error handling without confusing stack traces

**Options Evaluated**:
1. **CLI validates before calling TaskManager**: Input sanitization at UI boundary
2. **TaskManager validates and raises exceptions**: Business logic owns validation
3. **Both layers validate**: CLI for UX, TaskManager for integrity

**Decision**: **TaskManager validates and raises custom exceptions**, CLI catches and displays user-friendly messages

**Rationale**:
- **Separation of concerns**: Business logic owns data integrity (TaskManager), UI owns presentation (CLI)
- **Reusability**: TaskManager can be used by other interfaces (future phases: GUI, web) without duplicating validation
- **Simplicity**: Single source of truth for validation rules
- **Error clarity**: Custom exceptions (e.g., `InvalidTaskError`) provide meaningful messages
- **Testability**: Business logic validation can be unit tested independently

**Alternatives Considered**:
- CLI-only validation: Rejected - violates separation of concerns, duplicates logic if interfaces expand
- No validation (Python raises built-in errors): Rejected - stack traces confuse users (FR-018, SC-005)

**Trade-offs**:
- ✅ Single source of truth (DRY principle)
- ✅ Clear separation of concerns
- ✅ Testable business logic
- ❌ Requires exception handling in CLI (acceptable - clean try/except pattern)

**Implementation**:
```python
# task_manager.py
class InvalidTaskError(Exception):
    """Raised when task validation fails"""
    pass

class TaskManager:
    def add_task(self, title: str, description: str | None = None) -> Task:
        # Validation in TaskManager
        title = title.strip()
        if not title:
            raise InvalidTaskError("Title cannot be empty")
        if len(title) > 200:
            raise InvalidTaskError("Title too long (max 200 characters)")
        # ... create task

# cli.py
def add_task_flow(self):
    title = input("Enter task title: ")
    description = input("Enter description (optional): ")
    try:
        task = self.manager.add_task(title, description or None)
        print(f"✓ Task added successfully! (ID: {task.id})")
    except InvalidTaskError as e:
        print(f"✗ Error: {e}")
```

---

### 4. Graceful Ctrl+C Handling

**Question**: Use signal handlers or try/except KeyboardInterrupt?

**Context**:
- FR-018 requires graceful exit on Ctrl+C without stack traces
- Constitution Principle 5: Beginner-friendly code
- Cross-platform requirement (Windows, macOS, Linux)

**Options Evaluated**:
1. **Signal handler**: `signal.signal(signal.SIGINT, handler)` with custom handler
2. **try/except KeyboardInterrupt**: Wrap main loop in exception handler
3. **Both**: Signal handler + exception handling

**Decision**: Use **try/except KeyboardInterrupt** in main loop

**Rationale**:
- **Simplicity**: More beginner-friendly than signal module
- **Readability**: Exception handling is familiar Python pattern
- **Cross-platform**: Works identically on Windows/macOS/Linux (signal behavior varies)
- **Constitution alignment**: Principle 5 emphasizes beginner-friendly code
- **Pythonic**: Exception handling is idiomatic Python

**Alternatives Considered**:
- Signal handler: Rejected - more complex, signal module less familiar to beginners, platform differences
- Both: Rejected - over-engineering, single method sufficient

**Trade-offs**:
- ✅ Simple, readable code
- ✅ Cross-platform consistent behavior
- ✅ Beginner-friendly (exception handling taught early in Python)
- ❌ Doesn't prevent default signal behavior during blocking I/O (acceptable - input() is brief)

**Implementation**:
```python
# main.py
def main():
    cli = CLI()
    try:
        cli.run()  # Main menu loop
    except KeyboardInterrupt:
        print("\n\nGoodbye!")  # Two newlines for clean spacing after ^C
        sys.exit(0)

if __name__ == "__main__":
    main()
```

---

## Summary of Decisions

| Question | Decision | Key Rationale |
|----------|----------|---------------|
| Timestamp format | Local time (`datetime.now().isoformat()`) | Simplicity, matches user expectations, Phase I scope |
| Task storage | `dict[int, Task]` | O(1) lookup performance, maintains insertion order (Python 3.13+) |
| Validation pattern | TaskManager validates, raises exceptions | Separation of concerns, reusability, testability |
| Ctrl+C handling | `try/except KeyboardInterrupt` | Simplicity, cross-platform, beginner-friendly |

## Best Practices Applied

1. **YAGNI (You Aren't Gonna Need It)**: No premature optimization (e.g., avoided complex timezone handling, didn't add both dict + list storage)
2. **KISS (Keep It Simple, Stupid)**: Chose simplest solution for each problem (local time, try/except over signal handlers)
3. **DRY (Don't Repeat Yourself)**: Single source of truth for validation (TaskManager, not duplicated in CLI)
4. **Separation of Concerns**: TaskManager owns business logic, CLI owns presentation
5. **Pythonic Code**: Used idiomatic Python patterns (.isoformat(), dict insertion order, exception handling)

## Implementation Readiness

All technical unknowns resolved. Ready to proceed with:
- ✅ Phase 1: Create data-model.md (Task entity structure)
- ✅ Phase 1: Create contracts/cli-menu.md (CLI interface contracts)
- ✅ Phase 1: Create quickstart.md (setup and demo workflow)
- ✅ Phase 2: Generate tasks.md via `/sp.tasks`
