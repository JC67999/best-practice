# MCP Usage Examples

> **Purpose**: Practical examples showing when and how to manually request MCP tool usage
> **Last Updated**: 2025-10-30
> **Audience**: Users working with Claude Code on projects with MCP servers installed

---

## Overview

While CLAUDE.md contains directives for AI assistants to automatically invoke MCP tools, there are times when you (the user) need to explicitly request MCP operations. This guide provides examples of when and how to do that.

---

## Session Start Examples

### Example 1: Starting Fresh Work Session

**You say**:
```
"Load the project context and show me where we left off"
```

**What happens**:
1. Claude calls `load_project_context` → Gets objective, decisions, history
2. Claude calls `get_current_status` → Gets current tasks and progress
3. Claude shows you:
   - Project objective and clarity score
   - Recent session summaries
   - Pending tasks
   - Decisions made previously

**Expected output**:
```
Project: Best Practice Toolkit
Objective: Enforce excellent coding practices... (clarity: 80/100)

Last session: Testing MCP server functionality
Decisions: Use MCP tools to test the system

Current status:
- 3 tasks total
- 0 completed
- 3 pending
- Next: [details of next task]
```

---

### Example 2: Starting After Long Break

**You say**:
```
"I haven't worked on this in a week. What was I doing?"
```

**What happens**:
1. Claude calls `load_project_context`
2. Shows recent session summaries (sorted by date)
3. Shows next steps from last session
4. Shows any blockers that were recorded

---

## Task Validation Examples

### Example 3: Before Starting New Feature

**You say**:
```
"I want to add a dark mode toggle. Does this align with our objective?"
```

**What happens**:
1. Claude calls `validate_task_alignment` with task description
2. Gets alignment score (0-100)
3. Interprets result:
   - Score ≥70: "This aligns well (score: 85). Let's proceed."
   - Score <70: "This has low alignment (score: 45). This doesn't serve the core objective. Should we defer this?"

**Expected output (aligned)**:
```
Alignment check: 85/100 ✓

This task serves the objective because:
- Improves user experience (success metric)
- Aligns with UI component development (solution)

Task is aligned. Should we proceed?
```

**Expected output (misaligned)**:
```
Alignment check: 35/100 ✗

This task does NOT strongly serve the objective:
- Not mentioned in success metrics
- Doesn't address core problem
- Could be deferred to v2

Recommendation: Focus on objective-critical work first.
Should we proceed anyway?
```

---

### Example 4: Checking If Task Is Too Large

**You say**:
```
"Validate that implementing user profiles is small enough"
```

**What happens**:
1. Claude calls `validate_task_size` with task description
2. Gets estimated lines of code
3. If >30 lines, suggests breaking down

**Expected output**:
```
Task size check: ~120 lines ✗

This task is too large (target: ≤30 lines)

Suggested breakdown:
1. Create user profile data model (≤30 lines)
2. Add profile API endpoints (≤30 lines)
3. Create profile UI component (≤30 lines)
4. Add profile tests (≤30 lines)

Which sub-task should we start with?
```

---

## Quality Gate Examples

### Example 5: Before Committing

**You say**:
```
"Run the quality gate before we commit"
```

**What happens**:
1. Claude calls `run_quality_gate` with list of changed files
2. Runs all quality checks (tests, linting, types, security)
3. Reports PASS or FAIL with details

**Expected output (PASS)**:
```
Quality Gate: PASS ✓

✓ Tests: 45/45 passing (coverage: 85%)
✓ Linting: 0 errors (ruff)
✓ Type checking: 0 errors (mypy)
✓ Security: 0 issues (bandit)
✓ Structure: Compliant

Ready to commit.
```

**Expected output (FAIL)**:
```
Quality Gate: FAIL ✗

✗ Tests: 3 failing
  - test_auth.py::test_login_invalid
  - test_auth.py::test_password_hash
  - test_profile.py::test_update

✗ Linting: 2 errors
  - auth.py:45 - Unused import 'os'
  - profile.py:12 - Line too long (105 chars)

✓ Type checking: PASS
✓ Security: PASS
✓ Structure: PASS

Cannot commit until issues are fixed.
```

---

### Example 6: Checking Specific Files

**You say**:
```
"Check code quality for auth.py and profile.py"
```

**What happens**:
1. Claude calls `check_code_quality` with specific file paths
2. Runs quality checks on just those files
3. Reports issues found

---

## Structure Validation Examples

### Example 7: Audit Project Structure

**You say**:
```
"Check if our project structure is compliant"
```

**What happens**:
1. Claude calls `audit_project_structure`
2. Checks root folder count (target: ≤5)
3. Checks for forbidden folders in root
4. Returns compliance score

**Expected output**:
```
Structure Audit: 40/100 ⚠️

Violations:
- Too many root folders: 6 (target: 5)
  Found: mcp-servers, logs, tests, docs, dist, retrofit-tools

- Forbidden folder: logs/
  Suggestion: Move to artifacts/logs/

- Missing: artifacts/ folder
  Suggestion: Create artifacts/ directory

Recommendations:
1. Move logs/ to artifacts/logs/
2. This will bring root folders to 5 (compliant)
```

---

### Example 8: Check File Placement

**You say**:
```
"Are all our files in the right locations?"
```

**What happens**:
1. Claude calls `validate_file_placement`
2. Checks each file against placement rules
3. Reports misplaced files

**Expected output**:
```
File Placement: 40/100 ⚠️

Violations:
- autonomous_daemon.py (root) → Move to src/ or temp/
- learning_daemon.py (root) → Move to src/ or temp/
- code_review_daemon.py (root) → Move to src/ or temp/

Compliant files:
✓ mcp-servers/*.py
✓ docs/**/*.md
✓ tests/**/*.py
```

---

## Development Workflow Examples

### Example 9: Check Priority

**You say**:
```
"Challenge the priority of implementing email notifications"
```

**What happens**:
1. Claude calls `challenge_task_priority` with task
2. Compares to other pending tasks
3. Determines if it's highest priority

**Expected output**:
```
Priority Challenge: ⚠️

Task: Implement email notifications
Priority: MEDIUM

Higher priority tasks exist:
1. Fix authentication bug (CRITICAL)
2. Add password reset (HIGH)

Recommendation: Complete higher priority tasks first.

Should we proceed with email notifications anyway?
```

---

### Example 10: Detect Scope Creep

**You say**:
```
"Run scope creep detection"
```

**What happens**:
1. Claude calls `identify_scope_creep`
2. Analyzes all pending tasks against objective
3. Identifies tasks that don't serve objective

**Expected output**:
```
Scope Creep Detection:

Non-essential tasks found:
1. Add animated splash screen (alignment: 25/100)
   → Doesn't serve core objective
   → Recommend: Defer to v2

2. Implement social media sharing (alignment: 30/100)
   → Not in success metrics
   → Recommend: Cut or defer

Essential tasks (keep):
✓ Implement user authentication (95/100)
✓ Add quality gate integration (90/100)
✓ Create objective clarification flow (88/100)

Recommendation: Cut 2 non-essential tasks, focus on 3 essential.
```

---

## Session End Examples

### Example 11: Save Session Summary

**You say**:
```
"Save a session summary before we end"
```

**What happens**:
1. Claude summarizes what was done
2. Lists decisions made
3. Lists next steps
4. Calls `save_session_summary`

**Expected output**:
```
Session Summary:

Accomplished:
- Updated CLAUDE.md with mandatory MCP usage directives
- Created MCP usage examples documentation
- Tested all three MCP servers

Decisions:
- Add enforcement rules to CLAUDE.md
- Create examples documentation in docs/guides/
- Use hooks for automatic MCP invocation

Next steps:
- Create Claude Code hooks configuration
- Test hooks in practice
- Update PROJECT_PLAN.md

Blockers: None

✓ Summary saved to project memory
```

---

### Example 12: Save Important Decision

**You say**:
```
"Save the decision to use JWT tokens for authentication"
```

**What happens**:
1. Claude calls `save_decision` with decision + rationale
2. Stores in project memory
3. Available for future context loading

**Expected output**:
```
Decision saved:

Decision: Use JWT tokens for authentication
Rationale:
- Stateless (no session storage needed)
- Industry standard
- Easy to implement with existing libraries
- Supports mobile clients

✓ Stored in project memory
```

---

## Objective Management Examples

### Example 13: Check Objective Clarity

**You say**:
```
"What's our objective clarity score?"
```

**What happens**:
1. Claude calls `score_objective_clarity`
2. Returns score (0-100) and weak areas

**Expected output**:
```
Objective Clarity: 80/100

Strengths:
✓ Problem statement: Clear (90/100)
✓ Target users: Well-defined (85/100)
✓ Solution: Specific (80/100)

Weak areas:
⚠️ Success metrics: Could be more measurable (70/100)
⚠️ Constraints: Vague (65/100)

Recommendation: Refine success metrics and constraints to reach 85+
```

---

### Example 14: Refocus on Objective

**You say**:
```
"Review all tasks and cut anything that doesn't serve the objective"
```

**What happens**:
1. Claude calls `refocus_on_objective`
2. Reviews every pending task
3. Suggests cutting low-alignment tasks

**Expected output**:
```
Objective Refocus:

Reviewed 12 pending tasks

Keep (8 tasks, alignment ≥70):
✓ Task 1: Implement MCP servers (95/100)
✓ Task 2: Add quality gates (90/100)
✓ Task 3: Create retrofit tools (85/100)
[...]

Cut (4 tasks, alignment <70):
✗ Task 9: Add GraphQL API (45/100)
✗ Task 10: Implement real-time sync (40/100)
✗ Task 11: Add AI code suggestions (35/100)
✗ Task 12: Create mobile app (30/100)

Recommendation: Cut 4 tasks, focus on 8 essential tasks.
This will improve delivery speed by ~33%.

Proceed with cuts?
```

---

## Search and Discovery Examples

### Example 15: Search Across Projects

**You say**:
```
"Search my memory for decisions about authentication"
```

**What happens**:
1. Claude calls `search_memory` with query
2. Searches across all tracked projects
3. Returns relevant context

**Expected output**:
```
Memory search: "authentication"

Found in 2 projects:

best-practice:
- Decision (2025-10-29): Use JWT tokens for authentication
  Rationale: Stateless, industry standard, mobile-friendly

document-generator:
- Session (2025-10-28): Implemented OAuth2 authentication
  Decision: Use Auth0 for social login
  Next step: Add email/password fallback
```

---

### Example 16: List All Projects

**You say**:
```
"Show me all projects you're tracking"
```

**What happens**:
1. Claude calls `list_projects`
2. Returns all projects with metadata

**Expected output**:
```
Tracked Projects: 2

1. document-generator
   Path: /home/jc/CascadeProjects/document-generator
   Last activity: 2025-10-29 (today)
   Sessions: 2
   Has objective: Yes

2. best-practice
   Path: /home/jc/CascadeProjects/best-practice
   Last activity: 2025-10-29 (today)
   Sessions: 1
   Has objective: Yes
```

---

## Quick Reference: Common Requests

### At Session Start
```
"Load project context"
"Show me current status"
"What was I working on?"
```

### Before Starting Work
```
"Does [task] align with our objective?"
"Is [task] small enough to implement?"
"What's the highest priority task?"
```

### During Development
```
"Check code quality for [files]"
"Audit project structure"
"Run scope creep detection"
```

### Before Committing
```
"Run quality gate"
"Check if this is ready to commit"
```

### At Session End
```
"Save session summary"
"Save this decision: [decision]"
```

### Objective Management
```
"What's our objective clarity score?"
"Refocus on objective and cut non-essential tasks"
"Create task breakdown from objective"
```

---

## Tips for Effective MCP Usage

### 1. Be Explicit When Needed
While Claude should invoke MCPs automatically (per CLAUDE.md directives), you can always request explicitly:
- "Before we start, validate alignment"
- "Don't commit yet - run quality gate first"

### 2. Use at Decision Points
Request MCP tools when making important decisions:
- "Should we implement [feature]? Check alignment first."
- "Is this the right priority? Challenge it."

### 3. Regular Check-ins
Periodically request scope and priority checks:
- Every 5-10 tasks: "Run scope creep detection"
- Before major features: "Challenge priority"
- After refactoring: "Audit structure"

### 4. End-of-Day Ritual
Always save context before ending:
- "Save session summary with decisions and next steps"
- Ensures continuity for next session

### 5. Use Search for Context
When uncertain about past decisions:
- "Search memory for decisions about [topic]"
- Avoid repeating past discussions

---

## When Claude Should Use MCPs Automatically

According to CLAUDE.md, these should happen WITHOUT you asking:

**Automatic at session start**:
- Load project context
- Get current status

**Automatic before implementing**:
- Validate task alignment
- Validate task size

**Automatic before completion**:
- Run quality gate
- Never commit on failed quality gate

**Automatic at session end**:
- Save session summary

**If Claude isn't doing these automatically**, remind them:
- "Follow CLAUDE.md standards for MCP usage"
- "You should validate alignment before implementing"
- "Run quality gate before committing per CLAUDE.md"

---

## Troubleshooting

### Claude Not Using MCPs Automatically

**Problem**: Claude implements features without checking alignment

**Solution**: Say:
```
"Per CLAUDE.md, you must validate task alignment before implementing.
Please check alignment for [task] now."
```

---

### Quality Gate Failures

**Problem**: Quality gate fails but you need to commit

**Solution**: Don't override - fix the issues:
```
"Quality gate failed. Let's fix the issues one by one:
1. First fix failing tests
2. Then fix linting errors
3. Re-run quality gate
4. Only commit when it passes"
```

---

### Low Alignment Score

**Problem**: Task has alignment score <70

**Solution**: Either defer or refine:
```
Option 1 (defer): "Let's skip this and focus on higher-alignment tasks"
Option 2 (refine): "Can we refine this task to better serve the objective?"
Option 3 (override): "I understand it's low alignment, but let's proceed anyway"
```

---

**Last Updated**: 2025-10-30
**Related Docs**: CLAUDE.md (mandatory directives), mcp-servers/README.md (installation)
