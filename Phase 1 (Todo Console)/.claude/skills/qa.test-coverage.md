---
name: qa.test-coverage
owner: QA Agent
category: Testing
description: Analyze test coverage depth, quality, and completeness to ensure robust testing practices
version: 1.0.0
created: 2025-12-27
---

# QA Test Coverage Validation Skill

## Purpose

Measure and validate test coverage to ensure adequate testing of all code paths, edge cases, and business logic. This skill goes beyond line coverage to assess test quality, effectiveness, and adherence to TDD principles.

## When to Use

- After implementing new features
- Before merging pull requests
- During test suite refactoring
- When debugging flaky tests
- As a quality gate in CI/CD pipelines

## Inputs

**Required:**
- `target_path` (path): Source code directory to analyze (e.g., `src/`)

**Optional:**
- `test_path` (path): Test directory (default: auto-detect `tests/`, `test/`, or files matching `test_*.py`)
- `min_coverage` (number): Minimum acceptable coverage percentage (default: 80)
- `coverage_type` (enum): Coverage metric - "line" | "branch" | "statement" (default: "branch")
- `output_format` (enum): Report format - "markdown" | "json" | "html" | "console" (default: "markdown")
- `include_integration` (boolean): Include integration tests in analysis (default: true)
- `fail_under` (number): Fail if coverage is below this threshold (default: same as min_coverage)

## Step-by-Step Process

### 1. Discovery Phase

**1.1. Locate Source Files**
- Find all `*.py` files in `{target_path}`
- Exclude: `__init__.py` (if empty), test files, migrations, config files
- Build list of modules to analyze

**1.2. Locate Test Files**
- Find test files matching patterns:
  - `test_*.py`
  - `*_test.py`
  - Files in `tests/` or `test/` directories
- Categorize by type:
  - Unit tests (test single functions/classes)
  - Integration tests (test interactions)
  - End-to-end tests (test full workflows)

**1.3. Identify Test Framework**
- Detect pytest, unittest, or other frameworks
- Verify test runner is available
- Check for configuration files (pytest.ini, .coveragerc, setup.cfg)

### 2. Coverage Measurement Phase

**2.1. Run Tests with Coverage**

Execute coverage analysis:

```bash
# Using pytest with coverage
pytest --cov={target_path} --cov-report=term --cov-report=json --cov-report=html

# Using coverage.py
coverage run -m pytest {test_path}
coverage report
coverage json
```

**2.2. Collect Coverage Metrics**

Capture:
- **Line coverage**: % of executable lines run
- **Branch coverage**: % of conditional branches taken
- **Function coverage**: % of functions called
- **Class coverage**: % of classes instantiated

**2.3. Analyze Uncovered Code**

For each uncovered section:
- Identify: file, function, line range
- Categorize: dead code, edge case, error path, or critical logic
- Assess criticality: high (business logic), medium (validation), low (logging)

### 3. Test Quality Assessment Phase

**3.1. Assertion Density**

Calculate assertions per test:
```
Assertion Density = Total Assertions / Total Tests
```

Targets:
- Unit tests: ≥ 1.5 assertions per test
- Integration tests: ≥ 2.0 assertions per test

**3.2. Test Independence**

Check for:
- Tests that depend on execution order
- Shared mutable state between tests
- Tests that fail when run in isolation
- Proper setup/teardown usage

**3.3. Test Naming and Documentation**

Validate:
- Test names describe what is being tested
- Test names follow convention: `test_<function>_<scenario>_<expected>`
- Complex tests have docstrings explaining purpose
- Test data is realistic and representative

**3.4. Edge Case Coverage**

For each public function, verify tests exist for:
- **Happy path**: Valid inputs, expected outputs
- **Boundary conditions**: Empty inputs, max values, min values
- **Invalid inputs**: Wrong types, malformed data, nulls
- **Error conditions**: Exceptions, failures, timeouts
- **State transitions**: Valid state changes for stateful code

### 4. TDD Compliance Check

**4.1. Test-First Evidence**

Look for indicators of TDD:
- Tests committed before or with implementation (git history)
- Test file timestamps vs implementation timestamps
- Presence of failing tests (red) before passing (green)

**4.2. Red-Green-Refactor Cycle**

Validate workflow:
- Tests were written first and initially failed
- Minimal code added to make tests pass
- Refactoring happened after tests passed

### 5. Gap Analysis Phase

**5.1. Identify Coverage Gaps**

List uncovered code with priority:

**Critical Gaps (must fix):**
- Uncovered business logic
- Error handling paths
- Security-sensitive code
- Data validation

**Medium Gaps (should fix):**
- Edge cases
- Boundary conditions
- State transitions

**Low Priority Gaps:**
- Logging statements
- Trivial getters/setters
- Defensive assertions

**5.2. Suggest Missing Tests**

For each gap, generate test suggestions:
```python
# Missing test for: add_task with empty description
def test_add_task_with_empty_description_raises_error():
    """Verify that adding a task with empty description raises ValueError."""
    # Arrange
    manager = TaskManager()

    # Act & Assert
    with pytest.raises(ValueError, match="Description cannot be empty"):
        manager.add_task("")
```

### 6. Reporting Phase

**6.1. Generate Coverage Report**

```markdown
# Test Coverage Report

**Target**: {target_path}
**Date**: {YYYY-MM-DD HH:MM}
**Analyzer**: QA Agent

## Summary

- **Overall Coverage**: X.Y% ({coverage_type})
- **Minimum Required**: {min_coverage}%
- **Status**: ✅ PASS | ❌ FAIL
- **Total Lines**: N
- **Covered Lines**: M
- **Missing Lines**: N-M

## Coverage by Module

| Module | Line % | Branch % | Functions | Status |
|--------|--------|----------|-----------|--------|
| src/todo.py | 92% | 87% | 12/13 | ✅ |
| src/cli.py | 78% | 70% | 8/10 | ⚠️ |
| src/utils.py | 100% | 100% | 5/5 | ✅ |

## Test Quality Metrics

- **Total Tests**: X
- **Assertion Density**: Y (target: ≥1.5)
- **Test Independence**: ✅ All tests isolated
- **Edge Case Coverage**: 85% (17/20 functions)

## Critical Coverage Gaps

### src/todo.py:42-48 (delete_task error handling)
- **Severity**: CRITICAL
- **Category**: Error Handling
- **Description**: Exception handling for non-existent task ID not tested
- **Suggested Test**:
  ```python
  def test_delete_nonexistent_task_raises_error():
      manager = TaskManager()
      with pytest.raises(KeyError):
          manager.delete_task(999)
  ```

## Medium Priority Gaps

[Similar format for medium priority]

## Low Priority Gaps

[Similar format for low priority]

## TDD Compliance

- ✅ Test files exist for all modules
- ⚠️ 2 functions implemented without prior tests
- ✅ Red-Green-Refactor evidence in git history

## Recommendations

1. Add tests for critical error paths in src/todo.py:42-48
2. Improve branch coverage in src/cli.py (currently 70%, target 80%)
3. Add edge case tests for task description validation
4. Document integration test scenarios in tests/README.md

## Detailed Coverage

{Link to HTML coverage report or inline detailed breakdown}
```

**6.2. Output Results**
- Save report to `history/qa/{feature_name}/test-coverage-{timestamp}.md`
- Generate HTML coverage report (if supported)
- Print summary to console
- Return structured data if `output_format=json`

## Output

**Success Case (Coverage ≥ min_coverage):**
- Coverage report with detailed metrics
- Console summary showing coverage percentage
- Exit code 0

**Warning Case (Coverage < min_coverage but ≥ fail_under):**
- Report with identified gaps
- Exit code 1

**Failure Case (Coverage < fail_under):**
- Comprehensive gap analysis
- Suggested tests for critical gaps
- Exit code 2

**Report Structure (JSON):**
```json
{
  "target": "src/",
  "timestamp": "2025-12-27T10:30:00Z",
  "coverage": {
    "line": 87.5,
    "branch": 82.3,
    "function": 92.0
  },
  "summary": {
    "total_lines": 500,
    "covered_lines": 437,
    "missing_lines": 63,
    "total_tests": 45,
    "assertion_density": 1.8
  },
  "modules": [
    {
      "name": "src/todo.py",
      "line_coverage": 92,
      "branch_coverage": 87,
      "functions_covered": 12,
      "functions_total": 13,
      "status": "pass"
    }
  ],
  "gaps": [
    {
      "file": "src/todo.py",
      "lines": "42-48",
      "severity": "critical",
      "category": "error_handling",
      "description": "Exception handling for non-existent task ID not tested",
      "suggested_test": "def test_delete_nonexistent_task..."
    }
  ],
  "tdd_compliance": {
    "has_tests": true,
    "test_first_percentage": 88,
    "red_green_refactor_evidence": true
  },
  "status": "pass",
  "recommendations": []
}
```

## Failure Handling

### Failure Scenario: No Tests Found
- **Cause**: Test directory doesn't exist or no test files match patterns
- **Action**: Report missing tests with suggested structure
- **Recovery**: Run `/sp.implement` with TDD enabled
- **Exit Code**: 7

### Failure Scenario: Tests Fail to Run
- **Cause**: Test execution errors, import failures, syntax errors
- **Action**: Display test failure output
- **Recovery**: Fix test errors and retry
- **Exit Code**: 8

### Failure Scenario: Coverage Tool Not Available
- **Cause**: pytest-cov or coverage.py not installed
- **Action**: Display installation instructions
- **Recovery**: Install coverage tools and retry
- **Exit Code**: 9

### Failure Scenario: Coverage Below Threshold
- **Cause**: Coverage percentage < fail_under threshold
- **Action**: Generate gap analysis report
- **Recovery**: Add tests for uncovered code
- **Exit Code**: 2

### Failure Scenario: Zero Assertions Detected
- **Cause**: Tests exist but have no assertions
- **Action**: Flag tests as ineffective
- **Recovery**: Add proper assertions to tests
- **Exit Code**: 10

### Failure Scenario: Test Interdependencies
- **Cause**: Tests fail when run in different order
- **Action**: Identify dependent tests and report
- **Recovery**: Refactor tests to be independent
- **Exit Code**: 11

## Determinism Guarantees

- Same code and tests produce same coverage metrics
- Consistent gap identification across runs
- Reproducible test quality assessments
- No random test selection

## Integration Points

- Works with pytest, unittest, and coverage.py
- Integrates with `/sp.implement` (TDD validation)
- Feeds into `/sp.git.commit_pr` (coverage gate)
- Compatible with CI/CD pipelines
- Reads constitution for coverage thresholds

## Quality Standards

This skill enforces:
- Minimum coverage thresholds (default 80%)
- Branch coverage over line coverage
- Edge case testing requirements
- TDD compliance verification
- Test quality metrics (assertion density, independence)

## Usage Example

```bash
# Analyze coverage for src directory
/qa.test-coverage --target src/

# Require 90% coverage
/qa.test-coverage --target src/ --min-coverage 90 --fail-under 90

# Generate HTML report
/qa.test-coverage --target src/ --output html

# Check branch coverage only
/qa.test-coverage --target src/ --coverage-type branch

# Include integration tests
/qa.test-coverage --target src/ --test-path tests/ --include-integration true
```

## Advanced Features

**Coverage Trends:**
- Compare coverage against previous runs
- Track coverage changes over time
- Alert on coverage regression

**Mutation Testing Integration:**
- Detect ineffective tests (tests that don't fail when code is mutated)
- Suggest stronger assertions

**Flaky Test Detection:**
- Run tests multiple times to identify non-deterministic tests
- Report intermittent failures
