---
name: qa.acceptance-test
owner: QA Agent
category: Testing
description: Execute acceptance testing by validating implemented features against specification acceptance criteria
version: 1.0.0
created: 2025-12-27
---

# QA Acceptance Testing Skill

## Purpose

Systematically validate that implemented features meet their acceptance criteria as defined in the feature specification. This skill ensures feature completeness and correctness before marking work as done.

## When to Use

- After implementing tasks from `tasks.md`
- Before marking a feature as complete
- When validating a pull request or code review
- During manual QA cycles
- After bug fixes to prevent regression

## Inputs

**Required:**
- `feature_name` (string): Name of the feature to test (e.g., "todo-app")
- `spec_path` (path): Absolute path to the feature specification file (e.g., `specs/todo-app/spec.md`)

**Optional:**
- `task_id` (string): Specific task ID from tasks.md to validate (default: all tasks)
- `environment` (string): Testing environment context (default: "local")
- `output_format` (enum): Report format - "markdown" | "json" | "console" (default: "markdown")

## Step-by-Step Process

### 1. Preparation Phase

**1.1. Read Specification**
- Open and parse `{spec_path}`
- Extract all acceptance criteria sections
- Identify testable requirements
- Map acceptance criteria to task IDs (if tasks.md exists)

**1.2. Discover Test Artifacts**
- Locate implementation files (search for `*.py` in project root and subdirectories)
- Find test files (search for `test_*.py` or `*_test.py`)
- Identify executable entry points (CLI commands, main scripts)

**1.3. Environment Validation**
- Verify Python environment is active
- Check required dependencies are installed
- Confirm test runner is available (pytest, unittest, etc.)

### 2. Execution Phase

**2.1. Run Automated Tests**
- Execute all test suites related to the feature
- Capture test results, including:
  - Pass/fail status
  - Test names and descriptions
  - Failure messages and stack traces
  - Code coverage metrics

**2.2. Manual Validation Checklist**

For each acceptance criterion:

a. **Identify the criterion**
   - Extract from spec: criterion text, expected behavior, constraints

b. **Map to implementation**
   - Locate relevant code that implements this behavior
   - Identify corresponding test cases

c. **Execute validation**
   - If automated test exists: verify test passes
   - If no automated test: perform manual verification steps
   - Document actual vs expected behavior

d. **Record result**
   - Status: PASS | FAIL | PARTIAL | NOT_TESTED
   - Evidence: test output, CLI output, observations
   - Notes: deviations, concerns, questions

**2.3. Boundary and Edge Case Testing**

For each core operation (add, list, update, delete, complete):
- Test with valid inputs (happy path)
- Test with invalid inputs (malformed data, wrong types)
- Test boundary conditions (empty lists, max limits, special characters)
- Test error handling (non-existent IDs, duplicate operations)

### 3. Analysis Phase

**3.1. Gap Analysis**
- Identify acceptance criteria without corresponding tests
- Find implemented features not covered by acceptance criteria
- Detect missing error handling or edge case coverage

**3.2. Quality Assessment**
- Evaluate test quality (clear assertions, good coverage, realistic scenarios)
- Check for proper error messages and user feedback
- Validate adherence to constitution principles

**3.3. Regression Check**
- Verify that new changes don't break existing functionality
- Confirm all previously passing tests still pass

### 4. Reporting Phase

**4.1. Generate Report**

Include the following sections:

```markdown
# Acceptance Test Report: {feature_name}

**Feature**: {feature_name}
**Date**: {YYYY-MM-DD HH:MM}
**Tester**: QA Agent
**Environment**: {environment}

## Summary

- Total Acceptance Criteria: X
- Passed: Y
- Failed: Z
- Not Tested: N

## Detailed Results

### Criterion: {acceptance_criterion_1}
- **Status**: PASS | FAIL | PARTIAL | NOT_TESTED
- **Evidence**: {test output or manual validation notes}
- **Mapped Tests**: test_function_name
- **Notes**: {any deviations or concerns}

[Repeat for each criterion]

## Coverage Gaps

- {List untested acceptance criteria}
- {List missing edge case tests}

## Failures and Issues

{Detailed description of any failures, with reproduction steps}

## Recommendations

{Actionable next steps to achieve full compliance}
```

**4.2. Output Results**
- Save report to `history/qa/{feature_name}/acceptance-test-{timestamp}.md`
- Print summary to console
- Return structured data if `output_format=json`

## Output

**Success Case:**
- Acceptance test report (markdown or JSON)
- Console summary showing pass/fail counts
- Exit code 0 if all criteria pass, 1 if any fail

**Report Structure:**
```json
{
  "feature": "todo-app",
  "timestamp": "2025-12-27T10:30:00Z",
  "summary": {
    "total": 12,
    "passed": 10,
    "failed": 2,
    "not_tested": 0
  },
  "results": [
    {
      "criterion": "User can add a task with description",
      "status": "PASS",
      "evidence": "test_add_task_with_description PASSED",
      "notes": ""
    }
  ],
  "gaps": [],
  "issues": [],
  "recommendations": []
}
```

## Failure Handling

### Failure Scenario: Specification Not Found
- **Cause**: Invalid `spec_path` or file doesn't exist
- **Action**: Display error message with expected path format
- **Recovery**: Prompt user for correct spec path
- **Exit Code**: 2

### Failure Scenario: No Acceptance Criteria Found
- **Cause**: Spec exists but contains no testable acceptance criteria
- **Action**: Warn user and list spec sections found
- **Recovery**: Suggest running `/sp.specify` to improve spec
- **Exit Code**: 3

### Failure Scenario: Implementation Not Found
- **Cause**: No Python files exist in project
- **Action**: Report that feature appears unimplemented
- **Recovery**: Suggest running `/sp.implement`
- **Exit Code**: 4

### Failure Scenario: Tests Fail to Execute
- **Cause**: Test runner error, import issues, syntax errors
- **Action**: Capture error output and display
- **Recovery**: Fix test execution issues before retrying
- **Exit Code**: 5

### Failure Scenario: Acceptance Criteria Not Met
- **Cause**: Tests fail or manual validation shows non-compliance
- **Action**: Generate detailed failure report with evidence
- **Recovery**: Fix implementation issues and re-run
- **Exit Code**: 1

### Failure Scenario: Partial Coverage
- **Cause**: Some acceptance criteria have no tests
- **Action**: List untested criteria in gaps section
- **Recovery**: Add missing tests and re-run
- **Exit Code**: 6 (warning, not blocking)

## Determinism Guarantees

- Same inputs always produce same validation results
- Test execution order is consistent
- Reports are reproducible across runs
- No random test data (use fixed test fixtures)

## Integration Points

- Works with `/sp.specify` outputs (reads spec.md)
- Works with `/sp.tasks` outputs (maps criteria to tasks)
- Works with `/sp.implement` outputs (tests implementation)
- Feeds into `/sp.git.commit_pr` (validation gate)

## Quality Standards

This skill enforces:
- 100% acceptance criteria coverage (all criteria must have validation)
- Clear pass/fail determination (no ambiguous results)
- Reproducible tests (same inputs = same outputs)
- Actionable failure reports (specific steps to fix)

## Usage Example

```bash
# Test all acceptance criteria for todo-app
/qa.acceptance-test --feature todo-app --spec specs/todo-app/spec.md

# Test specific task
/qa.acceptance-test --feature todo-app --spec specs/todo-app/spec.md --task TASK-003

# Generate JSON report
/qa.acceptance-test --feature todo-app --spec specs/todo-app/spec.md --output json
```
