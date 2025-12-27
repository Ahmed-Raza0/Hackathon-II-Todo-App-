# CLI Interface Contract: Todo CLI Core

**Feature**: Todo CLI Core
**Branch**: 001-todo-cli-core
**Date**: 2025-12-27
**Status**: Approved

## Overview

This document specifies the CLI interface contract for the Todo CLI Core application, implementing the menu system and user interaction flows defined in spec.md and constitution Principle 6 (User Experience Requirements).

## Menu System Contract

### Menu Display

**Format** (exact per Principle 6):
```
=== Todo App ===
1. Add Task
2. View All Tasks
3. Update Task
4. Mark Task Complete
5. Delete Task
6. Exit

Enter your choice (1-6):
```

**Behavior**:
- Display menu after every operation completes
- Wait for user input (blocking)
- Validate input before executing action
- Re-display menu after invalid input or after action completion

### Input Validation

**Valid Inputs**: Integers 1-6 (inclusive)

**Invalid Input Handling**:

| Input Type | Example | Response | Next Action |
|------------|---------|----------|-------------|
| Non-numeric | "abc", "hello", "" | "Invalid choice. Please enter 1-6" | Re-display menu |
| Out of range (low) | "0", "-1" | "Invalid choice. Please enter 1-6" | Re-display menu |
| Out of range (high) | "7", "10", "99" | "Invalid choice. Please enter 1-6" | Re-display menu |
| Decimal | "1.5", "3.14" | "Invalid choice. Please enter 1-6" | Re-display menu |

**Implementation Pattern**:
```python
def get_menu_choice() -> int | None:
    """Get and validate user menu choice.

    Returns:
        Valid choice (1-6) or None if invalid
    """
    try:
        choice = int(input("Enter your choice (1-6): "))
        if 1 <= choice <= 6:
            return choice
        else:
            print("Invalid choice. Please enter 1-6")
            return None
    except ValueError:
        print("Invalid choice. Please enter 1-6")
        return None
```

---

## Operation Flows

### 1. Add Task Flow

**Trigger**: User selects menu option 1

**Input Prompts**:
1. `"Enter task title: "` → title (string, required)
2. `"Enter description (optional): "` → description (string, optional, press Enter to skip)

**Processing**:
1. Call `TaskManager.add_task(title, description or None)`
2. Handle exceptions:
   - `InvalidTaskError` → Display error message
   - Other exceptions → Display generic error

**Success Output**:
```
✓ Task added successfully! (ID: {task.id})
```

**Error Output Examples**:
```
✗ Error: Title cannot be empty
✗ Error: Title too long (max 200 characters)
✗ Error: Description too long (max 1000 characters)
```

**Next Action**: Re-display menu

**Contract**:
```
add_task_flow() -> void
  Inputs: title (str), description (str | None)
  Calls: TaskManager.add_task(title, description)
  Outputs:
    Success: "✓ Task added successfully! (ID: {id})"
    Error: "✗ Error: {error_message}"
  Exceptions: Caught and displayed as errors
  Menu: Re-displayed after completion
```

---

### 2. View All Tasks Flow

**Trigger**: User selects menu option 2

**Processing**:
1. Call `TaskManager.get_all_tasks() -> list[Task]`
2. If empty: Display "No tasks found"
3. If not empty: Display each task using `task.to_display()`

**Output Format** (per Principle 6):
```
ID: 1 | [X] Buy groceries | Created: 2025-01-15 10:30
    Description: Milk, eggs, bread

ID: 2 | [ ] Call dentist | Created: 2025-01-15 11:45
    Description: Schedule annual checkup

ID: 3 | [ ] Read documentation | Created: 2025-01-15 12:00
```

**Empty List Output**:
```
No tasks found
```

**Next Action**: Re-display menu

**Contract**:
```
view_tasks_flow() -> void
  Inputs: None
  Calls: TaskManager.get_all_tasks()
  Outputs:
    Empty: "No tasks found"
    Non-empty: task.to_display() for each task
  Exceptions: None expected (get_all_tasks() doesn't raise)
  Menu: Re-displayed after completion
```

---

### 3. Update Task Flow

**Trigger**: User selects menu option 3

**Input Prompts**:
1. `"Enter task ID: "` → task_id (integer)
2. `"Enter new title (press Enter to keep current): "` → title (string, optional)
3. `"Enter new description (press Enter to keep current): "` → description (string, optional)

**Processing**:
1. Validate task_id is positive integer
2. If both title and description empty → Display "No changes provided" and return
3. Call `TaskManager.update_task(task_id, title or None, description or None)`
4. Handle exceptions

**Success Output**:
```
✓ Task updated successfully!
```

**Error Output Examples**:
```
✗ Error: Invalid ID. Please enter a number
✗ Error: Task ID {id} does not exist
✗ Error: Title cannot be empty
✗ Error: Title too long (max 200 characters)
✗ Error: Description too long (max 1000 characters)
✗ Error: No changes provided
```

**Next Action**: Re-display menu

**Contract**:
```
update_task_flow() -> void
  Inputs: task_id (int), title (str | None), description (str | None)
  Calls: TaskManager.update_task(task_id, title, description)
  Outputs:
    Success: "✓ Task updated successfully!"
    Error: "✗ Error: {error_message}"
  Exceptions: TaskNotFoundError, InvalidTaskError (caught and displayed)
  Menu: Re-displayed after completion
```

---

### 4. Mark Task Complete Flow

**Trigger**: User selects menu option 4

**Input Prompts**:
1. `"Enter task ID: "` → task_id (integer)

**Processing**:
1. Validate task_id is positive integer
2. Call `TaskManager.toggle_complete(task_id)`
3. Handle exceptions

**Success Output**:
```
✓ Task marked as complete!
```
OR
```
✓ Task marked as incomplete!
```
(Determined by Task.is_complete after toggle)

**Error Output Examples**:
```
✗ Error: Invalid ID. Please enter a number
✗ Error: Task ID {id} does not exist
```

**Next Action**: Re-display menu

**Contract**:
```
mark_complete_flow() -> void
  Inputs: task_id (int)
  Calls: TaskManager.toggle_complete(task_id)
  Outputs:
    Success: "✓ Task marked as complete!" or "✓ Task marked as incomplete!"
    Error: "✗ Error: {error_message}"
  Exceptions: TaskNotFoundError (caught and displayed)
  Menu: Re-displayed after completion
```

---

### 5. Delete Task Flow

**Trigger**: User selects menu option 5

**Input Prompts**:
1. `"Enter task ID: "` → task_id (integer)
2. `"Are you sure you want to delete this task? (y/n): "` → confirmation (char)

**Processing**:
1. Validate task_id is positive integer
2. Prompt for confirmation (y/n, case-insensitive)
3. If user enters anything other than 'y' or 'Y' → Cancel and display "Deletion cancelled"
4. If confirmed → Call `TaskManager.delete_task(task_id)`
5. Handle exceptions

**Success Output**:
```
✓ Task deleted successfully!
```

**Cancellation Output**:
```
Deletion cancelled
```

**Error Output Examples**:
```
✗ Error: Invalid ID. Please enter a number
✗ Error: Task ID {id} does not exist
```

**Next Action**: Re-display menu

**Contract**:
```
delete_task_flow() -> void
  Inputs: task_id (int), confirmation (char)
  Calls: TaskManager.delete_task(task_id) if confirmed
  Outputs:
    Success: "✓ Task deleted successfully!"
    Cancelled: "Deletion cancelled"
    Error: "✗ Error: {error_message}"
  Exceptions: TaskNotFoundError (caught and displayed)
  Menu: Re-displayed after completion
```

---

### 6. Exit Flow

**Trigger**: User selects menu option 6

**Processing**:
1. Display exit message
2. Exit application cleanly (exit code 0)

**Output**:
```
Goodbye!
```

**Next Action**: Application terminates

**Contract**:
```
exit_application() -> never
  Inputs: None
  Calls: sys.exit(0)
  Outputs: "Goodbye!"
  Exceptions: None
  Menu: Not re-displayed (application exits)
```

---

## Exception Handling Contract

**All CLI flows must catch and display exceptions from TaskManager**:

| Exception | Display Format | User Action |
|-----------|----------------|-------------|
| `InvalidTaskError(msg)` | `"✗ Error: {msg}"` | Re-display menu |
| `TaskNotFoundError(msg)` | `"✗ Error: {msg}"` | Re-display menu |
| `ValueError` (from invalid int input) | `"✗ Error: Invalid ID. Please enter a number"` | Re-display menu |
| `KeyboardInterrupt` (Ctrl+C) | `"\n\nGoodbye!"` | Clean exit (code 0) |
| Unexpected exception | `"✗ An unexpected error occurred. Please try again."` | Re-display menu |

**Implementation Pattern**:
```python
def some_task_flow(self):
    try:
        # Get user input
        # Call TaskManager method
        # Display success message
    except InvalidTaskError as e:
        print(f"✗ Error: {e}")
    except TaskNotFoundError as e:
        print(f"✗ Error: {e}")
    except ValueError:
        print("✗ Error: Invalid ID. Please enter a number")
    except Exception as e:
        print(f"✗ An unexpected error occurred: {e}")
```

---

## Main Loop Contract

**Entry Point**: `CLI.run()`

**Behavior**:
1. Initialize TaskManager
2. Enter infinite loop:
   - Display menu
   - Get user choice
   - Execute corresponding flow (1-6)
   - If choice 6 → Exit
   - Otherwise → Loop continues
3. Catch KeyboardInterrupt (Ctrl+C) → Display "Goodbye!" and exit cleanly

**Pseudocode**:
```python
def run(self):
    """Main CLI loop."""
    while True:
        self.display_menu()
        choice = self.get_menu_choice()

        if choice is None:
            continue  # Invalid input, re-display menu

        if choice == 1:
            self.add_task_flow()
        elif choice == 2:
            self.view_tasks_flow()
        elif choice == 3:
            self.update_task_flow()
        elif choice == 4:
            self.mark_complete_flow()
        elif choice == 5:
            self.delete_task_flow()
        elif choice == 6:
            self.exit_application()
```

---

## Compliance Matrix

| Requirement | Contract Section | Validation |
|-------------|------------------|------------|
| FR-015 (menu with 6 options) | Menu System Contract | ✅ Exact format specified |
| FR-016 (validate menu input, error message) | Input Validation | ✅ "Invalid choice. Please enter 1-6" |
| FR-018 (exit cleanly on option 6 or Ctrl+C) | Exit Flow, Exception Handling | ✅ "Goodbye!" + sys.exit(0) |
| Principle 6 (menu interface format) | Menu Display | ✅ Matches exact format |
| Principle 6 (task display format) | View All Tasks Flow | ✅ Uses task.to_display() |
| Principle 6 (clear prompts) | All operation flows | ✅ Explicit prompts for all inputs |
| Principle 6 (immediate feedback) | Success/Error outputs | ✅ "✓ Success!" or "✗ Error: ..." |
| Principle 6 (no crashes) | Exception Handling Contract | ✅ All exceptions caught |

---

## User Experience Guarantees

1. **No Stack Traces**: All exceptions caught and displayed as user-friendly messages
2. **Immediate Feedback**: Every action confirms success or explains failure
3. **Clear Navigation**: Menu always re-displayed except on exit
4. **Forgiving Input**: Invalid inputs handled gracefully, user can retry
5. **Confirmation for Destructive Actions**: Delete requires "y" confirmation
6. **Graceful Exit**: Ctrl+C or option 6 both exit cleanly with "Goodbye!"

---

## Next Steps

- ✅ CLI interface contract complete and approved
- ⏩ Create quickstart.md (setup and demo workflow)
- ⏩ Generate tasks.md via `/sp.tasks` (implementation tasks)
