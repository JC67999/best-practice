# Claude Code Project Setup - Minimal Root Philosophy

> **Purpose**: Improved template for Claude Code projects emphasizing minimal root directory clutter
> **Last Updated**: 2025-10-26
> **Philosophy**: Keep root clean, consolidate operational/ephemeral data, maximize clarity

---

## Critique of Original Structure

### Problem: Too Many Top-Level Directories

The original `CLAUDE_CODE_PROJECT_SETUP_BEST_PRACTICES.md` creates **~14 top-level items**:

```
my-project/
├── src/                    # ✓ Essential
├── tests/                  # ✓ Essential
├── SPECIFICATION/          # ❌ Could consolidate
├── logs/                   # ❌ Operational data
├── temp/                   # ❌ Ephemeral data
├── scripts/                # ❌ Could move to src/
├── migrations/             # ❌ Could consolidate
├── config/                 # ❌ Usually empty, use pyproject.toml
├── import/                 # ❌ Operational data
├── output/                 # ❌ Operational data
├── .claude/                # ✓ Essential (hidden)
├── .ai-validation/         # ✓ Essential (hidden)
├── CLAUDE.md               # ✓ Essential
├── README.md               # ✓ Essential
└── [10+ more files]
```

**Issues**:
- Cognitive overload when navigating project
- Difficult to distinguish essential vs. operational folders
- Many folders empty or rarely used
- Inconsistent naming conventions (SPECIFICATION vs. scripts)

---

## Improved Structure: Minimal Root

### Core Principle: 4 Top-Level Folders + Hidden Config

```
my-project/
├── src/                    # Application source code
├── tests/                  # All tests (unit, integration, fixtures)
├── docs/                   # ALL documentation (design, schema, specs)
├── _project_data/          # ALL operational/ephemeral data
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

**Benefits**:
- Root directory fits on one screen
- Clear separation: code, tests, docs, data
- Easy to navigate for both humans and AI
- Hidden folders don't clutter `ls` output
- Consistent with modern project conventions

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
- All test utilities here (no root-level test scripts)

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

### 4. `_project_data/` - Operational & Ephemeral Data

```
_project_data/
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
└── migrations/            # Database migrations
    ├── 001_initial_schema.sql
    └── 002_add_users.sql
```

**Rules**:
- All operational data here
- Prefix with `_` to de-prioritize visually
- Can be excluded from version control (.gitignore)
- Scripts here are temporary, not production

**Why Consolidate?**
- Single location for all runtime artifacts
- Easy to exclude from backups/sync
- Clear that nothing here is source code
- Can safely delete and regenerate

### 5. `.claude/` - Claude Code Configuration

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

### 6. `.ai-validation/` - Quality Tools

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

4. **Is it operational/ephemeral?**
   - Log files → `_project_data/logs/`
   - Temporary scripts → `_project_data/temp/`
   - Input data → `_project_data/input/`
   - Output files → `_project_data/output/`
   - Old versions → `_project_data/.archive/`
   - Database migrations → `_project_data/migrations/`
   - NO → Continue

5. **Is it configuration?**
   - Python tools → `pyproject.toml`
   - Dependencies → `requirements.txt`
   - Environment → `.env.example`
   - Claude context → `.claude/context/`
   - Quality tools → `.ai-validation/`
   - NO → Continue

6. **Is it project documentation?**
   - Claude instructions → `CLAUDE.md` (root)
   - User-facing docs → `README.md` (root)
   - Coding standards → Include in `CLAUDE.md`

**If none of above**: Reconsider if file is necessary!

---

## Documentation Strategy

### Three Tiers of Documentation

#### Tier 1: Root Documentation (Immediate Context)
- `README.md` - What is this project?
- `CLAUDE.md` - How to work with this project?

Keep these concise (<300 lines each). Link to deeper docs.

#### Tier 2: `.claude/context/` (AI Context)
- Focused context for Claude Code
- 200-500 lines per file
- Optimized for token efficiency
- References Tier 3 for details

#### Tier 3: `docs/` (Deep Documentation)
- Comprehensive design documents
- Detailed specifications
- Full schema documentation
- Can be longer, more detailed

**Rationale**: Claude reads root → .claude/context → docs/ as needed. This minimizes token usage while maintaining accessibility.

---

## Benefits of Minimal Root Structure

### 1. Cognitive Load Reduction
- New developers see 4 folders instead of 14
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
- Familiar to experienced developers

---

## Migration from Legacy Structure

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
mkdir -p docs/notes

# Move scripts into src or temp
# If production scripts:
mv scripts/ src/scripts/
# If temporary/utility scripts:
mv scripts/ _project_data/temp/

# Update references in code and documentation
# Update .gitignore paths
# Update CLAUDE.md with new structure
```

---

## Comparison: Before vs. After

### Before (14 items in root)
```
ls -1
.ai-validation/
.claude/
.git/
SPECIFICATION/
config/
import/
logs/
migrations/
output/
scripts/
src/
temp/
tests/
CLAUDE.md
README.md
pyproject.toml
requirements.txt
```

### After (8 items in root, 3 hidden)
```
ls -1
_project_data/
docs/
src/
tests/
CLAUDE.md
README.md
pyproject.toml
requirements.txt

ls -1a  # Including hidden
.ai-validation/
.claude/
.git/
.gitignore
.env.example
_project_data/
docs/
src/
tests/
CLAUDE.md
README.md
pyproject.toml
requirements.txt
requirements-dev.txt
```

**50% reduction in visible root items!**

---

## Quality Gates & Tooling

(Same as original guide - no changes needed)

### pyproject.toml
```toml
[project]
name = "my-project"
version = "0.1.0"
requires-python = ">=3.10"

[tool.ruff]
line-length = 88
target-version = "py310"
src = ["src", "tests"]  # Updated for new structure

[tool.pytest.ini_options]
testpaths = ["tests"]
addopts = [
    "-v",
    "--strict-markers",
    "--cov=src",
    "--cov-report=term-missing",
    "--cov-fail-under=80"
]

[tool.coverage.run]
source = ["src"]
omit = ["*/tests/*", "*/venv/*"]
```

---

## Development Workflow

(Same TDD cycle as original, no changes)

---

## Quick Start Checklist

### Phase 1: Foundation (10 minutes)

- [ ] Run `setup_project.sh <project-name>` (see next section)
- [ ] Verify structure: `tree -L 2 -a`
- [ ] Initialize virtual environment
- [ ] Install dependencies
- [ ] Test quality gates: `.ai-validation/check_quality.sh`

### Phase 2: Documentation (20 minutes)

- [ ] Write `README.md` (what, why, how)
- [ ] Write `CLAUDE.md` (structure, rules, workflow)
- [ ] Create initial plan in `docs/notes/plan.md`
- [ ] Add architecture overview to `docs/design/architecture.md`

### Phase 3: Core Setup (30 minutes)

- [ ] Create first module in `src/core/`
- [ ] Write first test in `tests/unit/`
- [ ] Verify test runs and passes
- [ ] Run quality gates, ensure all pass

### Phase 4: Development

- [ ] Follow TDD workflow
- [ ] Keep root clean (files go in subdirectories)
- [ ] Log work to `_project_data/logs/completed-actions.log`
- [ ] Update docs as you go

---

## Template Files

### Minimal README.md

```markdown
# Project Name

Brief description (1-2 sentences).

## Quick Start

\`\`\`bash
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
pytest
\`\`\`

## Structure

- `src/` - Application code
- `tests/` - Test suite
- `docs/` - Documentation
- `_project_data/` - Logs, temp files, data

## Documentation

- `CLAUDE.md` - Development guide
- `docs/design/architecture.md` - System design
- `docs/notes/plan.md` - Current development plan
```

### Minimal CLAUDE.md

```markdown
# CLAUDE.md - Development Guide

## Structure

- **Source**: `src/` - Production code only
- **Tests**: `tests/` - Unit and integration tests
- **Docs**: `docs/` - All documentation (design, schema, notes)
- **Data**: `_project_data/` - Logs, temp, migrations, I/O

## File Placement Rules

1. Production code → `src/`
2. Tests → `tests/unit/` or `tests/integration/`
3. Documentation → `docs/design/`, `docs/schema/`, or `docs/notes/`
4. Logs → `_project_data/logs/`
5. Temporary scripts → `_project_data/temp/`
6. Input/output data → `_project_data/input/` or `_project_data/output/`

**NEVER create files in project root unless it's configuration (pyproject.toml, etc.)**

## Workflow

1. **Plan**: Update `docs/notes/plan.md`
2. **Test First**: Write test in `tests/`
3. **Implement**: Write code in `src/`
4. **Validate**: Run `.ai-validation/check_quality.sh`
5. **Log**: Add entry to `_project_data/logs/completed-actions.log`

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

This minimal root structure provides:

- **Clarity**: 4 top-level folders with clear purposes
- **Scalability**: Structure works for small and large projects
- **Efficiency**: Reduced cognitive load and faster navigation
- **Maintainability**: Clear conventions prevent clutter
- **AI-Friendly**: Optimized for Claude Code navigation

**Remember**: When in doubt, use subdirectories. Keep the root clean!

---

## Appendix: Structure Visualization

```
my-project/                          # ROOT (Minimal!)
│
├── src/                             # All production code
│   ├── core/                        # Business logic
│   ├── services/                    # Services layer
│   ├── adapters/                    # External integrations
│   └── infrastructure/              # DB, config, etc.
│
├── tests/                           # All testing
│   ├── unit/                        # Unit tests
│   ├── integration/                 # Integration tests
│   └── fixtures/                    # Test data
│
├── docs/                            # All documentation
│   ├── design/                      # Architecture & design
│   ├── schema/                      # Data models & APIs
│   ├── notes/                       # Active dev notes
│   └── specifications/              # Requirements
│
├── _project_data/                   # All operational data
│   ├── logs/                        # Application logs
│   ├── temp/                        # Scratch files
│   ├── input/                       # Input data
│   ├── output/                      # Generated files
│   ├── .archive/                    # Old versions
│   └── migrations/                  # DB migrations
│
├── .claude/                         # Claude Code config (hidden)
│   └── context/                     # AI context docs
│
├── .ai-validation/                  # Quality tools (hidden)
│   └── check_quality.sh
│
├── CLAUDE.md                        # Claude instructions
├── README.md                        # Project overview
├── pyproject.toml                   # Tool configuration
├── requirements.txt                 # Dependencies
└── requirements-dev.txt             # Dev dependencies
```

**Clean. Simple. Effective.**
