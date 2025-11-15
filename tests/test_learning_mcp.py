#!/usr/bin/env python3
"""
Unit tests for Learning MCP - Project-Objective-Driven Features

Tests the new domain-adaptive research capabilities.
"""
import json
import pytest
import tempfile
from pathlib import Path
from datetime import datetime
import sys

# Add parent directory to path to import learning_mcp
sys.path.insert(0, str(Path(__file__).parent.parent / ".claude" / "mcp-servers"))

from learning_mcp import LearningServer


class TestProjectObjectiveDetection:
    """Test detect_project_objective functionality."""

    def test_detect_objective_from_project_plan(self, tmp_path):
        """Test detecting objective from PROJECT_PLAN.md."""
        # Create a mock project with PROJECT_PLAN.md
        project_dir = tmp_path / "test-project"
        project_dir.mkdir()
        docs_dir = project_dir / "docs" / "notes"
        docs_dir.mkdir(parents=True)

        # Create PROJECT_PLAN.md with sample content
        plan_content = """# Test Project - Optimization Tool

## Problem
Need to optimize task allocation across multiple resources with constraints.

## Target Users
Operations managers and resource planners.

## Solution
Build AI-powered optimization engine using constraint programming.

## Success
Reduce planning time by 50% and improve resource utilization by 30%.
"""
        plan_file = docs_dir / "PROJECT_PLAN.md"
        plan_file.write_text(plan_content)

        # Test detection
        server = LearningServer()
        result = server.detect_project_objective(str(project_dir))

        assert result["success"] is True
        assert "objective" in result
        objective = result["objective"]
        assert objective["project_name"] == "test-project"
        assert "optimize" in objective.get("problem", "").lower()
        assert "operations managers" in objective.get("target_users", "").lower()
        assert "constraint programming" in objective.get("solution", "").lower()

    def test_detect_objective_missing_plan(self, tmp_path):
        """Test error handling when PROJECT_PLAN.md doesn't exist."""
        project_dir = tmp_path / "no-plan-project"
        project_dir.mkdir()

        server = LearningServer()
        result = server.detect_project_objective(str(project_dir))

        assert "error" in result
        assert "PROJECT_PLAN.md not found" in result["error"]
        assert "searched_paths" in result


class TestDomainMapping:
    """Test map_objective_to_domains functionality."""

    def test_map_optimization_domain(self):
        """Test mapping optimization keywords to optimization domain."""
        server = LearningServer()

        objective_data = {
            "objective": {
                "project_name": "task-optimizer",
                "title": "Task Optimization System",
                "problem": "Need to optimize resource allocation and minimize costs",
                "solution": "Use linear programming solver with constraint satisfaction"
            }
        }

        result = server.map_objective_to_domains(objective_data)

        assert result["success"] is True
        assert "detected_domains" in result
        assert len(result["detected_domains"]) > 0

        # Primary domain should be optimization
        assert result["primary_domain"] == "optimization"

        # Should have optimization sources
        sources = result["recommended_sources"]
        assert any("optimization" in s.lower() or "scipy" in s.lower() for s in sources)

    def test_map_project_management_domain(self):
        """Test mapping PM keywords to project_management domain."""
        server = LearningServer()

        objective_data = {
            "objective": {
                "project_name": "rapid-pm",
                "title": "Rapid Project Management Tool",
                "problem": "Teams need better sprint planning and backlog management",
                "solution": "Agile project management tool with Scrum and Kanban support"
            }
        }

        result = server.map_objective_to_domains(objective_data)

        assert result["success"] is True
        assert result["primary_domain"] == "project_management"

        # Should have PM-specific sources
        sources = result["recommended_sources"]
        assert any("scrum" in s.lower() or "pmi" in s.lower() or "agile" in s.lower() for s in sources)

    def test_map_claude_development_domain(self):
        """Test mapping Claude/MCP keywords to claude_development domain."""
        server = LearningServer()

        objective_data = {
            "objective": {
                "project_name": "best-practice",
                "title": "Claude Code Best Practices Toolkit",
                "problem": "Need standardized Claude Code development patterns",
                "solution": "MCP servers and skills for enforcing best practices"
            }
        }

        result = server.map_objective_to_domains(objective_data)

        assert result["success"] is True
        assert result["primary_domain"] == "claude_development"

        # Should have Claude/Anthropic sources
        sources = result["recommended_sources"]
        assert any("anthropic" in s.lower() or "claude" in s.lower() for s in sources)


class TestDomainAdaptiveResearch:
    """Test research_domain_topic functionality."""

    def test_research_optimization_topic(self):
        """Test generating research plan for optimization topic."""
        server = LearningServer()
        server.project_domain = "optimization"  # Set domain

        result = server.research_domain_topic(topic="constraint solving")

        assert result["success"] is True
        assert result["domain"] == "optimization"
        assert "search_queries" in result
        assert len(result["search_queries"]) > 0

        # Should have optimization-specific queries
        queries = result["search_queries"]
        assert any("constraint" in q.lower() for q in queries)
        assert any("optimization" in q.lower() or "solver" in q.lower() for q in queries)

        # Should have optimization sources
        sources = result["recommended_sources"]
        assert len(sources) > 0

    def test_research_pm_topic(self):
        """Test generating research plan for PM topic."""
        server = LearningServer()
        server.project_domain = "project_management"

        result = server.research_domain_topic(topic="sprint planning")

        assert result["success"] is True
        assert result["domain"] == "project_management"

        # Should have PM-specific queries
        queries = result["search_queries"]
        assert any("sprint planning" in q.lower() for q in queries)
        assert any("agile" in q.lower() or "scrum" in q.lower() for q in queries)

    def test_research_with_auto_detect_domain(self, tmp_path):
        """Test auto-detecting domain from project_path."""
        # Create project with PROJECT_PLAN.md indicating optimization
        project_dir = tmp_path / "optimizer-project"
        docs_dir = project_dir / "docs" / "notes"
        docs_dir.mkdir(parents=True)

        plan_content = """# Optimizer

## Problem
Optimize resource allocation with constraints.

## Solution
Linear programming solver.
"""
        (docs_dir / "PROJECT_PLAN.md").write_text(plan_content)

        server = LearningServer()
        result = server.research_domain_topic(
            topic="linear programming",
            project_path=str(project_dir)
        )

        assert result["success"] is True
        assert result["domain"] == "optimization"


class TestProjectSpecificStorage:
    """Test store_learning and get_learnings with project-specific storage."""

    def test_store_learning_to_project(self, tmp_path):
        """Test storing learning to project-specific location."""
        project_dir = tmp_path / "test-project"
        project_dir.mkdir()

        server = LearningServer()
        server.project_domain = "optimization"

        learning_data = {
            "domain": "optimization",
            "overview": "Linear programming basics",
            "best_practices": ["Use simplex method", "Check feasibility first"],
            "anti_patterns": ["Don't ignore constraints"],
            "tools": ["scipy.optimize", "PuLP"],
            "sources": ["https://scipy.org/docs"],
            "confidence": "high",
            "recommendations": "Apply to resource allocation"
        }

        result = server.store_learning(
            topic="linear-programming",
            learning_data=learning_data,
            project_path=str(project_dir)
        )

        assert result["success"] is True
        assert result["storage_type"] == "project-specific"

        # Verify file was created
        expected_path = project_dir / "docs" / "references" / "domain-knowledge" / "optimization" / "linear-programming.md"
        assert expected_path.exists()

        # Verify content
        content = expected_path.read_text()
        assert "linear" in content.lower()
        assert "Linear programming basics" in content
        assert "simplex method" in content
        assert "scipy.optimize" in content

    def test_get_learnings_from_project(self, tmp_path):
        """Test retrieving learnings from project-specific location."""
        project_dir = tmp_path / "test-project"
        kb_dir = project_dir / "docs" / "references" / "domain-knowledge" / "optimization"
        kb_dir.mkdir(parents=True)

        # Create a sample learning file
        learning_content = """# Constraint Programming

**Domain**: optimization
**Last Updated**: 2025-11-15
**Confidence**: high

## Overview
Constraint programming techniques for optimization.

## Best Practices
- Define constraints clearly
- Use constraint propagation

## Sources
- https://example.com/cp-guide
"""
        (kb_dir / "constraint-programming.md").write_text(learning_content)

        server = LearningServer()
        result = server.get_learnings(project_path=str(project_dir))

        assert result["success"] is True
        assert result["storage_type"] == "project-specific"
        assert result["count"] == 1
        assert len(result["learnings"]) == 1

        learning = result["learnings"][0]
        assert learning["domain"] == "optimization"
        assert "constraint" in learning["topic"].lower()
        assert learning["format"] == "markdown"

    def test_get_learnings_filter_by_domain(self, tmp_path):
        """Test filtering learnings by domain."""
        project_dir = tmp_path / "multi-domain-project"

        # Create learnings in different domains
        for domain in ["optimization", "project_management"]:
            kb_dir = project_dir / "docs" / "references" / "domain-knowledge" / domain
            kb_dir.mkdir(parents=True)
            (kb_dir / f"{domain}-topic.md").write_text(f"# {domain} topic\n\n**Domain**: {domain}")

        server = LearningServer()

        # Get all learnings
        result_all = server.get_learnings(project_path=str(project_dir))
        assert result_all["count"] == 2

        # Filter by domain
        result_filtered = server.get_learnings(
            project_path=str(project_dir),
            domain="optimization"
        )
        assert result_filtered["count"] == 1
        assert result_filtered["learnings"][0]["domain"] == "optimization"


class TestDynamicScanning:
    """Test that scanning methods return WebFetch instructions instead of hardcoded data."""

    @pytest.mark.asyncio
    async def test_scan_skills_returns_webfetch_instructions(self):
        """Test that scan_anthropic_skills returns WebFetch instructions."""
        server = LearningServer()
        result = await server.scan_anthropic_skills()

        assert result["success"] is True
        assert result["method"] == "dynamic"
        assert "webfetch_urls" in result
        assert len(result["webfetch_urls"]) > 0
        assert "workflow" in result
        assert "WebFetch" in result["workflow"]

    @pytest.mark.asyncio
    async def test_scan_cookbooks_returns_domain_relevance(self):
        """Test that scan_anthropic_cookbooks includes domain filtering."""
        server = LearningServer()
        result = await server.scan_anthropic_cookbooks()

        assert result["success"] is True
        assert result["method"] == "dynamic"
        assert "domain_relevance" in result

        # Should have domain-specific mappings
        relevance = result["domain_relevance"]
        assert "optimization" in relevance
        assert "project_management" in relevance
        assert "claude_development" in relevance

    @pytest.mark.asyncio
    async def test_scan_org_returns_domain_priority(self):
        """Test that scan_anthropic_org includes domain priority."""
        server = LearningServer()
        result = await server.scan_anthropic_org()

        assert result["success"] is True
        assert "domain_priority" in result

        # Should prioritize different repos for different domains
        priority = result["domain_priority"]
        assert priority["claude_development"] == "all repos"
        assert isinstance(priority["optimization"], list)


class TestEndToEndWorkflow:
    """Test complete workflow from objective detection to research storage."""

    def test_complete_research_workflow(self, tmp_path):
        """Test full workflow: detect objective → map domain → research → store."""
        # Setup: Create project with PROJECT_PLAN.md
        project_dir = tmp_path / "research-test-project"
        docs_dir = project_dir / "docs" / "notes"
        docs_dir.mkdir(parents=True)

        plan_content = """# Optimization Engine

## Problem
Optimize delivery routes for logistics company.

## Solution
Vehicle routing optimization using constraint programming.
"""
        (docs_dir / "PROJECT_PLAN.md").write_text(plan_content)

        server = LearningServer()

        # Step 1: Detect objective
        obj_result = server.detect_project_objective(str(project_dir))
        assert obj_result["success"] is True

        # Step 2: Map to domains
        domain_result = server.map_objective_to_domains(obj_result)
        assert domain_result["success"] is True
        assert domain_result["primary_domain"] == "optimization"

        # Step 3: Generate research plan
        research_result = server.research_domain_topic(
            topic="vehicle routing",
            project_path=str(project_dir)
        )
        assert research_result["success"] is True
        assert research_result["domain"] == "optimization"
        assert "search_queries" in research_result

        # Step 4: Store research (simulate)
        learning_data = {
            "domain": "optimization",
            "overview": "Vehicle routing optimization techniques",
            "best_practices": ["Use Clarke-Wright algorithm", "Consider time windows"],
            "sources": ["https://optimization.example.com/vrp"],
            "confidence": "high",
            "recommendations": "Apply to delivery route planning"
        }

        store_result = server.store_learning(
            topic="vehicle-routing",
            learning_data=learning_data,
            project_path=str(project_dir)
        )
        assert store_result["success"] is True
        assert store_result["storage_type"] == "project-specific"

        # Step 5: Retrieve stored learning
        get_result = server.get_learnings(
            project_path=str(project_dir),
            domain="optimization"
        )
        assert get_result["success"] is True
        assert get_result["count"] == 1
        assert "vehicle" in get_result["learnings"][0]["topic"].lower()


if __name__ == "__main__":
    # Run tests with pytest
    pytest.main([__file__, "-v", "--tb=short"])
