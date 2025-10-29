# Changelog - Claude Code Minimal Root Setup

All notable changes to the minimal root project setup will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/).

---

## [2.0.0] - 2025-10-26

### 🎉 Major Improvements Based on Professional Feedback

This release addresses three key areas for improvement identified in the original v1.0 structure.

### Changed

#### 1. **Renamed `_project_data/` → `artifacts/`**
   - **Rationale**: The underscore prefix (`_`) has Python "private" member connotations, causing confusion
   - **New name**: `artifacts/` is an industry-standard term used in CI/CD and build systems
   - **Benefits**:
     - Clearer purpose for cross-language teams
     - No "private" connotation confusion
     - Works across programming languages (Python, Go, Rust, TypeScript)
     - More professional and widely recognized
   - **Migration**: Simple rename operation, update references in code/docs
   - **Impact**: All operational and ephemeral data now in `artifacts/` folder

#### 2. **Configurable Migrations Placement**
   - **Problem**: Original v1.0 always placed migrations in `_project_data/migrations/`
   - **Issue**: Django, Alembic, and SQLAlchemy projects treat migrations as version-controlled source code
   - **Solution**: Added `--database` flag to setup script

   **Database Projects** (Django/Alembic):
   ```bash
   ./setup_minimal_project_v2.sh --database my-django-app
   # Creates: migrations/ in root (convention)
   # Includes: Alembic configuration (alembic.ini, env.py)
   # Treatment: Migrations as version-controlled code
   ```

   **Non-Database Projects**:
   ```bash
   ./setup_minimal_project_v2.sh my-api-project
   # Creates: artifacts/migrations/ (minimal root)
   # Use case: Simple SQL scripts, not core to application
   ```

   - **Benefits**:
     - Respects industry conventions when appropriate
     - Maintains minimal root philosophy for non-database projects
     - Reduces confusion for experienced Django/Alembic developers
     - Flexible: can migrate between approaches as project evolves

#### 3. **Configuration File Management Guidance**
   - **Problem**: Single `pyproject.toml` can grow to ~300+ lines
   - **Issue**: Large files difficult to scan, especially for specific tool configs
   - **Solution**: Added comprehensive guidance on when/how to split

   **When to Keep Single `pyproject.toml`** (Recommended):
   - ✅ Small to medium projects (<10k lines)
   - ✅ Standard tooling setup
   - ✅ Python-only projects
   - ✅ Modern Python practices (PEP 518)

   **When to Consider Splitting**:
   - ⚠️ Individual tool configs exceed 100 lines
   - ⚠️ Large projects (>10k lines of code)
   - ⚠️ Multi-language projects
   - ⚠️ Team with mixed tool preferences

   **Split Configuration Example**:
   ```
   my-project/
   ├── pyproject.toml    # Project metadata only
   ├── mypy.ini         # MyPy configuration
   ├── pytest.ini       # Pytest configuration
   ├── ruff.toml        # Ruff configuration
   └── .coveragerc      # Coverage configuration
   ```

   - **Documentation**: Added extensive comments in generated `pyproject.toml`
   - **Guidance**: When to split, how to split, documenting the decision

### Added

#### Script Features
- `--database` flag for root migrations folder
- `--python VERSION` flag (specify Python version)
- `--author NAME` flag (set author name)
- `--email EMAIL` flag (set author email)
- Help menu (`--help` or `-h`)
- Colored output for better UX
- Informational messages about choices made

#### Documentation
- **CLAUDE_CODE_PROJECT_SETUP_MINIMAL_ROOT_V2.md**: Complete updated guide
  - Version comparison table (v1.0 vs v2.0)
  - Migration guide from v1.0
  - Configuration management section
  - Benefits analysis of each change

- **Alembic Configuration** (for database projects):
  - `migrations/README.md` - Usage guide
  - `migrations/env.py` - Environment setup
  - `alembic.ini` - Alembic configuration

- **Enhanced CLAUDE.md Template**:
  - v2.0 changes section
  - Migration guidance based on project type
  - Configuration management section
  - Updated file placement rules

#### Quality Improvements
- More comprehensive `.gitignore` handling for `artifacts/`
- Better comments in `pyproject.toml` (~20 comment lines explaining philosophy)
- Version information in all generated files
- Clearer separation of concerns in setup script

### Fixed
- Confusion about underscore-prefixed folder naming
- Django/Alembic developers expecting root `migrations/` folder
- Lack of guidance on managing large configuration files
- Missing rationale for design decisions in documentation

### Deprecated
- ❌ `_project_data/` naming (use `artifacts/` instead)
- ❌ Hard-coded migrations in `_project_data/migrations/` (now configurable)

### Migration Guide (v1.0 → v2.0)

#### Quick Migration

```bash
# 1. Rename folder
mv _project_data/ artifacts/

# 2. (Optional) Move migrations to root if database project
mkdir migrations
mv artifacts/migrations/* migrations/
rmdir artifacts/migrations

# 3. Update all references
find . -type f \( -name "*.py" -o -name "*.md" -o -name "*.sh" \) \
  -exec sed -i 's/_project_data/artifacts/g' {} +

# 4. Update .gitignore
sed -i 's/_project_data/artifacts/g' .gitignore

# 5. Update pyproject.toml exclusions
sed -i 's/_project_data/artifacts/g' pyproject.toml

# 6. Commit changes
git add .
git commit -m "Upgrade to minimal root structure v2.0

- Rename _project_data/ → artifacts/
- Move migrations/ to root (database project)
- Update all references"
```

---

## [1.0.0] - 2025-10-26

### Initial Release

#### Added
- **Minimal root philosophy**: Reduced from 14+ folders to 4 folders
- **Consolidated structure**:
  - `src/` - All production code
  - `tests/` - All tests
  - `docs/` - All documentation
  - `_project_data/` - All operational data

#### Features
- Automated setup script (`setup_minimal_project.sh`)
- Complete `pyproject.toml` configuration
  - Ruff (linting)
  - MyPy (strict type checking)
  - Pytest (with coverage)
  - Bandit (security)
  - Radon (complexity)
  - Interrogate (docstring coverage)
- Quality gates script (`.ai-validation/check_quality.sh`)
- Comprehensive documentation templates
- TDD workflow enforcement
- Sample tests and code

#### Directory Structure
```
my-project/
├── src/                    # Production code
├── tests/                  # Test suite
├── docs/                   # Documentation
├── _project_data/          # Operational data
│   ├── logs/
│   ├── temp/
│   ├── input/
│   ├── output/
│   ├── .archive/
│   └── migrations/
├── .claude/                # Claude config
└── .ai-validation/         # Quality tools
```

#### Benefits
- 71% reduction in root directories (14 → 4)
- Faster navigation for humans and AI
- Clear file placement rules
- Comprehensive quality enforcement
- TDD-ready structure

### Known Issues (Fixed in v2.0)
- `_project_data/` naming caused underscore confusion
- Migrations always in `_project_data/`, breaking Django/Alembic conventions
- No guidance on managing large `pyproject.toml` files

---

## Comparison: v1.0 vs v2.0

| Feature | v1.0 | v2.0 | Improvement |
|---------|------|------|-------------|
| **Operational folder** | `_project_data/` | `artifacts/` | ✅ Clearer naming |
| **Migrations location** | Always in `_project_data/` | Configurable (root or artifacts) | ✅ Respects conventions |
| **Config guidance** | None | Comprehensive | ✅ Helps scale |
| **Database projects** | No special handling | `--database` flag | ✅ Professional support |
| **Documentation** | Good | Excellent | ✅ More detailed |
| **Cross-language** | Good | Better | ✅ Universal terms |
| **Root folders** | 4 | 4-5 (optional migrations/) | ✅ Still minimal |
| **Setup options** | Basic | Full flags | ✅ More flexible |

---

## Future Considerations

### Potential v2.1 Features
- [ ] `--framework` flag (django, fastapi, flask) for framework-specific setup
- [ ] `--database-type` flag (postgresql, mysql, sqlite) for specific DB configs
- [ ] `--ci` flag to generate CI/CD configurations (GitHub Actions, GitLab CI)
- [ ] `--docker` flag to generate Dockerfile and docker-compose.yml
- [ ] Interactive mode for step-by-step configuration
- [ ] Templates for common project types (API, CLI, library, web app)

### Potential v3.0 Features
- [ ] Multi-language support (Go, Rust, TypeScript)
- [ ] Monorepo support with multiple projects
- [ ] Integration with project management tools
- [ ] Auto-update mechanism for existing projects
- [ ] Plugin system for custom project templates

---

## Upgrading

### From v1.0 to v2.0

1. **Read** `CLAUDE_CODE_PROJECT_SETUP_MINIMAL_ROOT_V2.md` for full details
2. **Rename** `_project_data/` → `artifacts/`
3. **Decide** on migrations placement (root or artifacts)
4. **Update** all references in code and documentation
5. **Review** configuration management guidance
6. **Test** that all quality gates still pass

### Future Upgrades

When new versions are released:
1. Check `CHANGELOG.md` for breaking changes
2. Review migration guide for your version
3. Test in a separate branch first
4. Update documentation accordingly
5. Run quality gates to verify

---

## Credits

### v2.0 Improvements
- Based on professional feedback from experienced developers
- Incorporates industry best practices (Django, Alembic conventions)
- Inspired by modern Python project structures (PEP 518, packaging standards)
- CI/CD terminology (artifacts folder)

### v1.0 Foundation
- Distilled from real-world Python project (`my-finances-v2`)
- Influenced by Rust project structure (src/, tests/, docs/)
- Optimized for AI-assisted development (Claude Code)
- Test-driven development principles

---

## Questions or Feedback?

If you have suggestions for improvements or encounter issues:
1. Document your use case
2. Explain what didn't work or could be better
3. Propose a solution or ask for guidance
4. Consider contributing improvements back

**Philosophy**: This structure should serve YOUR projects. If something doesn't work for your use case, adapt it! Document your decisions in `docs/design/decisions/`.

---

## License

This setup template and documentation is provided as-is for use in any project.
Feel free to adapt, modify, and distribute as needed.

---

**Keep the root clean. Keep the code clean. Ship great software.** 🚀
