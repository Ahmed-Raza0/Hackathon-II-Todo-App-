# Manual Test Plan: Todo CLI Core

**Feature**: Todo CLI Core (Phase I)
**Date**: 2025-12-27
**Test Type**: Manual acceptance testing
**Total Scenarios**: 17 acceptance scenarios + 9 edge cases

## Prerequisites

- Python 3.13+ installed
- UV package manager installed
- Application built and runnable via `uv run python src/main.py`

## Test Execution Instructions

1. Launch the application: `uv run python src/main.py`
2. For each test scenario below:
   - Follow the **Given/When/Then** steps exactly
   - Mark the checkbox [x] if test passes
   - Note any failures in the "Notes" column
3. All 17 acceptance scenarios MUST pass for feature to be considered complete

---

## User Story 1: Add and View Tasks (P1) - 3 scenarios

### Scenario 1.1: Add first task with description
- [ ] **Given** the application is running and the task list is empty
- [ ] **When** the user selects "Add Task" (option 1) and enters:
  - Title: "Buy groceries"
  - Description: "Milk, eggs, bread"
- [ ] **Then** verify:
  - Task is created with ID 1
  - Task is marked as incomplete [ ]
  - Task displays creation timestamp
  - Task appears in the task list with title and description

**Notes**: _____________________

### Scenario 1.2: View multiple tasks
- [ ] **Given** the task list has 2 tasks (IDs 1 and 2)
- [ ] **When** the user selects "View All Tasks" (option 2)
- [ ] **Then** verify:
  - All tasks are displayed
  - Each task shows: ID, checkbox [ ] or [X], title, creation timestamp, description

**Notes**: _____________________

### Scenario 1.3: View empty task list
- [ ] **Given** the task list is empty (fresh start or all tasks deleted)
- [ ] **When** the user selects "View All Tasks" (option 2)
- [ ] **Then** verify:
  - Message "No tasks found" is displayed

**Notes**: _____________________

---

## User Story 2: Mark Tasks Complete (P2) - 3 scenarios

### Scenario 2.1: Mark incomplete task as complete
- [ ] **Given** task ID 3 exists and is incomplete [ ]
- [ ] **When** the user selects "Mark Task Complete" (option 4) and enters ID 3
- [ ] **Then** verify:
  - Task completion status changes to true
  - Task displays with [X] checkbox
  - Confirmation message displayed

**Notes**: _____________________

### Scenario 2.2: Toggle complete task back to incomplete
- [ ] **Given** task ID 3 exists and is complete [X]
- [ ] **When** the user selects "Mark Task Complete" (option 4) and enters ID 3 again
- [ ] **Then** verify:
  - Task completion status toggles to false
  - Task displays with [ ] checkbox
  - Confirmation message displayed

**Notes**: _____________________

### Scenario 2.3: Mark non-existent task complete
- [ ] **Given** task ID 999 does not exist
- [ ] **When** the user tries to mark it complete
- [ ] **Then** verify:
  - Error message "Task ID 999 does not exist" is displayed
  - Application does not crash
  - Menu is re-displayed

**Notes**: _____________________

---

## User Story 3: Update Task Details (P3) - 3 scenarios

### Scenario 3.1: Update task title and description
- [ ] **Given** task ID 1 has title "Cal dentist" and no description
- [ ] **When** the user selects "Update Task" (option 3) and enters:
  - Task ID: 1
  - New title: "Call dentist"
  - New description: "Schedule annual checkup"
- [ ] **Then** verify:
  - Task title is updated to "Call dentist"
  - Task description is updated to "Schedule annual checkup"
  - Updated timestamp changes (is more recent than created timestamp)

**Notes**: _____________________

### Scenario 3.2: Update non-existent task
- [ ] **Given** task ID 5 does not exist
- [ ] **When** the user tries to update it
- [ ] **Then** verify:
  - Error message "Task ID 5 does not exist" is displayed
  - Application does not crash
  - Menu is re-displayed

**Notes**: _____________________

### Scenario 3.3: Update with empty title
- [ ] **Given** task ID 2 exists with title "Original Title"
- [ ] **When** the user updates it with an empty title (just press Enter for title)
- [ ] **Then** verify:
  - Error message "Title cannot be empty" is displayed
  - Original title is preserved
  - Task is not modified

**Notes**: _____________________

---

## User Story 4: Delete Unwanted Tasks (P4) - 3 scenarios

### Scenario 4.1: Delete existing task
- [ ] **Given** task ID 4 exists
- [ ] **When** the user selects "Delete Task" (option 5) and enters:
  - Task ID: 4
  - Confirmation: y
- [ ] **Then** verify:
  - Task is permanently removed
  - Task no longer appears in task list
  - Confirmation message displayed

**Notes**: _____________________

### Scenario 4.2: Delete non-existent task
- [ ] **Given** task ID 10 does not exist
- [ ] **When** the user tries to delete it
- [ ] **Then** verify:
  - Error message "Task ID 10 does not exist" is displayed
  - Application does not crash
  - Menu is re-displayed

**Notes**: _____________________

### Scenario 4.3: Cancel deletion with confirmation prompt
- [ ] **Given** task ID 2 exists
- [ ] **When** the user selects "Delete Task" and enters:
  - Task ID: 2
  - Confirmation: n (or any input other than 'y')
- [ ] **Then** verify:
  - Message "Deletion cancelled" is displayed
  - Task ID 2 still exists in task list
  - No changes made to task

**Notes**: _____________________

---

## User Story 5: Navigate and Exit Safely (P5) - 4 scenarios

### Scenario 5.1: Execute valid menu choices
- [ ] **Given** the application displays the main menu
- [ ] **When** the user enters each valid choice (1-6) in sequence
- [ ] **Then** verify:
  - Option 1 → Add Task flow starts
  - Option 2 → View Tasks flow executes
  - Option 3 → Update Task flow starts
  - Option 4 → Mark Complete flow starts
  - Option 5 → Delete Task flow starts
  - Option 6 → Exit flow executes

**Notes**: _____________________

### Scenario 5.2: Handle invalid menu choice (out of range)
- [ ] **Given** the application displays the main menu
- [ ] **When** the user enters choice 7
- [ ] **Then** verify:
  - Error message "Invalid choice. Please enter 1-6" is displayed
  - Menu is shown again
  - Application does not crash

**Notes**: _____________________

### Scenario 5.3: Handle invalid menu choice (non-numeric)
- [ ] **Given** the application displays the main menu
- [ ] **When** the user enters "abc"
- [ ] **Then** verify:
  - Error message "Invalid choice. Please enter 1-6" is displayed
  - Menu is shown again
  - Application does not crash

**Notes**: _____________________

### Scenario 5.4: Exit gracefully with option 6
- [ ] **Given** the application is running
- [ ] **When** the user selects option 6 "Exit"
- [ ] **Then** verify:
  - Application displays "Goodbye!" message
  - Application exits cleanly (exit code 0)
  - No error messages or stack traces

**Notes**: _____________________

### Scenario 5.5: Exit gracefully with Ctrl+C
- [ ] **Given** the application is running at the menu prompt
- [ ] **When** the user presses Ctrl+C
- [ ] **Then** verify:
  - Application exits gracefully
  - No stack traces displayed
  - Clean exit (no error messages)

**Notes**: _____________________

---

## Edge Case Testing (9 cases)

### Edge Case 1: Maximum valid title length (200 characters)
- [ ] **Given** the user adds a task
- [ ] **When** the title is exactly 200 characters long
- [ ] **Then** verify:
  - Task is accepted as valid
  - No error message displayed

**Notes**: _____________________

### Edge Case 2: Title exceeds maximum (201 characters)
- [ ] **Given** the user adds a task
- [ ] **When** the title is 201 characters long
- [ ] **Then** verify:
  - Task is rejected
  - Error message "Title too long (max 200 characters)" is displayed

**Notes**: _____________________

### Edge Case 3: Title with only whitespace
- [ ] **Given** the user adds a task
- [ ] **When** the title contains only spaces "   "
- [ ] **Then** verify:
  - Task is rejected
  - Error message "Title cannot be empty" is displayed

**Notes**: _____________________

### Edge Case 4: Maximum valid description length (1000 characters)
- [ ] **Given** the user adds a task
- [ ] **When** the description is exactly 1000 characters long
- [ ] **Then** verify:
  - Task is accepted as valid
  - No error message displayed

**Notes**: _____________________

### Edge Case 5: Description exceeds maximum (1001 characters)
- [ ] **Given** the user adds a task
- [ ] **When** the description is 1001 characters long
- [ ] **Then** verify:
  - Task is rejected
  - Error message "Description too long (max 1000 characters)" is displayed

**Notes**: _____________________

### Edge Case 6: Non-numeric task ID input
- [ ] **Given** the user selects an operation requiring task ID
- [ ] **When** the user enters "abc" as task ID
- [ ] **Then** verify:
  - Error message "Invalid ID. Please enter a number" is displayed
  - Application does not crash

**Notes**: _____________________

### Edge Case 7: Negative task ID
- [ ] **Given** the user selects an operation requiring task ID
- [ ] **When** the user enters -5 as task ID
- [ ] **Then** verify:
  - Error message "Invalid ID. Task IDs must be positive" or "Task ID -5 does not exist" is displayed
  - Application does not crash

**Notes**: _____________________

### Edge Case 8: Zero as task ID
- [ ] **Given** the user selects an operation requiring task ID
- [ ] **When** the user enters 0 as task ID
- [ ] **Then** verify:
  - Appropriate error handling (treated as cancel or error)
  - Application does not crash

**Notes**: _____________________

### Edge Case 9: Update task with no changes
- [ ] **Given** task ID 1 exists
- [ ] **When** the user updates it but presses Enter for both title and description (no changes)
- [ ] **Then** verify:
  - Message "No changes provided" is displayed
  - Task is not modified
  - No error occurred

**Notes**: _____________________

---

## Test Summary

**Total Scenarios**: 17 acceptance + 9 edge cases = 26 total tests

**Acceptance Tests**:
- [ ] User Story 1 (3/3 passed)
- [ ] User Story 2 (3/3 passed)
- [ ] User Story 3 (3/3 passed)
- [ ] User Story 4 (3/3 passed)
- [ ] User Story 5 (5/5 passed)

**Edge Case Tests**:
- [ ] All 9 edge cases passed

**Overall Status**: ___________ (PASS/FAIL)

**Tested By**: _____________________
**Date Completed**: _____________________

---

## Notes and Issues

Record any bugs, unexpected behavior, or issues discovered during testing:

1. _____________________
2. _____________________
3. _____________________

---

## Success Criteria Validation

After all tests pass, verify these success criteria from spec.md:

- [ ] SC-001: Users can add a task in under 10 seconds
- [ ] SC-002: Users can view their task list in under 3 seconds
- [ ] SC-003: Users can mark a task complete in under 8 seconds
- [ ] SC-004: Application handles 1000 tasks without performance degradation (< 1 second per operation)
- [ ] SC-005: 100% of error scenarios display helpful error messages (no stack traces)
- [ ] SC-006: Users can update task details without losing original timestamps
- [ ] SC-007: Users can delete tasks with confirmation to prevent accidental deletion
- [ ] SC-008: Users can complete full workflow (add → view → complete → update → delete) in under 60 seconds
- [ ] SC-009: Application exits cleanly on user request or Ctrl+C without errors

**All Success Criteria Met**: [ ] YES / [ ] NO

---

## Appendix: Test Data Templates

### Valid Task Titles
- "Buy groceries"
- "Call dentist"
- "Submit project report"
- "A" * 200 (200 characters)

### Valid Descriptions
- "Milk, eggs, bread"
- "Schedule annual checkup"
- "" (empty is valid)
- "A" * 1000 (1000 characters)

### Invalid Inputs
- Title: "" (empty), "   " (whitespace), "A" * 201 (too long)
- Description: "A" * 1001 (too long)
- Task IDs: "abc", -5, 0, 999 (non-existent)
