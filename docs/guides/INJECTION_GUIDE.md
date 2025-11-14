# Best Practice Toolkit - Injection Guide

> **Complete guide to injecting toolkit into any project**

## Table of Contents

1. [Overview](#overview)
2. [Injection Process](#injection-process)
3. [Folder Structure Created](#folder-structure-created)
4. [Installation Modes](#installation-modes)
5. [How Projects Use the Toolkit](#how-projects-use-the-toolkit)
6. [Examples](#examples)
7. [Troubleshooting](#troubleshooting)

---

## Overview

### What is Injection?

**Injection** = Installing the best-practice toolkit into another project

**ONE command** installs complete system:
```bash
cd /path/to/your-project
/path/to/best-practice/retrofit-tools/smart_install.sh
```

**Time**: <2 minutes
**Risk**: Zero (creates safety checkpoint, no breaking changes)
**Result**: Project gets standards, skills, quality gates, MCP servers

---

## Injection Process

### Step-by-Step

```bash
# 1. Navigate to target project
cd /path/to/my-angular-app

# 2. Run smart installer
/path/to/best-practice/retrofit-tools/smart_install.sh

# What happens:
┌─────────────────────────────────────────────┐
│ 🔍 Analyzing project...                     │
│   - Checking git activity... 3 commits/30d  │
│   - Checking deployment configs... found    │
│   - Checking CI/CD... found                 │
│   - Checking production env... found        │
│                                              │
│ 🟡 PRODUCTION detected (score: 3/4)         │
│    • Low activity (3 commits/30d)           │
│    • Has deployment config                  │
│    • Has CI/CD                              │
│                                              │
│ Will install: LIGHT mode (safe, minimal)    │
├─────────────────────────────────────────────┤
│ Proceed? (Y/n): Y                           │
│                                              │
│ [1/5] Creating structure... ✅              │
│ [2/5] Organizing docs... ✅                 │
│ [3/5] Creating PROJECT_PLAN... ✅           │
│ [4/5] Installing toolkit files... ✅        │
│ [5/5] Verifying .claude/... ✅              │
│                                              │
│ ✅ Installation complete (LIGHT mode)       │
└─────────────────────────────────────────────┘
```

---

## Folder Structure Created

### DEFAULT: Local-Only Mode (Recommended)

**BEFORE injection**:
```
my-angular-app/
├── src/
├── README.md
├── package.json
└── angular.json
```

**AFTER injection** (Local-Only):
```
my-angular-app/
├── src/                          # Unchanged
├── .claude/                      # NEW - GITIGNORED (local only)
│   ├── best-practice.md         # Project standards (49KB)
│   ├── TASKS.md                 # Live task list
│   ├── USER_GUIDE.md            # 500+ line guide
│   ├── skills/                  # 10 skills (progressive disclosure)
│   │   ├── quality-standards.md
│   │   ├── tdd-workflow.md
│   │   ├── problem-solving.md
│   │   ├── git-workflow.md
│   │   ├── file-placement.md
│   │   ├── planning-mode.md
│   │   ├── mcp-usage.md
│   │   ├── context-management.md
│   │   ├── domain-learning.md
│   │   ├── README.md
│   │   └── template/            # For creating project-specific skills
│   ├── quality-gate/            # FULL mode only
│   │   └── check_quality.sh     # Quality enforcement script
│   └── mcp-servers/             # FULL mode only
│       ├── memory_mcp.py        # Persistent context
│       ├── quality_mcp.py       # Quality enforcement
│       ├── project_mcp.py       # Objective management
│       ├── learning_mcp.py      # Self-learning
│       └── README.md            # MCP documentation
├── docs/                         # NEW - Organized documentation
│   ├── design/                  # Architecture, design docs
│   ├── guides/                  # How-to guides, methodology
│   ├── analysis/                # Analysis, assessments
│   ├── references/              # Reference materials
│   └── notes/
│       └── PROJECT_PLAN.md      # ALWAYS CURRENT plan
├── tests/                        # FULL mode only
│   └── test_basic.py            # Test structure starter
├── README.md                     # Unchanged
├── CLAUDE.md                     # NEW - Root-level standards reference
├── package.json                  # Unchanged
└── angular.json                  # Unchanged
```

**Key Points**:
- **`.claude/` is GITIGNORED by default** (Claude Code does this automatically)
- **No git pollution** - toolkit stays local to each developer
- **Each developer can customize** their own toolkit
- **No merge conflicts** from toolkit updates

---

### COMMIT Mode (Optional)

**With `--commit` flag**:
```bash
cd my-project
/path/to/best-practice/retrofit-tools/smart_install.sh --commit
```

**Result**: Everything above PLUS:
- `.claude/` folder IS committed to git
- All team members get same toolkit
- Toolkit updates create git history

**Use when**: Team wants shared, versioned toolkit configuration

---

## Installation Modes

### Auto-Detection Logic

The installer **automatically detects** if project is production or development:

**Production Indicators** (each +1 point):
- Low commit activity (<5 commits/30 days)
- Deployment configs (Dockerfile, docker-compose.yml)
- CI/CD (.github/workflows, .gitlab-ci.yml, Jenkinsfile)
- Production env files (.env.production, config/production.yml)

**Score ≥2** → LIGHT mode
**Score <2** → FULL mode

### LIGHT Mode (Production-Safe)

**For**: Production projects, stable codebases, live applications
**Philosophy**: Non-breaking, minimal changes
**Risk**: Zero

**What Gets Installed**:
```
.claude/
├── best-practice.md          ✅ Standards document
├── TASKS.md                  ✅ Task tracking
├── USER_GUIDE.md             ✅ Toolkit guide
└── skills/                   ✅ 10 toolkit skills

docs/
└── notes/
    └── PROJECT_PLAN.md       ✅ Planning document

CLAUDE.md                     ✅ Root reference
```

**What's EXCLUDED** (to avoid disruption):
- ❌ Quality gate scripts (no enforcement)
- ❌ MCP servers (no automation)
- ❌ Test structure (don't change existing tests)

**Benefit**: Get standards & skills without changing project behavior

---

### FULL Mode (Complete Retrofit)

**For**: Development projects, new projects, experimental codebases
**Philosophy**: Complete best practices, full enforcement
**Risk**: Low (still creates safety checkpoint)

**What Gets Installed**:
```
Everything from LIGHT mode PLUS:

.claude/
├── quality-gate/
│   └── check_quality.sh      ✅ Quality enforcement
└── mcp-servers/
    ├── memory_mcp.py          ✅ Persistent context
    ├── quality_mcp.py         ✅ Quality checks
    ├── project_mcp.py         ✅ Objective management
    ├── learning_mcp.py        ✅ Self-learning
    └── README.md              ✅ MCP docs

tests/
└── test_basic.py              ✅ Test structure
```

**Benefit**: Complete best-practice system with enforcement

---

## How Projects Use the Toolkit

### 1. Automatic Discovery (Claude Code)

**Claude Code automatically reads**:
- `CLAUDE.md` (root-level standards reference)
- `.claude/best-practice.md` (full standards)
- `.claude/skills/` (loads relevant skills on-demand)
- `.claude/TASKS.md` (current task list)

**No manual action required** - Claude sees these files automatically

---

### 2. Daily Workflow

#### Session Start

```bash
# Developer opens Claude Code in project
cd /path/to/my-angular-app
code .

# Claude Code automatically:
# 1. Reads CLAUDE.md and .claude/best-practice.md
# 2. Loads relevant skills based on task
# 3. Sees current tasks in .claude/TASKS.md
```

**Developer asks**:
```
"What should I work on today?"
```

**Claude responds** (using injected standards):
```
Based on .claude/TASKS.md, your next task is:

[ ] Implement user profile validation (≤30 lines, ≤15 min)

Before starting:
1. I'll validate this task aligns with project objective (MCP)
2. Task size looks good (≤30 lines rule)
3. Let's break it into:
   - Add validation function (10 lines)
   - Add unit tests (15 lines)
   - Update TASKS.md when complete

Ready to start with TDD (Red-Green-Refactor)?
```

---

#### During Work

**Standards automatically enforced**:
```
User: "Add user profile form"

Claude: [Reads .claude/skills/file-placement.md]
"I'll create the form component in the correct location:

src/components/user-profile/
├── user-profile-form.component.ts    (logic)
├── user-profile-form.component.html  (template)
├── user-profile-form.component.css   (styles)
└── user-profile-form.component.spec.ts (tests)

Per file-placement rules:
✅ Components in src/components/
✅ Each component gets own folder
✅ Tests co-located with source
```

---

#### Before Commit (FULL mode)

**Quality gate enforcement**:
```bash
# Developer ready to commit
git add .

# FULL mode: Quality gate runs automatically
bash .claude/quality-gate/check_quality.sh

Running quality gate...
✅ All tests pass (15/15)
✅ No linting errors
✅ No type errors
✅ Structure compliant (≤5 root folders)
❌ CHANGELOG.md not updated

Quality gate: FAILED
Please update CHANGELOG.md before committing
```

**Developer fixes**:
```bash
# Update changelog
echo "- feat: Add user profile form" >> CHANGELOG.md

# Retry
bash .claude/quality-gate/check_quality.sh
✅ Quality gate: PASSED

# Now can commit
git commit -m "feat: add user profile form"
```

---

### 3. Skills System (Progressive Disclosure)

**Auto-loading based on context**:

| User asks...                    | Claude loads skill...     | Token cost |
|---------------------------------|---------------------------|------------|
| "How do I test this?"           | tdd-workflow.md           | ~3KB       |
| "Where should this file go?"    | file-placement.md         | ~2KB       |
| "Debug this error"              | problem-solving.md        | ~4KB       |
| "Plan new feature"              | planning-mode.md          | ~3KB       |
| "How to use MCP tools?"         | mcp-usage.md              | ~3KB       |

**vs loading entire CLAUDE.md**: 49KB every time

**Benefit**:
- 94% reduction in context usage
- Faster responses
- Load only what's needed

---

### 4. MCP Integration (FULL Mode)

**If MCP servers installed**:

```bash
# Developer uses MCP prompts
/mcp__project__plan_feature user authentication

# Claude (using Project MCP):
"Planning feature: user authentication

Loading project objective from .project_manager/project_data.json...

Objective: Build user management system
Clarity Score: 85/100

Breaking down into ≤30 line tasks:
1. Create user model (20 lines)
2. Add authentication service (25 lines)
3. Create login component (30 lines)
4. Add unit tests (25 lines each)

Validating alignment with objective...
✅ All tasks align (score: 85+)

Ready to start?"
```

---

### 5. Context Persistence

**Memory MCP saves session**:

```bash
# End of day
"Save session summary: Implemented user authentication,
decided to use JWT tokens, next: add password reset"

# Next day (new conversation)
"Load project context"

Claude: "Welcome back! Last session:
- Implemented: User authentication with JWT
- Decision: JWT tokens expire after 24 hours
- Next steps: Add password reset functionality
- Blockers: None

Ready to continue with password reset?"
```

---

## Examples

### Example 1: Angular App (Production)

**Project**: Live e-commerce app with 50k users

```bash
cd ~/projects/ecommerce-app

# Analyze detects: production
/path/to/best-practice/retrofit-tools/smart_install.sh

# Result: LIGHT mode
🟡 PRODUCTION detected
   • Low activity (2 commits/30d)
   • Has deployment config
   • Has CI/CD

Will install: LIGHT mode (safe)

[Installing...]

✅ Complete

Files added (GITIGNORED):
- .claude/best-practice.md
- .claude/skills/ (10 skills)
- .claude/USER_GUIDE.md
- docs/notes/PROJECT_PLAN.md
```

**Developer experience**:
- Standards available via CLAUDE.md
- Skills load on-demand
- No quality gate (safe, non-disruptive)
- PROJECT_PLAN.md for planning

---

### Example 2: New Python Project

**Project**: Brand new Flask API

```bash
cd ~/projects/flask-api

# Analyze detects: development
/path/to/best-practice/retrofit-tools/smart_install.sh

# Result: FULL mode
🟢 DEVELOPMENT detected
   • High activity (45 commits/30d)
   • No deployment config
   • No CI/CD

Will install: FULL mode (complete)

[Installing...]

✅ Complete

Files added (GITIGNORED):
- .claude/best-practice.md
- .claude/skills/ (10 skills)
- .claude/quality-gate/check_quality.sh
- .claude/mcp-servers/ (4 MCPs)
- tests/test_basic.py
- docs/notes/PROJECT_PLAN.md
```

**Developer experience**:
- Full standards + enforcement
- Quality gate blocks bad commits
- MCP servers for automation
- TDD workflow enforced
- Objective clarification required

---

### Example 3: Team Project (Commit Mode)

**Project**: Team of 5 developers

```bash
cd ~/projects/team-app

# Use --commit flag (team wants shared toolkit)
/path/to/best-practice/retrofit-tools/smart_install.sh --commit

# Result: Toolkit committed to git
Will install: FULL mode
Mode: COMMIT (files WILL be committed)

[Installing...]

✅ Complete + Committed

Git commit created:
- .claude/ folder tracked in git
- All team members get same standards
- Toolkit updates create git history
```

**Team experience**:
- Everyone has same standards
- No configuration drift
- Toolkit updates via git pull
- Can review toolkit changes in PRs

---

## Comparison: Before vs After

### Before Injection

**Problems**:
```
Developer: "Where should I put this file?"
Claude: [Guesses based on general knowledge]

Developer: "Is this tested enough?"
Claude: [No objective measure]

Developer: "What's the project objective?"
Claude: [No persistent memory]

Developer: "Should I commit this?"
Claude: [No quality gate]
```

---

### After Injection

**Solutions**:
```
Developer: "Where should I put this file?"
Claude: [Reads .claude/skills/file-placement.md]
"Per file placement rules, put it in:
src/components/feature-name/component.ts"

Developer: "Is this tested enough?"
Claude: [Runs quality gate]
"✅ 85% coverage (target: 80%)
✅ All tests pass
✅ Ready to commit"

Developer: "What's the project objective?"
Claude: [Loads from MCP]
"Problem: Users need fast checkout
Target: Mobile shoppers
Solution: One-click payment
Clarity: 85/100"

Developer: "Should I commit this?"
Claude: [Runs quality gate]
"❌ Quality gate failed:
- 2 linting errors
- CHANGELOG not updated
Fix these first"
```

---

## Folder Details

### `.claude/` Folder (Core Toolkit)

**Purpose**: Contains all toolkit files
**Location**: Project root
**Git**: GITIGNORED by default (Claude Code does this automatically)
**Size**: ~150KB (LIGHT) or ~400KB (FULL)

**Contents**:
```
.claude/
├── best-practice.md          # 49KB - Complete standards
├── TASKS.md                  # ~1KB - Live task list
├── USER_GUIDE.md             # ~35KB - Toolkit guide
├── skills/                   # ~26KB - 10 skills
│   ├── README.md             # Skills index
│   ├── quality-standards.md  # Quality rules
│   ├── tdd-workflow.md       # TDD cycle
│   ├── problem-solving.md    # 10 debugging techniques
│   ├── git-workflow.md       # Git best practices
│   ├── file-placement.md     # File organization
│   ├── planning-mode.md      # Planning workflow
│   ├── mcp-usage.md          # MCP tool usage
│   ├── context-management.md # Token optimization
│   ├── domain-learning.md    # Learning new domains
│   └── template/             # Create project skills
├── quality-gate/             # FULL mode only
│   └── check_quality.sh      # ~5KB - Quality enforcement
└── mcp-servers/              # FULL mode only (~170KB)
    ├── memory_mcp.py         # Context persistence
    ├── quality_mcp.py        # Quality automation
    ├── project_mcp.py        # Objective management
    ├── learning_mcp.py       # Self-learning
    └── README.md             # MCP documentation
```

---

### `docs/` Folder (Documentation)

**Purpose**: Organized documentation
**Location**: Project root
**Git**: COMMITTED (documentation should be versioned)

**Structure**:
```
docs/
├── design/                   # Architecture, design docs
│   └── [Moved design docs]
├── guides/                   # How-to guides
│   └── [Moved methodology docs]
├── analysis/                 # Analysis, assessments
│   └── [Moved analysis docs]
├── references/               # Reference materials
│   └── [External references]
└── notes/
    └── PROJECT_PLAN.md       # ALWAYS CURRENT project plan
```

**Auto-organization**:
- Installer moves root-level *.md files to appropriate folders
- README.md and CLAUDE.md stay in root
- Other .md files sorted by keyword matching

---

### `tests/` Folder (FULL Mode Only)

**Purpose**: Test suite
**Location**: Project root
**Git**: COMMITTED (tests should be versioned)

**Starter**:
```python
# tests/test_basic.py
import pytest

def test_placeholder():
    assert True
```

**Expanded** (developer adds):
```
tests/
├── test_basic.py
├── test_user_model.py
├── test_auth_service.py
├── test_api_endpoints.py
└── conftest.py           # Pytest configuration
```

---

## Git Behavior

### Default: Local-Only (Recommended)

**What happens**:
1. `.claude/` folder created
2. Claude Code automatically gitignores it
3. Toolkit files stay local
4. Each developer independent

**Git status**:
```bash
git status
# On branch main
# Changes not staged for commit:
#   modified:   docs/notes/PROJECT_PLAN.md

# (.claude/ not shown - automatically ignored)
```

**Benefits**:
- ✅ No git pollution
- ✅ No merge conflicts
- ✅ Each developer can customize
- ✅ Toolkit updates don't create git noise

---

### With --commit Flag

**What happens**:
1. `.claude/` folder created
2. All toolkit files staged
3. Git commit created
4. Toolkit tracked in repository

**Git status**:
```bash
git status
# On branch main
# Changes to be committed:
#   new file:   .claude/best-practice.md
#   new file:   .claude/skills/quality-standards.md
#   ...
```

**Benefits**:
- ✅ Shared team standards
- ✅ Versioned toolkit
- ✅ Reviewable in PRs
- ✅ No configuration drift

---

## Safety Features

### 1. Git Checkpoint

**Before any changes**:
```bash
git tag retrofit-start
```

**Rollback anytime**:
```bash
git reset --hard retrofit-start
git clean -fd
```

---

### 2. Non-Destructive

**Installer NEVER**:
- ❌ Deletes existing files
- ❌ Modifies source code
- ❌ Changes configuration files
- ❌ Alters build process

**Installer ONLY**:
- ✅ Creates new folders
- ✅ Moves documentation
- ✅ Adds toolkit files
- ✅ Updates PROJECT_PLAN.md

---

### 3. Validation

**After installation**:
```
📋 Installation Summary
✅ CLAUDE.md (49KB)
✅ .claude/best-practice.md (49KB)
✅ .claude/USER_GUIDE.md (35KB)
✅ .claude/TASKS.md (1KB)
✅ .claude/skills/ (10 files)
✅ docs/notes/PROJECT_PLAN.md (2KB)

[FULL mode only]
✅ .claude/quality-gate/check_quality.sh (5KB)
✅ .claude/mcp-servers/ (4 servers, 170KB)
✅ tests/test_basic.py (1KB)

Installation: SUCCESS
Errors: 0, Warnings: 0
```

---

## Troubleshooting

### "Installation failed - not a git repo"

**Solution**:
```bash
# Initialize git first
git init
git add .
git commit -m "Initial commit"

# Then install
/path/to/best-practice/retrofit-tools/smart_install.sh
```

---

### ".claude/ folder is committed to git"

**If you used --commit but didn't mean to**:
```bash
# Remove from git tracking (keep files)
git rm -r --cached .claude/
git commit -m "chore: untrack .claude/ folder"

# Claude Code will now automatically ignore it
```

---

### "Want to switch from LIGHT to FULL mode"

**Solution**:
```bash
# Rerun installer, override mode
/path/to/best-practice/retrofit-tools/smart_install.sh

# When prompted:
Override detected mode? (y/N): y
1) LIGHT - Production safe
2) FULL  - Complete retrofit
Choice: 2

# FULL mode components installed
```

---

### "Quality gate not found"

**Cause**: Installed in LIGHT mode
**Solution**: Reinstall in FULL mode (see above)

---

### "Skills not loading"

**Check**:
```bash
ls .claude/skills/
# Should show: quality-standards.md, tdd-workflow.md, etc.
```

**If missing**:
```bash
# Reinstall
/path/to/best-practice/retrofit-tools/smart_install.sh
```

---

## Summary

### What Gets Injected

**ALWAYS** (Both modes):
- ✅ CLAUDE.md (root reference)
- ✅ .claude/best-practice.md (standards)
- ✅ .claude/skills/ (10 skills)
- ✅ .claude/TASKS.md (task tracking)
- ✅ .claude/USER_GUIDE.md (guide)
- ✅ docs/notes/PROJECT_PLAN.md (planning)

**FULL mode adds**:
- ✅ .claude/quality-gate/ (enforcement)
- ✅ .claude/mcp-servers/ (automation)
- ✅ tests/ (test structure)

---

### How It Works

1. **Claude Code reads** CLAUDE.md and .claude/best-practice.md automatically
2. **Skills load on-demand** based on context (saves 94% tokens)
3. **MCP servers** (FULL mode) provide automation
4. **Quality gate** (FULL mode) enforces standards
5. **PROJECT_PLAN.md** stays current with objectives

---

### Git Behavior

**Default (local-only)**:
- .claude/ automatically gitignored
- No git pollution
- Each developer independent

**With --commit**:
- .claude/ tracked in git
- Team shares standards
- Toolkit versioned

---

### One Command

```bash
cd /path/to/project
/path/to/best-practice/retrofit-tools/smart_install.sh
```

**Time**: <2 minutes
**Risk**: Zero
**Result**: Production-ready best practices

---

**Last Updated**: 2025-11-14
**Related**: RETROFIT_METHODOLOGY.md, USER_GUIDE.md
