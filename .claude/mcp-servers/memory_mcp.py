#!/usr/bin/env python3
"""
Universal Memory MCP Server
Persistent context across all projects and sessions
"""
import asyncio
import json
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional

from mcp.server import Server
from mcp.server.stdio import stdio_server
from mcp.types import Tool, TextContent, Prompt, PromptArgument, GetPromptResult, PromptMessage


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

        @self.server.list_prompts()
        async def list_prompts() -> list[Prompt]:
            """List available memory prompts."""
            return [
                Prompt(
                    name="session_start",
                    description="Load project context and summarize for session start",
                    arguments=[
                        PromptArgument(
                            name="project_path",
                            description="Absolute path to project directory",
                            required=True
                        )
                    ]
                ),
                Prompt(
                    name="session_end",
                    description="Guided session summary before ending work",
                    arguments=[
                        PromptArgument(
                            name="project_path",
                            description="Absolute path to project directory",
                            required=True
                        )
                    ]
                ),
                Prompt(
                    name="document_decision",
                    description="Document an architectural or technical decision with rationale",
                    arguments=[
                        PromptArgument(
                            name="project_path",
                            description="Absolute path to project directory",
                            required=True
                        ),
                        PromptArgument(
                            name="topic",
                            description="Topic or decision area (e.g., 'authentication', 'database choice')",
                            required=True
                        )
                    ]
                )
            ]

        @self.server.get_prompt()
        async def get_prompt(name: str, arguments: dict[str, str] | None) -> GetPromptResult:
            """Get a specific prompt template."""
            if arguments is None:
                arguments = {}

            if name == "session_start":
                project_path = arguments.get("project_path", "")

                # Load project context
                context_summary = ""
                try:
                    result = self.load_project_context(project_path=project_path)

                    if "error" not in result:
                        objective = result.get("objective", {})
                        recent_sessions = result.get("recent_sessions", [])
                        decisions = result.get("decisions", [])

                        context_summary = f"""
**Project Context Loaded**:

**Objective**:
- Problem: {objective.get('problem', 'Not defined')}
- Target Users: {objective.get('target_users', 'Not defined')}
- Solution: {objective.get('solution', 'Not defined')}
- Clarity Score: {objective.get('clarity_score', 0)}/100

**Recent Sessions** (last 3):
{chr(10).join(f"- {s.get('summary', 'No summary')}" for s in recent_sessions[-3:]) if recent_sessions else "- None"}

**Key Decisions** (last 3):
{chr(10).join(f"- {d.get('decision', 'No decision')}" for d in decisions[-3:]) if decisions else "- None"}

**Next Steps from Last Session**:
{chr(10).join(f"- {step}" for step in recent_sessions[-1].get('next_steps', [])) if recent_sessions else "- None"}

**Current Blockers**:
{chr(10).join(f"- {blocker}" for blocker in recent_sessions[-1].get('blockers', [])) if recent_sessions and recent_sessions[-1].get('blockers') else "- None"}
"""
                    else:
                        context_summary = "\n**Note**: No previous context found. This may be a new project.\n"
                except:
                    context_summary = "\n**Note**: Could not load project context.\n"

                prompt_text = f"""You are starting a new session for the project at: {project_path}
{context_summary}
## Session Start Checklist

### 1. Review Context
- Understand the project objective
- Review recent work (last sessions)
- Note key decisions made
- Identify next steps from last session
- Check for blockers

### 2. Set Session Goal
Based on the context above, what should this session accomplish?
- Is there a specific task to complete?
- Are we continuing from where we left off?
- Are there any blockers to address first?

### 3. Load Detailed Status
You may want to call:
- `get_current_status` (Project MCP) - See current task list
- `score_objective_clarity` (Project MCP) - Check if objective needs clarification
- `search_memory` - Search for specific past context

### 4. Plan This Session
Given the context and next steps, create a plan for THIS session:
1. What will we accomplish?
2. What's the success criteria?
3. What risks or unknowns exist?

### Output Format

```markdown
## Session Start: {project_path}

### Context Summary
- Objective Clarity: {context_summary.split('Clarity Score: ')[1].split('/100')[0] if 'Clarity Score:' in context_summary else '0'}/100
- Last Session: [date/summary if available]
- Current Phase: [infer from next steps]

### Session Goal
**What we'll accomplish today**:
- [goal 1]
- [goal 2]

**Success Criteria**:
- [ ] [criterion 1]
- [ ] [criterion 2]

### Action Plan
1. [First task]
2. [Second task]
3. [Third task]

### Blockers to Address
{chr(10).join(f"- {blocker}" for blocker in (recent_sessions[-1].get('blockers', []) if recent_sessions else [])) if recent_sessions else "- None identified"}

### Next Steps
[After reviewing context, what should we tackle first?]
```

**Now provide the session start summary and plan.**
"""

                return GetPromptResult(
                    description="Session start with context loading",
                    messages=[
                        PromptMessage(
                            role="user",
                            content=TextContent(type="text", text=prompt_text)
                        )
                    ]
                )

            elif name == "session_end":
                project_path = arguments.get("project_path", "")

                prompt_text = f"""You are ending a work session for the project at: {project_path}

## Session End - Save Context for Next Time

### Required: Complete Session Summary

You MUST call `save_session_summary` with the following information:

**project_path**: {project_path}

**summary**: (Required) Brief overview of what was accomplished
- 1-3 sentences max
- Focus on WHAT was done, not HOW
- Example: "Implemented user authentication with JWT tokens and added password reset functionality"

**decisions**: (Optional) List of key decisions made
- Format as array of strings
- Example: ["Using bcrypt for password hashing", "JWT tokens expire after 24 hours"]
- Only include significant decisions that affect future work

**next_steps**: (Required) What should be done in the next session
- Format as array of strings
- Concrete, actionable items
- Example: ["Add email verification", "Implement rate limiting on login", "Add password strength requirements"]

**blockers**: (Optional) Current blockers or issues
- Format as array of strings
- Example: ["Need API key for email service", "Unclear password strength requirements"]

### Session End Checklist

#### 1. What Was Accomplished?
- List completed tasks
- Highlight wins
- Note any partial work

#### 2. What Decisions Were Made?
- Technical decisions
- Architectural choices
- Trade-offs accepted
- Why these decisions were made

#### 3. What's Next?
- Immediate next tasks
- Priorities for next session
- Dependencies to unblock

#### 4. Any Blockers?
- What's blocking progress?
- What needs clarification?
- What external dependencies exist?

### Output Format

```markdown
## Session End Summary

### Accomplished
- [completed task 1]
- [completed task 2]
- [partial work if any]

### Key Decisions
1. **[Decision]**: [Rationale]
2. **[Decision]**: [Rationale]

### Next Session
**Priority tasks**:
1. [task 1] - [why it's next]
2. [task 2] - [dependency info]
3. [task 3]

### Blockers
- [blocker 1]: [what's needed to unblock]
- [blocker 2]: [action required]

### Ready to Save
Now call `save_session_summary` with:
- summary: "[your 1-3 sentence summary]"
- decisions: [list of decision strings]
- next_steps: [list of next step strings]
- blockers: [list of blocker strings]
```

**Now create your session end summary and call save_session_summary.**
"""

                return GetPromptResult(
                    description="Session end with guided summary",
                    messages=[
                        PromptMessage(
                            role="user",
                            content=TextContent(type="text", text=prompt_text)
                        )
                    ]
                )

            elif name == "document_decision":
                project_path = arguments.get("project_path", "")
                topic = arguments.get("topic", "")

                prompt_text = f"""You are documenting a decision for: **{topic}**

Project: {project_path}

## Decision Documentation Framework

### Why Document Decisions?
- Future you won't remember why
- Team members need context
- Prevents re-litigating settled questions
- Builds institutional knowledge

### Required Information

#### 1. What Decision Was Made?
- Clear statement of the decision
- Be specific and actionable
- Example: "Use PostgreSQL for primary database" (not "Use SQL database")

#### 2. What Were the Options Considered?
- List alternatives that were evaluated
- Example: PostgreSQL vs MySQL vs MongoDB

#### 3. Why This Decision?
- Technical rationale
- Business constraints
- Trade-offs accepted
- Example: "PostgreSQL chosen for JSONB support, strong ACID guarantees, and team familiarity"

#### 4. What Trade-offs Were Accepted?
- What did we give up?
- What limitations does this introduce?
- Example: "Accepted complexity of PostgreSQL vs simpler NoSQL options"

#### 5. When Can This Be Revisited?
- Under what conditions should we reconsider?
- What would trigger a review?
- Example: "Revisit if we need horizontal scaling beyond 10M records"

### Output Format

```markdown
## Decision: {topic}

### Context
**Date**: {datetime.now().strftime('%Y-%m-%d')}
**Project**: {project_path}
**Topic**: {topic}

### Decision Made
[Clear, specific statement of what was decided]

### Options Considered
1. **[Option A]**
   - Pros: [list]
   - Cons: [list]
2. **[Option B]**
   - Pros: [list]
   - Cons: [list]
3. **[Option C]**
   - Pros: [list]
   - Cons: [list]

### Rationale
**Why we chose [Option X]**:
1. [Reason 1]
2. [Reason 2]
3. [Reason 3]

**Trade-offs accepted**:
- [Trade-off 1]: [Why acceptable]
- [Trade-off 2]: [Why acceptable]

### Constraints Considered
- [Constraint 1]
- [Constraint 2]

### Review Triggers
**Revisit this decision if**:
- [Condition 1]
- [Condition 2]

### Next Steps
- [ ] [Action item 1]
- [ ] [Action item 2]

### Ready to Save
Now call `save_decision` with:
- project_path: "{project_path}"
- decision: "[your decision statement]"
- rationale: "[your full rationale with options, trade-offs, etc.]"
```

**Now document the decision for: {topic}**
"""

                return GetPromptResult(
                    description=f"Document decision: {topic}",
                    messages=[
                        PromptMessage(
                            role="user",
                            content=TextContent(type="text", text=prompt_text)
                        )
                    ]
                )

            else:
                raise ValueError(f"Unknown prompt: {name}")

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
            except Exception:
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

            except Exception:
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
