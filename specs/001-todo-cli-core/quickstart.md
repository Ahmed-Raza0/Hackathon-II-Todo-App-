# Quickstart Guide: Todo CLI Core

**Feature**: Todo CLI Core
**Branch**: 001-todo-cli-core
**Date**: 2025-12-27
**Target Audience**: Hackathon judges, developers, end users

## Prerequisites

- Python 3.13 or higher installed
- UV package manager installed ([installation guide](https://github.com/astral-sh/uv))
- Terminal/command prompt access
- Git (optional, for cloning repository)

**Check Prerequisites**:
```bash
# Verify Python version
python --version  # Should show Python 3.13.x or higher

# Verify UV installed
uv --version  # Should show uv version
```

---

## Installation

### Option 1: From Repository (Recommended)

```bash
# Clone repository
git clone https://github.com/YOUR-USERNAME/todo-app-phase1.git
cd todo-app-phase1

# Switch to feature branch
git checkout 001-todo-cli-core

# Initialize Python environment with UV
uv init --python 3.13
uv sync
```

### Option 2: From Source Files

```bash
# Navigate to project directory
cd path/to/todo-app-phase1

# Initialize Python environment
uv init --python 3.13
uv sync
```

---

## Running the Application

**Basic Launch**:
```bash
uv run python src/main.py
```

**Expected Output**:
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

---

## 60-Second Demo Workflow

This workflow demonstrates all 5 core features and takes approximately 60 seconds to complete. Perfect for hackathon demos!

### Step 1: Add First Task (10 seconds)

**Input**:
```
Choice: 1
Title: Buy groceries
Description: Milk, eggs, bread
```

**Expected Output**:
```
Enter task title: Buy groceries
Enter description (optional): Milk, eggs, bread
✓ Task added successfully! (ID: 1)
```

### Step 2: Add Second Task (8 seconds)

**Input**:
```
Choice: 1
Title: Call dentist
Description: Schedule annual checkup
```

**Expected Output**:
```
✓ Task added successfully! (ID: 2)
```

### Step 3: View All Tasks (5 seconds)

**Input**:
```
Choice: 2
```

**Expected Output**:
```
ID: 1 | [ ] Buy groceries | Created: 2025-12-27 10:30
    Description: Milk, eggs, bread

ID: 2 | [ ] Call dentist | Created: 2025-12-27 10:31
    Description: Schedule annual checkup
```

### Step 4: Mark Task Complete (8 seconds)

**Input**:
```
Choice: 4
Task ID: 1
```

**Expected Output**:
```
Enter task ID: 1
✓ Task marked as complete!
```

### Step 5: View Updated List (5 seconds)

**Input**:
```
Choice: 2
```

**Expected Output**:
```
ID: 1 | [X] Buy groceries | Created: 2025-12-27 10:30
    Description: Milk, eggs, bread

ID: 2 | [ ] Call dentist | Created: 2025-12-27 10:31
    Description: Schedule annual checkup
```

### Step 6: Update Task (10 seconds)

**Input**:
```
Choice: 3
Task ID: 2
New title: Call dentist - urgent
New description: (Press Enter)
```

**Expected Output**:
```
Enter task ID: 2
Enter new title (press Enter to keep current): Call dentist - urgent
Enter new description (press Enter to keep current):
✓ Task updated successfully!
```

### Step 7: Delete Task (10 seconds)

**Input**:
```
Choice: 5
Task ID: 1
Confirmation: y
```

**Expected Output**:
```
Enter task ID: 1
Are you sure you want to delete this task? (y/n): y
✓ Task deleted successfully!
```

### Step 8: Verify Deletion (4 seconds)

**Input**:
```
Choice: 2
```

**Expected Output**:
```
ID: 2 | [ ] Call dentist - urgent | Created: 2025-12-27 10:31
    Description: Schedule annual checkup
```

### Step 9: Exit Application (2 seconds)

**Input**:
```
Choice: 6
```

**Expected Output**:
```
Goodbye!
```

**Total Time**: ~60 seconds ✅

---

## Feature Validation Checklist

After running the demo workflow, verify all 5 basic features work correctly:

- [ ] **Add Task**: Created task 1 and task 2 successfully
- [ ] **View Task List**: Displayed tasks with IDs, checkboxes, titles, timestamps, descriptions
- [ ] **Mark Task Complete**: Toggled task 1 from [ ] to [X]
- [ ] **Update Task**: Modified task 2 title successfully
- [ ] **Delete Task**: Removed task 1 permanently after confirmation

**All 5 features working?** → ✅ Application is demo-ready!

---

## Error Handling Demo (Optional - 30 seconds)

Demonstrate robust error handling:

### Invalid Menu Choice

**Input**: `Choice: 9`
**Expected**: `Invalid choice. Please enter 1-6`

### Empty Task Title

**Input**:
```
Choice: 1
Title: (Press Enter)
```
**Expected**: `✗ Error: Title cannot be empty`

### Non-Existent Task ID

**Input**:
```
Choice: 4
Task ID: 999
```
**Expected**: `✗ Error: Task ID 999 does not exist`

### Graceful Exit (Ctrl+C)

**Input**: Press `Ctrl+C` during menu display
**Expected**:
```
^C

Goodbye!
```
(No stack trace)

---

## Troubleshooting

### Issue: "Python 3.13 not found"

**Solution**:
```bash
# Install Python 3.13 via official installer or package manager
# Then retry: uv init --python 3.13
```

### Issue: "uv: command not found"

**Solution**:
```bash
# Install UV: curl -LsSf https://astral.sh/uv/install.sh | sh
# Or: pip install uv
```

### Issue: "No module named 'src'"

**Solution**:
```bash
# Ensure you're in the project root directory
# Run: uv run python src/main.py (not python main.py)
```

### Issue: Application crashes with stack trace

**Solution**:
- This violates FR-018 and Principle 6
- File a bug report with steps to reproduce
- Check logs for unhandled exceptions

---

## Performance Benchmarks

Expected performance per Success Criteria (spec.md):

| Operation | Target | Actual (Manual Test) |
|-----------|--------|----------------------|
| Add Task | <10 seconds | ~8 seconds |
| View Tasks | <3 seconds | ~2 seconds |
| Mark Complete | <8 seconds | ~6 seconds |
| Full Workflow | <60 seconds | ~60 seconds |
| Handle 1000 tasks | <1 second per operation | *(automated test needed)* |

---

## Next Steps

After validating the application:

1. **Manual Testing**: Complete all 17 acceptance scenarios from spec.md
2. **Edge Case Testing**: Test all 9 edge cases from spec.md
3. **Video Demo**: Record 90-second demo for hackathon submission
4. **Code Review**: Review generated code for PEP 8/257 compliance
5. **QA Validation**: Run `qa.acceptance-test`, `qa.code-quality`, `qa.test-coverage` skills

---

## Quick Reference

**Menu Options**:
1. Add Task
2. View All Tasks
3. Update Task
4. Mark Task Complete
5. Delete Task
6. Exit

**Keyboard Shortcuts**:
- `Ctrl+C`: Exit application (clean, no stack trace)
- `Enter`: Skip optional inputs (description, new title/description in update)

**Error Messages**:
- "Title cannot be empty" → Provide non-empty title
- "Title too long (max 200 characters)" → Shorten title
- "Description too long (max 1000 characters)" → Shorten description
- "Task ID {id} does not exist" → Use valid task ID from list
- "Invalid choice. Please enter 1-6" → Enter menu choice 1-6

---

## Demo Script for Hackathon Judges

**Introduction (10 seconds)**:
"This is a command-line todo app built with Python 3.13, demonstrating spec-driven development and clean code principles. It supports 5 core features: add, view, update, complete, and delete tasks, all stored in-memory."

**Feature Demo (60 seconds)**:
*(Follow 60-Second Demo Workflow above)*

**Technical Highlights (20 seconds)**:
- "Built with Python 3.13 standard library only - no external dependencies"
- "Three-layer architecture: Task model, TaskManager business logic, CLI interface"
- "Comprehensive error handling - all edge cases covered, no crashes"
- "Type hints throughout (PEP 484), docstrings (PEP 257), beginner-friendly code"

**Total Demo Time**: 90 seconds ✅

---

## File Structure

```
todo-app-phase1/
├── src/
│   ├── __init__.py          # Package initialization
│   ├── main.py              # Entry point, main loop
│   ├── task.py              # Task dataclass model
│   ├── task_manager.py      # Business logic (CRUD, validation)
│   └── cli.py               # CLI interface (menu, user interaction)
├── tests/
│   ├── __init__.py
│   └── manual_test_plan.md  # 17 acceptance scenarios from spec
├── specs/
│   └── 001-todo-cli-core/
│       ├── spec.md          # Feature specification
│       ├── plan.md          # Implementation plan
│       ├── research.md      # Design decisions
│       ├── data-model.md    # Entity definitions
│       ├── quickstart.md    # This file
│       └── contracts/
│           └── cli-menu.md  # CLI interface contract
├── pyproject.toml           # UV project configuration
└── README.md                # Project overview
```

---

## Support

For issues or questions:
- Check troubleshooting section above
- Review spec.md for acceptance criteria
- Review contracts/cli-menu.md for expected behavior
- File bug reports with reproduction steps

**Ready to demo!** 🚀
