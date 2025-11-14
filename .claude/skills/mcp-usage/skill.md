---
name: MCP Usage
description: When and how to use Memory, Quality, and Project MCP tools
tags: mcp, tools, workflow, session, quality-gate
auto_load_triggers: mcp, session, quality gate, objective, alignment
priority: toolkit
---

# MCP Usage

## Purpose

Defines when and how to use the three MCP servers (Memory, Quality, Project) to enforce standards, maintain context, and ensure objective alignment.

---

## Session Start (ALWAYS)

**Before doing ANY work, call these tools in order**:

### 1. load_project_context
```
Call: mcp__memory__load_project_context
Args: project_path = current working directory
```

### 2. get_current_status
```
Call: mcp__project__get_current_status
Args: project_path = current working directory
```

**Output tells you**:
- Project objective and clarity score
- Tasks pending/in-progress/completed
- Decisions made in previous sessions
- Next steps

**NEVER skip these** - working without context leads to scope creep.

---

## Before Starting ANY Task (MANDATORY)

### 1. validate_task_alignment
```
Call: mcp__project__validate_task_alignment
Args:
  project_path = current working directory
  task_description = what you're about to do
```

**Interpret results**:
- **Alignment score ≥70**: Task is aligned, proceed
- **Alignment score <70**: Task does NOT serve objective
  - STOP immediately
  - Ask user for confirmation

### 2. validate_task_size
```
Call: mcp__project__validate_task_size
Args: task_description = what you're about to do
```

- If task is too large (>30 lines), break it down BEFORE implementing

---

## Before Completing ANY Task (MANDATORY)

### run_quality_gate
```
Call: mcp__quality__run_quality_gate
Args:
  project_path = current working directory
  changes_made = list of files modified
```

**Interpret results**:
- **PASS**: All checks passed → Proceed to commit
- **FAIL**: Quality issues detected
  - DO NOT commit
  - DO NOT mark task complete
  - Fix issues one by one
  - Re-run quality gate
  - Repeat until PASS

**NEVER override quality gate failure**.

---

## Session End (ALWAYS)

### save_session_summary
```
Call: mcp__memory__save_session_summary
Args:
  project_path = current working directory
  summary = brief overview of what was accomplished
  decisions = list of key decisions made
  next_steps = list of what to do next session
  blockers = list of current blockers (if any)
```

**Example**:
```
Summary: "Implemented user authentication with JWT tokens"
Decisions: [
  "Using bcrypt for password hashing",
  "JWT tokens expire after 24 hours"
]
Next steps: [
  "Add password reset functionality",
  "Implement email verification"
]
Blockers: []
```

---

## Complete MCP Tool Reference

### Memory MCP Tools
- `list_projects` - See all tracked projects
- `load_project_context` - **MANDATORY at session start**
- `save_session_summary` - **MANDATORY at session end**
- `save_decision` - Save architectural/technical decisions
- `search_memory` - Search across all projects
- `load_project_objective` - Load objective details
- `save_project_objective` - Save objective (used by Project MCP)

### Quality MCP Tools
- `run_quality_gate` - **MANDATORY before task completion**
- `check_code_quality` - Check specific files
- `audit_project_structure` - Validate minimal root compliance
- `validate_file_placement` - Check files in correct locations
- `find_obsolete_files` - Detect unused code
- `verify_standards` - Comprehensive standards check
- `update_documentation` - Update README with changes
- `update_changelog` - Add changelog entry
- `add_missing_docstrings` - Generate docstrings

### Project MCP Tools
- `get_current_status` - **MANDATORY at session start**
- `validate_task_alignment` - **MANDATORY before starting task**
- `validate_task_size` - Check if task is small enough
- `clarify_project_objective` - Define objective (new projects)
- `score_objective_clarity` - Check objective clarity
- `define_project_objective` - Finalize objective
- `create_task_breakdown` - Break project into tasks
- `challenge_task_priority` - Verify working on highest priority
- `mark_task_complete` - Mark task done (requires quality gate PASS)
- `identify_scope_creep` - Find non-essential tasks
- `refocus_on_objective` - Cut tasks that don't serve objective
- `sync_plan_to_reality` - Update plan to match actual state

---

## Workflow Integration

**Complete session workflow**:
```
1. Session Start
   - load_project_context
   - get_current_status

2. For each task:
   - validate_task_alignment
   - validate_task_size (if needed)
   - Implement (≤30 lines)
   - run_quality_gate
   - Commit if PASS

3. Session End
   - save_session_summary
```

---

## Enforcement Rules

**AI assistants MUST**:
1. Call `load_project_context` + `get_current_status` at session start
2. Call `validate_task_alignment` before implementing anything
3. Call `run_quality_gate` before marking tasks complete
4. Call `save_session_summary` at session end
5. NEVER skip quality gate failures
6. NEVER implement tasks with alignment score <70 without user confirmation

---

## Resources

- **CLAUDE.md**: Full MCP usage section (MANDATORY MCP Usage)
- **Memory MCP**: mcp-servers/memory_mcp.py
- **Quality MCP**: mcp-servers/quality_mcp.py
- **Project MCP**: mcp-servers/project_mcp.py
