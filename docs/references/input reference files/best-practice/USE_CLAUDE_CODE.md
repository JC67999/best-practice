# Claude Code Usage - Best Practices for Effective AI-Assisted Development

> **Purpose**: Maximize Claude Code efficiency while maintaining code quality and project standards
> **Audience**: Developers using Claude Code with the Minimal Root project structure
> **Last Updated**: 2025-10-26
> **Version**: 1.1 (Refined based on professional review)

---

## Version 1.1 Changes

**Refinements based on professional feedback**:
1. ✨ Consolidated repetitive checklists - now reference master script
2. ✨ Clarified CLAUDE.md update protocol - only for architectural changes
3. ✨ Refined file deletion protocol - distinguish source code vs ephemeral data

---

## How to Use This Guide

**Choose your reading path based on experience level:**

- **Beginner (0-2 weeks)**: Read [Quick Start](#quick-start-5-minutes) + [Quick Reference](#quick-reference) only
- **Intermediate (2-8 weeks)**: Add [Quality Gates](#quality-gates-integration) + [TDD](#test-driven-development-with-ai) sections
- **Advanced (2+ months)**: Explore [Advanced Configuration](#advanced-configuration-power-users)
- **Reference**: Use [Quick Reference](#quick-reference) + search (Ctrl+F)

**TL;DR**: Skip to [Quick Start](#quick-start-5-minutes) to get productive in 5 minutes.

---

## Table of Contents

1. [⚡ Quick Start (5 Minutes)](#quick-start-5-minutes) ← **START HERE**
2. [Quick Reference](#quick-reference) ← **Use Daily**
3. [Project Context & Initialization](#project-context--initialization)
4. [Effective Communication Patterns](#effective-communication-patterns)
5. [Quality Gates Integration](#quality-gates-integration)
6. [Test-Driven Development with AI](#test-driven-development-with-ai)
7. [File Operations Best Practices](#file-operations-best-practices)
8. [Advanced Features](#advanced-features)
9. [Safety Protocols](#safety-protocols)
10. [Custom Commands & Workflows](#custom-commands--workflows)
11. [Common Mistakes to Avoid](#common-mistakes-to-avoid)
12. [Advanced Configuration (Power Users)](#advanced-configuration-power-users)

---

## ⚡ Quick Start (5 Minutes)

**Just want to get productive right now? Here's everything you need:**

### 1. Start Every Session (30 seconds)

```markdown
"Read @CLAUDE.md to understand this project's structure and standards"
```

**What this does**: Loads your project's file placement rules, quality standards, and workflow requirements into Claude's context.

### 2. The Basic Development Cycle (4 minutes)

**Test-Driven Development with Claude:**

```markdown
# Step 1: Write the test FIRST (1 minute)
"Write a unit test in @tests/unit/test_parser.py for the parse_csv() function.
Test cases: valid CSV, empty file, invalid format"

# Step 2: Implement to pass the test (2 minutes)
"Implement parse_csv() in @src/parser.py to make the tests pass.
Keep it ≤30 lines, full type hints, Google-style docstring"

# Step 3: Validate quality (1 minute)
"Run bash .ai-validation/check_quality.sh and report results"
```

### 3. Essential Commands

```markdown
# Reference files with @
"Review @src/models.py"

# Check quality before committing
"Run the quality gates and confirm all pass"

# Get help
"Read @CLAUDE.md section on file placement rules"
```

### 4. The Golden Rule

**NEVER paste code into chat. ALWAYS use file references:**

❌ BAD: `"Here's my code: [pastes 200 lines]"`
✅ GOOD: `"Review @src/parser.py - there's a bug at line 47"`

### That's It!

**You're now ready to use Claude Code effectively.**

For more details:
- **Daily reference**: Jump to [Quick Reference](#quick-reference)
- **Quality workflow**: See [Quality Gates](#quality-gates-integration)
- **Common questions**: Check [Common Mistakes](#common-mistakes-to-avoid)
- **Advanced features**: Explore [Advanced Configuration](#advanced-configuration-power-users) (when ready)

---

## Quick Reference

> **Use this section daily** - Bookmark this for quick command lookup

### Essential Commands

```markdown
# Context
"Read @CLAUDE.md to understand the project"

# File Reference
"Review @src/core/models.py"

# Quality Gates (Master Script)
"Run bash .ai-validation/check_quality.sh and report results"

# TDD Cycle
"Write test for X in @tests/unit/"
"Implement X in @src/ to pass the test"
"Refactor X to meet quality standards"
"Run quality gates to confirm all pass"

# Safety
"Before making changes, explain your plan"
"After changes, run tests and quality gates"
```

### Pre-Commit Checklist

```markdown
Before committing, Claude must:
1. Run: bash .ai-validation/check_quality.sh
2. Report: All checks passed (pytest, ruff, mypy, bandit, radon, interrogate)
3. Confirm: No TODO/FIXME in changed files
4. Verify: No hardcoded secrets
5. Check: Files in correct locations per CLAUDE.md
6. Update: artifacts/logs/completed-actions.log
7. Generate: Proper commit message
```

**Master script validates**: Tests (≥80% coverage), Ruff (linting), MyPy (types), Bandit (security), Radon (complexity ≤10), Interrogate (docstrings ≥80%)

### File Placement Quick Reference

```markdown
src/              → Production code
tests/unit/       → Unit tests
tests/integration/→ Integration tests
docs/design/      → Architecture docs
docs/notes/       → Active work (plan.md, todo.md)
artifacts/logs/   → Logs (completed-actions.log)
artifacts/temp/   → Temporary scripts
artifacts/migrations/ → DB migrations (or root migrations/ for database projects)
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
bash .ai-validation/check_quality.sh

# 5. Accept or reject
git add . && git commit  # Accept
git reset --hard HEAD    # Reject (back to safe state)
```

### When to Update Documentation

```markdown
# CLAUDE.md (RARE - only architectural changes)
- New database layer
- Framework change
- Modified TDD cycle
- New top-level directory
- Changed quality thresholds

# Design Docs (FREQUENT - detailed decisions)
- docs/design/architecture.md - Architecture details
- docs/design/decisions/ - ADRs for specific choices

# Task Docs (DAILY - active work)
- docs/notes/plan.md - Current development plan
- docs/notes/todo.md - Task tracking
- artifacts/logs/completed-actions.log - Work log
```

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

#### When to Update CLAUDE.md

**IMPORTANT**: CLAUDE.md should be relatively stable. Only update for **architectural changes**.

```markdown
# When to Update CLAUDE.md (RARE)

Update CLAUDE.md ONLY when there is a major architectural change:
- ✅ Adding a new database layer
- ✅ Changing application framework (e.g., Flask → FastAPI)
- ✅ Modifying the core TDD cycle
- ✅ Adding new top-level directories to project structure
- ✅ Changing quality gate requirements (e.g., coverage threshold)

Do NOT update CLAUDE.md for:
- ❌ Daily feature work
- ❌ New modules within existing structure
- ❌ Bug fixes
- ❌ Routine refactoring
```

**For daily work**: Update task-specific documents instead:
- `docs/design/architecture.md` - Detailed design decisions
- `docs/design/decisions/` - Architecture Decision Records (ADRs)
- `docs/notes/plan.md` - Current development plan
- `docs/notes/todo.md` - Task tracking

**Best Practice**: Keep CLAUDE.md as your project's **stable constitution**, not a changelog.

---

## Effective Communication Patterns

### The Golden Rule: Reference, Don't Paste

This is the **most crucial, high-value takeaway** for effective Claude Code usage.

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
- AI loses awareness of project structure

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
- **Maintains AI's awareness of Minimal Root Philosophy**

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

### The Master Quality Gate Script

Your project has a comprehensive quality validation script that checks **all standards** in one command.

#### Quality Gate Requirement

**Before ANY commit, Claude must execute and report a passing result for:**

```bash
bash .ai-validation/check_quality.sh
```

**This script verifies all project standards**:
- ✅ **pytest** - All tests pass with ≥80% coverage
- ✅ **Ruff** - Zero linting errors
- ✅ **MyPy** - Zero type errors (strict mode)
- ✅ **Bandit** - Zero medium/high security issues
- ✅ **Radon** - Cyclomatic complexity ≤10
- ✅ **Interrogate** - Docstring coverage ≥80%

**Claude should report**:
```markdown
✓ Quality gates passed:
  - Tests: 157 passed, coverage 87%
  - Ruff: No issues found
  - MyPy: No type errors
  - Bandit: No security issues
  - Radon: Max complexity 8/10
  - Interrogate: Docstring coverage 85%

Ready to commit.
```

### Standard Quality Workflow

```markdown
# 1. Make changes
"Add type hints to all functions in @src/core/utils.py"

# 2. Validate
"Run the quality gates and report results"

# 3. Fix if needed
"Fix the MyPy errors found in the quality check"

# 4. Confirm
"Re-run quality gates and confirm all pass"
```

#### When Quality Gates Fail

Claude should:
1. **Read the error output carefully**
2. **Fix the specific issues identified**
3. **Re-run the quality gates**
4. **Confirm all checks pass**

**Don't accept**: "I've made the changes, the tests should pass now."

**Require**: "I've made the changes and verified all quality gates pass."

### Custom Quality Focus Areas

While the master script covers everything, you can request focused checks:

```markdown
# Security focus
"Review @src/infrastructure/database.py for security issues.
Run Bandit specifically and fix any medium/high severity findings."

# Complexity focus
"Refactor @src/services/report_generator.py to reduce complexity.
All functions must have cyclomatic complexity ≤10.
Verify with Radon."

# Coverage focus
"Improve test coverage for @src/core/calculator.py to ≥90%.
Focus on edge cases and error conditions.
Verify with pytest --cov."
```

**Best Practice**: Use the master script for pre-commit validation, use individual tools for focused improvements during development.

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

#### Testing Best Practices

**Key Principles for Quality Tests**:

1. **Test Behavior, Not Implementation**
   - ✅ Test what the function does, not how it does it
   - ❌ Don't test internal method calls or private functions
   - ✅ Test observable outcomes and side effects

2. **One Assertion Per Test** (when possible)
   - Each test should verify one specific behavior
   - Makes failures easier to diagnose
   - Exceptions: Multiple assertions for same concept (e.g., object state)

3. **Prefer Integration Over Heavy Mocking**
   - Use real dependencies when practical
   - Mock only external services or slow operations
   - Integration tests catch more real-world issues

4. **Ensure Deterministic Tests**
   - Tests should always produce same results
   - Avoid time-dependent tests (use fixed timestamps)
   - Don't rely on external state or network

5. **Use Existing Test Utilities**
   - Leverage project's test helpers and fixtures
   - Don't recreate common setup code
   - Ask Claude to review existing test patterns first

**Example Prompt**:
```markdown
"Before writing tests for @src/parsers/starling.py:
1. Review existing test patterns in @tests/unit/test_parser_template.py
2. Use the same fixtures and utilities
3. Follow the one-assertion-per-test pattern
4. Test behavior (correct parsing output) not implementation (internal methods)
5. Ensure tests are deterministic (use fixed dates, not datetime.now())"
```

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
Confirm all checks pass before we commit."
```

**After this phase, Claude must run the pre-commit checklist** (quality gates script).

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

### Deleting Files

**IMPORTANT**: Distinguish between source code and ephemeral data.

#### Safe Deletion Protocol for Source Code (`src/` and `tests/`)

```markdown
"Before deleting @src/adapters/old_parser.py:
1. Verify Dependencies: Check for all imports referencing this file
   (grep -r 'from old_parser' . or 'import old_parser')
2. Verify Tests: Confirm no tests reference this file
3. Check Git History: Confirm it's marked as deprecated
4. If safe: Use 'git rm src/adapters/old_parser.py' to stage deletion
5. Run all tests to verify nothing breaks
6. Run quality gates to confirm project still valid"
```

**Why `git rm`?**
- Source code is tracked by version control
- Git history preserves the code if needed
- No need to manually archive - Git IS the archive

#### Deletion Protocol for Ephemeral Data (`artifacts/`)

```markdown
"For temporary/generated files in artifacts/:
1. Verify it's truly ephemeral (not a migration script or important log)
2. Move to artifacts/.archive/ with date prefix if uncertain
   Example: mv artifacts/temp/debug_script.py artifacts/.archive/2025-10-26_debug_script.py
3. No git tracking needed - these are operational files"
```

**Key Distinction**:
- **Source code** (`src/`, `tests/`) → Use `git rm`, rely on Git history
- **Ephemeral data** (`artifacts/temp/`, `artifacts/output/`) → Delete or archive manually

**Best Practice**: Claude should verify no dependencies before deletion. Never delete without verification.

### Moving Files

```markdown
"Move @src/utils/file_ops.py to @src/infrastructure/file_system.py.
Update all imports across the project.
Run tests to verify nothing breaks.
Run quality gates to confirm."
```

**Best Practice**: Include import updates, test verification, and quality gate check.

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

### Task Agent (Sub-Agents) for Deep Work

**Task agents** (also called sub-agents) allow Claude to spin up lightweight, independent instances to handle specific sub-problems. When Claude uses a Task agent, you'll see `Task()` in the output.

#### Core Benefits

1. **Context Window Management**: Each sub-agent gets its own context, preventing the main agent from being overwhelmed
2. **Parallelization**: Sub-agents run in parallel (up to ~10 agents, with queuing for more)
3. **Specialization**: Each sub-agent can focus on a specific aspect of a problem

#### When to Use Task Agents

✅ **Ideal scenarios**:
- **Complex research/exploration**: Gathering information from multiple files or directories
- **Large-scale refactoring**: Breaking down into independent chunks
- **Verification/review**: Independent agents checking implementations
- **Testing**: Comprehensive test generation and validation
- **Specialized perspectives**: Different agents with different priorities (e.g., accessibility expert, mobile expert, security expert)

❌ **Poor use cases**:
- Simple, single-file changes
- Tasks requiring sequential dependencies
- When context sharing is critical

#### How to Invoke Task Agents

**Direct instruction**:
```markdown
"Use sub-agents for these tasks..."
"Please use the Task tool to delegate suitable tasks to sub-agents"
```

**Specify parallelism** (up to ~10 agents):
```markdown
"Explore the codebase using 4 tasks in parallel. Each agent should explore different directories."
"Use the task tool to create 10 parallel tasks to analyze all parser files."
```

**Define roles/responsibilities**:
```markdown
"Refactor the authentication module. Spin up three sub-agents:
- Agent 1: Focus on user model
- Agent 2: Focus on API endpoints
- Agent 3: Focus on test suite"

"Spawn 4 sub-tasks with different priorities:
- Design/color expert
- Accessibility expert
- Mobile/responsive expert
- Overall style expert
Compare their results and synthesize the best approach."
```

**Emphasize context isolation** (critical for token efficiency):
```markdown
"Reminder: Maintain focused contexts. Use the Task tool to delegate tasks.
Each sub-agent should read ONLY the specific files needed for its task."
```

#### Best Practices for Efficient Sub-Agent Use

**1. Clear Planning (Main Agent's Role)**

Before involving sub-agents, ensure the main agent has a clear plan:
```markdown
"Create a plan for refactoring the parser module.
Think through the approach, then use sub-agents to execute."
```

Use Plan mode (`Shift+Tab`) and extended thinking (`"think hard"` or `"ultrathink"`) for complex problems.

**2. Granular Task Definition**

Break down into specific, independently-executable tasks:

❌ **BAD** (too vague):
```markdown
"Use sub-agents to fix the parsers"
```

✅ **GOOD** (specific, independent):
```markdown
"Launch 5 parallel sub-agents:
- Agent 1: Analyze @src/parsers/starling.py for type errors
- Agent 2: Analyze @src/parsers/ibkr.py for type errors
- Agent 3: Analyze @src/parsers/revolut.py for type errors
- Agent 4: Analyze @src/parsers/firstdirect.py for type errors
- Agent 5: Analyze @src/parsers/ig.py for type errors

Each agent should read ONLY its assigned file."
```

**3. Context Isolation** (Critical for Token Efficiency)

Tell sub-agents to read specific files only:

❌ **BAD** (wastes tokens):
```markdown
"Use sub-agents to analyze the parsers"
```
*Result: Each sub-agent reads all parser files unnecessarily*

✅ **GOOD** (efficient):
```markdown
"Launch sub-agent to analyze @src/parsers/starling.py ONLY.
Read this file and identify type errors. Do not read other files."
```

**4. Iterative Approach** (3-Phase Workflow)

Don't expect perfection in one pass. Use sub-agents iteratively:

**Phase 1: Identify Issues**
```markdown
"Launch 5 parallel sub-agents to identify issues in each parser file.
Report issues only, do not fix yet."
```

**Phase 2: Fix with Full Context**
```markdown
"Launch sub-agents to fix the identified issues.
Each agent should read the FULL file for context before making changes."
```

**Phase 3: Verify**
```markdown
"Use sub-agents to verify the implementations aren't overfitting to tests.
Check for edge cases and potential issues."
```

**5. Monitor and Guide**

Keep an eye on sub-agents and course-correct if needed:
```markdown
# If a sub-agent goes off track
"Stop. Agent 2 is reading unnecessary files.
Restart Agent 2 with explicit instruction to read ONLY @src/parsers/ibkr.py"
```

**6. Avoid Redundant Token Usage**

Ensure task splitting is logical and contributes to efficiency:

❌ **BAD** (redundant splitting):
```markdown
"Use 10 sub-agents to add a single docstring to one function"
```

✅ **GOOD** (logical splitting):
```markdown
"Use 10 sub-agents to add docstrings to 10 different modules in parallel"
```

#### Example: Research and Analysis

```markdown
"Launch a Task agent to:
1. Analyze all parser files in @src/parsers/
2. Identify code duplication across parsers
3. Design a base parser class to eliminate duplication
4. Estimate the refactoring effort
5. Report back with findings and recommendations

Do NOT make changes, just analyze and recommend.
Read only the parser files, not the entire codebase."
```

#### Example: Large-Scale Refactoring

```markdown
"I need to add type hints to all files in @src/.

Phase 1: Launch 10 parallel sub-agents to analyze and identify missing type hints.
Each agent takes one module. Report issues only.

Phase 2 (after review): Launch sub-agents to add type hints to each file.
Each agent reads the FULL file for context.

Phase 3: Verify all changes pass mypy --strict."
```

#### Example: Role-Based Specialization

```markdown
"Analyze the UI design in @src/components/dashboard.tsx.

Spawn 4 parallel sub-agents with different focuses:
1. Accessibility expert: WCAG compliance, ARIA labels, keyboard navigation
2. Performance expert: Render optimization, lazy loading, memoization
3. Mobile expert: Responsive design, touch targets, viewport handling
4. Design system expert: Consistency with design tokens, component patterns

Each agent provides 3-5 specific recommendations.
I'll synthesize the best recommendations from all perspectives."
```

**Key Insight**: Sub-agents are powerful for parallelizable work, but require clear orchestration and context management from the main agent (you)

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
- You have **clean working directory** you can revert with `git reset --hard`
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
bash .ai-validation/check_quality.sh

# 7. Decision point:
# Accept: git add . && git commit -m "Refactoring from Claude"
# Reject: git reset --hard HEAD
```

**Best Practice**: **DON'T USE YOLO MODE**. The approval step takes 2 seconds and prevents disasters.

**Git is the ultimate safety net** - use it properly.

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
3. If all pass, suggest a commit message"
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
1. Run quality gates (bash .ai-validation/check_quality.sh)
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

### Proven Workflow: Explore-Plan-Code-Commit

**The foundational workflow for complex, multi-file tasks.** This structured approach prevents rushed implementations and ensures quality outcomes.

#### Phase 1: Explore (Gather Context)

**Don't jump straight to coding.** Explore first to understand the full scope.

```markdown
"Before implementing the CGT calculation feature, I need you to explore:

1. Read @src/models.py and identify existing trade/transaction models
2. Read @src/parsers/ to understand how trades are currently imported
3. Search for any existing tax or calculation-related code
4. Review @tests/ to understand our testing patterns
5. Check @docs/design/ for any relevant architecture docs

Do NOT write any code yet. Report back with:
- Relevant files and their purposes
- Potential integration points
- Any existing patterns we should follow
- Potential conflicts or challenges"
```

**Benefits**:
- Prevents reinventing existing functionality
- Identifies integration points early
- Surfaces potential conflicts before coding
- Uses sub-agents efficiently for discovery

**Use sub-agents for exploration**:
```markdown
"Use 4 parallel sub-agents to explore:
- Agent 1: Search for tax-related code patterns
- Agent 2: Analyze existing calculation modules
- Agent 3: Review database schema for relevant tables
- Agent 4: Check test coverage for similar features

Each agent reads ONLY files relevant to their search."
```

#### Phase 2: Plan (Document Approach)

**Create a written plan before implementation.** This becomes your source of truth.

**Option A: Feature Specification First (Recommended for Complex Features)**

For complex features, create a specification document *before* the implementation plan:

```markdown
"Create a feature specification for the CGT calculation module.
Write it to @docs/specs/cgt-calculation-spec.md

Include:
## Overview
- Purpose and goals
- Success criteria

## Expected Behavior
- User workflow (step by step)
- Input → Process → Output flow
- Example scenarios (3-5 concrete examples)

## Edge Cases
- What happens when there are no matching acquisitions?
- How do we handle partial share disposals?
- Cross-tax-year transactions?
- Currency conversions with missing rates?

## Technical Requirements
- Performance targets (must handle 10k trades in <5s)
- Data persistence requirements
- API endpoints or interfaces needed
- Error handling strategy

## Out of Scope (for now)
- Multi-currency complex instruments
- Options and derivatives
- Real-time calculations (batch only)

Use 'ultrathink' mode to consider alternatives and edge cases."
```

**Why this works**:
- Forces comprehensive thinking before code
- Saves multiple back-and-forth prompts
- Claude has clear foundation for implementation
- Easier to review and approve before coding starts
- Documents requirements for future reference

**Option B: Implementation Plan (Standard Approach)**

For simpler features, go straight to implementation plan:

```markdown
"Based on your exploration, create a detailed implementation plan:

1. Write the plan to @docs/notes/cgt-calculation-plan.md
2. Include:
   - Files to create/modify (with specific paths)
   - New functions/classes needed (with signatures)
   - Database changes required
   - Testing strategy (unit + integration)
   - Dependencies and integration points
   - Potential risks and mitigations
   - Implementation order (which parts first)

Use 'ultrathink' mode to consider alternatives thoroughly."
```

**Validate the plan**:
```markdown
"Review your plan for:
- Alignment with existing architecture (@docs/design/architecture.md)
- Compliance with quality standards (functions ≤30 lines, complexity ≤10)
- Test coverage approach (≥80%)
- Potential edge cases and error handling

Update the plan with any improvements."
```

**Scale-aware validation** (Think 10x from day one):

```markdown
"Before finalizing the plan, validate it against 10x scale:

Current state: 100 users, 1,000 transactions/day
Think ahead: 1,000 users, 10,000 transactions/day

Questions to ask:
1. **Database queries**: Will this query work with 100,000 records?
   - Do we need indexes from day one?
   - Are we doing N+1 queries that will slow down at scale?

2. **File operations**: How do we handle 10x the file uploads?
   - File size limits appropriate?
   - Storage strategy scales?

3. **Background jobs**: Can we process 10x the queue depth?
   - Job processing time reasonable?
   - Queue won't back up?

4. **API response times**: Will this endpoint stay under 200ms at 10x load?
   - Caching strategy?
   - Pagination implemented?

5. **Memory usage**: Will this fit in memory at 10x data?
   - Are we loading entire datasets unnecessarily?

If any answer is 'no', adjust the design NOW. Fixing later costs 10-100x more."
```

**Real-world insight** (from 47 failed startup audits):

Common patterns that kill startups at scale:
- 89% had zero database indexing → queries take seconds instead of milliseconds
- 91% had no automated tests → every change breaks 3 other things
- 68% had auth vulnerabilities → security nightmares at scale
- Most didn't think about scale until month 18 → required $500k-2M rebuild

**The pattern**: Month 1-6 great → Month 7-12 slowing → Month 13-18 can't add features → Month 19-24 maintaining mess → Month 25+ rebuild or die

**Prevention**: Ask "what breaks at 10x?" during planning, not after it's too late.

**Example prompt**:
```markdown
"Review the transaction import plan (@docs/notes/import-plan.md) for scale:

Current: 50 transactions/day
Target: 500 transactions/day (realistic in 6 months)

Check:
1. Are we loading all transactions into memory? (Won't scale)
2. Do we have indexes on transaction_date and institution? (Need them)
3. Is file processing synchronous? (Will block at 500/day)
4. Are we validating efficiently? (Batch validation vs per-record)

Suggest changes to handle 10x from day one."
```

**When to do this**:
- ✅ Every new feature (during planning phase)
- ✅ Database schema changes (indexes from start)
- ✅ API endpoint design (pagination, caching considered)
- ✅ File handling logic (storage strategy that scales)
- ❌ Micro-optimizations (premature optimization is still bad)

**Benefits**:
- Forces thorough thinking before coding
- Creates documentation for future reference
- Enables plan review before implementation
- Provides context for resuming work later
- **Prevents costly rebuilds months later**

#### Phase 3: Code (Incremental Implementation)

**Implement in small, testable increments.** Follow TDD strictly.

```markdown
"Following @docs/notes/cgt-calculation-plan.md:

Step 1: Implement ONLY the trade matching logic (same-day rule)
- Write tests first in @tests/unit/test_cgt_matching.py
- Implement to pass tests in @src/cgt/matcher.py
- Run quality gates
- Commit when passing

Stop after Step 1. I'll review before continuing."
```

**Maintain focus on the plan**:
```markdown
"I see you're implementing additional features beyond the plan.
STOP. Stick to the documented plan in @docs/notes/cgt-calculation-plan.md.

If you think the plan needs changes, update the plan document FIRST,
then wait for my approval before implementing."
```

**Benefits**:
- Prevents scope creep
- Enables checkpoint reviews
- Maintains quality standards throughout
- Allows course correction early

#### Phase 4: Commit (Quality Validation)

**Validate before committing.** Every commit should be production-ready.

```markdown
"We've completed the same-day matching implementation.
Before committing:

1. Run ALL quality gates (bash .ai-validation/check_quality.sh)
2. Verify test coverage ≥80% for new code
3. Check the plan - did we complete this step fully?
4. Update the plan document with completion status
5. Update @artifacts/logs/completed-actions.log
6. Generate a commit message following our format
7. Show me a summary of changes before committing"
```

**Commit message generation**:
```markdown
"Generate a commit message:

Format:
feat: [brief description]

- Detailed change 1
- Detailed change 2

Refs: @docs/notes/cgt-calculation-plan.md
Tests: Added comprehensive tests with 85% coverage

Include:
- What was implemented (from the plan)
- Which tests were added
- Any deviations from original plan and why"
```

**Benefits**:
- Ensures quality gates pass consistently
- Creates clear commit history
- Links commits to plans for traceability
- Documentation stays current

#### Living Documentation Principle

**Treat plans as living documents**, not static artifacts.

```markdown
"Update @docs/notes/cgt-calculation-plan.md:

- Mark completed steps with ✅
- Add 'Implementation Notes' section documenting:
  - Unexpected challenges encountered
  - Solutions different from original plan
  - New insights about the codebase
  - Recommendations for future work

This helps when we resume work later or other developers read the plan."
```

**Benefits**:
- Plans evolve with understanding
- Captures tribal knowledge
- Eases resumption after breaks
- Valuable for code reviews

#### Example: Complete Workflow

```markdown
# Session 1: Explore
"Explore the codebase for implementing CSV export feature.
Use 3 parallel agents to search for existing export patterns,
file generation utilities, and similar features."

# Session 2: Plan
"Create implementation plan at @docs/notes/csv-export-plan.md.
Think through the architecture, testing strategy, and integration points.
Use 'ultrathink' to consider alternatives."

# Session 3: Review Plan (Human)
[Human reviews plan, suggests changes, approves]

# Session 4: Implement Step 1
"Following the plan, implement ONLY the CSV formatter class.
Write tests first, implement to pass, run quality gates.
Commit when green. Stop after this step."

# Session 5: Implement Step 2
"Implement the export service layer.
Follow the same TDD cycle. Update the plan with any insights."

# Session 6: Implement Step 3
"Add CLI command for CSV export.
Integration test with real data.
Update all documentation."

# Session 7: Final Validation
"Run full quality gates, update plan to mark complete,
update completed-actions.log, commit final changes."
```

**Key Insight**: This workflow prevents the common mistake of "just start coding" which leads to rushed implementations, missed edge cases, and technical debt. The small time investment in exploration and planning pays dividends in quality and maintainability.

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
[Make major architectural changes without updating docs/]
```

✅ **Do this instead**:
```markdown
"We just added a new authentication module.
Update:
1. docs/design/architecture.md (auth architecture)
2. docs/design/decisions/003-auth-choice.md (why this approach)
3. docs/notes/plan.md (mark auth task complete)

Note: CLAUDE.md stays unchanged unless this affects project structure."
```

**Lesson**: Keep documentation current, but distinguish between architectural docs and CLAUDE.md (stable constitution).

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

### Mistake 8: Persisting When Stuck (The 2-3 Prompt Rule)

❌ **Don't do this**:
```markdown
# Prompt 1: "Add authentication to the API"
# Prompt 2: "No, I meant JWT-based authentication"
# Prompt 3: "That's still not right, use refresh tokens"
# Prompt 4: "Try again with better error handling"
# Prompt 5: "This isn't working, start over"
# [Continues failing...]
```

✅ **Do this instead**:
```markdown
# Prompt 1: "Add JWT authentication to the API"
# Prompt 2: "Include refresh token rotation"
# Prompt 3: "Add error handling for expired tokens"

# If you're not 80% of the way there after 2-3 prompts:
# STOP. Start a new conversation with better context.

"I'm resetting this conversation. Let me provide better context:
@docs/design/architecture.md - our API structure
@src/auth/ - existing auth utilities
@tests/integration/test_auth.py - what we expect

Now implement JWT authentication with refresh tokens following our patterns."
```

**Lesson**: Claude can get "stuck" on a bad approach. If 2-3 prompts don't get you 80% there, reset with fresh context. Don't waste time on a dead-end thread.

**When to reset**:
- ✅ Claude keeps making the same mistake
- ✅ Solutions get progressively worse
- ✅ You're spending more time correcting than making progress
- ✅ The conversation has become confusing or contradictory

**How to reset effectively**:
1. Use `/clear` to start fresh in same session
2. Provide better context (reference relevant files)
3. Be more specific about requirements
4. Consider using Plan mode first
5. Try extended thinking (`"ultrathink"`) for complex problems

### Mistake 9: Letting Files Grow Too Large

❌ **Don't do this**:
```markdown
# After weeks of development
@src/services/processor.py - 3,247 lines
# Claude keeps appending code, file becomes unmanageable
```

✅ **Do this instead**:
```markdown
# Regular refactoring (every few days or when files hit 300-500 lines)
"The @src/services/processor.py file is now 523 lines.
Let's refactor it:

1. Identify logical sections (parsing, validation, processing, output)
2. Extract to separate modules:
   - @src/services/parser.py
   - @src/services/validator.py
   - @src/services/processor_core.py
   - @src/services/output.py
3. Update imports in all dependent files
4. Ensure all tests still pass
5. Run quality gates"
```

**Lesson**: AI tends to append code rather than refactor. Set triggers for manual refactoring.

**Refactoring triggers**:
- ⚠️ Files exceed 500 lines (target: ≤300)
- ⚠️ Functions exceed 30 lines (hard limit)
- ⚠️ Multiple unrelated responsibilities in one file
- ⚠️ Heavy duplication across files
- ⚠️ Cyclomatic complexity >10

**Benefits of smaller files**:
- ✅ Easier for AI to work with (smaller context)
- ✅ Saves tokens
- ✅ Faster development
- ✅ Clearer structure
- ✅ Better testability

### Mistake 10: Not Managing Mental Load

❌ **Don't do this**:
```markdown
# Hour 1: Build authentication module
# Hour 2: Add payment integration
# Hour 3: Implement notifications
# Hour 4: Debug edge cases
# Hour 5: Refactor entire codebase
# [Feeling overwhelmed, making mistakes, losing track]
```

✅ **Do this instead**:
```markdown
# Working with AI is mentally exhausting
# 2 hours of AI-assisted coding = feels like a full week of traditional work

# Set time limits:
- Work in 90-minute focused blocks
- Take 15-minute breaks between blocks
- Stop after 2-3 hours of intense AI work
- Resume the next day with fresh perspective

# Use planning documents to resume:
"Read @docs/notes/plan.md and @artifacts/logs/completed-actions.log
Tell me what we were working on and what's next."
```

**Lesson**: AI enables incredibly fast development, but it's mentally draining. Pace yourself.

**Signs you need a break**:
- ⚠️ Making careless mistakes
- ⚠️ Accepting Claude's suggestions without reviewing
- ⚠️ Losing track of what you're building
- ⚠️ Feeling overwhelmed by the pace
- ⚠️ Struggling to understand your own code

**Recovery strategies**:
- ✅ Step away for a few hours or until next day
- ✅ Review code with fresh eyes before committing
- ✅ Update documentation to capture your thinking
- ✅ Use quality gates as checkpoints
- ✅ Work in shorter sessions (90 minutes max)

### Mistake 11: Forgetting to Add Comments for AI

❌ **Don't do this**:
```python
def process(data):
    x = transform(data)
    y = validate(x)
    z = optimize(y)
    return finalize(z)
```

✅ **Do this instead**:
```python
def process(data):
    """Process transaction data through our pipeline.

    This is the main entry point for transaction processing.
    We transform, validate, optimize, and finalize in sequence.
    Each step can fail independently - see error handling in each function.
    """
    # Step 1: Transform raw data to our internal format
    # Uses the standardized transaction schema from src/models.py
    x = transform(data)

    # Step 2: Validate against business rules
    # Includes duplicate detection and amount verification
    y = validate(x)

    # Step 3: Optimize for database insertion
    # Batches operations and minimizes queries
    z = optimize(y)

    # Step 4: Write to database with transaction safety
    return finalize(z)
```

**Lesson**: Comments help AI understand your code when you return days later. They also help *you* remember why you made certain decisions.

**What to comment**:
- ✅ **Why** decisions were made (not obvious from code)
- ✅ **Business logic** that might be unclear
- ✅ **Gotchas** and edge cases
- ✅ **References** to other parts of the codebase
- ✅ **Future considerations** or TODOs

**Strategic commenting for AI**:
```markdown
"Add detailed comments to @src/cgt/matcher.py explaining:
1. The HMRC same-day matching rule and why we check dates first
2. The 30-day rule and how we handle it
3. Why Section 104 pooling comes last
4. Edge cases we handle (partial matches, multiple disposals)

Comments should help an AI assistant working on this code later."
```

**Benefits**:
- ✅ AI resumes work more accurately
- ✅ You remember your own decisions
- ✅ Reduces need to re-read entire files
- ✅ Makes code review easier
- ✅ Captures tribal knowledge

---

## Integration with Project Standards

### Aligning with CLAUDE.md

Your `CLAUDE.md` file is the project's **stable constitution**. Remind Claude of these frequently:

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

Reference your master quality gate script:

```markdown
"Our quality gates are defined in the script:
bash .ai-validation/check_quality.sh

Run this script after every change and fix any failures.
This validates all our standards: tests, linting, types, security, complexity, documentation."
```

### Aligning with TDD Workflow

Enforce the cycle:

```markdown
"Follow our TDD workflow:
1. Write test in tests/
2. Implement code in src/
3. Refactor to meet standards
4. Run quality gates (bash .ai-validation/check_quality.sh)
5. Log to artifacts/logs/completed-actions.log"
```

---

## Advanced Configuration (Power Users)

> **Source**: Insights from 3+ years of daily heavy LLM usage
> **Level**: Intermediate to Advanced
> **Optional**: These optimizations provide substantial improvements but require additional setup

### The Philosophy: Innovation Over "Vibe Coding"

**Critical Insight from Experience**:

> "Vibe coding" only takes you so far. Put in the effort to enhance the model with the right context, persistent memory, well-crafted prompt workflows, and you'll be amazed. Don't be lazy, be innovative.

**Reality Check**:
- Initial AI feels like you can build anything
- Quickly discover it doesn't work like that
- There's a plateau with minimal gains
- Innovation and human mind are what push through the plateau

**The Difference**:
- ❌ **Vibe coding**: "Make this work" → plateaus quickly
- ✅ **Engineered workflows**: Context + memory + structure → continuous improvement

### Extended Thinking Mode

Enable Claude's extended thinking capabilities for complex problems.

#### Configuration

Add to your `.vscode/settings.json` (or user settings):

```json
{
  "env": {
    "ANTHROPIC_CUSTOM_HEADERS": "anthropic-beta: interleaved-thinking-2025-05-14",
    "MAX_THINKING_TOKENS": "30000"
  }
}
```

**What this does**:
- Activates additional thinking triggers between thoughts
- Allows up to 30,000 tokens for internal reasoning
- Substantially improves complex problem-solving
- Minimal cost impact (thinking tokens are cheaper)

**When to use**:
- ✅ Complex architectural decisions
- ✅ Multi-step refactoring planning
- ✅ Debugging intricate issues
- ✅ Algorithm optimization
- ❌ Simple CRUD operations (overkill)

**Best Practice**: Enable globally, Claude only uses extra thinking when needed.

### Large Codebase Strategies

For projects >1GB or with complex architectures, standard referencing isn't enough.

#### Problem: Context Limitations

```markdown
# Symptom
Claude recreates functions that already exist
Can't find relevant code across large codebase
Misses important dependencies
```

**Why this happens**:
- Claude's context window is large but finite
- Can't hold entire 2.5GB codebase in memory
- File referencing only works if you know which files to reference

#### Solution 1: Codebase Mapping (Recommended)

**Create a knowledge graph of your codebase** for Claude to query.

**High-Level Workflow**:

```markdown
"Map this entire codebase and create a searchable index.

Phase 1 (Analysis): Identify all major sections/modules of the codebase
  - List top-level directories and their purposes
  - Identify core vs supporting code
  - Note external dependencies and APIs

Phase 2 (Indexing): For each section, extract and index:
  - All public functions/classes and their signatures
  - Key data structures and types
  - Important patterns and conventions
  - Cross-module dependencies

Phase 3 (Verification): Check for gaps
  - Verify all entry points are mapped
  - Ensure key utilities are indexed
  - Validate cross-references

CRITICAL: Execute Phase 2 in PARALLEL using task invocation.
Launch one agent per section. DO NOT execute sequentially."
```

**Follow-up usage**:
```markdown
"Before implementing the new authentication module:
1. Search the codebase index for existing auth-related functions
2. Identify which can be reused vs what needs to be created
3. Propose implementation using existing code where possible"
```

**Tools for this**:
- **Graphiti MCP** (advanced): Knowledge graph with Neo4j backend
- **basic-memory MCP** (simpler): Note-based memory system
- **Sequential thinking MCP**: Enhanced reasoning during mapping

#### Solution 2: Repomix + Indexing

For smaller projects (<100MB):

```bash
# Install repomix
npm install -g repomix

# Generate single-file representation
repomix --output codebase-summary.txt

# Reference in Claude
"Review @codebase-summary.txt before implementing..."
```

**Limitations**: Only practical for small-medium codebases

### Parallel Execution Enforcement

**Critical lesson from experience**:

> When you ask for parallel execution, DEMAND it. If Claude doesn't execute in parallel, STOP and say "I SAID LAUNCH IN PARALLEL" with severity and disappointment noted.

**Why this matters**:
- Serial execution of independent tasks wastes time
- Claude can and will execute tasks in parallel if properly instructed
- You must be EXPLICIT and enforce it

**Bad (Sequential)**:
```markdown
"Analyze all parser files and identify duplication"
# Claude processes one at a time → slow
```

**Good (Parallel)**:
```markdown
"Analyze all parser files and identify duplication.

CRITICAL: Use task invocation to launch parallel agents.
One agent per parser file.
They must work simultaneously, NOT sequentially.

If you cannot execute in parallel, STOP and explain why."
```

**Verification**:
```markdown
# After Claude responds
"Confirm: Did you execute those tasks in parallel or sequentially?
If sequentially, we're starting over and doing it RIGHT this time."
```

**Best Practice**: Be assertive about parallel execution. It's a capability Claude has but won't always use without explicit direction.

### MCP Servers for Enhanced Capabilities

**What are MCPs**: Model Context Protocol servers that extend Claude's capabilities.

#### Recommended MCPs

**1. Sequential Thinking (Enhanced Reasoning)**

GitHub: https://github.com/arben-adm/mcp-sequential-thinking

**What it does**: Substantially upgraded sequential thinking beyond standard version

**Use case**:
```markdown
"Use sequential thinking to break down this complex CGT calculation algorithm:
1. Identify all edge cases
2. Map out the calculation flow
3. Identify potential optimization points
4. Propose implementation approach"
```

**2. Persistent Memory for Cross-Session Context**

Choose based on your project complexity and existing infrastructure:

**basic-memory** (Simple/Beginner): https://github.com/basicmachines-co/basic-memory
- Note-based memory system
- Lightweight, minimal setup
- No database required
- ✅ **Best for**: Starting out, small projects, simple note-taking

**mcp-ai-memory** (Intermediate/PostgreSQL users): https://github.com/scanadi/mcp-ai-memory
- **Semantic memory** with vector similarity search
- PostgreSQL + pgvector (including Neon cloud support)
- **DBSCAN clustering** for automatic memory consolidation
- **Local embeddings** - No API keys needed (privacy-friendly, zero cost)
- Redis caching + background workers for performance
- Smart compression for large memories
- ✅ **Best for**: Projects already using PostgreSQL, need semantic search, production deployments

**Install**:
```bash
npm install mcp-ai-memory
```

**Graphiti** (Advanced/Complex projects): https://github.com/getzep/graphiti
- **Temporal knowledge graph** with relationships
- Neo4j backend (requires separate Neo4j installation)
- Most sophisticated memory management
- ✅ **Best for**: Complex, evolving projects needing relationship tracking

**Comparison**:

| Feature | basic-memory | mcp-ai-memory | Graphiti |
|---------|--------------|---------------|----------|
| **Setup** | Minimal | Moderate (PostgreSQL) | Complex (Neo4j) |
| **Search** | Keyword | Semantic (vector) | Graph + Temporal |
| **Clustering** | No | Yes (DBSCAN) | Yes (advanced) |
| **Database** | None | PostgreSQL | Neo4j |
| **API Keys** | No | No (local embeddings) | No |
| **Production-ready** | Basic | Yes | Yes |
| **Best for** | Learning | PostgreSQL projects | Complex relationships |

**Use case (mcp-ai-memory)**:
```markdown
# Store architectural decision (automatically embedded)
"Store in memory: We decided to use PostgreSQL over MongoDB because
our data is highly relational and we need ACID compliance.
Performance benchmarks showed 3x faster joins for our query patterns."

# Retrieve later (different session, semantic search)
"Why did we choose PostgreSQL?"
# Claude searches semantically, finds related memories:
# - Database decision (exact match)
# - Performance considerations (related concept)
# - Query pattern analysis (related context)
# Returns consolidated answer from all related memories

# Track preference over time
"Store in memory: User prefers type-safe approaches. Always use TypeScript
over JavaScript, Pydantic over plain dicts in Python."

# Later in different session
"Should I use JavaScript or TypeScript for this new module?"
# Claude queries memory, finds preference, recommends TypeScript
```

**Use case (building knowledge graph)**:
```markdown
# Store related decisions with context
"Store in memory: Authentication flow uses JWT tokens (stored in memory March 2024).
Related to: API security architecture, user session management.
Rationale: Stateless scaling, easier load balancing."

# Build relationships over time
"Store in memory: Switched to refresh tokens (April 2024) to improve security.
Supersedes: JWT-only approach from March 2024."

# Query across timeline
"How has our authentication approach evolved?"
# Claude retrieves chronological sequence:
# 1. JWT tokens (March 2024) - initial approach
# 2. Refresh tokens added (April 2024) - security improvement
# Shows decision progression and rationale
```

**Recommendation**:
- Start with **basic-memory** to learn the concept
- Upgrade to **mcp-ai-memory** when you need semantic search or already use PostgreSQL
- Use **Graphiti** only for complex projects requiring sophisticated relationship tracking

**3. Web Search MCPs**

**Exa Search**: https://github.com/exa-labs/exa-mcp-server
- Better for most searches
- Semantic understanding

**Firecrawl**: https://github.com/mendableai/firecrawl-mcp-server
- Better for real-time data
- Current events

**Use case**:
```markdown
"Search for best practices for PostgreSQL connection pooling in Python.
Focus on production-ready solutions with error handling."
```

### Setting Up MCPs

1. **Install the MCP server** (follow each server's docs)
2. **Configure in Claude Code** settings
3. **Test the integration**:
   ```markdown
   "List available MCP tools and confirm they're working"
   ```

**Best Practice**: Start with one MCP, verify it works, then add more. Don't install everything at once.

### ⚠️ Warning: Avoid Tool Bloat

**Real-world experience** (developer testing 100+ Claude Code tools):

> "My setup got bloated. Had 15 plugins, 8 MCP servers, 30 slash commands running simultaneously. Claude started acting weird - slower responses, sometimes confused about what tools it had access to."

**What happened:**
- Started collecting every tool mentioned on Reddit/Discord
- Installed plugins, MCPs, hooks without testing
- Setup became unmanageable
- Claude's performance degraded (slower, confused)

**Solution:**
- Uninstalled everything
- Tested tools methodically
- **Kept only 8 tools for daily use** (out of 100+ tested)

**The minimal effective setup:**
1. awesome-claude-code (reference, not installed)
2. GitHub MCP Server (essential)
3. Playwright MCP (testing)
4. One persistent memory MCP (mcp-ai-memory or basic-memory)
5. Sequential Thinking MCP (complex problems)
6. One status line (optional, cosmetic)
7. 3-5 custom slash commands (project-specific)
8. 1-2 hooks (TDD guard, quality checks)

**Lessons learned:**

✅ **DO**:
- Install tools one at a time
- Test for 3-5 days before adding another
- Remove tools you don't use weekly
- Keep it minimal and focused
- Prioritize quality over quantity

❌ **DON'T**:
- Install "awesome lists" of 100+ tools
- Add every tool mentioned online
- Keep tools "just in case"
- Run multiple orchestrators simultaneously
- Install unverified marketplace plugins

**How to evaluate new tools:**

```markdown
# Before installing ANY tool, ask:
1. What specific problem does this solve?
2. Can I solve it without adding a tool? (often yes)
3. Does it integrate well with existing setup?
4. Is it actively maintained? (check GitHub commits)
5. Can I test it in isolation first?

# After installing:
1. Use it for 3-5 days
2. Does it actually improve workflow?
3. Any conflicts or slowdowns?
4. Would I miss it if removed?

If you answered "no" to #2 or #4, uninstall it.
```

**Quality over quantity:** 3 well-chosen, tested tools > 30 untested tools causing conflicts

**Tool discovery resources** (reference only, don't install everything):
- https://github.com/hesreallyhim/awesome-claude-code (comprehensive catalog)
- https://github.com/wong2/awesome-mcp-servers (MCP directory)
- https://mcpmarket.com (MCP marketplace)

**Use these for research**, not as shopping lists. Our recommended tools in this document are already curated for quality-first development.

### Hooks for Automation

**What are hooks**: Scripts that run automatically on certain Claude Code events

Example: Auto-store thinking patterns in knowledge graph

```bash
# .claude/hooks/on-thought.sh
#!/bin/bash
# Triggered when Claude generates thinking blocks
# Automatically stores formatted thoughts in Graphiti

# Parse thinking block
# Format with metadata
# Send to knowledge graph
# Log for verification
```

**Common use cases**:
- Auto-save important decisions to knowledge base
- Trigger background validation
- Update project documentation automatically
- Log complex interactions for later review

**Documentation**: https://docs.anthropic.com/en/docs/claude-code/hooks

**Best Practice**: Start simple. Add complexity as you understand the system.

### Orchestrator Pattern

For complex multi-step tasks, use an "orchestrator agent" approach:

**Step 1: Plan with Claude (Orchestrator)**
```markdown
"Before we implement the new authentication system:

1. Break down into phases
2. Identify all components needed
3. Determine which can be done in parallel
4. Estimate complexity for each phase
5. Create detailed execution plan

DO NOT implement yet. Just plan."
```

**Step 2: Review and Approve Plan**
```markdown
# You review the plan
# Adjust as needed
# Give explicit approval
```

**Step 3: Execute with Verification**
```markdown
"Execute the plan we created.

For each phase:
1. Confirm you're following the plan
2. Execute (in parallel where possible)
3. Verify results before moving to next phase
4. Report progress

STOP if anything deviates from the plan."
```

**Why this works**:
- Separates planning from execution
- Gives you control points
- Prevents Claude from going off-track
- Enables parallel execution within phases

### The Innovation Mindset

**From 3+ years of experience**:

1. **Claude's capabilities are declining** (recent weeks)
   - Still far from "useless"
   - Work with what you have
   - Innovate around limitations

2. **Model enhancements matter more than model quality**
   - Right context > slightly better model
   - Persistent memory > larger context window
   - Well-crafted workflows > raw intelligence

3. **Put in the effort**
   - Setup takes time (elbow grease required)
   - Payoff is substantial
   - Compound improvements over time

4. **Don't rely on "vibe"**
   - Structure your interactions
   - Engineer your prompts
   - Build systems, not scripts

**Best Practice**: Treat Claude as a powerful tool that requires proper configuration, not magic that "just works."

### Advanced Workflows

#### Multi-Repository Development with Git Worktrees

**Problem**: Working on multiple features in parallel within the same repository.

**Traditional approach**: Constant branch switching (`git checkout`), stashing changes, context loss.

**Better approach**: Git Worktrees + Multiple Claude Sessions

**Setup**:
```bash
# In your main repository
git worktree add ../myproject-feature-a feature-a
git worktree add ../myproject-feature-b feature-b
git worktree add ../myproject-bugfix-123 bugfix-123

# Each worktree is a separate directory with independent working tree
# But shares the same git history
```

**Usage**:
```bash
# Terminal 1: Work on feature-a
cd ../myproject-feature-a
claude code

# Terminal 2: Work on feature-b (simultaneously)
cd ../myproject-feature-b
claude code

# Terminal 3: Handle urgent bugfix
cd ../myproject-bugfix-123
claude code
```

**Benefits**:
- ✅ Independent file changes (no conflicts)
- ✅ Separate Claude sessions with focused context
- ✅ Shared git history (easy merging)
- ✅ No branch switching overhead
- ✅ Visual separation (can use different VS Code profiles/themes)

**VS Code Profiles** (optional enhancement):
```bash
# Create profiles for different work types
code --profile "Feature Development" ../myproject-feature-a
code --profile "Bug Fixes" ../myproject-bugfix-123

# Different themes, extensions, settings per profile
# Visual differentiation reduces context switching errors
```

**Best Practice**: Use worktrees for parallel development streams. Single repo with branch switching for sequential work.

**Cleanup**:
```bash
# When done with feature-a
cd ../myproject-feature-a
# Merge or close PR
cd ..
git worktree remove myproject-feature-a
```

#### Visual Iteration Workflow (UI/UX Development)

**For projects with visual components**: Iterative development driven by screenshots and mockups.

**Setup**:

1. **Screenshot Capability**:
   - **Puppeteer MCP**: Automated browser screenshots
   - **iOS/Android Simulators**: Mobile app screenshots
   - **Manual**: Screenshot tool + paste into Claude

2. **Design Mockups**: Figma exports, design specs, reference screenshots

**Workflow**:

**Step 1: Provide Visual Reference**
```markdown
"I'm attaching a screenshot of the target design for the dashboard.
Implement this design in @src/components/Dashboard.tsx.

Key requirements from the mockup:
- Card layout with 3 columns
- Gradient header background (#1a73e8 to #0d47a1)
- Rounded corners (8px border-radius)
- Shadow on hover (elevation change)

Match the visual design exactly."
```

**Step 2: Implement Initial Version**
```markdown
"Implement the dashboard component.
When done, provide instructions for taking a screenshot so we can compare."
```

**Step 3: Screenshot and Compare**
```markdown
# Option A: Using Puppeteer MCP
"Take a screenshot of the dashboard at http://localhost:3000/dashboard
Save as @artifacts/screenshots/dashboard-v1.png"

# Option B: Manual
"I've taken a screenshot (see attached).
Compare it to the original design mockup.
List all visual differences."
```

**Step 4: Iterative Refinement**
```markdown
"Differences identified:
1. Spacing between cards is 8px, should be 16px
2. Font weight is 400, should be 500
3. Shadow is too subtle

Make these adjustments and confirm they match the design."
```

**Step 5: Final Validation**
```markdown
"Take final screenshot.
Compare to original mockup.
Confirm visual parity or document remaining intentional differences."
```

**Benefits**:
- ✅ Objective visual comparison (not just "looks good")
- ✅ Catches subtle spacing/color/font differences
- ✅ Faster iteration than manual testing
- ✅ Documentation of visual decisions

**Best Practice**: Start with high-level layout, then refine details. Use screenshots at each iteration for comparison.

#### Headless Automation for CI/CD

**Use Case**: Running Claude Code non-interactively for automated workflows.

**Basic Usage**:
```bash
# Headless mode with prompt
claude -p "Run quality gates and report results" > qa-report.txt

# Exit code indicates success/failure
if [ $? -eq 0 ]; then
  echo "Quality gates passed"
else
  echo "Quality gates failed"
  exit 1
fi
```

**Advanced Use Cases**:

**1. Automated Issue Triage**
```bash
#!/bin/bash
# .github/workflows/triage-issues.sh

# Get new issue
ISSUE_BODY=$(gh issue view $ISSUE_NUMBER --json body -q .body)

# Ask Claude to triage
claude -p "Analyze this GitHub issue and suggest labels:

$ISSUE_BODY

Return only the labels as comma-separated values." > labels.txt

# Apply labels
gh issue edit $ISSUE_NUMBER --add-label $(cat labels.txt)
```

**2. Automated Code Review**
```bash
#!/bin/bash
# .github/workflows/ai-review.sh

# Get PR diff
DIFF=$(gh pr diff $PR_NUMBER)

# Ask Claude to review
claude -p "Review this code diff for:
- Security vulnerabilities
- Performance issues
- Code quality problems
- Missing tests

$DIFF

Return findings in markdown format." > review-comments.md

# Post as PR comment
gh pr comment $PR_NUMBER --body-file review-comments.md
```

**3. Large-Scale Refactoring (Fan-Out Pattern)**
```bash
#!/bin/bash
# Migrate 100 files from old pattern to new

# Generate task list
claude -p "List all files in @src/ that use the old authentication pattern" > files.txt

# Process in parallel (fan-out)
cat files.txt | xargs -P 10 -I {} bash -c '
  claude -p "Migrate {} from old auth pattern to new pattern per @docs/migration-guide.md" > logs/{}.log
'

# Verify results
claude -p "Review all migration logs in @logs/ and report any failures" > migration-report.md
```

**4. Dependency Update Validation**
```bash
#!/bin/bash
# .github/workflows/validate-deps.sh

# Update dependencies
npm update

# Run tests
npm test > test-results.txt

# Ask Claude to analyze failures
if [ $? -ne 0 ]; then
  claude -p "Analyze these test failures after dependency update:

  $(cat test-results.txt)

  Determine:
  - Which dependency caused the issue
  - Whether it's a breaking change
  - Suggested fix

  Return as JSON." > analysis.json

  # Post to Slack/PR/Issue based on analysis
fi
```

**Benefits**:
- ✅ Consistent automated workflows
- ✅ Scales to handle bulk operations
- ✅ Integrates with existing CI/CD pipelines
- ✅ Reduces manual review burden
- ✅ Enables "offline" processing

**Limitations**:
- ⚠️ No interactive clarification
- ⚠️ Must have clear, unambiguous prompts
- ⚠️ Error handling must be robust
- ⚠️ Results should be reviewed (don't auto-commit)

**Best Practice**: Start with non-critical automations (triage, labeling). Graduate to code changes only after validation. Always include human review for production changes.

**Configuration**:
```json
// .claude/settings.json
{
  "headless": {
    "timeout": 300000,  // 5 minutes max
    "retries": 3,
    "logLevel": "info",
    "allowedCommands": ["read", "grep", "bash:pytest"]  // Restrict capabilities
  }
}
```

---

## Conclusion

**Claude Code is a powerful assistant, but YOU are the architect.**

### Golden Rules

1. **Context is King**: Keep CLAUDE.md stable, update design docs frequently
2. **Reference, Don't Paste**: Use `@file` notation (most crucial takeaway)
3. **Test First**: Always write tests before implementation
4. **Verify Everything**: Run quality gates script, review diffs
5. **Git is Your Friend**: Commit often, rollback when needed
6. **Stay in Control**: Claude suggests, you decide
7. **Document Strategically**: Architectural changes in CLAUDE.md, everything else in docs/

### Success Metrics

You're using Claude Code effectively when:

✅ Quality gates pass on every commit
✅ Test coverage stays ≥80%
✅ Documentation stays current (right docs updated for right changes)
✅ You can explain every change Claude makes
✅ You catch mistakes before committing
✅ You use Git to safely experiment
✅ You feel in control, not overwhelmed

---

**Claude Code amplifies good practices and accelerates development, but cannot replace thoughtful engineering.**

**Use it wisely. Trust Git. Verify everything. Ship great software.** 🚀
