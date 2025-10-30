---
description: Execute test-driven development cycle for a feature
---

# TDD Cycle: $ARGUMENTS

Execute the Red-Green-Refactor cycle for: "$ARGUMENTS"

## Phase 1: RED - Write Failing Tests

### Step 1: Write Test First

**CRITICAL**: Write tests BEFORE any implementation.

```python
# tests/test_[feature].py

def test_should_[behavior]_when_[condition]():
    """Test [specific behavior]."""
    # Given: [Setup test conditions]

    # When: [Execute the behavior]

    # Then: [Assert expected outcome]
    assert expected == actual
```

**Test Requirements**:
- Use Given-When-Then structure
- Clear descriptive name (Should_When pattern)
- Single assertion per test
- Cover happy path AND edge cases
- Include error conditions

### Step 2: Confirm Tests Fail

Run tests and VERIFY they fail for the right reason:

```bash
pytest tests/test_[feature].py -v
```

**Expected output**: FAILED (function doesn't exist or wrong behavior)

**If tests pass**: STOP - Tests are wrong, fix tests first

### Step 3: Commit Failing Tests

```bash
git add tests/test_[feature].py
git commit -m "test: add [feature] tests (RED)"
```

## Phase 2: GREEN - Make Tests Pass

### Step 4: Write Minimal Implementation

**Rules**:
- Write ONLY enough code to pass tests
- No extra features
- No premature optimization
- Simple implementation first

### Step 5: Run Tests - Iterate Until Green

```bash
pytest tests/test_[feature].py -v
```

**If tests fail**:
- Analyze failure message
- Fix implementation
- Re-run tests
- Repeat until ALL tests pass

**Loop detection** (if stuck after 3 attempts):
1. Review test expectations
2. Simplify implementation approach
3. Break into smaller steps
4. Ask for help if blocked

### Step 6: Verify All Tests Pass

```bash
# Run full test suite to ensure no regressions
pytest tests/ -v

# Check coverage
pytest tests/ --cov=[module] --cov-report=term-missing
```

**Must see**: All tests PASSED, coverage ≥80%

## Phase 3: REFACTOR - Improve Code

### Step 7: Refactor (Tests Stay Green)

**Now improve code quality**:
- Extract duplicate code
- Improve naming
- Simplify logic
- Add type hints
- Enhance docstrings

**CRITICAL**: Run tests after EVERY refactor step

```bash
pytest tests/test_[feature].py -v
# Must remain GREEN
```

### Step 8: Final Validation

Run quality checks:

```bash
# Linting
ruff check [file].py

# Type checking
mypy [file].py

# Run all tests
pytest tests/ -v

# Run quality gate
cd .ai-validation && bash check_quality.sh
```

**All must pass** before committing.

### Step 9: Commit

```bash
git add -A
git commit -m "feat: implement [feature] (GREEN)

- [What was implemented]
- Tests passing: [X/X]
- Coverage: [X%]"
```

## Autonomous TDD Loop

For autonomous execution, follow this pattern:

**User says**: "Use TDD to implement [feature]"

**Claude executes**:
1. Write comprehensive tests (RED)
2. Run tests → see failures
3. Commit failing tests
4. Implement minimal solution
5. Run tests → iterate autonomously until GREEN
6. Refactor with tests green
7. Run quality gate
8. Commit
9. Report completion with test results

**Maximum iterations**: Use `--max-turns 10` to prevent infinite loops

**Progress reporting**:
- After RED phase: "Tests written and failing (expected)"
- During GREEN: "Iteration X/10 - Y tests passing"
- After GREEN: "All tests passing - refactoring"
- After refactor: "Refactor complete - tests still green"
- After quality gate: "Quality gate PASSED - ready to commit"

## TDD Best Practices

**DO**:
- Write tests first (always)
- See tests fail before implementation
- Write minimal code to pass
- Refactor only when green
- Commit after each cycle
- Keep tests independent

**DON'T**:
- Write implementation before tests
- Skip seeing tests fail (RED phase)
- Add extra features beyond tests
- Refactor with failing tests
- Ignore test failures
- Write tests that depend on each other

## Edge Case Coverage

Ensure tests cover:
- Happy path (valid inputs, expected outputs)
- Invalid inputs (wrong types, out of range)
- Empty/null values
- Boundary conditions
- Error conditions
- Performance requirements (if specified)
- Security requirements (if specified)
