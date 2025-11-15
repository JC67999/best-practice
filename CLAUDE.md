# Project Standards - Best Practice Toolkit

> **Purpose**: Enforce changelog, comments, minimal structure - maximum efficiency
> **Last Updated**: 2025-11-15
> **Applies To**: Claude Code and all AI assistants working on this codebase

---

## 🎯 Core Objective

**Enforce**: Changelog for every change + Well-commented code + Minimal structure
**Focus**: Speed and frugality - no bloat
**No**: Unsolicited reports, verbose docs, or folder sprawl

---

## 💡 Skills-Based Architecture

> **Progressive disclosure**: Load only what you need, when you need it

**Claude automatically loads relevant skills based on your task**:
- `quality-standards` - When testing or checking code
- `tdd-workflow` - When writing tests
- `problem-solving` - When debugging (10 systematic techniques)
- `git-workflow` - When committing
- `file-placement` - When creating files
- `planning-mode` - When planning features
- `mcp-usage` - When using MCP tools
- `context-management` - When managing tokens
- `domain-learning` - When learning new domains

**Skills location**: `.claude/skills/` folder
**Benefits**: Load ~3KB skills vs entire CLAUDE.md (was 64KB, now streamlined)
**Create your own**: Use `.claude/skills/template/skill.md`

---

## ✅ MANDATORY: Live Task List (TASKS.md)

**Every change must be tracked as a granular task**

### Task Rules
1. **Read .claude/TASKS.md first** - Check current tasks before coding
2. **Task size**: ≤30 lines of code, ≤15 minutes
3. **One task at a time**: Complete, test, commit before next
4. **Break down large tasks**: If >30 lines, STOP and break into sub-tasks
5. **Update TASKS.md**: Mark complete when done, add new as discovered

### Workflow
```
1. Check .claude/TASKS.md
2. Implement (≤30 lines)
3. Test change works
4. Run quality gate
5. Commit with descriptive message
6. Mark task complete
7. Move to next task
```

**If task feels too large**: STOP, break it down first, then implement smallest piece.

---

## ⚡ MANDATORY MCP Usage

> **CRITICAL**: MCP tools enforce project standards - NOT optional

### Session Start (ALWAYS)

**Before ANY work**:
```
1. mcp__memory__load_project_context
2. mcp__project__get_current_status
```

**NEVER skip** - working without context = scope creep

---

### Before Starting ANY Task (MANDATORY)

**Validate alignment**:
```
1. mcp__project__validate_task_alignment
   - Score ≥70: Proceed
   - Score <70: Ask user for confirmation

2. mcp__project__validate_task_size
   - Too large: Break down BEFORE implementing
```

---

### Before Completing ANY Task (MANDATORY)

**Quality gate**:
```
1. mcp__quality__run_quality_gate
   - PASS: Commit and mark complete
   - FAIL: Fix issues, re-run, repeat until PASS
```

**NEVER override quality gate failure**

---

### Session End (ALWAYS)

**Save context**:
```
mcp__memory__save_session_summary
```

---

### Complete MCP Tool Reference

**Memory MCP**:
- `load_project_context` - **MANDATORY at session start**
- `save_session_summary` - **MANDATORY at session end**
- `save_decision` - Save architectural decisions
- `search_memory` - Search across projects
- `list_projects` - See all tracked projects

**Quality MCP**:
- `run_quality_gate` - **MANDATORY before task completion**
- `check_code_quality` - Check specific files
- `audit_project_structure` - Validate minimal root
- `validate_file_placement` - Check file locations
- `verify_standards` - Comprehensive check

**Project MCP**:
- `get_current_status` - **MANDATORY at session start**
- `validate_task_alignment` - **MANDATORY before starting**
- `validate_task_size` - Check if task is small enough
- `challenge_task_priority` - Verify highest priority
- `mark_task_complete` - Mark done (requires quality gate PASS)
- `identify_scope_creep` - Find non-essential tasks
- `create_task_breakdown` - Break project into tasks

**Learning MCP** (FULL mode only):
- `detect_project_objective` - Read PROJECT_PLAN.md to understand domain
- `map_objective_to_domains` - Map objective to research domains (PM, optimization, docs, etc.)
- `research_domain_topic` - Generate domain-specific research plan
- `store_learning` - Save research to `docs/references/domain-knowledge/`
- `get_learnings` - Retrieve project-specific knowledge base

**How Learning MCP Works**:
- **Project-Objective-Driven**: Adapts to each project's domain
- **Examples**:
  - rapid-pm → researches PM methodologies, Scrum, Agile, tools
  - ai-task-optimisation-MVP → researches optimization algorithms, solvers
  - document-generator → researches doc methodologies, templates
- **Storage**: Saves to project's `docs/references/domain-knowledge/{domain}/`
- **Dynamic**: Uses WebFetch for real-time data, no hardcoded lists

**Usage Example**:
```
1. mcp__learning__detect_project_objective(project_path="/path/to/project")
2. mcp__learning__map_objective_to_domains(objective_data)
3. mcp__learning__research_domain_topic(topic="sprint planning")
   → Returns domain-specific search queries and sources
4. Use WebSearch/WebFetch with returned queries
5. mcp__learning__store_learning(topic, learning_data, project_path)
   → Saves to docs/references/domain-knowledge/project_management/
```

**See** `.claude/skills/domain-learning/` for detailed workflows

---

## 🎯 Planning Mode - MANDATORY for New Features

> **CRITICAL**: Planning Mode (Shift+Tab×2) is NON-NEGOTIABLE

**ALWAYS enter Planning Mode for**:
- New features or functionality
- Significant refactoring (>30 lines)
- Complex bug fixes requiring multiple files
- Architecture changes
- Unclear requirements

**Rules**:
1. NEVER skip Planning Mode for new features
2. Plans must include: tasks, acceptance criteria, file changes, tests
3. Get explicit user approval before exiting Planning Mode
4. Document plan in .claude/TASKS.md

**See** `.claude/skills/planning-mode/` for detailed workflow

---

## 🧠 Context Management

> **The 60% Rule**: Never exceed 60% of context window

**When approaching 60%**:
- Use `/compact` or `/clear` and save state to files
- Scope sessions to single features
- Use selective file loading with `@filename`
- Use `.claudeignore` to exclude: node_modules/, vendor/, dist/, build/

**See** `.claude/skills/context-management/` for best practices

---

## 📁 File Placement Rules

### Root Directory - MINIMAL (≤5 folders, ≤5 files)

**Allowed Folders** (5 maximum):
```
/.claude/         - Toolkit files
/tests/           - Test suite
/docs/            - ALL documentation
/dist/            - Distribution packages (generated)
/retrofit-tools/  - Retrofit scripts
```

**Allowed Files**:
```
/README.md        - Brief overview
/CLAUDE.md        - This file
/package_toolkit.sh - Build script
/.gitignore       - Git ignore
/LICENSE          - MIT license
```

**FORBIDDEN in Root**:
- ❌ Documentation files (except README.md and CLAUDE.md)
- ❌ Configuration files
- ❌ Data files
- ❌ Log files
- ❌ Temporary files

**See** `.claude/skills/file-placement/` for complete structure

---

## 🎯 Development Workflow

### MANDATORY: Create GitHub Issue Before Code Changes

**Before ANY code changes going to GitHub**:

```bash
# 1. Create issue BEFORE work
gh issue create --title "feat: Add feature X"

# 2. Note issue number (#42)

# 3. Create branch
git checkout -b feature/feature-x-#42

# 4. Work on task

# 5. Link commits
git commit -m "feat: implement X

Closes #42"

# 6. Create PR
gh pr create --title "feat: Add feature X (closes #42)"
```

**When to create issue**:
- ✅ New features, bug fixes, refactoring, performance, security
- ❌ Documentation-only, local experiments, trivial changes

**Enforcement**:
- ❌ DO NOT start coding without issue
- ❌ DO NOT commit without referencing issue
- ✅ ALWAYS: issue → branch → code → commit → PR

---

### Quality Standards

**Before ANY commit**:
```bash
bash .claude/quality-gate/check_quality.sh
```

**Requirements**:
- ≥80% test coverage
- Zero linting errors
- Zero type errors
- Zero security issues

**See** `.claude/skills/quality-standards/` for details

---

### Test-Driven Development (TDD) - MANDATORY

> **Red-Green-Refactor**: Write tests first, see them fail, make them pass

**Workflow**:
1. Write failing tests (RED)
2. Confirm tests fail
3. Commit failing tests
4. Implement minimal code (GREEN)
5. Iterate until tests pass
6. Refactor while green
7. Commit

**See** `.claude/skills/tdd-workflow/` for detailed cycle

---

### Git Checkpoint Workflow

> **Fearless exploration**: Save before risky changes

**Native checkpointing**:
- Claude auto-saves before edits
- Use Esc×2 or `/rewind` to rollback

**Manual checkpoints**:
```bash
git tag checkpoint-before-refactor
# ... risky work ...
git reset --hard checkpoint-before-refactor  # if failed
```

**See** `.claude/skills/git-workflow/` for patterns

---

## 🚫 Anti-Patterns - What NOT to Do

### Prohibited Implementation
**NEVER**:
- Incomplete implementations or placeholders
- Mock functions or TODO comments
- Skip error handling or edge cases

### Prohibited Communication
**NEVER**:
- Social validation ("You're absolutely right!")
- Hedging language ("might," "could")
- Over-apologizing

### Premature Coding (#1 Failure Mode)
**NEVER start coding when**:
- Requirements unclear
- No plan created
- User hasn't approved
- Success criteria undefined

**ALWAYS ask first**: What? Why? Edge cases? Constraints?

### Technical Mistakes
**NEVER**:
- Skip compiling before tests
- Write tests expecting pass without seeing fail
- Leave old code when rewriting

---

## 🧠 Problem-Solving Techniques

> **MANDATORY when debugging**: Apply systematic techniques, NO random changes

**Decision tree when stuck**:
| Type | Technique |
|------|-----------|
| Syntax/compile | Check docs, minimal reproduction |
| Logic error | Rubber duck, state inspection |
| Unknown cause | Binary search debugging |
| Concept gap | First principles |
| Performance | Profile first, never guess |

**10 Core Techniques**:
1. First Principles - Break to fundamentals
2. Inversion - Ask what would break this worse
3. Binary Search - Isolate in log₂(n) steps
4. State Inspection - Verify assumptions
5. Minimal Reproduction - Remove non-essential
6. Constraint Relaxation - Solve simpler first
7. Analogical Thinking - Map to solved problems
8. Rubber Duck - Explain out loud
9. Five Whys - Dig to root cause
10. SCAMPER - Creative pivots

**See** `.claude/skills/problem-solving/` and `docs/guides/thinking skills.md` for detailed examples

---

## ⚡ Slash Commands

**Core commands**:
- `/spec [feature]` - Create minimal specification
- `/plan [feature]` - Enter Planning Mode
- `/tdd [feature]` - Execute TDD cycle
- `/checkpoint [name]` - Create git checkpoint

**Custom commands**: `.claude/commands/[name].md`

---

## ✅ Pre-Commit Checklist

- [ ] GitHub issue created (for code changes)
- [ ] Commit references issue number
- [ ] All tests pass
- [ ] Quality gate passed
- [ ] Structure compliance (≤5 root folders)
- [ ] Documentation updated (if API changed)
- [ ] Changes ≤30 lines (or checkpointed)

---

## 🎯 Success Metrics

**Code Quality**:
- Test coverage ≥80%
- Zero linting/type/security errors

**Structure**:
- Root folders ≤5
- All docs in docs/
- No forbidden files in root

**Process**:
- Daily commits minimum
- 100% quality gate pass rate
- Task size compliance (≤30 lines)

---

## 🎯 The Discovery-First Principle

> **"The plan truly is the prompt"** - Ten minutes defining boundaries saves hours of drift

**Framework**:
1. **Planning Mode** - NON-NEGOTIABLE for new features
2. **Ask first** - Never code with unclear requirements
3. **60% context rule** - Manage before hitting limits
4. **TDD cycle** - Tests first, see fail, make pass
5. **Atomic tasks** - ≤30 lines, testable, independent
6. **Git checkpoints** - Fearless exploration
7. **Slash commands** - Automate workflows
8. **Problem-solving** - Systematic debugging only
9. **Skills-based** - Load what you need

The best code is written while you're not watching—if you've defined what you want clearly first.

---

**Last Updated**: 2025-11-15
**Review**: After major features or monthly
**Applies To**: All AI assistants on this project
