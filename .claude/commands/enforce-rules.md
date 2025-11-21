---
description: Enforce Critical Constraints before starting implementation
---

# Enforce Rules: Critical Constraints Checklist

> **Purpose**: Prevent scope creep and wandering by validating all 5 Critical Constraints are defined BEFORE coding starts.

## Why This Matters

The #2 Failure Mode is **Scope Too Big (Claude Wanders)**:
- Tasks >30 lines → Claude invents features
- No file boundaries → touches unnecessary files
- No constraints → adds dependencies freely
- "While we're here..." → scope creep

**This command prevents that by forcing explicit boundaries.**

---

## Constraint Validation

Before starting ANY implementation, define these 5 Critical Constraints:

### 1️⃣ Existing Pattern to Follow

**Question**: Which existing file/pattern should be used as a template?

**Examples**:
- ✅ "Follow the structure in `.claude/commands/checkpoint.md`"
- ✅ "Use the same MVC pattern as `src/controllers/UserController.ts`"
- ✅ "Match the API service pattern in `src/services/AuthService.ts`"
- ❌ "Use best practices" (too vague)
- ❌ "Do what makes sense" (no constraint)

**Your Answer**:
```
Pattern to follow: _________________________________
```

---

### 2️⃣ Files to Touch ONLY

**Question**: Which files are you allowed to modify? (explicit list)

**Examples**:
- ✅ "ONLY modify: `.claude/commands/enforce-rules.md`, `CHANGELOG.md`"
- ✅ "Touch: `src/auth/login.ts`, `src/components/LoginForm.tsx`"
- ❌ "Any files needed" (no boundary)
- ❌ "Whatever is necessary" (scope creep invitation)

**Your Answer**:
```
Files allowed: _________________________________
```

---

### 3️⃣ Dependencies Allowed

**Question**: Can new dependencies be added? Which ones?

**Examples**:
- ✅ "Use existing libraries only (lodash, axios)"
- ✅ "No new npm packages without approval"
- ✅ "Can add: jest-mock-extended (testing only)"
- ❌ "Add whatever is needed" (no constraint)

**Your Answer**:
```
Dependencies: _________________________________
```

---

### 4️⃣ Scope Boundaries

**Question**: What is explicitly IN scope vs OUT of scope?

**Examples**:
- ✅ "IN: Login form only. OUT: Password reset, 2FA, registration"
- ✅ "IN: Timer start/stop. OUT: Reporting, analytics, export"
- ✅ "IN: Create /enforce-rules command. OUT: Automated enforcement"
- ❌ "Implement authentication" (too broad)
- ❌ "Whatever is needed" (infinite scope)

**Your Answer**:
```
IN scope: _________________________________
OUT of scope: _________________________________
```

---

### 5️⃣ Checkpoint Plan

**Question**: When will you commit? (granular checkpoints)

**Examples**:
- ✅ "After: structure, prompts 1-3, prompts 4-5, examples, testing"
- ✅ "After: tests, implementation, fixes, refactor"
- ✅ "Every 30 lines or 15 minutes"
- ❌ "When done" (too coarse)
- ❌ "At end of day" (no safety net)

**Your Answer**:
```
Commit checkpoints: _________________________________
```

---

## ✅ Constraint Summary

Once all 5 constraints are defined, copy this summary for reference during implementation:

```markdown
# Task Constraints

**Pattern**: [Your pattern to follow]
**Files**: [Explicit list of files allowed]
**Dependencies**: [Dependency policy]
**Scope IN**: [What's included]
**Scope OUT**: [What's excluded]
**Checkpoints**: [When to commit]
```

---

## 🚦 Validation Rules

**Before proceeding to implementation**:
- [ ] All 5 constraints explicitly defined (no blanks)
- [ ] File list is explicit (not "whatever needed")
- [ ] Scope boundaries are clear (IN vs OUT)
- [ ] Checkpoint plan is granular (not "when done")
- [ ] Pattern to follow is specific (not "best practices")

**If ANY constraint is vague or missing** → STOP, refine before coding

---

## 📚 Usage

Run this command BEFORE starting implementation:

```bash
/enforce-rules
```

Then:
1. Fill in all 5 constraints
2. Copy constraint summary to notes
3. Reference constraints during implementation
4. STOP if work expands beyond constraints

---

## 🎯 Real Example

**Task**: Create `/enforce-rules` slash command

**Constraints**:
```
Pattern: Follow structure in .claude/commands/checkpoint.md
Files: ONLY .claude/commands/enforce-rules.md, CHANGELOG.md
Dependencies: None (markdown only)
Scope IN: Command creation, prompts, examples, documentation
Scope OUT: Automated enforcement, hook integration, validation logic
Checkpoints: After structure, prompts 1-3, prompts 4-5, examples, testing
```

This is what **explicit boundaries** look like.

---

## 🚫 What This Prevents

Without these constraints, Claude will:
- ❌ Touch files you didn't expect
- ❌ Add dependencies without asking
- ❌ Expand scope ("while we're here...")
- ❌ Invent features you didn't request
- ❌ Make large changes without checkpoints

**With constraints, Claude stays on-rails.** 🎯

