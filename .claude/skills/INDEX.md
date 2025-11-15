# Skills Auto-Loading Index

> **Smart skill discovery**: Skills automatically suggest themselves based on context

---

## How Auto-Loading Works

Claude Code can automatically load relevant skills based on:
- **Error patterns** - Detecting failures or exceptions in output
- **File patterns** - Files being created or edited
- **Command patterns** - Git commands, test runs, etc.
- **Task keywords** - Keywords in TASKS.md or conversation
- **Context state** - Context usage, session events, etc.

---

## Skill Catalog & Auto-Load Triggers

### 🧠 problem-solving
**Purpose**: Systematic debugging and problem-solving (10 mandatory techniques)

**Auto-loads when**:
- Error patterns: `FAILED`, `Error:`, `Exception`, `Traceback`
- Task keywords: `debug`, `fix`, `error`, `bug`, `stuck`, `troubleshoot`
- File patterns: `tests/test_*.py`
- Command patterns: `git bisect`, `git reset`

**Use for**:
- Test failures
- Unexpected errors
- Debugging issues >5 minutes
- Logic errors or mysterious bugs

---

### ✅ tdd-workflow
**Purpose**: Test-Driven Development (Red-Green-Refactor cycle)

**Auto-loads when**:
- File patterns: `test_*.py`, `*.test.js`, `*_test.go`
- Task keywords: `test`, `tdd`, `red-green`, `failing test`
- Command patterns: `pytest`, `npm test`, `go test`
- Context: Creating new features or functions

**Use for**:
- Writing new features
- Adding test coverage
- Refactoring code
- Ensuring code quality

---

### 📋 quality-standards
**Purpose**: Code quality requirements and enforcement

**Auto-loads when**:
- Command patterns: `git commit`, `quality gate`, `pre-commit`
- Task keywords: `quality`, `lint`, `coverage`, `standards`
- Error patterns: `linting error`, `type error`, `coverage`
- Context: Before commits, during code review

**Use for**:
- Pre-commit checks
- Code review preparation
- Setting up quality tools
- Understanding requirements

---

### 🔀 git-workflow
**Purpose**: Git operations, commits, branches, checkpoints

**Auto-loads when**:
- Command patterns: `git commit`, `git push`, `git merge`, `git rebase`
- Task keywords: `commit`, `merge`, `branch`, `checkpoint`, `pr`
- Error patterns: `merge conflict`, `diverged branches`
- Context: Git operations or PR creation

**Use for**:
- Committing changes
- Creating pull requests
- Handling merge conflicts
- Creating checkpoints

---

### 📁 file-placement
**Purpose**: Where files belong in project structure

**Auto-loads when**:
- Command patterns: `mkdir`, `touch`, creating new files
- Task keywords: `create file`, `new directory`, `file structure`
- File patterns: New file creation in root
- Context: Project structure questions

**Use for**:
- Creating new files/folders
- Understanding project structure
- Maintaining minimal root
- Organizing documentation

---

### 🎯 planning-mode
**Purpose**: Feature planning and requirement discovery

**Auto-loads when**:
- Task keywords: `new feature`, `plan`, `architecture`, `design`, `refactor`
- Context: Large tasks >30 lines, unclear requirements
- Command patterns: `/plan`, `/spec`
- File patterns: Creating multiple new files

**Use for**:
- Planning new features
- Architectural decisions
- Breaking down large tasks
- Requirements clarification

---

### ⚡ mcp-usage
**Purpose**: MCP tool usage and workflows

**Auto-loads when**:
- Context: Session start, session end
- Task keywords: `mcp`, `objective`, `quality gate`, `context`
- Command patterns: `mcp__*` tool calls
- Context: Every session automatically

**Use for**:
- Session initialization
- Project objective setup
- Quality gate enforcement
- Saving session summaries

---

### 🧠 context-management
**Purpose**: Managing Claude's context window effectively

**Auto-loads when**:
- Context: Usage >60% of context window
- Task keywords: `context`, `compact`, `clear`, `memory`
- Error patterns: `approaching usage limit`
- Context: Large file reads, many tool calls

**Use for**:
- Avoiding context limits
- Managing large codebases
- Progressive disclosure
- External memory strategies

---

### 📚 domain-learning
**Purpose**: Learning new domains, technologies, frameworks

**Auto-loads when**:
- Task keywords: `learn`, `understand`, `how does`, `explain`
- File patterns: Scanning unfamiliar codebases
- Context: Exploring new projects
- Command patterns: Documentation searches

**Use for**:
- Understanding new codebases
- Learning frameworks
- Exploring architectures
- Building mental models

---

## Usage Examples

### Example 1: Test Failure
```
User: "The tests are failing with KeyError"

Auto-loads: problem-solving
→ Applies systematic debugging (State Inspection, Rubber Duck)
→ References: .claude/skills/problem-solving/skill.md
```

### Example 2: Creating New Feature
```
User: "Add user authentication system"

Auto-loads: planning-mode, tdd-workflow
→ Asks clarifying questions
→ Creates implementation plan
→ Suggests TDD approach
→ References: .claude/skills/planning-mode/skill.md
```

### Example 3: Before Commit
```
User: "git commit -m 'feat: add login'"

Auto-loads: quality-standards, git-workflow
→ Runs quality gate
→ Validates commit message format
→ Checks test coverage
→ References: .claude/skills/quality-standards/skill.md
```

### Example 4: Context Warning
```
System: "Approaching usage limit (62%)"

Auto-loads: context-management
→ Suggests using /clear or /compact
→ Recommends saving state to files
→ References: .claude/skills/context-management/skill.md
```

---

## Manual Skill Loading

You can also manually load skills:

```bash
# In Claude Code, reference a skill
@.claude/skills/problem-solving/skill.md

# Or view directly
cat .claude/skills/problem-solving/skill.md

# List all skills
ls .claude/skills/
```

---

## Creating Custom Skills

Use the template to create project-specific skills:

```bash
# Copy template
cp .claude/skills/template/skill.md .claude/skills/my-skill/skill.md

# Edit metadata for auto-loading
vi .claude/skills/my-skill/skill.md
```

Add `auto_load_triggers` to frontmatter:
```yaml
---
name: My Custom Skill
description: Project-specific patterns
auto_load_triggers: keyword1, keyword2, pattern
priority: project
---
```

---

## Skill Priority

When multiple skills match:
1. **Project skills** (priority: project) - Load first
2. **Toolkit skills** (priority: toolkit) - Universal best practices

Custom skills in your project override toolkit defaults.

---

## Benefits of Auto-Loading

✅ **Discoverability** - Learn which skills exist
✅ **Context-aware** - Right skill at right time
✅ **Progressive disclosure** - Only load what's needed
✅ **Reduced cognitive load** - No need to remember all skills
✅ **Maximum effectiveness** - Features actually used

---

**Last Updated**: 2025-11-15
**Skill Count**: 9 toolkit skills + unlimited project skills
