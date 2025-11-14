---
name: Planning Mode
description: Discovery-first planning for new features (Shift+Tab×2)
tags: planning, discovery, requirements, plan, new-feature
auto_load_triggers: plan, feature, new, requirements, design
priority: toolkit
---

# Planning Mode

## Purpose

Enforces discovery-first approach for new features using Planning Mode (Shift+Tab×2) to prevent premature coding and ensure clear requirements before implementation.

---

## When to Use Planning Mode

**ALWAYS enter Planning Mode for**:
- New features or functionality
- Significant refactoring (>30 lines)
- Complex bug fixes requiring multiple files
- Architecture changes
- Any work where requirements aren't crystal clear

**How to Enter**:
Press **Shift+Tab twice** to enter read-only Planning Mode where Claude cannot modify files.

---

## Planning Mode Workflow

### Step 1: Requirements Discovery

**Ask clarifying questions BEFORE planning**:

```
User: "I want to add user authentication"

Claude: [In Planning Mode] "Before planning, let me ask questions:
1. What authentication method? (JWT, sessions, OAuth)
2. What user data needs to be stored?
3. Are there existing auth patterns in the codebase?
4. What security requirements must we meet?
5. What are the edge cases? (password reset, account lockout, etc.)"
```

### Step 2: Plan Creation

**Create detailed plan with**:
- Clear objectives
- Task breakdown (each ≤30 lines)
- File changes required
- Test requirements
- Acceptance criteria
- Estimated effort

```
Claude: [Creates detailed plan with]:
- Clear objectives
- Task breakdown (each ≤30 lines)
- File changes required
- Test requirements
- Acceptance criteria
- Estimated effort
```

### Step 3: Plan Review

**Get user approval**:

```
User reviews plan and either:
- Approves → Claude can begin implementation
- Requests changes → Claude refines plan
- Rejects → Return to requirements
```

### Step 4: Implementation

**Only after explicit approval** does Claude exit Planning Mode and begin coding.

---

## Why Planning Mode Works

**Physical barrier**: Claude literally cannot write code in Planning Mode
**Forces comprehensive planning**: No shortcuts to implementation
**Prevents context drift**: Clear plan = clear execution
**Enables autonomous work**: With approved plan, Claude can work for hours without supervision

---

## Planning Mode Rules

1. **NEVER skip Planning Mode for new features**
2. **Plans must include**:
   - Task list with checkboxes
   - Acceptance criteria
   - File changes
   - Test requirements
3. **Get explicit user approval** before exiting Planning Mode
4. **Document plan** in tasks.md or feature-plan.md for persistence

---

## Example Plan Structure

```markdown
# Feature: User Authentication

## Objective
Add JWT-based authentication to API

## Tasks
- [ ] Create User model with password hashing (≤30 lines)
- [ ] Add /login endpoint (≤30 lines)
- [ ] Add /register endpoint (≤30 lines)
- [ ] Implement JWT token generation (≤30 lines)
- [ ] Add authentication middleware (≤30 lines)
- [ ] Write tests for auth flow (≤30 lines per test file)

## File Changes
- New: models/user.py
- New: routes/auth.py
- New: middleware/auth_middleware.py
- Mod: app.py (add routes)
- New: tests/test_auth.py

## Acceptance Criteria
- [ ] Users can register with email/password
- [ ] Users can login and receive JWT token
- [ ] Protected routes require valid JWT
- [ ] Passwords are hashed (bcrypt)
- [ ] Tests cover happy path and error cases
- [ ] Test coverage ≥80%

## Estimated Effort
6 tasks × 15 min = 90 minutes
```

---

## Integration with Workflows

**Use with slash commands**:
- `/plan [feature]` - Enter Planning Mode and create plan
- `/spec [feature]` - Create minimal specification first
- `/tdd [task]` - Execute task with test-driven development

**Workflow**:
```
1. /spec - Define minimal scope
2. /plan - Create implementation plan
3. User approves plan
4. /tdd - Implement each task
5. Quality gate before completion
```

---

## Anti-Patterns

**DON'T**:
- ❌ Skip Planning Mode for "small" features (they grow)
- ❌ Start coding before plan approval
- ❌ Create vague tasks (must be ≤30 lines, testable)
- ❌ Ignore clarifying questions
- ❌ Plan without understanding existing codebase

**DO**:
- ✅ Ask questions first
- ✅ Break large tasks into small pieces
- ✅ Get explicit approval
- ✅ Document plan for persistence
- ✅ Update plan as you learn

---

## Resources

- **CLAUDE.md**: Full Planning Mode section
- **/plan slash command**: Automated Planning Mode entry
- **/spec slash command**: Specification creation
- **TDD workflow skill**: Implementation after planning
