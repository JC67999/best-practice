# Troubleshooting Guide

> **Solutions to common issues** with the best-practice toolkit

---

## 🔍 Quick Diagnosis

**Symptom → Solution**:
- Quality gate fails → [Quality Gate Issues](#quality-gate-issues)
- Git hooks blocking → [Git Hook Issues](#git-hook-issues)
- MCP tools not working → [MCP Issues](#mcp-issues)
- Context warnings → [Context Management](#context-management-issues)
- Tests failing → [Test Issues](#test-issues)
- Can't find files → [File Structure](#file-structure-issues)

---

## Quality Gate Issues

### ❌ "Quality gate script not found"

**Cause**: `.claude/quality-gate/check_quality.sh` missing

**Fix**:
```bash
# Check if file exists
ls .claude/quality-gate/check_quality.sh

# If missing, reinject toolkit or create manually
bash /path/to/best-practice/inject.sh .
```

---

### ❌ "Linting errors"

**Python (ruff)**:
```bash
# See errors
ruff check .

# Auto-fix
ruff check . --fix

# If ruff not installed
pip install ruff
```

**JavaScript (eslint)**:
```bash
# See errors
npm run lint

# Auto-fix
npm run lint -- --fix

# If eslint not configured
npm install --save-dev eslint
npx eslint --init
```

**Go (golangci-lint)**:
```bash
# See errors
golangci-lint run

# Install if missing
go install github.com/golangci/golangci-lint/cmd/golangci-lint@latest
```

---

### ❌ "Type checking failed"

**Python (mypy)**:
```bash
# See detailed errors
mypy . --show-error-codes

# Common fixes:
# 1. Add type hints
def my_function(param: str) -> int:
    return len(param)

# 2. Use Optional for nullable
from typing import Optional
def get_user(id: int) -> Optional[User]:
    pass

# 3. Ignore specific line (last resort)
result = some_call()  # type: ignore
```

**TypeScript**:
```bash
# See errors
npx tsc --noEmit

# Common fixes:
# 1. Add types
const name: string = "Alice"

# 2. Use interfaces
interface User {
    id: number;
    name: string;
}

# 3. Fix tsconfig.json strict settings
```

---

### ❌ "Tests failing"

**Python**:
```bash
# Run with verbose output
pytest -v

# Run specific test
pytest tests/test_file.py::test_function

# Run last failures only
pytest --lf

# See test coverage
pytest --cov --cov-report=html
# → Open htmlcov/index.html
```

**JavaScript**:
```bash
# Run with details
npm test -- --verbose

# Run specific test
npm test -- path/to/test.spec.js

# Update snapshots
npm test -- -u
```

**Go**:
```bash
# Run with verbose
go test -v ./...

# Run specific test
go test -v -run TestFunctionName

# With race detection
go test -race ./...
```

---

### ❌ "Coverage below 80%"

**Fix**:
```bash
# 1. Find untested code
pytest --cov --cov-report=term-missing

# 2. Add tests for uncovered lines
# → Focus on critical paths first

# 3. Re-run coverage
pytest --cov
```

**Acceptable exceptions**:
- Configuration files
- Simple getters/setters
- Error handling for impossible cases
- Deprecated code marked for removal

**Use coverage comments** (if justified):
```python
def simple_getter(self):  # pragma: no cover
    return self._value
```

---

### ❌ "Security vulnerabilities found"

**Python (bandit)**:
```bash
# See issues
bandit -r .

# See high/medium only
bandit -r . -ll

# Common issues:
# 1. Hardcoded passwords → Use environment variables
# 2. SQL injection risk → Use parameterized queries
# 3. Unsafe YAML load → Use safe_load
```

**JavaScript (npm audit)**:
```bash
# See vulnerabilities
npm audit

# Auto-fix
npm audit fix

# Force fix (may break things)
npm audit fix --force

# Update specific package
npm update package-name
```

---

### ❌ "Root structure compliance failed"

**Cause**: Too many folders in project root (max: 5)

**Allowed folders**:
```
/.claude/    - Toolkit files
/tests/      - Test suite
/docs/       - ALL documentation
/dist/       - Distribution (generated)
/src/        - Source code (or language-specific)
```

**Fix**:
```bash
# Move documentation to docs/
mv *.md docs/  # except README.md and CLAUDE.md

# Move configs to hidden dirs
mkdir .config && mv *.config.js .config/

# Consolidate source
mkdir src && mv lib/ utils/ core/ src/
```

**See**: `.claude/skills/file-placement/skill.md`

---

## Git Hook Issues

### ❌ "pre-commit hook not running"

**Check**:
```bash
# Verify hook installed
ls -la .git/hooks/pre-commit

# Check if executable
file .git/hooks/pre-commit
```

**Fix**:
```bash
# Reinstall hooks
bash .claude/hooks/install-hooks.sh

# Verify installation
bash .git/hooks/pre-commit  # Should run quality gate
```

---

### ❌ "commit-msg: Invalid format"

**Error**: Commit message doesn't follow conventional format

**Valid formats**:
```bash
# Correct:
git commit -m "feat: add user login"
git commit -m "fix(api): handle null response"
git commit -m "docs: update README"

# Wrong:
git commit -m "added some stuff"  # ❌ No type
git commit -m "Feature: login"    # ❌ Wrong case
git commit -m "feat add login"    # ❌ Missing colon
```

**Valid types**:
- `feat` - New feature
- `fix` - Bug fix
- `docs` - Documentation
- `style` - Code style
- `refactor` - Refactoring
- `test` - Tests
- `chore` - Maintenance
- `perf` - Performance
- `ci` - CI/CD
- `build` - Build system
- `revert` - Revert commit

**See**: `.claude/skills/git-workflow/skill.md`

---

### ❌ "pre-push: TODO markers found"

**Cause**: Committed code contains `TODO` or `FIXME` comments

**Fix**:
```bash
# Find TODOs in staged changes
git diff origin/main --cached | grep -E "TODO|FIXME"

# Options:
# 1. Remove TODOs
# 2. Create GitHub issues instead
gh issue create --title "TODO: Implement feature X"

# 3. Convert to tasks in TASKS.md
echo "- [ ] Implement feature X" >> .claude/TASKS.md
```

**Why this matters**: TODOs in committed code are forgotten. Use issue tracker instead.

---

### ❌ "Hook failed but I need to commit urgently"

**Emergency bypass** (use sparingly):
```bash
# Bypass ALL hooks (logged)
git commit --no-verify -m "feat: emergency fix"

# Bypass push hooks
git push --no-verify
```

**After bypassing**:
1. Create issue to fix quality problems: `gh issue create`
2. Fix issues in next commit
3. Don't make bypassing a habit

---

## MCP Issues

### ❌ "MCP tools not showing in Claude Code"

**Check configuration**:
1. Open Claude Code Settings
2. Go to "MCP Servers"
3. Should see: Memory MCP, Quality MCP, Project MCP

**Fix**:
```bash
# 1. Check MCP servers installed
ls ~/.mcp-servers/
# Should show: memory_mcp.py, quality_mcp.py, project_mcp.py

# 2. Reinstall if missing
cd .claude/mcp-servers/
pip install mcp
cp *.py ~/.mcp-servers/
chmod +x ~/.mcp-servers/*.py

# 3. Test MCP server
python ~/.mcp-servers/memory_mcp.py --test

# 4. Restart Claude Code
```

**See**: `.claude/mcp-servers/README.md` for detailed setup

---

### ❌ "mcp__*__* tool not found"

**Cause**: MCP server not configured in Claude Code

**Fix**:
```bash
# Add to Claude Code MCP config
# (~/.config/claude-code/mcp.json or similar)
{
  "mcpServers": {
    "memory": {
      "command": "python",
      "args": ["/home/user/.mcp-servers/memory_mcp.py"]
    },
    "quality": {
      "command": "python",
      "args": ["/home/user/.mcp-servers/quality_mcp.py"]
    },
    "project": {
      "command": "python",
      "args": ["/home/user/.mcp-servers/project_mcp.py"]
    }
  }
}
```

---

### ❌ "MCP tool returns error"

**Debug**:
```bash
# Run MCP server directly
python ~/.mcp-servers/memory_mcp.py --debug

# Check logs
tail -f ~/.mcp-servers/logs/*.log

# Verify permissions
ls -la ~/.mcp-servers/data/
```

**Common issues**:
- File permissions → `chmod 755 ~/.mcp-servers/*.py`
- Missing dependencies → `pip install -r .claude/mcp-servers/requirements.txt`
- Corrupted data → Backup and remove `~/.mcp-servers/data/`

---

## Context Management Issues

### ⚠️ "Approaching usage limit (>60%)"

**Immediate actions**:
```bash
# 1. Save state to files
cat .claude/TASKS.md > progress.md
# Document current work

# 2. Use /compact (loses some details)
# → In Claude Code, type /compact

# 3. Use /clear (recommended for fresh start)
# → In Claude Code, type /clear

# 4. Resume later with context
# → Use /resume or --continue flag
```

**Prevention**:
```bash
# Read selectively
@specific-file.py  # Not "read all files"

# Use subagents for exploration
# → Preserves main context

# Scope sessions to single features
# → One chat = one feature

# Use .claudeignore
echo "node_modules/" >> .claudeignore
echo "vendor/" >> .claudeignore
echo "dist/" >> .claudeignore
echo "*.log" >> .claudeignore
```

**See**: `.claude/skills/context-management/skill.md`

---

## Test Issues

### ❌ "pytest: command not found"

**Fix**:
```bash
# Install pytest
pip install pytest pytest-cov

# Or from requirements
pip install -r requirements.txt
```

---

### ❌ "Tests pass locally, fail in CI"

**Common causes**:
1. **Environment differences**
   ```bash
   # Pin dependencies
   pip freeze > requirements.txt
   ```

2. **Timing issues**
   ```python
   # Use freezegun for time-based tests
   from freezegun import freeze_time

   @freeze_time("2024-01-01")
   def test_date_logic():
       pass
   ```

3. **File path assumptions**
   ```python
   # Use pathlib for cross-platform paths
   from pathlib import Path
   test_file = Path(__file__).parent / "fixtures" / "data.json"
   ```

4. **Missing test dependencies**
   ```bash
   # Install test extras
   pip install -e ".[test]"
   ```

---

## File Structure Issues

### ❌ "Can't find .claude/TASKS.md"

**Check**:
```bash
# List hidden dirs
ls -la | grep claude

# If missing, run wizard
bash .claude/init-wizard.sh

# Or create manually
mkdir -p .claude
cat > .claude/TASKS.md << 'EOF'
# Project Tasks
...
EOF
```

---

### ❌ "Where should I put X file?"

**Reference**:
```
Source code      → /src/ or language-specific (/lib, /pkg)
Tests            → /tests/
Documentation    → /docs/
Config files     → Hidden dirs (/.config, .vscode)
Build artifacts  → /dist/ or /build/
Logs             → /logs/ (gitignored)
Temp files       → /temp/ (gitignored)
```

**See**: `.claude/skills/file-placement/skill.md`

---

## Installation Issues

### ❌ "inject.sh fails"

**Debug**:
```bash
# Run with debug output
bash -x ./inject.sh /path/to/project

# Check requirements
# → Target must be valid directory
# → Must have write permissions

# Try manual installation
cd /path/to/project
/path/to/best-practice/retrofit-tools/smart_install.sh
```

---

### ❌ "init-wizard.sh: command not found"

**Fix**:
```bash
# Check if file exists and is executable
ls -la .claude/init-wizard.sh

# Make executable if needed
chmod +x .claude/init-wizard.sh

# Run
bash .claude/init-wizard.sh
```

---

## Getting Help

### 📚 Resources
```bash
# Quick reference
cat .claude/QUICK_REFERENCE.md

# Standards
cat CLAUDE.md

# Skills catalog
cat .claude/skills/INDEX.md

# MCP setup
cat .claude/mcp-servers/README.md
```

### 🆘 Still Stuck?

1. **Check skills**: Relevant skill might have detailed guidance
   ```bash
   ls .claude/skills/
   cat .claude/skills/<skill-name>/skill.md
   ```

2. **Review logs**: Look for error messages
   ```bash
   git log --oneline -5
   cat .claude/hooks/pre-commit  # See what hook does
   ```

3. **Reset to clean state**:
   ```bash
   # Create checkpoint first
   git tag checkpoint-before-reset

   # Reset to last working commit
   git reset --hard HEAD~1
   ```

4. **Uninstall and reinstall**:
   ```bash
   bash .claude/uninstall.sh
   bash /path/to/inject.sh .
   ```

---

**Last Updated**: 2025-11-15
**Need more help?** Check `.claude/skills/` for technique-specific guidance.
