# 🚀 Best Practice Toolkit - Injected

> **This project now uses best-practice enforcement** for excellent code quality

This README explains what was added to your project and how to use it.

---

## ✅ What Was Added

The best-practice toolkit was injected into this project to enforce:
- ✅ Quality standards (linting, types, tests, coverage)
- ✅ Git workflow best practices (conventional commits)
- ✅ Minimal root structure (≤5 folders)
- ✅ Task-driven development (granular ≤30 line tasks)
- ✅ MCP integration for Claude Code
- ✅ Auto-loading skills for context-aware guidance

---

## 📁 New Files & Folders

```
project/
├── .claude/                    # Toolkit (gitignored)
│   ├── config.json            # Project-specific settings
│   ├── TASKS.md               # Current task list
│   ├── QUICK_REFERENCE.md     # One-page cheat sheet
│   ├── TROUBLESHOOTING.md     # Problem solutions
│   ├── init-wizard.sh         # Re-run setup wizard
│   ├── hooks/                 # Git hooks (optional)
│   │   ├── pre-commit         # Quality gate enforcement
│   │   ├── commit-msg         # Message validation
│   │   ├── pre-push           # Final checks
│   │   └── install-hooks.sh   # Install/reinstall hooks
│   ├── skills/                # Auto-loading skills
│   │   ├── INDEX.md           # Skill catalog
│   │   ├── problem-solving/   # Debugging techniques
│   │   ├── tdd-workflow/      # Test-driven development
│   │   ├── quality-standards/ # Quality requirements
│   │   ├── git-workflow/      # Git best practices
│   │   ├── planning-mode/     # Feature planning
│   │   ├── mcp-usage/         # MCP tool workflows
│   │   └── ... (9 total)
│   ├── quality-gate/          # Quality checks
│   │   └── check_quality.sh   # Language-aware gate
│   ├── templates/             # Project type configs
│   └── mcp-servers/           # MCP server code
├── docs/                      # Documentation (gitignored)
├── tests/                     # Tests (if FULL mode)
├── CLAUDE.md                  # Standards reference (gitignored)
└── README.md                  # This file (injected)
```

**All toolkit folders are gitignored by default** - clean git history.

---

## 🚀 Quick Start (60 Seconds)

### 1. Review Configuration
```bash
# See project-specific settings
cat .claude/config.json

# See current tasks
cat .claude/TASKS.md
```

### 2. Install Git Hooks (Optional but Recommended)
```bash
# Install quality enforcement hooks
bash .claude/hooks/install-hooks.sh
```

This installs:
- **pre-commit**: Runs quality gate before commits
- **commit-msg**: Validates commit message format
- **pre-push**: Final checks before pushing

### 3. Open in Claude Code
```bash
code .
```

Claude Code will:
- Auto-load MCP tools (Memory, Quality, Project)
- Suggest relevant skills based on context
- Enforce best practices

### 4. Start Working
```bash
# Check current task
cat .claude/TASKS.md

# Work on task (≤30 lines, ≤15 minutes)

# Run quality gate
bash .claude/quality-gate/check_quality.sh

# Commit (git hooks auto-run if installed)
git commit -m "feat: add feature X"
```

---

## 📚 Learn the Standards

### First-Time Users
1. **Read**: `cat CLAUDE.md` - Core standards (streamlined)
2. **Reference**: `cat .claude/QUICK_REFERENCE.md` - One-page cheat sheet
3. **Explore**: `cat .claude/skills/INDEX.md` - Skill catalog

### Quick Reference
```bash
# One-page cheat sheet
cat .claude/QUICK_REFERENCE.md

# When stuck
cat .claude/TROUBLESHOOTING.md

# Skill catalog
cat .claude/skills/INDEX.md
```

---

## 🎯 Daily Workflow

### Option 1: With Git Hooks (Recommended)
```bash
# 1. Check tasks
cat .claude/TASKS.md

# 2. Work on task (≤30 lines)

# 3. Test changes
pytest tests/          # or npm test, go test, etc.

# 4. Commit (hooks auto-run quality checks)
git commit -m "feat: implement X"
# → pre-commit runs quality gate automatically
# → commit-msg validates format automatically

# 5. Push (hooks run final checks)
git push
# → pre-push ensures tests pass, no TODOs

# 6. Mark task complete in TASKS.md
```

### Option 2: Manual Quality Checks
```bash
# 1. Check tasks
cat .claude/TASKS.md

# 2. Work on task

# 3. Run quality gate manually
bash .claude/quality-gate/check_quality.sh

# 4. Commit if quality gate passes
git commit -m "feat: implement X"

# 5. Update TASKS.md
```

---

## 🧠 Skills Auto-Loading

Skills automatically suggest themselves when needed:

| Situation | Skill Loads | What It Does |
|-----------|-------------|--------------|
| Test fails | problem-solving | 10 systematic debugging techniques |
| New feature | planning-mode | Requirements discovery, task breakdown |
| Writing tests | tdd-workflow | Red-Green-Refactor cycle |
| git commit | git-workflow | Commit format, checkpoints |
| Creating files | file-placement | Where files belong |
| Context >60% | context-management | Avoiding limits |
| Session start | mcp-usage | MCP tool workflows |

**View all skills**:
```bash
cat .claude/skills/INDEX.md
ls .claude/skills/
```

**Load skill manually**:
```bash
cat .claude/skills/problem-solving/skill.md
cat .claude/skills/tdd-workflow/skill.md
```

---

## ⚡ MCP Integration (Claude Code)

### What Are MCP Tools?

Model Context Protocol (MCP) tools that enforce standards:

1. **Memory MCP** - Persistent context across sessions
2. **Quality MCP** - Automated quality enforcement
3. **Project MCP** - Objective-driven task management

### Session Workflow

**Session Start** (automatic):
```python
# Claude auto-runs:
mcp__memory__load_project_context()  # Load history
mcp__project__get_current_status()    # See tasks
```

**Before Tasks** (required):
```python
# Validate task aligns with objective
mcp__project__validate_task_alignment(task_description)

# Check task size
mcp__project__validate_task_size(task_description)
```

**After Tasks** (required):
```python
# Quality gate before completion
mcp__quality__run_quality_gate(changes_made)
```

**Session End** (automatic):
```python
# Save session summary
mcp__memory__save_session_summary(summary, decisions, next_steps)
```

### MCP Setup

See `.claude/mcp-servers/README.md` for installation instructions.

---

## 🔧 Configuration

### Project Settings (`.claude/config.json`)

```json
{
  "project": {
    "name": "your-project",
    "type": "python",           // or javascript, go, rust
    "team_size": "solo",        // or small, large
    "ci_cd": "github-actions"   // or gitlab-ci, jenkins, none
  },
  "standards": {
    "max_task_lines": 30,
    "max_task_minutes": 15,
    "test_coverage_minimum": 80
  },
  "quality_gate": {
    "enabled": true,
    "block_commit_on_failure": true
  },
  "git_hooks": {
    "pre_commit": true,
    "commit_msg": true,
    "pre_push": true
  }
}
```

### Customize Standards

Edit `.claude/config.json` to adjust:
- Task size limits
- Coverage requirements
- Enable/disable specific hooks
- CI/CD integrations

---

## 📋 Task Management

### TASKS.md Rules

1. **Task size**: ≤30 lines of code, ≤15 minutes
2. **One at a time**: Complete, test, commit before next
3. **Break down large tasks**: If >30 lines, STOP and break into sub-tasks
4. **Update after each task**: Mark complete when done

### Example TASKS.md
```markdown
## Current Sprint: User Authentication

### 🔄 In Progress
- [ ] Add JWT token generation (≤30 lines)

### 📋 Todo
- [ ] Create login endpoint (≤30 lines)
- [ ] Add password hashing (≤30 lines)
- [ ] Write authentication tests (≤30 lines)

### ✅ Completed
- [x] Set up user model
- [x] Add email validation
```

---

## 🔍 Quality Gate

### What It Checks

The quality gate runs language-aware checks:

**Python**:
- Linting (ruff)
- Type checking (mypy)
- Tests (pytest)
- Coverage (≥80%)
- Security (bandit)

**JavaScript**:
- Linting (eslint)
- Type checking (TypeScript)
- Tests (jest/npm test)
- Security (npm audit)

**Go**:
- Linting (golangci-lint)
- Formatting (gofmt)
- Tests (go test)
- Race detection

### Run Manually
```bash
# Run quality gate
bash .claude/quality-gate/check_quality.sh

# See what it checks
cat .claude/quality-gate/check_quality.sh
```

### Auto-Run via Git Hooks
```bash
# Install hooks (if not already done)
bash .claude/hooks/install-hooks.sh

# Hooks run automatically on:
git commit  # → pre-commit (quality gate)
git push    # → pre-push (tests, no TODOs)
```

---

## 🆘 Troubleshooting

### Quality Gate Failing
```bash
# See detailed errors
bash .claude/quality-gate/check_quality.sh

# Common fixes:
ruff check . --fix      # Auto-fix linting
pytest --lf             # Re-run last failures
mypy .                  # See type errors

# Full troubleshooting guide
cat .claude/TROUBLESHOOTING.md
```

### Git Hooks Blocking
```bash
# See what failed (hook output shows errors)

# Fix issues, then retry commit

# Emergency bypass (use sparingly):
git commit --no-verify
```

### Need Help?
```bash
# Quick reference
cat .claude/QUICK_REFERENCE.md

# Troubleshooting
cat .claude/TROUBLESHOOTING.md

# Skills catalog
cat .claude/skills/INDEX.md
```

---

## 🔄 Re-run Setup Wizard

If you need to reconfigure:
```bash
bash .claude/init-wizard.sh
```

This will:
- Re-detect project type
- Update configuration
- Reinstall git hooks (if requested)
- Create fresh TASKS.md

---

## 🗑️ Uninstall

To remove the toolkit:
```bash
bash .claude/uninstall.sh
```

This removes:
- `.claude/` folder
- `CLAUDE.md`
- Git hooks
- Gitignore entries

**Your code is untouched** - only toolkit files removed.

---

## 📚 Resources

| Resource | Purpose |
|----------|---------|
| `CLAUDE.md` | Core standards (read first!) |
| `.claude/QUICK_REFERENCE.md` | One-page cheat sheet |
| `.claude/TROUBLESHOOTING.md` | Problem solutions |
| `.claude/skills/INDEX.md` | Skill catalog |
| `.claude/config.json` | Project settings |
| `.claude/TASKS.md` | Current task list |
| `.claude/mcp-servers/README.md` | MCP setup guide |

---

## 🎯 Key Principles

1. **Task-driven** - Work in ≤30 line, ≤15 minute tasks
2. **Quality-enforced** - Quality gate before every commit
3. **Minimal structure** - ≤5 root folders
4. **Conventional commits** - `type: description` format
5. **Test-driven** - Red-Green-Refactor cycle
6. **MCP-integrated** - AI-assisted with guardrails
7. **Skills-based** - Progressive disclosure of guidance

---

## ❓ FAQ

**Q: Do I have to use git hooks?**
A: No, but highly recommended. You can run quality gate manually.

**Q: Can I customize the standards?**
A: Yes, edit `.claude/config.json` and adjust as needed.

**Q: What if quality gate fails?**
A: See `.claude/TROUBLESHOOTING.md` for solutions to common issues.

**Q: Can I add my own skills?**
A: Yes! Use `.claude/skills/template/skill.md` as a starting point.

**Q: Are toolkit files committed to git?**
A: No, by default all toolkit folders are gitignored. Use `--commit` flag during injection to commit them.

**Q: How do I update the toolkit?**
A: Re-run injection: `./inject.sh . --commit` (from toolkit directory)

---

**Welcome to best-practice development!** 🚀

For questions, see `.claude/TROUBLESHOOTING.md` or `.claude/skills/INDEX.md`

---

**Last Updated**: 2025-11-15
**Toolkit Version**: 1.0
