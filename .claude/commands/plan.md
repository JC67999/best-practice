---
description: Enter Planning Mode and create comprehensive implementation plan
---

# Planning Mode: $ARGUMENTS

## Entering Planning Mode

**ACTION**: Press **Shift+Tab twice** to enter read-only Planning Mode.

You are now in Planning Mode where you CANNOT modify files. This physical barrier ensures comprehensive planning before implementation.

## Create Implementation Plan

For the feature/task: "$ARGUMENTS"

### Step 1: Load Context

Read relevant files to understand:
- Existing architecture patterns
- Similar implementations
- Code standards
- Test patterns

Use @ syntax to reference specific files only.

### Step 2: Break Down into Atomic Tasks

Create task list where EACH task is:
- ≤30 lines of implementation
- ≤30 minutes to complete
- Independent (no blocking dependencies)
- Testable (objective pass/fail)
- Valuable (delivers user benefit)

### Step 3: Create plan.md

```markdown
# Implementation Plan: [Feature Name]

## Objective
[What we're building and why]

## Files to Modify
- `path/to/file1.py` - [What changes]
- `path/to/file2.py` - [What changes]

## Files to Create
- `path/to/new_file.py` - [Purpose]

## Task Breakdown

### Task 1: [Description] (≤30 lines)
**File**: path/to/file.py
**Changes**:
- [Specific change 1]
- [Specific change 2]

**Tests**:
```python
def test_task1_functionality():
    # Test case
    pass
```

**Acceptance Criteria**:
- [ ] [Criterion 1]
- [ ] [Criterion 2]

**Estimated effort**: [15 minutes]

### Task 2: [Description] (≤30 lines)
[Same structure as Task 1]

## Testing Strategy
- Unit tests for each task
- Integration tests for full feature
- Edge case coverage

## Rollback Plan
- Git checkpoint before starting
- Rollback command: `git reset --hard checkpoint-name`

## Estimated Total Effort
[Sum of all tasks - if >2 hours, break down further]
```

### Step 4: Present Plan for Approval

Say:

"Plan complete. Please review plan.md for:
1. Task size (all ≤30 lines?)
2. Clear acceptance criteria
3. Comprehensive tests
4. Reasonable effort estimate

Approve to proceed with implementation?"

### Step 5: Wait for Approval

**DO NOT start implementation until explicitly approved.**

If approved, say:
"Exiting Planning Mode. Creating git checkpoint before implementation."

Then execute:
```bash
git tag checkpoint-$(date +%Y%m%d-%H%M)-$ARGUMENTS
```

## Implementation Phase

After approval and checkpoint:

1. Work through tasks sequentially
2. Implement one task at a time
3. Run tests after each task
4. Commit after each passing task
5. Move to next task

Use `/tdd` command for test-driven implementation of each task.
