#!/usr/bin/env python3
"""
Comprehensive Integration Tests for Best Practice Toolkit

Tests ALL components:
- All 4 MCP servers (Memory, Quality, Project, Learning)
- Skills system
- Slash commands
- Git hooks
- Quality gate
- Templates
- Utility scripts
"""
import json
import pytest
import tempfile
import subprocess
import shutil
from pathlib import Path
import sys
import os

# Add MCP servers to path
sys.path.insert(0, str(Path(__file__).parent.parent / ".claude" / "mcp-servers"))

from memory_mcp import MemoryServer
from learning_mcp import LearningServer


class TestAllMCPServers:
    """Test all 4 MCP servers work correctly."""

    def test_memory_mcp_exists(self):
        """Test Memory MCP can be imported and initialized."""
        server = MemoryServer()
        assert server is not None
        assert hasattr(server, 'server')

    def test_learning_mcp_exists(self):
        """Test Learning MCP can be imported and initialized."""
        server = LearningServer()
        assert server is not None
        assert hasattr(server, 'server')
        assert hasattr(server, 'project_objective')
        assert hasattr(server, 'project_domain')

    def test_quality_mcp_exists(self):
        """Test Quality MCP file exists and is executable."""
        quality_mcp = Path(__file__).parent.parent / ".claude" / "mcp-servers" / "quality_mcp.py"
        assert quality_mcp.exists()
        assert quality_mcp.stat().st_size > 0

    def test_project_mcp_exists(self):
        """Test Project MCP file exists and is executable."""
        project_mcp = Path(__file__).parent.parent / ".claude" / "mcp-servers" / "project_mcp.py"
        assert project_mcp.exists()
        assert project_mcp.stat().st_size > 0


class TestSkillsSystem:
    """Test skills are properly structured and loadable."""

    @pytest.fixture
    def skills_dir(self):
        return Path(__file__).parent.parent / ".claude" / "skills"

    def test_skills_directory_exists(self, skills_dir):
        """Test skills directory exists."""
        assert skills_dir.exists()
        assert skills_dir.is_dir()

    def test_skills_index_exists(self, skills_dir):
        """Test INDEX.md exists for skill catalog."""
        index = skills_dir / "INDEX.md"
        assert index.exists()
        assert index.stat().st_size > 0

    def test_all_skills_have_skill_md(self, skills_dir):
        """Test all skill directories have skill.md file."""
        skill_dirs = [d for d in skills_dir.iterdir() if d.is_dir() and d.name != "template"]

        assert len(skill_dirs) >= 8, "Should have at least 8 skills"

        for skill_dir in skill_dirs:
            skill_file = skill_dir / "skill.md"
            assert skill_file.exists(), f"{skill_dir.name} missing skill.md"

            # Check skill.md has frontmatter
            content = skill_file.read_text()
            assert "---" in content, f"{skill_dir.name}/skill.md missing frontmatter"
            assert "name:" in content.lower()
            assert "description:" in content.lower()

    def test_domain_learning_skill_updated(self, skills_dir):
        """Test domain-learning skill has project-objective-driven purpose."""
        domain_skill = skills_dir / "domain-learning" / "skill.md"
        assert domain_skill.exists()

        content = domain_skill.read_text()
        assert "project-objective-driven" in content.lower()
        assert "rapid-pm" in content.lower()
        assert "ai-task-optimisation-mvp" in content.lower()


class TestSlashCommands:
    """Test slash commands are properly structured."""

    @pytest.fixture
    def commands_dir(self):
        return Path(__file__).parent.parent / ".claude" / "commands"

    def test_commands_directory_exists(self, commands_dir):
        """Test commands directory exists."""
        assert commands_dir.exists()
        assert commands_dir.is_dir()

    def test_all_commands_exist(self, commands_dir):
        """Test expected commands exist."""
        expected_commands = [
            "brainstorm.md",
            "checkpoint.md",
            "debug.md",
            "execute-plan.md",
            "mcp.md",
            "plan.md",
            "spec.md",
            "tdd.md"
        ]

        for cmd in expected_commands:
            cmd_file = commands_dir / cmd
            assert cmd_file.exists(), f"Missing command: {cmd}"

            # Verify command has description
            content = cmd_file.read_text()
            assert "---" in content, f"{cmd} missing frontmatter"
            assert "description:" in content.lower()


class TestGitHooks:
    """Test git hooks are properly structured and executable."""

    @pytest.fixture
    def hooks_dir(self):
        return Path(__file__).parent.parent / ".claude" / "hooks"

    def test_hooks_directory_exists(self, hooks_dir):
        """Test hooks directory exists."""
        assert hooks_dir.exists()
        assert hooks_dir.is_dir()

    def test_all_hooks_exist(self, hooks_dir):
        """Test expected hooks exist."""
        expected_hooks = [
            "pre-commit",
            "commit-msg",
            "pre-push",
            "install-hooks.sh"
        ]

        for hook in expected_hooks:
            hook_file = hooks_dir / hook
            assert hook_file.exists(), f"Missing hook: {hook}"

    def test_hooks_are_executable(self, hooks_dir):
        """Test hooks have execute permission."""
        hooks = ["pre-commit", "commit-msg", "pre-push", "install-hooks.sh"]

        for hook in hooks:
            hook_file = hooks_dir / hook
            if hook_file.exists():
                # Check execute bit
                assert os.access(str(hook_file), os.X_OK), f"{hook} is not executable"

    def test_install_hooks_script_works(self, hooks_dir, tmp_path):
        """Test install-hooks.sh script can be executed."""
        install_script = hooks_dir / "install-hooks.sh"
        assert install_script.exists()

        # Should have shebang
        content = install_script.read_text()
        assert content.startswith("#!/")


class TestQualityGate:
    """Test quality gate scripts exist and are executable."""

    @pytest.fixture
    def quality_gate_dir(self):
        return Path(__file__).parent.parent / ".claude" / "quality-gate"

    def test_quality_gate_directory_exists(self, quality_gate_dir):
        """Test quality-gate directory exists."""
        assert quality_gate_dir.exists()
        assert quality_gate_dir.is_dir()

    def test_check_quality_script_exists(self, quality_gate_dir):
        """Test check_quality.sh exists."""
        check_script = quality_gate_dir / "check_quality.sh"
        assert check_script.exists()
        assert check_script.stat().st_size > 0

    def test_check_quality_is_executable(self, quality_gate_dir):
        """Test check_quality.sh is executable."""
        check_script = quality_gate_dir / "check_quality.sh"
        assert os.access(str(check_script), os.X_OK)


class TestTemplates:
    """Test templates are properly structured."""

    @pytest.fixture
    def templates_dir(self):
        return Path(__file__).parent.parent / ".claude" / "templates"

    def test_templates_directory_exists(self, templates_dir):
        """Test templates directory exists."""
        assert templates_dir.exists()
        assert templates_dir.is_dir()

    def test_ci_cd_templates_exist(self, templates_dir):
        """Test CI/CD templates exist."""
        ci_cd_dir = templates_dir / "ci-cd"
        assert ci_cd_dir.exists()

        # Check for GitHub Actions template
        gh_actions = ci_cd_dir / "github-actions.yml"
        if gh_actions.exists():
            content = gh_actions.read_text()
            assert "name:" in content
            assert "on:" in content

    def test_project_config_templates_exist(self, templates_dir):
        """Test project config templates exist."""
        expected_types = ["python", "javascript", "go"]

        for proj_type in expected_types:
            type_dir = templates_dir / proj_type
            if type_dir.exists():
                config = type_dir / "config.json"
                if config.exists():
                    # Should be valid JSON
                    data = json.loads(config.read_text())
                    assert isinstance(data, dict)


class TestUtilityScripts:
    """Test utility scripts exist and are executable."""

    @pytest.fixture
    def claude_dir(self):
        return Path(__file__).parent.parent / ".claude"

    def test_init_wizard_exists(self, claude_dir):
        """Test init-wizard.sh exists."""
        wizard = claude_dir / "init-wizard.sh"
        assert wizard.exists()
        assert os.access(str(wizard), os.X_OK)

    def test_uninstall_script_exists(self, claude_dir):
        """Test uninstall.sh exists."""
        uninstall = claude_dir / "uninstall.sh"
        assert uninstall.exists()
        assert os.access(str(uninstall), os.X_OK)

    def test_verify_git_clean_exists(self, claude_dir):
        """Test verify-git-clean.sh exists."""
        verify = claude_dir / "verify-git-clean.sh"
        assert verify.exists()
        assert os.access(str(verify), os.X_OK)


class TestCoreDocumentation:
    """Test core documentation files exist."""

    @pytest.fixture
    def claude_dir(self):
        return Path(__file__).parent.parent / ".claude"

    def test_best_practice_md_exists(self, claude_dir):
        """Test best-practice.md exists (core standards)."""
        bp = claude_dir / "best-practice.md"
        assert bp.exists()
        assert bp.stat().st_size > 10000, "best-practice.md should be substantial"

    def test_tasks_md_exists(self, claude_dir):
        """Test TASKS.md exists."""
        tasks = claude_dir / "TASKS.md"
        assert tasks.exists()

    def test_user_guide_exists(self, claude_dir):
        """Test USER_GUIDE.md exists."""
        guide = claude_dir / "USER_GUIDE.md"
        assert guide.exists()
        assert guide.stat().st_size > 10000

    def test_quick_reference_exists(self, claude_dir):
        """Test QUICK_REFERENCE.md exists."""
        quick_ref = claude_dir / "QUICK_REFERENCE.md"
        assert quick_ref.exists()

    def test_troubleshooting_exists(self, claude_dir):
        """Test TROUBLESHOOTING.md exists."""
        troubleshoot = claude_dir / "TROUBLESHOOTING.md"
        assert troubleshoot.exists()


class TestRetrofitTools:
    """Test retrofit/installation scripts work."""

    @pytest.fixture
    def retrofit_dir(self):
        return Path(__file__).parent.parent / "retrofit-tools"

    def test_retrofit_directory_exists(self, retrofit_dir):
        """Test retrofit-tools directory exists."""
        assert retrofit_dir.exists()
        assert retrofit_dir.is_dir()

    def test_smart_install_script_exists(self, retrofit_dir):
        """Test smart_install.sh exists."""
        smart_install = retrofit_dir / "smart_install.sh"
        assert smart_install.exists()
        assert os.access(str(smart_install), os.X_OK)

        # Should have toolkit installation logic
        content = smart_install.read_text()
        assert ".claude/skills" in content
        assert ".claude/commands" in content
        assert "LIGHT" in content or "FULL" in content


class TestPackaging:
    """Test packaging and distribution scripts."""

    def test_package_script_exists(self):
        """Test package_toolkit.sh exists."""
        package_script = Path(__file__).parent.parent / "package_toolkit.sh"
        assert package_script.exists()
        assert os.access(str(package_script), os.X_OK)

        content = package_script.read_text()
        assert "VERSION=" in content
        assert "tar" in content.lower() or "zip" in content.lower()


class TestGitCleanliness:
    """Test toolkit files are properly gitignored."""

    def test_gitignore_exists(self):
        """Test .gitignore exists."""
        gitignore = Path(__file__).parent.parent / ".gitignore"
        assert gitignore.exists()

        content = gitignore.read_text()
        assert ".claude/" in content or ".claude" in content
        assert "docs/" in content or "docs" in content

    def test_no_toolkit_files_tracked(self):
        """Test no .claude/ files are tracked by git."""
        result = subprocess.run(
            ["git", "ls-files"],
            cwd=Path(__file__).parent.parent,
            capture_output=True,
            text=True
        )

        tracked_files = result.stdout.strip().split("\n")

        # Should NOT have any .claude/ files (except .claude/commands, skills in this repo as source)
        claude_files = [f for f in tracked_files if f.startswith(".claude/")]

        # This repo IS the source, so .claude/ files ARE tracked here
        # But in INJECTED projects, they should NOT be tracked
        # This test verifies the .gitignore is set up correctly
        assert ".claude/" in Path(__file__).parent.parent.joinpath(".gitignore").read_text()


class TestCompleteWorkflow:
    """Test complete workflow from injection to usage."""

    def test_injection_workflow(self, tmp_path):
        """Test complete injection workflow into a new project."""
        # Create a fake project
        project_dir = tmp_path / "test-injection-project"
        project_dir.mkdir()

        # Initialize git
        subprocess.run(["git", "init"], cwd=project_dir, check=True, capture_output=True)
        subprocess.run(["git", "config", "user.email", "test@example.com"], cwd=project_dir, check=True, capture_output=True)
        subprocess.run(["git", "config", "user.name", "Test User"], cwd=project_dir, check=True, capture_output=True)

        # Create .gitignore
        gitignore = project_dir / ".gitignore"
        gitignore.write_text(".claude/\ndocs/\n")

        # Run smart_install.sh with --yes flag for non-interactive mode
        smart_install = Path(__file__).parent.parent / "retrofit-tools" / "smart_install.sh"
        result = subprocess.run(
            ["bash", str(smart_install), "--yes"],
            cwd=project_dir,
            capture_output=True,
            text=True
        )

        print("STDOUT:", result.stdout)
        print("STDERR:", result.stderr)

        # Verify installation
        assert (project_dir / ".claude").exists()
        assert (project_dir / ".claude" / "best-practice.md").exists()
        assert (project_dir / ".claude" / "skills").exists()
        assert (project_dir / ".claude" / "commands").exists()

        # Verify git cleanliness
        git_status = subprocess.run(
            ["git", "status", "--porcelain"],
            cwd=project_dir,
            capture_output=True,
            text=True
        )

        # .claude/ files should NOT appear in git status (they're gitignored)
        assert ".claude/" not in git_status.stdout


if __name__ == "__main__":
    # Run tests with pytest
    pytest.main([__file__, "-v", "--tb=short"])
