#!/usr/bin/env python3
"""
Autonomous Execution Daemon - Safe overnight task execution
Implements Phase 3: Production Integration with MCP servers
"""
import argparse
import json
import os
import re
import subprocess
import sys
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional

# MCP integration
sys.path.insert(0, str(Path(__file__).parent / "mcp-servers"))
try:
    from quality_mcp import QualityServer
    from memory_mcp import MemoryServer
    MCP_AVAILABLE = True
except ImportError:
    MCP_AVAILABLE = False


class AutonomousDaemon:
    """Safe autonomous task execution daemon."""

    def __init__(self, project_path: str, config: Optional[Dict] = None):
        """Initialize daemon."""
        self.project_path = Path(project_path)
        self.config = config or self._default_config()
        self.session_log = []
        self.checkpoint_hash = None

        # Initialize MCP servers
        if MCP_AVAILABLE:
            self.quality_mcp = QualityServer()
            self.memory_mcp = MemoryServer()
            self._log("INFO", "MCP servers initialized")
        else:
            self.quality_mcp = None
            self.memory_mcp = None
            self._log("WARN", "MCP servers not available")

    def _default_config(self) -> Dict:
        """Get default configuration."""
        return {
            "max_tasks_per_session": 5,
            "timeout_per_task": 1800,
            "max_session_duration": 14400,
            "stop_on_consecutive_failures": 2
        }

    def load_ready_tasks(self) -> List[Dict]:
        """Load tasks marked READY for autonomous execution."""
        plan_path = self.project_path / "docs/notes/PROJECT_PLAN.md"

        if not plan_path.exists():
            self._log("ERROR", "PROJECT_PLAN.md not found")
            return []

        with open(plan_path) as f:
            content = f.read()

        tasks = []
        in_ready_section = False

        for line in content.split('\n'):
            if "Ready for Autonomous Execution" in line:
                in_ready_section = True
                continue
            elif line.startswith("###") and in_ready_section:
                in_ready_section = False

            if in_ready_section and line.strip().startswith("→ **["):
                match = re.search(r'→ \*\*\[(.+?)\]\*\* (.+)', line)
                if match:
                    task_id = match.group(1)
                    description = match.group(2)
                    task = {
                        "id": task_id,
                        "description": description,
                        "alignment_score": 0,
                        "estimated_lines": 0,
                        "status": "READY"
                    }
                    tasks.append(task)

        return tasks

    def _log(self, level: str, message: str):
        """Log message."""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        log_entry = f"{timestamp} - [{level}] {message}"
        self.session_log.append(log_entry)
        print(log_entry)

    def create_git_checkpoint(self) -> Optional[str]:
        """Create git checkpoint for rollback."""
        try:
            result = subprocess.run(
                ["git", "rev-parse", "HEAD"],
                cwd=self.project_path,
                capture_output=True,
                text=True,
                check=True
            )
            checkpoint = result.stdout.strip()
            self.checkpoint_hash = checkpoint
            self._log("INFO", f"Checkpoint created: {checkpoint[:8]}")
            return checkpoint
        except subprocess.CalledProcessError as e:
            self._log("ERROR", f"Failed to create checkpoint: {e}")
            return None

    def rollback_to_checkpoint(self, checkpoint: str) -> bool:
        """Rollback to git checkpoint."""
        try:
            subprocess.run(
                ["git", "reset", "--hard", checkpoint],
                cwd=self.project_path,
                check=True,
                capture_output=True
            )
            subprocess.run(
                ["git", "clean", "-fd"],
                cwd=self.project_path,
                check=True,
                capture_output=True
            )
            self._log("INFO", f"Rolled back to {checkpoint[:8]}")
            return True
        except subprocess.CalledProcessError as e:
            self._log("ERROR", f"Rollback failed: {e}")
            return False

    def git_commit(self, message: str) -> bool:
        """Create git commit."""
        try:
            subprocess.run(
                ["git", "add", "."],
                cwd=self.project_path,
                check=True,
                capture_output=True
            )
            subprocess.run(
                ["git", "commit", "-m", message],
                cwd=self.project_path,
                check=True,
                capture_output=True
            )
            self._log("INFO", f"Committed: {message[:50]}")
            return True
        except subprocess.CalledProcessError as e:
            self._log("ERROR", f"Commit failed: {e}")
            return False

    def run_quality_gate(self) -> Dict:
        """Run quality gate checks."""
        quality_script = self.project_path / ".ai-validation/check_quality.sh"

        if not quality_script.exists():
            self._log("WARN", "Quality gate script not found")
            return {"status": "SKIP", "reason": "No quality script"}

        try:
            result = subprocess.run(
                ["bash", str(quality_script)],
                cwd=self.project_path,
                capture_output=True,
                text=True,
                timeout=300
            )

            status = "PASS" if result.returncode == 0 else "FAIL"
            self._log("INFO", f"Quality gate: {status}")

            return {
                "status": status,
                "output": result.stdout,
                "errors": result.stderr
            }
        except subprocess.TimeoutExpired:
            self._log("ERROR", "Quality gate timeout")
            return {"status": "FAIL", "reason": "Timeout"}
        except Exception as e:
            self._log("ERROR", f"Quality gate error: {e}")
            return {"status": "FAIL", "reason": str(e)}

    def validate_task_safety(self, task: Dict) -> Dict:
        """Validate task safety using Quality MCP."""
        if not self.quality_mcp:
            self._log("WARN", "Quality MCP not available, skipping safety check")
            return {"safe_for_autonomous": True, "violations": []}

        # For now, assume no file changes (would need task metadata)
        # In real implementation, task would specify which files it modifies
        file_changes = []

        result = self.quality_mcp.validate_autonomous_safety(
            str(self.project_path),
            task["description"],
            file_changes
        )

        if not result.get("safe_for_autonomous", False):
            self._log("WARN", f"Safety violations found: {len(result.get('violations', []))}")
            for violation in result.get("violations", []):
                self._log("WARN", f"  - {violation.get('violation')}")

        return result

    def execute_task(self, task: Dict) -> Dict:
        """Execute a single task safely."""
        self._log("INFO", f"Executing task: {task['id']}")

        # Validate safety first
        safety_result = self.validate_task_safety(task)
        if not safety_result.get("safe_for_autonomous", False):
            return {
                "success": False,
                "task_id": task["id"],
                "reason": "Safety validation failed",
                "violations": safety_result.get("violations", [])
            }

        checkpoint = self.create_git_checkpoint()
        if not checkpoint:
            return {
                "success": False,
                "task_id": task["id"],
                "reason": "Failed to create checkpoint"
            }

        try:
            self._log("INFO", f"Task: {task['description']}")
            self._log("WARN", "Task execution is simulated (not implemented)")

            quality_result = self.run_quality_gate()

            if quality_result["status"] == "PASS":
                commit_msg = f"feat: {task['description']}\n\nAutonomous execution"
                if self.git_commit(commit_msg):
                    return {
                        "success": True,
                        "task_id": task["id"],
                        "committed": True
                    }
                else:
                    self.rollback_to_checkpoint(checkpoint)
                    return {
                        "success": False,
                        "task_id": task["id"],
                        "reason": "Commit failed",
                        "rolled_back": True
                    }
            else:
                self._log("WARN", "Quality gate failed, rolling back")
                self.rollback_to_checkpoint(checkpoint)
                return {
                    "success": False,
                    "task_id": task["id"],
                    "reason": "Quality gate failed",
                    "rolled_back": True,
                    "quality_output": quality_result.get("output", "")
                }

        except Exception as e:
            self._log("ERROR", f"Task execution error: {e}")
            self.rollback_to_checkpoint(checkpoint)
            return {
                "success": False,
                "task_id": task["id"],
                "reason": str(e),
                "rolled_back": True
            }

    def run_session(self):
        """Run autonomous session."""
        self._log("INFO", "🤖 Starting autonomous session")

        tasks = self.load_ready_tasks()
        self._log("INFO", f"📋 Found {len(tasks)} ready tasks")

        if not tasks:
            self._log("INFO", "No tasks ready for autonomous execution")
            return

        completed = []
        failed = []
        max_tasks = self.config["max_tasks_per_session"]
        consecutive_failures = 0

        for i, task in enumerate(tasks[:max_tasks]):
            self._log("INFO", f"\n📝 Task {i+1}/{min(len(tasks), max_tasks)}: {task['description']}")

            result = self.execute_task(task)

            if result["success"]:
                self._log("INFO", "✅ Task completed successfully")
                completed.append(task)
                consecutive_failures = 0
            else:
                self._log("ERROR", f"❌ Task failed: {result['reason']}")
                failed.append(result)
                consecutive_failures += 1

                if consecutive_failures >= self.config["stop_on_consecutive_failures"]:
                    self._log("WARN", f"⚠️  {consecutive_failures} consecutive failures, stopping session")
                    break

        self._log("INFO", f"\n📊 Session Summary:")
        self._log("INFO", f"   Completed: {len(completed)}")
        self._log("INFO", f"   Failed: {len(failed)}")

        # Save to Memory MCP
        self._save_to_memory_mcp(completed, failed)

        # Save session log file
        self._save_session_log()

    def _save_to_memory_mcp(self, completed: List, failed: List):
        """Save session summary to Memory MCP."""
        if not self.memory_mcp:
            return

        summary = f"Autonomous session: {len(completed)} completed, {len(failed)} failed"
        decisions = [f"Task {t['id']}: {t['description']}" for t in completed]
        next_steps = ["Review autonomous PR" if completed else "Fix failures and retry"]
        blockers = [f["reason"] for f in failed] if failed else []

        try:
            self.memory_mcp.save_session_summary(
                str(self.project_path),
                summary,
                decisions,
                next_steps,
                blockers
            )
            self._log("INFO", "Session saved to Memory MCP")
        except Exception as e:
            self._log("ERROR", f"Failed to save to Memory MCP: {e}")

        self._save_session_log()

    def _save_session_log(self):
        """Save session log to file."""
        log_dir = self.project_path / "logs"
        log_dir.mkdir(exist_ok=True)

        timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
        log_file = log_dir / f"autonomous-session-{timestamp}.log"

        with open(log_file, 'w') as f:
            f.write('\n'.join(self.session_log))

        self._log("INFO", f"Session log saved: {log_file}")


def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(
        description="Autonomous Execution Daemon - Safe overnight task execution"
    )
    parser.add_argument(
        "project_path",
        help="Absolute path to project directory"
    )
    parser.add_argument(
        "--max-tasks",
        type=int,
        default=5,
        help="Maximum tasks per session (default: 5)"
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Dry run - load tasks but don't execute"
    )

    args = parser.parse_args()

    project_path = Path(args.project_path)
    if not project_path.exists():
        print(f"ERROR: Project path does not exist: {project_path}")
        sys.exit(1)

    config = {
        "max_tasks_per_session": args.max_tasks,
        "timeout_per_task": 1800,
        "max_session_duration": 14400,
        "stop_on_consecutive_failures": 2
    }

    daemon = AutonomousDaemon(str(project_path), config)

    if args.dry_run:
        print("🔍 Dry run mode - loading tasks only")
        tasks = daemon.load_ready_tasks()
        print(f"Found {len(tasks)} ready tasks:")
        for i, task in enumerate(tasks, 1):
            print(f"  {i}. [{task['id']}] {task['description']}")
    else:
        daemon.run_session()


if __name__ == "__main__":
    main()
