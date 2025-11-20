# Project Standards - Best Practice Toolkit

> **Purpose**: Enforce changelog, comments, minimal structure - maximum efficiency
> **Last Updated**: 2025-11-20 (v2.0 - Systems Analyst Edition)
> **Applies To**: Claude Code and all AI assistants working on this codebase

---

## 🎯 Core Objective

**Enforce**: Changelog for every change + Well-commented code + Minimal structure
**Focus**: Speed and frugality - no bloat
**No**: Unsolicited reports, verbose docs, or folder sprawl

---

## 🎯 Pre-Flight Setup (Project-Level Rules)

> **The game-changer**: Define boundaries BEFORE coding to prevent Claude from making random decisions

**MANDATORY: Every project MUST define in CLAUDE.md:**

### 📋 Project Documentation Template

```markdown
# PROJECT OVERVIEW
[What this system does in 2-3 sentences]

# TECH STACK (Don't change without approval)
- Backend: [Python/Flask, Node/Express, etc.]
- Frontend: [Angular, React, Vue, etc.]
- Database: [PostgreSQL, MySQL, MongoDB, etc.]
- Hosting: [AWS, Azure, etc.]

# DATABASE SCHEMA
[Paste ERD or table definitions]
- users: id, email, name, created_at
- projects: id, user_id, title, status
- tasks: id, project_id, title, due_date

# BUSINESS RULES
1. Users can only see their own data
2. Required field validation rules
3. Status transitions allowed
4. Data constraints (dates, amounts, etc.)

# ARCHITECTURE RULES
- All database queries through repository pattern
- No raw SQL in routes/controllers
- All dates stored as UTC
- All money stored as integers (cents/pennies)
- [Add your patterns here]

# FILE ORGANIZATION
/backend
  /models        <- Database models only
  /repositories  <- All DB queries here
  /routes        <- API endpoints only
  /services      <- Business logic only

/frontend
  /components    <- Reusable UI pieces
  /pages         <- Full pages
  /services      <- API calls only

# NAMING CONVENTIONS
- Functions: snake_case (get_user_projects)
- Classes: PascalCase (ProjectRepository)
- Variables: snake_case (user_id)
- Database tables: plural (users, projects)
- API endpoints: /api/v1/resource-name

# THINGS CLAUDE MUST NEVER DO
- ❌ Add new packages without asking
- ❌ Change database schema without approval
- ❌ Modify authentication logic
- ❌ Change existing API contracts
- ❌ Invent new patterns - use existing only
- ❌ Touch files outside specified scope
```

**Why this matters:**
- Claude follows rules across sessions → stops random decisions
- Boundaries defined = better autonomous performance
- Less course-correction, more coding time

**Enforcement:**
- ALWAYS read project CLAUDE.md at session start (via MCP context load)
- NEVER create new patterns when existing ones work
- ALWAYS ask if constraints unclear

---

## ✅ BEFORE EVERY CHANGE - Your Checklist

> **CRITICAL**: Run through this checklist BEFORE starting ANY work

### 📋 Session Start (First Thing)
```
□ Load project context: mcp__memory__load_project_context
□ Get current status: mcp__project__get_current_status
□ Read project CLAUDE.md for rules/patterns
□ Check .claude/TASKS.md for current tasks
```

### 📋 Before Planning/Discussion
```
□ DO NOT jump to code
□ Understand: What? Why? Edge cases? Constraints?
□ Ask clarifying questions first
□ Identify existing patterns to follow
```

### 📋 Before Starting Any Task
```
□ Validate alignment: mcp__project__validate_task_alignment (≥70 score)
□ Validate size: mcp__project__validate_task_size (≤30 lines)
□ Create step-by-step plan (Phase 1)
□ Break into 3-5 small chunks
□ Get explicit user approval
□ Document plan in .claude/TASKS.md
```

### 📋 Task Constraints (Define These)
```
□ Existing pattern to follow: _____________
□ Files to touch ONLY: _____________
□ Dependencies allowed: _____________
□ Scope boundaries: _____________
□ Commit checkpoints: After tests, structure, implementation, fixes
```

### 📋 Before Implementation (Each Chunk)
```
□ Create GitHub issue (if pushing to GitHub)
□ Create feature branch
□ Write failing tests FIRST
□ Confirm tests FAIL
□ Commit: "test: add failing tests for X"
```

### 📋 During Implementation
```
□ Implement ≤30 lines only
□ Run tests after each change
□ Commit granularly (tests → structure → implementation → fixes)
□ Stay within file boundaries
□ NO refactoring yet (wait for Phase 4)
□ NO scope expansion
□ NO new dependencies without approval
```

### 📋 Before Completing Task
```
□ All tests passing
□ Feature stable and working
□ Run quality gate: mcp__quality__run_quality_gate
□ Quality gate PASS (if FAIL → fix → rerun)
□ Mark task complete: mcp__project__mark_task_complete
□ Update .claude/TASKS.md
```

### 📋 Before Creating PR
```
□ All tests pass locally
□ Linting/formatting applied
□ Commit references issue (#123)
□ Branch pushed to remote
□ PR description: What, Why, How to test
□ Screenshots (if UI changes)
```

### 📋 Session End
```
□ Save session summary: mcp__memory__save_session_summary
□ Update .claude/TASKS.md with next steps
□ Commit any pending changes
```

---

**Quick Reference Card:**
```
NEVER:
❌ Jump to code without plan
❌ Implement >30 lines without checkpoint
❌ Refactor before stable
❌ Add dependencies without asking
❌ Touch files outside scope
❌ Skip quality gate

ALWAYS:
✅ Discuss first, code second
✅ Break large tasks down
✅ Write tests first, see them fail
✅ Commit granularly
✅ Use existing patterns
✅ Ask when uncertain
```

---

## 📝 How to Communicate Requirements (For Non-Coders)

> **Think like a systems analyst, not a programmer**

### ❌ Don't Say:
```
"Add a feature to track time"
"Make it look better"
"Fix the login"
```

### ✅ Instead, Specify:

**Format:**
```markdown
TASK: [Feature name]

DATABASE CHANGES NEEDED:
- New table: time_entries
  - id (primary key)
  - task_id (foreign key → tasks)
  - user_id (foreign key → users)
  - start_time (timestamp)
  - end_time (timestamp, nullable)
  - duration_minutes (integer, calculated)
  - notes (text, optional)

BUSINESS RULES:
- Only one active timer per user at a time
- Can't start timer if one already running
- End time must be after start time
- Duration auto-calculated when timer stops
- Only user who started can stop their timer

API ENDPOINTS NEEDED:
- POST /api/v1/time-entries/start (task_id)
- POST /api/v1/time-entries/stop (entry_id)
- GET /api/v1/time-entries (filter by task_id or date range)

UI REQUIREMENTS:
- Timer widget on task detail page
- Shows current running time if active
- "Start/Stop" button
- List of past entries below

EDGE CASES TO HANDLE:
- What if user closes browser with timer running?
- What if task deleted with active timer?
- Timezone handling (store UTC, display user's TZ)

CONSTRAINTS:
- Use existing pattern: [specify file/pattern]
- Touch only: [list files]
- No new dependencies
- Scope: Timer only, not reporting yet
```

### Your Strengths (Leverage These):
- ✅ **Database design** - You understand data relationships
- ✅ **Business logic** - You know how the system should work
- ✅ **Data flow** - You understand the process
- ✅ **Edge cases** - You think through scenarios

### Let Claude Handle:
- ❌ Syntax (Python/JavaScript/TypeScript)
- ❌ Framework patterns (Flask/Angular/React)
- ❌ Package management
- ❌ Modern tooling

**You're the architect, Claude is the carpenter.**

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

## 🎯 The Autonomous Coding Flow (5 Phases)

> **CRITICAL**: Follow this sequence religiously to prevent drift and random decisions

### **Phase 1: Plan Before Code** ⚠️ MANDATORY

**❌ NEVER let Claude jump straight to code**

**Required steps:**
1. **Discuss the problem** - Understand context, constraints, edge cases
2. **Request step-by-step plan** - Tighten logic, surface unknowns
3. **Get explicit approval** - Most mistakes disappear here
4. **Break into 3-5 small chunks** - Each ≤30 lines, laser-focused

**Enforcement:**
- If requirements unclear → ASK, don't assume
- If no plan exists → STOP, create plan first
- If user hasn't approved → WAIT, don't start coding
- If chunks feel large → BREAK DOWN smaller

**Planning Mode (Shift+Tab×2) is NON-NEGOTIABLE for:**
- New features or functionality
- Significant refactoring (>30 lines)
- Complex bug fixes requiring multiple files
- Architecture changes
- Unclear requirements

**Plans must include:**
- Tasks (each ≤30 lines)
- Acceptance criteria
- File changes (explicit list)
- Tests to write
- User approval checkpoint

**See** `.claude/skills/planning-mode/` for detailed workflow

---

### **Phase 2: Test-Driven Cycle** 🔁 MANDATORY

> **Red-Green-Refactor with granular commits**

**FOR EACH CHUNK (≤30 lines):**

```
1. Write failing tests first      → git commit "test: add failing tests for X"
2. Confirm tests FAIL              → verify red state
3. Write skeleton/structure        → git commit "feat: add structure for X"
4. Add minimal implementation      → git commit "feat: implement X logic"
5. Run tests                       → check results
6. Fix what breaks                 → git commit "fix: resolve X error"
7. LOOP until tests pass           → repeat steps 5-6
8. Tests pass & feature stable     → git commit "feat: complete X functionality"
9. Refactor ONLY if working        → git commit "refactor: optimize X"
```

**Granular commit philosophy:**
- Commit after EVERY meaningful step (not just at end)
- Each commit is a checkpoint (easy rollback)
- Commit messages tell the story
- Small commits = easy debugging

**Visual feedback loop:**
- Run tests in terminal/browser after each change
- See immediate results
- Fix → Test → Fix → Test until stable

**NEVER:**
- Skip seeing tests fail first (you might write passing tests by accident)
- Refactor before tests pass (Claude invents features)
- Make >30 lines changes without checkpoint

**See** `.claude/skills/tdd-workflow/` for detailed cycle

---

### **Phase 3: Autonomous Mode** 🤖 (Lazy Mode)

> **Let Claude work unattended for heavy lifting**

**When to use:**
- Repetitive file changes (e.g., updating 20 components)
- Long-running test-fix cycles
- Comprehensive refactoring (after feature works)

**Setup:**
```bash
# Tell Claude:
"Use tests to verify, loop until complete and functioning.
Commit after each fix. Notify me when done or blocked."
```

**Monitoring:**
- Set up notification hook for human input needed
- Let Claude run 20-30 minutes unattended
- Check completed work in git log

**Boundaries for autonomous mode:**
- Clear success criteria defined
- Tests written and passing baseline
- No architectural decisions required
- File scope pre-defined

**Safety:**
- Frequent commits = easy rollback
- Quality gate still required before completion
- User reviews final result

---

### **Phase 4: Polish** ✨

> **Refactor ONLY after everything works**

**CRITICAL RULE**: NEVER refactor before feature is stable

**Why:**
- Refactoring unstable code → Claude invents features
- Working code first → safe to optimize
- Tests passing → refactor with confidence

**Refactoring checklist:**
- ✅ All tests passing
- ✅ Feature complete and stable
- ✅ User has tested functionality
- ❌ Don't refactor during implementation

**Allowed refactors:**
- Extract repeated code into functions
- Improve naming for clarity
- Optimize performance (with profiling data)
- Simplify complex logic

**Claude's refactors are "honestly great" once feature is solid**

---

### **Phase 5: Ship** 🚀

1. Push branch
2. Create PR with descriptive summary
3. Request review (if team project)
4. Merge after approval
5. Delete feature branch
6. Done ✅

---

## 🔍 User Quality Review (Non-Technical)

> **Review as a systems analyst, not a programmer**

After Claude completes work, review **logic and requirements**, not syntax:

### Your Review Checklist:
```
□ Does it match my requirements document?
□ Did it follow the database schema I specified?
□ Are business rules enforced correctly?
□ Does the API match what I asked for?
□ Can I trace the data flow? (DB → Repository → Service → Route → Frontend)
□ Did it touch ONLY the files I specified?
□ Did it use existing patterns (no new inventions)?
```

### Testing Without Coding:

**Walk through scenarios:**
```
You: "Walk me through what happens when user clicks 'Start Timer'"

Claude explains:
1. Frontend calls POST /api/v1/time-entries/start
2. Route validates user authenticated
3. Service checks if user already has running timer
4. If not, creates new time_entry record
5. Returns entry with start_time
6. Frontend updates UI

You: "What if they already have a timer running?"

Claude: Service returns error 400 "Timer already active"
         Frontend shows error message
         No database write occurs
```

**You're testing the LOGIC, not the SYNTAX.**

### Signs Claude Went Rogue:
- "I've added a helpful utility library..."
- "I've refactored the authentication..."
- "I've improved the database structure..."
- Files changed you didn't expect

### Recovery:
```
You: "Stop. Show me git diff of changes."
[Review]
You: "Revert the authentication changes.
     Stick to ONLY time tracking feature.
     Use existing patterns."
```

---

## 📦 Build in Vertical Slices

> **Complete features incrementally, not horizontally**

### ❌ Don't Build Horizontally:
```
Week 1: All database models
Week 2: All repositories
Week 3: All services
Week 4: All routes
Week 5: All frontend
```
**Problem:** Nothing works until week 5

### ✅ Build Vertical Slices:
```
Week 1: Basic timer (start/stop only)
        ├─ Database: time_entries table
        ├─ Repository: start(), stop()
        ├─ Service: validate, create
        ├─ Route: POST /start, /stop
        └─ Frontend: Start/Stop button
        ✅ WORKS END-TO-END

Week 2: Timer history list
        ├─ Repository: get_entries()
        ├─ Route: GET /time-entries
        └─ Frontend: History table
        ✅ WORKS END-TO-END

Week 3: Reporting/analytics
Week 4: Export functionality
```

**Each slice is COMPLETE** (database → backend → frontend → tests)

**Benefits:**
- ✅ Working feature every week
- ✅ Can test immediately
- ✅ Easy to rollback one slice
- ✅ User can give feedback early
- ✅ Claude stays on-rails (scope is clear)

---

## ⚠️ Critical Constraints (ALWAYS Provide)

> **Explicit boundaries = way better performance**

**MANDATORY: Always specify these constraints when assigning work:**

### 1. **Use Existing Patterns** 🎯
```
✅ "Follow the existing MVC pattern in src/"
✅ "Use the same component structure as UserProfile.tsx"
✅ "Match the API service pattern in src/services/"

❌ Don't let Claude invent new patterns
```

**Enforcement:**
- If pattern exists → USE IT, don't create new
- If uncertain → ASK which pattern to follow
- NEVER create abstractions for one-off use

---

### 2. **Touch Only These Files** 📁
```
✅ "Modify ONLY: src/auth/login.ts, src/components/LoginForm.tsx"
✅ "Don't touch any other files unless absolutely necessary"

❌ Don't let Claude wander into other files
```

**Enforcement:**
- Explicit file list = focused work
- If other files needed → ASK first
- Scope creep = primary failure mode

---

### 3. **No New Dependencies** 🚫
```
✅ "Use existing libraries (lodash, axios)"
✅ "No new npm packages without approval"

❌ Don't let Claude add dependencies freely
```

**Enforcement:**
- If new dependency needed → ASK with justification
- Check package.json before adding
- Prefer standard library or existing deps

---

### 4. **Checkpoint Frequently** 💾
```
✅ Commit after every meaningful change
✅ Use git tags before risky refactors
✅ Claude auto-saves before edits (Esc×2 to rollback)

❌ Don't make large changes without checkpoints
```

**Enforcement:**
- Commit granularly (see Phase 2)
- Use `/checkpoint` before risky work
- NEVER batch 50+ line changes

---

### 5. **Scope Boundaries** 📦
```
✅ "Implement only the login form, not password reset"
✅ "Fix this specific bug, don't refactor surrounding code"
✅ "Add tests for this function only"

❌ Don't let scope expand
```

**Enforcement:**
- If task expands → STOP, ask if in scope
- "While we're here..." = scope creep
- Finish one thing before adding "improvements"

---

**Example Task with Constraints:**
```
Task: Add user login functionality

Constraints:
- Use existing pattern: src/auth/register.ts
- Touch only: src/auth/login.ts, src/components/LoginForm.tsx
- No new dependencies (use existing JWT library)
- Scope: Login only, not password reset or 2FA
- Commit after: tests, structure, implementation, fixes
```

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

# 5. Commit with clear, atomic messages
# Simple format (small changes):
git commit -m "feat: implement user login (closes #42)"

# Detailed format (larger changes):
git commit -m "feat: add user authentication (closes #42)

- Implement JWT token generation
- Add login endpoint with validation
- Create user session management
- Add error handling for invalid credentials"

# 6. Push branch
git push -u origin feature/feature-x-#42

# 7. Create PR
gh pr create --title "feat: Add user authentication (closes #42)"
```

**When to create issue**:
- ✅ New features, bug fixes, refactoring, performance, security
- ❌ Documentation-only, local experiments, trivial changes

**Enforcement**:
- ❌ DO NOT start coding without issue
- ❌ DO NOT commit without referencing issue
- ✅ ALWAYS: issue → branch → code → commit → PR

---

### Branching Strategy

**Keep `main` protected**:
- Never commit directly to main
- Always work in feature branches
- Merge only via pull requests

**Branch naming convention**:
```
feature/issue-{number}-{short-description}
bugfix/issue-{number}-{short-description}
refactor/issue-{number}-{short-description}
```

**Branch from latest main**:
```bash
git checkout main
git pull origin main
git checkout -b feature/issue-123-user-authentication
```

**One issue per branch**:
- Create new branch for each issue
- Keep branches focused and short-lived
- Delete branch after PR merge

---

### Pull Request Workflow

**Create descriptive PRs** - Include:
- **What**: Summary of changes made
- **Why**: Reason/motivation for changes
- **How to test**: Steps to verify the changes work
- **Screenshots/videos**: For UI changes (Angular, React, etc.)
- **Link to issue**: Use "Closes #123" or "Fixes #123"

**Example PR description**:
```markdown
## Summary
Implements user authentication with JWT tokens (Closes #123)

## Changes Made
- Add JWT token generation
- Create login endpoint
- Implement session management

## How to Test
1. Start server: `npm start`
2. Navigate to /login
3. Enter credentials: test@example.com / password123
4. Verify redirect to dashboard

## Screenshots
[Attach screenshots of login flow]
```

**PR best practices**:
- Request at least one review (team projects)
- Keep PRs small and focused (<400 lines changed)
- Respond to review comments promptly
- Don't merge your own PRs without review

---

### Code Quality - Language-Specific

**Python Projects**:
```bash
# Linting
flake8 . --max-line-length=100
# or
pylint src/
# or
ruff check .

# Formatting
black .

# Type checking
mypy src/

# Update dependencies
pip freeze > requirements.txt
# or update pyproject.toml
```

**Requirements**:
- Use type hints where appropriate
- Follow PEP 8 style guide
- Document all public functions/classes
- Keep functions ≤30 lines

**Angular Projects**:
```bash
# Linting
ng lint

# Tests
ng test
ng e2e

# Build check
ng build --configuration production
```

**Requirements**:
- Follow Angular style guide
- Component/service/module naming conventions
- Properly test components with TestBed
- Update package.json dependencies when needed
- Keep components focused (Single Responsibility)

**Universal Requirements** (all languages):
- ≥80% test coverage
- Zero linting errors
- Zero type errors
- Zero security vulnerabilities
- Documented public APIs

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

> **CRITICAL**: These are the top failure modes that destroy autonomous coding

### ❌ #1 Failure Mode: Letting Claude Dive Into Code Too Fast

**The problem:**
- Claude jumps straight to implementation without understanding
- Skips planning, discussion, edge cases
- Makes assumptions instead of asking

**The fix:**
- ✅ ALWAYS discuss problem first (Phase 1)
- ✅ Create step-by-step plan before coding
- ✅ Get explicit approval before implementation
- ✅ Break into small chunks (≤30 lines)

**Enforcement:**
- If no plan exists → STOP, ask questions
- If requirements unclear → ASK, don't assume
- If user hasn't approved → WAIT

---

### ❌ #2 Failure Mode: Scope Too Big (Claude Wanders)

**The problem:**
- Tasks >30 lines → Claude invents features
- No file boundaries → touches unnecessary files
- No constraints → adds dependencies freely
- "While we're here..." → scope creep

**The fix:**
- ✅ Tasks ≤30 lines, break down larger
- ✅ Explicit file list: "Touch ONLY these files"
- ✅ No new dependencies without approval
- ✅ Scope boundaries: "Login only, not password reset"

**Enforcement:**
- If task feels large → STOP, break down
- If scope expands → ASK if in scope
- If new files needed → ASK first

---

### ❌ #3 Failure Mode: Refactoring Before Stability (Claude Invents)

**The problem:**
- Refactoring unstable code → Claude invents features
- "Improving" while implementing → breaks tests
- Optimizing before working → premature abstraction

**The fix:**
- ✅ Implement first, refactor after (Phase 4)
- ✅ All tests passing before refactoring
- ✅ Feature stable and user-tested first
- ✅ One thing at a time

**Enforcement:**
- If code not working → NO refactoring
- If tests not passing → NO optimization
- If feature incomplete → NO "improvements"

---

### Prohibited Implementation
**NEVER**:
- Incomplete implementations or placeholders
- Mock functions or TODO comments
- Skip error handling or edge cases
- Refactor during initial implementation
- Make >30 line changes without checkpoint

### Prohibited Communication
**NEVER**:
- Social validation ("You're absolutely right!")
- Hedging language ("might," "could")
- Over-apologizing

### Technical Mistakes
**NEVER**:
- Skip compiling before tests
- Write tests expecting pass without seeing fail
- Leave old code when rewriting
- Add dependencies without asking
- Touch files outside explicit scope

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

**Before Committing**:
- [ ] GitHub issue created (for code changes)
- [ ] Branch created from latest main
- [ ] Commit references issue number
- [ ] All tests pass locally
- [ ] Quality gate passed
- [ ] Linting/formatting applied (language-specific)
- [ ] Structure compliance (≤5 root folders)
- [ ] Changes ≤30 lines (or checkpointed)

**Before Creating PR**:
- [ ] Branch pushed to remote
- [ ] PR description includes: What, Why, How to test
- [ ] Screenshots attached (if UI changes)
- [ ] PR references issue ("Closes #123")
- [ ] PR is small and focused (<400 lines)
- [ ] Documentation updated (if API changed)

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

**Last Updated**: 2025-11-20
**Review**: After major features or monthly
**Applies To**: All AI assistants on this project
