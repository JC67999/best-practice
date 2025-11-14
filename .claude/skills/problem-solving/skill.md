---
name: Problem-Solving Techniques
description: Systematic debugging and problem-solving methods (10 mandatory techniques)
tags: debugging, problem-solving, troubleshooting, stuck, error, bug
auto_load_triggers: error, bug, stuck, debug, troubleshoot, failing, broken
priority: toolkit
---

# Problem-Solving Techniques

## Purpose

Provides systematic problem-solving techniques to apply when encountering bugs, errors, or challenges. **Random changes and guessing are PROHIBITED** - use these techniques instead.

---

## When to Apply

**ALWAYS use these techniques when**:
- Tests fail unexpectedly
- Code produces incorrect output
- Errors or exceptions occur
- Performance issues arise
- Stuck on implementation approach
- Debugging any issue for >5 minutes

**NEVER**:
- Make random changes hoping it works
- Skip to solution without diagnosis
- Trust error messages blindly
- Give up after 1-2 attempts

---

## Decision Tree: When Stuck

**Step 1: Classify the problem**

| Type | Technique to Apply |
|------|-------------------|
| Syntax/compile error | Check docs, minimal reproduction |
| Logic error | Rubber duck, add logging |
| Unknown cause | Binary search debugging |
| Concept gap | First principles |
| Performance issue | Profile first, never guess |

**Step 2: Apply relevant technique(s) from below**

---

## The 10 Mandatory Techniques

### 1. FIRST PRINCIPLES
**For**: Concept gaps, complex problems

**Method**: Break problem to fundamentals, ignore conventions

**Questions to ask**:
- What MUST be true for this to work?
- What am I assuming that might be false?
- Can I solve this without library X or pattern Y?
- What's the simplest possible version?

**Example**:
```
Problem: Authentication not working
First Principles:
- User MUST have valid credentials ✓
- Token MUST be generated ?
- Token MUST be sent in request ?
- Token MUST be validated on server ?
→ Found: Token generation returns undefined
```

---

### 2. INVERSION
**For**: Mysterious bugs, unexpected behavior

**Method**: Instead of "how to fix", ask "what would break this worse?"

**Questions to ask**:
- What would cause this EXACT error?
- What would I do if I WANTED this bug?
- What's the opposite of what I expect?

**Example**:
```
Problem: Function returns wrong value sometimes
Inversion: What would make it ALWAYS return wrong value?
→ If input validation was broken
→ Check input validation
→ Found: Edge case when input is empty string
```

---

### 3. BINARY SEARCH DEBUGGING
**For**: Unknown cause, large codebase

**Method**: Isolate issue in log₂(n) steps

**Process**:
1. Comment out 50% of code
2. Does problem persist?
   - YES → Problem is in remaining code
   - NO → Problem is in commented code
3. Repeat on relevant half

**Example**:
```
100 lines of code causing error
→ Comment out lines 50-100: Still errors
→ Comment out lines 25-50: Still errors
→ Comment out lines 12-25: Error gone!
→ Issue is in lines 12-25
```

---

### 4. STATE INSPECTION
**For**: Logic errors, unexpected values

**Method**: Verify assumptions at each step

**Process**:
1. Print ACTUAL values vs EXPECTED values
2. Check types, shapes, nulls
3. Verify state at each step of execution

**Example**:
```python
# Wrong
result = process_data(data)

# Right - inspect state
print(f"Input data: {data}, type: {type(data)}")
result = process_data(data)
print(f"Result: {result}, type: {type(result)}")
print(f"Expected: {expected}, match: {result == expected}")
```

---

### 5. MINIMAL REPRODUCTION
**For**: Before asking for help, complex systems

**Method**: Remove all non-essential code

**Process**:
1. Create new file with ONLY the failing code
2. Remove all dependencies possible
3. Does problem still occur?
   - YES → Problem is in remaining code
   - NO → Removed code caused it

---

### 6. CONSTRAINT RELAXATION
**For**: Stuck on "optimal" solution

**Method**: Solve simpler version first

**Process**:
1. Solve for smallest input (n=1, n=2)
2. Solve without constraint X
3. Solve inefficiently first, optimize later

**Example**:
```
Problem: Optimize algorithm for 1M records
Constraint Relaxation:
1. First make it work for 10 records
2. Then 100 records
3. Then 1000 records
4. THEN optimize for 1M records
```

---

### 7. ANALOGICAL THINKING
**For**: New problems, unfamiliar domains

**Method**: Map to similar solved problems

**Questions**:
- What similar problem have I solved before?
- How do other domains handle this?
- What's the data structure equivalent?

---

### 8. RUBBER DUCK
**For**: All debugging (always helpful)

**Method**: Force precision by explaining out loud

**Template**:
```
"The function should [expected behavior] when given [input].
Instead, it [actual behavior].
I think this is because [assumption].
Let me verify [assumption] is true..."
```

---

### 9. FIVE WHYS
**For**: Root cause analysis

**Method**: Dig to root cause, not symptoms

**Process**:
```
Problem: X fails
1. Why? → Y is wrong
2. Why? → Z wasn't set
3. Why? → Config missing
4. Why? → Docs unclear
5. Why? → [ROOT CAUSE]
```

---

### 10. SCAMPER
**For**: Creative blocks, stuck approaches

**Method**: Creative pivots

**Techniques**:
- **S**ubstitute: Different algorithm/library?
- **C**ombine: Merge two approaches?
- **A**dapt: How does X solve this?
- **M**odify: Change scope/constraints?
- **P**urpose: Solve different problem instead?
- **E**liminate: What's unnecessary?
- **R**everse: Work backwards from goal?

---

## Quick Wins Checklist

**Before applying advanced techniques, check these**:

- [ ] Read the FULL error message (not just first line)
- [ ] Verify types match expected types
- [ ] Check file paths, names, and case sensitivity
- [ ] Test with simplest possible input
- [ ] Verify version compatibility
- [ ] Read relevant docs section
- [ ] Search error message verbatim
- [ ] Confirm example code actually runs

---

## Meta-Strategy: Still Stuck After 3 Techniques?

**If you've applied 3 techniques and still stuck**:

1. **Write it out**: Explain the problem in writing
2. **List attempts**: Document everything tried
3. **Identify gaps**: What do you NOT know?
4. **Research gaps**: Search/read docs for missing knowledge
5. **Try opposite**: Do the opposite of current approach

**When to escalate**:
- After applying 5+ techniques
- After >30 minutes on same issue
- When you've exhausted your knowledge

---

## Anti-Patterns

**NEVER do these** (they waste time):

- ❌ Random changes hoping something works
- ❌ Optimizing before it works at all
- ❌ Assuming docs are current without verifying
- ❌ Trusting errors blindly without investigation
- ❌ Skipping minimal reproduction
- ❌ Giving up after 1-2 attempts
- ❌ Copy-pasting solutions without understanding
- ❌ Debugging in production instead of locally

---

## Integration with TDD

**When tests fail**:
1. ✅ Read full error (Quick Wins #1)
2. ✅ Apply State Inspection (#4)
3. ✅ Rubber Duck the failure (#8)
4. ✅ Fix minimal code to pass

**When code breaks**:
1. ✅ Apply Binary Search Debugging (#3)
2. ✅ Create Minimal Reproduction (#5)
3. ✅ Use Five Whys for root cause (#9)

---

## Success Metrics

**Track these to improve**:
- Time to isolate root cause
- Number of techniques applied before solving
- Percentage of issues solved with first technique
- Rate of recurring similar issues (should decrease)

**Remember**:
- Most bugs are typos, off-by-one errors, or wrong variables
- Complex solutions are usually wrong
- Sleep on it if stuck >1 hour
- Fresh perspective beats brute force

---

## Resources

- **Full Guide**: See `docs/guides/thinking skills.md` for detailed examples
- **CLAUDE.md**: Complete problem-solving section
- **Integration**: Works with TDD Workflow, Quality Standards skills
