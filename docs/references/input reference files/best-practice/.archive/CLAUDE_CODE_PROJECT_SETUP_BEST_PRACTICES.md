# Claude Code Project Setup - Best Practices Guide

> **Purpose**: Template for setting up new Claude Code projects with maximum clarity, efficiency, and coding excellence.
> **Last Updated**: 2025-10-26
> **Source**: Distilled from my-finances-v2 project

---

## Table of Contents

1. [Initial Project Setup](#initial-project-setup)
2. [Directory Structure](#directory-structure)
3. [Documentation Architecture](#documentation-architecture)
4. [Quality Gates & Tooling](#quality-gates--tooling)
5. [Development Workflow](#development-workflow)
6. [Database & Schema Management](#database--schema-management)
7. [Testing Strategy](#testing-strategy)
8. [Claude Code Configuration](#claude-code-configuration)
9. [Quick Start Checklist](#quick-start-checklist)

---

## Initial Project Setup

### 1. Create Core Directory Structure

```bash
# Project root
mkdir -p my-project
cd my-project

# Source code
mkdir -p src
mkdir -p src/parsers  # or appropriate modules

# Tests
mkdir -p tests/unit
mkdir -p tests/integration
mkdir -p tests/fixtures

# Documentation
mkdir -p SPECIFICATION
mkdir -p SPECIFICATION/Database
mkdir -p SPECIFICATION/"TO DO"
mkdir -p SPECIFICATION/DONE

# Operations
mkdir -p logs
mkdir -p temp
mkdir -p scripts
mkdir -p migrations
mkdir -p config
mkdir -p import  # if needed
mkdir -p output

# Claude Code configuration
mkdir -p .claude
mkdir -p .claude/context
mkdir -p .ai-validation
```

### 2. Initialize Version Control

```bash
git init
```

Create `.gitignore`:
```gitignore
# Virtual Environment
venv/
.venv/
env/

# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
*.egg-info/
dist/
build/

# Environment & Secrets
.env
.env.local
*.key
credentials.json

# IDE
.vscode/
.idea/
*.swp
*.swo

# Logs & Temp
logs/*.log
temp/*
!temp/.gitkeep
!logs/.gitkeep

# Output
output/*
!output/.gitkeep

# OS
.DS_Store
Thumbs.db

# Testing
.pytest_cache/
.coverage
htmlcov/
.tox/
```

### 3. Initialize Python Environment

```bash
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

Create `requirements.txt`:
```txt
# Core dependencies
python-dotenv>=1.0.0
requests>=2.31.0
# Add your project-specific dependencies
```

Create `requirements-dev.txt`:
```txt
# Testing
pytest>=7.4.0
pytest-cov>=4.1.0
pytest-mock>=3.11.0

# Code Quality
ruff>=0.1.0
mypy>=1.5.0
bandit>=1.7.5
radon>=6.0.1
interrogate>=1.5.0

# Utilities
ipython>=8.14.0
```

Install dependencies:
```bash
pip install -r requirements.txt
pip install -r requirements-dev.txt
```

---

## Directory Structure

### File Placement Rules (Define Early)

**Purpose**: Eliminate confusion about where files belong.

```markdown
### Source Code (`src/`)
- Production code only
- Core modules by domain/feature
- No tests, no scripts, no temporary files
- Submodules for logical groupings (parsers, processors, models, etc.)

### Tests (`tests/`)
- Unit tests: `tests/unit/test_<module>.py`
- Integration tests: `tests/integration/test_<feature>.py`
- Fixtures: `tests/fixtures/` (sample data, mocks)
- Test utilities: Root of tests/ (shared helpers)

### Scripts (`scripts/`)
- Standalone operational scripts
- Entry points for workflows
- NOT one-off debugging (use temp/)

### Logs (`logs/`)
- **completed-actions.log** - Main work log (SINGLE SOURCE)
- Date-stamped logs: `YYYY-MM-DD_<description>.md`
- Process logs from application runs
- NEVER in project root

### Migrations (`migrations/`)
- SQL/Schema migration files
- Naming: `migration_NNN_<description>.sql`
- Apply scripts: `apply_migration_*.py`
- Base schema: `phase1_schema.sql`

### Specifications (`SPECIFICATION/`)
- Requirements documents (root level)
- `TO DO/` - Pending specs
- `DONE/` - Implemented specs
- `Database/` - Schema documentation

### Temporary Files (`temp/`)
- One-off debugging scripts
- Investigation/analysis scripts
- SQL queries for manual execution
- These are NOT production code

### Configuration (`config/`)
- Environment-specific settings
- Feature flags
- Not secrets (use .env)

### Root Level
- `README.md` - Project overview
- `CLAUDE.md` - Claude Code instructions
- `CURRENT_STATUS.md` - Current state
- `TODO.json` - Structured task tracking
- `FILE_DIRECTORY.txt` - File index
- `pyproject.toml` - Tool configuration
- `requirements*.txt` - Dependencies
- `.env.example` - Environment template
```

---

## Documentation Architecture

### 1. CLAUDE.md (Root Level)

**Purpose**: Primary instructions for Claude Code

```markdown
# CLAUDE.md

## Communication Style
- DO NOT create summary documents
- Log completed work to `logs/completed-actions.log`
- Keep temporary files in `temp/`
- Minimize token usage

## Workflow Enforcement Extension

### Change Control
- Every code change must include:
  - **Purpose** – why the change is being made
  - **Impact** – what files/modules/functions are affected
  - **Expected Outcome** – how behavior will change
- Claude must not proceed until explanation is written
- Log all changes to `logs/completed-actions.log` with:
  - Date/time
  - Description and rationale
  - Files modified
  - Linked test cases

### Test Coverage Enforcement
- For every change:
  1. Identify what tests must be created/updated/rerun
  2. Generate or suggest unit and integration tests
  3. Include expected results and pass/fail criteria
  4. Remind: "Run pytest and verify all tests pass before committing"

### Validation Before Commit
Ensure:
- All quality gates pass (pytest, ruff, mypy, bandit, radon)
- Documentation current
- Test coverage ≥ 80%
- Changes logged in `logs/completed-actions.log`

### Planning and Documentation
Before implementing:
- Update active plan or TODO entry
- Verify architecture documentation aligned
- If logic/schema/structure changes, prompt for doc updates

### QA Guidance Behavior
Challenge changes by asking:
- "What problem does this solve?"
- "What test confirms this works?"
- "Is this the smallest logical unit?"
- "Are plan, logs, and docs updated?"
If unclear, halt and request clarification.

### Test Script Generation
For each change, suggest/create:
- `tests/unit/test_<module>.py` – isolated functional tests
- `tests/integration/test_<feature>.py` – end-to-end tests
- Include descriptive docstrings (purpose, inputs/outputs, expected behavior)

## File Placement Rules
[Include your specific rules]

## Project Overview
[Brief description of project]

## Architecture
[Key components and patterns]

## Configuration
[Environment variables, tool configs]

## Critical Code Quality Standards
- Functions ≤ 30 lines
- Cyclomatic complexity ≤ 10
- 80%+ test coverage
- Zero linting/type/security errors
- Complete type hints on public functions
- Comments explaining each section

## Development Workflow
**Before Starting**: Check quality gates, review docs
**During Development**: Plan → Test First → Implement → Validate → Iterate
**Before Committing**: Run quality gates, all tests pass, update docs

## Common Commands
[Key commands for testing, linting, database, etc.]
```

### 2. Global CLAUDE.md (~/.claude/CLAUDE.md)

```markdown
# Global Claude Code Instructions

- Always keep logs in /logs
- Always keep temporary scripts in /temp
- Check FILE_DIRECTORY.txt before creating new files
- Follow file placement rules in project CLAUDE.md
```

### 3. .claude/context/ Directory

Create context files for complex topics:

```
.claude/context/
├── architecture.md          # System architecture overview
├── database-schema.md       # Database design and relationships
├── testing-strategy.md      # Testing approach and patterns
├── api-documentation.md     # API endpoints and contracts
└── deployment.md            # Deployment procedures
```

### 4. CURRENT_STATUS.md (Root Level)

```markdown
# Current Status

**Last Updated**: YYYY-MM-DD

## Project State
[Current phase, what's working, what's not]

## Recent Changes
[Major changes in last session]

## Active Tasks
[What needs to be done next]

## Blockers
[Any issues preventing progress]

## Key Decisions
[Important architectural or design decisions made]
```

### 5. TODO.json (Root Level)

```json
{
  "last_updated": "2025-10-26",
  "active_tasks": [
    {
      "id": 1,
      "title": "Task description",
      "status": "in_progress",
      "priority": "high",
      "created": "2025-10-26",
      "notes": "Additional context"
    }
  ],
  "completed_tasks": [],
  "blocked_tasks": []
}
```

### 6. logs/completed-actions.log

```markdown
# Completed Actions Log

## 2025-10-26

### [14:30] Implemented user authentication
**Purpose**: Add JWT-based authentication to API
**Impact**:
- Modified: src/auth.py, src/api.py
- Added: tests/unit/test_auth.py
**Outcome**: All endpoints now require valid JWT token
**Tests**: tests/unit/test_auth.py (12 tests, all passing)
**Verified**: pytest coverage 85% → 87%
```

---

## Quality Gates & Tooling

### 1. pyproject.toml

```toml
[project]
name = "my-project"
version = "0.1.0"
requires-python = ">=3.10"

[tool.ruff]
line-length = 88
target-version = "py310"
select = ["E", "F", "I", "N", "UP", "B", "A", "C4", "DTZ", "T10", "ISC", "ICN", "PIE", "PT", "Q", "RET", "SIM", "TID", "TCH", "PTH"]
ignore = []
exclude = [
    ".venv",
    "venv",
    "__pycache__",
    ".pytest_cache",
    ".git",
    "build",
    "dist",
]

[tool.ruff.per-file-ignores]
"tests/**/*.py" = ["F401", "F811"]

[tool.mypy]
python_version = "3.10"
strict = true
warn_return_any = true
warn_unused_configs = true
disallow_untyped_defs = true
disallow_any_generics = true
check_untyped_defs = true
no_implicit_optional = true
warn_redundant_casts = true
warn_unused_ignores = true
warn_no_return = true
warn_unreachable = true
strict_equality = true
exclude = ["venv", ".venv", "build", "dist"]

[[tool.mypy.overrides]]
module = "tests.*"
disallow_untyped_defs = false

[tool.pytest.ini_options]
testpaths = ["tests"]
python_files = ["test_*.py"]
python_classes = ["Test*"]
python_functions = ["test_*"]
addopts = [
    "-v",
    "--strict-markers",
    "--cov=src",
    "--cov-report=term-missing",
    "--cov-report=html",
    "--cov-fail-under=80"
]

[tool.coverage.run]
source = ["src"]
omit = [
    "*/tests/*",
    "*/venv/*",
    "*/__pycache__/*",
    "*/test_*.py"
]

[tool.coverage.report]
exclude_lines = [
    "pragma: no cover",
    "def __repr__",
    "raise AssertionError",
    "raise NotImplementedError",
    "if __name__ == .__main__.:",
    "if TYPE_CHECKING:",
    "@abstractmethod",
]

[tool.bandit]
exclude_dirs = ["tests", "venv", ".venv"]
skips = []

[tool.interrogate]
ignore-init-method = true
ignore-init-module = false
ignore-magic = false
ignore-semiprivate = false
ignore-private = false
ignore-property-decorators = false
ignore-module = false
ignore-nested-functions = false
ignore-nested-classes = true
ignore-setters = false
fail-under = 80
exclude = ["venv", ".venv", "tests"]
verbose = 1
quiet = false
```

### 2. Quality Check Script (.ai-validation/check_quality.sh)

```bash
#!/bin/bash
set -e

echo "=== Running Quality Gates ==="
echo ""

echo "1. Running pytest with coverage..."
pytest --cov=src --cov-report=term-missing -v
echo "✓ Tests passed"
echo ""

echo "2. Running ruff linter..."
ruff check .
echo "✓ Linting passed"
echo ""

echo "3. Running mypy type checker..."
mypy src/
echo "✓ Type checking passed"
echo ""

echo "4. Running bandit security scanner..."
bandit -r src/ -ll
echo "✓ Security check passed"
echo ""

echo "5. Running radon complexity analysis..."
radon cc src/ -a -nb --total-average -nc
echo "✓ Complexity check passed"
echo ""

echo "6. Running interrogate docstring coverage..."
interrogate -vv src/
echo "✓ Documentation check passed"
echo ""

echo "=== All Quality Gates Passed ==="
```

Make executable:
```bash
chmod +x .ai-validation/check_quality.sh
```

### 3. Pre-commit Hook (Optional)

```bash
#!/bin/bash
# .git/hooks/pre-commit

echo "Running quality checks before commit..."
.ai-validation/check_quality.sh

if [ $? -ne 0 ]; then
    echo "Quality checks failed. Commit aborted."
    exit 1
fi

echo "All checks passed. Proceeding with commit."
```

---

## Development Workflow

### Test-Driven Development (TDD) Cycle

```
1. PLAN
   - Use TodoWrite tool to create task breakdown
   - Write Chain-of-Thought in comments
   - Define success criteria

2. TEST FIRST
   - Write failing test that defines expected behavior
   - Include happy path and error cases
   - Run: pytest tests/unit/test_module.py -v
   - Confirm test fails as expected

3. IMPLEMENT
   - Write minimal code to pass test
   - Keep functions ≤ 30 lines
   - Add type hints and docstrings
   - Run test to verify it passes

4. VALIDATE
   - Run full quality gate: .ai-validation/check_quality.sh
   - Check coverage: pytest --cov=src --cov-report=term
   - Review for complexity: radon cc src/ -nc

5. ITERATE
   - Refactor if needed (keeping tests green)
   - Add edge case tests
   - Update documentation
   - Mark todo as completed

6. LOG
   - Add entry to logs/completed-actions.log
   - Update TODO.json
   - Update CURRENT_STATUS.md if significant change
```

### Change Control Template

Before implementing any change, document:

```markdown
## Change: [Brief Title]

### Purpose
Why is this change needed? What problem does it solve?

### Impact
- Files modified: [list]
- Functions affected: [list with file:line]
- Breaking changes: [yes/no, explain]
- Dependencies: [new/changed dependencies]

### Expected Outcome
How will behavior change? What will work differently?

### Tests
- Tests created: [list test files]
- Tests modified: [list test files]
- Coverage impact: [before% → after%]

### Rollback Plan
If this fails, how do we revert?
```

---

## Database & Schema Management

### Schema Versioning Approach

```sql
-- migrations/phase1_schema.sql (Base Schema v1.0.0)

-- Create schema version tracking table
CREATE TABLE IF NOT EXISTS schema_version (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    version VARCHAR(20) NOT NULL,
    description TEXT,
    applied_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    applied_by VARCHAR(100) DEFAULT 'system'
);

-- Insert base version
INSERT INTO schema_version (version, description)
VALUES ('1.0.0', 'Base schema');

-- [Your initial tables here]
```

### Migration Files

```sql
-- migrations/migration_001_add_users_table.sql (v1.1.0)

-- Migration: Add users table
-- Version: 1.1.0
-- Date: 2025-10-26
-- Description: Add user authentication support

BEGIN;

-- Check current version
DO $$
BEGIN
    IF NOT EXISTS (
        SELECT 1 FROM schema_version
        WHERE version = '1.0.0'
    ) THEN
        RAISE EXCEPTION 'Cannot apply migration 001: Base schema v1.0.0 not found';
    END IF;
END $$;

-- Create users table
CREATE TABLE IF NOT EXISTS users (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    email VARCHAR(255) NOT NULL UNIQUE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Add indexes
CREATE INDEX idx_users_email ON users(email);

-- Add comments (documentation)
COMMENT ON TABLE users IS 'User accounts for authentication';
COMMENT ON COLUMN users.email IS 'User email address (unique)';

-- Record migration
INSERT INTO schema_version (version, description)
VALUES ('1.1.0', 'Add users table with authentication support');

COMMIT;
```

### Migration Best Practices

1. **Always use transactions** (BEGIN/COMMIT)
2. **Check prerequisites** (previous version exists)
3. **Idempotent operations** (IF NOT EXISTS, IF EXISTS)
4. **Add indexes** for foreign keys and frequently queried columns
5. **Document with COMMENT ON** for tables and columns
6. **Record in schema_version** table
7. **Include rollback script** in comments

### Verify Current Schema Version

```bash
# scripts/verify_schema.py
from src.db import DatabaseManager

db = DatabaseManager()
result = db.client.table('schema_version').select('*').order('applied_at', desc=True).limit(1).execute()

if result.data:
    version = result.data[0]
    print(f"Current schema version: {version['version']}")
    print(f"Description: {version['description']}")
    print(f"Applied: {version['applied_at']}")
else:
    print("No schema version found!")
```

---

## Testing Strategy

### Test Structure

```
tests/
├── unit/                      # Isolated unit tests
│   ├── test_models.py        # Data models
│   ├── test_db.py            # Database operations
│   ├── test_parser.py        # Parsing logic
│   └── ...
├── integration/               # End-to-end tests
│   ├── test_import_flow.py   # Full import pipeline
│   ├── test_api_endpoints.py # API integration
│   └── ...
├── fixtures/                  # Shared test data
│   ├── sample_data.json
│   ├── mock_responses.py
│   └── ...
└── conftest.py               # Pytest configuration and fixtures
```

### conftest.py (Shared Fixtures)

```python
"""Shared pytest fixtures for all tests."""
import pytest
from unittest.mock import Mock
from src.db import DatabaseManager

@pytest.fixture
def mock_db():
    """Mock database manager for unit tests."""
    db = Mock(spec=DatabaseManager)
    return db

@pytest.fixture
def sample_transaction():
    """Sample transaction data for testing."""
    return {
        'account_id': 'test-account-id',
        'transaction_date': '2024-10-17',
        'amount': 50.00,
        'currency': 'GBP',
        'description': 'Test Transaction'
    }

@pytest.fixture(scope="session")
def test_db():
    """Real database connection for integration tests (use test environment)."""
    # Only use in integration tests with test database
    db = DatabaseManager()  # Should connect to TEST_SUPABASE_URL
    yield db
    # Cleanup after all tests
```

### Unit Test Example

```python
"""Unit tests for database manager."""
import pytest
from src.db import DatabaseManager
from unittest.mock import Mock, patch

class TestDatabaseManager:
    """Test DatabaseManager class."""

    def test_insert_transaction_success(self, mock_db, sample_transaction):
        """Test successful transaction insertion.

        Given: A valid transaction dictionary
        When: insert_transaction is called
        Then: Transaction is inserted and ID is returned
        """
        # Arrange
        mock_db.insert_transaction.return_value = {'id': 'test-id'}

        # Act
        result = mock_db.insert_transaction(sample_transaction)

        # Assert
        assert result['id'] == 'test-id'
        mock_db.insert_transaction.assert_called_once_with(sample_transaction)

    def test_insert_transaction_duplicate(self, mock_db, sample_transaction):
        """Test duplicate transaction handling.

        Given: A transaction that already exists
        When: insert_transaction is called
        Then: None is returned (duplicate detected)
        """
        # Arrange
        mock_db.insert_transaction.return_value = None

        # Act
        result = mock_db.insert_transaction(sample_transaction)

        # Assert
        assert result is None

    @pytest.mark.parametrize("missing_field", ["account_id", "amount", "transaction_date"])
    def test_insert_transaction_missing_required_fields(self, mock_db, sample_transaction, missing_field):
        """Test transaction insertion fails with missing required fields.

        Given: A transaction missing a required field
        When: insert_transaction is called
        Then: ValueError is raised
        """
        # Arrange
        del sample_transaction[missing_field]
        mock_db.insert_transaction.side_effect = ValueError(f"Missing required field: {missing_field}")

        # Act & Assert
        with pytest.raises(ValueError, match=f"Missing required field: {missing_field}"):
            mock_db.insert_transaction(sample_transaction)
```

### Integration Test Example

```python
"""Integration tests for import pipeline."""
import pytest
from src.scanner import FileScanner
from src.parser import Parser
from src.db import DatabaseManager

@pytest.mark.integration
class TestImportPipeline:
    """Test full import pipeline flow."""

    def test_full_import_flow(self, test_db, tmp_path):
        """Test complete import from file scan to database insertion.

        Given: Sample CSV file in test directory
        When: Full import pipeline runs
        Then: Transactions are in database with correct batch
        """
        # Arrange
        test_file = tmp_path / "test_transactions.csv"
        test_file.write_text("date,amount,description\n2024-10-17,50.00,Test")

        # Act
        scanner = FileScanner(test_db)
        files = scanner.scan(str(tmp_path))

        parser = Parser()
        transactions = parser.parse(files[0])

        batch = test_db.insert_batch(file_name=files[0].name)
        for txn in transactions:
            test_db.insert_transaction(txn, batch_id=batch['id'])

        # Assert
        result = test_db.client.table('bank_transactions').select('*').eq('import_batch_id', batch['id']).execute()
        assert len(result.data) == 1
        assert result.data[0]['amount'] == 50.00

        # Cleanup
        test_db.client.table('bank_transactions').delete().eq('import_batch_id', batch['id']).execute()
        test_db.client.table('import_batches').delete().eq('id', batch['id']).execute()
```

### Test Documentation Standards

Every test must have:
1. **Docstring** explaining purpose
2. **Given-When-Then** structure in docstring
3. **Clear variable names** (no single letters except loop counters)
4. **Assertions with messages** when helpful
5. **Cleanup** in integration tests

### Running Tests

```bash
# All tests
pytest

# Unit tests only
pytest tests/unit/ -v

# Integration tests only
pytest tests/integration/ -v -m integration

# Specific test file
pytest tests/unit/test_db.py -v

# Specific test function
pytest tests/unit/test_db.py::TestDatabaseManager::test_insert_transaction_success -v

# With coverage
pytest --cov=src --cov-report=html

# Show slowest tests
pytest --durations=10
```

---

## Claude Code Configuration

### .claude/PROJECT.yaml (Optional Skills)

```yaml
# Skills are not currently implemented but this is the proposed structure
claude_code:
  skills:
    understand:
      description: "Explain code structure, dependencies, and data flows"
      constraints:
        - "Trace execution paths"
        - "Identify side effects"
        - "Document assumptions"

    refactor:
      description: "Improve code quality while maintaining behavior"
      constraints:
        - "Keep function signatures unchanged"
        - "Preserve all tests"
        - "Maintain Python >= 3.10 compatibility"
      output:
        - "Changed code blocks"
        - "Before/after comparison"

    test:
      description: "Generate comprehensive test coverage"
      constraints:
        - "Target >80% coverage"
        - "Include happy path and error cases"
        - "Use pytest fixtures"
      structure:
        unit: "tests/unit/test_<module>.py"
        integration: "tests/integration/test_<feature>.py"

    debug:
      description: "Root cause analysis with safe fixes"
      process:
        - "Analyze error trace/logs"
        - "Identify root cause"
        - "Provide tested fix"
        - "Suggest prevention measures"

    doc:
      description: "Add/update documentation"
      style: "Google-style docstrings"
      coverage:
        - "All public functions"
        - "Complex private functions"
        - "Module-level docstrings"

    arch:
      description: "Analyze and design system architecture"
      output:
        - "Component diagrams"
        - "Interaction flows"
        - "Data models"
        - "Design decisions"
```

---

## Quick Start Checklist

### Phase 1: Foundation (Day 1)

- [ ] Create directory structure
- [ ] Initialize git repository
- [ ] Create `.gitignore`
- [ ] Setup Python virtual environment
- [ ] Create `requirements.txt` and `requirements-dev.txt`
- [ ] Install dependencies
- [ ] Create `pyproject.toml` with tool configs
- [ ] Create `.env.example` (no secrets)
- [ ] Create `.ai-validation/check_quality.sh`
- [ ] Test quality gates run successfully

### Phase 2: Documentation (Day 1-2)

- [ ] Write `README.md` (project overview)
- [ ] Write comprehensive `CLAUDE.md` (Claude Code instructions)
- [ ] Create global `~/.claude/CLAUDE.md` (if not exists)
- [ ] Create `CURRENT_STATUS.md`
- [ ] Create `TODO.json`
- [ ] Create `logs/completed-actions.log`
- [ ] Create `.claude/context/` documentation files
- [ ] Write file placement rules in `CLAUDE.md`

### Phase 3: Core Setup (Day 2-3)

- [ ] Setup database (if applicable)
- [ ] Create base schema migration
- [ ] Implement database connection module
- [ ] Write first unit test (database connection)
- [ ] Verify test runs and passes
- [ ] Setup CI/CD (optional but recommended)
- [ ] Create `scripts/verify_setup.py`

### Phase 4: Development Workflow (Day 3+)

- [ ] Pick first feature from TODO.json
- [ ] Follow TDD cycle: Plan → Test → Implement → Validate
- [ ] Run quality gates before each commit
- [ ] Log completed work to `logs/completed-actions.log`
- [ ] Update `TODO.json` and `CURRENT_STATUS.md`
- [ ] Create first pull request (if using Git flow)

### Ongoing Practices

- [ ] Run `.ai-validation/check_quality.sh` before every commit
- [ ] Maintain 80%+ test coverage
- [ ] Keep functions ≤ 30 lines
- [ ] Update documentation as code changes
- [ ] Log all completed work
- [ ] Use TodoWrite tool for task tracking
- [ ] Review and update `CURRENT_STATUS.md` weekly

---

## Key Principles Summary

### 1. Documentation First
- Write CLAUDE.md before coding
- Keep CURRENT_STATUS.md current
- Log all completed work
- Update TODO.json regularly

### 2. Test-Driven Development
- Write tests before implementation
- Aim for >80% coverage
- Test both happy path and errors
- Use fixtures for common setup

### 3. Quality Gates
- Zero tolerance for quality gate failures
- Run checks before every commit
- Automate with pre-commit hooks
- Fix issues immediately, don't accumulate

### 4. File Organization
- Clear placement rules eliminate confusion
- Logs always in `/logs`, never root
- Temp scripts in `/temp`
- One source of truth for everything

### 5. Change Control
- Document purpose, impact, outcome
- Link tests to changes
- Review before implementing
- Log after completing

### 6. Database Versioning
- Sequential migrations
- Idempotent operations
- Document with COMMENT ON
- Track in schema_version table

### 7. Claude Code Integration
- Comprehensive CLAUDE.md instructions
- Use TodoWrite tool for planning
- Workflow enforcement extension
- Context documentation in .claude/

---

## Template Files

### Minimal .env.example

```env
# Application
ENV=development
LOG_LEVEL=INFO

# Database (if applicable)
DATABASE_URL=
DATABASE_KEY=

# APIs
API_KEY=

# Secrets (NEVER commit actual secrets)
SECRET_KEY=
```

### Minimal README.md

```markdown
# Project Name

Brief description of what this project does.

## Setup

```bash
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
pip install -r requirements-dev.txt
cp .env.example .env
# Edit .env with your configuration
```

## Development

```bash
# Run tests
pytest

# Run quality checks
.ai-validation/check_quality.sh

# Run application
python scripts/main.py
```

## Documentation

- See `CLAUDE.md` for development guidelines
- See `CURRENT_STATUS.md` for project status
- See `SPECIFICATION/` for requirements
```

### Minimal setup_quick.sh

```bash
#!/bin/bash
set -e

echo "Setting up project..."

# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
pip install -r requirements-dev.txt

# Create .env if not exists
if [ ! -f .env ]; then
    cp .env.example .env
    echo "Created .env file - please configure it"
fi

# Make quality check script executable
chmod +x .ai-validation/check_quality.sh

# Run quality checks
echo "Running quality checks..."
.ai-validation/check_quality.sh

echo "Setup complete!"
```

---

## Success Metrics

Your project is well-configured when:

- ✅ Anyone can run `.ai-validation/check_quality.sh` and it passes
- ✅ `CLAUDE.md` clearly explains project structure and workflow
- ✅ All files follow placement rules (no confusion about location)
- ✅ Test coverage is >80% and maintained
- ✅ `logs/completed-actions.log` has entries for all significant changes
- ✅ `CURRENT_STATUS.md` accurately reflects project state
- ✅ Database has schema versioning in place
- ✅ New developers can onboard in <1 hour
- ✅ Claude Code can navigate codebase without confusion
- ✅ Zero linting, type, or security errors

---

## Additional Resources

### Recommended Tools

- **Database**: Supabase (PostgreSQL), SQLite for local
- **Linting**: Ruff (fast, comprehensive)
- **Type Checking**: MyPy (strict mode)
- **Security**: Bandit (Python security scanner)
- **Complexity**: Radon (cyclomatic complexity)
- **Testing**: Pytest with pytest-cov
- **Documentation**: Google-style docstrings

### Recommended Reading

- Clean Code by Robert C. Martin
- Test-Driven Development by Kent Beck
- The Pragmatic Programmer
- Software Engineering at Google (chapters on testing & documentation)

---

## Conclusion

This setup provides:
- **Clarity**: Clear structure, placement rules, documentation
- **Efficiency**: Quality gates, TDD workflow, automated checks
- **Best Practices**: Testing, type hints, complexity limits, change control

Clone this structure for your next project and you'll spend less time on setup and more time building features. Claude Code will understand your project immediately and provide better assistance.

**Remember**: The investment in setup pays dividends in development velocity, code quality, and long-term maintainability.
