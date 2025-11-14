#!/usr/bin/env python3
"""
Code Review Daemon - Automated code quality improvement
Reviews project code and adds findings to PROJECT_PLAN.md as prioritized tasks
"""
import sys
from pathlib import Path
from datetime import datetime

# Add mcp-servers to path
sys.path.insert(0, str(Path(__file__).parent / "mcp-servers"))

try:
    from learning_mcp import review_code
except ImportError:
    print("Error: learning_mcp.py not found")
    sys.exit(1)

def run_code_review(project_path: str):
    """Run code review and report findings."""

    print(f"🔍 Code Review Daemon - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"Project: {project_path}")
    print("")

    # Run review
    result = review_code(project_path, file_patterns=['*.py', '*.js', '*.ts'])

    if result["success"]:
        findings = result["findings"]
        total = sum(len(findings[p]) for p in findings)

        print("✅ Review complete:")
        print(f"  Critical: {len(findings['critical'])}")
        print(f"  High: {len(findings['high'])}")
        print(f"  Medium: {len(findings['medium'])}")
        print(f"  Low: {len(findings['low'])}")
        print(f"  Total: {total} findings")
    else:
        print(f"❌ Review failed: {result.get('error', 'Unknown error')}")

    print("")
    print("Next: Findings will be added to PROJECT_PLAN.md (feature pending)")

if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Code Review Daemon")
    parser.add_argument("project_path", help="Path to project to review")
    args = parser.parse_args()

    run_code_review(args.project_path)
