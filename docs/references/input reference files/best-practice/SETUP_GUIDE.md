# Claude Code Project Setup - Minimal Root Philosophy (v2.0)

> **Purpose**: Improved template for Claude Code projects emphasizing minimal root directory clutter
> **Version**: 2.0 (Refined based on community feedback)
> **Last Updated**: 2025-10-26
> **Philosophy**: Keep root clean, consolidate operational/ephemeral data, maximize clarity

---

## Version 2.0 Improvements

Based on professional feedback, this version addresses:

1. **Renamed `_project_data/` → `artifacts/`**
   - Removes underscore prefix confusion (Python "private" convention)
   - Uses industry-standard term
   - Clearer purpose for cross-language teams

2. **Configurable Migrations Placement**
   - Database projects: `migrations/` in root (Django/Alembic convention)
   - Non-database projects: `artifacts/migrations/` (minimal root)
   - Setup script asks which approach to use

3. **Configuration File Management Guidance**
   - Documentation on when to split `pyproject.toml`
   - Examples of split configurations
   - Best practices for large projects

---

## ⚡ Quick Start (2 Minutes)

**Just want to create a project right now?**

```bash
# 1. Navigate to the best-practice folder
cd best-practice

# 2. Run the setup script
./setup_project.sh my-project-name

# 3. Start developing
cd my-project-name
source venv/bin/activate
pytest  # Verify setup works
```

**That's it!** You now have a fully configured project with:
- ✅ Minimal root structure (4 folders)
- ✅ Quality gates configured
- ✅ Virtual environment with dependencies
- ✅ Sample tests passing
- ✅ CLAUDE.md with project standards

**Next steps**:
- Read the generated `CLAUDE.md` in your project
- Start with TDD: Write test → Implement → Validate
- Run quality gates: `bash .ai-validation/check_quality.sh`

**With options**:
```bash
# Database project (Django/Alembic)
./setup_project.sh --database my-django-app

# Specific Python version
./setup_project.sh --python 3.11 my-app

# Full options
./setup_project.sh --database --python 3.11 --author "Your Name" --email "you@example.com" my-app
```

**For full details**, continue reading below.

---

## Critique of Original Structure

### Problem: Too Many Top-Level Directories

The original structure creates **~14 top-level items**:

```
my-project/
├── src/                    # ✓ Essential
├── tests/                  # ✓ Essential
├── SPECIFICATION/          # ❌ Could consolidate
├── logs/                   # ❌ Operational data
├── temp/                   # ❌ Ephemeral data
├── scripts/                # ❌ Could move to src/
├── migrations/             # ⚠️ Depends on project type
├── config/                 # ❌ Usually empty, use pyproject.toml
├── import/                 # ❌ Operational data
├── output/                 # ❌ Operational data
├── .claude/                # ✓ Essential (hidden)
├── .ai-validation/         # ✓ Essential (hidden)
├── CLAUDE.md               # ✓ Essential
└── README.md               # ✓ Essential
```

**Issues**:
- Cognitive overload when navigating project
- Difficult to distinguish essential vs. operational folders
- Many folders empty or rarely used
- Inconsistent naming conventions

---

## Improved Structure: Minimal Root v2.0

### Core Principle: 4-5 Top-Level Folders + Hidden Config

```
my-project/
├── src/                    # Application source code
├── tests/                  # All tests (unit, integration, fixtures)
├── docs/                   # ALL documentation (design, schema, specs)
├── artifacts/              # ALL operational/ephemeral data (RENAMED!)
├── migrations/             # [OPTIONAL] DB migrations (root for convention)
├── .claude/                # Claude Code configuration (hidden)
├── .ai-validation/         # Quality tools (hidden)
├── .git/                   # Version control (hidden)
├── .gitignore
├── .env.example
├── CLAUDE.md               # Claude instructions
├── README.md               # Project overview
├── pyproject.toml          # Tool configuration
├── requirements.txt
└── requirements-dev.txt
```

**Key Changes from v1.0**:
- ✨ `_project_data/` → `artifacts/` (clearer naming)
- ✨ `migrations/` optionally in root for database projects
- ✨ Configuration guidance for large projects

**Benefits**:
- Root directory fits on one screen
- Clear separation: code, tests, docs, artifacts
- No underscore confusion
- Follows industry conventions where appropriate
- Easy to navigate for both humans and AI

---

## Detailed Structure

### 1. `src/` - Application Source Code

```
src/
├── __init__.py
├── main.py                 # Entry point
├── core/                   # Core business logic
│   ├── __init__.py
│   ├── models.py
│   └── utils.py
├── services/               # Service layer
│   ├── __init__.py
│   └── processor.py
├── adapters/               # External integrations (parsers, APIs)
│   ├── __init__.py
│   └── parser.py
└── infrastructure/         # Infrastructure concerns
    ├── __init__.py
    ├── database.py
    └── config.py
```

**Rules**:
- Production code only
- Well-organized by domain/layer
- No tests, no scripts, no data files
- Each module has `__init__.py`

### 2. `tests/` - All Testing Code

```
tests/
├── __init__.py
├── conftest.py             # Shared fixtures
├── unit/                   # Unit tests
│   ├── __init__.py
│   ├── test_models.py
│   └── test_utils.py
├── integration/            # Integration tests
│   ├── __init__.py
│   └── test_pipeline.py
└── fixtures/               # Test data
    ├── sample_data.json
    └── mock_responses.py
```

**Rules**:
- Mirror `src/` structure in `unit/`
- Integration tests for workflows
- Fixtures for reusable test data
- All test utilities here

### 3. `docs/` - All Documentation

```
docs/
├── design/                 # Design documents
│   ├── architecture.md
│   ├── data-flows.md
│   └── decisions/          # ADRs (Architecture Decision Records)
│       └── 001-use-postgres.md
├── schema/                 # Data definitions
│   ├── database-schema.md
│   ├── api-spec.yaml
│   └── data-models.md
├── notes/                  # Active development notes
│   ├── plan.md            # Current development plan
│   ├── todo.md            # Task list
│   └── ideas.md           # Future ideas
└── specifications/         # Requirements & specs
    ├── requirements.md
    ├── pending/           # Specs in progress
    └── completed/         # Implemented specs
```

**Rules**:
- Long-form documentation only
- Design decisions with rationale
- Schema and data model documentation
- Active notes separate from archived specs

### 4. `artifacts/` - Operational & Ephemeral Data (RENAMED!)

```
artifacts/
├── logs/                   # Application logs
│   ├── app.log
│   ├── completed-actions.log
│   └── 2025-10-26_bugfix.md
├── temp/                   # Temporary/scratch files
│   ├── debug_script.py
│   └── analysis.ipynb
├── input/                  # Input data files
│   └── sample_import.csv
├── output/                 # Generated outputs
│   └── report_2025-10.pdf
├── .archive/              # Old versions, backups
│   └── old_implementation_2024.py
└── migrations/            # [OPTIONAL] DB migrations if not in root
    ├── 001_initial_schema.sql
    └── 002_add_users.sql
```

**Rules**:
- All operational data here
- ⚠️ **Changed from `_project_data/`** (clearer name, no underscore)
- Can be excluded from version control (.gitignore)
- Scripts here are temporary, not production

**Why "artifacts"?**
- Industry-standard term (CI/CD, build systems)
- Clear purpose: generated/operational files
- No Python "private" connotation
- Works across programming languages

### 5. `migrations/` - Database Migrations (OPTIONAL, ROOT)

**For Database-Centric Projects (Django, Alembic, SQLAlchemy):**

```
migrations/                 # Root level (convention)
├── alembic.ini            # Alembic config
├── env.py                 # Alembic environment
├── versions/              # Migration files
│   ├── 001_initial_schema.py
│   └── 002_add_users.py
└── README.md              # Migration instructions
```

**When to Use Root `migrations/`:**
- ✅ Django projects (standard convention)
- ✅ Alembic/SQLAlchemy projects
- ✅ Database is central to application
- ✅ Migrations are version-controlled code

**When to Use `artifacts/migrations/`:**
- ✅ Non-database projects
- ✅ Simple SQL migration scripts
- ✅ Prefer minimal root directory
- ✅ Migrations are operational artifacts

**Setup Script Option:**
```bash
./setup_minimal_project.sh my-project --database
# Creates root migrations/ folder

./setup_minimal_project.sh my-project
# Creates artifacts/migrations/ folder
```

### 6. `.claude/` - Claude Code Configuration

```
.claude/
├── context/               # Context documentation for Claude
│   ├── architecture.md
│   ├── database.md
│   └── workflows.md
└── commands/              # Custom slash commands (future)
    └── review.md
```

**Rules**:
- Claude-specific context and configuration
- Keep context docs focused and concise
- Reference main docs/ for details

### 7. `.ai-validation/` - Quality Tools

```
.ai-validation/
├── check_quality.sh       # Main quality gate script
├── install_tools.sh       # Setup script for tools
└── pre-commit-config.yaml # Pre-commit hooks config
```

**Rules**:
- Quality enforcement scripts
- Installation/setup scripts
- CI/CD integration scripts

---

## File Placement Decision Tree

When creating a new file, ask:

1. **Is it production source code?**
   - YES → `src/`
   - NO → Continue

2. **Is it a test?**
   - YES → `tests/unit/` or `tests/integration/`
   - NO → Continue

3. **Is it documentation?**
   - Design/architecture → `docs/design/`
   - Schema/data models → `docs/schema/`
   - Requirements/specs → `docs/specifications/`
   - Active notes/plans → `docs/notes/`
   - NO → Continue

4. **Is it a database migration?**
   - Database-centric project → `migrations/` (root)
   - Simple SQL scripts → `artifacts/migrations/`
   - NO → Continue

5. **Is it operational/ephemeral?**
   - Log files → `artifacts/logs/`
   - Temporary scripts → `artifacts/temp/`
   - Input data → `artifacts/input/`
   - Output files → `artifacts/output/`
   - Old versions → `artifacts/.archive/`
   - NO → Continue

6. **Is it configuration?**
   - Python tools → `pyproject.toml`
   - Dependencies → `requirements.txt`
   - Environment → `.env.example`
   - Claude context → `.claude/context/`
   - Quality tools → `.ai-validation/`
   - NO → Continue

7. **Is it project documentation?**
   - Claude instructions → `CLAUDE.md` (root)
   - User-facing docs → `README.md` (root)
   - Coding standards → Include in `CLAUDE.md`

**If none of above**: Reconsider if file is necessary!

---

## Configuration File Management

### When to Use Single `pyproject.toml`

**Recommended for:**
- ✅ Small to medium projects (<10k lines)
- ✅ Standard tooling setup
- ✅ Python-only projects
- ✅ Modern Python practices (PEP 518)

**Benefits:**
- Single source of truth
- Easy to find all configuration
- Modern Python standard
- Better IDE support

**Example `pyproject.toml` (Full config ~300 lines):**
```toml
[project]
name = "my-project"

[tool.ruff]
line-length = 88

[tool.mypy]
strict = true

[tool.pytest.ini_options]
testpaths = ["tests"]

[tool.coverage.run]
source = ["src"]
```

### When to Split Configuration Files

**Consider splitting for:**
- ⚠️ Large projects (>10k lines)
- ⚠️ Complex tool configurations (>50 lines per tool)
- ⚠️ Multi-language projects
- ⚠️ Team with mixed tool preferences

**Split Configuration Approach:**

```
my-project/
├── pyproject.toml          # Minimal: project metadata only
├── mypy.ini               # MyPy configuration
├── pytest.ini             # Pytest configuration
├── .coveragerc            # Coverage configuration
├── ruff.toml              # Ruff configuration
└── .bandit               # Bandit configuration
```

**Benefits:**
- Easier to scan individual tool configs
- Can use tool-specific features
- Clearer git diffs for config changes

**Drawbacks:**
- Multiple files to maintain
- Harder to find "all configuration"
- Not the modern Python standard

### Recommendation: Start with pyproject.toml

```python
# Start with everything in pyproject.toml
# Split only when:
# 1. Individual tool configs exceed 100 lines
# 2. Team requests it
# 3. Tool requires specific config file
```

**Example: When to split MyPy**

If your MyPy config grows to this:

```toml
[tool.mypy]
python_version = "3.10"
strict = true
# ... 50 more lines of overrides for specific modules ...
# ... 30 more lines of plugin configs ...
# ... 20 more lines of exclusions ...
```

**Consider creating `mypy.ini`:**

```ini
[mypy]
python_version = 3.10
strict = True

[mypy-tests.*]
disallow_untyped_defs = False

[mypy-external_package.*]
ignore_missing_imports = True
```

**Document the decision in `docs/design/decisions/`!**

---

## Benefits of Minimal Root Structure

### 1. Cognitive Load Reduction
- New developers see 4-5 folders instead of 14
- Clear purpose for each top-level item
- Easy to remember structure

### 2. Better Git Diffs
- Fewer top-level changes
- Clearer organization of commits
- Less noise in file listings

### 3. Improved AI Assistance
- Claude can navigate structure faster
- Less ambiguity about file placement
- Better context window utilization

### 4. Scalability
- Structure scales to large projects
- Subfolders organize complexity
- Root stays clean regardless of size

### 5. Convention Alignment
- Follows modern Python project structure
- Similar to Rust (src/, tests/, docs/)
- Accommodates database conventions (migrations/)
- Familiar to experienced developers

### 6. Cross-Language Compatibility
- `artifacts/` is language-agnostic
- Structure works for Python, Go, Rust, TypeScript
- Clear separation of concerns

---

## Migration Guide

### From v1.0 (with `_project_data/`)

```bash
# Rename _project_data to artifacts
mv _project_data/ artifacts/

# If database project, move migrations to root
mkdir migrations
mv artifacts/migrations/* migrations/
rmdir artifacts/migrations

# Update all references
grep -r "_project_data" . --include="*.py" --include="*.md" --include="*.sh"
# Replace each occurrence with "artifacts"

# Update .gitignore
sed -i 's/_project_data/artifacts/g' .gitignore

# Update CLAUDE.md
sed -i 's/_project_data/artifacts/g' CLAUDE.md

# Update pyproject.toml exclusions
sed -i 's/_project_data/artifacts/g' pyproject.toml

# Commit changes
git add .
git commit -m "Rename _project_data to artifacts for clarity"
```

### From Legacy Structure (many root folders)

```bash
# Consolidate operational data
mkdir -p artifacts
mv logs/ artifacts/
mv temp/ artifacts/
mv import/ artifacts/input/
mv output/ artifacts/

# Consolidate documentation
mkdir -p docs
mv SPECIFICATION/ docs/specifications/
mkdir -p docs/notes docs/design docs/schema

# Handle migrations (database project)
# Option 1: Keep in root (Django/Alembic convention)
# migrations/ already exists - no change needed

# Option 2: Move to artifacts (minimal root)
mv migrations/ artifacts/

# Handle scripts
# If production: mv scripts/ src/scripts/
# If temporary: mv scripts/ artifacts/temp/

# Update all file references in code
find . -type f \( -name "*.py" -o -name "*.md" \) -exec sed -i 's|logs/|artifacts/logs/|g' {} +

# Update .gitignore paths
# Update CLAUDE.md with new structure
```

---

## Comparison: v1.0 vs v2.0

| Aspect | v1.0 | v2.0 | Improvement |
|--------|------|------|-------------|
| **Operational folder name** | `_project_data/` | `artifacts/` | ✅ Clearer, no underscore confusion |
| **Migrations placement** | Always in `_project_data/` | Configurable: root or artifacts | ✅ Follows conventions when needed |
| **Config management** | Single pyproject.toml | Guidance on when to split | ✅ Flexibility for large projects |
| **Root visible folders** | 4 | 4-5 (optional migrations/) | ✅ Still minimal |
| **Cross-language compatibility** | Good | Better | ✅ "artifacts" is universal |
| **Django/Alembic compatibility** | Breaks convention | Follows convention | ✅ Professional standards |

---

## Template Files

### Minimal CLAUDE.md (Updated)

```markdown
# CLAUDE.md - Development Guide

## Structure

- **Source**: `src/` - Production code only
- **Tests**: `tests/` - Unit and integration tests
- **Docs**: `docs/` - All documentation (design, schema, notes)
- **Artifacts**: `artifacts/` - Logs, temp, migrations, I/O
- **Migrations**: `migrations/` - [If database project] DB migrations

## File Placement Rules

1. Production code → `src/`
2. Tests → `tests/unit/` or `tests/integration/`
3. Documentation → `docs/design/`, `docs/schema/`, or `docs/notes/`
4. Logs → `artifacts/logs/`
5. Temporary scripts → `artifacts/temp/`
6. Input/output data → `artifacts/input/` or `artifacts/output/`
7. Database migrations:
   - Database project → `migrations/` (root)
   - Simple SQL → `artifacts/migrations/`

**NEVER create files in project root unless it's configuration!**

## Workflow

1. **Plan**: Update `docs/notes/plan.md`
2. **Test First**: Write test in `tests/`
3. **Implement**: Write code in `src/`
4. **Validate**: Run `.ai-validation/check_quality.sh`
5. **Log**: Add entry to `artifacts/logs/completed-actions.log`

## Quality Standards

- Functions ≤ 30 lines
- Test coverage ≥ 80%
- Zero linting/type errors
- All public functions have docstrings

## Before Committing

\`\`\`bash
.ai-validation/check_quality.sh
\`\`\`

All checks must pass!
```

---

## Conclusion

Version 2.0 improves upon v1.0 by:

1. **Clearer Naming**: `artifacts/` instead of `_project_data/`
2. **Flexible Migrations**: Supports both convention-based and minimal approaches
3. **Configuration Guidance**: Helps teams scale configuration management

This structure provides:

- **Clarity**: 4-5 folders with clear, distinct purposes
- **Efficiency**: Faster navigation for humans and AI
- **Scalability**: Works for projects of any size
- **Convention Alignment**: Respects industry standards when appropriate
- **Quality**: Built-in quality gates and TDD workflow

**Key Insight**: A minimal root doesn't mean rigid - it means intentional. We accommodate database conventions while maintaining the core philosophy of reducing clutter.

**Keep the root clean. Keep the code clean. Ship great software.**
