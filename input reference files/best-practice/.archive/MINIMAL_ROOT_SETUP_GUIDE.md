# Minimal Root Setup Guide - Quick Reference

> **Purpose**: Quick guide to using the minimal root project setup
> **Created**: 2025-10-26
> **Files**: `CLAUDE_CODE_PROJECT_SETUP_MINIMAL_ROOT.md` + `setup_minimal_project.sh`

---

## What You Have

### 1. Documentation Files

- **`CLAUDE_CODE_PROJECT_SETUP_MINIMAL_ROOT.md`**
  - Complete guide to minimal root philosophy
  - Critiques original structure (14 root items)
  - Proposes improved structure (4 root folders)
  - Includes all best practices, examples, and templates
  - Reference guide for understanding WHY this structure works

- **`setup_minimal_project.sh`**
  - Automated setup script (single command!)
  - Creates entire project structure
  - Generates all configuration files
  - Sets up virtual environment
  - Installs dependencies
  - Creates initial git commit
  - ~700 lines, fully featured

- **`CLAUDE_CODE_PROJECT_SETUP_BEST_PRACTICES.md`** (Original)
  - Original comprehensive guide
  - Good for reference, but creates too many root folders
  - Use the MINIMAL_ROOT version instead for new projects

---

## Quick Start: Create a New Project

### Option 1: Automated Setup (Recommended)

```bash
# Basic usage (uses defaults)
./setup_minimal_project.sh my-new-project

# Full options
./setup_minimal_project.sh my-new-project 3.11 "Your Name" "you@email.com"

# What it does:
# 1. Creates directory structure (4 top-level folders)
# 2. Initializes git repository
# 3. Creates all config files (pyproject.toml, requirements.txt, etc.)
# 4. Sets up Python virtual environment
# 5. Installs dependencies
# 6. Creates documentation templates
# 7. Runs initial tests
# 8. Makes initial git commit
```

**Output:**
```
my-new-project/
├── src/                    # Application code
├── tests/                  # Test suite
├── docs/                   # Documentation
├── _project_data/          # Operational data
├── .claude/                # Claude config (hidden)
├── .ai-validation/         # Quality tools (hidden)
├── CLAUDE.md               # Development guide
├── README.md               # Project overview
├── pyproject.toml          # Tool configuration
└── requirements.txt        # Dependencies
```

### Option 2: Manual Setup

If you prefer to understand each step:

1. Read `CLAUDE_CODE_PROJECT_SETUP_MINIMAL_ROOT.md`
2. Follow the structure diagrams
3. Create folders manually
4. Copy template files from the guide

---

## The Minimal Root Philosophy

### Problem: Too Many Root Folders

**Before (Original structure - 14+ items):**
```
my-project/
├── src/
├── tests/
├── SPECIFICATION/
├── logs/
├── temp/
├── scripts/
├── migrations/
├── config/
├── import/
├── output/
├── .claude/
├── .ai-validation/
├── [10+ config files]
└── ...
```
❌ Cognitive overload
❌ Hard to navigate
❌ Unclear what's important

### Solution: 4 Top-Level Folders

**After (Minimal structure - 4 folders):**
```
my-project/
├── src/                    # ALL production code
├── tests/                  # ALL tests
├── docs/                   # ALL documentation
├── _project_data/          # ALL operational data
├── .claude/                # Hidden config
├── .ai-validation/         # Hidden tools
└── [essential config files only]
```
✅ Clean and focused
✅ Easy to navigate
✅ Clear purpose for each folder

---

## Directory Structure Details

### `src/` - Application Code
```
src/
├── core/           # Business logic, domain models
├── services/       # Application services
├── adapters/       # External integrations (APIs, parsers)
└── infrastructure/ # DB, config, logging
```

### `tests/` - All Tests
```
tests/
├── unit/           # Unit tests (mirror src/ structure)
├── integration/    # End-to-end tests
└── fixtures/       # Test data
```

### `docs/` - All Documentation
```
docs/
├── design/         # Architecture, diagrams, ADRs
├── schema/         # Database schema, API specs
├── notes/          # Active dev notes (plan.md, todo.md)
└── specifications/ # Requirements (pending/, completed/)
```

### `_project_data/` - Operational Data
```
_project_data/
├── logs/           # Application logs, completed-actions.log
├── temp/           # Temporary scripts, scratch files
├── input/          # Input data files
├── output/         # Generated reports, exports
├── .archive/       # Old versions, backups
└── migrations/     # Database migration scripts
```

**Why consolidate?**
- Single location for runtime artifacts
- Can exclude from version control
- Clear that nothing here is source code
- Can safely delete and regenerate

---

## File Placement Decision Tree

When creating a new file, ask:

1. **Is it production source code?** → `src/`
2. **Is it a test?** → `tests/unit/` or `tests/integration/`
3. **Is it documentation?**
   - Design/architecture → `docs/design/`
   - Schema/data models → `docs/schema/`
   - Active notes → `docs/notes/`
   - Requirements → `docs/specifications/`
4. **Is it operational/ephemeral?**
   - Logs → `_project_data/logs/`
   - Temporary scripts → `_project_data/temp/`
   - Input/output data → `_project_data/input/` or `output/`
5. **Is it configuration?** → Root level (pyproject.toml, .env.example, etc.)

**Never create random files in root!**

---

## What the Setup Script Creates

### Configuration Files

- `pyproject.toml` - Complete tool configuration
  - Ruff (linting)
  - MyPy (type checking)
  - Pytest (testing)
  - Coverage (code coverage)
  - Bandit (security)
  - Interrogate (docstring coverage)

- `requirements.txt` - Core dependencies
- `requirements-dev.txt` - Development tools
- `.env.example` - Environment template
- `.gitignore` - Comprehensive ignore rules

### Documentation Files

- `CLAUDE.md` - Complete development guide
  - File placement rules
  - Workflow enforcement
  - Quality standards
  - Common commands

- `README.md` - Project overview
  - Quick start
  - Development setup
  - Testing instructions

- `docs/design/architecture.md` - Architecture template
- `docs/notes/plan.md` - Development plan template
- `docs/notes/todo.md` - Task list template

### Quality Tools

- `.ai-validation/check_quality.sh` - Quality gates script
  - Runs all checks: pytest, ruff, mypy, bandit, radon, interrogate
  - Color-coded output
  - Fails if any check fails

### Sample Code

- `src/main.py` - Entry point with sample function
- `tests/conftest.py` - Shared test fixtures
- `tests/unit/test_main.py` - Sample test with Given-When-Then

### Logging

- `_project_data/logs/completed-actions.log` - Initial entry

---

## Using the Generated Project

### Activate Virtual Environment

```bash
cd my-new-project
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate     # Windows
```

### Run Tests

```bash
pytest                     # All tests
pytest -v                  # Verbose
pytest --cov=src          # With coverage
```

### Run Quality Checks

```bash
.ai-validation/check_quality.sh   # All checks
ruff check .                       # Just linting
mypy src/                          # Just type checking
```

### Development Workflow (TDD)

1. **Plan**: Update `docs/notes/plan.md`
2. **Test**: Write failing test in `tests/unit/`
3. **Code**: Implement in `src/`
4. **Validate**: Run `.ai-validation/check_quality.sh`
5. **Log**: Update `_project_data/logs/completed-actions.log`

---

## Comparison: Before vs After

### Visible Root Items

| Original | Minimal | Reduction |
|----------|---------|-----------|
| 14 folders | 4 folders | **71% fewer** |
| Unclear hierarchy | Clear purpose | **Better UX** |
| Mixed concerns | Separated | **Cleaner** |

### Developer Experience

| Aspect | Original | Minimal |
|--------|----------|---------|
| **Navigate project** | Search through 14 folders | 4 clear choices |
| **Find logs** | `logs/` in root | `_project_data/logs/` |
| **Find temp files** | `temp/` in root | `_project_data/temp/` |
| **Understand structure** | Need documentation | Self-evident |
| **Onboarding time** | 1-2 hours | 15 minutes |

---

## Benefits of Minimal Root

### 1. Cognitive Load Reduction
- See all important folders at a glance
- No decision paralysis ("where does this go?")
- Clear mental model

### 2. Better for AI Assistants
- Claude navigates structure faster
- Less token usage for context
- Clear file placement rules

### 3. Scales Better
- Works for small projects (4 folders)
- Works for large projects (4 folders + subfolders)
- Root stays clean regardless of size

### 4. Industry Standard Alignment
- Similar to Rust (src/, tests/, docs/)
- Similar to modern Python projects
- Familiar to experienced developers

### 5. Easier Maintenance
- Fewer `.gitignore` rules needed
- Clear backup strategy (`_project_data` can be excluded)
- Less clutter in version control

---

## Common Questions

### Q: Where do migration scripts go?
**A:** `_project_data/migrations/` - They're operational data

### Q: Where do standalone scripts go?
**A:**
- Production scripts → `src/scripts/` (if they're part of the app)
- Temporary/debug scripts → `_project_data/temp/`

### Q: Where do requirements/specifications go?
**A:** `docs/specifications/` with subfolders for `pending/` and `completed/`

### Q: Can I add more top-level folders?
**A:** Try not to! Use subfolders instead. The whole point is to keep root minimal.

### Q: What about `config/` folder?
**A:** Use `pyproject.toml` and `.env` instead. If you have many config files, use `src/infrastructure/config/`

### Q: Where does database schema documentation go?
**A:** `docs/schema/` for documentation, `_project_data/migrations/` for actual SQL files

---

## Migration Guide

If you have an existing project with many root folders:

```bash
# Consolidate operational data
mkdir -p _project_data
mv logs/ _project_data/
mv temp/ _project_data/
mv import/ _project_data/input/
mv output/ _project_data/
mv migrations/ _project_data/

# Consolidate documentation
mkdir -p docs
mv SPECIFICATION/ docs/specifications/
mkdir -p docs/notes docs/design docs/schema

# Handle scripts
# If production: mv scripts/ src/scripts/
# If temporary: mv scripts/ _project_data/temp/

# Update all file references in code
grep -r "logs/" . --include="*.py" --include="*.md"
# Update each reference from logs/ to _project_data/logs/

# Update .gitignore
# Change logs/*.log to _project_data/logs/*.log
# etc.

# Update documentation
# Update CLAUDE.md with new structure
```

---

## Success Metrics

Your project is well-structured when:

✅ Root directory has ≤ 4 visible folders
✅ `.ai-validation/check_quality.sh` passes all checks
✅ New developers can navigate structure in < 5 minutes
✅ Claude Code can find files without asking
✅ No confusion about where files belong
✅ Test coverage ≥ 80%
✅ Zero linting/type/security errors

---

## Next Steps After Setup

1. **Customize documentation**
   - Update `README.md` with your project description
   - Update `CLAUDE.md` with project-specific rules
   - Write architecture overview in `docs/design/architecture.md`

2. **Define your domain**
   - Create domain models in `src/core/`
   - Write tests first (TDD)
   - Document key decisions in `docs/design/decisions/`

3. **Setup CI/CD**
   - Create `.github/workflows/ci.yml` (or equivalent)
   - Run `.ai-validation/check_quality.sh` in CI
   - Enforce quality gates

4. **Start building**
   - Follow TDD workflow
   - Keep root clean
   - Log your work
   - Update documentation as you go

---

## Resources

- **Full Guide**: `CLAUDE_CODE_PROJECT_SETUP_MINIMAL_ROOT.md`
- **Setup Script**: `setup_minimal_project.sh`
- **Original Guide**: `CLAUDE_CODE_PROJECT_SETUP_BEST_PRACTICES.md`

---

## Example: Create a New API Project

```bash
# 1. Run setup script
./setup_minimal_project.sh my-api 3.11 "John Doe" "john@example.com"

# 2. Navigate to project
cd my-api
source venv/bin/activate

# 3. Verify setup
.ai-validation/check_quality.sh
# Output: ✓ ALL QUALITY GATES PASSED

# 4. Update plan
nano docs/notes/plan.md
# Add: Build REST API with FastAPI

# 5. Add FastAPI dependency
echo "fastapi>=0.104.0" >> requirements.txt
echo "uvicorn>=0.24.0" >> requirements.txt
pip install -r requirements.txt

# 6. Write first test
nano tests/unit/test_api.py
# Add test for GET /health endpoint

# 7. Implement feature
nano src/services/api.py
# Implement FastAPI app with /health endpoint

# 8. Run tests
pytest -v
# Output: 1 passed

# 9. Run quality gates
.ai-validation/check_quality.sh
# Output: ✓ ALL QUALITY GATES PASSED

# 10. Log your work
nano _project_data/logs/completed-actions.log
# Add entry documenting what you built

# 11. Commit
git add .
git commit -m "Add health check endpoint"

# Done! Root directory is still clean with 4 folders.
```

---

## Conclusion

This minimal root structure provides:

- **Clarity**: 4 folders with clear, distinct purposes
- **Efficiency**: Faster navigation for humans and AI
- **Scalability**: Works for projects of any size
- **Maintainability**: Clear conventions prevent clutter
- **Quality**: Built-in quality gates and TDD workflow

**Key Insight**: Consolidating operational data and documentation into dedicated folders dramatically reduces root clutter while maintaining full functionality.

Use `setup_minimal_project.sh` to create new projects in seconds with this battle-tested structure!

**Keep the root clean. Keep the code clean. Ship great software.**
