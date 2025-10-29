# Claude Code Usage - Best Practices for Effective AI-Assisted Development

> **Purpose**: Maximize Claude Code efficiency while maintaining code quality and project standards
> **Audience**: Developers using Claude Code with the Minimal Root project structure
> **Last Updated**: 2025-10-26
> **Version**: 1.0

---

## Table of Contents

1. [Project Context & Initialization](#project-context--initialization)
2. [Effective Communication Patterns](#effective-communication-patterns)
3. [Quality Gates Integration](#quality-gates-integration)
4. [Test-Driven Development with AI](#test-driven-development-with-ai)
5. [File Operations Best Practices](#file-operations-best-practices)
6. [Advanced Features](#advanced-features)
7. [Safety Protocols](#safety-protocols)
8. [Custom Commands & Workflows](#custom-commands--workflows)
9. [Common Mistakes to Avoid](#common-mistakes-to-avoid)
10. [Quick Reference](#quick-reference)

---

## Project Context & Initialization

### The Critical First Step: Context Setup

Claude Code's effectiveness depends on **understanding your project structure**. Poor context = poor results.

#### When Starting a New Session

```markdown
# First interaction in a new chat
"Review the CLAUDE.md file to understand this project's structure,
quality standards, and file placement rules."
```

**Why this works**:
- Claude reads your project's "constitution" (CLAUDE.md)
- Understands file placement rules
- Knows quality standards (80% coverage, functions ≤30 lines, etc.)
- Aware of TDD workflow requirements

#### Reference Project Documentation

| Document | When to Reference | Command |
|----------|------------------|---------|
| `CLAUDE.md` | Start of session | `@CLAUDE.md - Read this first` |
| `docs/notes/plan.md` | Before new features | `@docs/notes/plan.md - What's the current plan?` |
| `docs/design/architecture.md` | Architecture questions | `@docs/design/architecture.md - Review the architecture` |
| `pyproject.toml` | Tool configuration | `@pyproject.toml - Check our quality settings` |

#### Update Context When Needed

```markdown
# When you make significant changes
"Update CLAUDE.md to reflect the new authentication module we just added."

# When plans change
"Update docs/notes/plan.md - we're postponing feature X, prioritizing Y."
```

**Best Practice**: Keep context documents current. Stale context = confused AI.

---

## Effective Communication Patterns

### The Golden Rule: Reference, Don't Paste

#### ❌ BAD: Pasting Entire Files

```markdown
"Here's my code:
[pastes 200 lines]
Can you fix the bug?"
```

**Problems**:
- Wastes tokens (costs money, slower responses)
- Loses file context (Claude doesn't know where it lives)
- Can't track changes properly
- Difficult to apply fixes

#### ✅ GOOD: Reference Files by Path

```markdown
"There's a bug in @src/services/processor.py at line 47.
The function isn't handling None values correctly."
```

**Benefits**:
- Claude reads the file in context
- Knows exact location
- Can suggest precise edits
- Maintains file structure awareness
- Uses fewer tokens

### Using the `@` Symbol Effectively

| Usage | Example | When to Use |
|-------|---------|-------------|
| **Single file** | `@src/core/models.py` | Discussing specific file |
| **Multiple files** | `@src/core/models.py @tests/unit/test_models.py` | Related files (code + test) |
| **Directories** | `@src/services/` | Discussing entire module |
| **Documentation** | `@docs/design/architecture.md` | Referencing design docs |

### Prompt Patterns That Work

#### Pattern 1: Context + Task + Constraints

```markdown
"In @src/adapters/parser.py, refactor the parse_csv() function to:
1. Handle encoding errors gracefully
2. Keep function ≤30 lines (our standard)
3. Add comprehensive error logging
4. Maintain existing test compatibility"
```

#### Pattern 2: Problem + Expected Behavior

```markdown
"The test in @tests/integration/test_import_flow.py is failing.
Expected: Import completes with 100 records
Actual: Import stops at 50 records
Debug and fix."
```

#### Pattern 3: Request for Analysis Before Action

```markdown
"Before implementing feature X in @src/core/calculator.py:
1. Review the existing architecture
2. Identify potential impacts on other modules
3. Propose 2-3 implementation approaches
4. Recommend the best approach with rationale"
```

**Best Practice**: Give context, be specific, set constraints. Avoid vague requests like "make it better."

---

## Quality Gates Integration

### Enforcing Standards Automatically

Your project has quality gates (`.ai-validation/check_quality.sh`). **Claude should run these before suggesting commits.**

#### Standard Quality Workflow

```markdown
# 1. Make changes
"Add type hints to all functions in @src/core/utils.py"

# 2. Validate (Claude should do this automatically, but you can prompt)
"Run the quality gates and fix any issues"

# 3. Claude should report:
# ✓ Tests passed (coverage 85%)
# ✓ Ruff linting passed
# ✓ MyPy type checking passed
# ✓ Bandit security passed
# ✓ Radon complexity passed
```

#### When Quality Gates Fail

Claude should:
1. **Read the error output**
2. **Fix the specific issues**
3. **Re-run quality gates**
4. **Confirm all pass**

**Don't accept**: "I've made the changes, the tests should pass now."
**Require**: "I've made the changes and verified all quality gates pass."

#### Custom Quality Prompts

```markdown
# Security focus
"Review @src/infrastructure/database.py for security issues.
Run Bandit and fix any medium/high severity findings."

# Complexity focus
"Refactor @src/services/report_generator.py to reduce complexity.
All functions must have cyclomatic complexity ≤10."

# Coverage focus
"Improve test coverage for @src/core/calculator.py to ≥90%.
Focus on edge cases and error conditions."
```

### Quality Gate Checklist

Before ANY commit, Claude should confirm:

- [ ] All tests pass (`pytest`)
- [ ] Coverage ≥ 80% (`pytest --cov`)
- [ ] No linting errors (`ruff check .`)
- [ ] No type errors (`mypy src/`)
- [ ] No security issues (`bandit -r src/`)
- [ ] Complexity acceptable (`radon cc src/`)
- [ ] Docstrings present (`interrogate src/`)

**Best Practice**: Make Claude run `.ai-validation/check_quality.sh` before every commit suggestion.

---

## Test-Driven Development with AI

### The TDD Cycle with Claude

Claude Code can accelerate TDD, but **you must enforce the cycle**:

```
1. WRITE TEST (RED)
   ↓
2. IMPLEMENT CODE (GREEN)
   ↓
3. REFACTOR (CLEAN)
   ↓
4. VALIDATE QUALITY GATES
```

### Phase 1: Write the Test First

#### Effective Test Prompts

```markdown
# Specific test requirements
"Write a unit test in @tests/unit/test_parser.py for the parse_starling_csv() function.
Test cases:
1. Valid CSV with 10 transactions
2. Empty CSV file
3. CSV with invalid date format
4. CSV with missing required fields
Expected: Given-When-Then structure, pytest fixtures, 100% branch coverage"

# Integration test
"Write an integration test in @tests/integration/test_import_flow.py for the complete import pipeline.
Test: Scanner finds file → Parser processes → Database inserts → Batch status updates
Expected: Real file fixtures, database cleanup, clear assertions"
```

#### Test Quality Standards

Claude-generated tests should include:
- ✅ **Given-When-Then structure** in docstring
- ✅ **Descriptive test names** (`test_parse_handles_missing_date_column`)
- ✅ **Fixtures for setup** (defined in `conftest.py`)
- ✅ **Clear assertions** with messages
- ✅ **Edge cases and errors** (not just happy path)
- ✅ **Cleanup** (for integration tests)

### Phase 2: Implement to Pass

```markdown
"Implement the parse_starling_csv() function in @src/parsers/starling.py
to make the tests in @tests/unit/test_parser.py pass.

Constraints:
- Function ≤30 lines
- Full type hints
- Google-style docstring
- Handle all error cases from tests
- Log errors using our standard logger"
```

**Best Practice**: Reference the test file so Claude knows exactly what behavior to implement.

### Phase 3: Refactor

```markdown
"The tests pass, but the code in @src/parsers/starling.py is complex.
Refactor to:
1. Reduce cyclomatic complexity (currently 12, target ≤10)
2. Extract repeated logic to helper functions
3. Improve readability
4. Keep all tests passing"
```

**Critical**: Run tests after refactoring to ensure behavior unchanged.

### Phase 4: Validate

```markdown
"Run the quality gates for the changes we just made.
Confirm:
- All tests pass
- Coverage for src/parsers/starling.py is ≥80%
- No linting/type/security errors
- Complexity ≤10 for all functions"
```

---

## File Operations Best Practices

### Creating New Files

#### ❌ BAD: Vague Location

```markdown
"Create a new parser for HSBC"
```

**Problem**: Where should it go? Claude might guess wrong.

#### ✅ GOOD: Specific Path

```markdown
"Create a new parser file at src/parsers/hsbc.py following the pattern in @src/parsers/starling.py.
Include:
- Parser class inheriting from BaseParser
- parse() method with type hints
- Google-style docstrings
- Error handling for common CSV issues"
```

**Best Practice**: Always specify the exact path and reference a similar file as a template.

### Editing Existing Files

#### ❌ BAD: Rewrite Entire File

```markdown
"Rewrite @src/core/models.py to use dataclasses"
```

**Problem**: Loses working code, may break things.

#### ✅ GOOD: Targeted Changes

```markdown
"In @src/core/models.py, convert the Transaction class (lines 45-78) to a dataclass.
Preserve:
- All existing fields
- The validate() method
- Compatibility with existing tests in @tests/unit/test_models.py"
```

**Best Practice**: Specify what to change, what to preserve, and how to verify.

### Deleting Code

#### Safe Deletion Protocol

```markdown
"Before deleting the old_importer.py file:
1. Check if any files import from it (grep for 'from old_importer')
2. Verify no tests reference it
3. Confirm it's marked as deprecated in git history
4. If safe to delete, move to artifacts/.archive/ with date prefix"
```

**Best Practice**: Claude should verify no dependencies before deletion.

### Moving Files

```markdown
"Move @src/utils/file_ops.py to @src/infrastructure/file_system.py.
Update all imports across the project.
Run tests to verify nothing breaks."
```

**Best Practice**: Include import updates and test verification.

---

## Advanced Features

### Multi-Agent Workflows

For complex tasks, Claude can spawn multiple agents to work in parallel.

#### When to Use Multi-Agent

✅ **Good use cases**:
- Exploring multiple design approaches
- Large refactoring across many files
- Comprehensive code analysis
- Generating multiple test scenarios

❌ **Poor use cases**:
- Simple, single-file changes
- When you need complete control
- Quick bug fixes

#### Example: Design Exploration

```markdown
"Using concurrent agents, propose 3 different architectures for the CGT calculation module:

Agent 1: Object-oriented with classes for each calculation rule
Agent 2: Functional approach with pure functions
Agent 3: Data-driven with configuration files

For each approach, provide:
- Code structure diagram
- Main advantages/disadvantages
- Complexity estimate
- Testing strategy
- Migration effort from current code"
```

**Best Practice**: Use for exploration and analysis, not for direct implementation.

### Task Agent for Deep Work

The Task agent can work autonomously on complex, multi-step tasks.

#### Effective Task Agent Prompts

```markdown
"Launch a Task agent to:
1. Analyze all parser files in @src/parsers/
2. Identify code duplication across parsers
3. Design a base parser class to eliminate duplication
4. Estimate the refactoring effort
5. Report back with findings and recommendations

Do NOT make changes, just analyze and recommend."
```

**Best Practice**:
- Use for research and analysis tasks
- Be specific about what NOT to do (e.g., "do not make changes")
- Request a report, not direct implementation

### Code Search with Explore Agent

For navigating large codebases:

```markdown
"Use the Explore agent to find all locations where we:
1. Make database queries without error handling
2. Parse dates without timezone awareness
3. Log sensitive information

Report file paths and line numbers."
```

**Best Practice**: Use for codebase discovery, security audits, and refactoring planning.

---

## Safety Protocols

### The Dangers of "YOLO Mode"

Some Claude Code interfaces offer a "dangerously-skip-permissions" or "auto-approve" mode.

**⚠️ WARNING**: This removes ALL safety checks. Claude will make changes without asking.

#### When YOLO Mode Might Be Acceptable

✅ **Only if ALL of these are true**:
- You're working in a feature branch (not main)
- You have **uncommitted work** you can easily revert with `git reset --hard`
- You're doing exploratory refactoring
- You're watching the changes in real-time
- You can immediately review with `git diff`

#### YOLO Mode Survival Protocol

```bash
# 1. Create safety branch
git checkout -b experiment/claude-refactor

# 2. Commit current state
git add .
git commit -m "Safe state before YOLO mode"

# 3. Enable YOLO mode (if you must)
# (method depends on your Claude Code client)

# 4. Let Claude work

# 5. IMMEDIATELY review changes
git diff HEAD

# 6. Run quality gates
.ai-validation/check_quality.sh

# 7. Decision point:
# Accept: git add . && git commit -m "Refactoring from Claude"
# Reject: git reset --hard HEAD
```

**Best Practice**: **DON'T USE YOLO MODE**. The approval step takes 2 seconds and prevents disasters.

### Git Workflow Integration

#### Before Claude Makes Changes

```markdown
"Before making any changes:
1. Show me your planned changes (file list)
2. Explain the impact on existing functionality
3. Identify which tests will need updates"
```

#### After Claude Makes Changes

```markdown
"You've made changes to 5 files. Please:
1. Show me a summary of changes per file
2. Run the quality gates
3. Run relevant tests
4. If all pass, suggest a commit message"
```

#### Commit Message Standards

Claude should generate commit messages following your project's format:

```markdown
"Generate a commit message for these changes following our format:

[type]: brief description

- Detailed change 1
- Detailed change 2

Fixes: #issue-number (if applicable)
```

**Types**: `feat`, `fix`, `refactor`, `test`, `docs`, `chore`

### Rollback Protocol

If Claude makes a mistake:

```bash
# If changes not committed
git status
git diff  # Review
git checkout -- <file>  # Discard changes to specific file
git reset --hard HEAD  # Discard all changes (DANGER!)

# If changes committed
git log  # Find the bad commit
git revert <commit-hash>  # Safe: creates new commit undoing changes
git reset --hard HEAD~1  # DANGER: deletes the commit
```

**Best Practice**: Use `git revert` for safety, not `git reset --hard`.

---

## Custom Commands & Workflows

### Creating Reusable Workflows

Define custom commands in `.claude/commands/` for repeated tasks.

#### Example: Unit Test Command

Create `.claude/commands/unit-test.md`:

```markdown
# Unit Test Generator

When I use `/unit-test <module>`, perform the following:

1. Identify the module at `src/<module>.py`
2. Generate comprehensive unit tests in `tests/unit/test_<module>.py`
3. Include test cases for:
   - Happy path (normal operation)
   - Edge cases (boundary conditions)
   - Error cases (invalid inputs)
   - Type validation
4. Use Given-When-Then docstring format
5. Aim for ≥90% coverage for this module
6. Run the tests and confirm they pass
7. Report coverage percentage

Example:
/unit-test parser
# Generates tests/unit/test_parser.py with comprehensive coverage
```

#### Example: Security Audit Command

Create `.claude/commands/security-audit.md`:

```markdown
# Security Audit

When I use `/security-audit <file>`, perform:

1. Read the file at `<file>`
2. Run Bandit security scanner
3. Check for common vulnerabilities:
   - SQL injection risks
   - Path traversal issues
   - Hardcoded secrets
   - Unsafe deserialization
   - Command injection
4. Review for our Security Priority standards
5. Report findings with severity levels
6. Suggest fixes for any issues found

Example:
/security-audit src/infrastructure/database.py
```

#### Example: Refactor Command

Create `.claude/commands/refactor.md`:

```markdown
# Intelligent Refactoring

When I use `/refactor <file>`, perform:

1. Analyze the file for:
   - Functions >30 lines
   - Cyclomatic complexity >10
   - Code duplication
   - Missing docstrings
   - Missing type hints
2. Propose specific refactoring changes
3. Maintain ALL existing functionality
4. Ensure all tests still pass
5. Run quality gates after refactoring
6. Report before/after metrics

Constraints:
- Functions ≤30 lines
- Complexity ≤10
- 100% type hints on public functions
- Google-style docstrings

Example:
/refactor src/services/processor.py
```

### Workflow Templates

#### Morning Standup Review

```markdown
"Review the project status:
1. Read @artifacts/logs/completed-actions.log (last 3 days)
2. Read @docs/notes/plan.md (current plan)
3. Read @docs/notes/todo.md (pending tasks)
4. Summarize: what's done, what's next, any blockers"
```

#### Pre-Commit Checklist

```markdown
"Before I commit, perform the pre-commit checklist:
1. Run quality gates (.ai-validation/check_quality.sh)
2. Verify all tests pass
3. Check for TODO/FIXME comments in changed files
4. Review for any hardcoded secrets or sensitive data
5. Confirm files are in correct locations per CLAUDE.md
6. Generate a proper commit message
7. Update artifacts/logs/completed-actions.log"
```

#### Weekly Cleanup

```markdown
"Perform weekly maintenance:
1. Check for unused imports across src/
2. Identify deprecated functions still in use
3. Review test coverage and identify gaps
4. Check for large files that should be split
5. Update documentation if code has changed
6. Clean up artifacts/temp/ (old debug scripts)
7. Generate a summary report"
```

---

## Common Mistakes to Avoid

### Mistake 1: Trusting Without Verifying

❌ **Don't do this**:
```markdown
"The code looks good, commit it."
```

✅ **Do this instead**:
```markdown
"Before committing, run the quality gates and show me the results."
```

**Lesson**: Always verify. Claude can make mistakes.

### Mistake 2: Over-Relying on Claude for Architecture

❌ **Don't do this**:
```markdown
"Design the entire authentication system and implement it."
```

✅ **Do this instead**:
```markdown
"Propose 3 authentication approaches with pros/cons.
I'll decide which to implement, then we'll do it step-by-step with tests."
```

**Lesson**: You make strategic decisions, Claude assists with tactical implementation.

### Mistake 3: Letting Claude Create Lots of Files

❌ **Don't do this**:
```markdown
"Create all the files we need for this feature."
```

✅ **Do this instead**:
```markdown
"List the files we need for this feature with their purposes.
I'll approve the list, then we'll create them one at a time with tests."
```

**Lesson**: Control file creation to maintain project structure.

### Mistake 4: Not Updating Documentation

❌ **Don't do this**:
```markdown
[Make major changes without updating CLAUDE.md or docs/]
```

✅ **Do this instead**:
```markdown
"We just added a new authentication module.
Update:
1. CLAUDE.md (file placement rules for auth code)
2. docs/design/architecture.md (auth architecture)
3. docs/notes/plan.md (mark auth task complete)"
```

**Lesson**: Keep documentation current or Claude will get confused in future sessions.

### Mistake 5: Asking Claude to "Fix Everything"

❌ **Don't do this**:
```markdown
"The tests are failing, fix everything."
```

✅ **Do this instead**:
```markdown
"Run pytest -v and show me which specific tests are failing.
Then we'll debug them one at a time, starting with test_parse_csv."
```

**Lesson**: Incremental, focused fixes are more reliable than shotgun approaches.

### Mistake 6: Ignoring Token Limits

❌ **Don't do this**:
```markdown
[Reference 20 large files in one prompt]
```

✅ **Do this instead**:
```markdown
"Review just the parse() method in @src/parsers/starling.py
and its test in @tests/unit/test_parser.py"
```

**Lesson**: Be selective with file references to avoid context overload.

### Mistake 7: Not Using Git for Safety

❌ **Don't do this**:
```markdown
[Let Claude make changes without committing working state first]
```

✅ **Do this instead**:
```bash
# Always commit working state before major changes
git add .
git commit -m "Working state before Claude refactoring"
# Now let Claude work
```

**Lesson**: Git is your safety net. Use it.

---

## Quick Reference

### Essential Commands

```markdown
# Context
"Read @CLAUDE.md to understand the project"

# File Reference
"Review @src/core/models.py"

# Quality Gates
"Run .ai-validation/check_quality.sh and fix any issues"

# TDD Cycle
"Write test for X in @tests/unit/"
"Implement X in @src/ to pass the test"
"Refactor X to meet quality standards"

# Safety
"Before making changes, explain your plan"
"After changes, run tests and quality gates"
```

### Quality Gate Checklist

```markdown
Before committing, verify:
- [ ] pytest passes
- [ ] Coverage ≥80%
- [ ] ruff check passes
- [ ] mypy passes
- [ ] bandit passes
- [ ] radon complexity ≤10
- [ ] Documentation updated
- [ ] artifacts/logs/completed-actions.log updated
```

### File Placement Quick Reference

```markdown
src/              → Production code
tests/unit/       → Unit tests
tests/integration/→ Integration tests
docs/design/      → Architecture docs
docs/notes/       → Active work (plan.md, todo.md)
artifacts/logs/   → Logs (completed-actions.log)
artifacts/temp/   → Temporary scripts
artifacts/migrations/ → DB migrations (if not using root migrations/)
```

### Common Prompt Patterns

```markdown
# Analysis
"Analyze @<file> for <criteria> and report findings"

# Implementation
"In @<file>, implement <feature> following <constraints>"

# Testing
"Write tests for @<file> covering <scenarios>"

# Refactoring
"Refactor @<file> to <goal> while maintaining <constraints>"

# Review
"Review @<file> for <quality-aspect> and suggest improvements"
```

### Safety Workflow

```bash
# 1. Safe state
git status
git add .
git commit -m "Safe state"

# 2. Let Claude work
# ...

# 3. Review
git diff

# 4. Validate
.ai-validation/check_quality.sh

# 5. Accept or reject
git add . && git commit  # Accept
git reset --hard HEAD    # Reject (back to safe state)
```

---

## Integration with Project Standards

### Aligning with CLAUDE.md

Your `CLAUDE.md` file defines project standards. **Remind Claude of these frequently**:

```markdown
"As per CLAUDE.md, ensure:
- All code goes in src/
- All tests go in tests/
- Functions ≤30 lines
- Coverage ≥80%
- Full type hints
- Google-style docstrings"
```

### Aligning with Quality Gates

Reference your quality gate script:

```markdown
"Our quality gates are defined in @.ai-validation/check_quality.sh.
Run this script after every change and fix any failures."
```

### Aligning with TDD Workflow

Enforce the cycle:

```markdown
"Follow our TDD workflow:
1. Write test in tests/
2. Implement code in src/
3. Refactor to meet standards
4. Run quality gates
5. Log to artifacts/logs/completed-actions.log"
```

---

## Conclusion

**Claude Code is a powerful assistant, but YOU are the architect.**

### Golden Rules

1. **Context is King**: Keep CLAUDE.md and docs/ current
2. **Reference, Don't Paste**: Use `@file` notation
3. **Test First**: Always write tests before implementation
4. **Verify Everything**: Run quality gates, review diffs
5. **Git is Your Friend**: Commit often, rollback when needed
6. **Stay in Control**: Claude suggests, you decide
7. **Document Changes**: Update docs/ and logs/

### Success Metrics

You're using Claude Code effectively when:

✅ Quality gates pass on every commit
✅ Test coverage stays ≥80%
✅ Documentation stays current
✅ You can explain every change Claude makes
✅ You catch mistakes before committing
✅ You use Git to safely experiment
✅ You feel in control, not overwhelmed

---

**Claude Code amplifies good practices and accelerates development, but cannot replace thoughtful engineering.**

Use it wisely. 🚀
