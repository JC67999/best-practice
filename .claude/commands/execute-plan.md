---
description: Execute implementation plan with automated checkpoints and quality gates
---

# Execute Plan: $ARGUMENTS

Execute implementation plan for: "$ARGUMENTS"

## Prerequisites Check

**Before executing**:
- [ ] Plan exists (created with `/plan` command)
- [ ] Planning Mode completed (Shift+Tab×2)
- [ ] Plan reviewed and approved
- [ ] Git checkpoint created
- [ ] Current branch is correct

**Load plan from**: `docs/notes/plan-$ARGUMENTS.md` or `plan.md`

## Execution Mode

**IMPORTANT**: This command executes the plan AUTONOMOUSLY with safety guardrails.

**Safety guardrails**:
- ✅ Git checkpoint before starting
- ✅ Git checkpoint after each task
- ✅ Quality gate after each task
- ✅ Automatic rollback on failure
- ✅ Progress tracking
- ✅ User approval for risky changes

## Phase 1: Initialization

### Step 1: Load Plan

```bash
# Load the plan file
cat docs/notes/plan-$ARGUMENTS.md
# or
cat plan.md
```

**Plan summary**:
- Total tasks: [X]
- Estimated time: [Y hours]
- Files to modify: [List]
- Files to create: [List]

### Step 2: Create Execution Checkpoint

```bash
# Create safety checkpoint
git tag checkpoint-execute-$(date +%Y%m%d-%H%M)-$ARGUMENTS

# Verify clean state
git status
```

**Checkpoint created**: `checkpoint-execute-[timestamp]-$ARGUMENTS`

**Rollback command** (save this):
```bash
git reset --hard checkpoint-execute-[timestamp]-$ARGUMENTS
git clean -fd
```

### Step 3: Initialize Progress Tracker

Create execution tracker: `docs/notes/execution-$ARGUMENTS.md`

```markdown
# Execution Progress: $ARGUMENTS

**Started**: $(date)
**Plan**: plan-$ARGUMENTS.md
**Checkpoint**: checkpoint-execute-[timestamp]

## Tasks

- [ ] Task 1: [Description]
- [ ] Task 2: [Description]
- [ ] Task 3: [Description]

## Completed

[Tasks completed will be listed here]

## Blocked

[Any blockers will be listed here]
```

## Phase 2: Task Execution Loop

**For each task in plan**:

### Step 4: Pre-Task Checkpoint

```bash
# Before starting task N
git add -A
git commit -m "checkpoint: before task N - [task name]" || echo "No changes to checkpoint"
git tag checkpoint-task-N-$ARGUMENTS
```

### Step 5: Execute Task (TDD)

**Use TDD for each task**:

```bash
# 1. Write test first (RED)
# tests/test_[feature].py

def test_[task_name]():
    """Test for task N."""
    # Given: [Setup]

    # When: [Action]

    # Then: [Assert]
    assert expected == actual
```

**Run test - should FAIL**:
```bash
pytest tests/test_[feature].py::test_[task_name] -v
# Expected: FAILED
```

**Implement solution (GREEN)**:
```python
# Implement the task
[Code implementation]
```

**Run test - should PASS**:
```bash
pytest tests/test_[feature].py::test_[task_name] -v
# Expected: PASSED
```

**Refactor if needed** (tests stay green):
```bash
# Improve code quality
# Run tests after each refactor step
pytest tests/test_[feature].py -v
```

### Step 6: Task Quality Gate

**Run quality checks**:
```bash
# Linting
ruff check [modified-files]

# Type checking
mypy [modified-files]

# All tests
pytest tests/ -v

# Coverage
pytest tests/ --cov=[module] --cov-report=term-missing
```

**Quality gate status**:
- [ ] All tests pass
- [ ] No linting errors
- [ ] No type errors
- [ ] Coverage ≥80%

**If quality gate FAILS**:
1. Fix issues
2. Re-run quality gate
3. Do NOT proceed until passing

**If quality gate PASSES**:
- Continue to next step

### Step 7: Commit Task

```bash
git add -A
git commit -m "feat: complete task N - [task name]

- [Specific change 1]
- [Specific change 2]
- Tests passing: [X/X]
- Coverage: [Y%]

Part of: $ARGUMENTS

🤖 Generated with [Claude Code](https://claude.com/claude-code)

Co-Authored-By: Claude <noreply@anthropic.com>"
```

### Step 8: Update Progress Tracker

Update `docs/notes/execution-$ARGUMENTS.md`:

```markdown
## Completed

- ✅ Task N: [Description] (completed [timestamp])
  - Commit: [commit-hash]
  - Tests: [X/X passing]
  - Coverage: [Y%]
```

### Step 9: Check for Blockers

**Blocker detection**:
- ❌ Quality gate failed after 3 attempts
- ❌ Task taking >2× estimated time
- ❌ Dependency discovered not in plan
- ❌ Breaking change required

**If blocked**:
1. Document blocker in execution tracker
2. Create blocker issue
3. Stop execution
4. Return to planning phase

**If not blocked**:
- Continue to next task

### Step 10: Repeat for Next Task

Go back to Step 4 for next task in plan.

## Phase 3: Completion

### Step 11: Final Quality Gate

**Run comprehensive quality gate**:
```bash
# Full test suite
pytest tests/ -v --cov --cov-report=html

# All linting
ruff check .

# All type checking
mypy .

# Structure validation (if MCP available)
# Use quality MCP: run_quality_gate
```

**Final quality requirements**:
- [ ] All tests passing
- [ ] Coverage ≥80%
- [ ] Zero linting errors
- [ ] Zero type errors
- [ ] All tasks completed
- [ ] Documentation updated

### Step 12: Integration Test

**Test the complete feature**:
```bash
# Run integration tests
pytest tests/integration/ -v

# Manual testing (if needed)
# [Manual test steps]
```

### Step 13: Update Documentation

**Update README** (if public API changed):
```markdown
# Add to README.md
## New Feature: [Feature Name]

[Brief description]

Usage:
```python
[Usage example]
```
```

**Update CHANGELOG**:
```markdown
# Add to CHANGELOG.md or docs/notes/

## [Version] - $(date +%Y-%m-%d)

### Added
- [Feature description]

### Changed
- [Any breaking changes]

### Fixed
- [Any bugs fixed]
```

### Step 14: Final Commit

```bash
git add -A
git commit -m "feat: complete $ARGUMENTS

Completed all tasks:
- Task 1: [Description]
- Task 2: [Description]
- Task 3: [Description]

Quality gate: PASSED
- Tests: [X/X passing]
- Coverage: [Y%]
- Linting: PASS
- Type checking: PASS

Documentation updated:
- README.md
- CHANGELOG.md

🤖 Generated with [Claude Code](https://claude.com/claude-code)

Co-Authored-By: Claude <noreply@anthropic.com>"
```

### Step 15: Tag Completion

```bash
# Tag completion
git tag execute-complete-$ARGUMENTS

# Show completion summary
echo "✅ Execution complete: $ARGUMENTS"
echo "📊 Tasks completed: [X/X]"
echo "✅ Quality gate: PASSED"
echo "📝 Documentation: Updated"
```

## Phase 4: Review & Cleanup

### Step 16: Execution Summary

Create summary document: `docs/notes/execution-summary-$ARGUMENTS.md`

```markdown
# Execution Summary: $ARGUMENTS

**Completed**: $(date)
**Duration**: [X hours]
**Tasks**: [X completed / Y total]

## Metrics

- **Commits**: [N commits]
- **Tests added**: [N tests]
- **Coverage**: [X%]
- **Files modified**: [N files]
- **Lines added**: [+N lines]
- **Lines removed**: [-N lines]

## Quality Gate Results

- ✅ All tests passing ([X/X])
- ✅ Coverage ≥80% ([actual]%)
- ✅ Zero linting errors
- ✅ Zero type errors

## Blockers Encountered

[List any blockers and how they were resolved]

## Lessons Learned

[What went well / What could improve]

## Next Steps

[Any follow-up work needed]
```

### Step 17: Cleanup Checkpoints

```bash
# List all checkpoints created
git tag -l "checkpoint-*-$ARGUMENTS"

# Delete intermediate checkpoints (keep start/end)
git tag -d checkpoint-task-1-$ARGUMENTS
git tag -d checkpoint-task-2-$ARGUMENTS
# Keep: checkpoint-execute-[timestamp]-$ARGUMENTS
# Keep: execute-complete-$ARGUMENTS
```

### Step 18: Optional Push

**If ready to push**:
```bash
# Push to remote
git push origin [branch-name]
git push origin --tags

# Or create PR
gh pr create --title "feat: $ARGUMENTS" --body "$(cat docs/notes/execution-summary-$ARGUMENTS.md)"
```

## Rollback Procedures

### Full Rollback (Abort Execution)

```bash
# Rollback to start checkpoint
git reset --hard checkpoint-execute-[timestamp]-$ARGUMENTS
git clean -fd

# Delete execution artifacts
rm docs/notes/execution-$ARGUMENTS.md
rm docs/notes/execution-summary-$ARGUMENTS.md

# Delete task checkpoints
git tag -l "checkpoint-task-*-$ARGUMENTS" | xargs git tag -d
git tag -d execute-complete-$ARGUMENTS
```

### Partial Rollback (Undo Last Task)

```bash
# Rollback to previous task checkpoint
git reset --hard checkpoint-task-N-$ARGUMENTS
git clean -fd

# Update execution tracker
# Mark task N as pending
```

## Autonomous Mode

**For fully autonomous execution** (use with caution):

```bash
# Run with max turns limit
claude-code --max-turns 50 /execute-plan [feature]
```

**Safety limits**:
- Maximum 50 autonomous actions
- Stops on quality gate failure
- Stops on blocker detection
- Stops on user input required

**Progress monitoring**:
- Watch execution tracker in real-time
- Monitor git commits
- Check test results

## Execution Best Practices

**DO**:
- Create checkpoint before starting
- Use TDD for every task (RED → GREEN → REFACTOR)
- Run quality gate after every task
- Commit after every passing task
- Update progress tracker continuously
- Stop and replan if blocked >2 hours

**DON'T**:
- Skip checkpoints (they save hours of debugging)
- Skip tests (they catch regressions immediately)
- Skip quality gates (they enforce standards)
- Continue if quality gate fails 3× (stop and debug)
- Rush through tasks (small commits are safer)
- Work >2 hours without committing

## Monitoring Execution

**Watch progress**:
```bash
# Terminal 1: Watch execution tracker
watch -n 5 cat docs/notes/execution-$ARGUMENTS.md

# Terminal 2: Watch git log
watch -n 5 'git log --oneline -10'

# Terminal 3: Watch test results
watch -n 10 'pytest tests/ --tb=no -q'
```

## When to Stop and Replan

Stop execution if:
- Any task takes >2× estimated time
- Quality gate fails >3 times
- Blocker requires >30 minutes to resolve
- Breaking change discovered
- Plan assumptions are invalid

Then:
1. Document current state
2. Rollback to last stable checkpoint
3. Return to planning phase
4. Update plan with new knowledge
5. Resume execution

Execution complete! Use `/debug` if any issues encountered.
