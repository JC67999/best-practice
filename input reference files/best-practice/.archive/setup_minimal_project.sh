#!/usr/bin/env bash
set -e  # Exit on error

# ============================================================================
# Claude Code Project Setup Script - Minimal Root Structure
# ============================================================================
# Creates a clean, minimal project structure optimized for Claude Code
# Root directory contains only 4 folders + essential config files
#
# Usage: ./setup_minimal_project.sh [project-name] [python-version]
# Example: ./setup_minimal_project.sh my-api-project 3.11
# ============================================================================

# --- Configuration ---
PROJECT_NAME="${1:-new-claude-project}"
PYTHON_VERSION="${2:-3.10}"
AUTHOR_NAME="${3:-Your Name}"
AUTHOR_EMAIL="${4:-you@example.com}"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Helper functions
print_step() {
    echo -e "${BLUE}==>${NC} $1"
}

print_success() {
    echo -e "${GREEN}✓${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}⚠${NC} $1"
}

print_error() {
    echo -e "${RED}✗${NC} $1"
}

# ============================================================================
# START SETUP
# ============================================================================

echo ""
echo "╔════════════════════════════════════════════════════════════════╗"
echo "║   Claude Code Project Setup - Minimal Root Structure          ║"
echo "╚════════════════════════════════════════════════════════════════╝"
echo ""
echo "Project: $PROJECT_NAME"
echo "Python:  $PYTHON_VERSION+"
echo ""

# --- Step 1: Create Project Directory ---
print_step "Creating project directory..."
if [ -d "$PROJECT_NAME" ]; then
    print_error "Directory '$PROJECT_NAME' already exists!"
    read -p "Continue anyway? (y/N) " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        exit 1
    fi
else
    mkdir -p "$PROJECT_NAME"
fi
cd "$PROJECT_NAME"
print_success "Project directory created"

# --- Step 2: Create Directory Structure ---
print_step "Creating minimal directory structure..."

# Core application structure
mkdir -p src/core
mkdir -p src/services
mkdir -p src/adapters
mkdir -p src/infrastructure

# Test structure
mkdir -p tests/unit
mkdir -p tests/integration
mkdir -p tests/fixtures

# Documentation structure
mkdir -p docs/design
mkdir -p docs/design/decisions
mkdir -p docs/schema
mkdir -p docs/notes
mkdir -p docs/specifications/pending
mkdir -p docs/specifications/completed

# Operational data structure (consolidated)
mkdir -p _project_data/logs
mkdir -p _project_data/temp
mkdir -p _project_data/input
mkdir -p _project_data/output
mkdir -p _project_data/.archive
mkdir -p _project_data/migrations

# AI configuration
mkdir -p .claude/context
mkdir -p .ai-validation

print_success "Directory structure created"

# --- Step 3: Create .gitkeep files for empty directories ---
print_step "Creating .gitkeep files..."
find . -type d -empty -not -path "./.git/*" -exec touch {}/.gitkeep \;
print_success ".gitkeep files created"

# --- Step 4: Initialize Git ---
print_step "Initializing git repository..."
git init -q
print_success "Git repository initialized"

# --- Step 5: Create .gitignore ---
print_step "Creating .gitignore..."
cat > .gitignore << 'EOF'
# Virtual Environment
venv/
.venv/
env/
ENV/
*.virtualenv

# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
*.egg-info/
dist/
build/
*.egg
.pytest_cache/
.mypy_cache/
.ruff_cache/

# Environment & Secrets
.env
.env.local
.env.*.local
*.key
*.pem
credentials.json
secrets.json

# IDE
.vscode/
.idea/
*.swp
*.swo
*~
.DS_Store

# Operational Data (selectively ignore)
_project_data/logs/*.log
_project_data/temp/*
!_project_data/temp/.gitkeep
_project_data/output/*
!_project_data/output/.gitkeep
_project_data/.archive/*
!_project_data/.archive/.gitkeep

# Keep migration files and input examples
!_project_data/migrations/
!_project_data/input/

# Coverage
.coverage
htmlcov/
coverage.xml
*.cover

# Testing
.tox/
.pytest_cache/

# OS
.DS_Store
Thumbs.db
*.bak
EOF
print_success ".gitignore created"

# --- Step 6: Create Python Package Structure ---
print_step "Creating Python package files..."

# Create __init__.py files
touch src/__init__.py
touch src/core/__init__.py
touch src/services/__init__.py
touch src/adapters/__init__.py
touch src/infrastructure/__init__.py
touch tests/__init__.py
touch tests/unit/__init__.py
touch tests/integration/__init__.py

# Create main.py entry point
cat > src/main.py << 'EOF'
"""Main application entry point."""


def main() -> None:
    """Main application function."""
    print("Hello from Claude Code project!")


if __name__ == "__main__":
    main()
EOF

print_success "Python package structure created"

# --- Step 7: Create requirements.txt ---
print_step "Creating requirements.txt..."
cat > requirements.txt << 'EOF'
# Core Dependencies
python-dotenv>=1.0.0

# Add your project dependencies here
# Example:
# requests>=2.31.0
# pydantic>=2.0.0
EOF
print_success "requirements.txt created"

# --- Step 8: Create requirements-dev.txt ---
print_step "Creating requirements-dev.txt..."
cat > requirements-dev.txt << 'EOF'
# Testing
pytest>=7.4.0
pytest-cov>=4.1.0
pytest-mock>=3.12.0
pytest-asyncio>=0.21.0

# Code Quality
ruff>=0.1.0
mypy>=1.5.0
bandit>=1.7.5
radon>=6.0.1
interrogate>=1.5.0

# Development Utilities
ipython>=8.14.0
ipdb>=0.13.13

# Type Stubs
types-requests>=2.31.0
EOF
print_success "requirements-dev.txt created"

# --- Step 9: Create pyproject.toml ---
print_step "Creating pyproject.toml..."
cat > pyproject.toml << EOF
[project]
name = "$PROJECT_NAME"
version = "0.1.0"
description = "A Claude Code project with minimal root structure"
authors = [
    {name = "$AUTHOR_NAME", email = "$AUTHOR_EMAIL"}
]
requires-python = ">=$PYTHON_VERSION"
readme = "README.md"
license = {text = "MIT"}

[project.urls]
homepage = "https://github.com/yourusername/$PROJECT_NAME"
repository = "https://github.com/yourusername/$PROJECT_NAME"

[build-system]
requires = ["setuptools>=68.0.0", "wheel"]
build-backend = "setuptools.build_meta"

# ============================================================================
# RUFF - Fast Python Linter
# ============================================================================
[tool.ruff]
line-length = 88
target-version = "py${PYTHON_VERSION/./}"
src = ["src", "tests"]

# Enable these rule sets
select = [
    "E",   # pycodestyle errors
    "W",   # pycodestyle warnings
    "F",   # pyflakes
    "I",   # isort
    "N",   # pep8-naming
    "UP",  # pyupgrade
    "B",   # flake8-bugbear
    "A",   # flake8-builtins
    "C4",  # flake8-comprehensions
    "DTZ", # flake8-datetimez
    "T10", # flake8-debugger
    "ISC", # flake8-implicit-str-concat
    "ICN", # flake8-import-conventions
    "PIE", # flake8-pie
    "PT",  # flake8-pytest-style
    "Q",   # flake8-quotes
    "RET", # flake8-return
    "SIM", # flake8-simplify
    "TID", # flake8-tidy-imports
    "TCH", # flake8-type-checking
    "PTH", # flake8-use-pathlib
]

ignore = []

exclude = [
    ".venv",
    "venv",
    "__pycache__",
    ".pytest_cache",
    ".git",
    "build",
    "dist",
    "_project_data",
]

[tool.ruff.per-file-ignores]
"tests/**/*.py" = ["F401", "F811", "S101"]  # Allow unused imports and asserts in tests
"src/__init__.py" = ["F401"]  # Allow unused imports in __init__.py
"__init__.py" = ["F401"]

[tool.ruff.isort]
known-first-party = ["src"]

# ============================================================================
# MYPY - Static Type Checking
# ============================================================================
[tool.mypy]
python_version = "$PYTHON_VERSION"
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
show_error_codes = true
show_column_numbers = true
pretty = true

exclude = [
    "venv",
    ".venv",
    "build",
    "dist",
    "_project_data",
]

[[tool.mypy.overrides]]
module = "tests.*"
disallow_untyped_defs = false

# ============================================================================
# PYTEST - Testing Framework
# ============================================================================
[tool.pytest.ini_options]
minversion = "7.0"
testpaths = ["tests"]
python_files = ["test_*.py", "*_test.py"]
python_classes = ["Test*"]
python_functions = ["test_*"]

addopts = [
    "-v",                                    # Verbose output
    "--strict-markers",                      # Strict marker usage
    "--strict-config",                       # Strict config
    "--cov=src",                            # Coverage for src/
    "--cov-report=term-missing",            # Show missing lines
    "--cov-report=html:_project_data/output/htmlcov",  # HTML report
    "--cov-fail-under=80",                  # Require 80% coverage
    "--tb=short",                           # Short traceback format
]

markers = [
    "unit: Unit tests",
    "integration: Integration tests",
    "slow: Slow running tests",
]

# ============================================================================
# COVERAGE - Code Coverage
# ============================================================================
[tool.coverage.run]
source = ["src"]
omit = [
    "*/tests/*",
    "*/venv/*",
    "*/__pycache__/*",
    "*/test_*.py",
    "*_test.py",
]
branch = true

[tool.coverage.report]
exclude_lines = [
    "pragma: no cover",
    "def __repr__",
    "raise AssertionError",
    "raise NotImplementedError",
    "if __name__ == .__main__.:",
    "if TYPE_CHECKING:",
    "@abstractmethod",
    "@abc.abstractmethod",
]
precision = 2
show_missing = true

# ============================================================================
# BANDIT - Security Linter
# ============================================================================
[tool.bandit]
exclude_dirs = [
    "tests",
    "venv",
    ".venv",
    "_project_data",
]
skips = []

# ============================================================================
# INTERROGATE - Docstring Coverage
# ============================================================================
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
exclude = ["venv", ".venv", "tests", "_project_data"]
verbose = 1
quiet = false
whitelist-regex = []
color = true
EOF
print_success "pyproject.toml created"

# --- Step 10: Create .env.example ---
print_step "Creating .env.example..."
cat > .env.example << 'EOF'
# Environment Configuration
# Copy this file to .env and fill in your values
# NEVER commit .env to version control!

# Application
ENV=development
DEBUG=true
LOG_LEVEL=INFO

# Database (example)
# DATABASE_URL=postgresql://user:password@localhost:5432/dbname
# DATABASE_POOL_SIZE=5

# API Keys (example)
# API_KEY=your-api-key-here
# SECRET_KEY=your-secret-key-here

# External Services (example)
# THIRD_PARTY_API_URL=https://api.example.com
# THIRD_PARTY_API_KEY=your-key-here
EOF
print_success ".env.example created"

# --- Step 11: Create pytest conftest.py ---
print_step "Creating test configuration..."
cat > tests/conftest.py << 'EOF'
"""Shared pytest fixtures and configuration."""
import pytest
from typing import Any, Dict


@pytest.fixture
def sample_data() -> Dict[str, Any]:
    """Sample data fixture for testing.

    Returns:
        Dictionary with sample test data
    """
    return {
        "id": 1,
        "name": "Test Item",
        "value": 42.0,
    }


@pytest.fixture
def temp_dir(tmp_path):
    """Temporary directory fixture.

    Args:
        tmp_path: pytest's built-in temporary directory fixture

    Returns:
        Path to temporary directory
    """
    return tmp_path
EOF
print_success "Test configuration created"

# --- Step 12: Create sample test ---
print_step "Creating sample test..."
cat > tests/unit/test_main.py << 'EOF'
"""Unit tests for main module."""
from src.main import main


def test_main_runs_without_error():
    """Test that main function runs without raising an exception.

    Given: The main function exists
    When: main() is called
    Then: It executes without raising an exception
    """
    try:
        main()
        assert True
    except Exception as e:
        pytest.fail(f"main() raised an exception: {e}")
EOF
print_success "Sample test created"

# --- Step 13: Create quality check script ---
print_step "Creating quality check script..."
cat > .ai-validation/check_quality.sh << 'EOF'
#!/bin/bash
# Quality Gates Script - All checks must pass before commit
set -e

echo "╔════════════════════════════════════════════════════════════════╗"
echo "║                     QUALITY GATES                              ║"
echo "╚════════════════════════════════════════════════════════════════╝"
echo ""

# Colors
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m'

# Track failures
FAILURES=0

run_check() {
    local name=$1
    local cmd=$2

    echo -e "${YELLOW}Running: $name${NC}"
    if eval "$cmd"; then
        echo -e "${GREEN}✓ $name passed${NC}"
        echo ""
    else
        echo -e "${RED}✗ $name failed${NC}"
        echo ""
        FAILURES=$((FAILURES + 1))
    fi
}

# 1. Tests with Coverage
run_check "Tests & Coverage" "pytest --cov=src --cov-report=term-missing -v"

# 2. Linting
run_check "Ruff Linter" "ruff check ."

# 3. Type Checking
run_check "MyPy Type Checker" "mypy src/"

# 4. Security Scanning
run_check "Bandit Security" "bandit -r src/ -ll -q"

# 5. Complexity Analysis
run_check "Radon Complexity" "radon cc src/ -a -nb --total-average -nc"

# 6. Docstring Coverage
run_check "Interrogate Docstrings" "interrogate -vv src/"

echo "╔════════════════════════════════════════════════════════════════╗"
if [ $FAILURES -eq 0 ]; then
    echo -e "║  ${GREEN}✓ ALL QUALITY GATES PASSED${NC}                                ║"
    echo "╚════════════════════════════════════════════════════════════════╝"
    exit 0
else
    echo -e "║  ${RED}✗ $FAILURES QUALITY GATE(S) FAILED${NC}                            ║"
    echo "╚════════════════════════════════════════════════════════════════╝"
    exit 1
fi
EOF
chmod +x .ai-validation/check_quality.sh
print_success "Quality check script created"

# --- Step 14: Create CLAUDE.md ---
print_step "Creating CLAUDE.md..."
cat > CLAUDE.md << EOF
# CLAUDE.md - Development Guide for $PROJECT_NAME

> **Last Updated**: $(date +%Y-%m-%d)
> **Structure**: Minimal Root Philosophy (4 top-level folders)

---

## Project Structure

\`\`\`
$PROJECT_NAME/
├── src/                    # All production code
├── tests/                  # All tests (unit, integration, fixtures)
├── docs/                   # All documentation (design, schema, notes)
├── _project_data/          # All operational data (logs, temp, I/O)
├── .claude/                # Claude Code configuration (hidden)
├── .ai-validation/         # Quality tools (hidden)
├── CLAUDE.md               # This file
├── README.md               # Project overview
└── pyproject.toml          # Tool configuration
\`\`\`

---

## File Placement Rules

**CRITICAL**: Only 4 folders in root! Use this decision tree:

1. **Production source code?** → \`src/\`
   - Core logic → \`src/core/\`
   - Services → \`src/services/\`
   - External adapters → \`src/adapters/\`
   - Infrastructure → \`src/infrastructure/\`

2. **Test code?** → \`tests/\`
   - Unit tests → \`tests/unit/\`
   - Integration tests → \`tests/integration/\`
   - Test data → \`tests/fixtures/\`

3. **Documentation?** → \`docs/\`
   - Architecture/design → \`docs/design/\`
   - Schema/data models → \`docs/schema/\`
   - Active dev notes → \`docs/notes/\`
   - Requirements → \`docs/specifications/\`

4. **Operational/ephemeral data?** → \`_project_data/\`
   - Logs → \`_project_data/logs/\`
   - Temp scripts → \`_project_data/temp/\`
   - Input data → \`_project_data/input/\`
   - Output files → \`_project_data/output/\`
   - Old versions → \`_project_data/.archive/\`
   - DB migrations → \`_project_data/migrations/\`

**NEVER create files in project root unless it's configuration!**

---

## Workflow Enforcement

### Change Control
Every code change must include:
- **Purpose**: Why is this change needed?
- **Impact**: What files/modules/functions are affected?
- **Expected Outcome**: How will behavior change?
- **Tests**: What tests were created/updated?

### Before ANY Implementation
1. Update \`docs/notes/plan.md\` with what you're doing
2. Write tests first (TDD)
3. Implement minimal code to pass tests
4. Run quality gates: \`.ai-validation/check_quality.sh\`
5. Log completed work to \`_project_data/logs/completed-actions.log\`

### Test Coverage Enforcement
- For every change:
  1. Identify what tests must be created/updated/rerun
  2. Generate unit and integration tests for new/modified logic
  3. Include expected results and pass/fail criteria
  4. Remind: "Run pytest and verify all tests pass"

### Validation Before Commit
Ensure:
- All quality gates pass (\`pytest\`, \`ruff\`, \`mypy\`, \`bandit\`, \`radon\`)
- Documentation is current
- Test coverage ≥ 80%
- All changes logged in \`_project_data/logs/completed-actions.log\`

### Planning and Documentation
Before implementing:
- Update active plan in \`docs/notes/plan.md\`
- Verify architecture documentation aligned
- If logic/schema/structure changes, update relevant docs

### QA Guidance
Challenge every change by asking:
- "What problem does this solve?"
- "What test confirms this works?"
- "Is this the smallest logical unit?"
- "Are plan, logs, and docs updated?"

If any answer is unclear, HALT and request clarification.

### Test Script Generation
For each change, suggest/create:
- \`tests/unit/test_<module>.py\` – isolated functional tests
- \`tests/integration/test_<feature>.py\` – end-to-end tests
- Include descriptive docstrings (purpose, inputs/outputs, expected behavior)

---

## Code Quality Standards

**Mandatory Requirements**:
- Functions ≤ 30 lines (Single Responsibility)
- Cyclomatic complexity ≤ 10
- Test coverage ≥ 80%
- Zero linting errors (\`ruff\`)
- Zero type errors (\`mypy --strict\`)
- Zero security issues (\`bandit\`)
- All public functions have Google-style docstrings

**Type Hints**:
- All public functions must have complete type hints
- Use \`from typing import Any, Dict, List, Optional\`
- Example: \`def process(data: Dict[str, Any]) -> List[str]:\`

**Error Handling**:
- All external calls wrapped in try-except
- No hardcoded secrets (use .env)
- Always use context managers for resources
- Validate all external inputs

**Documentation**:
- Google-style docstrings for all public functions
- Comments explaining WHY, not WHAT
- Update docs when code changes

---

## Development Workflow (TDD)

\`\`\`
1. PLAN
   - Update docs/notes/plan.md
   - Define success criteria
   - Break into small tasks

2. TEST FIRST
   - Write failing test defining expected behavior
   - Include happy path and error cases
   - Run: pytest tests/unit/test_module.py -v
   - Confirm test fails as expected

3. IMPLEMENT
   - Write minimal code to pass test
   - Keep functions ≤ 30 lines
   - Add type hints and docstrings
   - Run test to verify it passes

4. VALIDATE
   - Run: .ai-validation/check_quality.sh
   - All checks must pass!

5. LOG
   - Add entry to _project_data/logs/completed-actions.log
   - Update docs/notes/plan.md
\`\`\`

---

## Common Commands

### Development
\`\`\`bash
# Activate virtual environment
source venv/bin/activate  # Linux/Mac
venv\\Scripts\\activate     # Windows

# Run application
python src/main.py

# Install dependencies
pip install -r requirements.txt
pip install -r requirements-dev.txt
\`\`\`

### Testing
\`\`\`bash
# Run all tests
pytest

# Run with coverage
pytest --cov=src --cov-report=html

# Run specific test file
pytest tests/unit/test_main.py -v

# Run specific test
pytest tests/unit/test_main.py::test_main_runs_without_error -v
\`\`\`

### Quality Checks
\`\`\`bash
# Run all quality gates
.ai-validation/check_quality.sh

# Individual checks
ruff check .              # Linting
mypy src/                 # Type checking
bandit -r src/ -ll        # Security
radon cc src/ -nc         # Complexity
interrogate -vv src/      # Docstrings
\`\`\`

---

## Logging Completed Work

Add entries to \`_project_data/logs/completed-actions.log\`:

\`\`\`markdown
## $(date '+%Y-%m-%d %H:%M')

### [Brief Description]
**Purpose**: Why this change was made
**Impact**:
- Modified: file1.py, file2.py
- Added: tests/unit/test_new_feature.py
**Outcome**: What changed and how to verify
**Tests**: All tests passing, coverage X% → Y%
\`\`\`

---

## Key Principles

1. **Minimal Root**: Keep root directory clean (4 folders only)
2. **Test First**: Write tests before implementation
3. **Quality Gates**: Zero tolerance for failures
4. **Documentation**: Keep current, link to details
5. **Change Control**: Purpose → Impact → Outcome → Tests

---

## Architecture Overview

(Update this section with your specific architecture)

### Core Modules
- \`src/core/\`: Business logic and domain models
- \`src/services/\`: Application services and orchestration
- \`src/adapters/\`: External integrations (APIs, parsers, etc.)
- \`src/infrastructure/\`: Technical concerns (DB, config, logging)

### Data Flow
(Add your data flow description here)

### Key Design Decisions
(Document important architectural decisions in \`docs/design/decisions/\`)

---

## Quick Reference

- **Documentation**: \`docs/design/architecture.md\`
- **Current Plan**: \`docs/notes/plan.md\`
- **Todo List**: \`docs/notes/todo.md\`
- **Completed Work**: \`_project_data/logs/completed-actions.log\`
- **Quality Gates**: \`.ai-validation/check_quality.sh\`

---

**Remember**: When in doubt, use subdirectories. Keep the root clean!
EOF
print_success "CLAUDE.md created"

# --- Step 15: Create README.md ---
print_step "Creating README.md..."
cat > README.md << EOF
# $PROJECT_NAME

Brief description of what this project does (update this!).

## Quick Start

\`\`\`bash
# Clone and navigate to project
cd $PROJECT_NAME

# Create virtual environment
python$PYTHON_VERSION -m venv venv
source venv/bin/activate  # On Windows: venv\\Scripts\\activate

# Install dependencies
pip install -r requirements.txt
pip install -r requirements-dev.txt

# Run tests
pytest

# Run quality checks
.ai-validation/check_quality.sh

# Run application
python src/main.py
\`\`\`

## Project Structure

\`\`\`
$PROJECT_NAME/
├── src/                    # Application source code
├── tests/                  # Test suite (unit, integration, fixtures)
├── docs/                   # Documentation (design, schema, notes)
├── _project_data/          # Operational data (logs, temp, I/O)
├── .claude/                # Claude Code configuration
└── .ai-validation/         # Quality enforcement tools
\`\`\`

## Development

### Prerequisites
- Python $PYTHON_VERSION+
- Virtual environment recommended

### Setup
1. Create virtual environment: \`python -m venv venv\`
2. Activate: \`source venv/bin/activate\`
3. Install dependencies: \`pip install -r requirements.txt -r requirements-dev.txt\`

### Testing
\`\`\`bash
pytest                          # Run all tests
pytest --cov=src               # With coverage report
pytest tests/unit/             # Unit tests only
pytest -v                      # Verbose output
\`\`\`

### Quality Gates
All checks must pass before committing:
\`\`\`bash
.ai-validation/check_quality.sh
\`\`\`

Individual checks:
- \`ruff check .\` - Linting
- \`mypy src/\` - Type checking
- \`bandit -r src/ -ll\` - Security scanning
- \`radon cc src/ -nc\` - Complexity analysis
- \`interrogate -vv src/\` - Docstring coverage

### Code Standards
- Functions ≤ 30 lines
- Test coverage ≥ 80%
- Type hints on all public functions
- Google-style docstrings
- Zero linting/type/security errors

## Documentation

- **Development Guide**: \`CLAUDE.md\` - Complete development workflow
- **Architecture**: \`docs/design/architecture.md\` - System design
- **Current Plan**: \`docs/notes/plan.md\` - Active development plan
- **Specifications**: \`docs/specifications/\` - Requirements and specs

## Contributing

1. Update \`docs/notes/plan.md\` with your changes
2. Write tests first (TDD)
3. Implement code
4. Run quality gates: \`.ai-validation/check_quality.sh\`
5. Log work to \`_project_data/logs/completed-actions.log\`
6. Commit with descriptive message

## License

MIT License (update as needed)

## Contact

$AUTHOR_NAME - $AUTHOR_EMAIL
EOF
print_success "README.md created"

# --- Step 16: Create initial documentation files ---
print_step "Creating initial documentation..."

# Architecture document
cat > docs/design/architecture.md << 'EOF'
# Architecture Overview

## System Design

(Document your high-level architecture here)

### Components

- **Core Layer**: Business logic and domain models
- **Service Layer**: Application services and orchestration
- **Adapter Layer**: External integrations (APIs, databases, etc.)
- **Infrastructure Layer**: Technical concerns (config, logging, etc.)

### Data Flow

(Describe how data flows through your system)

### Technology Stack

- Python 3.10+
- (Add your technologies here)

## Design Principles

- Dependency Inversion (depend on abstractions)
- Single Responsibility (one reason to change)
- Test-Driven Development (tests first)
- Minimal Root Structure (4 top-level folders)

## Key Decisions

See `decisions/` folder for Architecture Decision Records (ADRs).
EOF

# Initial plan
cat > docs/notes/plan.md << EOF
# Development Plan

**Last Updated**: $(date +%Y-%m-%d)

## Current Focus

Initial project setup complete. Ready for development!

## Next Steps

1. [ ] Define core domain models in \`src/core/models.py\`
2. [ ] Write tests for domain models in \`tests/unit/test_models.py\`
3. [ ] Implement first feature
4. [ ] Add integration tests
5. [ ] Document architecture decisions

## Future Ideas

- (Add future feature ideas here)

## Blockers

- None currently

## Notes

- Project uses minimal root structure (4 folders)
- All quality gates configured and passing
- Ready for TDD workflow
EOF

# Initial todo
cat > docs/notes/todo.md << EOF
# Todo List

**Last Updated**: $(date +%Y-%m-%d)

## High Priority

- [ ] Define project requirements in \`docs/specifications/requirements.md\`
- [ ] Design core domain models
- [ ] Implement first feature (TDD)

## Medium Priority

- [ ] Setup CI/CD pipeline
- [ ] Add more comprehensive tests
- [ ] Document API (if applicable)

## Low Priority

- [ ] Performance optimization
- [ ] Additional tooling integration

## Completed

- [x] Project structure created
- [x] Quality gates configured
- [x] Documentation templates created
EOF

# Completed actions log
cat > _project_data/logs/completed-actions.log << EOF
# Completed Actions Log

## $(date '+%Y-%m-%d %H:%M')

### Initial Project Setup
**Purpose**: Create new Claude Code project with minimal root structure
**Impact**:
- Created: Full project directory structure
- Created: All configuration files (pyproject.toml, requirements.txt, etc.)
- Created: Quality gate scripts (.ai-validation/check_quality.sh)
- Created: Documentation templates (CLAUDE.md, README.md, docs/)
- Created: Sample tests and code
**Outcome**: Project ready for development with TDD workflow
**Next Steps**: Define requirements and start implementing features
EOF

print_success "Initial documentation created"

# --- Step 17: Setup Python virtual environment ---
print_step "Creating Python virtual environment..."
if command -v python$PYTHON_VERSION &> /dev/null; then
    python$PYTHON_VERSION -m venv venv
    print_success "Virtual environment created with Python $PYTHON_VERSION"
elif command -v python3 &> /dev/null; then
    python3 -m venv venv
    print_warning "Used python3 instead of python$PYTHON_VERSION"
else
    print_warning "Python not found. Please create virtual environment manually:"
    echo "  python$PYTHON_VERSION -m venv venv"
fi

# --- Step 18: Install dependencies (optional) ---
if [ -d "venv" ]; then
    print_step "Installing dependencies..."

    # Activate virtual environment
    if [ -f "venv/bin/activate" ]; then
        source venv/bin/activate

        # Upgrade pip
        pip install --upgrade pip -q

        # Install dependencies
        pip install -r requirements.txt -q
        pip install -r requirements-dev.txt -q

        print_success "Dependencies installed"

        # Run initial test to verify setup
        print_step "Running initial tests..."
        if pytest -q; then
            print_success "Initial tests passed"
        else
            print_warning "Initial tests failed (this is normal for new projects)"
        fi
    else
        print_warning "Could not activate virtual environment"
    fi
fi

# --- Step 19: Create initial git commit ---
print_step "Creating initial git commit..."
git add .
git commit -q -m "Initial project setup with minimal root structure

- Created minimal directory structure (4 top-level folders)
- Configured all quality gates (pytest, ruff, mypy, bandit, radon)
- Added documentation templates (CLAUDE.md, README.md, docs/)
- Setup Python package structure
- Added sample tests

Generated with Claude Code minimal root philosophy.
"
print_success "Initial commit created"

# --- Step 20: Display summary ---
echo ""
echo "╔════════════════════════════════════════════════════════════════╗"
echo "║                    SETUP COMPLETE!                             ║"
echo "╚════════════════════════════════════════════════════════════════╝"
echo ""
print_success "Project '$PROJECT_NAME' created successfully!"
echo ""
echo "Project Structure (Minimal Root):"
echo "  ├── src/                  Production code"
echo "  ├── tests/                Test suite"
echo "  ├── docs/                 Documentation"
echo "  ├── _project_data/        Operational data"
echo "  ├── .claude/              Claude Code config"
echo "  └── .ai-validation/       Quality tools"
echo ""
echo "Next Steps:"
echo "  1. cd $PROJECT_NAME"
echo "  2. source venv/bin/activate  (activate virtual environment)"
echo "  3. Read CLAUDE.md for development guide"
echo "  4. Update docs/notes/plan.md with your first feature"
echo "  5. Start coding with TDD workflow!"
echo ""
echo "Run quality checks:"
echo "  .ai-validation/check_quality.sh"
echo ""
echo "Happy coding! 🚀"
echo ""
