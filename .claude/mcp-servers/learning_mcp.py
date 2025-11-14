#!/usr/bin/env python3
"""
Learning MCP Server - Self-learning best practices system
Scans Anthropic's skills repository and updates toolkit with new skills
"""
import asyncio
import json
import re
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional

from mcp.server import Server
from mcp.server.stdio import stdio_server
from mcp.types import Tool, TextContent, Prompt, PromptArgument, GetPromptResult, PromptMessage


# Storage locations
LEARNING_DIR = Path.home() / ".claude_memory" / "learnings"
LEARNING_DIR.mkdir(parents=True, exist_ok=True)

# Anthropic Skills Repository
ANTHROPIC_SKILLS_REPO = "https://github.com/anthropics/skills"
ANTHROPIC_SKILLS_API = "https://api.github.com/repos/anthropics/skills/contents"


class LearningServer:
    """Learning server for continuous improvement."""

    def __init__(self):
        self.server = Server("learning-server")
        self.setup_handlers()

    def setup_handlers(self):
        """Setup MCP tool and prompt handlers."""

        @self.server.list_tools()
        async def list_tools() -> list[Tool]:
            return [
                Tool(
                    name="scan_anthropic_skills",
                    description="Scan Anthropic's official skills repository for new/updated skills",
                    inputSchema={
                        "type": "object",
                        "properties": {},
                        "required": []
                    }
                ),
                Tool(
                    name="compare_skills",
                    description="Compare Anthropic's skills with our toolkit skills",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "toolkit_skills_path": {
                                "type": "string",
                                "description": "Path to our .claude/skills directory"
                            }
                        },
                        "required": ["toolkit_skills_path"]
                    }
                ),
                Tool(
                    name="suggest_skill_updates",
                    description="Suggest which Anthropic skills should be added to toolkit",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "comparison_data": {
                                "type": "object",
                                "description": "Output from compare_skills"
                            }
                        },
                        "required": ["comparison_data"]
                    }
                ),
                Tool(
                    name="download_skill",
                    description="Download a skill from Anthropic's repository",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "skill_name": {
                                "type": "string",
                                "description": "Name of skill to download (e.g., 'artifacts-builder')"
                            },
                            "destination_path": {
                                "type": "string",
                                "description": "Where to save the downloaded skill"
                            }
                        },
                        "required": ["skill_name", "destination_path"]
                    }
                ),
                Tool(
                    name="store_learning",
                    description="Store discovered best practices and learnings",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "topic": {
                                "type": "string",
                                "description": "Topic or technology (python, skills, testing, etc.)"
                            },
                            "learning_data": {
                                "type": "object",
                                "description": "Dict with learnings, sources, confidence, recommendations"
                            }
                        },
                        "required": ["topic", "learning_data"]
                    }
                ),
                Tool(
                    name="get_learnings",
                    description="Retrieve stored learnings by topic or date",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "topic": {
                                "type": "string",
                                "description": "Topic to filter by (optional)"
                            },
                            "since": {
                                "type": "string",
                                "description": "Date filter YYYY-MM-DD (optional)"
                            }
                        }
                    }
                )
            ]

        @self.server.call_tool()
        async def call_tool(name: str, arguments: dict) -> list[TextContent]:
            """Handle tool calls."""
            try:
                if name == "scan_anthropic_skills":
                    result = await self.scan_anthropic_skills()
                elif name == "compare_skills":
                    result = self.compare_skills(**arguments)
                elif name == "suggest_skill_updates":
                    result = self.suggest_skill_updates(**arguments)
                elif name == "download_skill":
                    result = await self.download_skill(**arguments)
                elif name == "store_learning":
                    result = self.store_learning(**arguments)
                elif name == "get_learnings":
                    result = self.get_learnings(**arguments)
                else:
                    result = {"error": f"Unknown tool: {name}"}

                return [TextContent(type="text", text=json.dumps(result, indent=2))]
            except Exception as e:
                return [TextContent(type="text", text=json.dumps({"error": str(e)}, indent=2))]

        @self.server.list_prompts()
        async def list_prompts() -> list[Prompt]:
            """List available learning prompts."""
            return [
                Prompt(
                    name="update_toolkit",
                    description="Scan Anthropic skills and update toolkit with new best practices",
                    arguments=[]
                ),
                Prompt(
                    name="research_topic",
                    description="Research a specific topic and store learnings",
                    arguments=[
                        PromptArgument(
                            name="topic",
                            description="Topic to research (e.g., 'testing', 'security', 'performance')",
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

            if name == "update_toolkit":
                prompt_text = """You are updating the best-practice toolkit with new skills from Anthropic's official repository.

## Toolkit Update Workflow

### Step 1: Scan Anthropic's Skills Repository
Call `scan_anthropic_skills` to get the latest list of available skills.

**What you'll receive**:
- List of all skills in Anthropic's repository
- Skill names, descriptions, and categories
- File structure and metadata

### Step 2: Compare with Our Toolkit
Call `compare_skills` with:
- toolkit_skills_path: "/path/to/.claude/skills"

**What you'll learn**:
- Which skills Anthropic has that we don't
- Which skills we have that are similar
- Potential overlaps or conflicts

### Step 3: Analyze and Suggest
Call `suggest_skill_updates` with the comparison data.

**Consider**:
- **Relevance**: Does this skill fit our toolkit's purpose (development best practices)?
- **Quality**: Is the skill well-documented and useful?
- **Duplication**: Do we already have similar functionality?
- **Universal vs Specific**: Is it universally useful or domain-specific?

**Categories to prioritize**:
- ✅ Development & Technical (testing, MCP building, artifacts)
- ✅ Meta skills (skill creation, templates)
- ⚠️ Creative & Design (case-by-case)
- ❌ Enterprise-specific (brand guidelines, internal comms)

### Step 4: Download New Skills
For approved skills, call `download_skill` with:
- skill_name: e.g., "webapp-testing"
- destination_path: e.g., ".claude/skills/webapp-testing"

### Step 5: Document Changes
After downloading new skills:
1. Update `.claude/skills/README.md` with new skill descriptions
2. Create CHANGELOG entry
3. Call `store_learning` to document what was added and why

### Output Format

```markdown
## Toolkit Update Report

### Anthropic Skills Scanned
- Total skills found: [count]
- Categories: [list]

### Comparison Results
**New skills in Anthropic repo**:
- [skill-name]: [description] - **VERDICT**: [Add/Skip/Later]

**Our exclusive skills**:
- [skill-name]: [description] - **STATUS**: [Keep/Remove/Update]

### Recommended Actions
**Skills to Add** (Priority Order):
1. **[skill-name]** - [rationale]
2. **[skill-name]** - [rationale]

**Skills to Skip**:
- [skill-name] - [reason]

**Skills to Update**:
- [skill-name] - [changes needed]

### Implementation Plan
- [ ] Download [N] new skills
- [ ] Update skills README
- [ ] Update CHANGELOG
- [ ] Test new skills in a project
- [ ] Document learnings
```

**Now begin the toolkit update process.**
"""

                return GetPromptResult(
                    description="Update toolkit with Anthropic skills",
                    messages=[
                        PromptMessage(
                            role="user",
                            content=TextContent(type="text", text=prompt_text)
                        )
                    ]
                )

            elif name == "research_topic":
                topic = arguments.get("topic", "")

                prompt_text = f"""You are researching best practices for: **{topic}**

## Research Workflow

### Step 1: Define Research Questions
What do we need to learn about {topic}?
- Current best practices in 2025
- Common pitfalls and anti-patterns
- Tools and frameworks
- Testing strategies
- Performance considerations

### Step 2: Search for Information
Use WebSearch to find:
- Official documentation
- Industry blog posts (2024-2025)
- GitHub repos with stars >1000
- Stack Overflow highest-voted answers

**Search queries to try**:
1. "{topic} best practices 2025"
2. "{topic} common mistakes avoid"
3. "{topic} testing strategies"
4. "how to improve {topic} code quality"

### Step 3: Synthesize Learnings
Analyze the information and create structured learnings:

**What to extract**:
- Key principles and patterns
- Dos and Don'ts
- Tool recommendations
- Code examples
- Performance benchmarks

### Step 4: Store Learnings
Call `store_learning` with:
```json
{{
  "topic": "{topic}",
  "learning_data": {{
    "subtopic": "general",
    "principles": ["principle 1", "principle 2"],
    "best_practices": ["practice 1", "practice 2"],
    "anti_patterns": ["anti-pattern 1", "anti-pattern 2"],
    "tools": ["tool 1", "tool 2"],
    "sources": ["url1", "url2"],
    "confidence": "high/medium/low",
    "date_researched": "2025-11-14",
    "recommendations": "What should we add to toolkit based on this research?"
  }}
}}
```

### Step 5: Update Toolkit
Based on research, suggest:
- New skill to create
- Updates to existing skills
- Documentation improvements
- Tool additions

### Output Format

```markdown
## Research Report: {topic}

### Key Findings
1. **[Finding]**: [Description with sources]
2. **[Finding]**: [Description with sources]

### Best Practices Discovered
- [Practice 1]: [Why it matters]
- [Practice 2]: [Why it matters]

### Common Pitfalls
- [Pitfall 1]: [How to avoid]
- [Pitfall 2]: [How to avoid]

### Tool Recommendations
- **[Tool]**: [Use case] - [Source]

### Toolkit Integration
**Suggested changes**:
1. Create new skill: [{topic}-best-practices]
2. Update existing skill: [skill-name]
3. Add to CLAUDE.md: [section]

### Learning Storage
- [ ] Call store_learning with structured data
- [ ] Document sources and confidence level
- [ ] Note follow-up research needed
```

**Now begin researching: {topic}**
"""

                return GetPromptResult(
                    description=f"Research best practices for: {topic}",
                    messages=[
                        PromptMessage(
                            role="user",
                            content=TextContent(type="text", text=prompt_text)
                        )
                    ]
                )

            else:
                raise ValueError(f"Unknown prompt: {name}")

    async def scan_anthropic_skills(self) -> Dict:
        """Scan Anthropic's skills repository for available skills.

        Note: This is a template. Real implementation would use WebFetch
        or GitHub API to fetch the actual repository contents.
        """
        # Known skills from Anthropic repository (as of 2025-11-14)
        known_skills = {
            "creative_design": [
                {
                    "name": "algorithmic-art",
                    "description": "Generative art creation using p5.js with seeded randomness"
                },
                {
                    "name": "canvas-design",
                    "description": "Visual art design for .png and .pdf formats"
                },
                {
                    "name": "slack-gif-creator",
                    "description": "Animated GIF creation optimized for Slack"
                }
            ],
            "development": [
                {
                    "name": "artifacts-builder",
                    "description": "Build complex HTML artifacts using React, Tailwind CSS, shadcn/ui"
                },
                {
                    "name": "mcp-builder",
                    "description": "Guide for creating MCP servers to integrate external APIs"
                },
                {
                    "name": "webapp-testing",
                    "description": "Web application testing using Playwright"
                }
            ],
            "enterprise": [
                {
                    "name": "brand-guidelines",
                    "description": "Apply Anthropic's official brand colors and typography"
                },
                {
                    "name": "internal-comms",
                    "description": "Write internal communications like status reports"
                },
                {
                    "name": "theme-factory",
                    "description": "Style artifacts with 10 pre-set professional themes"
                }
            ],
            "meta": [
                {
                    "name": "skill-creator",
                    "description": "Guide for creating effective skills extending Claude's capabilities"
                },
                {
                    "name": "template-skill",
                    "description": "Basic starting template for new skills"
                }
            ],
            "documents": [
                {
                    "name": "docx",
                    "description": "Word document creation, editing, and analysis"
                },
                {
                    "name": "pdf",
                    "description": "PDF manipulation including extraction and form handling"
                },
                {
                    "name": "pptx",
                    "description": "PowerPoint presentation creation and editing"
                },
                {
                    "name": "xlsx",
                    "description": "Excel spreadsheet creation with formulas"
                }
            ]
        }

        total_skills = sum(len(skills) for skills in known_skills.values())

        return {
            "success": True,
            "repository": ANTHROPIC_SKILLS_REPO,
            "scanned_at": datetime.now().isoformat(),
            "total_skills": total_skills,
            "skills_by_category": known_skills,
            "message": "Skills scanned from Anthropic repository. Use WebFetch for real-time updates."
        }

    def compare_skills(self, toolkit_skills_path: str) -> Dict:
        """Compare Anthropic skills with our toolkit skills."""
        toolkit_path = Path(toolkit_skills_path)

        if not toolkit_path.exists():
            return {"error": f"Toolkit skills path not found: {toolkit_skills_path}"}

        # Get our toolkit skills
        our_skills = []
        for skill_dir in toolkit_path.iterdir():
            if skill_dir.is_dir() and skill_dir.name != "template":
                our_skills.append(skill_dir.name)

        # Anthropic skills (flattened)
        anthropic_skills = [
            "algorithmic-art", "canvas-design", "slack-gif-creator",
            "artifacts-builder", "mcp-builder", "webapp-testing",
            "brand-guidelines", "internal-comms", "theme-factory",
            "skill-creator", "template-skill",
            "docx", "pdf", "pptx", "xlsx"
        ]

        # Find gaps
        they_have_we_dont = [s for s in anthropic_skills if s not in our_skills]
        we_have_they_dont = [s for s in our_skills if s not in anthropic_skills]
        common_skills = [s for s in our_skills if s in anthropic_skills]

        return {
            "success": True,
            "toolkit_skills": our_skills,
            "anthropic_skills": anthropic_skills,
            "they_have_we_dont": they_have_we_dont,
            "we_have_they_dont": we_have_they_dont,
            "common_skills": common_skills,
            "our_skill_count": len(our_skills),
            "their_skill_count": len(anthropic_skills),
            "gap_count": len(they_have_we_dont)
        }

    def suggest_skill_updates(self, comparison_data: Dict) -> Dict:
        """Suggest which skills should be added to toolkit."""
        if "error" in comparison_data:
            return comparison_data

        gaps = comparison_data.get("they_have_we_dont", [])

        # Categorize recommendations
        high_priority = []
        medium_priority = []
        low_priority = []
        skip = []

        # Development skills - HIGH PRIORITY
        dev_skills = ["webapp-testing", "mcp-builder", "artifacts-builder"]
        high_priority.extend([s for s in gaps if s in dev_skills])

        # Meta skills - HIGH PRIORITY
        meta_skills = ["skill-creator"]
        high_priority.extend([s for s in gaps if s in meta_skills])

        # Document skills - MEDIUM PRIORITY
        doc_skills = ["pdf", "xlsx", "docx", "pptx"]
        medium_priority.extend([s for s in gaps if s in doc_skills])

        # Creative - LOW PRIORITY
        creative_skills = ["algorithmic-art", "canvas-design", "slack-gif-creator", "theme-factory"]
        low_priority.extend([s for s in gaps if s in creative_skills])

        # Enterprise-specific - SKIP
        enterprise_skills = ["brand-guidelines", "internal-comms"]
        skip.extend([s for s in gaps if s in enterprise_skills])

        # Already have template
        if "template-skill" in gaps:
            skip.append("template-skill")

        return {
            "success": True,
            "recommendations": {
                "high_priority": high_priority,
                "medium_priority": medium_priority,
                "low_priority": low_priority,
                "skip": skip
            },
            "rationale": {
                "high_priority": "Directly relevant to development best practices",
                "medium_priority": "Useful for documentation, case-by-case adoption",
                "low_priority": "Creative/design skills, less relevant for dev toolkit",
                "skip": "Enterprise-specific or already have equivalent"
            },
            "suggested_actions": [
                f"Add {len(high_priority)} high-priority skills immediately",
                f"Evaluate {len(medium_priority)} medium-priority skills case-by-case",
                f"Consider {len(low_priority)} low-priority skills for specialized projects"
            ]
        }

    async def download_skill(self, skill_name: str, destination_path: str) -> Dict:
        """Download a skill from Anthropic's repository.

        Note: This is a template. Real implementation would use WebFetch
        to download the actual SKILL.md file from GitHub.
        """
        dest = Path(destination_path)
        dest.mkdir(parents=True, exist_ok=True)

        # Template for downloaded skill
        skill_template = f"""---
name: {skill_name}
description: Downloaded from Anthropic's skills repository
source: {ANTHROPIC_SKILLS_REPO}/tree/main/{skill_name}
downloaded: {datetime.now().isoformat()}
priority: toolkit
---

# {skill_name.replace('-', ' ').title()}

**Source**: Anthropic's Official Skills Repository

## Purpose
[Description from Anthropic repository]

## When to Use
[Use cases from Anthropic repository]

## Instructions
[Instructions from SKILL.md file]

## Resources
- Original: {ANTHROPIC_SKILLS_REPO}/tree/main/{skill_name}
- Last synced: {datetime.now().strftime('%Y-%m-%d')}

---

**Note**: Use WebFetch to download actual SKILL.md content from GitHub.
"""

        skill_file = dest / "skill.md"
        skill_file.write_text(skill_template)

        return {
            "success": True,
            "skill_name": skill_name,
            "destination": str(skill_file),
            "message": f"Skill template created at {skill_file}. Use WebFetch to download actual content.",
            "next_steps": [
                f"WebFetch: {ANTHROPIC_SKILLS_REPO}/blob/main/{skill_name}/SKILL.md",
                "Replace template with actual content",
                "Test skill in a project",
                "Update .claude/skills/README.md"
            ]
        }

    def store_learning(self, topic: str, learning_data: Dict) -> Dict:
        """Store discovered best practices."""
        try:
            # Create storage directory
            storage_dir = LEARNING_DIR / topic.lower()
            storage_dir.mkdir(parents=True, exist_ok=True)

            # Generate filename with timestamp
            timestamp = datetime.now().strftime("%Y-%m-%d_%H%M%S")
            subtopic = learning_data.get("subtopic", "general")
            filename = f"{timestamp}_{subtopic}.json"
            filepath = storage_dir / filename

            # Add metadata
            learning_data["stored_at"] = datetime.now().isoformat()
            learning_data["topic"] = topic

            # Store learning
            with open(filepath, 'w') as f:
                json.dump(learning_data, f, indent=2)

            return {
                "success": True,
                "topic": topic,
                "filepath": str(filepath),
                "message": f"Learning stored successfully"
            }
        except Exception as e:
            return {"success": False, "error": str(e)}

    def get_learnings(self, topic: Optional[str] = None, since: Optional[str] = None) -> Dict:
        """Retrieve stored learnings by topic or date."""
        try:
            learnings = []

            # Determine search path
            if topic:
                search_dir = LEARNING_DIR / topic.lower()
                if not search_dir.exists():
                    return {
                        "success": True,
                        "learnings": [],
                        "count": 0,
                        "message": f"No learnings found for topic: {topic}"
                    }
                search_dirs = [search_dir]
            else:
                search_dirs = [d for d in LEARNING_DIR.iterdir() if d.is_dir()]

            # Search for learning files
            for dir_path in search_dirs:
                for json_file in dir_path.glob("*.json"):
                    try:
                        with open(json_file, 'r') as f:
                            data = json.load(f)

                        # Filter by date if provided
                        if since:
                            stored_at = data.get("stored_at", "")
                            if stored_at < since:
                                continue

                        learnings.append({
                            "file": str(json_file),
                            "topic": data.get("topic"),
                            "subtopic": data.get("subtopic"),
                            "stored_at": data.get("stored_at"),
                            "confidence": data.get("confidence"),
                            "data": data
                        })
                    except:
                        continue

            # Sort by date (newest first)
            learnings.sort(key=lambda x: x.get("stored_at", ""), reverse=True)

            return {
                "success": True,
                "learnings": learnings,
                "count": len(learnings),
                "filtered_by": {
                    "topic": topic,
                    "since": since
                }
            }
        except Exception as e:
            return {"success": False, "error": str(e)}

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
    server = LearningServer()
    await server.run()


if __name__ == "__main__":
    asyncio.run(main())
