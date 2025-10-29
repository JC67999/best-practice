# Autonomous Daemon - Usage Guide

> **Status**: Phase 3 Complete - MCP Integration
> **Last Updated**: 2025-10-29
> **Prerequisites**: Python 3.10+, Git, PROJECT_PLAN.md with ready tasks

---

## Quick Start

### 1. Prepare Your Project

Ensure your project has:
- ✅ `docs/notes/PROJECT_PLAN.md` with defined objective
- ✅ Tasks marked as "Ready for Autonomous Execution"
- ✅ `.ai-validation/check_quality.sh` (quality gate script)
- ✅ Git repository initialized

### 2. Mark Tasks as Ready

Edit `PROJECT_PLAN.md` and move tasks to the Ready section:

```markdown
### Ready for Autonomous Execution ✅

→ **[task_1]** Add email validation function
  - Alignment score: 88/100 ✅
  - Estimated lines: 12 ✅
  - Tests defined: ✅ Yes (tests/test_validators.py)
  - Safety check: ✅ Pure function, no external calls
  - Status: READY
  - Auto-approved: 2025-10-29 22:00
```

### 3. Run Daemon

```bash
# Dry run first (see what would execute)
python3 autonomous_daemon.py /path/to/project --dry-run

# Execute up to 5 tasks
python3 autonomous_daemon.py /path/to/project

# Limit number of tasks
python3 autonomous_daemon.py /path/to/project --max-tasks 3
```

---

## Command Line Options

```
usage: autonomous_daemon.py [-h] [--max-tasks MAX_TASKS] [--dry-run]
                            project_path

Autonomous Execution Daemon - Safe overnight task execution

positional arguments:
  project_path          Absolute path to project directory

options:
  -h, --help            show this help message and exit
  --max-tasks MAX_TASKS
                        Maximum tasks per session (default: 5)
  --dry-run             Dry run - load tasks but don't execute
```

---

## Workflow

### Before Bed (10:00 PM)

1. **Review PROJECT_PLAN.md**
   - Ensure objective is defined
   - Check that tasks are well-defined

2. **Move Tasks to Ready Section**
   - Select 3-5 tasks that meet safety criteria
   - Ensure each task:
     - Has alignment score ≥80
     - Is ≤30 lines
     - Has tests defined (or is a test task)
     - Contains no forbidden operations

3. **Start Daemon**
   ```bash
   cd /path/to/project
   python3 /path/to/best-practice/autonomous_daemon.py $(pwd)
   ```

4. **Go to Sleep** 😴

### During Night (Autonomous Execution)

For each task, the daemon:

1. **Loads** task from PROJECT_PLAN.md
2. **Validates** safety (checks forbidden patterns)
3. **Creates** git checkpoint
4. **Executes** task (currently simulated - needs Claude Code CLI)
5. **Runs** quality gate
6. **Decision**:
   - ✅ PASS → Commit changes, mark complete
   - ❌ FAIL → Rollback to checkpoint, log failure
7. **Repeats** until max tasks reached or 2 consecutive failures

### Morning (8:00 AM)

1. **Check Session Log**
   ```bash
   cat logs/autonomous-session-YYYYMMDD-HHMMSS.log
   ```

2. **Review Changes**
   ```bash
   git log --oneline --since="yesterday"
   git diff HEAD~5  # Review last 5 commits
   ```

3. **Validate Quality**
   - All tests should pass (daemon ensures this)
   - Review code for correctness
   - Check that changes match task descriptions

4. **Next Steps**:
   - If satisfied: Continue with more tasks tonight
   - If issues: Fix and refine task descriptions
   - Move more tasks to Ready queue

---

## Safety Features

### Automatic Safety Checks

The daemon automatically blocks tasks that:

❌ **Modify forbidden files**:
- `.env` files
- `docker-compose.yml`, `Dockerfile`
- `.github/workflows/` (CI/CD)
- `requirements.txt`, `package.json` (dependencies)
- `.gitignore`

❌ **Contain dangerous operations**:
- "delete file", "remove file"
- "drop table", "truncate"
- "add dependency", "install package"
- "payment", "stripe"
- "push to remote"

❌ **Modify unapproved directories**:
- Files outside `src/`, `tests/`, `docs/`, `mcp-servers/`

### Auto-Rollback Triggers

Automatic rollback occurs when:
- ❌ Quality gate fails (tests, linting, types, security)
- ❌ Git commit fails
- ❌ Any exception during execution
- ❌ Safety validation detects violations

### Session Limits

- **Max tasks**: 5 per session (configurable)
- **Consecutive failures**: Stops after 2
- **Task timeout**: 30 minutes per task
- **Session timeout**: 4 hours total

---

## Configuration

### Default Configuration

```python
{
    "max_tasks_per_session": 5,
    "timeout_per_task": 1800,  # 30 minutes
    "max_session_duration": 14400,  # 4 hours
    "stop_on_consecutive_failures": 2
}
```

### Customizing (Future)

Edit `autonomous_daemon.py` or pass config file:

```python
daemon = AutonomousDaemon(
    project_path,
    config={
        "max_tasks_per_session": 10,
        "timeout_per_task": 3600
    }
)
```

---

## Logging

### Session Logs

Location: `logs/autonomous-session-YYYYMMDD-HHMMSS.log`

Example log:
```
2025-10-29 02:00:00 - [INFO] 🤖 Starting autonomous session
2025-10-29 02:00:05 - [INFO] 📋 Found 5 ready tasks
2025-10-29 02:00:10 - [INFO] 📝 Task 1/5: Add email validation
2025-10-29 02:00:15 - [INFO] Checkpoint created: abc123de
2025-10-29 02:05:30 - [INFO] Quality gate: PASS
2025-10-29 02:05:35 - [INFO] Committed: feat: Add email validation
2025-10-29 02:05:40 - [INFO] ✅ Task completed successfully
```

### Memory MCP Integration

Session summaries are saved to Memory MCP:
- Completed tasks
- Failed tasks with reasons
- Next steps (review PR)
- Blockers (if any)

Access via:
```bash
# View project context
# (Would use MCP tool in real usage)
```

---

## Troubleshooting

### Problem: No tasks found

**Solution**: Check PROJECT_PLAN.md format
```markdown
### Ready for Autonomous Execution ✅
These tasks can be executed safely without supervision:

→ **[task_1]** Description here
  - Alignment score: 85/100 ✅
  ...
```

### Problem: Quality gate not found

**Solution**: Ensure `.ai-validation/check_quality.sh` exists
```bash
ls -la .ai-validation/check_quality.sh
```

### Problem: All tasks fail

**Solution**: Run quality gate manually to see issues
```bash
cd .ai-validation
bash check_quality.sh
```

### Problem: MCP servers not available

**Current**: This is expected (daemon includes MCP integration code but servers run separately)

**Future**: Will integrate via MCP protocol when Claude Code CLI supports it

---

## Limitations (Current Version)

### Known Limitations

⚠️ **Task Execution**: Currently simulated
- Daemon creates checkpoint and runs quality gate
- Actual code changes must be done manually (for now)
- Full implementation needs Claude Code CLI integration

⚠️ **MCP Integration**: Partial
- Safety validation code is present
- Memory logging code is present
- Actual MCP calls work when servers are running via protocol

⚠️ **PR Creation**: Not implemented yet
- Commits are created on current branch
- Manual PR creation needed
- Phase 3 feature (planned)

### What Works Now

✅ Task loading from PROJECT_PLAN.md
✅ Git checkpoint creation
✅ Quality gate execution
✅ Automatic rollback
✅ Session logging
✅ Safety validation logic
✅ Session limits

---

## Scheduling (Future)

### Cron Setup

Run daemon every night at 2am:

```bash
# Edit crontab
crontab -e

# Add line:
0 2 * * * /usr/bin/python3 /path/to/autonomous_daemon.py /path/to/project
```

### Systemd Timer (Alternative)

Create `/etc/systemd/system/autonomous-daemon.timer`:

```ini
[Unit]
Description=Autonomous Coding Daemon Timer

[Timer]
OnCalendar=*-*-* 02:00:00
Persistent=true

[Install]
WantedBy=timers.target
```

---

## Best Practices

### Task Preparation

✅ **DO**:
- Write clear, specific task descriptions
- Define tests before marking tasks ready
- Keep tasks ≤30 lines
- Review safety constraints
- Start with simple tasks

❌ **DON'T**:
- Mark vague tasks as ready
- Include multiple changes in one task
- Skip test definitions
- Approve tasks touching authentication without review
- Queue >5 tasks initially

### Morning Review Checklist

After autonomous session:

1. ☑️ Check session log for errors
2. ☑️ Review all commits
3. ☑️ Run tests manually (`pytest`)
4. ☑️ Verify changes match task descriptions
5. ☑️ Check for unexpected file modifications
6. ☑️ Ensure code follows project standards
7. ☑️ Test functionality manually (if applicable)

### Quality Assurance

- Always review autonomous work before merging
- Don't blindly trust passing quality gates
- Verify logic correctness, not just syntax
- Check edge cases and error handling
- Ensure no security issues introduced

---

## Examples

### Example 1: Simple Function Addition

**Task in PROJECT_PLAN.md**:
```markdown
→ **[task_5]** Add is_valid_email() helper to validators.py
  - Alignment score: 92/100 ✅
  - Estimated lines: 8 ✅
  - Tests defined: ✅ Yes (tests/test_validators.py)
  - Safety check: ✅ Pure function, regex validation only
  - Status: READY
```

**Expected Result**:
- Function added to `src/validators.py`
- Tests added to `tests/test_validators.py`
- Quality gate passes
- Committed with message: "feat: Add is_valid_email() helper"

### Example 2: Documentation Update

**Task**:
```markdown
→ **[task_8]** Add usage examples to README.md
  - Alignment score: 85/100 ✅
  - Estimated lines: 20 ✅
  - Tests defined: ✅ N/A (documentation)
  - Safety check: ✅ Documentation only
  - Status: READY
```

**Expected Result**:
- Examples added to README.md
- No tests needed (documentation)
- Committed

---

## Success Metrics

Track these to validate autonomous mode:

### Performance
- **Success rate**: % of tasks completed (target: ≥85%)
- **Rollback rate**: % of tasks rolled back (target: ≤15%)
- **Tasks per night**: Average completed (target: 3-5)

### Quality
- **Quality gate pass rate**: First-time pass (target: ≥90%)
- **Bug introduction rate**: Bugs found post-merge (target: <5%)
- **Test coverage**: Maintained or improved (target: ≥80%)

### Productivity
- **Features shipped**: Per week increase (target: 3-5x)
- **Review time**: Time to review PRs (target: <30 min)
- **Morning surprises**: Unexpected issues (target: <10%)

---

## Support

### Getting Help

- Review `docs/autonomous-constraints.md` for safety rules
- Check `docs/analysis/AUTONOMOUS_TESTING_RESULTS.md` for test results
- See `docs/guides/AUTONOMOUS_MODE_ROADMAP.md` for implementation plan

### Reporting Issues

If daemon fails:
1. Check session log in `logs/`
2. Review git status and recent commits
3. Run quality gate manually
4. Check PROJECT_PLAN.md format
5. Verify task descriptions meet safety criteria

---

**Last Updated**: 2025-10-29
**Version**: Phase 3 (MCP Integration Complete)
**Status**: Functional prototype with safety features
**Next**: Phase 4 - Full Claude Code CLI integration
