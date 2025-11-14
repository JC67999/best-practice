# Best Practice Toolkit - User Guide

> **Complete guide to using the best-practice toolkit for AI-assisted development**

**Version**: 1.3.0
**Last Updated**: 2025-11-14

---

## 📚 Table of Contents

1. [What is This Toolkit?](#what-is-this-toolkit)
2. [Quick Start](#quick-start)
3. [The Three Components](#the-three-components)
4. [Daily Workflow](#daily-workflow)
5. [MCP Tools Reference](#mcp-tools-reference)
6. [Skills System](#skills-system)
7. [Learning MCP - Self-Learning](#learning-mcp---self-learning)
8. [Slash Commands](#slash-commands)
9. [Common Use Cases](#common-use-cases)
10. [Troubleshooting](#troubleshooting)

---

## What is This Toolkit?

The **best-practice toolkit** is a comprehensive system that enforces software engineering best practices during AI-assisted development. It ensures:

- ✅ **Quality**: 80%+ test coverage, zero linting errors
- ✅ **Structure**: Minimal root folders (≤5), organized codebase
- ✅ **Process**: Git checkpoints, TDD workflows, granular tasks
- ✅ **Clarity**: Mandatory objective clarification before work
- ✅ **Learning**: Auto-updates from Anthropic's latest best practices

### What Makes It Unique?

1. **Enforces, doesn't suggest**: Quality gates BLOCK commits until standards are met
2. **Self-learning**: Automatically scans Anthropic's repos (skills, cookbooks, quickstarts)
3. **Persistent memory**: Context survives across sessions
4. **Modular skills**: Progressive disclosure with auto-discovery
5. **Gitignored by default**: Stays local, never pollutes your repository

---

## Quick Start

### Installation

**Default: Local Only (NOT committed to git)**
```bash
cd /path/to/your/project
/home/jc/CascadeProjects/best-practice/retrofit-tools/smart_install.sh
```

**Optional: Commit Toolkit to Git**
```bash
cd /path/to/your/project
/home/jc/CascadeProjects/best-practice/retrofit-tools/smart_install.sh --commit
```

### What Gets Installed?

All files install to `.claude/` folder in your project:

```
your-project/
├── .claude/
│   ├── best-practice.md          # Project standards
│   ├── TASKS.md                   # Live task list
│   ├── skills/                    # 9 toolkit skills
│   │   ├── quality-standards/
│   │   ├── tdd-workflow/
│   │   ├── problem-solving/
│   │   ├── git-workflow/
│   │   └── ...
│   ├── mcp-servers/               # 3 MCP servers (FULL mode only)
│   │   ├── memory_mcp.py
│   │   ├── quality_mcp.py
│   │   ├── project_mcp.py
│   │   └── learning_mcp.py
│   ├── quality-gate/              # Quality gate scripts (FULL mode only)
│   └── commands/                  # Slash commands
└── your-project-files...
```

**Note**: `.claude/` is automatically gitignored by Claude Code, so toolkit files stay local by default.

---

## The Three Components

The toolkit has three main components that work together:

### 1. MCP Tools (Enforce Standards)

**Model Context Protocol** servers that provide AI-callable tools for:
- **Memory**: Persistent context across sessions
- **Quality**: Quality gates and code analysis
- **Project**: Objective clarification and task management
- **Learning**: Self-learning from Anthropic resources

### 2. Skills (Modular Knowledge)

**Progressive disclosure** system with 9 toolkit skills:
- Load only what's needed (saves tokens)
- Auto-discovery via trigger keywords
- Metadata-first, details on demand
- Projects can add domain-specific skills

### 3. Slash Commands (Automate Workflows)

**Custom commands** in `.claude/commands/` that automate:
- `/plan` - Enter Planning Mode
- `/spec` - Create feature specifications
- `/tdd` - Test-driven development workflow
- `/checkpoint` - Create git safety checkpoints
- `/debug` - Systematic debugging workflow
- `/mcp` - Scaffold new MCP servers

---

## Daily Workflow

### Start Every Session

**1. Load Project Context**
```bash
# Claude will automatically call:
mcp__memory__load_project_context
mcp__project__get_current_status
```

This tells you:
- Project objective and clarity score
- Current tasks (pending/in-progress/completed)
- Recent decisions and history
- Next steps

### Before Starting ANY Task

**2. Validate Task Alignment**
```bash
# Claude checks if task serves the objective:
mcp__project__validate_task_alignment
```

- **Alignment score ≥70**: Task is aligned, proceed
- **Alignment score <70**: Task does NOT serve objective, ask user

**3. Check Task Size**
```bash
# Claude checks if task is ≤30 lines:
mcp__project__validate_task_size
```

- If too large, break into smaller sub-tasks first

### During Development

**4. Work on Task**
- Implement changes (≤30 lines per task)
- Follow TDD: Write tests first, see them fail, make them pass
- Update TASKS.md as you go

**5. Test Changes**
```bash
# Run tests to verify changes work
pytest tests/ -v
```

### Before Completing Task

**6. Run Quality Gate**
```bash
# Claude calls MANDATORY quality gate:
mcp__quality__run_quality_gate
```

**Quality gate checks**:
- ✅ All tests pass
- ✅ No linting errors (ruff)
- ✅ No type errors (mypy)
- ✅ Structure compliance (≤5 root folders)
- ✅ Changelog updated

**If quality gate FAILS**: Fix issues, re-run gate. DO NOT proceed until it passes.

**7. Commit Changes**
```bash
git add -A
git commit -m "feat: descriptive message

🤖 Generated with [Claude Code](https://claude.com/claude-code)

Co-Authored-By: Claude <noreply@anthropic.com>"
```

### End Every Session

**8. Save Session Summary**
```bash
# Claude saves context for next time:
mcp__memory__save_session_summary
```

Includes:
- What was accomplished
- Decisions made
- Next steps
- Current blockers

---

## MCP Tools Reference

### Memory MCP (Context Persistence)

**Purpose**: Store and retrieve project context across sessions

**Tools**:
- `load_project_context` - **MANDATORY at session start**
- `save_session_summary` - **MANDATORY at session end**
- `save_decision` - Document architectural decisions
- `search_memory` - Search across all projects
- `load_project_objective` - Load objective details
- `list_projects` - See all tracked projects

**Prompts**:
- `/mcp__memory__session_start` - Guided session startup
- `/mcp__memory__session_end` - Guided session summary
- `/mcp__memory__document_decision` - Document decision with rationale

**When to use**:
- **Every session start**: Load context
- **Every session end**: Save summary
- **After major decisions**: Document why you chose approach X over Y

---

### Quality MCP (Quality Enforcement)

**Purpose**: Enforce code quality standards and block commits until met

**Tools**:
- `run_quality_gate` - **MANDATORY before task completion**
- `check_code_quality` - Check specific files
- `audit_project_structure` - Validate minimal root compliance
- `validate_file_placement` - Check files in correct locations
- `find_obsolete_files` - Detect unused code
- `verify_standards` - Comprehensive standards check
- `update_documentation` - Update README with changes
- `update_changelog` - Add changelog entry
- `add_missing_docstrings` - Generate docstrings

**Prompts**:
- `/mcp__quality__code_review` - Systematic code review (OWASP Top 10)
- `/mcp__quality__pre_commit_check` - Pre-commit checklist
- `/mcp__quality__security_audit` - Full security audit

**When to use**:
- **Before every commit**: Run quality gate
- **After writing significant code**: Check code quality
- **When creating new files**: Validate file placement
- **Before pull requests**: Run code review prompt

---

### Project MCP (Objective & Tasks)

**Purpose**: Clarify objectives, manage tasks, prevent scope creep

**Tools**:
- `get_current_status` - **MANDATORY at session start**
- `validate_task_alignment` - **MANDATORY before starting task**
- `validate_task_size` - Check if task is ≤30 lines
- `clarify_project_objective` - Define objective (new projects)
- `score_objective_clarity` - Check objective clarity (0-100)
- `define_project_objective` - Finalize objective
- `create_task_breakdown` - Break project into tasks
- `challenge_task_priority` - Verify working on highest priority
- `mark_task_complete` - Mark task done (requires quality gate PASS)
- `identify_scope_creep` - Find non-essential tasks
- `refocus_on_objective` - Cut tasks that don't serve objective
- `sync_plan_to_reality` - Update plan to match actual state

**Prompts**:
- `/mcp__project__plan_feature` - Feature planning with validation
- `/mcp__project__daily_standup` - Review progress and blockers
- `/mcp__project__refocus` - Identify and cut scope creep
- `/mcp__project__task_breakdown` - Break tasks into ≤30 line pieces

**When to use**:
- **Session start**: Get current status
- **Before any task**: Validate alignment and size
- **Every 5-10 tasks**: Check for scope creep
- **When stuck**: Challenge if working on right priority

---

### Learning MCP (Self-Learning)

**Purpose**: Keep toolkit updated with latest Anthropic best practices

**Tools**:
- `scan_anthropic_skills` - Scan 15 skills across 5 categories
- `scan_anthropic_cookbooks` - Scan 28 cookbooks (27.6k stars)
- `scan_anthropic_quickstarts` - Scan 4 starter projects (10.2k stars)
- `scan_anthropic_org` - Scan all 54 Anthropic repositories
- `compare_skills` - Compare Anthropic vs toolkit skills
- `suggest_skill_updates` - Prioritize skills as HIGH/MEDIUM/LOW/SKIP
- `download_skill` - Download skill from GitHub
- `store_learning` - Store best practices in JSON
- `get_learnings` - Retrieve learnings by topic/date

**Prompts**:
- `/mcp__learning__update_toolkit` - Scan and update with new skills
- `/mcp__learning__research_topic` - Research best practices for topic
- `/mcp__learning__scan_all_resources` - Comprehensive scan of ALL resources

**When to use**:
- **Weekly/Monthly**: Scan for new Anthropic skills and patterns
- **When starting new domain**: Research best practices for that domain
- **Before major projects**: Check if Anthropic has relevant examples

**Example - Update toolkit with new skills**:
```bash
/mcp__learning__update_toolkit

# This will:
# 1. Scan Anthropic's skills repository
# 2. Compare with our toolkit skills
# 3. Suggest which skills to add (HIGH/MEDIUM/LOW priority)
# 4. Download recommended skills
# 5. Update documentation
```

**Example - Research a topic**:
```bash
/mcp__learning__research_topic topic="testing"

# This will:
# 1. Search for testing best practices (2024-2025)
# 2. Extract key principles and patterns
# 3. Store learnings in ~/.claude_memory/learnings/testing/
# 4. Suggest toolkit updates based on research
```

**What gets scanned**:
- **15 Skills**: Development, Meta, Documents, Creative, Enterprise
- **28 Cookbooks**: RAG, Tool Use, Multimodal, Patterns, Third-Party
- **4 Quickstarts**: Customer support, Financial analysis, Computer use
- **54 Org Repos**: 7 SDKs, Agent frameworks, Security tools, Courses

---

## Skills System

### What Are Skills?

**Skills** are modular knowledge modules with progressive disclosure:
- **Metadata-first**: Claude sees name/description/tags first (low token cost)
- **Auto-discovery**: Loads automatically via trigger keywords
- **Details on demand**: Full content loaded only when relevant
- **Two-tier system**: Toolkit skills (universal) + Project skills (domain-specific)

### Toolkit Skills (9 Universal Skills)

**1. quality-standards** (6.75KB)
- **Triggers**: `test`, `quality`, `coverage`, `lint`, `commit`
- **Content**: Code quality, testing standards, documentation requirements

**2. tdd-workflow** (7.3KB)
- **Triggers**: `tdd`, `test-driven`, `red-green-refactor`, `test first`
- **Content**: Test-driven development workflow

**3. problem-solving** (7.8KB)
- **Triggers**: `debug`, `error`, `bug`, `stuck`, `troubleshoot`
- **Content**: 10 mandatory debugging techniques

**4. git-workflow**
- **Triggers**: `commit`, `git`, `checkpoint`, `rollback`, `branch`
- **Content**: Git commits, checkpoints, branch strategy, rollback patterns

**5. file-placement**
- **Triggers**: `file`, `folder`, `structure`, `organize`, `create`
- **Content**: Minimal root structure, file organization rules

**6. planning-mode**
- **Triggers**: `plan`, `planning`, `feature`, `design`, `architecture`
- **Content**: Discovery-first planning (Shift+Tab×2)

**7. mcp-usage**
- **Triggers**: `mcp`, `tools`, `memory`, `quality`, `project`
- **Content**: When/how to use Memory, Quality, Project MCPs

**8. context-management**
- **Triggers**: `context`, `tokens`, `memory`, `clear`, `compact`
- **Content**: 60% rule, token optimization strategies

**9. domain-learning**
- **Triggers**: `learn`, `research`, `documentation`, `best practices`
- **Content**: Autonomous research and knowledge base building

### How Skills Get Loaded

**1. Automatic (Trigger Keywords)**
```
User: "I need to debug this error"
# Triggers: "debug", "error"
# Auto-loads: problem-solving skill
```

**2. Manual (Explicit Request)**
```bash
# Load specific skill
@.claude/skills/tdd-workflow/skill.md
```

**3. Progressive Disclosure**
- Claude sees metadata first (name, description, tags)
- Loads full content only when relevant to current task
- Saves tokens (~70% reduction vs monolithic CLAUDE.md)

### Creating Project-Specific Skills

**Template available at**: `.claude/skills/template/skill.md`

**Example - Create "django-patterns" skill**:

```markdown
---
name: Django Patterns
description: Django best practices and common patterns for this project
tags: django, python, web, patterns, orm
auto_load_triggers: django, model, view, template, queryset
priority: project
---

# Django Patterns

**Purpose**: Document Django-specific patterns used in this project

## When to Use
- When working with Django models, views, or templates
- When implementing Django-specific features
- When following project Django conventions

## Model Patterns

### 1. Always Use Related Names
```python
class Author(models.Model):
    name = models.CharField(max_length=100)

class Book(models.Model):
    author = models.ForeignKey(
        Author,
        on_delete=models.CASCADE,
        related_name='books'  # Always specify!
    )
```

... (continue with project-specific patterns)
```

**Benefits of project skills**:
- ✅ Domain-specific knowledge preserved
- ✅ Team conventions documented
- ✅ Auto-loads when relevant
- ✅ Version-controlled with project

---

## Slash Commands

### Available Commands

**Feature Development**:
- `/spec [feature]` - Create minimal specification
- `/plan [feature]` - Enter Planning Mode and create plan
- `/tdd [feature]` - Execute test-driven development cycle
- `/execute-plan` - Execute plan with auto checkpoints

**Code Quality**:
- `/checkpoint [name]` - Create git checkpoint before risky operations
- `/debug [issue]` - Systematic debugging workflow

**Toolkit Management**:
- `/mcp [name]` - Scaffold new MCP server

### How to Use Slash Commands

**Syntax**:
```bash
/command [arguments]
```

**Example - Plan a feature**:
```bash
/plan user-authentication

# This will:
# 1. Enter Planning Mode (read-only, cannot write code)
# 2. Ask clarifying questions about requirements
# 3. Create detailed task breakdown
# 4. Request user approval before implementation
```

**Example - TDD workflow**:
```bash
/tdd implement-jwt-tokens

# This will:
# 1. Write failing tests (RED)
# 2. Implement minimal solution (GREEN)
# 3. Refactor with tests passing
# 4. Commit with descriptive message
```

**Example - Create checkpoint**:
```bash
/checkpoint before-auth-refactor

# This will:
# 1. Ensure working directory is clean
# 2. Create git tag: checkpoint-before-auth-refactor-20251114-1430
# 3. You can now work fearlessly
# 4. Rollback with: git reset --hard <tag>
```

### Creating Custom Commands

**Location**: `.claude/commands/[name].md`

**Example** - Create `/review` command:

```markdown
---
description: Review code for quality issues
---

# Code Review

Review the code in $ARGUMENTS for:

1. Code quality issues
2. Test coverage gaps
3. Security vulnerabilities (OWASP Top 10)
4. Performance concerns

Provide actionable feedback with specific line numbers.

Use the following tools:
- mcp__quality__check_code_quality for automated checks
- mcp__quality__verify_standards for comprehensive review
```

**Save to**: `.claude/commands/review.md`

**Use it**:
```bash
/review src/auth.py
```

---

## Common Use Cases

### Use Case 1: Starting a New Feature

```bash
# 1. Check current project status
# (Claude automatically calls load_project_context and get_current_status)

# 2. Create specification
/spec Add password reset functionality

# 3. Create implementation plan
/plan Password reset via email

# 4. Validate first task aligns with objective
# (Claude automatically calls validate_task_alignment)

# 5. Implement using TDD
/tdd Password reset token generation

# 6. Quality gate before commit
# (Claude automatically calls run_quality_gate)

# 7. Commit changes
# (Automatic git commit with proper message format)

# 8. Move to next task in plan
# (Repeat steps 4-7)
```

### Use Case 2: Debugging an Error

```bash
# 1. Use systematic debugging
/debug Tests failing in CI

# This will:
# - Apply 10 mandatory problem-solving techniques
# - Binary search debugging to isolate issue
# - State inspection to verify assumptions
# - Minimal reproduction to confirm fix
# - Document root cause
```

### Use Case 3: Updating Toolkit with New Best Practices

```bash
# 1. Scan all Anthropic resources
/mcp__learning__scan_all_resources

# This will:
# - Scan skills repository (15 skills)
# - Scan cookbooks repository (28 cookbooks)
# - Scan quickstarts repository (4 projects)
# - Scan organization repositories (54 repos)
# - Compare with our toolkit
# - Suggest which to add (HIGH/MEDIUM/LOW priority)
# - Generate action plan

# 2. Download high-priority skills
# (Follow recommendations from scan)

# 3. Update documentation
# (Update .claude/skills/README.md and CHANGELOG.md)
```

### Use Case 4: Code Review Before Pull Request

```bash
# 1. Run comprehensive code review
/mcp__quality__code_review

# This will check:
# - Code structure and organization
# - Security vulnerabilities (OWASP Top 10)
# - Performance issues
# - Test coverage
# - Documentation completeness

# 2. Run pre-commit check
/mcp__quality__pre_commit_check

# This will verify:
# - All tests pass
# - No linting errors
# - Changelog updated
# - Documentation updated

# 3. Create pull request
# (After all checks pass)
```

### Use Case 5: Risky Refactoring

```bash
# 1. Create safety checkpoint
/checkpoint before-auth-refactor

# 2. Break refactoring into small tasks (≤30 lines each)
# Example tasks:
# - Extract function signatures (no implementation)
# - Move functions to new module
# - Update implementations
# - Update tests

# 3. For each task:
#    a. Implement (≤30 lines)
#    b. Run tests (must pass)
#    c. Commit (creates automatic checkpoint)
#    d. If tests fail: git reset --hard <previous commit>

# 4. If entire refactor fails:
git reset --hard checkpoint-before-auth-refactor-...

# 5. If successful:
git tag -d checkpoint-before-auth-refactor-...
```

---

## Troubleshooting

### Quality Gate Failing

**Problem**: Quality gate blocks commit with errors

**Solution**:
```bash
# 1. Read the full error output
# 2. Fix issues one by one
# 3. Re-run quality gate after each fix
# 4. DO NOT skip quality gate - fix the issues

# Common issues:
# - Tests failing: Fix test logic or implementation
# - Linting errors: Run `ruff check --fix`
# - Type errors: Add type hints, fix mismatches
# - Missing changelog: Update CHANGELOG.md
```

### Task Too Large

**Problem**: Task estimated >30 lines

**Solution**:
```bash
# 1. STOP - Don't implement yet
# 2. Break task into smaller sub-tasks
# 3. Update TASKS.md with sub-tasks
# 4. Implement smallest sub-task first
# 5. Test, commit, move to next sub-task

# Example breakdown:
# Large task: "Add user authentication"
# Sub-tasks:
# 1. Create user model (≤30 lines)
# 2. Add authentication endpoints (≤30 lines)
# 3. Create login UI component (≤30 lines)
# 4. Add authentication tests (≤30 lines)
```

### Context Window Full

**Problem**: Approaching context limit (60% threshold)

**Solution**:
```bash
# 1. Save session summary FIRST
/mcp__memory__session_end

# 2. Clear context
/clear

# 3. Start new session
/mcp__memory__session_start

# Prevention:
# - Use @filename instead of reading all files
# - Add large files to .claudeignore
# - Scope sessions to single features
# - Use /clear proactively at 60% capacity
```

### Task Alignment Score Low (<70)

**Problem**: Task doesn't serve project objective

**Solution**:
```bash
# Claude will show:
# "This task has low alignment (score: 45). Should we proceed anyway?"

# Options:
# 1. Skip task - Focus on objective-critical work
# 2. Refocus objective - Maybe objective needs updating
# 3. Proceed anyway - User explicitly overrides

# To check alignment manually:
mcp__project__validate_task_alignment
# Args: task_description="what you want to do"
```

### Skills Not Auto-Loading

**Problem**: Skill should load but doesn't

**Check**:
```bash
# 1. Verify trigger keywords in skill metadata
cat .claude/skills/[skill-name]/skill.md
# Look for: auto_load_triggers: keyword1, keyword2

# 2. Use trigger keywords in your messages
# Example: "I need to debug this error"
# Should auto-load: problem-solving skill

# 3. Load manually if needed
@.claude/skills/[skill-name]/skill.md
```

### Learning MCP Not Finding New Resources

**Problem**: Scan returns old/stale data

**Solution**:
```bash
# Learning MCP has hardcoded knowledge (as of 2025-11-14)
# To get live data:

# 1. Use WebFetch tool for real-time data
WebFetch: https://github.com/anthropics/skills

# 2. Update learning_mcp.py with new findings
# 3. Store learnings for future reference
mcp__learning__store_learning
```

---

## Key Principles

### 1. Planning Before Coding
**Always enter Planning Mode (Shift+Tab×2) for new features**. Ask clarifying questions FIRST, get plan approved, THEN implement.

### 2. Small Atomic Tasks
**Every task ≤30 lines of code, ≤15 minutes**. If larger, STOP and break down first.

### 3. Quality Gate is Non-Negotiable
**NEVER skip quality gate failures**. If it fails, fix the issues. Period.

### 4. Context Management at 60%
**Proactively manage context BEFORE hitting limits**. Use /clear, save state to files first.

### 5. MCP Tools Are Mandatory
**load_project_context at start, validate_task_alignment before work, run_quality_gate before commit, save_session_summary at end**. These are not optional.

### 6. Skills Load Progressively
**Metadata first (low token cost), details on demand**. Use trigger keywords to auto-load relevant skills.

### 7. Self-Learning Weekly
**Scan Anthropic resources regularly** to stay current with latest best practices.

### 8. Git Checkpoints Before Risk
**Create safety checkpoints before refactoring, experiments, or risky changes**. Fearless exploration with instant rollback.

---

## Getting Help

### Documentation Locations

**In this toolkit**:
- `.claude/best-practice.md` - Full project standards
- `.claude/TASKS.md` - Live task list
- `.claude/skills/README.md` - Skills system documentation
- `.claude/USER_GUIDE.md` - This guide

**In best-practice source**:
- `README.md` - Overview and installation
- `CHANGELOG.md` - Version history and changes
- `docs/` - Comprehensive documentation

### Command Reference

**Quick reference**:
```bash
# Session management
/mcp__memory__session_start      # Load context
/mcp__memory__session_end        # Save summary

# Quality checks
/mcp__quality__code_review       # Review code
/mcp__quality__pre_commit_check  # Pre-commit checklist

# Project management
/mcp__project__plan_feature      # Plan new feature
/mcp__project__daily_standup     # Review progress
/mcp__project__refocus           # Cut scope creep

# Learning system
/mcp__learning__update_toolkit   # Update with new skills
/mcp__learning__scan_all_resources  # Comprehensive scan

# Workflows
/plan [feature]        # Planning Mode
/tdd [feature]         # Test-driven development
/checkpoint [name]     # Git safety checkpoint
/debug [issue]         # Systematic debugging
```

---

## Version History

**v1.3.0** (2025-11-14)
- Added Learning MCP with comprehensive Anthropic resource scanning
- 9 MCP tools for self-learning (skills, cookbooks, quickstarts, org repos)
- 3 MCP prompts for guided learning workflows
- Complete catalog of Anthropic ecosystem (97 resources)

**v1.2.0** (2025-11-10)
- Skills-based architecture with progressive disclosure
- 9 toolkit skills (28.5KB total vs 49KB monolithic)
- Domain learning skill with knowledge base
- MCP prompts added (10 prompts across 3 servers)
- Local-only installation by default

**v1.1.0** (2025-11-10)
- Live task list (TASKS.md)
- Granular change tracking (≤30 lines per task)
- Quality gate enforcement

**v1.0.0** (2025-11-04)
- Initial release with 3 MCP servers
- 8 slash commands
- Retrofit tools

---

**Questions?** Check the documentation in `docs/` or review the source code in the best-practice repository.

**Ready to start?** Follow the [Daily Workflow](#daily-workflow) section to begin using the toolkit!
