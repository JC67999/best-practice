# Claude Code Best Practice Setup (v2.0)

> **Complete system for creating minimal, well-structured Claude Code projects**
> **Version**: 2.0.0
> **Last Updated**: 2025-10-26

---

## 📦 What's in This Folder

### Active Files (Latest Versions)

### Essential Files Only

#### 1. **USE_CLAUDE_CODE.md** (28KB) ⭐ **READ THIS FIRST**
   - **THE definitive guide for effective AI-assisted development**
   - **Golden Rule: Reference, don't paste** (most crucial takeaway)
   - Quality gates integration (run master script before commits)
   - TDD cycle with Claude (4-phase workflow)
   - Safety protocols and Git workflow (trust Git, verify everything)
   - Advanced features (multi-agent, Task agent, Explore agent)
   - Custom commands and workflows (reusable templates)
   - Common mistakes to avoid (7 mistakes with solutions)
   - File operations best practices (create, edit, delete safely)

#### 2. **SETUP_GUIDE.md** (18KB)
   - Complete minimal root philosophy
   - Reduces clutter: 14 folders → 4 folders (`src/`, `tests/`, `docs/`, `artifacts/`)
   - File placement decision tree (where does every file go?)
   - Configuration management guidance (when to split pyproject.toml)
   - v2.0 improvements: `artifacts/` naming, configurable migrations

#### 3. **setup_project.sh** (44KB, executable)
   - Automated setup script - creates complete project in seconds
   - Options: `--database`, `--python VERSION`, `--author NAME`, `--email EMAIL`
   - Generates: pyproject.toml, requirements.txt, .gitignore, quality scripts
   - Creates: Complete directory structure, CLAUDE.md, sample tests
   - Installs: Dependencies, runs initial tests

#### 4. **README.md** (This file)
   - Quick reference and file index

### Archived Files (.archive/)

**Historical versions and changelogs** (reference only):
- `SETUP_CHANGELOG.md` - Setup version history (v1.0 → v2.0)
- `USE_CHANGELOG.md` - Usage guide version history (v1.0 → v1.1)
- `CLAUDE_CODE_PROJECT_SETUP_BEST_PRACTICES.md` - Original setup guide (v0)
- `CLAUDE_CODE_PROJECT_SETUP_MINIMAL_ROOT.md` - Setup guide v1.0
- `MINIMAL_ROOT_SETUP_GUIDE.md` - Quick reference v1.0
- `setup_minimal_project.sh` - Setup script v1.0
- `CLAUDE_CODE_USAGE_BEST_PRACTICES_V1.0.md` - Usage guide v1.0
- `IMPROVEMENTS_MADE.md` - Original improvement analysis

---

## 🚀 Quick Start

### Create a New Project

```bash
# Basic usage
./setup_project.sh my-new-project

# With options
./setup_project.sh --database my-django-app --python 3.11 --author "Your Name" --email "you@email.com"

# See all options
./setup_project.sh --help
```

### What Gets Created

```
my-new-project/
├── src/                    # Production code
├── tests/                  # Test suite
├── docs/                   # Documentation
├── artifacts/              # Operational data (logs, temp, I/O)
├── migrations/             # [Optional with --database] DB migrations
├── .claude/                # Claude Code config
├── .ai-validation/         # Quality tools
├── CLAUDE.md               # Development guide
├── README.md               # Project overview
├── pyproject.toml          # Tool configuration
└── requirements.txt        # Dependencies
```

---

## 🎯 Key Features

### v2.0 Improvements

1. **Better Naming**: `artifacts/` instead of `_project_data/`
   - No underscore confusion
   - Industry-standard term
   - Cross-language compatibility

2. **Flexible Migrations**: `--database` flag
   - Root `migrations/` for Django/Alembic projects
   - `artifacts/migrations/` for simple SQL scripts
   - Respects professional conventions

3. **Configuration Guidance**: When to split `pyproject.toml`
   - Comments in generated file
   - Guidelines for large projects
   - Examples of split configurations

### Core Features (v1.0 + v2.0)

- ✅ **Minimal Root**: 4-5 folders (71% reduction from typical 14+)
- ✅ **Complete Tooling**: Ruff, MyPy, Pytest, Bandit, Radon, Interrogate
- ✅ **Quality Gates**: Single script runs all checks
- ✅ **TDD Ready**: Sample tests, fixtures, pytest config
- ✅ **Documentation**: CLAUDE.md, README.md, docs/ templates
- ✅ **Git Ready**: .gitignore, initial commit
- ✅ **Virtual Environment**: Automatic setup and dependency installation

---

## 📖 Documentation

### Reading Order

1. **Start Here**: `README.md` (this file) - Overview and quick start
2. **Deep Dive**: `SETUP_GUIDE.md` - Full philosophy
3. **History**: `CHANGELOG.md` - Version changes and migration

### Key Concepts

**Minimal Root Philosophy**:
- Keep root directory clean (4-5 folders)
- Consolidate operational data in `artifacts/`
- Separate concerns clearly
- Optimize for both human and AI navigation

**File Placement Rules**:
1. Production code → `src/`
2. Tests → `tests/`
3. Documentation → `docs/`
4. Migrations → `migrations/` (database) or `artifacts/migrations/` (minimal)
5. Operational data → `artifacts/`

**Quality Standards**:
- Functions ≤ 30 lines
- Test coverage ≥ 80%
- Zero linting/type/security errors
- All public functions documented

---

## 🔧 Usage Examples

### Standard Python Project

```bash
./setup_project.sh my-api --python 3.11
cd my-api
source venv/bin/activate
.ai-validation/check_quality.sh
```

### Django/Database Project

```bash
./setup_project.sh --database my-django-app --python 3.11
cd my-django-app
source venv/bin/activate

# Migrations are in root migrations/ folder (convention)
alembic revision --autogenerate -m "initial"
alembic upgrade head
```

### CLI Tool

```bash
./setup_project.sh my-cli-tool
cd my-cli-tool
# Add entry point in pyproject.toml [project.scripts]
# Implement in src/main.py
```

---

## 📊 Comparison

| Aspect | Typical Structure | v1.0 | v2.0 |
|--------|-------------------|------|------|
| **Root folders** | 14+ | 4 | 4-5 |
| **Operational folder** | `logs/`, `temp/`, etc. | `_project_data/` | `artifacts/` |
| **Migrations** | `migrations/` | `_project_data/migrations/` | Configurable |
| **Config management** | Multiple files | Single `pyproject.toml` | Single + guidance |
| **Setup time** | 30+ min manual | 2 min automated | 2 min automated |
| **Quality gates** | Manual | Automated | Automated |

---

## 🛠️ Script Options

### Command Line Flags

```bash
--database          # Create root migrations/ folder (Django/Alembic)
--python VERSION    # Python version (default: 3.10)
--author NAME       # Author name for pyproject.toml
--email EMAIL       # Author email
-h, --help          # Show help message
```

### Examples

```bash
# Minimal
./setup_project.sh my-project

# Full options
./setup_project.sh \
  --database \
  --python 3.11 \
  --author "Jane Doe" \
  --email "jane@example.com" \
  my-django-project

# Help
./setup_project.sh --help
```

---

## 🔄 Upgrading from v1.0

### Quick Migration

```bash
# 1. Rename _project_data to artifacts
mv _project_data/ artifacts/

# 2. Update all references
find . -type f \( -name "*.py" -o -name "*.md" -o -name "*.sh" \) \
  -exec sed -i 's/_project_data/artifacts/g' {} +

# 3. Update config files
sed -i 's/_project_data/artifacts/g' .gitignore
sed -i 's/_project_data/artifacts/g' pyproject.toml

# 4. (Optional) Move migrations to root if database project
mkdir migrations
mv artifacts/migrations/* migrations/
rmdir artifacts/migrations

# 5. Commit
git add .
git commit -m "Upgrade to v2.0: artifacts/ and configurable migrations"
```

See `CHANGELOG.md` for detailed migration guide.

---

## 📐 Structure Philosophy

### Why Minimal Root?

**Problems with Many Root Folders**:
- ❌ Cognitive overload (14+ folders)
- ❌ Unclear what's important
- ❌ Mixed concerns (code, logs, temp files all at same level)
- ❌ Difficult to navigate

**Benefits of 4-5 Folders**:
- ✅ Fits on one screen
- ✅ Clear purpose for each folder
- ✅ Easy for humans to navigate
- ✅ Efficient for AI assistants
- ✅ Scales to any project size

### Why "artifacts/"?

**v1.0 used `_project_data/`**:
- ⚠️ Underscore suggests "private" (Python convention)
- ⚠️ Confusing for non-Python developers
- ⚠️ Not widely recognized term

**v2.0 uses `artifacts/`**:
- ✅ Industry standard (CI/CD, build systems)
- ✅ Clear purpose: generated/operational files
- ✅ No language-specific connotations
- ✅ Widely recognized across teams

### Why Configurable Migrations?

**v1.0**: Always in `_project_data/migrations/`
- ⚠️ Breaks Django convention (expects root `migrations/`)
- ⚠️ Breaks Alembic convention (expects root `migrations/`)
- ⚠️ Confuses experienced developers

**v2.0**: Configurable with `--database` flag
- ✅ Database projects: root `migrations/` (convention)
- ✅ Non-database projects: `artifacts/migrations/` (minimal)
- ✅ Respects professional standards
- ✅ Maintains minimal root when appropriate

---

## 🎓 Best Practices

### When to Use This Structure

✅ **Perfect for**:
- New Python projects
- API servers (FastAPI, Flask, Django)
- CLI tools
- Data processing pipelines
- Libraries and packages
- AI-assisted development

⚠️ **Consider alternatives for**:
- Legacy projects with established structure
- Monorepos (may need adaptation)
- Very small scripts (<100 lines)
- Projects with strict organizational standards

### Development Workflow

1. **Plan**: Update `docs/notes/plan.md`
2. **Test First**: Write test in `tests/`
3. **Implement**: Write code in `src/`
4. **Validate**: Run `.ai-validation/check_quality.sh`
5. **Log**: Update `artifacts/logs/completed-actions.log`
6. **Commit**: Clear commit message

### Working with Claude Code

- `CLAUDE.md` is your contract with AI
- Keep it current and concise
- Use `.claude/context/` for detailed context
- Follow file placement rules strictly
- Claude navigates minimal structure faster

---

## 🐛 Troubleshooting

### Common Issues

**Q: Script fails with "python3.10 not found"**
```bash
# Install Python 3.10 first, or use existing version:
./setup_project.sh my-project --python 3.11
```

**Q: Quality gates fail on fresh project**
```bash
# This is normal if you haven't added docstrings yet
# Fix by adding Google-style docstrings to public functions
```

**Q: Should I use --database flag?**
```bash
# Use --database if:
- Building Django app
- Using SQLAlchemy with Alembic
- Database is core to your application

# Don't use --database if:
- Simple SQL migration scripts
- Non-database project
- Prefer minimal root
```

**Q: When should I split pyproject.toml?**
```bash
# Consider splitting when:
- Individual tool configs exceed 100 lines
- Project exceeds 10k lines of code
- Team requests separate configs
- Tool requires specific config file

# Until then, keep single pyproject.toml (modern standard)
```

---

## 📚 Additional Resources

### Documentation Files

- `SETUP_GUIDE.md` - Complete guide
- `CHANGELOG.md` - Version history and migration
- `.archive/` - Historical v1.0 files for reference

### Generated Documentation

When you create a project, you'll get:
- `CLAUDE.md` - Project-specific development guide
- `README.md` - Project overview
- `docs/design/architecture.md` - Architecture template
- `docs/notes/plan.md` - Development plan
- `docs/notes/todo.md` - Task list

### External References

- [PEP 518](https://peps.python.org/pep-0518/) - pyproject.toml standard
- [Django Migrations](https://docs.djangoproject.com/en/stable/topics/migrations/)
- [Alembic Tutorial](https://alembic.sqlalchemy.org/en/latest/tutorial.html)
- [Ruff Documentation](https://docs.astral.sh/ruff/)
- [MyPy Documentation](https://mypy.readthedocs.io/)

---

## 🎯 Success Metrics

Your project is well-structured when:

✅ Root directory has ≤ 5 visible folders
✅ `.ai-validation/check_quality.sh` passes all checks
✅ New developers can navigate in < 5 minutes
✅ Claude Code finds files without asking
✅ No confusion about file placement
✅ Test coverage ≥ 80%
✅ Zero linting/type/security errors
✅ Documentation is current

---

## 📝 Version History

- **v2.0.0** (2025-10-26) - Renamed to `artifacts/`, configurable migrations, config guidance
- **v1.0.0** (2025-10-26) - Initial release with minimal root philosophy

See `CHANGELOG.md` for detailed version history.

---

## 🤝 Contributing

Have improvements? Found issues?

1. Document your use case
2. Explain the problem
3. Propose a solution
4. Test your changes
5. Share back (if appropriate)

**Philosophy**: This is a template, not a rigid framework. Adapt to your needs!

---

## 📄 License

This setup template and documentation is provided as-is for use in any project.
Adapt, modify, and distribute as needed.

---

## 🚀 Get Started

```bash
# Clone or copy this folder
cd best-practice

# Create your first project
./setup_project.sh my-awesome-project

# Navigate and start coding
cd my-awesome-project
source venv/bin/activate
pytest
.ai-validation/check_quality.sh

# Happy coding!
```

---

**Keep the root clean. Keep the code clean. Ship great software.** 🚀

---

*Generated with Claude Code v2.0 - Minimal Root Philosophy*
