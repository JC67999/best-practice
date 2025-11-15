#!/usr/bin/env python3
"""
Learning MCP Server - Project-Objective-Driven Self-Learning System

PURPOSE:
Adapts to the objective of whatever project it's injected into and continuously
researches that project's specific domain to support achieving that objective.

EXAMPLES:
- In rapid-pm: Researches project management methodologies, PM tools, artifacts
- In ai-task-optimisation-MVP: Researches optimization algorithms, solver techniques
- In document-generator: Researches doc methodologies, exemplar templates, best practices
- In best-practice: Researches Claude Code best practices, MCP patterns, skills usage

The system is PROJECT-OBJECTIVE-AWARE: It becomes a domain expert for whatever
domain it's deployed in, building specialized knowledge that directly supports
that project's success. It's a domain-adaptive research engine that makes each
project smarter about its own domain over time.
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

# Anthropic Repositories
ANTHROPIC_SKILLS_REPO = "https://github.com/anthropics/skills"
ANTHROPIC_SKILLS_API = "https://api.github.com/repos/anthropics/skills/contents"
ANTHROPIC_COOKBOOKS_REPO = "https://github.com/anthropics/claude-cookbooks"
ANTHROPIC_QUICKSTARTS_REPO = "https://github.com/anthropics/claude-quickstarts"
ANTHROPIC_ORG_URL = "https://github.com/orgs/anthropics/repositories"


class LearningServer:
    """Learning server for continuous improvement."""

    def __init__(self):
        self.server = Server("learning-server")
        self.project_objective = None
        self.project_domain = None
        self.research_domains = []
        self.setup_handlers()

    def setup_handlers(self):
        """Setup MCP tool and prompt handlers."""

        @self.server.list_tools()
        async def list_tools() -> list[Tool]:
            return [
                Tool(
                    name="detect_project_objective",
                    description="Detect and load the project objective to determine research focus",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "project_path": {
                                "type": "string",
                                "description": "Path to project root directory"
                            }
                        },
                        "required": ["project_path"]
                    }
                ),
                Tool(
                    name="map_objective_to_domains",
                    description="Analyze project objective and map it to research domains and sources",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "objective_data": {
                                "type": "object",
                                "description": "Project objective data from detect_project_objective"
                            }
                        },
                        "required": ["objective_data"]
                    }
                ),
                Tool(
                    name="research_domain_topic",
                    description="Research a topic using domain-specific sources (not just Anthropic)",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "topic": {
                                "type": "string",
                                "description": "Topic to research (e.g., 'sprint planning', 'constraint solving')"
                            },
                            "domain": {
                                "type": "string",
                                "description": "Optional domain override (project_management, optimization, etc.)"
                            },
                            "project_path": {
                                "type": "string",
                                "description": "Optional project path to auto-detect domain"
                            }
                        },
                        "required": ["topic"]
                    }
                ),
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
                    description="Store discovered best practices to project-specific knowledge base",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "topic": {
                                "type": "string",
                                "description": "Topic or technology (sprint-planning, constraint-solving, etc.)"
                            },
                            "learning_data": {
                                "type": "object",
                                "description": "Dict with domain, overview, best_practices, anti_patterns, tools, sources, confidence, recommendations"
                            },
                            "project_path": {
                                "type": "string",
                                "description": "Project path to store in docs/references/domain-knowledge/ (recommended)"
                            }
                        },
                        "required": ["topic", "learning_data"]
                    }
                ),
                Tool(
                    name="get_learnings",
                    description="Retrieve stored learnings from project knowledge base or global storage",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "topic": {
                                "type": "string",
                                "description": "Topic to filter by (optional)"
                            },
                            "project_path": {
                                "type": "string",
                                "description": "Project path to read from docs/references/domain-knowledge/"
                            },
                            "domain": {
                                "type": "string",
                                "description": "Domain to filter by (project_management, optimization, etc.)"
                            },
                            "since": {
                                "type": "string",
                                "description": "Date filter YYYY-MM-DD (optional)"
                            }
                        }
                    }
                ),
                Tool(
                    name="scan_anthropic_cookbooks",
                    description="Scan Anthropic's claude-cookbooks repository for code examples and guides",
                    inputSchema={
                        "type": "object",
                        "properties": {},
                        "required": []
                    }
                ),
                Tool(
                    name="scan_anthropic_quickstarts",
                    description="Scan Anthropic's claude-quickstarts repository for starter projects",
                    inputSchema={
                        "type": "object",
                        "properties": {},
                        "required": []
                    }
                ),
                Tool(
                    name="scan_anthropic_org",
                    description="Scan all repositories in Anthropic's GitHub organization",
                    inputSchema={
                        "type": "object",
                        "properties": {},
                        "required": []
                    }
                )
            ]

        @self.server.call_tool()
        async def call_tool(name: str, arguments: dict) -> list[TextContent]:
            """Handle tool calls."""
            try:
                if name == "detect_project_objective":
                    result = self.detect_project_objective(**arguments)
                elif name == "map_objective_to_domains":
                    result = self.map_objective_to_domains(**arguments)
                elif name == "research_domain_topic":
                    result = self.research_domain_topic(**arguments)
                elif name == "scan_anthropic_skills":
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
                elif name == "scan_anthropic_cookbooks":
                    result = await self.scan_anthropic_cookbooks()
                elif name == "scan_anthropic_quickstarts":
                    result = await self.scan_anthropic_quickstarts()
                elif name == "scan_anthropic_org":
                    result = await self.scan_anthropic_org()
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
                ),
                Prompt(
                    name="scan_all_resources",
                    description="Comprehensive scan of all Anthropic resources (skills, cookbooks, quickstarts, org repos)",
                    arguments=[]
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

            elif name == "scan_all_resources":
                prompt_text = """You are scanning ALL Anthropic resources to build comprehensive knowledge.

## Comprehensive Resource Scan Workflow

### Step 1: Scan All Resource Types
Call each scanning tool to gather complete data:

1. **Skills**: Call `scan_anthropic_skills`
   - Returns 15 skills across 5 categories
   - Development, Meta, Documents, Creative, Enterprise

2. **Cookbooks**: Call `scan_anthropic_cookbooks`
   - Returns code examples and guides organized by category
   - Capabilities, Tool Use, Multimodal, Patterns, etc.

3. **Quickstarts**: Call `scan_anthropic_quickstarts`
   - Returns starter projects with technologies
   - Customer support, Financial analysis, Computer use demos

4. **Organization Repos**: Call `scan_anthropic_org`
   - Returns all 54 repositories
   - SDKs (7 languages), Agent frameworks, Security tools, Courses

### Step 2: Analyze Resource Coverage
Compare what we have vs what Anthropic provides:

**Skills Analysis**:
- Which skills should we add to toolkit?
- Which are universally useful vs domain-specific?

**Cookbooks Analysis**:
- Which cookbook patterns should become toolkit guidance?
- Which code examples should we reference?
- Are there missing capabilities we should document?

**Quickstarts Analysis**:
- Should we create slash commands based on quickstart patterns?
- Are there common project structures we should adopt?

**Org Repos Analysis**:
- Which SDKs should we document for MCP integration?
- Are there security tools we should integrate?
- Should we reference the courses for learning paths?

### Step 3: Identify Gaps and Opportunities

**Toolkit Enhancement Opportunities**:
- Skills to add (from skills repo)
- Patterns to document (from cookbooks)
- Project templates to create (from quickstarts)
- Tools to integrate (from org repos)

**Best Practices to Extract**:
- Common patterns across multiple resources
- Anthropic-recommended approaches
- Emerging capabilities (extended thinking, computer use, etc.)

### Step 4: Prioritize Actions

**HIGH Priority** (Add immediately):
- Universal skills (testing, MCP building)
- Critical patterns (RAG, tool use, agents)
- Essential SDKs (Python, TypeScript)

**MEDIUM Priority** (Evaluate case-by-case):
- Domain-specific skills
- Advanced patterns (sub-agents, prompt caching)
- Language-specific SDKs

**LOW Priority** (Document for reference):
- Creative/design tools
- Enterprise-specific resources
- Specialized repositories

### Step 5: Create Action Plan

Generate structured recommendations:

```markdown
## Comprehensive Anthropic Resource Scan

### Summary Statistics
- Skills: [count] across [categories]
- Cookbooks: [count] across [categories]
- Quickstarts: [count] projects
- Org Repos: [count] repositories

### Key Findings

**Skills Gap Analysis**:
- Missing: [list skills we should add]
- Have: [list skills we already have equivalent functionality]
- Unique to us: [list our exclusive skills]

**Cookbook Patterns to Adopt**:
1. [Pattern name] - [Why it matters]
2. [Pattern name] - [Why it matters]

**Quickstart Templates**:
1. [Template name] - [Use case]
2. [Template name] - [Use case]

**Recommended SDK Integrations**:
- [SDK name] - [Integration point]

### Recommended Actions (Priority Order)

**Immediate** (This sprint):
1. Add [N] high-priority skills
2. Document [N] critical patterns from cookbooks
3. Create [N] slash commands based on quickstarts

**Next Sprint**:
1. Integrate [tools] from org repos
2. Add [N] medium-priority skills
3. Create learning paths referencing courses

**Future Consideration**:
- [Low priority items]

### Implementation Tasks
- [ ] Download high-priority skills
- [ ] Extract and document cookbook patterns
- [ ] Create project templates from quickstarts
- [ ] Update skills README
- [ ] Update CHANGELOG
- [ ] Store learnings for each resource type
```

**Now begin the comprehensive scan.**
"""

                return GetPromptResult(
                    description="Comprehensive scan of all Anthropic resources",
                    messages=[
                        PromptMessage(
                            role="user",
                            content=TextContent(type="text", text=prompt_text)
                        )
                    ]
                )

            else:
                raise ValueError(f"Unknown prompt: {name}")

    def detect_project_objective(self, project_path: str) -> Dict:
        """Detect and load project objective from PROJECT_PLAN.md or Project MCP.

        Args:
            project_path: Absolute path to project root directory

        Returns:
            Dictionary with objective data including problem, users, solution, etc.
        """
        try:
            project_dir = Path(project_path)
            if not project_dir.exists():
                return {"error": f"Project path not found: {project_path}"}

            # Try to read from docs/notes/PROJECT_PLAN.md
            plan_file = project_dir / "docs" / "notes" / "PROJECT_PLAN.md"

            if not plan_file.exists():
                # Try alternative locations
                plan_file = project_dir / "docs" / "PROJECT_PLAN.md"
                if not plan_file.exists():
                    plan_file = project_dir / "PROJECT_PLAN.md"
                    if not plan_file.exists():
                        return {
                            "error": "PROJECT_PLAN.md not found",
                            "searched_paths": [
                                str(project_dir / "docs" / "notes" / "PROJECT_PLAN.md"),
                                str(project_dir / "docs" / "PROJECT_PLAN.md"),
                                str(project_dir / "PROJECT_PLAN.md")
                            ],
                            "suggestion": "Create PROJECT_PLAN.md or use Project MCP to define objective"
                        }

            # Read and parse PROJECT_PLAN.md
            content = plan_file.read_text()

            # Extract objective sections using regex
            objective_data = {
                "project_path": project_path,
                "project_name": project_dir.name,
                "plan_file": str(plan_file)
            }

            # Extract key sections
            sections = {
                "problem": r"##\s*(?:Problem|The Problem|Problem Statement)\s*\n(.*?)(?=\n##|\Z)",
                "target_users": r"##\s*(?:Target Users|Users|Who)\s*\n(.*?)(?=\n##|\Z)",
                "solution": r"##\s*(?:Solution|The Solution|Approach)\s*\n(.*?)(?=\n##|\Z)",
                "success": r"##\s*(?:Success|Definition of Success|Goals)\s*\n(.*?)(?=\n##|\Z)",
                "constraints": r"##\s*(?:Constraints|Limitations)\s*\n(.*?)(?=\n##|\Z)"
            }

            for key, pattern in sections.items():
                match = re.search(pattern, content, re.DOTALL | re.IGNORECASE)
                if match:
                    objective_data[key] = match.group(1).strip()

            # Try to extract project description from top of file
            desc_match = re.search(r"#\s*(.+?)\n", content)
            if desc_match:
                objective_data["title"] = desc_match.group(1).strip()

            # Store objective for future use
            self.project_objective = objective_data

            return {
                "success": True,
                "objective": objective_data,
                "message": f"Project objective loaded from {plan_file.name}",
                "next_step": "Call map_objective_to_domains to identify research areas"
            }

        except Exception as e:
            return {"error": f"Failed to detect objective: {str(e)}"}

    def map_objective_to_domains(self, objective_data: Dict) -> Dict:
        """Map project objective to research domains and sources.

        Args:
            objective_data: Output from detect_project_objective

        Returns:
            Dictionary with research domains, keywords, and recommended sources
        """
        try:
            if "error" in objective_data:
                return objective_data

            objective = objective_data.get("objective", {})
            project_name = objective.get("project_name", "").lower()
            problem = objective.get("problem", "").lower()
            solution = objective.get("solution", "").lower()
            title = objective.get("title", "").lower()

            # Combine all text for analysis
            combined_text = f"{project_name} {title} {problem} {solution}"

            # Domain detection patterns
            domain_patterns = {
                "project_management": {
                    "keywords": ["project management", "pm", "agile", "scrum", "kanban", "sprint", "backlog", "jira", "roadmap"],
                    "sources": [
                        "https://www.pmi.org/",
                        "https://www.scrum.org/",
                        "https://www.atlassian.com/agile",
                        "https://asana.com/resources/project-management",
                        "https://www.scrumalliance.org/"
                    ],
                    "search_terms": ["project management best practices", "agile methodologies", "PM tools comparison", "sprint planning techniques"]
                },
                "optimization": {
                    "keywords": ["optimization", "optimize", "performance", "efficiency", "solver", "algorithm", "constraint", "minimize", "maximize"],
                    "sources": [
                        "https://optimization.cbe.cornell.edu/",
                        "https://neos-guide.org/",
                        "https://scipbook.readthedocs.io/",
                        "https://docs.scipy.org/doc/scipy/reference/optimize.html",
                        "https://or.stackexchange.com/"
                    ],
                    "search_terms": ["optimization algorithms", "solver techniques", "constraint programming", "linear programming best practices"]
                },
                "documentation": {
                    "keywords": ["documentation", "docs", "document", "technical writing", "readme", "api docs", "template", "markdown"],
                    "sources": [
                        "https://www.writethedocs.org/",
                        "https://developers.google.com/tech-writing",
                        "https://documentation.divio.com/",
                        "https://github.com/github/docs",
                        "https://www.markdownguide.org/"
                    ],
                    "search_terms": ["technical documentation best practices", "API documentation templates", "documentation methodologies", "README examples"]
                },
                "claude_development": {
                    "keywords": ["claude", "mcp", "skill", "anthropic", "ai assistant", "prompt", "best practice"],
                    "sources": [
                        "https://docs.anthropic.com/",
                        "https://github.com/anthropics/",
                        "https://modelcontextprotocol.io/",
                        "https://code.claude.com/docs",
                        "https://github.com/anthropics/skills"
                    ],
                    "search_terms": ["Claude Code best practices", "MCP server development", "Claude skills creation", "Anthropic API usage"]
                },
                "web_development": {
                    "keywords": ["web", "frontend", "backend", "api", "react", "node", "javascript", "typescript", "html", "css"],
                    "sources": [
                        "https://developer.mozilla.org/",
                        "https://web.dev/",
                        "https://react.dev/",
                        "https://nodejs.org/docs/",
                        "https://github.com/airbnb/javascript"
                    ],
                    "search_terms": ["web development best practices", "React patterns", "API design", "frontend performance"]
                },
                "data_science": {
                    "keywords": ["data", "analysis", "machine learning", "ml", "ai", "model", "training", "dataset", "pandas", "numpy"],
                    "sources": [
                        "https://scikit-learn.org/",
                        "https://www.kaggle.com/",
                        "https://pytorch.org/docs/",
                        "https://www.tensorflow.org/",
                        "https://pandas.pydata.org/"
                    ],
                    "search_terms": ["data science best practices", "ML model training", "data analysis techniques", "feature engineering"]
                }
            }

            # Detect which domains match
            detected_domains = []
            for domain, config in domain_patterns.items():
                # Count keyword matches
                matches = sum(1 for keyword in config["keywords"] if keyword in combined_text)
                if matches > 0:
                    detected_domains.append({
                        "domain": domain,
                        "match_score": matches,
                        "sources": config["sources"],
                        "search_terms": config["search_terms"],
                        "keywords_matched": [kw for kw in config["keywords"] if kw in combined_text]
                    })

            # Sort by match score
            detected_domains.sort(key=lambda x: x["match_score"], reverse=True)

            # Store for future use
            if detected_domains:
                self.project_domain = detected_domains[0]["domain"]
                self.research_domains = [d["domain"] for d in detected_domains[:3]]  # Top 3

            return {
                "success": True,
                "project_name": objective.get("project_name"),
                "detected_domains": detected_domains,
                "primary_domain": detected_domains[0]["domain"] if detected_domains else "general",
                "recommended_sources": detected_domains[0]["sources"] if detected_domains else [],
                "search_terms": detected_domains[0]["search_terms"] if detected_domains else [],
                "message": f"Detected {len(detected_domains)} relevant research domain(s)",
                "next_step": "Use search_terms with WebSearch to find domain-specific resources"
            }

        except Exception as e:
            return {"error": f"Failed to map domains: {str(e)}"}

    def research_domain_topic(self, topic: str, domain: Optional[str] = None, project_path: Optional[str] = None) -> Dict:
        """Research a topic using domain-specific sources (not just Anthropic).

        Args:
            topic: Topic to research (e.g., 'sprint planning', 'optimization algorithms')
            domain: Optional domain override (project_management, optimization, etc.)
            project_path: Optional project path to auto-detect domain

        Returns:
            Dictionary with domain-specific search queries, sources, and research guidance
        """
        try:
            # Determine which domain to use
            target_domain = domain

            if not target_domain and project_path:
                # Auto-detect domain from project
                obj_result = self.detect_project_objective(project_path)
                if "objective" in obj_result:
                    domain_result = self.map_objective_to_domains(obj_result)
                    if "primary_domain" in domain_result:
                        target_domain = domain_result["primary_domain"]

            if not target_domain and self.project_domain:
                # Use stored domain
                target_domain = self.project_domain

            if not target_domain:
                target_domain = "general"

            # Domain-specific research patterns
            domain_configs = {
                "project_management": {
                    "sources": [
                        "https://www.pmi.org/",
                        "https://www.scrum.org/",
                        "https://www.atlassian.com/agile",
                        "https://asana.com/resources/",
                        "https://www.scrumalliance.org/"
                    ],
                    "search_template": [
                        f"{topic} project management best practices",
                        f"{topic} agile methodology",
                        f"{topic} scrum guide",
                        f"how to {topic} in software projects"
                    ]
                },
                "optimization": {
                    "sources": [
                        "https://optimization.cbe.cornell.edu/",
                        "https://neos-guide.org/",
                        "https://scipbook.readthedocs.io/",
                        "https://docs.scipy.org/doc/scipy/reference/optimize.html",
                        "https://or.stackexchange.com/"
                    ],
                    "search_template": [
                        f"{topic} optimization algorithms",
                        f"{topic} mathematical programming",
                        f"{topic} solver techniques",
                        f"{topic} constraint satisfaction"
                    ]
                },
                "documentation": {
                    "sources": [
                        "https://www.writethedocs.org/",
                        "https://developers.google.com/tech-writing",
                        "https://documentation.divio.com/",
                        "https://github.com/github/docs",
                        "https://www.markdownguide.org/"
                    ],
                    "search_template": [
                        f"{topic} technical documentation best practices",
                        f"{topic} documentation templates",
                        f"{topic} technical writing guide",
                        f"examples of {topic} documentation"
                    ]
                },
                "claude_development": {
                    "sources": [
                        "https://docs.anthropic.com/",
                        "https://github.com/anthropics/",
                        "https://modelcontextprotocol.io/",
                        "https://code.claude.com/docs",
                        "https://github.com/anthropics/skills"
                    ],
                    "search_template": [
                        f"{topic} Claude Code best practices",
                        f"{topic} MCP server development",
                        f"{topic} Anthropic API",
                        f"{topic} Claude skills"
                    ]
                },
                "web_development": {
                    "sources": [
                        "https://developer.mozilla.org/",
                        "https://web.dev/",
                        "https://react.dev/",
                        "https://nodejs.org/docs/",
                        "https://github.com/airbnb/javascript"
                    ],
                    "search_template": [
                        f"{topic} web development best practices 2025",
                        f"{topic} React patterns",
                        f"{topic} frontend architecture",
                        f"{topic} JavaScript guide"
                    ]
                },
                "data_science": {
                    "sources": [
                        "https://scikit-learn.org/",
                        "https://www.kaggle.com/",
                        "https://pytorch.org/docs/",
                        "https://pandas.pydata.org/",
                        "https://github.com/google/jax"
                    ],
                    "search_template": [
                        f"{topic} machine learning best practices",
                        f"{topic} data science guide",
                        f"{topic} ML techniques",
                        f"{topic} feature engineering"
                    ]
                },
                "general": {
                    "sources": [],
                    "search_template": [
                        f"{topic} best practices 2025",
                        f"{topic} tutorial",
                        f"{topic} comprehensive guide",
                        f"{topic} examples and patterns"
                    ]
                }
            }

            config = domain_configs.get(target_domain, domain_configs["general"])

            return {
                "success": True,
                "topic": topic,
                "domain": target_domain,
                "search_queries": config["search_template"],
                "recommended_sources": config["sources"],
                "research_workflow": {
                    "step_1": f"Use WebSearch with queries: {config['search_template']}",
                    "step_2": f"Use WebFetch on top results from these sources: {', '.join(config['sources'][:3])}",
                    "step_3": f"Extract key patterns, techniques, and best practices for {topic}",
                    "step_4": f"Store learnings using store_learning tool",
                    "step_5": f"Save to project-specific docs/references/domain-knowledge/{target_domain}/"
                },
                "example_workflow": f"""
# Research Workflow for: {topic}

## 1. Web Search (Domain: {target_domain})
Use WebSearch tool with these queries:
{chr(10).join('- ' + q for q in config['search_template'])}

## 2. Fetch Top Resources
Use WebFetch on results from:
{chr(10).join('- ' + s for s in config['sources'][:5])}

## 3. Extract Learnings
Focus on:
- Best practices and patterns
- Common pitfalls and anti-patterns
- Tool recommendations
- Code/configuration examples
- Performance considerations

## 4. Store Results
Call store_learning with structured data:
- Topic: "{topic}"
- Domain: "{target_domain}"
- Sources: [URLs from WebFetch]
- Confidence: high/medium/low
- Recommendations: What to apply to project
                """,
                "storage_path": f"docs/references/domain-knowledge/{target_domain}/{topic.replace(' ', '-').lower()}.md",
                "message": f"Research plan generated for '{topic}' in {target_domain} domain"
            }

        except Exception as e:
            return {"error": f"Failed to generate research plan: {str(e)}"}

    async def scan_anthropic_skills(self) -> Dict:
        """Scan Anthropic's skills repository for available skills.

        Returns instructions for using WebFetch to get real-time data.
        """
        return {
            "success": True,
            "repository": ANTHROPIC_SKILLS_REPO,
            "method": "dynamic",
            "instructions": {
                "step_1": "Use WebFetch to scan the skills repository",
                "step_2": "Parse the repository structure",
                "step_3": "Categorize skills by domain",
                "step_4": "Compare with project domain to find relevant skills"
            },
            "webfetch_urls": [
                f"{ANTHROPIC_SKILLS_API}",  # Lists all skills
                f"{ANTHROPIC_SKILLS_REPO}"   # Repository overview
            ],
            "workflow": """
# Dynamic Skills Scanning Workflow

## 1. Fetch Repository Index
WebFetch: https://api.github.com/repos/anthropics/skills/contents
This returns JSON with all skill folders.

## 2. For Each Skill
WebFetch: https://raw.githubusercontent.com/anthropics/skills/main/{skill-name}/SKILL.md
Extract name, description, category from SKILL.md front matter.

## 3. Filter by Project Domain
If project domain is 'optimization', prioritize development/technical skills.
If project domain is 'project_management', consider all skill types.

## 4. Return Categorized Results
Group skills by relevance to current project objective.
            """,
            "message": "Use WebFetch with the URLs above to get real-time skills data",
            "fallback_categories": ["development", "meta", "documents", "creative", "enterprise"],
            "note": "This replaces hardcoded data with dynamic fetching"
        }


    def compare_skills(self, toolkit_skills_path: str) -> Dict:
        """Compare Anthropic skills with our toolkit skills.

        Returns instructions to use WebFetch for real-time comparison.
        """
        toolkit_path = Path(toolkit_skills_path)

        if not toolkit_path.exists():
            return {"error": f"Toolkit skills path not found: {toolkit_skills_path}"}

        # Get our toolkit skills
        our_skills = []
        for skill_dir in toolkit_path.iterdir():
            if skill_dir.is_dir() and skill_dir.name != "template":
                our_skills.append(skill_dir.name)

        return {
            "success": True,
            "method": "dynamic_comparison",
            "toolkit_skills": our_skills,
            "toolkit_skill_count": len(our_skills),
            "instructions": {
                "step_1": "Call scan_anthropic_skills to get WebFetch instructions",
                "step_2": "Use WebFetch to get real-time Anthropic skills list",
                "step_3": "Compare with our toolkit skills",
                "step_4": "Filter by project domain relevance"
            },
            "workflow": f"""
# Dynamic Skills Comparison

## 1. Get Anthropic Skills (Real-time)
Call scan_anthropic_skills, then use returned WebFetch URLs.

## 2. Our Toolkit Skills
We have {len(our_skills)} skills:
{chr(10).join('- ' + s for s in our_skills)}

## 3. Compare and Filter
- Find skills they have that we don't
- Filter by project domain (use map_objective_to_domains)
- Prioritize skills relevant to this project's objective

## 4. Recommend Additions
- HIGH priority: Skills matching project domain
- MEDIUM priority: Universal development skills
- LOW priority: Domain-specific but not matching project
- SKIP: Enterprise-specific, already have equivalent
            """,
            "note": "Use WebFetch for real-time Anthropic data instead of hardcoded lists"
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

    def store_learning(self, topic: str, learning_data: Dict, project_path: Optional[str] = None) -> Dict:
        """Store discovered best practices to project-specific location.

        Args:
            topic: Topic name (e.g., "optimization", "project-management")
            learning_data: Dictionary with learnings, sources, confidence, recommendations
            project_path: Optional project path. If provided, stores in project's docs/references/

        Returns:
            Dictionary with success status and file path
        """
        try:
            # Determine storage location
            if project_path:
                # Project-specific storage: {project}/docs/references/domain-knowledge/{domain}/
                project_dir = Path(project_path)
                domain = learning_data.get("domain", self.project_domain or "general")
                storage_dir = project_dir / "docs" / "references" / "domain-knowledge" / domain
                storage_dir.mkdir(parents=True, exist_ok=True)

                # Create markdown file (more readable than JSON)
                filename = f"{topic.replace(' ', '-').lower()}.md"
                filepath = storage_dir / filename

                # Format as markdown
                md_content = f"""# {topic}

**Domain**: {domain}
**Last Updated**: {datetime.now().strftime('%Y-%m-%d')}
**Confidence**: {learning_data.get('confidence', 'medium')}

## Overview

{learning_data.get('overview', 'Research findings for ' + topic)}

## Key Findings

{chr(10).join('- ' + str(p) for p in learning_data.get('principles', learning_data.get('best_practices', [])))}

## Best Practices

{chr(10).join('- ' + str(bp) for bp in learning_data.get('best_practices', []))}

## Anti-Patterns / Pitfalls

{chr(10).join('- ' + str(ap) for ap in learning_data.get('anti_patterns', []))}

## Tools & Resources

{chr(10).join('- ' + str(t) for t in learning_data.get('tools', []))}

## Sources

{chr(10).join('- ' + str(s) for s in learning_data.get('sources', []))}

## Recommendations

{learning_data.get('recommendations', 'Apply findings to project implementation.')}

---

*Researched for project: {Path(project_path).name if project_path else 'general'}*
*Stored at: {datetime.now().isoformat()}*
"""

                with open(filepath, 'w') as f:
                    f.write(md_content)

                storage_type = "project-specific"

            else:
                # Fallback to global storage
                storage_dir = LEARNING_DIR / topic.lower()
                storage_dir.mkdir(parents=True, exist_ok=True)

                timestamp = datetime.now().strftime("%Y-%m-%d_%H%M%S")
                subtopic = learning_data.get("subtopic", "general")
                filename = f"{timestamp}_{subtopic}.json"
                filepath = storage_dir / filename

                learning_data["stored_at"] = datetime.now().isoformat()
                learning_data["topic"] = topic

                with open(filepath, 'w') as f:
                    json.dump(learning_data, f, indent=2)

                storage_type = "global"

            return {
                "success": True,
                "topic": topic,
                "filepath": str(filepath),
                "storage_type": storage_type,
                "message": f"Learning stored successfully to {storage_type} location",
                "note": "Knowledge is now part of project repository" if project_path else "Use project_path parameter to store in project"
            }
        except Exception as e:
            return {"success": False, "error": str(e)}

    def get_learnings(
        self,
        topic: Optional[str] = None,
        project_path: Optional[str] = None,
        domain: Optional[str] = None,
        since: Optional[str] = None
    ) -> Dict:
        """Retrieve stored learnings from project-specific or global storage.

        Args:
            topic: Topic to filter by
            project_path: Project path to read from docs/references/domain-knowledge/
            domain: Domain to filter by (project_management, optimization, etc.)
            since: Date filter YYYY-MM-DD

        Returns:
            Dictionary with learnings list and metadata
        """
        try:
            learnings = []

            # Determine search location
            if project_path:
                # Project-specific storage
                project_dir = Path(project_path)
                knowledge_base = project_dir / "docs" / "references" / "domain-knowledge"

                if not knowledge_base.exists():
                    return {
                        "success": True,
                        "learnings": [],
                        "count": 0,
                        "storage_type": "project-specific",
                        "message": f"No knowledge base found at {knowledge_base}",
                        "suggestion": "Use store_learning with project_path to create knowledge base"
                    }

                # Search in domain folders
                if domain:
                    search_dirs = [knowledge_base / domain]
                else:
                    search_dirs = [d for d in knowledge_base.iterdir() if d.is_dir()]

                # Search for markdown files
                for dir_path in search_dirs:
                    if not dir_path.exists():
                        continue

                    for md_file in dir_path.glob("*.md"):
                        try:
                            content = md_file.read_text()

                            # Parse markdown metadata
                            if topic and topic.lower() not in md_file.stem.lower():
                                continue

                            # Extract date from content if since filter provided
                            if since:
                                date_match = re.search(r"\*\*Last Updated\*\*: (\d{4}-\d{2}-\d{2})", content)
                                if date_match and date_match.group(1) < since:
                                    continue

                            learnings.append({
                                "file": str(md_file),
                                "topic": md_file.stem.replace('-', ' '),
                                "domain": dir_path.name,
                                "format": "markdown",
                                "preview": content[:500] + "..." if len(content) > 500 else content
                            })
                        except:
                            continue

                storage_type = "project-specific"

            else:
                # Global storage (fallback)
                if topic:
                    search_dir = LEARNING_DIR / topic.lower()
                    if not search_dir.exists():
                        return {
                            "success": True,
                            "learnings": [],
                            "count": 0,
                            "storage_type": "global",
                            "message": f"No learnings found for topic: {topic}"
                        }
                    search_dirs = [search_dir]
                else:
                    search_dirs = [d for d in LEARNING_DIR.iterdir() if d.is_dir()]

                # Search for JSON files (global format)
                for dir_path in search_dirs:
                    for json_file in dir_path.glob("*.json"):
                        try:
                            with open(json_file, 'r') as f:
                                data = json.load(f)

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
                                "format": "json",
                                "data": data
                            })
                        except:
                            continue

                storage_type = "global"

            # Sort by filename (newest typically last)
            learnings.sort(key=lambda x: x.get("file", ""), reverse=True)

            return {
                "success": True,
                "learnings": learnings,
                "count": len(learnings),
                "storage_type": storage_type,
                "filtered_by": {
                    "topic": topic,
                    "domain": domain,
                    "project_path": project_path,
                    "since": since
                },
                "note": "Use project_path to read project-specific knowledge base" if not project_path else None
            }
        except Exception as e:
            return {"success": False, "error": str(e)}

    async def scan_anthropic_cookbooks(self) -> Dict:
        """Scan Anthropic's claude-cookbooks repository.

        Returns WebFetch instructions for real-time cookbook discovery.
        """
        return {
            "success": True,
            "repository": ANTHROPIC_COOKBOOKS_REPO,
            "method": "dynamic",
            "webfetch_urls": [
                "https://api.github.com/repos/anthropics/claude-cookbooks/contents",
                f"{ANTHROPIC_COOKBOOKS_REPO}/blob/main/README.md"
            ],
            "workflow": """
# Dynamic Cookbooks Scanning

## 1. Fetch Repository Structure
WebFetch: https://api.github.com/repos/anthropics/claude-cookbooks/contents
Returns all folders (capabilities, tool_use, multimodal, etc.)

## 2. Fetch README for Overview
WebFetch: https://github.com/anthropics/claude-cookbooks/blob/main/README.md
Extract categories and cookbook descriptions.

## 3. Filter by Project Domain
- If domain=optimization: Focus on patterns, automated_evaluation
- If domain=documentation: Focus on summarization, pdf_upload
- If domain=claude_development: All categories relevant

## 4. Return Domain-Relevant Cookbooks
Prioritize cookbooks that support project objective.
            """,
            "domain_relevance": {
                "optimization": ["patterns", "automated_evaluation"],
                "documentation": ["summarization", "pdf_upload_summarization"],
                "claude_development": ["all"],
                "project_management": ["tool_use", "retrieval_augmented_generation"],
                "web_development": ["tool_use", "third_party"],
                "data_science": ["multimodal", "retrieval_augmented_generation"]
            },
            "message": "Use WebFetch to get real-time cookbooks data filtered by project domain"
        }

    async def scan_anthropic_quickstarts(self) -> Dict:
        """Scan Anthropic's claude-quickstarts repository.

        Returns WebFetch instructions for real-time quickstart discovery.
        """
        return {
            "success": True,
            "repository": ANTHROPIC_QUICKSTARTS_REPO,
            "method": "dynamic",
            "webfetch_urls": [
                "https://api.github.com/repos/anthropics/claude-quickstarts/contents",
                f"{ANTHROPIC_QUICKSTARTS_REPO}/blob/main/README.md"
            ],
            "workflow": """
# Dynamic Quickstarts Scanning

## 1. Fetch Repository
WebFetch: https://api.github.com/repos/anthropics/claude-quickstarts/contents
Lists all quickstart project folders.

## 2. Filter by Project Domain
- If domain=optimization: Look for data-analyst, algorithm patterns
- If domain=web_development: Look for web-based quickstarts
- If domain=claude_development: All quickstarts relevant

## 3. Identify Reusable Patterns
Extract project structures, build configs, deployment patterns.

## 4. Suggest Project Templates
Recommend quickstarts that match project type and domain.
            """,
            "message": "Use WebFetch to get real-time quickstarts filtered by domain"
        }

    async def scan_anthropic_org(self) -> Dict:
        """Scan all repositories in Anthropic's GitHub organization.

        Returns WebFetch instructions for real-time organization scan.
        """
        return {
            "success": True,
            "organization": "anthropics",
            "org_url": ANTHROPIC_ORG_URL,
            "method": "dynamic",
            "webfetch_urls": [
                "https://api.github.com/orgs/anthropics/repos?per_page=100",
                "https://github.com/orgs/anthropics/repositories"
            ],
            "workflow": """
# Dynamic Organization Scanning

## 1. Fetch All Repositories
WebFetch: https://api.github.com/orgs/anthropics/repos?per_page=100
Returns JSON with all repos, stars, languages, descriptions.

## 2. Categorize Repositories
- SDKs: anthropic-sdk-*
- Agent Frameworks: claude-agent-*, claude-code
- Developer Resources: cookbooks, courses, quickstarts, skills
- Security Tools: *-action, *-security-*
- Domain-Specific: Based on description/README

## 3. Filter by Project Needs
- If domain=claude_development: Prioritize ALL repos
- If domain=web_development: Focus on TypeScript/JavaScript SDKs
- If domain=data_science: Focus on Python SDK, notebooks
- If domain=optimization: Focus on agent frameworks, patterns

## 4. Identify Integration Opportunities
- Which SDK to use for project language
- Which agent patterns to adopt
- Which security tools to integrate
- Which courses to reference for learning
            """,
            "domain_priority": {
                "claude_development": "all repos",
                "web_development": ["anthropic-sdk-typescript", "claude-cookbooks"],
                "data_science": ["anthropic-sdk-python", "courses"],
                "optimization": ["claude-agent-sdk-python", "claude-cookbooks"],
                "project_management": ["claude-agent-sdk-python"],
                "documentation": ["courses", "claude-cookbooks"]
            },
            "message": "Use WebFetch to get real-time org repos filtered by project domain"
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
    server = LearningServer()
    await server.run()


if __name__ == "__main__":
    asyncio.run(main())
