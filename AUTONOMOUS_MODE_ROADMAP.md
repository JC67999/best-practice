# Autonomous Mode - Implementation Roadmap

> **Objective**: Enable safe autonomous execution that works overnight
> **Expected Outcome**: 5x productivity at near-zero marginal cost
> **Timeline**: 4 weeks to production-ready

---

## Quick Summary

**What We're Building**: A daemon that safely executes pre-approved tasks overnight while maintaining our quality standards.

**Why It's Valuable**:
- Work happens during sleep (8 hours = 8 hours of coding)
- Quality gates prevent bad code
- Objective alignment prevents wasted work
- Auto-rollback prevents breaking things
- Near-zero marginal cost

**Safety**: Multiple tools prove this works, but they're unsafe. We'll build it PROPERLY with our existing quality infrastructure.

---

## Phase 1: Foundation (Week 1)

### Goal: Make PROJECT_PLAN.md autonomous-ready

#### Task 1.1: Enhance PROJECT_PLAN.md Format
**Time**: 2 hours

**Changes**:
```markdown
## 📋 Task Queue

### Ready for Autonomous Execution ✅
These tasks can be executed safely without supervision:

→ **[task_3]** Add User model with email and password fields
  - Alignment score: 95/100
  - Estimated lines: 10
  - Tests defined: ✅ Yes (tests/unit/test_models.py)
  - Safety check: ✅ No dependencies, no DB changes
  - Status: READY
  - Auto-approved: 2025-10-29 10:00

→ **[task_5]** Add password hashing function
  - Alignment score: 92/100
  - Estimated lines: 15
  - Tests defined: ✅ Yes (tests/unit/test_auth.py)
  - Safety check: ✅ Uses bcrypt (approved dependency)
  - Status: READY
  - Auto-approved: 2025-10-29 10:15

### Pending Approval ⏳
These tasks need review before autonomous execution:

- **[task_4]** Implement login endpoint
  - Alignment score: 88/100
  - Estimated lines: 25
  - Tests defined: ⏳ Needs definition
  - Safety check: ⚠️ Touches authentication (needs review)
  - Status: PENDING

### Not Ready ❌
These tasks cannot be executed autonomously:

- **[task_6]** Design database schema
  - Reason: Requires user input and architectural decisions
  - Use: max mode for planning

- **[task_7]** Add Stripe integration
  - Reason: Requires external credentials
  - Use: Manual implementation with user supervision
```

**Deliverable**: Updated PROJECT_PLAN.md template

#### Task 1.2: Define Autonomous Constraints
**Time**: 3 hours

**Create**: `docs/autonomous-constraints.md`

```markdown
# Autonomous Mode Constraints

## What Autonomous Mode CAN Do ✅

### Code Operations
- Implement functions <30 lines
- Add unit tests
- Add docstrings
- Refactor small functions (<30 lines)
- Fix linting errors
- Add type hints

### Documentation Operations
- Update README with features
- Add CHANGELOG entries
- Update API documentation
- Add inline comments

### File Operations
- Create new files in src/, tests/, docs/
- Modify existing files (with backup)
- Move files within approved directories

## What Autonomous Mode CANNOT Do ❌

### Forbidden Operations
- ❌ Delete any files
- ❌ Modify production configuration
- ❌ Change database schema
- ❌ Add new dependencies
- ❌ Modify CI/CD pipelines
- ❌ Touch authentication/security code without approval
- ❌ Make API calls to external services
- ❌ Commit to main branch
- ❌ Push to remote
- ❌ Modify .gitignore, .env files

### Requires Human Approval
- ⏳ Tasks >30 lines
- ⏳ Tasks touching authentication
- ⏳ Tasks requiring new dependencies
- ⏳ Architectural changes
- ⏳ Database migrations
- ⏳ External integrations

## Quality Requirements (All Must Pass)

1. ✅ **Alignment Score** ≥80
2. ✅ **Tests Defined** (or task is writing tests)
3. ✅ **Estimated Lines** ≤30
4. ✅ **No Forbidden Operations**
5. ✅ **Quality Gate Pass** after completion
6. ✅ **Git Commit** successful

## Auto-Rollback Triggers

Autonomous mode auto-rollbacks if:
- ❌ Any test fails
- ❌ Quality gate fails
- ❌ Linting errors introduced
- ❌ Type errors introduced
- ❌ No progress after 3 attempts
- ❌ Task takes >30 minutes

## Session Limits

- Max tasks per session: 5
- Max session duration: 4 hours
- Max attempts per task: 3
- Stop if 2 consecutive failures

## Safety Checks Before Execution

Before each task:
1. Create feature branch (if not exists)
2. Commit current state
3. Validate alignment score ≥80
4. Validate safety constraints
5. Validate tests exist (or task is writing tests)

After each task:
1. Run full quality gate
2. If PASS: commit, mark complete
3. If FAIL: rollback, log failure, move to next
```

**Deliverable**: Autonomous constraints document

#### Task 1.3: Add Safety Checks to Quality MCP
**Time**: 4 hours

**Implementation**:

```python
# Add to quality_mcp.py

def validate_autonomous_safety(
    project_path: str,
    task_description: str,
    file_changes: List[str]
) -> Dict:
    """Validate task is safe for autonomous execution."""

    violations = []

    # Load constraints
    constraints = load_autonomous_constraints(project_path)

    # Check for forbidden operations
    forbidden_patterns = [
        (r'\.env', "Modifying .env file"),
        (r'docker-compose\.yml', "Modifying Docker config"),
        (r'\.github/workflows', "Modifying CI/CD"),
        (r'requirements\.txt', "Adding dependencies"),
        (r'DROP TABLE', "Database schema changes"),
        (r'DELETE FROM', "Dangerous database operations"),
    ]

    for pattern, reason in forbidden_patterns:
        if any(re.search(pattern, f) for f in file_changes):
            violations.append({
                "severity": "CRITICAL",
                "violation": reason,
                "blocked": True
            })

    # Check task description for forbidden words
    forbidden_words = [
        "delete file", "drop table", "remove column",
        "add dependency", "install package", "stripe", "payment"
    ]

    task_lower = task_description.lower()
    for word in forbidden_words:
        if word in task_lower:
            violations.append({
                "severity": "HIGH",
                "violation": f"Task mentions forbidden operation: {word}",
                "blocked": True
            })

    # Check file paths
    for file_path in file_changes:
        # Must be in approved directories
        approved_dirs = ["src/", "tests/", "docs/"]
        if not any(file_path.startswith(d) for d in approved_dirs):
            violations.append({
                "severity": "HIGH",
                "violation": f"File outside approved directories: {file_path}",
                "blocked": True
            })

    return {
        "safe_for_autonomous": len(violations) == 0,
        "violations": violations,
        "can_proceed": len([v for v in violations if v["blocked"]]) == 0
    }
```

**Deliverable**: Safety validation in Quality MCP

#### Task 1.4: Manual Testing
**Time**: 3 hours

**Test Plan**:
1. Create PROJECT_PLAN.md with 3 ready tasks
2. Manually execute each following autonomous constraints
3. Verify quality gates catch issues
4. Verify rollback works
5. Document success rate

**Deliverable**: Test results showing manual workflow works

---

## Phase 2: Prototype Daemon (Week 2)

### Goal: Build working autonomous daemon with safety

#### Task 2.1: Basic Daemon Implementation
**Time**: 8 hours

**Create**: `autonomous_daemon.py`

```python
#!/usr/bin/env python3
"""
Autonomous Execution Daemon - Safe overnight task execution
"""
import asyncio
import json
import os
import subprocess
import time
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional

class AutonomousDaemon:
    """Safe autonomous task execution."""

    def __init__(self, project_path: str, config: Dict):
        self.project_path = Path(project_path)
        self.config = config
        self.session_log = []

    def load_ready_tasks(self) -> List[Dict]:
        """Load tasks marked READY for autonomous execution."""
        plan_path = self.project_path / "docs/notes/PROJECT_PLAN.md"

        if not plan_path.exists():
            return []

        with open(plan_path) as f:
            content = f.read()

        # Parse READY tasks
        tasks = []
        in_ready_section = False

        for line in content.split('\n'):
            if "Ready for Autonomous Execution" in line:
                in_ready_section = True
                continue
            elif line.startswith("###"):
                in_ready_section = False

            if in_ready_section and line.startswith("→ **["):
                # Extract task ID and description
                task_id = line.split('[')[1].split(']')[0]
                description = line.split(']')[1].strip()

                # Parse task details from following lines
                task = {
                    "id": task_id,
                    "description": description,
                    "alignment_score": 0,
                    "estimated_lines": 0
                }

                tasks.append(task)

        return tasks

    def create_feature_branch(self) -> bool:
        """Create feature branch for autonomous work."""
        branch_name = f"autonomous-{datetime.now().strftime('%Y%m%d-%H%M%S')}"

        try:
            subprocess.run(
                ["git", "checkout", "-b", branch_name],
                cwd=self.project_path,
                check=True,
                capture_output=True
            )
            self.session_log.append(f"Created branch: {branch_name}")
            return True
        except:
            return False

    def validate_task_safety(self, task: Dict) -> Dict:
        """Validate task is safe for autonomous execution."""

        # Check alignment score
        if task.get("alignment_score", 0) < 80:
            return {
                "safe": False,
                "reason": f"Alignment score too low: {task['alignment_score']}"
            }

        # Check estimated lines
        if task.get("estimated_lines", 999) > 30:
            return {
                "safe": False,
                "reason": f"Task too large: {task['estimated_lines']} lines"
            }

        # Additional safety checks via Quality MCP
        # (Would call MCP here in real implementation)

        return {"safe": True}

    def execute_task(self, task: Dict) -> Dict:
        """Execute a single task safely."""

        # Create checkpoint
        checkpoint = self.create_git_checkpoint()

        try:
            # Execute via Claude Code CLI
            result = self.execute_via_claude(task)

            # Run quality gate
            quality_result = self.run_quality_gate()

            if quality_result["status"] == "PASS":
                # Commit
                self.git_commit(f"feat: {task['description']}")

                return {
                    "success": True,
                    "task_id": task["id"],
                    "committed": True
                }
            else:
                # Rollback
                self.rollback_to_checkpoint(checkpoint)

                return {
                    "success": False,
                    "task_id": task["id"],
                    "reason": "Quality gate failed",
                    "rolled_back": True
                }

        except Exception as e:
            # Rollback on any error
            self.rollback_to_checkpoint(checkpoint)

            return {
                "success": False,
                "task_id": task["id"],
                "reason": str(e),
                "rolled_back": True
            }

    def execute_via_claude(self, task: Dict) -> Dict:
        """Execute task via Claude Code CLI."""

        # Build prompt
        prompt = f"""
Execute this task following best practices:

Task: {task['description']}

Requirements:
- Follow TDD (write test first if needed)
- Keep implementation ≤30 lines
- Add docstrings
- Add type hints
- Follow project standards in CLAUDE.md

Reference files:
- @docs/notes/PROJECT_PLAN.md (objective and context)
- @docs/context/tech-reference.md (patterns)
- @CLAUDE.md (standards)

Work step by step. Run tests after implementation.
"""

        # Execute via Claude Code CLI
        # (Simplified - real implementation would use proper CLI)
        result = subprocess.run(
            ["claude", "code", "--prompt", prompt],
            cwd=self.project_path,
            capture_output=True,
            text=True,
            timeout=1800  # 30 minute timeout
        )

        return {
            "success": result.returncode == 0,
            "output": result.stdout
        }

    def run_quality_gate(self) -> Dict:
        """Run quality gate checks."""
        quality_script = self.project_path / ".ai-validation/check_quality.sh"

        if not quality_script.exists():
            return {"status": "FAIL", "reason": "No quality script"}

        result = subprocess.run(
            ["bash", str(quality_script)],
            cwd=self.project_path,
            capture_output=True,
            text=True
        )

        return {
            "status": "PASS" if result.returncode == 0 else "FAIL",
            "output": result.stdout
        }

    def create_git_checkpoint(self) -> str:
        """Create git checkpoint for rollback."""
        result = subprocess.run(
            ["git", "rev-parse", "HEAD"],
            cwd=self.project_path,
            capture_output=True,
            text=True,
            check=True
        )
        return result.stdout.strip()

    def rollback_to_checkpoint(self, checkpoint: str):
        """Rollback to git checkpoint."""
        subprocess.run(
            ["git", "reset", "--hard", checkpoint],
            cwd=self.project_path,
            check=True
        )
        subprocess.run(
            ["git", "clean", "-fd"],
            cwd=self.project_path,
            check=True
        )

    def git_commit(self, message: str):
        """Create git commit."""
        subprocess.run(
            ["git", "add", "."],
            cwd=self.project_path,
            check=True
        )
        subprocess.run(
            ["git", "commit", "-m", message],
            cwd=self.project_path,
            check=True
        )

    def create_pr(self, completed_tasks: List[Dict]):
        """Create pull request."""
        # Use gh CLI
        pr_body = f"""
## Autonomous Session Results

**Completed**: {len(completed_tasks)} tasks

### Tasks Completed:
"""
        for task in completed_tasks:
            pr_body += f"- ✅ {task['description']}\n"

        pr_body += """
### Quality Checks:
- ✅ All tests passing
- ✅ Quality gate passed
- ✅ No linting errors

**Review carefully before merging.**
"""

        subprocess.run(
            ["gh", "pr", "create",
             "--title", f"Autonomous session: {len(completed_tasks)} tasks",
             "--body", pr_body],
            cwd=self.project_path
        )

    async def run_session(self):
        """Run autonomous session."""

        print("🤖 Starting autonomous session...")

        # Load tasks
        tasks = self.load_ready_tasks()
        print(f"📋 Found {len(tasks)} ready tasks")

        if not tasks:
            print("No tasks ready for autonomous execution")
            return

        # Create feature branch
        if not self.create_feature_branch():
            print("❌ Failed to create feature branch")
            return

        # Execute tasks
        completed = []
        failed = []

        max_tasks = self.config.get("max_tasks_per_session", 5)

        for i, task in enumerate(tasks[:max_tasks]):
            print(f"\n📝 Task {i+1}/{min(len(tasks), max_tasks)}: {task['description']}")

            # Validate safety
            safety = self.validate_task_safety(task)
            if not safety["safe"]:
                print(f"⚠️  Skipping: {safety['reason']}")
                continue

            # Execute
            result = self.execute_task(task)

            if result["success"]:
                print("✅ Completed")
                completed.append(task)
            else:
                print(f"❌ Failed: {result['reason']}")
                failed.append(result)

                # Stop if 2 consecutive failures
                if len(failed) >= 2:
                    print("⚠️  Too many failures, stopping session")
                    break

        # Create PR if any completed
        if completed:
            print(f"\n📤 Creating PR for {len(completed)} completed tasks...")
            self.create_pr(completed)
            print("✅ PR created! Review in morning.")

        # Summary
        print(f"\n📊 Session Summary:")
        print(f"   Completed: {len(completed)}")
        print(f"   Failed: {len(failed)}")


# Main execution
if __name__ == "__main__":
    import sys

    if len(sys.argv) < 2:
        print("Usage: python autonomous_daemon.py <project_path>")
        sys.exit(1)

    project_path = sys.argv[1]

    config = {
        "max_tasks_per_session": 5,
        "timeout_per_task": 1800
    }

    daemon = AutonomousDaemon(project_path, config)
    asyncio.run(daemon.run_session())
```

**Deliverable**: Working autonomous daemon prototype

#### Task 2.2: Integration Testing
**Time**: 4 hours

**Test Cases**:
1. ✅ Execute 3 ready tasks successfully
2. ✅ Rollback on quality gate failure
3. ✅ Stop after 2 consecutive failures
4. ✅ Create PR with completed tasks
5. ✅ Handle task timeout correctly
6. ✅ Skip unsafe tasks

**Deliverable**: Test results with success rate

#### Task 2.3: Refinement
**Time**: 4 hours

Based on test results:
- Adjust constraints
- Improve error handling
- Enhance logging
- Optimize performance

**Deliverable**: Refined daemon ready for production testing

---

## Phase 3: Production Integration (Weeks 3-4)

### Goal: Full MCP integration and production deployment

#### Task 3.1: MCP Integration
**Time**: 8 hours

Integrate daemon with existing MCPs:
- Quality MCP validates safety
- Project MCP marks tasks complete
- Memory MCP logs autonomous sessions

#### Task 3.2: Scheduling
**Time**: 4 hours

Add cron/scheduling:
```bash
# Run every night at 2am
0 2 * * * /path/to/autonomous_daemon.py /path/to/project
```

#### Task 3.3: Monitoring & Alerts
**Time**: 4 hours

- Log all executions
- Alert on failures
- Track success rate metrics

#### Task 3.4: Documentation
**Time**: 8 hours

Complete documentation:
- Usage guide
- Safety guidelines
- Troubleshooting
- Examples

#### Task 3.5: Production Testing
**Time**: 16 hours (2 weeks of overnight runs)

Test on real projects:
- Measure success rate
- Track productivity gain
- Identify edge cases
- Refine constraints

---

## Success Metrics

### Phase 1 Success
- ✅ PROJECT_PLAN.md format supports autonomous mode
- ✅ Constraints defined and documented
- ✅ Safety checks implemented
- ✅ Manual workflow tested (100% success)

### Phase 2 Success
- ✅ Daemon executes tasks autonomously
- ✅ Quality gates prevent bad code
- ✅ Auto-rollback works
- ✅ Success rate ≥80%

### Phase 3 Success
- ✅ Full MCP integration
- ✅ Production-ready deployment
- ✅ Success rate ≥85%
- ✅ 3-5x productivity gain measured

---

## Risk Mitigation

### Risk 1: Low Success Rate
**Mitigation**: Start with very simple tasks, increase complexity gradually

### Risk 2: Quality Issues
**Mitigation**: Quality gates catch issues, auto-rollback prevents damage

### Risk 3: Cost Overruns
**Mitigation**: Session limits (max 5 tasks, max 4 hours)

### Risk 4: Security Issues
**Mitigation**: Forbidden operations list, safety validation

---

## Go/No-Go Decision Points

### After Phase 1
**Criteria**: Manual workflow works 100%
**Decision**: Proceed to Phase 2 or refine constraints

### After Phase 2
**Criteria**: Success rate ≥80%, no quality issues
**Decision**: Proceed to Phase 3 or abandon

### After Phase 3
**Criteria**: Success rate ≥85%, positive productivity gain
**Decision**: Release or keep internal

---

## Timeline

```
Week 1: Foundation
├─ Mon-Tue: PROJECT_PLAN.md format + constraints
├─ Wed-Thu: Safety checks implementation
└─ Fri: Manual testing

Week 2: Prototype
├─ Mon-Tue: Daemon implementation
├─ Wed: Integration testing
└─ Thu-Fri: Refinement

Week 3: Production Prep
├─ Mon-Tue: MCP integration
├─ Wed: Scheduling setup
└─ Thu-Fri: Monitoring + docs

Week 4: Production Testing
├─ Entire week: Overnight runs on real projects
└─ End of week: Go/no-go decision
```

---

## Next Steps

1. **Review roadmap** - Approve approach and timeline
2. **Start Phase 1** - Begin with PROJECT_PLAN.md enhancements
3. **Weekly check-ins** - Review progress and adjust
4. **Go/no-go decisions** - At end of each phase

**Expected outcome**: Production-ready autonomous mode in 4 weeks, delivering 3-5x productivity gain.

---

*Based on analysis of 3 community tools with proven production usage*
*Safety-first approach with our existing quality infrastructure*
*Gradual rollout with clear success criteria at each phase*
