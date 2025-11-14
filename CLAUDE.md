# Project Standards - Best Practice Toolkit

> **Purpose**: Enforce changelog, comments, minimal structure - maximum efficiency
> **Last Updated**: 2025-11-10
> **Applies To**: Claude Code and all AI assistants working on this codebase

---

## 🎯 Core Objective

**Enforce**: Changelog for every change + Well-commented code + Minimal structure
**Focus**: Speed and frugality - no bloat
**No**: Unsolicited reports, verbose docs, or folder sprawl

---

## 💡 Skills-Based Architecture (NEW!)

> **This CLAUDE.md is now complemented by modular Skills for progressive disclosure**

**Claude automatically loads relevant skills based on your task**:
- Quality standards (when testing or checking code)
- TDD workflow (when writing tests)
- Problem-solving (when debugging)
- Git workflow (when committing)
- File placement (when creating files)
- Planning mode (when planning features)
- MCP usage (when using MCP tools)
- Context management (when managing tokens)

**Skills location**: `.claude/skills/` folder
**Benefits**: Load only what's needed (~3KB) vs entire CLAUDE.md (49KB)
**See**: `.claude/skills/README.md` for details

**Two-tier system**:
1. **Toolkit skills** (provided) - Universal best practices
2. **Project skills** (you create) - Your domain-specific patterns

**Create your own skills** using the template at `.claude/skills/template/skill.md`

---

## ✅ MANDATORY: Live Task List (TASKS.md)

**Every change must be tracked as a granular task**

### Task Rules
1. **Read TASKS.md first** - Always check current tasks before coding
2. **Task size**: ≤30 lines of code, ≤15 minutes
3. **One task at a time**: Complete, test, commit before next
4. **Break down large tasks**: If >30 lines, STOP and break into sub-tasks
5. **Update TASKS.md**: Mark complete when done, add new tasks as discovered

### Workflow (Required)
```
1. Check .claude/TASKS.md for current task
2. Implement (≤30 lines max)
3. Test change works
4. Update CHANGELOG.md
5. Run quality gate: bash .claude/quality-gate/check_quality.sh
6. Commit with descriptive message
7. Mark task complete in .claude/TASKS.md
8. Move to next task
```

### Why Granular Tasks?
- **Safe**: Small changes = easy rollback if issues
- **Fast**: Each task ships independently
- **Testable**: Can verify each change works
- **Clear**: Always know what's next

**If task feels too large**: STOP, break it down in TASKS.md first, then implement smallest piece.

---

## ⚡ MANDATORY MCP Usage

> **CRITICAL**: These MCP tools are NOT optional - they enforce project standards and MUST be used at specific stages.

### Session Start (ALWAYS)

**Before doing ANY work, call these tools in order**:

1. **`load_project_context`** - Load objective, decisions, and history
   ```
   Call: mcp__memory__load_project_context
   Args: project_path = current working directory
   ```

2. **`get_current_status`** - See current tasks and progress
   ```
   Call: mcp__project__get_current_status
   Args: project_path = current working directory
   ```

**Output from these tools tells you**:
- What is the project objective and clarity score
- What tasks are pending/in-progress/completed
- What decisions were made in previous sessions
- What are the next steps

**NEVER skip these** - working without context leads to scope creep and misalignment.

---

### Before Starting ANY Task (MANDATORY)

**Before implementing anything, validate alignment**:

1. **`validate_task_alignment`** - Check if task serves objective
   ```
   Call: mcp__project__validate_task_alignment
   Args:
     project_path = current working directory
     task_description = what you're about to do
   ```

2. **Interpret results**:
   - **Alignment score ≥70**: Task is aligned, proceed
   - **Alignment score <70**: Task does NOT serve objective
     - STOP immediately
     - Ask user: "This task has low alignment (score: X). Should we proceed anyway, or focus on objective-critical work?"

3. **If task is aligned, validate size**:
   ```
   Call: mcp__project__validate_task_size
   Args: task_description = what you're about to do
   ```
   - If task is too large (>30 lines), break it down BEFORE implementing

**Example conversation flow**:
```
User: "Add user profiles to the app"
Assistant: [Calls validate_task_alignment]
Result: {aligned: true, score: 85}
Assistant: [Calls validate_task_size]
Result: {too_large: true, estimated_lines: 120}
Assistant: "This task aligns with the objective (score: 85) but is too large.
Let me break it into smaller tasks:
1. Create user profile model (≤30 lines)
2. Add profile API endpoints (≤30 lines)
3. Create profile UI component (≤30 lines)
4. Add profile tests (≤30 lines)
Which should we start with?"
```

---

### Before Completing ANY Task (MANDATORY)

**Never mark a task complete without quality gate**:

1. **`run_quality_gate`** - Verify all quality standards
   ```
   Call: mcp__quality__run_quality_gate
   Args:
     project_path = current working directory
     changes_made = list of files modified
   ```

2. **Interpret results**:
   - **PASS**: All checks passed
     - Proceed to commit
     - Mark task complete

   - **FAIL**: Quality issues detected
     - DO NOT commit
     - DO NOT mark task complete
     - Fix issues one by one
     - Re-run quality gate
     - Repeat until PASS

**NEVER override quality gate failure** - if it fails, fix the issues.

**Example conversation flow**:
```
User: "The feature is done, commit it"
Assistant: [Calls run_quality_gate]
Result: {
  passed: false,
  issues: [
    "3 failing tests in test_auth.py",
    "2 linting errors in auth.py"
  ]
}
Assistant: "Quality gate FAILED. I cannot commit yet. Let me fix:
1. Fixing failing tests... [fixes tests]
2. Fixing linting errors... [fixes errors]
[Calls run_quality_gate again]
Result: {passed: true}
Assistant: "Quality gate PASSED. Now committing..."
```

---

### During Development (Use When Appropriate)

**Structure validation** (use when creating new files/folders):
```
mcp__quality__audit_project_structure
mcp__quality__validate_file_placement
```

**Code quality checks** (use after writing significant code):
```
mcp__quality__check_code_quality
Args: file_paths = files you just modified
```

**Priority challenges** (use when task list is long):
```
mcp__project__challenge_task_priority
Args: task_id = task you're about to start
```
- Ensures you're working on highest-priority tasks first
- Prevents busy work on low-value features

**Scope creep detection** (use every 5-10 tasks):
```
mcp__project__identify_scope_creep
Args: project_path = current working directory
```
- Identifies tasks that don't serve the objective
- Helps refocus on essential work

---

### Session End (ALWAYS)

**Before ending session, save context for next time**:

1. **`save_session_summary`** - Persist what happened
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
  "JWT tokens expire after 24 hours",
  "Refresh tokens stored in httpOnly cookies"
]
Next steps: [
  "Add password reset functionality",
  "Implement email verification",
  "Add rate limiting to login endpoint"
]
Blockers: []
```

**Why this matters**:
- Next session starts with full context
- No repeated questions about "what were we doing?"
- Decisions are preserved for future reference

---

### Complete MCP Tool Reference

#### Memory MCP Tools
- `list_projects` - See all tracked projects
- `load_project_context` - **MANDATORY at session start**
- `save_session_summary` - **MANDATORY at session end**
- `save_decision` - Save architectural/technical decisions
- `search_memory` - Search across all projects
- `load_project_objective` - Load objective details
- `save_project_objective` - Save objective (used by Project MCP)

#### Quality MCP Tools
- `run_quality_gate` - **MANDATORY before task completion**
- `check_code_quality` - Check specific files
- `audit_project_structure` - Validate minimal root compliance
- `validate_file_placement` - Check files in correct locations
- `find_obsolete_files` - Detect unused code
- `verify_standards` - Comprehensive standards check
- `update_documentation` - Update README with changes
- `update_changelog` - Add changelog entry
- `add_missing_docstrings` - Generate docstrings

#### Project MCP Tools
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

### Enforcement Rules

**AI assistants MUST**:
1. Call `load_project_context` + `get_current_status` at session start
2. Call `validate_task_alignment` before implementing anything
3. Call `run_quality_gate` before marking tasks complete
4. Call `save_session_summary` at session end
5. NEVER skip quality gate failures
6. NEVER implement tasks with alignment score <70 without user confirmation

**If you (AI assistant) skip these**:
- You're violating project standards
- You're introducing scope creep risk
- You're bypassing quality enforcement
- You're making the project harder to maintain

**User can override** alignment checks, but AI must:
1. Show the alignment score
2. Explain why it's low
3. Get explicit user confirmation to proceed

---

## 🎯 Planning Mode - MANDATORY for New Features

> **CRITICAL**: Planning Mode (Shift+Tab×2) is NON-NEGOTIABLE for new features

### When to Use Planning Mode

**ALWAYS enter Planning Mode for**:
- New features or functionality
- Significant refactoring (>30 lines)
- Complex bug fixes requiring multiple files
- Architecture changes
- Any work where requirements aren't crystal clear

**How to Enter**:
Press **Shift+Tab twice** to enter read-only Planning Mode where Claude cannot modify files.

### Planning Mode Workflow

**Step 1: Requirements Discovery**
```
User: "I want to add user authentication"
Claude: [In Planning Mode] "Before planning, let me ask questions:
1. What authentication method? (JWT, sessions, OAuth)
2. What user data needs to be stored?
3. Are there existing auth patterns in the codebase?
4. What security requirements must we meet?
5. What are the edge cases? (password reset, account lockout, etc.)"
```

**Step 2: Plan Creation**
```
Claude: [Creates detailed plan with]:
- Clear objectives
- Task breakdown (each ≤30 lines)
- File changes required
- Test requirements
- Acceptance criteria
- Estimated effort
```

**Step 3: Plan Review**
```
User reviews plan and either:
- Approves → Claude can begin implementation
- Requests changes → Claude refines plan
- Rejects → Return to requirements
```

**Step 4: Implementation**
Only after explicit approval does Claude exit Planning Mode and begin coding.

### Why Planning Mode Works

**Physical barrier**: Claude literally cannot write code in Planning Mode
**Forces comprehensive planning**: No shortcuts to implementation
**Prevents context drift**: Clear plan = clear execution
**Enables autonomous work**: With approved plan, Claude can work for hours without supervision

### Planning Mode Rules

1. **NEVER skip Planning Mode for new features**
2. **Plans must include**:
   - Task list with checkboxes
   - Acceptance criteria
   - File changes
   - Test requirements
3. **Get explicit user approval** before exiting Planning Mode
4. **Document plan** in tasks.md or feature-plan.md for persistence

---

## 🧠 Context Management Rules

> **The 60% Rule**: Never exceed 60% of context window capacity

### Context Limits

**Monitor context usage**:
- Watch for "approaching usage limit" warnings
- Proactively manage BEFORE hitting limits
- Context compaction = information loss

**When approaching 60%**:
- Use `/compact` manually if needed (loses some details)
- Use `/clear` to start fresh (recommended)
- Save state to files first (plan.md, progress.md)

### Context Best Practices

**Scope sessions to single features**:
- One chat = one project or feature
- Use `/clear` when feature complete
- Use `/resume` or `--continue` to return to conversations

**Selective file loading**:
- Use `@filename` syntax for specific files
- DON'T say "look at everything"
- Use `.claudeignore` to exclude: node_modules/, vendor/, dist/, build/, large data files

**Progressive context building**:
1. Read relevant files with NO CODE YET
2. Use subagents for investigation (preserves main context)
3. Request plan (do not code until confirmed)
4. Implement in small steps (diffs <200 lines)
5. Use checkpoints between steps

**External memory systems**:
- Write plans to files: spec.md, requirements.md, design.md, plan.md, tasks.md
- These survive context window limits
- Enable regeneration from specs
- Become living documentation

### Context Management Anti-Patterns

**DON'T**:
- Dump multiple tasks at once ("do these one by one" instead)
- Let automatic compaction happen (use /clear proactively)
- Fill context with irrelevant command outputs
- Assume Claude remembers earlier conversations
- Read all files when only some are needed

**DO**:
- One task at a time
- Clear between unrelated tasks
- Save important state to files
- Reference specific files with @
- Use scripts for repetitive operations

---

## 🚫 Anti-Patterns - What NOT to Do

> **Learn from common failures**: These patterns ALWAYS cause problems

### Prohibited Implementation Patterns

**NEVER write**:
- "In a full implementation..." or "This is a simplified version"
- "You would need to..." or "Consider adding..."
- Mock functions or placeholder data structures
- Incomplete error handling or validation
- Comments like "TODO: implement later"
- Stubs or partial implementations

**ALWAYS write**:
- Complete, production-ready code
- Full error handling
- All edge cases covered
- Working implementations only
- No placeholders or TODOs

### Prohibited Communication Patterns

**NEVER use**:
- Social validation ("You're absolutely right!")
- Hedging language ("might," "could potentially")
- Excessive explanation of obvious concepts
- Over-apologizing
- Asking permission for obvious next steps

**ALWAYS be**:
- Direct and concise
- Confident in technical decisions
- Focused on problem-solving
- Clear about trade-offs
- Professional and efficient

### Premature Coding (The #1 Failure Mode)

**NEVER start coding when**:
- Requirements are vague or unclear
- No plan has been created
- User hasn't approved approach
- Success criteria aren't defined
- You haven't asked clarifying questions

**ALWAYS ask first**:
- "What exactly should this do?"
- "What are the edge cases?"
- "What are the success criteria?"
- "Are there constraints I should know?"
- "Should I create a plan first?"

### Context Management Failures

**NEVER**:
- Let context exceed 60% before managing it
- Dump multiple unrelated tasks
- Trust automatic compaction to preserve details
- Keep reading files you've already read
- Fill context with command output dumps

### Over-Engineering

**NEVER add features not requested**:
- Extra configuration options "for flexibility"
- Additional features "that might be useful"
- Complex abstractions for simple problems
- Premature optimization
- "Best practices" that aren't needed

**ALWAYS solve the specific problem**:
- Minimal effective solution
- YAGNI (You Ain't Gonna Need It)
- Simple beats clever
- Constraints are features

### Technical Mistakes

**NEVER**:
- Skip compiling before running tests
- Write tests expecting them to pass without seeing failures first
- Use non-standard git commands
- Leave old code when rewriting
- Trust progress reports without validation

**ALWAYS**:
- Compile before testing
- See tests fail before making them pass (TDD)
- Use standard git operations
- Remove old implementation when rewriting
- Validate independently

---

## 🧠 MANDATORY Problem-Solving Techniques

> **CRITICAL**: When encountering ANY bug, error, or challenge, you MUST apply these systematic problem-solving techniques. Random changes and guessing are PROHIBITED.

### When to Apply These Techniques

**ALWAYS use these when**:
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

### Decision Tree: When Stuck

**Step 1: Classify the block**

| Type | Technique to Apply |
|------|-------------------|
| Syntax/compile error | Check docs, minimal reproduction |
| Logic error | Rubber duck, add logging |
| Unknown cause | Binary search debugging |
| Concept gap | First principles |
| Performance issue | Profile first, never guess |

**Step 2: Apply relevant technique from below**

---

### Core Problem-Solving Techniques (Apply in Order)

#### 1. FIRST PRINCIPLES (Mandatory for Concept Gaps)

Break problem to fundamentals, ignore conventions:

```
Questions to ask:
- What MUST be true for this to work?
- What am I assuming that might be false?
- Can I solve this without library X or pattern Y?
- What's the simplest possible version?
```

**Example**:
```
Problem: Authentication not working
First Principles:
- User MUST have valid credentials (check: ✓)
- Token MUST be generated (check: ?)
- Token MUST be sent in request (check: ?)
- Token MUST be validated on server (check: ?)
→ Found: Token generation returns undefined
```

---

#### 2. INVERSION (Mandatory for Mysterious Bugs)

Instead of "how to fix", ask "what would break this worse?"

```
Questions to ask:
- What would cause this EXACT error?
- What would I do if I WANTED this bug?
- What's the opposite of what I expect?
```

**Example**:
```
Problem: Function returns wrong value sometimes
Inversion: What would make it ALWAYS return wrong value?
→ If input validation was broken
→ Check input validation
→ Found: Edge case when input is empty string
```

---

#### 3. BINARY SEARCH DEBUGGING (Mandatory for Unknown Cause)

Isolate issue in log₂(n) steps:

```
1. Comment out 50% of code
2. Does problem persist?
   - YES → Problem is in remaining code
   - NO → Problem is in commented code
3. Repeat on relevant half
```

**Example**:
```
100 lines of code causing error
→ Comment out lines 50-100: Still errors
→ Comment out lines 25-50: Still errors
→ Comment out lines 12-25: Error gone!
→ Issue is in lines 12-25
→ Narrow down to specific line
```

---

#### 4. STATE INSPECTION (Mandatory for Logic Errors)

Verify assumptions at each step:

```
1. Print ACTUAL values vs EXPECTED values
2. Check types, shapes, nulls
3. Verify state at each step of execution
```

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

#### 5. MINIMAL REPRODUCTION (Mandatory Before Asking for Help)

Remove all non-essential code:

```
1. Create new file with ONLY the failing code
2. Remove all dependencies possible
3. Does problem still occur?
   - YES → Problem is in remaining code
   - NO → Removed code caused it
```

**Example**:
```python
# Original: 500 lines across 5 files
# Minimal reproduction: 10 lines, 1 file
def test_bug():
    result = function_with_bug(input)
    assert result == expected  # Fails here

# Now the bug is isolated and debuggable
```

---

#### 6. CONSTRAINT RELAXATION (Mandatory When Stuck on "Optimal")

Solve simpler version first:

```
1. Solve for smallest input (n=1, n=2)
2. Solve without constraint X
3. Solve inefficiently first, optimize later
```

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

#### 7. ANALOGICAL THINKING (Mandatory for New Problems)

Map to similar solved problems:

```
Questions:
- What similar problem have I solved before?
- How do other domains handle this?
- What's the data structure equivalent?
```

**Example**:
```
Problem: Rate limiting API requests
Analogical Thinking:
- Similar to: Token bucket algorithm
- Other domains: Traffic shaping in networks
- Data structure: Queue with time-based eviction
→ Implement token bucket pattern
```

---

#### 8. RUBBER DUCK (Mandatory for All Debugging)

Force precision by explaining out loud:

```
Explain to yourself (or write down):
1. What SHOULD happen
2. What ACTUALLY happens
3. Why I think X causes Y
4. What assumptions am I making
```

**Template**:
```
"The function should [expected behavior] when given [input].
Instead, it [actual behavior].
I think this is because [assumption].
Let me verify [assumption] is true..."
```

---

#### 9. FIVE WHYS (Mandatory for Root Cause Analysis)

Dig to root cause, not symptoms:

```
Problem: X fails
1. Why? → Y is wrong
2. Why? → Z wasn't set
3. Why? → Config missing
4. Why? → Docs unclear
5. Why? → [ROOT CAUSE]
```

**Example**:
```
Problem: Tests failing in CI
1. Why? → Environment variable not set
2. Why? → Not in CI config file
3. Why? → We forgot to add it
4. Why? → No checklist for new env vars
5. Why? → No documentation process
ROOT CAUSE: Need to create env var documentation checklist
```

---

#### 10. SCAMPER (Mandatory for Creative Blocks)

Creative pivots when standard approaches fail:

```
- Substitute: Different algorithm/library?
- Combine: Merge two approaches?
- Adapt: How does X solve this?
- Modify: Change scope/constraints?
- Purpose: Solve different problem instead?
- Eliminate: What's unnecessary?
- Reverse: Work backwards from goal?
```

---

### Quick Wins Checklist (Run FIRST, Every Time)

Before applying advanced techniques, check these:

- [ ] Read the FULL error message (not just first line)
- [ ] Verify types match expected types
- [ ] Check file paths, names, and case sensitivity
- [ ] Test with simplest possible input
- [ ] Verify version compatibility
- [ ] Read relevant docs section
- [ ] Search error message verbatim
- [ ] Confirm example code actually runs

---

### Meta-Strategy: Still Stuck After 3 Techniques?

If you've applied 3 techniques and still stuck:

1. **Write it out**: Explain the problem in writing
2. **List attempts**: Document everything tried
3. **Identify gaps**: What do you NOT know?
4. **Research gaps**: Search/read docs for missing knowledge
5. **Try opposite**: Do the opposite of current approach

**When to escalate**:
- After applying 5+ techniques
- After >30 minutes on same issue
- When you've exhausted your knowledge

**What to do**:
- Use `/checkpoint` to save current state
- Take a break (seriously, sleep on it)
- Ask for help with minimal reproduction ready

---

### Anti-Patterns in Problem-Solving

**NEVER do these** (they waste time):

❌ **Random changes** hoping something works
❌ **Optimizing** before it works at all
❌ **Assuming docs** are current without verifying
❌ **Trusting errors** blindly without investigation
❌ **Skipping** minimal reproduction
❌ **Giving up** after 1-2 attempts
❌ **Copy-pasting** solutions without understanding
❌ **Debugging in production** instead of locally

---

### Problem-Solving Success Metrics

Track these to improve:

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

### Integration with Workflows

**TDD Cycle**: When tests fail
1. ✅ Read full error (Quick Wins #1)
2. ✅ Apply State Inspection (#4)
3. ✅ Rubber Duck the failure (#8)
4. ✅ Fix minimal code to pass

**Error Recovery**: When code breaks
1. ✅ Apply Binary Search Debugging (#3)
2. ✅ Create Minimal Reproduction (#5)
3. ✅ Use Five Whys for root cause (#9)

**Performance Issues**: When code is slow
1. ✅ Profile first (never guess)
2. ✅ Apply Constraint Relaxation (#6)
3. ✅ Use First Principles (#1)

---

**Reference**: See `/docs/guides/thinking skills.md` for detailed examples and additional context.

---

## 📁 File Placement Rules

### Root Directory - MINIMAL (Target: ≤5 folders, ≤5 files)

**Allowed Folders** (5 maximum):
```
/.claude/         - Toolkit files (skills, commands, mcp-servers, quality-gate)
/tests/           - Test suite for all code
/docs/            - ALL documentation
/dist/            - Distribution packages (generated)
/retrofit-tools/  - Retrofit assessment scripts
```

**Allowed Files** (keep minimal):
```
/README.md        - Brief project overview (link to docs/)
/CLAUDE.md        - This file (project standards)
/package_toolkit.sh - Build script
/.gitignore       - Git ignore rules
/LICENSE          - MIT license (generated)
```

**FORBIDDEN in Root**:
- ❌ Documentation files (*.md except README.md and CLAUDE.md)
- ❌ Configuration files (move to .config/ or appropriate subdir)
- ❌ Data files (move to docs/references/ or artifacts/)
- ❌ Log files (use /logs if needed, add to .gitignore)
- ❌ Temporary files (use /temp if needed, add to .gitignore)

### Documentation Structure

**ALL documentation goes in `/docs/`**:
```
/docs/
├── README.md                    - Comprehensive documentation index
├── design/                      - Architecture and system design
│   ├── MCP_IMPLEMENTATION_APPROACH.md
│   └── CSO_FRAMEWORK_INTEGRATION.md
├── guides/                      - How-to guides and methodology
│   ├── RETROFIT_METHODOLOGY.md
│   ├── AUTONOMOUS_MODE_ROADMAP.md
│   └── thinking skills.md      - MANDATORY problem-solving techniques
├── analysis/                    - Assessments and analysis
│   ├── DELIVERY_SUMMARY.md
│   ├── AUTONOMOUS_TOOLS_ANALYSIS.md
│   └── PROJECT_RETROFIT_ASSESSMENT.md
├── references/                  - Reference materials and examples
│   └── [input reference files]/
└── notes/                       - Planning and status
    └── PROJECT_PLAN.md          - Current project plan (ALWAYS CURRENT)
```

### Source Code Structure

**MCP Servers** (`/.claude/mcp-servers/`):
```
/.claude/mcp-servers/
├── memory_mcp.py       - Context persistence MCP
├── quality_mcp.py      - Quality enforcement MCP
├── project_mcp.py      - Objective clarification MCP
├── requirements.txt    - Python dependencies
└── README.md           - Installation and usage
```

**Tests** (`/tests/`):
```
/tests/
├── test_memory_mcp.py
├── test_quality_mcp.py
├── test_project_mcp.py
├── conftest.py         - Pytest configuration
└── README.md           - Testing documentation
```

### Hidden Directories

**Configuration**:
```
/.claude/            - Claude Code configuration (gitignored)
    ├── skills/      - Toolkit and project skills
    ├── commands/    - Slash commands
    ├── mcp-servers/ - MCP server implementations (FULL mode)
    ├── quality-gate/ - Quality gate scripts (FULL mode)
    ├── best-practice.md - Project standards
    └── TASKS.md     - Live task list
/.git/               - Git repository
```

---

## 🎯 Development Workflow

### Starting Work

**1. Load Context**
```bash
# Always read these files first:
docs/notes/PROJECT_PLAN.md     # Current objectives and tasks
CLAUDE.md                       # This file (standards)
docs/README.md                  # System overview
```

**2. Check Current Phase**
Review PROJECT_PLAN.md → Current Sprint section to understand current work.

**3. Select Model**
- **Planning tasks** (architecture, breaking down features) → Use max mode
- **Implementation tasks** (writing code, tests, docs) → Use standard mode

### MANDATORY: Create GitHub Issue Before Code Changes

**CRITICAL**: Before starting ANY task that involves code changes going to GitHub, you MUST create a GitHub issue.

**When to Create an Issue**:
- ✅ New features or functionality
- ✅ Bug fixes
- ✅ Refactoring that changes behavior
- ✅ Performance improvements
- ✅ Security fixes
- ✅ Any code change that will be committed and pushed

**When NOT to Create an Issue**:
- ❌ Documentation-only changes (README updates, comments)
- ❌ Local experiments not intended for GitHub
- ❌ Trivial changes (typo fixes, formatting)

**Issue Creation Workflow**:

```bash
# 1. Create issue on GitHub BEFORE starting work
gh issue create --title "feat: Add user authentication" \
  --body "## Description
Implement JWT-based authentication system

## Acceptance Criteria
- [ ] User can register with email/password
- [ ] User can login and receive JWT token
- [ ] Token expires after 24 hours
- [ ] Protected routes require valid token

## Tasks (≤30 lines each)
- [ ] Create User model
- [ ] Add registration endpoint
- [ ] Add login endpoint
- [ ] Add JWT middleware

## Definition of Done
- [ ] All tests pass (≥80% coverage)
- [ ] Quality gate passes
- [ ] Code reviewed
- [ ] Documentation updated"

# 2. Note the issue number (e.g., #42)

# 3. Create branch with issue number
git checkout -b feature/auth-#42

# 4. Work on task (following all other standards)

# 5. Link commits to issue
git commit -m "feat: add user registration endpoint

Implements registration with email/password validation.

Closes #42"

# 6. Create PR referencing issue
gh pr create --title "feat: Add user authentication (closes #42)" \
  --body "Closes #42

## Changes
- User registration endpoint
- JWT token generation
- Login endpoint
- Protected route middleware

## Testing
- All tests pass
- Quality gate passed
- Manual testing completed"
```

**Issue Template**:

```markdown
## Description
[Brief description of what needs to be done]

## Acceptance Criteria
- [ ] Criterion 1
- [ ] Criterion 2
- [ ] Criterion 3

## Tasks (≤30 lines each)
- [ ] Task 1
- [ ] Task 2
- [ ] Task 3

## Definition of Done
- [ ] All tests pass (≥80% coverage)
- [ ] Quality gate passes
- [ ] Code reviewed
- [ ] Documentation updated
- [ ] CHANGELOG.md updated
```

**Why This Matters**:
1. **Traceability**: Every code change has context and justification
2. **Planning**: Forces you to think through requirements before coding
3. **Communication**: Team knows what you're working on
4. **History**: GitHub issues create permanent record of why changes were made
5. **Integration**: Automatic linking between commits, PRs, and issues

**Enforcement**:
- ❌ **DO NOT** start coding without an issue number
- ❌ **DO NOT** commit code without referencing the issue
- ❌ **DO NOT** create PRs without linking to an issue
- ✅ **ALWAYS** create issue first, then branch, then code

**Using gh CLI**:

```bash
# Install gh if needed
# See: https://cli.github.com/

# Create issue
gh issue create

# List your issues
gh issue list --assignee @me

# View issue
gh issue view 42

# Close issue (or use "Closes #42" in commit message)
gh issue close 42

# Create PR that closes issue
gh pr create --fill
```

---

### Working on Tasks

**Task Size Limits**:
- ≤30 lines of implementation per task
- ≤30 minutes to complete
- Must have clear acceptance criteria

**If task feels too large**:
1. STOP - Don't implement
2. Break down into smaller sub-tasks
3. Update PROJECT_PLAN.md with sub-tasks
4. Complete each sub-task independently

**Commit Frequency**:
- After EVERY passing quality gate
- After EVERY small task completion
- Before attempting risky changes
- At EVERY checkpoint in refactoring

### Quality Standards

**MANDATORY Before Any Commit**:
```bash
# Run quality gate
bash .claude/quality-gate/check_quality.sh

# Must see:
# ✅ All tests pass
# ✅ No linting errors
# ✅ No type errors
# ✅ No security issues
# ✅ Structure compliance
```

**Coverage Requirements**:
- Minimum 80% test coverage
- All new functions must have tests
- All edge cases must be tested

**Code Style**:
- Follow PEP 8 (enforced by ruff)
- Type hints required (checked by mypy)
- Docstrings required for all public functions
- Comments for complex logic only

---

### Test-Driven Development (TDD) - MANDATORY

> **Red-Green-Refactor**: Write tests first, see them fail, make them pass, refactor

### The TDD Cycle

**Step 1: Write Failing Tests**
```python
# Write test BEFORE implementation
def test_user_profile_creation():
    """Test creating user profile with valid data."""
    user = create_user_profile(name="Alice", email="alice@example.com")
    assert user.name == "Alice"
    assert user.email == "alice@example.com"
    assert user.created_at is not None
```

**Step 2: Confirm Tests Fail**
```bash
pytest tests/test_user.py
# MUST see: FAILED - function create_user_profile doesn't exist
```

**Step 3: Commit Failing Tests**
```bash
git add tests/test_user.py
git commit -m "test: add user profile creation test (RED)"
```

**Step 4: Implement Minimal Code**
```python
# Write ONLY enough code to pass the test
def create_user_profile(name: str, email: str) -> User:
    return User(
        name=name,
        email=email,
        created_at=datetime.now()
    )
```

**Step 5: Iterate Until Green**
```bash
pytest tests/test_user.py
# Keep iterating until: PASSED
```

**Step 6: Refactor**
```python
# Improve code quality while keeping tests green
# Extract functions, improve naming, reduce duplication
pytest tests/test_user.py  # Still passes after refactor
```

**Step 7: Commit**
```bash
git add -A
git commit -m "feat: implement user profile creation (GREEN)"
```

### TDD Rules

1. **NEVER write implementation before tests**
2. **ALWAYS see tests fail first** (RED phase)
3. **Write minimal code to pass** (no extra features)
4. **Refactor only when tests are green**
5. **Each test validates ONE thing**
6. **Tests are acceptance criteria**

### Test Structure - Given-When-Then

```python
def test_should_return_error_when_invalid_email():
    """Test error handling for invalid email format."""
    # Given: Invalid email input
    invalid_email = "not-an-email"

    # When: Attempt to create user
    with pytest.raises(ValidationError) as exc:
        create_user_profile(name="Bob", email=invalid_email)

    # Then: Should raise validation error with message
    assert "Invalid email format" in str(exc.value)
```

### Autonomous TDD with Claude

**Workflow**:
1. User: "Write failing tests for user authentication"
2. Claude writes tests (NO implementation)
3. Claude runs tests → confirms they fail
4. Claude commits failing tests
5. User approves
6. Claude implements → iterates until tests pass
7. Claude refactors (tests still green)
8. Claude commits

**Maximum attempt limits**:
- Simple tasks: 1-3 turns
- Medium complexity: 5-10 turns
- Complex tasks: 10-20 turns
- Use `--max-turns` flag to prevent infinite loops

**Loop detection triggers**:
- Same files read >3 times
- Same test failures after multiple attempts
- Context approaching limits without progress
- **Action**: Use `/compact` or `/clear` or break task smaller

### Test Quality Standards

**All tests must have**:
- Clear descriptive names (Should_When pattern)
- Given-When-Then structure
- Single assertion focus
- Edge cases covered
- Error cases validated
- Performance benchmarks (where applicable)

**Example test suite**:
```python
class TestUserAuthentication:
    """Tests for user authentication system."""

    def test_should_authenticate_when_valid_credentials(self):
        """Test successful authentication."""
        # Given: Valid credentials
        # When: Authenticate
        # Then: Return auth token

    def test_should_reject_when_invalid_password(self):
        """Test invalid password rejection."""
        # Given: Wrong password
        # When: Authenticate
        # Then: Raise AuthenticationError

    def test_should_lockout_after_failed_attempts(self):
        """Test account lockout after 5 failed attempts."""
        # Given: 5 failed login attempts
        # When: 6th attempt
        # Then: Raise AccountLockedError
```

---

### Git Checkpoint Workflow

> **Fearless exploration**: Save state before risky changes, instant rollback

### Native Checkpointing

**Automatic state capture**:
- Claude automatically saves state before each edit
- No manual intervention required
- Instant rewind capability

**Rewind commands**:
```bash
# Escape twice (Esc×2) - Quick rewind
# OR use command
/rewind

# Options:
# - Code only
# - Conversation only
# - Both code and conversation
```

### Manual Checkpoints

**Before risky operations**:
```bash
# Create safety checkpoint
git tag checkpoint-before-refactor

# Do risky refactor...

# If it works:
git tag -d checkpoint-before-refactor

# If it fails:
git reset --hard checkpoint-before-refactor
```

### Checkpoint Best Practices

**Create checkpoints**:
- Before large refactoring
- Before experimental features
- Before complex bug fixes
- Before merge operations
- At end of each working day

**Checkpoint workflow**:
```bash
# 1. Ensure working directory is clean
git status

# 2. Create descriptive checkpoint
git tag checkpoint-auth-refactor-$(date +%Y%m%d-%H%M)

# 3. Work fearlessly knowing rollback is instant

# 4. If successful, continue
# 5. If failed, instant rollback
```

### Advanced: Pre-Tool Hooks

**Automated checkpoints before file writes**:
```json
{
  "hooks": {
    "PreToolUse": [
      {
        "matcher": "Write|Edit|MultiEdit",
        "command": "git add -A && git commit -m 'auto-checkpoint: before ${tool}'"
      }
    ]
  }
}
```

**Benefits**:
- Automatic state capture
- No manual checkpoint management
- Granular undo without token waste
- Time-travel debugging

---

### Error Recovery - Delete and Reroll Pattern

**If debugging spiral detected** (3+ failed attempts on same issue):

```bash
# STOP - You're stuck
git log --oneline -5           # Find last working commit
git reset --hard <commit_hash> # Revert to working state
git clean -fd                  # Remove untracked files
```

**Then**:
1. Break task into smaller pieces
2. Ensure each piece is testable
3. Complete smallest piece first
4. Test and commit before proceeding

### Refactoring - Checkpoint Pattern

**Never refactor >30 lines at once**. Use checkpoints:

```markdown
## Refactor Plan: [Description]

Checkpoint 1: Extract function signatures (no implementation)
- Validation: All tests still pass
- Rollback point: YES

Checkpoint 2: Move functions to new module
- Validation: Import statements work, tests pass
- Rollback point: YES

Checkpoint 3: Update implementations
- Validation: All tests pass with new logic
- Rollback point: YES
```

**Workflow**:
1. Define target architecture
2. Break into checkpoints (each ≤30 lines)
3. For each checkpoint:
   - Implement
   - Run tests
   - PASS → Commit → Proceed
   - FAIL → Rollback checkpoint → Retry smaller

---

## 🧪 Testing Requirements

### Test Coverage

**Minimum Coverage**: 80% across all code

**Required Tests**:
- Unit tests for all MCP tool functions
- Integration tests for MCP workflows
- Edge case tests (error handling, invalid input)
- Regression tests for fixed bugs

### Test Structure

```python
# tests/test_memory_mcp.py
import pytest
from mcp_servers.memory_mcp import MemoryMCP

class TestMemoryMCP:
    """Tests for Memory MCP server."""

    def test_save_session_summary(self, tmp_path):
        """Test saving session summary."""
        mcp = MemoryMCP(storage_dir=tmp_path)
        result = mcp.save_session_summary(
            project_path="/test/project",
            summary="Test summary"
        )
        assert result["success"] is True

    def test_invalid_project_path(self, tmp_path):
        """Test error handling for invalid paths."""
        mcp = MemoryMCP(storage_dir=tmp_path)
        with pytest.raises(ValueError):
            mcp.save_session_summary(
                project_path="",
                summary="Test"
            )
```

### Running Tests

```bash
# Run all tests
pytest tests/ -v --cov=.claude/mcp-servers --cov-report=term-missing

# Run specific test file
pytest tests/test_memory_mcp.py -v

# Run with coverage report
pytest --cov=.claude/mcp-servers --cov-report=html
```

---

## 🔍 Code Quality Tools

### Linting - Ruff

```bash
# Check for linting issues
ruff check .claude/mcp-servers/

# Auto-fix issues
ruff check --fix .claude/mcp-servers/
```

**Configuration** (pyproject.toml or ruff.toml):
```toml
[tool.ruff]
line-length = 100
target-version = "py310"
select = ["E", "F", "W", "I", "N"]
```

### Type Checking - Mypy

```bash
# Check types
mypy .claude/mcp-servers/
```

**Configuration** (pyproject.toml):
```toml
[tool.mypy]
python_version = "3.10"
strict = true
warn_return_any = true
warn_unused_configs = true
```

### Security - Bandit

```bash
# Check for security issues
bandit -r .claude/mcp-servers/
```

---

## 🏗️ Architecture Conventions

### MCP Server Structure

**All MCP servers follow this pattern**:

```python
"""
MCP Server: [Name]
Purpose: [Brief description]
"""
from typing import Dict, List, Optional
import asyncio

class [Name]MCP:
    """[Name] MCP server."""

    def __init__(self, config: Optional[Dict] = None):
        """Initialize MCP server."""
        self.config = config or {}

    async def handle_tool_call(
        self,
        tool_name: str,
        arguments: Dict
    ) -> Dict:
        """Handle MCP tool calls."""
        handlers = {
            "tool_name": self._handle_tool_name,
        }

        handler = handlers.get(tool_name)
        if not handler:
            return {
                "error": f"Unknown tool: {tool_name}",
                "success": False
            }

        return await handler(arguments)

    async def _handle_tool_name(self, args: Dict) -> Dict:
        """Handle specific tool."""
        # Implementation
        return {"success": True, "data": {}}
```

### Naming Conventions

**Files**:
- MCP servers: `[name]_mcp.py` (e.g., `memory_mcp.py`)
- Tests: `test_[name]_mcp.py` (e.g., `test_memory_mcp.py`)
- Scripts: `[action]_[object].py` (e.g., `retrofit_assess.py`)

**Classes**:
- PascalCase: `MemoryMCP`, `QualityGate`, `ObjectiveClarifier`

**Functions**:
- snake_case: `save_session_summary`, `run_quality_gate`

**Constants**:
- UPPER_SNAKE: `MAX_RETRIES`, `DEFAULT_STORAGE_DIR`

**Variables**:
- snake_case: `project_path`, `clarity_score`

### Error Handling

**Always use try-except with logging**:

```python
import logging

logger = logging.getLogger(__name__)

async def risky_operation(self, data: Dict) -> Dict:
    """Perform operation that might fail."""
    try:
        result = await self._process(data)
        return {"success": True, "result": result}

    except ValueError as e:
        logger.error(f"Invalid data: {e}")
        return {
            "success": False,
            "error": f"Invalid data: {str(e)}",
            "error_type": "validation"
        }

    except Exception as e:
        logger.exception("Unexpected error")
        return {
            "success": False,
            "error": f"Unexpected error: {str(e)}",
            "error_type": "internal"
        }
```

---

## 📝 Documentation Standards

### Code Documentation

**All public functions require docstrings**:

```python
def save_project_objective(
    self,
    project_path: str,
    objective_data: Dict
) -> Dict:
    """Save project objective to persistent storage.

    Args:
        project_path: Absolute path to project directory
        objective_data: Dictionary containing:
            - problem: Problem statement
            - target_users: Target user description
            - solution: Solution description
            - success_metrics: List of success metrics
            - constraints: List of constraints
            - clarity_score: Score 0-100

    Returns:
        Dictionary containing:
            - success: Boolean indicating if save succeeded
            - message: Human-readable status message
            - clarity_score: The saved clarity score

    Raises:
        ValueError: If project_path is empty or invalid
        IOError: If unable to write to storage

    Example:
        >>> mcp = MemoryMCP()
        >>> result = mcp.save_project_objective(
        ...     "/path/to/project",
        ...     {"problem": "...", "clarity_score": 85}
        ... )
        >>> assert result["success"] is True
    """
    # Implementation
```

### Markdown Documentation

**All markdown files require**:
- Title (# heading)
- Brief purpose/description at top
- Table of contents for files >200 lines
- Clear section headings
- Code examples where applicable
- Last updated date

---

## 🔄 Git Workflow

### Branch Strategy

**Main branches**:
- `main` - Production-ready code only
- `develop` - Integration branch for features

**Feature branches**:
- `feature/[name]` - New features
- `fix/[name]` - Bug fixes
- `refactor/[name]` - Refactoring work
- `docs/[name]` - Documentation updates

### Commit Messages

**Format**:
```
[type]: [description]

[optional body]

[optional footer]
```

**Types**:
- `feat` - New feature
- `fix` - Bug fix
- `refactor` - Code refactoring
- `test` - Adding tests
- `docs` - Documentation changes
- `chore` - Build/config changes

**Examples**:
```
feat: add autonomous daemon to project MCP

Implements safe autonomous execution with quality gate enforcement
and auto-rollback on failure.

Closes #42
```

```
fix: handle null project path in memory MCP

Added validation to reject empty project paths before attempting
to save data.

Fixes #38
```

### Commit Frequency

**Commit after**:
- Every passing quality gate
- Every completed task (≤30 lines)
- Every refactor checkpoint
- Before risky changes

**Never commit**:
- Failing tests
- Linting errors
- Type errors
- Without running quality gate

---

## ⚡ Slash Commands - Workflow Automation

> **Custom commands** in `.claude/commands/` automate repeatable workflows

### Core Commands

**Feature Development**:
- `/spec [feature]` - Create minimal specification with aggressive scope reduction
- `/plan [feature]` - Enter Planning Mode and create implementation plan
- `/tdd [feature]` - Execute test-driven development cycle
- `/checkpoint [name]` - Create git checkpoint before risky operations

### Command Workflow

**Typical feature workflow**:
```
1. /spec user-authentication
   → Ask clarifying questions
   → Create SPEC.md with minimal scope
   → Get approval

2. /plan user-authentication
   → Enter Planning Mode (Shift+Tab×2)
   → Create detailed task breakdown
   → Get approval
   → Create git checkpoint

3. /tdd implement-jwt-tokens
   → Write failing tests (RED)
   → Implement minimal solution (GREEN)
   → Refactor with tests passing
   → Commit

4. Repeat step 3 for each task

5. Run quality gate before final commit
```

### Using Commands

**Syntax**:
```
/command [arguments]
```

**Examples**:
```
/spec Add password reset functionality
/plan Implement email verification
/tdd User profile creation
/checkpoint before-auth-refactor
```

### Creating Custom Commands

**Location**: `.claude/commands/[name].md`

**Basic structure**:
```markdown
---
description: Brief description of what command does
---

# Command Name

Instructions for Claude to follow when command is invoked.

Use $ARGUMENTS to reference command arguments.
```

**Example** (`.claude/commands/review.md`):
```markdown
---
description: Review code for quality issues
---

# Code Review

Review the code in $ARGUMENTS for:

1. Code quality issues
2. Test coverage gaps
3. Security vulnerabilities
4. Performance concerns

Provide actionable feedback with specific line numbers.
```

### Command Best Practices

**DO**:
- Create commands for repeated workflows
- Use clear, descriptive names
- Document arguments clearly
- Check commands into git for team sharing
- Keep commands focused (one purpose)

**DON'T**:
- Create commands for one-off tasks
- Mix multiple concerns in one command
- Assume context without loading it
- Skip validation steps
- Hardcode project-specific paths

### Team Command Library

**Check `.claude/commands/` into git** so entire team uses standardized workflows.

**Common team commands**:
- `/commit` - Create conventional commit
- `/pr` - Create pull request with description
- `/fix-issue [number]` - Fix GitHub issue by number
- `/optimize [file]` - Optimize code performance
- `/security-audit` - Run security analysis
- `/add-docs [file]` - Generate documentation

---

## 🎨 Code Style Guide

### Python Style

**Imports**:
```python
# Standard library
import os
import sys
from typing import Dict, List, Optional

# Third-party
import pytest
from anthropic import Anthropic

# Local
from mcp_servers.memory_mcp import MemoryMCP
```

**Function Length**:
- Maximum 50 lines per function
- If longer, break into smaller functions
- Each function should do ONE thing

**Line Length**:
- Maximum 100 characters
- Break long lines at logical points

**Type Hints**:
```python
# Always use type hints
def process_data(
    data: Dict[str, any],
    options: Optional[List[str]] = None
) -> Dict[str, bool]:
    """Process data with optional filters."""
    # Implementation
```

---

## 🚀 Building and Distribution

### Building Package

```bash
# Run packaging script
./package_toolkit.sh

# Creates:
# dist/best-practice-toolkit-v1.0.0.tar.gz
# dist/best-practice-toolkit-v1.0.0.zip
```

### Version Management

**Version format**: MAJOR.MINOR.PATCH (semantic versioning)

**Version increments**:
- MAJOR: Breaking changes
- MINOR: New features (backward compatible)
- PATCH: Bug fixes

**Current version**: 1.0.0 (stored in package_toolkit.sh)

---

## ⚡ Performance Guidelines

### MCP Tool Calls

**Target**: <100ms per tool call

**Optimization strategies**:
- Cache frequently accessed data
- Use async operations for I/O
- Minimize file system operations
- Batch operations when possible

### Quality Gate Execution

**Target**: <5 seconds for full quality gate

**Parallelization**:
```bash
# Run quality gate (handles all checks)
bash .claude/quality-gate/check_quality.sh
```

---

## 🔐 Security Considerations

### Secrets Management

**Never commit**:
- API keys
- Passwords
- Tokens
- Private keys

**Use environment variables**:
```python
import os

API_KEY = os.getenv("ANTHROPIC_API_KEY")
if not API_KEY:
    raise ValueError("ANTHROPIC_API_KEY not set")
```

### Input Validation

**Always validate user input**:
```python
def validate_project_path(path: str) -> bool:
    """Validate project path."""
    if not path or not path.strip():
        raise ValueError("Project path cannot be empty")

    if not os.path.isabs(path):
        raise ValueError("Project path must be absolute")

    return True
```

---

## 📚 Reference Documentation

**Always keep updated**:
- docs/notes/PROJECT_PLAN.md - Current status and roadmap
- docs/README.md - Comprehensive system documentation
- .claude/mcp-servers/README.md - MCP installation and usage
- tests/README.md - Testing documentation

**Review before starting work**:
- docs/design/MCP_IMPLEMENTATION_APPROACH.md - System design
- docs/guides/RETROFIT_METHODOLOGY.md - Retrofit process
- .claude/best-practice.md - This file (injected standards)

**Note**: When toolkit is injected into your project, all standards are in `.claude/` folder which is automatically gitignored.

---

## ✅ Pre-Commit Checklist

Before committing ANY code:

- [ ] **GitHub issue created** (for code changes going to GitHub)
- [ ] **Commit message references issue number** (e.g., "Closes #42")
- [ ] All tests pass (`pytest tests/ -v`)
- [ ] No linting errors (run quality gate)
- [ ] No type errors (run quality gate)
- [ ] No security issues (run quality gate)
- [ ] Structure compliance (≤5 root folders)
- [ ] Documentation updated (if API changed)
- [ ] docs/notes/PROJECT_PLAN.md updated (if status changed)
- [ ] Commit message follows format
- [ ] Changes are ≤30 lines (or checkpointed)

---

## 🎯 Success Metrics

Track these metrics to ensure quality:

**Code Quality**:
- Test coverage ≥80%
- Zero linting errors
- Zero type errors
- Zero security vulnerabilities

**Structure**:
- Root folders ≤5
- All docs in docs/
- No forbidden files in root

**Process**:
- Commit frequency (daily minimum)
- Quality gate pass rate (target: 100%)
- Task size compliance (≤30 lines)

---

**Last Updated**: 2025-10-30 (Discovery-First Framework integrated)
**Review Frequency**: After every major feature or monthly
**Applies To**: All AI assistants working on this project

---

## 🎯 The Discovery-First Principle

> **"The plan truly is the prompt"** - Ten minutes defining boundaries saves hours of implementation drift.

This CLAUDE.md embodies the Discovery-First Framework:

1. **Planning Mode (Shift+Tab×2)** is NON-NEGOTIABLE for new features
2. **Ask questions first** - Never start coding with unclear requirements
3. **60% context rule** - Proactively manage context before hitting limits
4. **TDD cycle** - Write tests first, see them fail, make them pass
5. **Atomic tasks** - Each ≤30 lines, testable, independent
6. **Git checkpoints** - Fearless exploration with instant rollback
7. **Slash commands** - Automate workflows (/spec, /plan, /tdd)
8. **Anti-patterns** - Learn from common failures
9. **Problem-solving techniques** - MANDATORY systematic debugging (no random changes)

The best code is written while you're not watching—if you've defined what you want clearly first.
