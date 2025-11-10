"""
Tests for Memory MCP server.
"""
import shutil
import tempfile
from pathlib import Path

import pytest

from mcp_servers.memory_mcp import MemoryServer


@pytest.fixture
def temp_memory_dir():
    """Create temporary memory directory for testing."""
    temp_dir = Path(tempfile.mkdtemp())
    yield temp_dir
    # Cleanup
    shutil.rmtree(temp_dir, ignore_errors=True)


@pytest.fixture
def memory_server(temp_memory_dir, monkeypatch):
    """Create MemoryServer instance with temporary storage."""
    import mcp_servers.memory_mcp as memory_module
    monkeypatch.setattr(memory_module, 'MEMORY_DIR', temp_memory_dir)
    server = MemoryServer()
    return server


@pytest.fixture
def sample_project_path():
    """Sample project path for testing."""
    return "/home/user/projects/test-project"


@pytest.fixture
def sample_objective_data():
    """Sample objective data for testing."""
    return {
        "problem": "Test problem statement",
        "target_users": "Test users",
        "solution": "Test solution",
        "success_metrics": ["Metric 1", "Metric 2"],
        "constraints": ["Constraint 1"],
        "clarity_score": 85
    }


class TestMemoryServer:
    """Tests for Memory MCP server."""

    def test_get_project_id(self, memory_server):
        """Test project ID generation."""
        project_path = "/home/user/projects/My Test Project"
        project_id = memory_server.get_project_id(project_path)
        assert project_id == "my_test_project"

    def test_get_project_file(self, memory_server, sample_project_path, temp_memory_dir):
        """Test project file path generation."""
        project_file = memory_server.get_project_file(sample_project_path)
        expected_file = temp_memory_dir / "test-project.json"
        assert project_file == expected_file

    def test_load_project_data_new_project(self, memory_server, sample_project_path):
        """Test loading data for new project creates default structure."""
        data = memory_server.load_project_data(sample_project_path)

        assert data["project_id"] == "test-project"
        assert data["project_path"] == sample_project_path
        assert "created_at" in data
        assert data["sessions"] == []
        assert data["decisions"] == []
        assert data["objective"] is None
        assert data["tech_stack"] == []
        assert data["current_status"] == "active"

    def test_save_and_load_project_data(self, memory_server, sample_project_path):
        """Test saving and loading project data."""
        # Create test data
        test_data = {
            "project_id": "test-project",
            "project_path": sample_project_path,
            "sessions": [{"summary": "Test session"}],
            "decisions": [],
            "objective": None,
            "tech_stack": ["Python"],
            "current_status": "active"
        }

        # Save data
        memory_server.save_project_data(sample_project_path, test_data)

        # Load data
        loaded_data = memory_server.load_project_data(sample_project_path)

        assert loaded_data["project_id"] == test_data["project_id"]
        assert loaded_data["sessions"] == test_data["sessions"]
        assert "updated_at" in loaded_data

    def test_save_session_summary(self, memory_server, sample_project_path):
        """Test saving session summary."""
        result = memory_server.save_session_summary(
            project_path=sample_project_path,
            summary="Implemented user authentication",
            decisions=["Use JWT tokens", "Store in httpOnly cookies"],
            next_steps=["Add password reset", "Add 2FA"],
            blockers=["Need email service configuration"]
        )

        assert result["success"] is True
        assert result["project_id"] == "test-project"

        # Verify data was saved
        data = memory_server.load_project_data(sample_project_path)
        assert len(data["sessions"]) == 1

        session = data["sessions"][0]
        assert session["summary"] == "Implemented user authentication"
        assert len(session["decisions"]) == 2
        assert len(session["next_steps"]) == 2
        assert len(session["blockers"]) == 1

    def test_save_session_summary_keeps_last_10(self, memory_server, sample_project_path):
        """Test that only last 10 sessions are kept."""
        # Save 15 sessions
        for i in range(15):
            memory_server.save_session_summary(
                project_path=sample_project_path,
                summary=f"Session {i}"
            )

        # Check only last 10 are kept
        data = memory_server.load_project_data(sample_project_path)
        assert len(data["sessions"]) == 10
        assert data["sessions"][0]["summary"] == "Session 5"
        assert data["sessions"][-1]["summary"] == "Session 14"

    def test_load_project_context(self, memory_server, sample_project_path):
        """Test loading project context."""
        # Save some sessions and decisions
        memory_server.save_session_summary(
            project_path=sample_project_path,
            summary="Session 1"
        )
        memory_server.save_decision(
            project_path=sample_project_path,
            decision="Use PostgreSQL",
            rationale="Better for relational data"
        )

        # Load context
        context = memory_server.load_project_context(sample_project_path)

        assert context["project_id"] == "test-project"
        assert context["project_path"] == sample_project_path
        assert len(context["recent_sessions"]) == 1
        assert len(context["all_decisions"]) == 1
        assert context["current_status"] == "active"

    def test_load_project_context_returns_last_3_sessions(self, memory_server, sample_project_path):
        """Test that load_project_context returns only last 3 sessions."""
        # Save 5 sessions
        for i in range(5):
            memory_server.save_session_summary(
                project_path=sample_project_path,
                summary=f"Session {i}"
            )

        context = memory_server.load_project_context(sample_project_path)

        assert len(context["recent_sessions"]) == 3
        assert context["recent_sessions"][0]["summary"] == "Session 2"
        assert context["recent_sessions"][-1]["summary"] == "Session 4"

    def test_save_decision(self, memory_server, sample_project_path):
        """Test saving architectural decision."""
        result = memory_server.save_decision(
            project_path=sample_project_path,
            decision="Use microservices architecture",
            rationale="Better scalability and team autonomy"
        )

        assert result["success"] is True
        assert result["decision_count"] == 1

        # Verify decision was saved
        data = memory_server.load_project_data(sample_project_path)
        assert len(data["decisions"]) == 1

        decision = data["decisions"][0]
        assert decision["decision"] == "Use microservices architecture"
        assert decision["rationale"] == "Better scalability and team autonomy"
        assert "timestamp" in decision

    def test_list_projects_empty(self, memory_server):
        """Test listing projects when none exist."""
        result = memory_server.list_projects()

        assert result["total_projects"] == 0
        assert result["projects"] == []

    def test_list_projects_with_data(self, memory_server):
        """Test listing multiple projects."""
        # Create two projects
        memory_server.save_session_summary("/home/user/project1", "Project 1 session")
        memory_server.save_session_summary("/home/user/project2", "Project 2 session")

        result = memory_server.list_projects()

        assert result["total_projects"] == 2
        assert len(result["projects"]) == 2

        # Check project structure
        project = result["projects"][0]
        assert "project_id" in project
        assert "project_path" in project
        assert "last_activity" in project
        assert "session_count" in project
        assert "has_objective" in project

    def test_search_memory_in_sessions(self, memory_server):
        """Test searching in session summaries."""
        memory_server.save_session_summary(
            "/home/user/project1",
            "Implemented authentication system"
        )
        memory_server.save_session_summary(
            "/home/user/project2",
            "Fixed database connection bug"
        )

        # Search for "authentication"
        result = memory_server.search_memory("authentication")

        assert result["query"] == "authentication"
        assert result["total_results"] == 1
        assert result["results"][0]["project_id"] == "project1"
        assert len(result["results"][0]["matches"]) == 1
        assert result["results"][0]["matches"][0]["type"] == "session"

    def test_search_memory_in_decisions(self, memory_server):
        """Test searching in decisions."""
        memory_server.save_decision(
            "/home/user/project1",
            "Use React for frontend",
            "Better component reusability"
        )

        result = memory_server.search_memory("React")

        assert result["total_results"] == 1
        assert result["results"][0]["matches"][0]["type"] == "decision"

    def test_search_memory_in_objective(self, memory_server, sample_objective_data):
        """Test searching in project objective."""
        memory_server.save_project_objective(
            "/home/user/project1",
            sample_objective_data
        )

        result = memory_server.search_memory("Test problem")

        assert result["total_results"] == 1
        assert any(m["type"] == "objective" for m in result["results"][0]["matches"])

    def test_search_memory_no_results(self, memory_server):
        """Test searching with no matches."""
        memory_server.save_session_summary("/home/user/project1", "Some content")

        result = memory_server.search_memory("nonexistent")

        assert result["total_results"] == 0
        assert result["results"] == []

    def test_save_project_objective(self, memory_server, sample_project_path, sample_objective_data):
        """Test saving project objective."""
        result = memory_server.save_project_objective(
            project_path=sample_project_path,
            objective_data=sample_objective_data
        )

        assert result["success"] is True
        assert result["clarity_score"] == 85

        # Verify objective was saved
        data = memory_server.load_project_data(sample_project_path)
        assert data["objective"] == sample_objective_data

    def test_load_project_objective_exists(self, memory_server, sample_project_path, sample_objective_data):
        """Test loading existing project objective."""
        # Save objective first
        memory_server.save_project_objective(sample_project_path, sample_objective_data)

        # Load it
        result = memory_server.load_project_objective(sample_project_path)

        assert result["found"] is True
        assert result["objective"] == sample_objective_data

    def test_load_project_objective_not_found(self, memory_server, sample_project_path):
        """Test loading objective when none exists."""
        result = memory_server.load_project_objective(sample_project_path)

        assert result["found"] is False
        assert "message" in result

    def test_get_storage_dir(self, memory_server, temp_memory_dir):
        """Test getting storage directory."""
        storage_dir = memory_server.get_storage_dir()
        assert storage_dir == temp_memory_dir

    def test_save_session_with_minimal_data(self, memory_server, sample_project_path):
        """Test saving session with only required fields."""
        result = memory_server.save_session_summary(
            project_path=sample_project_path,
            summary="Minimal session"
        )

        assert result["success"] is True

        data = memory_server.load_project_data(sample_project_path)
        session = data["sessions"][0]
        assert session["decisions"] == []
        assert session["next_steps"] == []
        assert session["blockers"] == []

    def test_multiple_projects_independence(self, memory_server):
        """Test that different projects maintain independent data."""
        project1 = "/home/user/project1"
        project2 = "/home/user/project2"

        memory_server.save_session_summary(project1, "Project 1 session")
        memory_server.save_session_summary(project2, "Project 2 session")

        context1 = memory_server.load_project_context(project1)
        context2 = memory_server.load_project_context(project2)

        assert context1["project_id"] == "project1"
        assert context2["project_id"] == "project2"
        assert context1["recent_sessions"][0]["summary"] == "Project 1 session"
        assert context2["recent_sessions"][0]["summary"] == "Project 2 session"
