---
name: Git Workflow
description: Git commits, checkpoints, branch strategy, and rollback patterns
tags: git, commit, checkpoint, rollback, version-control
auto_load_triggers: commit, checkpoint, rollback, git, rewind, branch
priority: toolkit
---

# Git Workflow

## Purpose

Defines git commit patterns, checkpoint workflows for safe exploration, branch strategy, and rollback procedures.

---

## Commit Messages

### Format

```
[type]: [description]

[optional body]

[optional footer]
```

###Types

- `feat` - New feature
- `fix` - Bug fix
- `refactor` - Code refactoring
- `test` - Adding tests
- `docs` - Documentation changes
- `chore` - Build/config changes

### Examples

```
feat: add autonomous daemon to project MCP

Implements safe autonomous execution with quality gate enforcement
and auto-rollback on failure.

Closes #42
```

```
fix: handle null project path in memory MCP

Added validation to reject empty project paths before attempting
to save data.

Fixes #38
```

---

## Commit Frequency

**Commit after**:
- Every passing quality gate
- Every completed task (≤30 lines)
- Every refactor checkpoint
- Before risky changes

**Never commit**:
- Failing tests
- Linting errors
- Type errors
- Without running quality gate

---

## Git Checkpoint Workflow

> **Fearless exploration**: Save state before risky changes, instant rollback

### Native Checkpointing

**Automatic state capture**:
- Claude automatically saves state before each edit
- No manual intervention required
- Instant rewind capability

**Rewind commands**:
```bash
# Escape twice (Esc×2) - Quick rewind
# OR use command
/rewind

# Options:
# - Code only
# - Conversation only
# - Both code and conversation
```

### Manual Checkpoints

**Before risky operations**:
```bash
# Create safety checkpoint
git tag checkpoint-before-refactor

# Do risky refactor...

# If it works:
git tag -d checkpoint-before-refactor

# If it fails:
git reset --hard checkpoint-before-refactor
```

### Checkpoint Best Practices

**Create checkpoints**:
- Before large refactoring
- Before experimental features
- Before complex bug fixes
- Before merge operations
- At end of each working day

**Checkpoint workflow**:
```bash
# 1. Ensure working directory is clean
git status

# 2. Create descriptive checkpoint
git tag checkpoint-auth-refactor-$(date +%Y%m%d-%H%M)

# 3. Work fearlessly knowing rollback is instant

# 4. If successful, continue
# 5. If failed, instant rollback
```

---

## Branch Strategy

**Main branches**:
- `main` - Production-ready code only
- `develop` - Integration branch for features

**Feature branches**:
- `feature/[name]` - New features
- `fix/[name]` - Bug fixes
- `refactor/[name]` - Refactoring work
- `docs/[name]` - Documentation updates

---

## Error Recovery Pattern

**If debugging spiral detected** (3+ failed attempts):

```bash
# STOP - You're stuck
git log --oneline -5           # Find last working commit
git reset --hard <commit_hash> # Revert to working state
git clean -fd                  # Remove untracked files
```

**Then**:
1. Break task into smaller pieces
2. Ensure each piece is testable
3. Complete smallest piece first
4. Test and commit before proceeding

---

## Refactoring Checkpoint Pattern

**Never refactor >30 lines at once**. Use checkpoints:

### Example Plan

```
Checkpoint 1: Extract function signatures (no implementation)
- Validation: All tests still pass
- Rollback point: YES

Checkpoint 2: Move functions to new module
- Validation: Import statements work, tests pass
- Rollback point: YES

Checkpoint 3: Update implementations
- Validation: All tests pass with new logic
- Rollback point: YES
```

**Workflow**:
1. Define target architecture
2. Break into checkpoints (each ≤30 lines)
3. For each checkpoint:
   - Implement
   - Run tests
   - PASS → Commit → Proceed
   - FAIL → Rollback checkpoint → Retry smaller

---

## Integration with Quality Gate

**Before every commit**:
1. Run quality gate
2. PASS → Commit
3. FAIL → Fix issues, re-run

**Use slash commands**:
- `/checkpoint [name]` - Create checkpoint
- Standard commit after quality gate passes

---

## Resources

- **CLAUDE.md**: Full git workflow sections (Git Checkpoint Workflow, Commit Messages)
- **/checkpoint slash command**: Automated checkpoint creation
- **quality-standards skill**: Pre-commit checklist
