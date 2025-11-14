---
name: TDD Workflow
description: Test-driven development cycle and best practices (Red-Green-Refactor)
tags: tdd, testing, red-green-refactor, test-first
auto_load_triggers: tdd, test-driven, failing test, red-green
priority: toolkit
---

# TDD Workflow

## Purpose

Enforces test-driven development methodology: write tests first, see them fail (RED), implement minimal code to pass (GREEN), then refactor while keeping tests green.

---

## The TDD Cycle

### Step 1: Write Failing Tests

**ALWAYS write tests BEFORE implementation**:

```python
# Write test BEFORE implementation
def test_user_profile_creation():
    """Test creating user profile with valid data."""
    user = create_user_profile(name="Alice", email="alice@example.com")
    assert user.name == "Alice"
    assert user.email == "alice@example.com"
    assert user.created_at is not None
```

### Step 2: Confirm Tests Fail (RED Phase)

**Must see test failure before proceeding**:

```bash
pytest tests/test_user.py
# MUST see: FAILED - function create_user_profile doesn't exist
```

**If test passes immediately**:
- Test is not validating correctly
- Feature already exists
- Rewrite test to actually fail first

### Step 3: Commit Failing Tests

**Save RED state in version control**:

```bash
git add tests/test_user.py
git commit -m "test: add user profile creation test (RED)"
```

### Step 4: Implement Minimal Code

**Write ONLY enough code to pass the test** (no extra features):

```python
# Write ONLY enough code to pass the test
def create_user_profile(name: str, email: str) -> User:
    return User(
        name=name,
        email=email,
        created_at=datetime.now()
    )
```

### Step 5: Iterate Until Green (GREEN Phase)

**Keep iterating until test passes**:

```bash
pytest tests/test_user.py
# Keep iterating until: PASSED
```

**Green means**:
- Test passes
- All existing tests still pass
- Ready to refactor

### Step 6: Refactor

**Improve code quality while keeping tests green**:

```python
# Improve code quality while keeping tests green
# - Extract functions
# - Improve naming
# - Reduce duplication
# - Optimize performance

pytest tests/test_user.py  # Still passes after refactor
```

**Refactoring rules**:
- Tests MUST stay green
- If tests fail, revert refactoring
- Small incremental changes
- Re-run tests after each change

### Step 7: Commit (GREEN State)

**Save GREEN state in version control**:

```bash
git add -A
git commit -m "feat: implement user profile creation (GREEN)"
```

---

## TDD Rules (MANDATORY)

1. **NEVER write implementation before tests**
2. **ALWAYS see tests fail first** (RED phase)
3. **Write minimal code to pass** (no extra features)
4. **Refactor only when tests are green**
5. **Each test validates ONE thing**
6. **Tests are acceptance criteria**

---

## Test Structure - Given-When-Then

**Use Given-When-Then pattern for clarity**:

```python
def test_should_return_error_when_invalid_email():
    """Test error handling for invalid email format."""
    # Given: Invalid email input
    invalid_email = "not-an-email"

    # When: Attempt to create user
    with pytest.raises(ValidationError) as exc:
        create_user_profile(name="Bob", email=invalid_email)

    # Then: Should raise validation error with message
    assert "Invalid email format" in str(exc.value)
```

**Pattern breakdown**:
- **Given**: Setup/preconditions
- **When**: Action being tested
- **Then**: Expected outcome

---

## Autonomous TDD with Claude

**Workflow for AI-assisted TDD**:

1. User: "Write failing tests for user authentication"
2. Claude writes tests (NO implementation)
3. Claude runs tests → confirms they fail
4. Claude commits failing tests
5. User approves
6. Claude implements → iterates until tests pass
7. Claude refactors (tests still green)
8. Claude commits

**Maximum attempt limits**:
- Simple tasks: 1-3 turns
- Medium complexity: 5-10 turns
- Complex tasks: 10-20 turns
- Use `--max-turns` flag to prevent infinite loops

**Loop detection triggers**:
- Same files read >3 times
- Same test failures after multiple attempts
- Context approaching limits without progress
- **Action**: Use `/compact` or `/clear` or break task smaller

---

## Test Quality Standards

**All tests must have**:

- ✅ Clear descriptive names (Should_When pattern)
- ✅ Given-When-Then structure
- ✅ Single assertion focus
- ✅ Edge cases covered
- ✅ Error cases validated
- ✅ Performance benchmarks (where applicable)

**Example test suite**:

```python
class TestUserAuthentication:
    """Tests for user authentication system."""

    def test_should_authenticate_when_valid_credentials(self):
        """Test successful authentication."""
        # Given: Valid credentials
        # When: Authenticate
        # Then: Return auth token

    def test_should_reject_when_invalid_password(self):
        """Test invalid password rejection."""
        # Given: Wrong password
        # When: Authenticate
        # Then: Raise AuthenticationError

    def test_should_lockout_after_failed_attempts(self):
        """Test account lockout after 5 failed attempts."""
        # Given: 5 failed login attempts
        # When: 6th attempt
        # Then: Raise AccountLockedError
```

---

## Common Patterns

### Testing Exceptions

```python
def test_should_raise_error_when_invalid_input():
    """Test error handling."""
    with pytest.raises(ValueError) as exc:
        process_data(invalid_input)

    assert "Invalid input" in str(exc.value)
```

### Testing Async Functions

```python
async def test_async_operation():
    """Test async function."""
    result = await async_function()
    assert result == expected_value
```

### Parametrized Tests

```python
@pytest.mark.parametrize("input,expected", [
    ("test", "TEST"),
    ("hello", "HELLO"),
    ("", ""),
])
def test_uppercase(input, expected):
    """Test multiple inputs."""
    assert uppercase(input) == expected
```

---

## Integration with Quality Gate

**Before marking task complete**:

1. All tests pass (GREEN state)
2. Coverage meets threshold (≥80%)
3. No linting errors
4. Quality gate passes

**Use MCP tools**:
```
mcp__quality__run_quality_gate
Args:
  project_path = current working directory
  changes_made = list of files modified
```

---

## When to Use TDD

**Always use TDD for**:
- New features
- Bug fixes (write failing test first)
- Refactoring (tests ensure behavior preserved)
- API changes

**TDD less critical for**:
- Exploratory prototyping (but add tests after)
- UI layout (use visual testing instead)
- Configuration files

---

## TDD Anti-Patterns

**DON'T**:
- ❌ Write implementation before tests
- ❌ Skip seeing tests fail (RED phase)
- ❌ Write tests that always pass
- ❌ Test implementation details (test behavior)
- ❌ Make tests depend on each other
- ❌ Write flaky tests (non-deterministic)

**DO**:
- ✅ Write tests for edge cases
- ✅ Keep tests independent
- ✅ Use descriptive test names
- ✅ Test one thing per test
- ✅ Refactor tests too

---

## Resources

- **CLAUDE.md**: Full TDD workflow (section: Test-Driven Development)
- **quality-standards skill**: Testing requirements and code quality
- **/tdd slash command**: Automated TDD cycle execution
- **docs/guides/**: Additional TDD examples and patterns
