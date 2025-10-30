---
description: Create detailed specification for new feature with aggressive scope reduction
---

# Feature Specification: $ARGUMENTS

You are creating a minimal, focused specification. Follow these steps:

## Step 1: Understand the Feature Request

Analyze the request: "$ARGUMENTS"

## Step 2: Ask Clarifying Questions

Before writing anything, ask 5-10 clarifying questions:

1. **Problem**: What exact problem does this solve?
2. **Users**: Who will use this feature?
3. **Scope**: What's the MINIMUM viable version?
4. **Constraints**: Are there technical limitations?
5. **Success**: How will we know it's done?
6. **Edge Cases**: What failure modes exist?
7. **Existing**: Does similar functionality exist in the codebase?
8. **Dependencies**: What does this depend on?
9. **Performance**: Are there performance requirements?
10. **Security**: Are there security considerations?

**STOP HERE** - Wait for answers before proceeding.

## Step 3: Aggressively Reduce Scope

After receiving answers, identify:
- **Core requirement** (must have)
- **Nice-to-haves** (defer to v2)
- **Out of scope** (explicitly exclude)

Create SPEC.md with:

```markdown
# Specification: [Feature Name]

## Problem Statement
[What problem are we solving?]

## Target Users
[Who needs this?]

## Minimal Solution (v1)
[Core functionality only - what's the absolute minimum?]

## Explicitly Out of Scope (v2+)
- [Feature X - defer]
- [Enhancement Y - not needed for v1]

## Success Criteria
- [ ] [Testable criterion 1]
- [ ] [Testable criterion 2]
- [ ] [Testable criterion 3]

## Technical Approach
[High-level technical approach]

## Edge Cases
1. [Edge case 1]
2. [Edge case 2]

## Acceptance Tests
```python
def test_feature_works_when_valid_input():
    # Test case 1
    pass

def test_feature_fails_when_invalid_input():
    # Test case 2
    pass
```

## Estimated Effort
[Small/Medium/Large - break down if Large]
```

## Step 4: Enter Planning Mode

After SPEC.md is reviewed and approved, say:

"SPEC approved. Entering Planning Mode (Shift+Tab×2) to create implementation plan."

Then create detailed task breakdown with:
- Each task ≤30 lines
- Clear acceptance criteria per task
- Test requirements per task
- File changes per task
