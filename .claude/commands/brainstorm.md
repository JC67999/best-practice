---
description: Structured brainstorming session before planning
---

# Brainstorm: $ARGUMENTS

Structured brainstorming for: "$ARGUMENTS"

## Phase 1: Divergent Thinking (Generate Ideas)

### Step 1: Problem Reframing

Ask 5 different ways to frame this problem:
1. **As an opportunity**: What opportunity does this create?
2. **As a constraint**: What constraints drive innovation?
3. **As a user need**: What do users actually need?
4. **As a technical challenge**: What's technically interesting?
5. **As a business goal**: What business value does this unlock?

### Step 2: Idea Generation (No Filtering)

Generate 10+ ideas WITHOUT judging them:
- Wild ideas (ignore constraints)
- Boring ideas (simplest possible)
- Expensive ideas (unlimited resources)
- Cheap ideas (zero budget)
- Fast ideas (ship in 1 day)
- Slow ideas (perfect over time)
- User-driven ideas (what users ask for)
- Data-driven ideas (what metrics suggest)
- Competitive ideas (what competitors don't have)
- Experimental ideas (uncertain but interesting)

**Rules**:
- ✅ Quantity over quality
- ✅ Build on others' ideas
- ✅ Encourage wild ideas
- ❌ No criticism yet
- ❌ No filtering yet

### Step 3: Pattern Recognition

Group similar ideas:
- **Theme 1**: [Name] - [Ideas that fit]
- **Theme 2**: [Name] - [Ideas that fit]
- **Theme 3**: [Name] - [Ideas that fit]

## Phase 2: Convergent Thinking (Evaluate Ideas)

### Step 4: Feasibility Matrix

Rate each idea on:
- **Impact** (1-10): User/business value
- **Effort** (1-10): Implementation complexity
- **Risk** (1-10): Technical/business risk

```markdown
| Idea | Impact | Effort | Risk | Score |
|------|--------|--------|------|-------|
| Idea 1 | 9 | 3 | 2 | High |
| Idea 2 | 7 | 8 | 7 | Low |
```

**Score calculation**: `Impact / (Effort × Risk)`

### Step 5: Constraint Filtering

Filter by constraints:
- **Must have**: [List constraints]
- **Nice to have**: [List preferences]
- **Deal breakers**: [List blockers]

Which ideas survive all constraints?

### Step 6: Top 3 Selection

Select top 3 ideas based on:
1. Highest feasibility score
2. Best constraint fit
3. Team excitement level

**Top 3**:
1. **[Idea name]** - [Why it's top]
2. **[Idea name]** - [Why it's top]
3. **[Idea name]** - [Why it's top]

## Phase 3: Refinement

### Step 7: Devil's Advocate

For each top idea, ask:
- **What could go wrong?**
- **What assumptions are we making?**
- **What's the worst-case scenario?**
- **How would competitors attack this?**
- **What would make users hate this?**

Document risks and mitigation strategies.

### Step 8: Enhancement

For each top idea:
- **Make it 10x better**: What if unlimited resources?
- **Make it 10x smaller**: What's the absolute minimum?
- **Make it 10x faster**: How to ship in 1/10 the time?
- **Make it 10x cheaper**: How to build for free?

### Step 9: Prototype Thinking

For the #1 idea:
- **5-minute prototype**: What could you sketch/build in 5 min?
- **1-hour prototype**: What could you validate in 1 hour?
- **1-day prototype**: What MVP could ship in 1 day?

## Phase 4: Decision

### Step 10: Final Recommendation

**Recommended approach**: [Idea name]

**Why this one**:
- Impact: [Specific user/business value]
- Feasibility: [Why it's achievable]
- Risk: [Why risks are manageable]
- Alignment: [How it fits constraints/goals]

**Next steps**:
1. Use `/plan [idea]` to create implementation plan
2. Use `/spec [idea]` to write detailed specification
3. Create prototype to validate assumptions

**Alternatives to consider**:
- **Plan B**: [Second choice if #1 fails]
- **Plan C**: [Third choice as fallback]

## Brainstorming Best Practices

**DO**:
- Separate idea generation from evaluation
- Generate at least 10 ideas before filtering
- Consider wild/impossible ideas (they spark creativity)
- Build on others' ideas ("yes, and...")
- Document all ideas (even "bad" ones)

**DON'T**:
- Judge ideas during generation phase
- Stop at first good idea
- Ignore constraints forever (but ignore them initially)
- Forget to validate assumptions
- Skip the devil's advocate phase

## Output Format

Save brainstorm to: `docs/notes/brainstorm-[feature]-[date].md`

Include:
- All generated ideas
- Feasibility matrix
- Top 3 selections with rationale
- Final recommendation
- Next steps

Ready to move to planning phase? Use `/plan [recommended-idea]`
