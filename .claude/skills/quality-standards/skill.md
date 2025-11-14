---
name: Quality Standards
description: Code quality, testing, and documentation standards enforcement
tags: quality, testing, coverage, lint, documentation, pre-commit
auto_load_triggers: test, quality, coverage, lint, commit, checklist
priority: toolkit
---

# Quality Standards

## Purpose

Enforces code quality, test coverage, and documentation standards to ensure maintainable, reliable code. Defines mandatory pre-commit checks and quality gates.

---

## Testing Requirements

### Test Coverage

**Minimum Coverage**: 80% across all code

**Required Tests**:
- Unit tests for all MCP tool functions
- Integration tests for MCP workflows
- Edge case tests (error handling, invalid input)
- Regression tests for fixed bugs

### Test Structure

Use pytest with clear, descriptive test classes and methods:

```python
# tests/test_memory_mcp.py
import pytest
from mcp_servers.memory_mcp import MemoryMCP

class TestMemoryMCP:
    """Tests for Memory MCP server."""

    def test_save_session_summary(self, tmp_path):
        """Test saving session summary."""
        mcp = MemoryMCP(storage_dir=tmp_path)
        result = mcp.save_session_summary(
            project_path="/test/project",
            summary="Test summary"
        )
        assert result["success"] is True

    def test_invalid_project_path(self, tmp_path):
        """Test error handling for invalid paths."""
        mcp = MemoryMCP(storage_dir=tmp_path)
        with pytest.raises(ValueError):
            mcp.save_session_summary(
                project_path="",
                summary="Test"
            )
```

### Running Tests

```bash
# Run all tests
pytest tests/ -v --cov=mcp-servers --cov-report=term-missing

# Run specific test file
pytest tests/test_memory_mcp.py -v

# Run with coverage report
pytest --cov=mcp-servers --cov-report=html
```

---

## Code Quality Tools

### Linting - Ruff

**Check for linting issues**:
```bash
ruff check mcp-servers/
```

**Auto-fix issues**:
```bash
ruff check --fix mcp-servers/
```

**Configuration** (pyproject.toml or ruff.toml):
```toml
[tool.ruff]
line-length = 100
target-version = "py310"
select = ["E", "F", "W", "I", "N"]
```

### Type Checking - Mypy

**Check types**:
```bash
mypy mcp-servers/
```

**Configuration** (pyproject.toml):
```toml
[tool.mypy]
python_version = "3.10"
strict = true
warn_return_any = true
warn_unused_configs = true
```

### Security - Bandit

**Check for security issues**:
```bash
bandit -r mcp-servers/
```

---

## Code Style

### Python Standards

**Type Hints Required**:
```python
def process_data(
    data: Dict[str, any],
    options: Optional[List[str]] = None
) -> Dict[str, bool]:
    """Process data with optional filters."""
    # Implementation
```

**Docstrings Required**:
- All public functions must have docstrings
- Include Args, Returns, Raises sections
- Add usage examples for complex functions

**Function Length**:
- Maximum 50 lines per function
- If longer, break into smaller functions
- Each function should do ONE thing

**Line Length**:
- Maximum 100 characters
- Break long lines at logical points

---

## Pre-Commit Checklist

**Before committing ANY code, verify**:

- [ ] All tests pass (`pytest tests/ -v`)
- [ ] No linting errors (`ruff check mcp-servers/`)
- [ ] No type errors (`mypy mcp-servers/`)
- [ ] No security issues (`bandit -r mcp-servers/`)
- [ ] Structure compliance (≤5 root folders)
- [ ] Documentation updated (if API changed)
- [ ] PROJECT_PLAN.md updated (if status changed)
- [ ] Commit message follows format
- [ ] Changes are ≤30 lines (or checkpointed)

---

## Quality Gate

**MANDATORY before any commit**:

```bash
# Run quality gate script
bash .ai-validation/check_quality.sh
```

**Must see**:
- ✅ All tests pass
- ✅ No linting errors
- ✅ No type errors
- ✅ No security issues
- ✅ Structure compliance

**If quality gate FAILS**:
- DO NOT commit
- Fix all issues
- Re-run quality gate
- Repeat until PASS

**NEVER override quality gate failure** - if it fails, fix the issues.

---

## Success Metrics

Track these metrics to ensure quality:

**Code Quality**:
- Test coverage ≥80%
- Zero linting errors
- Zero type errors
- Zero security vulnerabilities

**Structure**:
- Root folders ≤5
- All docs in docs/
- No forbidden files in root

**Process**:
- Commit frequency (daily minimum)
- Quality gate pass rate (target: 100%)
- Task size compliance (≤30 lines)

---

## Documentation Standards

### Code Documentation

**All public functions require docstrings**:

```python
def save_project_objective(
    self,
    project_path: str,
    objective_data: Dict
) -> Dict:
    """Save project objective to persistent storage.

    Args:
        project_path: Absolute path to project directory
        objective_data: Dictionary containing:
            - problem: Problem statement
            - target_users: Target user description
            - solution: Solution description
            - success_metrics: List of success metrics
            - constraints: List of constraints
            - clarity_score: Score 0-100

    Returns:
        Dictionary containing:
            - success: Boolean indicating if save succeeded
            - message: Human-readable status message
            - clarity_score: The saved clarity score

    Raises:
        ValueError: If project_path is empty or invalid
        IOError: If unable to write to storage

    Example:
        >>> mcp = MemoryMCP()
        >>> result = mcp.save_project_objective(
        ...     "/path/to/project",
        ...     {"problem": "...", "clarity_score": 85}
        ... )
        >>> assert result["success"] is True
    """
    # Implementation
```

### Markdown Documentation

**All markdown files require**:
- Title (# heading)
- Brief purpose/description at top
- Table of contents for files >200 lines
- Clear section headings
- Code examples where applicable
- Last updated date

---

## Integration with MCP

**Quality MCP Tools**:

Before any commit, call:
```
mcp__quality__run_quality_gate
Args:
  project_path = current working directory
  changes_made = list of files modified
```

**Interpret results**:
- **PASS**: All checks passed → Proceed to commit
- **FAIL**: Quality issues detected → Fix issues, re-run

**Other Quality MCP Tools**:
- `check_code_quality` - Check specific files
- `audit_project_structure` - Validate minimal root
- `validate_file_placement` - Check files in correct locations
- `verify_standards` - Comprehensive standards check

---

## Resources

- **CLAUDE.md**: Full project standards (sections: Testing Requirements, Code Quality Tools, Pre-Commit Checklist)
- **quality_mcp.py**: Quality enforcement MCP server
- **.ai-validation/check_quality.sh**: Quality gate script
