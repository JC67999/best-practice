#!/usr/bin/env python3
"""
Universal Memory MCP Server
Persistent context across all projects and sessions
"""
import asyncio
import json
import os
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional

from mcp.server import Server
from mcp.server.stdio import stdio_server
from mcp.types import Tool, TextContent


# Storage location
MEMORY_DIR = Path.home() / ".claude_memory"
MEMORY_DIR.mkdir(exist_ok=True)


class MemoryServer:
    """Universal memory server for persistent context."""

    def __init__(self):
        self.server = Server("memory-server")
        self.setup_handlers()

    def setup_handlers(self):
        """Setup MCP tool handlers."""

        @self.server.list_tools()
        async def list_tools() -> list[Tool]:
            return [
                Tool(
                    name="save_session_summary",
                    description="Save session summary for a project",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "project_path": {
                                "type": "string",
                                "description": "Absolute path to project"
                            },
                            "summary": {
                                "type": "string",
                                "description": "Brief summary of session"
                            },
                            "decisions": {
                                "type": "array",
                                "items": {"type": "string"},
                                "description": "Key decisions made"
                            },
                            "next_steps": {
                                "type": "array",
                                "items": {"type": "string"},
                                "description": "Next steps to take"
                            },
                            "blockers": {
                                "type": "array",
                                "items": {"type": "string"},
                                "description": "Current blockers"
                            }
                        },
                        "required": ["project_path", "summary"]
                    }
                ),
                Tool(
                    name="load_project_context",
                    description="Load project context from memory",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "project_path": {
                                "type": "string",
                                "description": "Absolute path to project"
                            }
                        },
                        "required": ["project_path"]
                    }
                ),
                Tool(
                    name="save_decision",
                    description="Save architectural or technical decision",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "project_path": {
                                "type": "string",
                                "description": "Absolute path to project"
                            },
                            "decision": {
                                "type": "string",
                                "description": "Decision made"
                            },
                            "rationale": {
                                "type": "string",
                                "description": "Rationale for decision"
                            }
                        },
                        "required": ["project_path", "decision", "rationale"]
                    }
                ),
                Tool(
                    name="list_projects",
                    description="List all tracked projects",
                    inputSchema={
                        "type": "object",
                        "properties": {}
                    }
                ),
                Tool(
                    name="search_memory",
                    description="Search across all projects for relevant context",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "query": {
                                "type": "string",
                                "description": "Search query"
                            }
                        },
                        "required": ["query"]
                    }
                ),
                Tool(
                    name="save_project_objective",
                    description="Save project objective data",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "project_path": {
                                "type": "string",
                                "description": "Absolute path to project"
                            },
                            "objective_data": {
                                "type": "object",
                                "description": "Complete objective data"
                            }
                        },
                        "required": ["project_path", "objective_data"]
                    }
                ),
                Tool(
                    name="load_project_objective",
                    description="Load project objective from memory",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "project_path": {
                                "type": "string",
                                "description": "Absolute path to project"
                            }
                        },
                        "required": ["project_path"]
                    }
                )
            ]

        @self.server.call_tool()
        async def call_tool(name: str, arguments: Any) -> list[TextContent]:
            try:
                if name == "save_session_summary":
                    result = self.save_session_summary(**arguments)
                elif name == "load_project_context":
                    result = self.load_project_context(**arguments)
                elif name == "save_decision":
                    result = self.save_decision(**arguments)
                elif name == "list_projects":
                    result = self.list_projects()
                elif name == "search_memory":
                    result = self.search_memory(**arguments)
                elif name == "save_project_objective":
                    result = self.save_project_objective(**arguments)
                elif name == "load_project_objective":
                    result = self.load_project_objective(**arguments)
                else:
                    result = {"error": f"Unknown tool: {name}"}

                return [TextContent(type="text", text=json.dumps(result, indent=2))]
            except Exception as e:
                return [TextContent(type="text", text=json.dumps({"error": str(e)}, indent=2))]

    def get_storage_dir(self) -> Path:
        """Get memory storage directory path."""
        return MEMORY_DIR

    def get_project_id(self, project_path: str) -> str:
        """Generate project ID from path."""
        return Path(project_path).name.replace(" ", "_").lower()

    def get_project_file(self, project_path: str) -> Path:
        """Get path to project memory file."""
        project_id = self.get_project_id(project_path)
        return MEMORY_DIR / f"{project_id}.json"

    def load_project_data(self, project_path: str) -> Dict:
        """Load project data from memory."""
        project_file = self.get_project_file(project_path)

        if not project_file.exists():
            return {
                "project_id": self.get_project_id(project_path),
                "project_path": project_path,
                "created_at": datetime.now().isoformat(),
                "sessions": [],
                "decisions": [],
                "objective": None,
                "tech_stack": [],
                "current_status": "active"
            }

        with open(project_file) as f:
            return json.load(f)

    def save_project_data(self, project_path: str, data: Dict):
        """Save project data to memory."""
        project_file = self.get_project_file(project_path)
        data["updated_at"] = datetime.now().isoformat()

        with open(project_file, 'w') as f:
            json.dump(data, f, indent=2)

    def save_session_summary(
        self,
        project_path: str,
        summary: str,
        decisions: Optional[List[str]] = None,
        next_steps: Optional[List[str]] = None,
        blockers: Optional[List[str]] = None
    ) -> Dict:
        """Save session summary."""
        data = self.load_project_data(project_path)

        session = {
            "timestamp": datetime.now().isoformat(),
            "summary": summary,
            "decisions": decisions or [],
            "next_steps": next_steps or [],
            "blockers": blockers or []
        }

        data["sessions"].append(session)

        # Keep only last 10 sessions
        if len(data["sessions"]) > 10:
            data["sessions"] = data["sessions"][-10:]

        self.save_project_data(project_path, data)

        return {
            "success": True,
            "message": "Session summary saved",
            "project_id": self.get_project_id(project_path)
        }

    def load_project_context(self, project_path: str) -> Dict:
        """Load project context."""
        data = self.load_project_data(project_path)

        # Get last 3 sessions
        recent_sessions = data["sessions"][-3:] if data["sessions"] else []

        return {
            "project_id": data["project_id"],
            "project_path": data["project_path"],
            "objective": data.get("objective"),
            "recent_sessions": recent_sessions,
            "all_decisions": data["decisions"],
            "current_status": data.get("current_status", "active"),
            "tech_stack": data.get("tech_stack", []),
            "last_updated": data.get("updated_at", data.get("created_at"))
        }

    def save_decision(
        self,
        project_path: str,
        decision: str,
        rationale: str
    ) -> Dict:
        """Save architectural/technical decision."""
        data = self.load_project_data(project_path)

        decision_entry = {
            "timestamp": datetime.now().isoformat(),
            "decision": decision,
            "rationale": rationale
        }

        data["decisions"].append(decision_entry)

        self.save_project_data(project_path, data)

        return {
            "success": True,
            "message": "Decision saved",
            "decision_count": len(data["decisions"])
        }

    def list_projects(self) -> Dict:
        """List all tracked projects."""
        projects = []

        for project_file in MEMORY_DIR.glob("*.json"):
            try:
                with open(project_file) as f:
                    data = json.load(f)
                    projects.append({
                        "project_id": data["project_id"],
                        "project_path": data.get("project_path", "Unknown"),
                        "last_activity": data.get("updated_at", data.get("created_at", "Unknown")),
                        "session_count": len(data.get("sessions", [])),
                        "has_objective": data.get("objective") is not None
                    })
            except:
                pass

        # Sort by last activity
        projects.sort(key=lambda x: x["last_activity"], reverse=True)

        return {
            "total_projects": len(projects),
            "projects": projects
        }

    def search_memory(self, query: str) -> Dict:
        """Search across all projects."""
        query_lower = query.lower()
        results = []

        for project_file in MEMORY_DIR.glob("*.json"):
            try:
                with open(project_file) as f:
                    data = json.load(f)

                    matches = []

                    # Search in sessions
                    for session in data.get("sessions", []):
                        if query_lower in session.get("summary", "").lower():
                            matches.append({
                                "type": "session",
                                "timestamp": session.get("timestamp"),
                                "content": session.get("summary")
                            })

                    # Search in decisions
                    for decision in data.get("decisions", []):
                        if query_lower in decision.get("decision", "").lower() or \
                           query_lower in decision.get("rationale", "").lower():
                            matches.append({
                                "type": "decision",
                                "timestamp": decision.get("timestamp"),
                                "content": f"{decision.get('decision')} - {decision.get('rationale')}"
                            })

                    # Search in objective
                    objective = data.get("objective")
                    if objective and isinstance(objective, dict):
                        objective_str = json.dumps(objective).lower()
                        if query_lower in objective_str:
                            matches.append({
                                "type": "objective",
                                "content": "Objective contains search term"
                            })

                    if matches:
                        results.append({
                            "project_id": data["project_id"],
                            "project_path": data.get("project_path"),
                            "matches": matches[:5]  # Limit to 5 per project
                        })

            except:
                pass

        return {
            "query": query,
            "total_results": len(results),
            "results": results[:10]  # Limit to 10 projects
        }

    def save_project_objective(
        self,
        project_path: str,
        objective_data: Dict
    ) -> Dict:
        """Save project objective."""
        data = self.load_project_data(project_path)
        data["objective"] = objective_data
        self.save_project_data(project_path, data)

        return {
            "success": True,
            "message": "Project objective saved",
            "clarity_score": objective_data.get("clarity_score", 0)
        }

    def load_project_objective(self, project_path: str) -> Dict:
        """Load project objective."""
        data = self.load_project_data(project_path)

        if not data.get("objective"):
            return {
                "found": False,
                "message": "No objective found for project"
            }

        return {
            "found": True,
            "objective": data["objective"]
        }

    async def run(self):
        """Run the MCP server."""
        async with stdio_server() as (read_stream, write_stream):
            await self.server.run(
                read_stream,
                write_stream,
                self.server.create_initialization_options()
            )


async def main():
    """Main entry point."""
    server = MemoryServer()
    await server.run()


if __name__ == "__main__":
    asyncio.run(main())
