# Problem-Solving Guide for Claude Code

## When Stuck: Decision Tree

**Step 1: Classify the block**
- Syntax/compile error → Check docs, try minimal reproduction
- Logic error → Rubber duck it, add logging
- Unknown cause → Binary search (comment out half)
- Concept gap → First principles (see below)
- Performance → Profile first, never guess

**Step 2: Apply relevant technique**

## Core Techniques

### 1. FIRST PRINCIPLES
Break to fundamentals, ignore conventions:
- What MUST be true?
- What am I assuming that might be false?
- Can I solve this without library X/pattern Y?

### 2. INVERSION
Instead of "how to fix", ask "what would break this worse?"
- What would cause this exact error?
- What would I do if I wanted this bug?
- Reveals hidden assumptions

### 3. BINARY SEARCH DEBUGGING
- Comment out 50% of code
- Does problem persist?
- Repeat on relevant half
- Isolates issue in log₂(n) steps

### 4. STATE INSPECTION
- Print actual values vs expected
- Check types/shapes/nulls
- Verify assumptions at each step

### 5. MINIMAL REPRODUCTION
- Remove all non-essential code
- Does problem still occur?
- If yes: problem is in remaining code
- If no: removed code caused it

### 6. CONSTRAINT RELAXATION
Stuck on "optimal" solution?
- Solve for small input first (n=1, n=2)
- Solve without constraint X
- Solve inefficiently, then optimize

### 7. ANALOGICAL THINKING
- What similar problem have I solved?
- How do other domains handle this?
- What's the data structure equivalent?

### 8. RUBBER DUCK (Force Precision)
Explain out loud:
- What should happen
- What actually happens
- Why I think X causes Y
- Often reveals false assumptions

### 9. FIVE WHYS (Root Cause)
- Problem: X fails
- Why? → Y is wrong
- Why? → Z wasn't set
- Why? → Config missing
- Why? → Docs unclear
- Why? → [root cause]

### 10. SCAMPER (Creative Pivots)
- **Substitute**: Different algorithm/library?
- **Combine**: Merge two approaches?
- **Adapt**: How does X do this?
- **Modify**: Change scope/constraints?
- **Purpose**: Solve different problem?
- **Eliminate**: What's unnecessary?
- **Reverse**: Work backwards?

## Anti-Patterns to Avoid

❌ Random changes hoping it works
❌ Optimizing before it works
❌ Assuming docs are current
❌ Trusting error messages blindly
❌ Skipping minimal reproduction
❌ Giving up after 1-2 attempts

## Quick Wins Checklist

✓ Read actual error (not first line, all of it)
✓ Check types match expected
✓ Verify file paths/names/case
✓ Test with simplest possible input
✓ Check version compatibility
✓ Read relevant docs section
✓ Search error verbatim
✓ Check if example code actually runs

## Meta-Strategy

**If still stuck after 3 techniques:**
1. Explain the problem to yourself in writing
2. List everything you've tried
3. Identify what you DON'T know
4. Search/read docs for gaps
5. Try opposite of current approach

**Remember:**
- Most bugs are typos/off-by-one/wrong variable
- Complex solutions usually wrong
- Sleep on it if >1 hour stuck
- Fresh perspective > brute force