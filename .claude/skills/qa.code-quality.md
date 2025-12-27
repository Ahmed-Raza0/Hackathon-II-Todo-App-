---
name: qa.code-quality
owner: QA Agent
category: Code Review
description: Perform automated and manual code quality review against constitution standards and Python best practices
version: 1.0.0
created: 2025-12-27
---

# QA Code Quality Review Skill

## Purpose

Evaluate code quality by checking adherence to project constitution principles, Python best practices, security standards, and maintainability criteria. This skill provides actionable feedback to ensure high-quality, production-ready code.

## When to Use

- After implementing new features or bug fixes
- Before creating pull requests
- During code review process
- When refactoring existing code
- After running `/sp.implement`

## Inputs

**Required:**
- `target_path` (path): File or directory to review (e.g., `src/` or `src/todo.py`)

**Optional:**
- `constitution_path` (path): Path to constitution.md (default: `.specify/memory/constitution.md`)
- `severity_threshold` (enum): Minimum severity to report - "info" | "warning" | "error" | "critical" (default: "warning")
- `output_format` (enum): Report format - "markdown" | "json" | "console" (default: "markdown")
- `auto_fix` (boolean): Attempt automatic fixes for violations (default: false)
- `focus_areas` (list): Specific areas to check - ["security", "style", "complexity", "documentation", "testing"] (default: all)

## Step-by-Step Process

### 1. Setup Phase

**1.1. Load Standards**
- Read constitution from `{constitution_path}`
- Extract code quality principles and constraints
- Load Python style guide (PEP 8, PEP 257)
- Initialize linting rules

**1.2. Discover Code Files**
- If `target_path` is a directory: find all `*.py` files recursively
- If `target_path` is a file: validate it exists and is Python
- Exclude virtual environments, `__pycache__`, `.git`, etc.

**1.3. Prepare Tools**
- Verify static analysis tools are available (pylint, flake8, bandit, mypy)
- Set up code complexity analyzer (radon, mccabe)
- Initialize security scanner (bandit for Python)

### 2. Automated Analysis Phase

**2.1. Static Code Analysis**

Run automated linters and capture results:

a. **Style Checking (flake8/pylint)**
   - PEP 8 compliance (line length, indentation, naming)
   - Code formatting consistency
   - Import organization
   - Whitespace usage

b. **Type Checking (mypy)**
   - Type hint coverage
   - Type consistency
   - Proper use of Optional, Union, etc.

c. **Security Scanning (bandit)**
   - SQL injection vulnerabilities
   - Command injection risks
   - Hardcoded secrets or credentials
   - Unsafe deserialization
   - Insecure random number generation

d. **Complexity Analysis (radon)**
   - Cyclomatic complexity per function
   - Maintainability index
   - Lines of code metrics
   - Nesting depth

**2.2. Parse and Categorize Issues**

For each detected issue:
- Extract: file, line, column, severity, rule code, message
- Categorize by focus area: security, style, complexity, etc.
- Filter by `severity_threshold`
- Group related issues

### 3. Manual Review Phase

**3.1. Constitution Compliance**

Check against constitution principles:

a. **Test Coverage Requirements**
   - Verify tests exist for new functions
   - Check for TDD evidence (tests before implementation)
   - Validate test quality (assertions, edge cases)

b. **Library-First Principle** (if applicable)
   - Ensure code is modular and reusable
   - Check for clear separation of concerns
   - Validate library interfaces

c. **Simplicity and YAGNI**
   - Identify over-engineering
   - Flag premature optimization
   - Check for unnecessary abstractions

d. **Error Handling**
   - Verify proper exception handling
   - Check for informative error messages
   - Validate error recovery paths

**3.2. Code Patterns Review**

Evaluate code patterns:

a. **Naming Conventions**
   - Functions: snake_case, verb phrases
   - Classes: PascalCase, noun phrases
   - Constants: UPPER_SNAKE_CASE
   - Variables: descriptive, not abbreviated

b. **Function Quality**
   - Single Responsibility Principle
   - Function length (< 50 lines recommended)
   - Parameter count (< 5 recommended)
   - Return type clarity

c. **Documentation**
   - Docstrings for public functions and classes
   - Complex logic has explanatory comments
   - README updated if public API changed

d. **Dependency Management**
   - No circular imports
   - Proper use of stdlib before third-party
   - Dependencies are necessary, not redundant

**3.3. Security Deep Dive**

Manual security checks:

- Input validation for user-provided data
- Output encoding to prevent injection
- Proper file path handling (no path traversal)
- Secrets not in source code (use environment variables)
- No eval(), exec(), or unsafe deserialization

### 4. Scoring and Prioritization

**4.1. Calculate Quality Score**

```
Quality Score = 100 - (
  critical_issues * 20 +
  error_issues * 10 +
  warning_issues * 2 +
  info_issues * 0.5
)
```

Minimum score: 0
Maximum score: 100

**4.2. Prioritize Issues**

Sort by:
1. Severity (critical > error > warning > info)
2. Impact (security > correctness > maintainability > style)
3. File frequency (issues affecting multiple files)

### 5. Reporting Phase

**5.1. Generate Report**

```markdown
# Code Quality Review Report

**Target**: {target_path}
**Date**: {YYYY-MM-DD HH:MM}
**Reviewer**: QA Agent
**Quality Score**: {score}/100

## Summary

- Critical Issues: X
- Errors: Y
- Warnings: Z
- Info: N

## Critical Issues (Action Required)

### {file_path}:{line}
- **Severity**: CRITICAL
- **Category**: Security | Correctness | ...
- **Rule**: {rule_code}
- **Message**: {description}
- **Fix**: {suggested_fix}

[Repeat for each critical issue]

## Errors

[Similar format]

## Warnings

[Similar format]

## Constitution Compliance

- ✅ Test coverage meets requirements
- ❌ Missing docstrings for public API
- ✅ No over-engineering detected

## Code Metrics

- Total Lines of Code: X
- Average Complexity: Y
- Maintainability Index: Z
- Type Hint Coverage: N%

## Recommendations

1. {Prioritized action item}
2. {Prioritized action item}
3. {Prioritized action item}

## Auto-Fix Suggestions

{If auto_fix=true, show fixable issues with diffs}
```

**5.2. Output Results**
- Save report to `history/qa/{feature_name}/code-quality-{timestamp}.md`
- Print summary to console
- Return structured data if `output_format=json`

## Output

**Success Case (Quality Score ≥ 80):**
- Code quality report with detailed findings
- Console summary showing score and issue counts
- Exit code 0

**Warning Case (60 ≤ Quality Score < 80):**
- Report with prioritized fixes
- Exit code 1

**Failure Case (Quality Score < 60):**
- Comprehensive report with critical issues highlighted
- Exit code 2

**Report Structure (JSON):**
```json
{
  "target": "src/todo.py",
  "timestamp": "2025-12-27T10:30:00Z",
  "quality_score": 85,
  "summary": {
    "critical": 0,
    "error": 2,
    "warning": 5,
    "info": 3
  },
  "issues": [
    {
      "file": "src/todo.py",
      "line": 42,
      "column": 10,
      "severity": "error",
      "category": "security",
      "rule": "B608",
      "message": "Possible SQL injection vector through string-based query construction",
      "suggestion": "Use parameterized queries"
    }
  ],
  "metrics": {
    "loc": 250,
    "avg_complexity": 3.2,
    "maintainability_index": 72,
    "type_coverage": 85
  },
  "constitution_compliance": {
    "test_coverage": true,
    "documentation": false,
    "simplicity": true
  },
  "recommendations": []
}
```

## Failure Handling

### Failure Scenario: Target Path Not Found
- **Cause**: Invalid `target_path` or file/directory doesn't exist
- **Action**: Display error with expected path
- **Recovery**: Verify path and retry
- **Exit Code**: 3

### Failure Scenario: No Python Files Found
- **Cause**: Target directory contains no `*.py` files
- **Action**: Warn user and suggest correct directory
- **Recovery**: Provide correct path
- **Exit Code**: 4

### Failure Scenario: Linting Tools Missing
- **Cause**: Required tools (flake8, bandit, etc.) not installed
- **Action**: List missing tools and installation commands
- **Recovery**: Install tools and retry
- **Exit Code**: 5

### Failure Scenario: Constitution Not Found
- **Cause**: Constitution file missing or invalid path
- **Action**: Warn and use default Python best practices only
- **Recovery**: Continue with reduced checks
- **Exit Code**: 0 (warning logged)

### Failure Scenario: Critical Security Issues
- **Cause**: Bandit detects high-severity vulnerabilities
- **Action**: Generate report with security issues highlighted
- **Recovery**: Fix issues and re-run
- **Exit Code**: 2

### Failure Scenario: Syntax Errors in Code
- **Cause**: Python files have syntax errors
- **Action**: Report syntax errors with file and line
- **Recovery**: Fix syntax and retry
- **Exit Code**: 6

## Determinism Guarantees

- Same code input produces same quality score and issues
- Consistent rule application across runs
- Reproducible metrics and analysis
- No time-dependent checks

## Integration Points

- Works with constitution.md for custom standards
- Integrates with `/sp.implement` workflow
- Feeds into `/sp.git.commit_pr` (quality gate)
- Compatible with CI/CD pipelines

## Quality Standards

This skill enforces:
- PEP 8 compliance (style)
- PEP 257 compliance (docstrings)
- OWASP Top 10 security checks
- Cyclomatic complexity < 10 per function
- Constitution-defined standards

## Usage Example

```bash
# Review entire src directory
/qa.code-quality --target src/

# Review specific file with auto-fix
/qa.code-quality --target src/todo.py --auto-fix true

# Security-focused review
/qa.code-quality --target src/ --focus security --severity critical

# Generate JSON report
/qa.code-quality --target src/ --output json
```

## Auto-Fix Capabilities

When `auto_fix=true`, automatically fix:
- Import sorting (isort)
- Code formatting (black)
- Trailing whitespace
- Missing newlines at end of file
- Simple PEP 8 violations

**Manual review required for:**
- Security vulnerabilities
- Logic errors
- Complex refactoring
- API changes
