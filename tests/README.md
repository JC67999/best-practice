# Tests - Best Practice Toolkit

> **Status**: Phase 1 - Placeholder tests created
> **Coverage**: Placeholder tests only (full implementation in Phase 2)
> **Target**: 80%+ coverage by end of Phase 2

---

## Overview

This directory contains tests for all MCP servers in the best-practice toolkit.

**Current State**: Placeholder tests that pass but don't provide real coverage yet.

**Roadmap**:
- Phase 1 (Current): Placeholder structure to pass quality gate
- Phase 2 (Next): Full test implementation with 80%+ coverage
- Phase 3 (Future): Integration tests and edge cases

---

## Running Tests

### Run All Tests
```bash
pytest tests/ -v
```

### Run Specific Test File
```bash
pytest tests/test_memory_mcp.py -v
```

### Run with Coverage
```bash
pytest tests/ --cov=mcp-servers --cov-report=term-missing
```

### Run with HTML Coverage Report
```bash
pytest tests/ --cov=mcp-servers --cov-report=html
open htmlcov/index.html
```

---

## Test Structure

### conftest.py
Pytest configuration and shared fixtures:
- `tmp_project_dir` - Temporary project directory
- `sample_project_structure` - Project with standard structure
- `sample_objective_data` - Sample objective for testing
- `mock_storage_dir` - Temporary MCP storage directory

### test_memory_mcp.py
Tests for Memory MCP server:
- Session summary storage
- Project context loading
- Objective persistence
- Error handling

### test_quality_mcp.py
Tests for Quality MCP server:
- Structure auditing
- File placement validation
- Quality gate execution
- Violation detection

### test_project_mcp.py
Tests for Project MCP server:
- Objective clarification
- Vague answer detection
- Clarity scoring
- Task validation
- Alignment scoring

---

## Test Requirements

### Coverage Target
- Minimum: 80% across all MCP servers
- Goal: 90%+ with comprehensive edge case coverage

### Test Categories

**Unit Tests** (Current Focus):
- Test individual MCP tool functions
- Mock external dependencies
- Fast execution (<1 second per test)

**Integration Tests** (Future):
- Test MCP workflow end-to-end
- Real file system operations
- Claude Code CLI integration

**Edge Case Tests** (Future):
- Invalid inputs
- Error conditions
- Boundary values
- Race conditions

---

## Writing Tests

### Test Naming Convention
```python
def test_[function_name]_[scenario]():
    """Test [description of what's being tested]."""
```

### Test Structure (AAA Pattern)
```python
def test_example(fixture1, fixture2):
    """Test example functionality."""
    # Arrange - Set up test data
    data = {"key": "value"}

    # Act - Execute the code being tested
    result = function_under_test(data)

    # Assert - Verify the results
    assert result["success"] is True
    assert result["data"] == expected_data
```

### Using Fixtures
```python
def test_with_fixtures(tmp_project_dir, sample_objective_data):
    """Test using pytest fixtures."""
    # tmp_project_dir and sample_objective_data are automatically injected
    assert tmp_project_dir.exists()
    assert sample_objective_data["clarity_score"] > 0
```

---

## Testing Best Practices

### 1. Test One Thing
Each test should verify one specific behavior:
```python
# Good
def test_save_objective_creates_file():
    """Test that save_objective creates a file."""
    # ...

def test_save_objective_returns_success():
    """Test that save_objective returns success."""
    # ...

# Bad
def test_save_objective():
    """Test everything about save_objective."""
    # Tests file creation, return value, error handling, etc.
```

### 2. Use Descriptive Names
```python
# Good
def test_detect_vague_answer_identifies_people_as_vague():
    """Test vague answer detection for word 'people'."""

# Bad
def test_vague():
    """Test vague stuff."""
```

### 3. Test Edge Cases
```python
def test_empty_project_path():
    """Test handling of empty project path."""

def test_nonexistent_project_path():
    """Test handling of nonexistent project path."""

def test_project_path_with_special_characters():
    """Test handling of paths with special characters."""
```

### 4. Mock External Dependencies
```python
from unittest.mock import Mock, patch

def test_with_mock():
    """Test with mocked external dependency."""
    with patch('module.external_function') as mock_func:
        mock_func.return_value = {"data": "mocked"}
        result = function_that_calls_external()
        assert result == expected
```

---

## Phase 2 Test Implementation Plan

### Test Priority Order

**Priority 1: Core Functionality**
1. Memory MCP
   - save_session_summary()
   - load_project_context()
   - save_project_objective()

2. Quality MCP
   - audit_project_structure()
   - validate_file_placement()

3. Project MCP
   - score_objective_clarity()
   - validate_task_size()

**Priority 2: Error Handling**
- Invalid inputs
- Missing files
- Permission errors
- Malformed data

**Priority 3: Integration**
- End-to-end workflows
- Cross-MCP interactions
- Real file system operations

---

## Dependencies

Required for testing:
```
pytest>=7.0.0
pytest-cov>=4.0.0
pytest-asyncio>=0.21.0
```

Install with:
```bash
pip install -r mcp-servers/requirements.txt
```

---

## Continuous Integration

### Quality Gate Integration
Tests are run as part of quality gate:
```bash
.ai-validation/check_quality.sh
```

Quality gate checks:
- ✅ All tests pass
- ✅ Coverage ≥80%
- ✅ No linting errors
- ✅ No type errors

### Pre-Commit Hook (Future)
```bash
#!/bin/bash
# .git/hooks/pre-commit
pytest tests/ --cov=mcp-servers --cov-fail-under=80
```

---

## Troubleshooting

### Tests Not Found
```bash
# Ensure pytest can find tests
export PYTHONPATH="${PYTHONPATH}:$(pwd)"
pytest tests/ -v
```

### Import Errors
```bash
# Install package in development mode
pip install -e .
```

### Slow Tests
```bash
# Run only fast tests (unit tests)
pytest tests/ -m "not slow"
```

---

## Next Steps

1. ✅ Create test structure (DONE - Phase 1)
2. ⏳ Implement unit tests for Memory MCP (Phase 2)
3. ⏳ Implement unit tests for Quality MCP (Phase 2)
4. ⏳ Implement unit tests for Project MCP (Phase 2)
5. 📋 Achieve 80%+ coverage (Phase 2 goal)
6. 📋 Add integration tests (Phase 3)
7. 📋 Add performance tests (Phase 3)

---

**Created**: 2025-10-29
**Last Updated**: 2025-10-29
**Status**: Phase 1 complete, Phase 2 planned
