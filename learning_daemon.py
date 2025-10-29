#!/usr/bin/env python3
"""
Learning Daemon - Scheduled best practices research
Runs periodic searches to continuously improve toolkit standards
"""
import sys
from pathlib import Path
from datetime import datetime

# Add mcp-servers to path
sys.path.insert(0, str(Path(__file__).parent / "mcp-servers"))

try:
    from learning_mcp import search_best_practices, store_learning
except ImportError:
    print("Error: learning_mcp.py not found")
    sys.exit(1)

def run_learning_cycle():
    """Run one cycle of learning (search → store)."""
    topics = ["python", "angular", "redis", "nginx", "claude-ai", "testing"]

    print(f"🎓 Learning Daemon - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"Topics: {', '.join(topics)}")
    print("")

    for topic in topics:
        print(f"Searching: {topic}...")
        result = search_best_practices(topic, max_results=3)

        if result["success"]:
            print(f"  ✅ Search complete: {len(result.get('queries', []))} queries")
        else:
            print(f"  ❌ Search failed: {result.get('error', 'Unknown error')}")

    print("")
    print("✅ Learning cycle complete")

if __name__ == "__main__":
    run_learning_cycle()
