# Project Standards - Best Practice Toolkit

> **Purpose**: Standards and guidelines for AI-assisted development of this project
> **Last Updated**: 2025-10-29
> **Applies To**: Claude Code and all AI assistants working on this codebase

---

## 📋 Project Overview

**Project**: Best Practice Toolkit for AI-Assisted Development
**Type**: MCP server system + retrofit methodology
**Language**: Python 3.10+
**License**: MIT

**Objective**: Enforce excellent coding practices and project delivery through mandatory objective clarification, quality gates, and minimal root structure.

**Key Principle**: We practice what we preach - this project uses its own best practices.

---

## 📁 File Placement Rules

### Root Directory - MINIMAL (Target: ≤5 folders, ≤5 files)

**Allowed Folders** (5 maximum):
```
/mcp-servers/     - MCP server implementations
/tests/           - Test suite for all code
/docs/            - ALL documentation
/dist/            - Distribution packages (generated)
/retrofit-tools/  - Retrofit assessment scripts
```

**Allowed Files** (keep minimal):
```
/README.md        - Brief project overview (link to docs/)
/CLAUDE.md        - This file (project standards)
/package_toolkit.sh - Build script
/.gitignore       - Git ignore rules
/LICENSE          - MIT license (generated)
```

**FORBIDDEN in Root**:
- ❌ Documentation files (*.md except README.md and CLAUDE.md)
- ❌ Configuration files (move to .config/ or appropriate subdir)
- ❌ Data files (move to docs/references/ or artifacts/)
- ❌ Log files (use /logs if needed, add to .gitignore)
- ❌ Temporary files (use /temp if needed, add to .gitignore)

### Documentation Structure

**ALL documentation goes in `/docs/`**:
```
/docs/
├── README.md                    - Comprehensive documentation index
├── design/                      - Architecture and system design
│   ├── MCP_IMPLEMENTATION_APPROACH.md
│   └── CSO_FRAMEWORK_INTEGRATION.md
├── guides/                      - How-to guides and methodology
│   ├── RETROFIT_METHODOLOGY.md
│   └── AUTONOMOUS_MODE_ROADMAP.md
├── analysis/                    - Assessments and analysis
│   ├── DELIVERY_SUMMARY.md
│   ├── AUTONOMOUS_TOOLS_ANALYSIS.md
│   └── PROJECT_RETROFIT_ASSESSMENT.md
├── references/                  - Reference materials and examples
│   └── [input reference files]/
└── notes/                       - Planning and status
    └── PROJECT_PLAN.md          - Current project plan (ALWAYS CURRENT)
```

### Source Code Structure

**MCP Servers** (`/mcp-servers/`):
```
/mcp-servers/
├── memory_mcp.py       - Context persistence MCP
├── quality_mcp.py      - Quality enforcement MCP
├── project_mcp.py      - Objective clarification MCP
├── requirements.txt    - Python dependencies
└── README.md           - Installation and usage
```

**Tests** (`/tests/`):
```
/tests/
├── test_memory_mcp.py
├── test_quality_mcp.py
├── test_project_mcp.py
├── conftest.py         - Pytest configuration
└── README.md           - Testing documentation
```

### Hidden Directories

**Configuration**:
```
/.claude/            - Claude Code configuration
/.ai-validation/     - Quality gate scripts
/.git/               - Git repository
```

---

## 🎯 Development Workflow

### Starting Work

**1. Load Context**
```bash
# Always read these files first:
docs/notes/PROJECT_PLAN.md     # Current objectives and tasks
CLAUDE.md                       # This file (standards)
docs/README.md                  # System overview
```

**2. Check Current Phase**
Review PROJECT_PLAN.md → Current Sprint section to understand current work.

**3. Select Model**
- **Planning tasks** (architecture, breaking down features) → Use max mode
- **Implementation tasks** (writing code, tests, docs) → Use standard mode

### Working on Tasks

**Task Size Limits**:
- ≤30 lines of implementation per task
- ≤30 minutes to complete
- Must have clear acceptance criteria

**If task feels too large**:
1. STOP - Don't implement
2. Break down into smaller sub-tasks
3. Update PROJECT_PLAN.md with sub-tasks
4. Complete each sub-task independently

**Commit Frequency**:
- After EVERY passing quality gate
- After EVERY small task completion
- Before attempting risky changes
- At EVERY checkpoint in refactoring

### Quality Standards

**MANDATORY Before Any Commit**:
```bash
# Run quality gate
cd .ai-validation && bash check_quality.sh

# Must see:
# ✅ All tests pass
# ✅ No linting errors
# ✅ No type errors
# ✅ No security issues
# ✅ Structure compliance
```

**Coverage Requirements**:
- Minimum 80% test coverage
- All new functions must have tests
- All edge cases must be tested

**Code Style**:
- Follow PEP 8 (enforced by ruff)
- Type hints required (checked by mypy)
- Docstrings required for all public functions
- Comments for complex logic only

### Error Recovery - Delete and Reroll Pattern

**If debugging spiral detected** (3+ failed attempts on same issue):

```bash
# STOP - You're stuck
git log --oneline -5           # Find last working commit
git reset --hard <commit_hash> # Revert to working state
git clean -fd                  # Remove untracked files
```

**Then**:
1. Break task into smaller pieces
2. Ensure each piece is testable
3. Complete smallest piece first
4. Test and commit before proceeding

### Refactoring - Checkpoint Pattern

**Never refactor >30 lines at once**. Use checkpoints:

```markdown
## Refactor Plan: [Description]

Checkpoint 1: Extract function signatures (no implementation)
- Validation: All tests still pass
- Rollback point: YES

Checkpoint 2: Move functions to new module
- Validation: Import statements work, tests pass
- Rollback point: YES

Checkpoint 3: Update implementations
- Validation: All tests pass with new logic
- Rollback point: YES
```

**Workflow**:
1. Define target architecture
2. Break into checkpoints (each ≤30 lines)
3. For each checkpoint:
   - Implement
   - Run tests
   - PASS → Commit → Proceed
   - FAIL → Rollback checkpoint → Retry smaller

---

## 🧪 Testing Requirements

### Test Coverage

**Minimum Coverage**: 80% across all code

**Required Tests**:
- Unit tests for all MCP tool functions
- Integration tests for MCP workflows
- Edge case tests (error handling, invalid input)
- Regression tests for fixed bugs

### Test Structure

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

## 🔍 Code Quality Tools

### Linting - Ruff

```bash
# Check for linting issues
ruff check mcp-servers/

# Auto-fix issues
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

```bash
# Check types
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

```bash
# Check for security issues
bandit -r mcp-servers/
```

---

## 🏗️ Architecture Conventions

### MCP Server Structure

**All MCP servers follow this pattern**:

```python
"""
MCP Server: [Name]
Purpose: [Brief description]
"""
from typing import Dict, List, Optional
import asyncio

class [Name]MCP:
    """[Name] MCP server."""

    def __init__(self, config: Optional[Dict] = None):
        """Initialize MCP server."""
        self.config = config or {}

    async def handle_tool_call(
        self,
        tool_name: str,
        arguments: Dict
    ) -> Dict:
        """Handle MCP tool calls."""
        handlers = {
            "tool_name": self._handle_tool_name,
        }

        handler = handlers.get(tool_name)
        if not handler:
            return {
                "error": f"Unknown tool: {tool_name}",
                "success": False
            }

        return await handler(arguments)

    async def _handle_tool_name(self, args: Dict) -> Dict:
        """Handle specific tool."""
        # Implementation
        return {"success": True, "data": {}}
```

### Naming Conventions

**Files**:
- MCP servers: `[name]_mcp.py` (e.g., `memory_mcp.py`)
- Tests: `test_[name]_mcp.py` (e.g., `test_memory_mcp.py`)
- Scripts: `[action]_[object].py` (e.g., `retrofit_assess.py`)

**Classes**:
- PascalCase: `MemoryMCP`, `QualityGate`, `ObjectiveClarifier`

**Functions**:
- snake_case: `save_session_summary`, `run_quality_gate`

**Constants**:
- UPPER_SNAKE: `MAX_RETRIES`, `DEFAULT_STORAGE_DIR`

**Variables**:
- snake_case: `project_path`, `clarity_score`

### Error Handling

**Always use try-except with logging**:

```python
import logging

logger = logging.getLogger(__name__)

async def risky_operation(self, data: Dict) -> Dict:
    """Perform operation that might fail."""
    try:
        result = await self._process(data)
        return {"success": True, "result": result}

    except ValueError as e:
        logger.error(f"Invalid data: {e}")
        return {
            "success": False,
            "error": f"Invalid data: {str(e)}",
            "error_type": "validation"
        }

    except Exception as e:
        logger.exception("Unexpected error")
        return {
            "success": False,
            "error": f"Unexpected error: {str(e)}",
            "error_type": "internal"
        }
```

---

## 📝 Documentation Standards

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

## 🔄 Git Workflow

### Branch Strategy

**Main branches**:
- `main` - Production-ready code only
- `develop` - Integration branch for features

**Feature branches**:
- `feature/[name]` - New features
- `fix/[name]` - Bug fixes
- `refactor/[name]` - Refactoring work
- `docs/[name]` - Documentation updates

### Commit Messages

**Format**:
```
[type]: [description]

[optional body]

[optional footer]
```

**Types**:
- `feat` - New feature
- `fix` - Bug fix
- `refactor` - Code refactoring
- `test` - Adding tests
- `docs` - Documentation changes
- `chore` - Build/config changes

**Examples**:
```
feat: add autonomous daemon to project MCP

Implements safe autonomous execution with quality gate enforcement
and auto-rollback on failure.

Closes #42
```

```
fix: handle null project path in memory MCP

Added validation to reject empty project paths before attempting
to save data.

Fixes #38
```

### Commit Frequency

**Commit after**:
- Every passing quality gate
- Every completed task (≤30 lines)
- Every refactor checkpoint
- Before risky changes

**Never commit**:
- Failing tests
- Linting errors
- Type errors
- Without running quality gate

---

## 🎨 Code Style Guide

### Python Style

**Imports**:
```python
# Standard library
import os
import sys
from typing import Dict, List, Optional

# Third-party
import pytest
from anthropic import Anthropic

# Local
from mcp_servers.memory_mcp import MemoryMCP
```

**Function Length**:
- Maximum 50 lines per function
- If longer, break into smaller functions
- Each function should do ONE thing

**Line Length**:
- Maximum 100 characters
- Break long lines at logical points

**Type Hints**:
```python
# Always use type hints
def process_data(
    data: Dict[str, any],
    options: Optional[List[str]] = None
) -> Dict[str, bool]:
    """Process data with optional filters."""
    # Implementation
```

---

## 🚀 Building and Distribution

### Building Package

```bash
# Run packaging script
./package_toolkit.sh

# Creates:
# dist/best-practice-toolkit-v1.0.0.tar.gz
# dist/best-practice-toolkit-v1.0.0.zip
```

### Version Management

**Version format**: MAJOR.MINOR.PATCH (semantic versioning)

**Version increments**:
- MAJOR: Breaking changes
- MINOR: New features (backward compatible)
- PATCH: Bug fixes

**Current version**: 1.0.0 (stored in package_toolkit.sh)

---

## ⚡ Performance Guidelines

### MCP Tool Calls

**Target**: <100ms per tool call

**Optimization strategies**:
- Cache frequently accessed data
- Use async operations for I/O
- Minimize file system operations
- Batch operations when possible

### Quality Gate Execution

**Target**: <5 seconds for full quality gate

**Parallelization**:
```bash
# Run checks in parallel
pytest & \
ruff check & \
mypy & \
bandit -r mcp-servers/ &
wait
```

---

## 🔐 Security Considerations

### Secrets Management

**Never commit**:
- API keys
- Passwords
- Tokens
- Private keys

**Use environment variables**:
```python
import os

API_KEY = os.getenv("ANTHROPIC_API_KEY")
if not API_KEY:
    raise ValueError("ANTHROPIC_API_KEY not set")
```

### Input Validation

**Always validate user input**:
```python
def validate_project_path(path: str) -> bool:
    """Validate project path."""
    if not path or not path.strip():
        raise ValueError("Project path cannot be empty")

    if not os.path.isabs(path):
        raise ValueError("Project path must be absolute")

    return True
```

---

## 📚 Reference Documentation

**Always keep updated**:
- docs/notes/PROJECT_PLAN.md - Current status and roadmap
- docs/README.md - Comprehensive system documentation
- mcp-servers/README.md - MCP installation and usage
- tests/README.md - Testing documentation

**Review before starting work**:
- docs/design/MCP_IMPLEMENTATION_APPROACH.md - System design
- docs/guides/RETROFIT_METHODOLOGY.md - Retrofit process

---

## ✅ Pre-Commit Checklist

Before committing ANY code:

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

## 🎯 Success Metrics

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

**Last Updated**: 2025-10-29
**Review Frequency**: After every major feature or monthly
**Applies To**: All AI assistants working on this project
