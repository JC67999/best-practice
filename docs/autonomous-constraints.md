# Autonomous Mode Constraints

> **Purpose**: Define safe operational boundaries for autonomous task execution
> **Last Updated**: 2025-10-29
> **Status**: Active

---

## Overview

Autonomous mode allows Claude Code to execute pre-approved tasks overnight without supervision. This document defines strict safety constraints to prevent dangerous operations while maintaining productivity.

**Key Principle**: Better to skip a task than break something.

---

## What Autonomous Mode CAN Do ✅

### Code Operations
- ✅ Implement functions ≤30 lines
- ✅ Add unit tests
- ✅ Add docstrings to existing code
- ✅ Refactor small functions (≤30 lines)
- ✅ Fix linting errors
- ✅ Add type hints
- ✅ Fix simple bugs (well-defined, ≤30 lines)

### Documentation Operations
- ✅ Update README with new features
- ✅ Add CHANGELOG entries
- ✅ Update API documentation
- ✅ Add inline comments
- ✅ Create usage examples

### File Operations
- ✅ Create new files in approved directories (src/, tests/, docs/)
- ✅ Modify existing files (with git checkpoint backup)
- ✅ Move files within approved directories

### Git Operations
- ✅ Create commits on feature branch
- ✅ Create feature branch for autonomous work
- ✅ Tag checkpoints for rollback

---

## What Autonomous Mode CANNOT Do ❌

### Forbidden Operations - Will Block Execution

#### File Deletions
- ❌ Delete any files
- ❌ Remove directories
- ❌ Clear file contents

#### Configuration Changes
- ❌ Modify production configuration files
- ❌ Change .env files
- ❌ Modify .gitignore
- ❌ Change CI/CD pipelines (.github/workflows/)
- ❌ Modify Docker configuration (docker-compose.yml, Dockerfile)

#### Database Operations
- ❌ Change database schema
- ❌ Create/drop tables
- ❌ Modify migrations
- ❌ Execute raw SQL with DELETE/DROP/TRUNCATE

#### Dependency Management
- ❌ Add new dependencies (requirements.txt, package.json)
- ❌ Update dependency versions
- ❌ Install new packages

#### Security-Sensitive Operations
- ❌ Modify authentication code (without approval)
- ❌ Change security middleware
- ❌ Modify API key handling
- ❌ Touch payment processing code

#### External Interactions
- ❌ Make API calls to external services
- ❌ Send emails or notifications
- ❌ Upload/download files from external sources
- ❌ Execute network requests (except package installs via approval)

#### Git Operations
- ❌ Commit to main/master branch
- ❌ Push to remote repository
- ❌ Force push
- ❌ Rewrite history (rebase, amend without approval)
- ❌ Merge branches

---

## Requires Human Approval ⏳

These operations need review before autonomous execution:

### Code Changes
- ⏳ Tasks >30 lines (must be broken down)
- ⏳ Refactoring affecting multiple files
- ⏳ Changes to authentication/authorization logic
- ⏳ API endpoint modifications

### Architecture
- ⏳ Architectural changes or patterns
- ⏳ Adding new modules or services
- ⏳ Database schema changes
- ⏳ API contract changes

### Dependencies
- ⏳ Adding new dependencies
- ⏳ Upgrading major versions
- ⏳ Changing build configuration

### External Integrations
- ⏳ Adding third-party services
- ⏳ Payment processing changes
- ⏳ Authentication provider changes

---

## Quality Requirements (All Must Pass) ✅

Every autonomous task must meet these criteria:

### Pre-Execution Validation
1. ✅ **Alignment Score** ≥80 (task serves project objective)
2. ✅ **Estimated Lines** ≤30 (small, manageable changes)
3. ✅ **Tests Defined** (or task IS writing tests)
4. ✅ **No Forbidden Operations** (checked against patterns)
5. ✅ **Git Checkpoint Created** (for rollback)

### Post-Execution Validation
1. ✅ **All Tests Pass** (pytest, 100% pass rate)
2. ✅ **Quality Gate Pass** (linting, types, security)
3. ✅ **No New Errors** (zero introduced issues)
4. ✅ **Git Commit Successful** (changes recorded)
5. ✅ **Alignment Still Valid** (re-check after completion)

### Coverage Requirements
- Minimum 80% test coverage maintained
- All new functions must have tests
- Edge cases tested

---

## Auto-Rollback Triggers 🔄

Autonomous mode automatically rolls back to last checkpoint if:

### Quality Failures
- ❌ Any test fails
- ❌ Quality gate fails (linting, types, security)
- ❌ Coverage drops below 80%
- ❌ New linting errors introduced
- ❌ New type errors introduced
- ❌ Security vulnerabilities detected

### Execution Failures
- ❌ Task takes >30 minutes (timeout)
- ❌ No progress after 3 attempts
- ❌ Exception during execution
- ❌ Git operations fail

### Safety Violations
- ❌ Forbidden operation detected
- ❌ File outside approved directories
- ❌ Unapproved dependency added

**Rollback Process**:
1. Log failure details
2. Execute `git reset --hard <checkpoint>`
3. Execute `git clean -fd`
4. Mark task as FAILED in PROJECT_PLAN.md
5. Move to next task (or stop if 2 consecutive failures)

---

## Session Limits 🔒

To prevent runaway execution and control costs:

### Task Limits
- **Max tasks per session**: 5 tasks
- **Max attempts per task**: 3 attempts
- **Stop condition**: 2 consecutive failures

### Time Limits
- **Max session duration**: 4 hours total
- **Max task duration**: 30 minutes per task
- **Timeout action**: Auto-rollback and move to next

### Cost Controls
- Session terminates after max tasks reached
- All limits configurable in daemon config
- Summary report generated for morning review

---

## Safety Checks Before Execution 🛡️

Before each autonomous task execution:

### 1. Create Safety Checkpoint
```bash
# Create feature branch if not exists
git checkout -b autonomous-YYYYMMDD-HHMMSS

# Commit current state
git add .
git commit -m "checkpoint: before task_X"

# Record commit hash for rollback
CHECKPOINT_HASH=$(git rev-parse HEAD)
```

### 2. Validate Task Safety
- Check alignment score ≥80
- Verify estimated lines ≤30
- Confirm tests exist (or task is writing tests)
- Scan for forbidden patterns
- Validate file paths in approved directories

### 3. Load Context
- Read PROJECT_PLAN.md (objective, constraints)
- Load Memory MCP context (past sessions)
- Review tech reference (patterns, conventions)
- Read CLAUDE.md (project standards)

### 4. Execute with Monitoring
- Run with 30-minute timeout
- Capture all output (stdout, stderr)
- Monitor for error patterns
- Track progress

---

## After Each Task ✅

### 1. Run Full Quality Gate
```bash
cd .ai-validation
bash check_quality.sh
```

Must pass:
- All tests (pytest)
- Linting (ruff)
- Type checking (mypy)
- Security (bandit)
- Structure compliance

### 2. Decision Point

**If PASS**:
```bash
git add .
git commit -m "feat: <task description>"
# Mark task COMPLETE in PROJECT_PLAN.md
# Update Memory MCP with completion
# Proceed to next task
```

**If FAIL**:
```bash
git reset --hard $CHECKPOINT_HASH
git clean -fd
# Mark task FAILED in PROJECT_PLAN.md
# Log failure reason
# Proceed to next task (or stop if 2nd consecutive failure)
```

---

## File Path Restrictions 📁

### Approved Directories
Tasks can only modify files in:
- `src/` - Source code
- `tests/` - Test files
- `docs/` - Documentation
- `mcp-servers/` - MCP server code (this project)

### Forbidden Directories
Cannot touch files in:
- `.git/` - Git internals
- `.github/` - CI/CD configuration
- `.env*` - Environment files
- `node_modules/` - Dependencies
- `venv/`, `.venv/` - Virtual environments
- `dist/`, `build/` - Build artifacts (unless rebuilding)

### Root Directory
- Can read root files (README.md, CLAUDE.md)
- Cannot modify root files without approval
- Cannot create new root files

---

## Forbidden Code Patterns 🚫

Tasks are blocked if they contain:

### Dangerous SQL
- `DROP TABLE`
- `TRUNCATE`
- `DELETE FROM` (without WHERE clause)
- `ALTER TABLE` (schema changes)

### Dangerous File Operations
- `os.remove()`, `shutil.rmtree()`
- `unlink()`, `rmdir()`
- Writing to `.env` files

### Network Operations
- `requests.post()` to external APIs (without approval)
- `urllib.request.urlopen()` (without approval)
- `socket` operations

### Subprocess Execution
- `subprocess.run(['rm', ...])` (file deletion)
- `os.system()` with dangerous commands
- Shell injection patterns

---

## Task Approval Workflow 📋

### Marking Tasks as READY

To approve a task for autonomous execution:

1. **Review Task Details**
   ```markdown
   - **[task_5]** Add password hashing function
     - Alignment score: 92/100 ✅
     - Estimated lines: 15 ✅
     - Tests defined: ✅ Yes (tests/unit/test_auth.py)
     - Safety check: ✅ Uses bcrypt (approved dependency)
     - Status: PENDING
   ```

2. **Validate Safety**
   - Check no forbidden operations
   - Verify tests exist
   - Confirm alignment score ≥80
   - Ensure size ≤30 lines

3. **Move to Ready Section**
   ```markdown
   ### Ready for Autonomous Execution ✅

   → **[task_5]** Add password hashing function
     - Alignment score: 92/100
     - Estimated lines: 15
     - Tests defined: ✅ Yes (tests/unit/test_auth.py)
     - Safety check: ✅ Uses bcrypt (approved dependency)
     - Status: READY
     - Auto-approved: 2025-10-29 22:00
   ```

4. **Run Autonomous Daemon**
   ```bash
   python autonomous_daemon.py /path/to/project
   ```

---

## Emergency Stop 🛑

### Manual Intervention Required If:

- More than 2 consecutive task failures
- Quality gate consistently failing
- Unexpected system behavior
- Resource exhaustion (disk, memory)

### How to Stop:
1. Kill daemon process (Ctrl+C or `kill <pid>`)
2. Review last commit: `git log -1`
3. Check for damage: `git diff <checkpoint-hash>`
4. Rollback if needed: `git reset --hard <checkpoint-hash>`
5. Review session log: `logs/autonomous-session-YYYYMMDD.log`

---

## Monitoring & Logging 📊

### Session Log Format
```
2025-10-29 02:00:00 - Session started
2025-10-29 02:00:05 - Loaded 5 ready tasks
2025-10-29 02:00:10 - Created branch: autonomous-20251029-020000
2025-10-29 02:00:15 - Task 1/5: Add password hashing function
2025-10-29 02:05:30 - Quality gate: PASS
2025-10-29 02:05:35 - Committed: abc123f
2025-10-29 02:05:40 - Task 2/5: Add login endpoint validation
...
2025-10-29 02:45:00 - Session complete: 5/5 tasks successful
2025-10-29 02:45:05 - Created PR: #123
```

### What Gets Logged
- All task executions (start, end, duration)
- Quality gate results (pass/fail with details)
- Rollback events (reason, checkpoint)
- Error messages and stack traces
- Git operations (commits, branch creation)

---

## Success Metrics 📈

Track these metrics to validate autonomous mode:

### Performance Metrics
- **Success rate**: % of tasks completed successfully (target: ≥85%)
- **Rollback rate**: % of tasks rolled back (target: ≤15%)
- **Average tasks per session**: How many tasks completed (target: 3-5)
- **Time per task**: Average execution time (target: 5-15 minutes)

### Quality Metrics
- **Quality gate pass rate**: First-time pass rate (target: ≥90%)
- **Test coverage**: Maintained or improved (target: ≥80%)
- **Bug introduction rate**: Bugs found post-merge (target: <5%)

### Value Metrics
- **Productivity multiplier**: Features shipped per week increase (target: 3-5x)
- **Code review time**: Time to review autonomous PRs (target: <30 min)
- **Morning surprise factor**: Unexpected issues on wake-up (target: <10%)

---

## Example Task Flows

### ✅ Good Task - Will Execute

```markdown
→ **[task_12]** Add email validation helper function
  - Alignment score: 88/100 ✅ (serves user registration objective)
  - Estimated lines: 12 ✅ (well under 30 line limit)
  - Tests defined: ✅ Yes (tests/unit/test_validators.py)
  - Safety check: ✅ Pure function, no external calls
  - Status: READY
```

**Why it's safe**:
- Small, focused change (12 lines)
- Tests pre-defined
- Pure function (no side effects)
- High alignment with objective
- No forbidden operations

---

### ❌ Bad Task - Will Block

```markdown
→ **[task_15]** Integrate Stripe payment processing
  - Alignment score: 95/100 ✅
  - Estimated lines: 150 ❌ (exceeds 30 line limit)
  - Tests defined: ⏳ Needs definition
  - Safety check: ❌ Requires API keys, external service
  - Status: NOT READY
```

**Why it's blocked**:
- Too large (150 lines > 30 limit)
- No tests defined
- External service integration (forbidden)
- Requires secrets/API keys (dangerous)

**How to fix**:
Break into smaller tasks:
- Task A: Add Stripe config structure (10 lines, no API calls)
- Task B: Add Stripe client wrapper with tests (25 lines, mocked)
- Task C: Add payment intent creation (20 lines, with tests)
Each task must be approved separately.

---

### 🔄 Example Workflow - End-to-End

**Before Bed (10:00 PM)**:
1. Review PROJECT_PLAN.md
2. Move 3-5 tasks to "Ready for Autonomous Execution"
3. Start autonomous daemon: `python autonomous_daemon.py /path/to/project`
4. Go to sleep

**During Night (2:00 AM - 6:00 AM)**:
- Daemon executes tasks sequentially
- Each task: checkpoint → execute → quality gate → commit or rollback
- Creates PR with completed work

**Morning (8:00 AM)**:
1. Review PR created by daemon
2. Check quality (should already pass)
3. Review code changes for correctness
4. Merge if satisfied, or provide feedback
5. Move more tasks to Ready queue for next night

---

## Review Before Merging ☑️

Even though quality gates pass, **ALWAYS REVIEW** autonomous PRs:

### What to Check
1. ✅ All tasks in PR description match what was approved
2. ✅ No unexpected file changes
3. ✅ Code follows project patterns and standards
4. ✅ Tests are meaningful (not just passing)
5. ✅ No TODO comments or incomplete work
6. ✅ Commit messages are clear
7. ✅ No secrets or sensitive data committed

### Red Flags
- 🚩 Files modified outside approved directories
- 🚩 More changes than expected (scope creep)
- 🚩 Tests that don't actually test anything
- 🚩 Commented-out code
- 🚩 Hard-coded values that should be configurable
- 🚩 Missing error handling

---

## Updates to This Document

This constraints document should be updated when:

- New forbidden patterns are discovered
- Quality requirements change
- Session limits need adjustment
- New approval workflows added

**Update process**:
1. Propose change with rationale
2. Test on non-critical project
3. Update this document
4. Notify all users of autonomous mode

---

**Last Updated**: 2025-10-29
**Next Review**: After first 10 autonomous sessions
**Owner**: Project team (human oversight required)
