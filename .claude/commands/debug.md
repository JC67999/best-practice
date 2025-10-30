---
description: Systematic debugging workflow - root cause to documented fix
---

# Debug: $ARGUMENTS

Systematic debugging for: "$ARGUMENTS"

**Problem Statement**: [Clear description of the bug/issue]

## Phase 1: Reproduction (Confirm the Problem)

### Step 1: Reproduce Reliably

**Can you reproduce it?**
- ✅ Yes, every time (deterministic)
- ⚠️ Yes, sometimes (probabilistic - note frequency)
- ❌ No, cannot reproduce

**Reproduction steps**:
1. [Step 1]
2. [Step 2]
3. [Step 3]

**Expected behavior**: [What should happen]

**Actual behavior**: [What actually happens]

**Evidence** (screenshots, logs, error messages):
```
[Paste error output, stack trace, or logs]
```

### Step 2: Minimal Reproduction

Reduce to smallest case that reproduces the issue:
- Remove unnecessary steps
- Simplify inputs
- Isolate the component

**Minimal reproduction**:
```
[Smallest code/steps that trigger the bug]
```

## Phase 2: Information Gathering

### Step 3: Collect Context

**Environment**:
- OS: [Operating system]
- Version: [Software version]
- Dependencies: [Relevant library versions]
- Configuration: [Relevant config settings]

**Recent changes**:
- Last working version: [When did it work?]
- Recent commits: [Git log last 5 commits]
- Recent dependency updates: [Any package updates?]

**Scope**:
- Affects: [All users / Some users / Only you]
- Severity: [Critical / High / Medium / Low]
- Frequency: [Always / Sometimes / Rarely]

### Step 4: Read Error Messages Carefully

**Error message**:
```
[Full error text]
```

**Parse the error**:
- What type of error? [TypeError, ValueError, etc.]
- What line number? [File:line]
- What's the root vs symptom? [Which part is the real cause?]

### Step 5: Check Logs

Relevant logs:
```bash
# Check application logs
tail -100 logs/*.log

# Check system logs
journalctl -n 100

# Check specific component
grep "ERROR" logs/pipeline.log
```

**Key log entries**:
```
[Paste relevant log lines]
```

## Phase 3: Root Cause Analysis

### Step 6: Form Hypotheses

Generate 3-5 hypotheses about the root cause:

**Hypothesis 1**: [Possible cause]
- **Why this might be it**: [Reasoning]
- **How to test**: [Specific test]
- **Expected result if true**: [What we'd see]

**Hypothesis 2**: [Possible cause]
- **Why this might be it**: [Reasoning]
- **How to test**: [Specific test]
- **Expected result if true**: [What we'd see]

**Hypothesis 3**: [Possible cause]
- **Why this might be it**: [Reasoning]
- **How to test**: [Specific test]
- **Expected result if true**: [What we'd see]

### Step 7: Binary Search Debugging

For complex issues, use binary search:

```bash
# Test midpoint in git history
git log --oneline | head -20
git bisect start
git bisect bad HEAD
git bisect good <last-known-good-commit>

# Git will checkout midpoint
# Test if bug exists, then:
git bisect bad  # or git bisect good

# Continue until root commit found
```

### Step 8: Test Hypotheses (One at a Time)

**Testing Hypothesis 1**:
```bash
# Command to test
[Test command]
```

**Result**: ✅ Confirmed / ❌ Rejected

**Testing Hypothesis 2**:
```bash
# Command to test
[Test command]
```

**Result**: ✅ Confirmed / ❌ Rejected

### Step 9: Identify Root Cause

**Root cause identified**: [Specific cause]

**Evidence**:
- [Evidence 1]
- [Evidence 2]
- [Evidence 3]

**Why it causes the symptom**:
[Explain the causal chain from root cause to observed symptom]

## Phase 4: Fix Development

### Step 10: Design Fix

**Fix strategy**: [How to fix the root cause]

**Alternatives considered**:
1. **[Approach 1]** - [Pros/cons]
2. **[Approach 2]** - [Pros/cons]
3. **[Chosen approach]** - [Why this one]

**Fix scope**:
- Files to modify: [List files]
- Lines to change: [Estimate]
- Tests to add: [What tests]

### Step 11: Create Safety Checkpoint

```bash
# Create checkpoint before fix
git tag checkpoint-debug-$(date +%Y%m%d-%H%M)-$ARGUMENTS
```

### Step 12: Implement Fix

**Use TDD approach**:
1. Write test that reproduces the bug (fails)
2. Implement fix
3. Verify test now passes
4. Verify no regressions

```bash
# Write reproduction test
# tests/test_[issue].py

def test_should_not_[bug_symptom]():
    """Test that reproduces the bug - should fail initially."""
    # Given: [Setup that triggers bug]

    # When: [Action that causes bug]

    # Then: [Assert correct behavior]
    assert expected == actual
```

**Run test - verify it fails**:
```bash
pytest tests/test_[issue].py -v
# Should FAIL with same error as bug
```

**Implement fix**:
```python
# [Modified code with fix]
```

**Run test - verify it passes**:
```bash
pytest tests/test_[issue].py -v
# Should PASS now
```

**Run full test suite - verify no regressions**:
```bash
pytest tests/ -v
# All tests should pass
```

### Step 13: Verify Fix

**Verification checklist**:
- [ ] Bug no longer reproduces with original steps
- [ ] Minimal reproduction case now works
- [ ] Regression test added and passing
- [ ] No new failures in test suite
- [ ] Fix works in all environments
- [ ] Edge cases handled

## Phase 5: Documentation & Prevention

### Step 14: Document the Fix

Create fix documentation:

```markdown
# Bug Fix: [Issue Name]

## Problem
[What was broken]

## Root Cause
[Why it was broken]

## Fix
[What was changed]

Files modified:
- `path/to/file1.py:123` - [Change description]
- `path/to/file2.py:456` - [Change description]

## Testing
- Added test: `tests/test_[issue].py::test_should_not_[bug]`
- Verified: [Verification steps]

## Prevention
[How to prevent this class of bug in future]
```

### Step 15: Commit Fix

```bash
git add -A
git commit -m "fix: resolve [issue description]

Root cause: [One-line root cause]
Solution: [One-line solution]

- [Specific change 1]
- [Specific change 2]
- Added regression test

Fixes #[issue-number]

🤖 Generated with [Claude Code](https://claude.com/claude-code)

Co-Authored-By: Claude <noreply@anthropic.com>"
```

### Step 16: Prevention Analysis

**How to prevent similar bugs**:
- **Lint rule**: [Could a linter catch this?]
- **Type check**: [Would type hints prevent this?]
- **Test coverage**: [What test was missing?]
- **Code review**: [What review question would catch this?]
- **Architecture**: [What design pattern would prevent this?]

**Action items**:
- [ ] Add lint rule: [Specific rule]
- [ ] Add type hints: [Where]
- [ ] Improve test coverage: [What to test]
- [ ] Update review checklist: [What to check]
- [ ] Refactor if needed: [What to improve]

## Debugging Best Practices

**DO**:
- Read error messages completely (don't just grep for keywords)
- Reproduce before fixing (if you can't reproduce, you can't verify fix)
- Form hypotheses before changing code
- Test one hypothesis at a time
- Use git bisect for "when did this break" questions
- Add regression tests for all bug fixes
- Document root cause, not just fix

**DON'T**:
- Randomly change things hoping it works
- Skip reproduction steps
- Test multiple hypotheses simultaneously
- Fix symptoms instead of root cause
- Commit fixes without tests
- Debug in production (use staging/local)
- Give up after 3 failed attempts (take a break, ask for help)

## Emergency Debugging (Production Issues)

**If production is down**:

1. **Rollback first** (restore service immediately):
   ```bash
   git revert HEAD
   # or
   git reset --hard <last-working-commit>
   ```

2. **Then debug** (find root cause offline):
   - Reproduce in staging
   - Follow systematic process
   - Fix and test thoroughly
   - Deploy with monitoring

## Debugging Tools

**Logging**:
```python
import logging
logger = logging.getLogger(__name__)

# Add strategic logging
logger.debug(f"Variable state: {var}")
logger.info(f"Checkpoint reached: {checkpoint}")
logger.error(f"Error occurred: {error}", exc_info=True)
```

**Interactive debugging**:
```python
# Add breakpoint
import pdb; pdb.set_trace()

# Or use debugger
# - VS Code: F5
# - PyCharm: Shift+F9
# - Claude Code: Use logging instead
```

**Print debugging** (when debugger unavailable):
```python
print(f"DEBUG: {variable=}")
print(f"DEBUG: reached checkpoint A")
```

## When to Ask for Help

Ask for help after:
1. 3 failed hypothesis tests
2. 2 hours of debugging with no progress
3. Issue is outside your expertise area
4. Production impact is critical

**How to ask**:
- Show minimal reproduction
- Show hypotheses tested
- Show evidence collected
- Show what you've tried

Ready to implement the fix? Use `/tdd` for test-driven fix implementation.
