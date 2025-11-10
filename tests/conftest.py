"""
Pytest configuration and fixtures for best-practice toolkit tests.
"""
import importlib.util
import os
import sys
import tempfile
from pathlib import Path
from typing import Generator

import pytest

# Add project root to Python path and create mcp_servers module alias
# This allows importing from mcp-servers despite the hyphenated name
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

# Create module alias for mcp-servers -> mcp_servers
mcp_servers_init = project_root / "mcp-servers" / "__init__.py"
if mcp_servers_init.exists():
    spec = importlib.util.spec_from_file_location("mcp_servers", mcp_servers_init)
    if spec and spec.loader:
        mcp_servers_module = importlib.util.module_from_spec(spec)
        sys.modules["mcp_servers"] = mcp_servers_module
        spec.loader.exec_module(mcp_servers_module)


@pytest.fixture
def tmp_project_dir() -> Generator[Path, None, None]:
    """Create a temporary project directory for testing.

    Yields:
        Path to temporary project directory
    """
    with tempfile.TemporaryDirectory() as tmpdir:
        project_path = Path(tmpdir) / "test_project"
        project_path.mkdir()
        yield project_path


@pytest.fixture
def sample_project_structure(tmp_project_dir: Path) -> Path:
    """Create a sample project structure for testing.

    Args:
        tmp_project_dir: Temporary project directory

    Returns:
        Path to project with sample structure
    """
    # Create standard directories
    (tmp_project_dir / "src").mkdir()
    (tmp_project_dir / "tests").mkdir()
    (tmp_project_dir / "docs").mkdir()

    # Create sample files
    (tmp_project_dir / "README.md").write_text("# Test Project\n")
    (tmp_project_dir / "src" / "main.py").write_text("def main():\n    pass\n")

    return tmp_project_dir


@pytest.fixture
def sample_objective_data() -> dict:
    """Sample objective data for testing.

    Returns:
        Dictionary with sample objective data
    """
    return {
        "problem": "Users waste time on manual data entry",
        "target_users": "Data analysts at mid-size companies",
        "solution": "Automated data import tool with validation",
        "success_metrics": [
            "50% reduction in data entry time",
            "99% accuracy in imports",
            "Process 10,000 records per minute"
        ],
        "constraints": [
            "Must support Excel and CSV formats",
            "Must work offline",
            "Must be under $1000 per year cost"
        ],
        "clarity_score": 85
    }


@pytest.fixture
def mock_storage_dir(tmp_path: Path) -> Path:
    """Create a temporary storage directory for MCP data.

    Args:
        tmp_path: Pytest tmp_path fixture

    Returns:
        Path to temporary storage directory
    """
    storage_dir = tmp_path / ".claude_memory"
    storage_dir.mkdir()
    return storage_dir
