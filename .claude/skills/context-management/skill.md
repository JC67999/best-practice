---
name: Context Management
description: 60% rule and context optimization strategies
tags: context, token-management, memory, clear, compact
auto_load_triggers: context, compact, clear, token, memory, limit
priority: toolkit
---

# Context Management

## Purpose

Enforces the 60% Rule and provides strategies for managing context window efficiently to prevent information loss and maintain conversation quality.

---

## The 60% Rule

> **Never exceed 60% of context window capacity**

### Why 60%?

- Automatic compaction loses information
- Need buffer for responses
- Proactive management prevents emergency situations

---

## Context Limits

**Monitor context usage**:
- Watch for "approaching usage limit" warnings
- Proactively manage BEFORE hitting limits
- Context compaction = information loss

**When approaching 60%**:
- Use `/compact` manually if needed (loses some details)
- Use `/clear` to start fresh (recommended)
- Save state to files first (plan.md, progress.md)

---

## Context Best Practices

### Scope Sessions to Single Features

- One chat = one project or feature
- Use `/clear` when feature complete
- Use `/resume` or `--continue` to return to conversations

### Selective File Loading

**DO**:
- ✅ Use `@filename` syntax for specific files
- ✅ Use `.claudeignore` to exclude: node_modules/, vendor/, dist/, build/, large data files
- ✅ Load only relevant files

**DON'T**:
- ❌ Say "look at everything"
- ❌ Read all files when only some are needed
- ❌ Load large generated files

### Progressive Context Building

**Step-by-step approach**:
1. Read relevant files with NO CODE YET
2. Use subagents for investigation (preserves main context)
3. Request plan (do not code until confirmed)
4. Implement in small steps (diffs <200 lines)
5. Use checkpoints between steps

### External Memory Systems

**Write plans to files**:
- spec.md - Feature specifications
- requirements.md - Requirements
- design.md - Architecture designs
- plan.md - Implementation plans
- tasks.md - Task tracking

**Benefits**:
- Survive context window limits
- Enable regeneration from specs
- Become living documentation

---

## Context Management Anti-Patterns

### DON'T

- ❌ Dump multiple tasks at once ("do these one by one" instead)
- ❌ Let automatic compaction happen (use /clear proactively)
- ❌ Fill context with irrelevant command outputs
- ❌ Assume Claude remembers earlier conversations
- ❌ Read all files when only some are needed

### DO

- ✅ One task at a time
- ✅ Clear between unrelated tasks
- ✅ Save important state to files
- ✅ Reference specific files with @
- ✅ Use scripts for repetitive operations

---

## Token Optimization Strategies

### Use Subagents

**For exploration and research**:
```
Use Task tool with Explore subagent for:
- Codebase exploration
- Finding files
- Searching for patterns
```

**Benefits**:
- Independent context window
- Preserves main conversation context
- Results summarized back to main chat

### File Loading Strategy

**Instead of**:
```
"Read all the files in src/"
```

**Do**:
```
"Read src/auth.py and src/user.py"
```

**Use patterns**:
```
@src/auth.py - Load specific file
@src/**/*.test.ts - Load test files only
```

### Command Output Management

**DON'T fill context with**:
- Long npm install outputs
- Verbose test outputs
- Large file listings

**DO**:
- Filter outputs to relevant information
- Use `--quiet` flags when available
- Redirect verbose output to files

---

## When to Use /clear vs /compact

### Use /clear (Recommended)

**When**:
- Feature is complete
- Starting new unrelated task
- Context approaching 60%
- Clean slate needed

**Before clearing**:
- Save important state to files
- Document current progress
- Update task tracking

### Use /compact (Careful)

**When**:
- Mid-feature and need a bit more room
- Can't afford to lose current context
- Temporary measure only

**Note**: Compaction loses some details - not ideal

---

## Integration with MCP

**Save state before clearing**:
```
mcp__memory__save_session_summary
Args:
  summary = what was accomplished
  decisions = key decisions made
  next_steps = what to do next
```

**Load state in new session**:
```
mcp__memory__load_project_context
Args: project_path = current working directory
```

---

## Practical Example

**Bad - Context wasteful**:
```
User: "Fix all the bugs and add these 10 features"
Claude: [Tries to do everything, fills context, gets compacted, loses info]
```

**Good - Context efficient**:
```
User: "Fix all the bugs and add these 10 features"
Claude: "Let me work on these one at a time.
Starting with bug #1: Authentication error.
@src/auth.py [loads only relevant file]
[Fixes bug]
[Commits]
Ready for next task. What should I work on next?"
```

---

## Resources

- **CLAUDE.md**: Full context management section (Context Management Rules)
- **Memory MCP**: save_session_summary, load_project_context for persistence
- **.claudeignore**: Exclude files from context
