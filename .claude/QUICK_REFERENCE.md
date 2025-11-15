# Quick Reference - Best Practice Toolkit

> **One-page cheat sheet** for common operations

---

## 🚀 Daily Workflow

```bash
# 1. Start session in Claude Code
# → MCP tools auto-load: load_project_context, get_current_status

# 2. Check current tasks
cat .claude/TASKS.md

# 3. Work on task (≤30 lines, ≤15 minutes)

# 4. Test changes
pytest tests/          # Python
npm test               # JavaScript
go test ./...          # Go

# 5. Run quality gate
bash .claude/quality-gate/check_quality.sh

# 6. Commit (git hooks auto-run quality checks)
git add .
git commit -m "feat: add feature X"
git push

# 7. Update TASKS.md - mark task complete

# 8. End session
# → MCP: save_session_summary
```

---

## 📁 File Structure

```
project/
├── .claude/                  # Toolkit (gitignored by default)
│   ├── config.json          # Project-specific settings
│   ├── TASKS.md             # Current task list
│   ├── init-wizard.sh       # Post-injection setup
│   ├── hooks/               # Git hooks
│   │   ├── pre-commit       # Quality gate
│   │   ├── commit-msg       # Message validation
│   │   └── pre-push         # Final checks
│   ├── skills/              # Auto-loading skills
│   │   └── INDEX.md         # Skill catalog
│   ├── quality-gate/        # Quality checks
│   │   └── check_quality.sh # Language-aware gate
│   └── templates/           # Project type configs
├── docs/                    # ALL documentation
├── tests/                   # Test suite
├── CLAUDE.md                # Standards (read this first!)
└── README.md                # Project overview
```

---

## ⚡ Common Commands

### Initialization
```bash
# Run setup wizard
bash .claude/init-wizard.sh

# Install git hooks
bash .claude/hooks/install-hooks.sh

# View project config
cat .claude/config.json
```

### Quality Checks
```bash
# Run quality gate
bash .claude/quality-gate/check_quality.sh

# Run specific checks
ruff check .           # Python linting
mypy .                 # Python types
pytest --cov           # Python tests + coverage
npm run lint           # JavaScript linting
npm test               # JavaScript tests
```

### Git Operations
```bash
# Create checkpoint before risky work
git tag checkpoint-$(date +%Y%m%d-%H%M)

# Commit with hooks
git commit -m "type: description"
# → Runs: pre-commit (quality gate) + commit-msg (validates format)

# Push with hooks
git push
# → Runs: pre-push (tests, no TODOs, TASKS.md check)

# Bypass hooks (NOT recommended, logged)
git commit --no-verify
git push --no-verify
```

### Commit Message Format
```bash
# Format: type: description
# or: type(scope): description

# Valid types:
feat       # New feature
fix        # Bug fix
docs       # Documentation
style      # Code style
refactor   # Code refactoring
test       # Tests
chore      # Maintenance
perf       # Performance
ci         # CI/CD
build      # Build system

# Examples:
git commit -m "feat: add user authentication"
git commit -m "fix(api): handle null pointer error"
git commit -m "docs: update installation guide"
git commit -m "test: add unit tests for login"
```

---

## 🧠 MCP Tools (Claude Code)

### Session Start (Automatic)
```python
# These auto-run at session start:
mcp__memory__load_project_context(project_path=cwd)
mcp__project__get_current_status(project_path=cwd)
```

### Before Tasks (Required)
```python
# Validate task aligns with objective
mcp__project__validate_task_alignment(
    project_path=cwd,
    task_description="What you're about to do"
)
# → Score ≥70: Proceed
# → Score <70: Ask user confirmation

# Check task size
mcp__project__validate_task_size(
    task_description="What you're about to do"
)
# → Too large: Break down first
```

### After Tasks (Required)
```python
# Quality gate before completion
mcp__quality__run_quality_gate(
    project_path=cwd,
    changes_made=["file1.py", "file2.py"]
)
# → PASS: Commit + mark complete
# → FAIL: Fix issues, re-run
```

### Session End (Automatic)
```python
# Save session summary
mcp__memory__save_session_summary(
    project_path=cwd,
    summary="Brief overview",
    decisions=["Decision 1", "Decision 2"],
    next_steps=["Task 1", "Task 2"],
    blockers=[]
)
```

---

## 🎯 Skills Auto-Loading

Skills automatically suggest when needed:

| When | Skill Loads |
|------|-------------|
| Test fails | problem-solving |
| New feature | planning-mode, tdd-workflow |
| git commit | git-workflow, quality-standards |
| Creating files | file-placement |
| Context >60% | context-management |
| Session start | mcp-usage |
| Debug >5min | problem-solving |
| Learn new code | domain-learning |

**View skill catalog**:
```bash
cat .claude/skills/INDEX.md
```

**Manual load**:
```bash
cat .claude/skills/problem-solving/skill.md
cat .claude/skills/tdd-workflow/skill.md
cat .claude/skills/planning-mode/skill.md
```

---

## 📋 Task Management

### TASKS.md Format
```markdown
## Current Sprint: Feature X

### 🔄 In Progress
- [ ] Task being worked on now (≤30 lines)

### 📋 Todo
- [ ] Task 1 (≤30 lines, ≤15 minutes)
- [ ] Task 2 (≤30 lines, ≤15 minutes)

### ✅ Completed
- [x] Finished task
```

### Task Rules
- **Size**: ≤30 lines of code, ≤15 minutes
- **One at a time**: Complete, test, commit before next
- **Too large?**: STOP, break down into sub-tasks first

---

## 🔍 Troubleshooting

### Quality Gate Fails
```bash
# See detailed output
bash .claude/quality-gate/check_quality.sh

# Common fixes:
ruff check . --fix      # Auto-fix linting
pytest --lf             # Re-run last failures
mypy . --show-error-codes  # See type errors

# See troubleshooting guide
cat .claude/TROUBLESHOOTING.md
```

### Git Hooks Blocking
```bash
# See what failed
# → Hook output shows specific errors

# Fix issues, then retry:
git commit

# Emergency bypass (logs bypass):
git commit --no-verify
```

### MCP Tools Not Working
```bash
# Check MCP installation
cat .claude/mcp-servers/README.md

# Verify Claude Code configuration
# → Settings > MCP Servers should list Memory, Quality, Project MCPs
```

### Context Limit Warning
```bash
# Save state to files first
cat .claude/TASKS.md > progress.md

# Then use /clear or /compact
# → Skills show how: .claude/skills/context-management/
```

---

## 📚 Resources

```bash
# Core standards
cat CLAUDE.md

# Skill catalog
cat .claude/skills/INDEX.md

# Project config
cat .claude/config.json

# Current tasks
cat .claude/TASKS.md

# Troubleshooting
cat .claude/TROUBLESHOOTING.md

# MCP setup
cat .claude/mcp-servers/README.md
```

---

## 🆘 Help

| Issue | Solution |
|-------|----------|
| Don't know where to start | cat .claude/TASKS.md |
| Quality gate failing | cat .claude/TROUBLESHOOTING.md |
| Git hook blocking | See hook output, fix issues |
| Skill not loading | cat .claude/skills/INDEX.md |
| Task too large | Break into ≤30 line sub-tasks |
| Context limit | cat .claude/skills/context-management/skill.md |
| MCP not working | cat .claude/mcp-servers/README.md |

---

**Last Updated**: 2025-11-15
**Version**: 1.0
