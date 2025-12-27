# Feature Specification: Todo CLI Core

**Feature Branch**: `001-todo-cli-core`
**Created**: 2025-12-27
**Status**: Draft
**Input**: User description: "todo-cli-core"

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Add and View Tasks (Priority: P1)

A user launches the todo application and wants to capture tasks they need to complete. They add their first task with a title, optionally provide a description for context, and immediately see it in their task list.

**Why this priority**: This is the foundation of any task management system. Without the ability to add and view tasks, no other functionality matters. This alone provides value as a simple task capture tool.

**Independent Test**: Can be fully tested by launching the app, adding 2-3 tasks with different titles and descriptions, viewing the task list, and verifying all tasks appear with correct IDs, titles, and statuses.

**Acceptance Scenarios**:

1. **Given** the application is running and the task list is empty, **When** the user selects "Add Task" and enters title "Buy groceries" with description "Milk, eggs, bread", **Then** the task is created with ID 1, marked as incomplete, displays creation timestamp, and appears in the task list
2. **Given** the task list has 2 tasks, **When** the user selects "View All Tasks", **Then** all tasks are displayed with IDs, completion status checkboxes, titles, creation timestamps, and descriptions
3. **Given** the task list is empty, **When** the user selects "View All Tasks", **Then** the message "No tasks found" is displayed

---

### User Story 2 - Mark Tasks Complete (Priority: P2)

A user has completed a task from their list and wants to mark it as done to track their progress. They select the complete option, enter the task ID, and the task is visually marked as complete.

**Why this priority**: Marking tasks complete provides immediate satisfaction and progress tracking. Combined with US1, users have a minimal but functional task manager.

**Independent Test**: Can be tested independently by first adding 3 tasks (from US1), then marking task ID 2 as complete, viewing the list to verify the checkbox shows [X], marking it incomplete again, and verifying the checkbox shows [ ].

**Acceptance Scenarios**:

1. **Given** task ID 3 exists and is incomplete, **When** the user selects "Mark Task Complete" and enters ID 3, **Then** the task completion status changes to true and displays with [X] checkbox
2. **Given** task ID 3 exists and is complete, **When** the user selects "Mark Task Complete" and enters ID 3 again, **Then** the task completion status toggles to false and displays with [ ] checkbox
3. **Given** task ID 999 does not exist, **When** the user tries to mark it complete, **Then** error message "Task ID 999 does not exist" is displayed

---

### User Story 3 - Update Task Details (Priority: P3)

A user realizes they need to change a task's title or add more detail to the description. They select the update option, choose the task by ID, and modify the title or description.

**Why this priority**: Tasks evolve and need corrections. This enables users to refine their task list without deleting and re-adding tasks, preserving task history and IDs.

**Independent Test**: Can be tested independently by adding a task "Cal dentist" (typo), then updating it to "Call dentist" and adding description "Schedule annual checkup", and verifying changes persist in the task list.

**Acceptance Scenarios**:

1. **Given** task ID 1 has title "Cal dentist" and no description, **When** the user updates it with title "Call dentist" and description "Schedule annual checkup", **Then** the task title and description are updated and updated timestamp changes
2. **Given** task ID 5 does not exist, **When** the user tries to update it, **Then** error message "Task ID 5 does not exist" is displayed
3. **Given** task ID 2 exists, **When** the user updates it with an empty title, **Then** error message "Title cannot be empty" is displayed and the original title is preserved

---

### User Story 4 - Delete Unwanted Tasks (Priority: P4)

A user has tasks that are no longer relevant or were added by mistake. They want to permanently remove these tasks from their list to keep it clean and focused.

**Why this priority**: List maintenance is important but not critical for initial value delivery. Users can work around deletions by simply not looking at unwanted tasks.

**Independent Test**: Can be tested independently by adding 3 tasks, deleting task ID 2, viewing the list to confirm only tasks 1 and 3 remain, and attempting to delete ID 2 again to verify proper error handling.

**Acceptance Scenarios**:

1. **Given** task ID 4 exists, **When** the user selects "Delete Task" and enters ID 4, **Then** the task is permanently removed and no longer appears in the task list
2. **Given** task ID 10 does not exist, **When** the user tries to delete it, **Then** error message "Task ID 10 does not exist" is displayed
3. **Given** the user accidentally enters a wrong ID during deletion, **When** they are prompted for confirmation before deletion, **Then** they can cancel the operation

---

### User Story 5 - Navigate and Exit Safely (Priority: P5)

A user wants to navigate between different task management functions using a clear menu and exit the application cleanly when done.

**Why this priority**: Essential for usability but doesn't provide direct task management value. Assumes a working menu system from the start.

**Independent Test**: Can be tested by launching the app, trying each menu option (1-6), entering invalid choices like 7 or "abc", and verifying graceful error handling and exit on option 6.

**Acceptance Scenarios**:

1. **Given** the application displays the main menu, **When** the user enters a valid choice (1-6), **Then** the corresponding action is executed
2. **Given** the application displays the main menu, **When** the user enters an invalid choice like 7 or "abc", **Then** error message "Invalid choice. Please enter 1-6" is displayed and menu is shown again
3. **Given** the application is running, **When** the user selects option 6 "Exit", **Then** the application displays "Goodbye!" and exits cleanly
4. **Given** the application is running, **When** the user presses Ctrl+C, **Then** the application exits gracefully without stack traces

---

### Edge Cases

- What happens when a task title is exactly 200 characters? (Accepted as valid)
- What happens when a task title is 201 characters? (Rejected with "Title too long (max 200 characters)")
- What happens when a task title contains only whitespace "   "? (Rejected with "Title cannot be empty")
- What happens when a description is exactly 1000 characters? (Accepted as valid)
- What happens when a description is 1001 characters? (Rejected with "Description too long (max 1000 characters)")
- What happens when user enters non-numeric input for task ID? (Error: "Invalid ID. Please enter a number")
- What happens when user enters negative task ID like -5? (Error: "Invalid ID. Task IDs must be positive")
- What happens when user enters 0 as task ID? (Treated as cancel operation where applicable, otherwise error)
- What happens when trying to add tasks after reaching maximum in-memory capacity? (Accept tasks until system memory exhausted - no artificial limit)

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: System MUST allow users to add a new task with a required title (1-200 characters) and optional description (max 1000 characters)
- **FR-002**: System MUST assign each task a unique sequential integer ID starting from 1
- **FR-003**: System MUST automatically generate and store creation timestamp (ISO 8601 format) when a task is added
- **FR-004**: System MUST automatically update and store updated timestamp (ISO 8601 format) whenever a task is modified
- **FR-005**: System MUST display all tasks with their ID, completion status ([X] or [ ]), title, creation timestamp, and description
- **FR-006**: System MUST display "No tasks found" when the task list is empty
- **FR-007**: Users MUST be able to toggle task completion status by task ID
- **FR-008**: Users MUST be able to update a task's title and/or description by task ID
- **FR-009**: Users MUST be able to delete a task permanently by task ID
- **FR-010**: System MUST reject task titles that are empty or contain only whitespace with error message "Title cannot be empty"
- **FR-011**: System MUST reject task titles exceeding 200 characters with error message "Title too long (max 200 characters)"
- **FR-012**: System MUST reject task descriptions exceeding 1000 characters with error message "Description too long (max 1000 characters)"
- **FR-013**: System MUST return error "Task ID {id} does not exist" when operations reference non-existent task IDs
- **FR-014**: System MUST allow duplicate task titles (users may intentionally create similar tasks)
- **FR-015**: System MUST present a numbered menu (1-6) with options: Add Task, View All Tasks, Update Task, Mark Task Complete, Delete Task, Exit
- **FR-016**: System MUST validate menu input and display "Invalid choice. Please enter 1-6" for invalid selections
- **FR-017**: System MUST store all tasks in memory only (no file or database persistence)
- **FR-018**: System MUST exit cleanly on menu option 6 or Ctrl+C without stack traces

### Key Entities

- **Task**: Represents a single todo item with the following attributes:
  - ID: Unique sequential integer identifier (auto-generated)
  - Title: Required text description of the task (1-200 characters)
  - Description: Optional detailed context for the task (max 1000 characters)
  - Completion Status: Boolean flag indicating if task is complete (default: false)
  - Created Timestamp: ISO 8601 formatted datetime when task was created (auto-generated)
  - Updated Timestamp: ISO 8601 formatted datetime when task was last modified (auto-generated)

- **Task List**: In-memory collection of all tasks, accessible by ID, maintains insertion order for consistent display

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: Users can add a new task in under 10 seconds (from menu selection to confirmation message)
- **SC-002**: Users can view their complete task list in under 3 seconds regardless of list size
- **SC-003**: Users can mark a task complete in under 8 seconds (menu selection, ID entry, confirmation)
- **SC-004**: Application handles 1000 tasks in memory without noticeable performance degradation (under 1 second for any operation)
- **SC-005**: 100% of invalid inputs result in helpful error messages (no stack traces or cryptic errors)
- **SC-006**: Application can run continuously for user session without crashes or data loss (until user exits)
- **SC-007**: New users can understand all available operations from the menu within 30 seconds of launching
- **SC-008**: Users can complete a full workflow (add task, view list, mark complete, delete task) in under 60 seconds
- **SC-009**: Zero crashes occur during normal usage (valid and invalid inputs)

## Assumptions

1. **Single User**: Application runs on a single machine for a single user at a time (no concurrent access)
2. **Session-Based**: Tasks persist only during application runtime; cleared when application exits
3. **Console Environment**: Users have access to a terminal/command prompt with keyboard input
4. **Python Environment**: Users have Python 3.13+ installed and accessible via command line
5. **Display Assumptions**: Terminal supports standard ASCII characters for checkboxes ([ ] and [X])
6. **Memory Availability**: System has sufficient memory to store reasonable task counts (100-1000 tasks)
7. **Input Method**: All user input is keyboard-based text entry (no mouse, no GUI elements)
8. **Locale**: Timestamps use system locale; no internationalization required for Phase I
9. **ID Recycling**: Deleted task IDs are not reused within a session (IDs only increment)

## Out of Scope

The following are explicitly excluded from this feature to maintain Phase I simplicity:

- Data persistence (saving tasks to files or databases)
- Task priorities, categories, or tags
- Due dates or reminders
- Task search or filtering
- Task sorting options
- Undo/redo functionality
- Multi-user support or user accounts
- Authentication or authorization
- Cloud synchronization
- Web interface or GUI
- Mobile application
- Task dependencies or subtasks
- Recurring tasks
- Task notes or attachments
- Export/import functionality
- Statistics or analytics
- Keyboard shortcuts beyond Ctrl+C
