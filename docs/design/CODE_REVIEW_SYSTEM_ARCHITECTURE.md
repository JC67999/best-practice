# Code Review Self-Improvement System

> **Purpose**: Continuous automated code review for constant project improvement
> **Status**: Design Phase
> **Last Updated**: 2025-10-29

---

## Overview

The Code Review System automatically analyzes project code to find bugs, inconsistencies, and improvement opportunities. All findings are added to PROJECT_PLAN.md as prioritized tasks, encouraging constant self-improvement.

## Goals

1. **Continuous Quality**: Regular automated code reviews
2. **Proactive Improvement**: Find issues before they become problems
3. **Learning Loop**: Discoveries feed back into best practices
4. **Actionable Tasks**: Auto-generate prioritized todo items

## Architecture

### Components

#### 1. Code Review Tool (`learning_mcp.py`)

**New MCP Tool**: `review_code`

```python
def review_code(
    project_path: str,
    file_patterns: list = ["*.py", "*.js", "*.ts"],
    review_type: str = "incremental"  # or "full"
) -> dict:
    """
    Review project code for issues.

    Returns:
        {
            "success": true,
            "findings": [
                {
                    "file": "src/module.py",
                    "line": 42,
                    "category": "bug|inconsistency|improvement|tech_debt",
                    "severity": "critical|high|medium|low",
                    "title": "Potential null pointer exception",
                    "description": "Variable 'data' not checked before access",
                    "suggested_fix": "Add null check before line 42",
                    "priority": "CRITICAL"
                }
            ],
            "summary": {
                "total_findings": 15,
                "critical": 2,
                "high": 5,
                "medium": 6,
                "low": 2
            }
        }
    """
```

#### 2. Review Daemon (`code_review_daemon.py`)

**Purpose**: Scheduled code reviews

**Features**:
- Incremental review (changed files only)
- Full codebase review (monthly)
- Respects .gitignore
- Configurable schedule
- Session logging

#### 3. PROJECT_PLAN.md Integration

**Auto-generates tasks** in appropriate section:

```markdown
### Code Review Findings - 2025-10-29

→ **[review_critical_1]** Fix null pointer in src/module.py:42
  - Priority: CRITICAL
  - Category: Bug
  - File: src/module.py:42
  - Description: Variable 'data' not checked before access
  - Suggested fix: Add null check before line 42
  - Auto-generated: 2025-10-29

→ **[review_high_1]** Inconsistent naming in api_handler.py
  - Priority: HIGH
  - Category: Inconsistency
  - ...
```

## Review Categories

### 1. Bugs (CRITICAL/HIGH Priority)

**Detected Issues**:
- Null/undefined access without checks
- Uncaught exceptions
- Logic errors (if/else branches)
- Off-by-one errors in loops
- Resource leaks (file handles, connections)
- Race conditions
- Infinite loops

**Detection Methods**:
- Static analysis patterns
- Common bug patterns
- Exception handling gaps
- Edge case analysis

### 2. Inconsistencies (HIGH/MEDIUM Priority)

**Detected Issues**:
- Naming convention violations
- Code style inconsistencies
- API design inconsistencies
- Error handling patterns vary
- Documentation format varies
- Test structure inconsistencies

**Detection Methods**:
- Compare against CLAUDE.md standards
- Analyze existing patterns
- Check naming conventions
- Review API consistency

### 3. Improvements (MEDIUM/LOW Priority)

**Detected Issues**:
- Complex functions (>50 lines)
- High cyclomatic complexity
- Duplicate code
- Missing type hints
- Missing docstrings
- Performance bottlenecks
- Readability issues

**Detection Methods**:
- Complexity metrics
- Duplicate detection
- Documentation coverage
- Type hint coverage

### 4. Tech Debt (LOW Priority)

**Detected Issues**:
- TODO comments
- Deprecated API usage
- Commented-out code
- Temporary hacks/workarounds
- Old dependencies
- Dead code

**Detection Methods**:
- Search for TODO/FIXME/HACK
- Check for deprecated patterns
- Detect commented code
- Unused import detection

## Priority Assignment

### Automatic Prioritization

```python
def assign_priority(finding: dict) -> str:
    """Assign priority based on category and severity."""

    if finding["category"] == "bug":
        if finding["severity"] == "critical":
            return "CRITICAL"
        elif finding["severity"] == "high":
            return "HIGH"
        else:
            return "MEDIUM"

    elif finding["category"] == "inconsistency":
        if finding["impact"] == "functionality":
            return "HIGH"
        else:
            return "MEDIUM"

    elif finding["category"] == "improvement":
        return "MEDIUM"

    elif finding["category"] == "tech_debt":
        return "LOW"

    return "MEDIUM"  # default
```

### Priority Definitions

- **CRITICAL**: Bugs that could cause crashes, data loss, security issues
- **HIGH**: Bugs affecting functionality, major inconsistencies
- **MEDIUM**: Code improvements, refactoring opportunities
- **LOW**: Minor style issues, tech debt cleanup

## Review Strategies

### 1. Incremental Review (Daily)

**Scope**: Changed files since last review

```python
def incremental_review(project_path: str) -> dict:
    """Review only changed files."""

    # Get changed files from git
    changed_files = git.get_changed_files(since_last_review=True)

    # Review each file
    findings = []
    for file in changed_files:
        findings.extend(review_file(file))

    return findings
```

**Triggers**:
- After git commit
- Daily at configured time
- On demand via MCP tool

### 2. Full Review (Weekly/Monthly)

**Scope**: Entire codebase

```python
def full_review(project_path: str) -> dict:
    """Review entire codebase."""

    # Get all source files
    files = glob_source_files(project_path)

    # Review each file
    findings = []
    for file in files:
        findings.extend(review_file(file))

    # Deduplicate and prioritize
    return deduplicate_findings(findings)
```

**Triggers**:
- Weekly (configurable)
- Before major releases
- On demand via MCP tool

### 3. Focused Review (On Demand)

**Scope**: Specific files or modules

```python
def focused_review(
    project_path: str,
    files: list[str] = None,
    modules: list[str] = None
) -> dict:
    """Review specific files or modules."""

    target_files = resolve_targets(files, modules)

    findings = []
    for file in target_files:
        findings.extend(review_file(file))

    return findings
```

**Triggers**:
- User request
- After major refactoring
- Before code review meeting

## Integration Workflow

### 1. Review Execution

```
1. Daemon triggers (schedule or manual)
   ↓
2. Select review strategy (incremental/full/focused)
   ↓
3. Analyze files for issues
   ↓
4. Categorize and prioritize findings
   ↓
5. Generate task descriptions
   ↓
6. Add to PROJECT_PLAN.md
   ↓
7. Create review report
```

### 2. Task Generation

```python
def generate_tasks(findings: list[dict]) -> list[dict]:
    """Convert findings to PROJECT_PLAN.md tasks."""

    tasks = []
    for finding in findings:
        task = {
            "id": f"review_{finding['category']}_{finding['id']}",
            "title": finding["title"],
            "priority": finding["priority"],
            "category": finding["category"],
            "file": finding["file"],
            "line": finding["line"],
            "description": finding["description"],
            "suggested_fix": finding["suggested_fix"],
            "auto_generated": datetime.now().isoformat()
        }
        tasks.append(task)

    return tasks
```

### 3. PROJECT_PLAN.md Update

```python
def add_tasks_to_plan(project_path: str, tasks: list[dict]):
    """Add review findings to PROJECT_PLAN.md."""

    plan_path = Path(project_path) / "docs/notes/PROJECT_PLAN.md"

    # Read existing plan
    content = plan_path.read_text()

    # Find or create "Code Review Findings" section
    section = find_or_create_section(content, "Code Review Findings")

    # Add tasks by priority
    for task in sorted(tasks, key=lambda t: priority_order(t["priority"])):
        section.add_task(task)

    # Write back
    plan_path.write_text(content)
```

## Configuration

### Default Configuration

```json
{
    "review_schedule": {
        "incremental": "daily",
        "full": "weekly"
    },
    "file_patterns": ["*.py", "*.js", "*.ts"],
    "exclude_patterns": [
        "*/node_modules/*",
        "*/venv/*",
        "*/.venv/*",
        "*/dist/*",
        "*/build/*"
    ],
    "priorities": {
        "bug_critical": "CRITICAL",
        "bug_high": "HIGH",
        "inconsistency": "MEDIUM",
        "improvement": "LOW"
    },
    "max_findings_per_run": 50,
    "auto_add_to_plan": true
}
```

## Review Patterns

### Python Patterns

```python
PYTHON_PATTERNS = {
    "null_check": {
        "pattern": r"(\w+)\[\w+\]|\(\w+\)\.",
        "check": "variable_checked_before_access",
        "severity": "high",
        "message": "Potential null/undefined access"
    },
    "exception_handling": {
        "pattern": r"^(?!.*try:).*open\(|.*request\.",
        "check": "wrapped_in_try_except",
        "severity": "medium",
        "message": "I/O operation without exception handling"
    },
    "long_function": {
        "check": "function_length > 50",
        "severity": "low",
        "message": "Function exceeds 50 lines (consider refactoring)"
    }
}
```

### JavaScript/TypeScript Patterns

```javascript
JS_PATTERNS = {
    "async_no_await": {
        "pattern": r"async\s+\w+.*\{[^}]*\}",
        "check": "contains_await",
        "severity": "medium",
        "message": "Async function without await"
    },
    "console_log": {
        "pattern": r"console\.log\(",
        "severity": "low",
        "message": "Debug console.log should be removed"
    }
}
```

## Success Metrics

### Review Quality

- **Accuracy**: >90% of findings are valid issues
- **False positive rate**: <10%
- **Coverage**: >80% of actual issues detected
- **Actionable**: >85% of findings result in code changes

### Impact

- **Bug prevention**: Bugs found before production
- **Code quality**: Measurable improvement in quality scores
- **Tech debt**: Reduction in TODO/FIXME comments
- **Consistency**: Improved style consistency scores

### Adoption

- **Task completion**: >70% of generated tasks completed
- **User satisfaction**: Findings perceived as helpful
- **Time saved**: Reduced manual code review time

## Example Output

### Review Report

```markdown
# Code Review Report - 2025-10-29

## Summary
- Files reviewed: 47
- Findings: 23
- Critical: 2
- High: 7
- Medium: 10
- Low: 4

## Critical Issues (2)

### src/api/handler.py:142
**Potential null pointer exception**
- Variable 'response' not checked before access
- Could cause crash if API call fails
- Suggested fix: Add null check at line 141

### src/db/connection.py:78
**Database connection not closed**
- Resource leak in error path
- Connection pool exhaustion risk
- Suggested fix: Use context manager or add finally block

## High Priority Issues (7)
...

## Tasks Added to PROJECT_PLAN.md
- 23 tasks added
- 2 CRITICAL priority
- 7 HIGH priority
- 10 MEDIUM priority
- 4 LOW priority
```

---

**Status**: Design complete, ready for implementation
**Next**: Implement review_code tool in learning_mcp.py
