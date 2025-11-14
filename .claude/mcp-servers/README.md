# MCP Servers - Installation and Configuration Guide

> **Complete MCP setup for objective-driven development with best practices**
> **Version**: 1.0
> **Date**: 2025-10-29

---

## Overview

Four production-ready MCP servers that enforce excellent coding practices:

1. **Memory MCP** - Persistent context across sessions
2. **Quality MCP** - Automated quality enforcement
3. **Project MCP** - Objective-driven task management
4. **Learning MCP** - Self-learning from Anthropic resources (scans GitHub for latest best practices)

---

## Quick Start (5 Minutes)

```bash
# 1. Install MCP SDK
pip install mcp

# 2. Copy MCPs to home directory
mkdir -p ~/.mcp-servers
cp memory_mcp.py ~/.mcp-servers/
cp quality_mcp.py ~/.mcp-servers/
cp project_mcp.py ~/.mcp-servers/
cp learning_mcp.py ~/.mcp-servers/

# 3. Make executable
chmod +x ~/.mcp-servers/*.py

# 4. Configure Claude Code (see below)

# 5. Test
python ~/.mcp-servers/memory_mcp.py --test
```

---

## Installation

### Prerequisites

```bash
# Python 3.10+
python --version

# Install MCP SDK
pip install mcp

# Verify installation
python -c "import mcp; print('MCP SDK installed')"
```

### Install MCPs

```bash
# Create MCP directory
mkdir -p ~/.mcp-servers

# Copy server files
cp memory_mcp.py ~/.mcp-servers/
cp quality_mcp.py ~/.mcp-servers/
cp project_mcp.py ~/.mcp-servers/
cp learning_mcp.py ~/.mcp-servers/

# Make executable
chmod +x ~/.mcp-servers/*.py

# Verify
ls -la ~/.mcp-servers/
```

---

## Configuration

### Claude Desktop Configuration

**Location**:
- macOS: `~/.config/claude/claude_desktop_config.json`
- Windows: `%APPDATA%\Claude\claude_desktop_config.json`
- Linux: `~/.config/claude/claude_desktop_config.json`

**Configuration JSON**:

```json
{
  "mcpServers": {
    "memory": {
      "command": "python3",
      "args": [
        "/Users/YOUR_USERNAME/.mcp-servers/memory_mcp.py"
      ],
      "disabled": false
    },
    "quality": {
      "command": "python3",
      "args": [
        "/Users/YOUR_USERNAME/.mcp-servers/quality_mcp.py"
      ],
      "disabled": false
    },
    "project": {
      "command": "python3",
      "args": [
        "/Users/YOUR_USERNAME/.mcp-servers/project_mcp.py"
      ],
      "disabled": false
    },
    "learning": {
      "command": "python3",
      "args": [
        "/Users/YOUR_USERNAME/.mcp-servers/learning_mcp.py"
      ],
      "disabled": false
    }
  }
}
```

**Important**: Replace `/Users/YOUR_USERNAME/` with your actual home directory path.

### Find Your Home Directory

```bash
# Linux/macOS
echo $HOME

# Windows
echo %USERPROFILE%
```

---

## Testing

### Test Each MCP

```bash
# Test Memory MCP
python ~/.mcp-servers/memory_mcp.py

# Test Quality MCP
python ~/.mcp-servers/quality_mcp.py

# Test Project MCP
python ~/.mcp-servers/project_mcp.py
```

### Test in Claude Code

1. Open Claude Code
2. Start new chat
3. Type: `List available MCP tools`
4. You should see tools from all three MCPs

---

## Usage Guide

### Memory MCP

**Purpose**: Remember project context across sessions

**Key Tools**:
- `save_session_summary` - Save what you did in this session
- `load_project_context` - Load project history and objective
- `save_decision` - Record architectural decisions
- `list_projects` - See all tracked projects
- `search_memory` - Search across all projects

**Example**:
```
# At end of session
"Save session summary: Implemented user authentication,
decided to use JWT tokens, next steps: add password reset"

# Start of new session
"Load project context for current project"
```

### Quality MCP

**Purpose**: Enforce code quality automatically

**Key Tools**:
- `run_quality_gate` - MANDATORY before task completion
- `check_code_quality` - Check specific files
- `audit_project_structure` - Validate minimal root compliance
- `validate_file_placement` - Check files are in correct locations
- `find_obsolete_files` - Detect unused code
- `verify_standards` - Comprehensive quality check

**Example**:
```
# Before marking task complete
"Run quality gate for this project"

# Check specific files
"Check code quality for src/auth.py and src/models.py"

# Audit structure
"Audit project structure for minimal root compliance"
```

### Project MCP

**Purpose**: Objective-driven task management

**Key Tools**:
- `clarify_project_objective` - START HERE (comprehensive interrogation)
- `score_objective_clarity` - Check if objective is clear enough
- `validate_task_alignment` - Check if task serves objective
- `challenge_task_priority` - Is this highest priority?
- `mark_task_complete` - Complete task (requires quality gate PASS)
- `identify_scope_creep` - Find non-essential tasks
- `get_current_status` - See project status with objective

**Example**:
```
# Start new project
"Clarify project objective: I want to build a task manager"
[MCP asks 10-15 comprehensive questions]
[Answer each question]
[Objective defined with score >80]

# Start work
"Create task breakdown from objective"
"Validate task alignment: Implement user profiles"
"Challenge task priority for task_3"

# Complete task
"Mark task_1 complete (quality gate passed: true)"
```

### Learning MCP

**Purpose**: Self-learning system that keeps toolkit up-to-date with latest Anthropic best practices

**Key Tools**:
- `scan_anthropic_skills` - Scan official skills repository (15 skills)
- `scan_anthropic_cookbooks` - Scan cookbooks (28 cookbooks, 27.6k stars)
- `scan_anthropic_quickstarts` - Scan quickstarts (4 projects, 10.2k stars)
- `scan_anthropic_org` - Scan all 54 Anthropic repositories
- `compare_skills` - Compare Anthropic vs toolkit skills
- `suggest_skill_updates` - Prioritize updates (HIGH/MEDIUM/LOW/SKIP)
- `download_skill` - Download skills from GitHub
- `store_learning` - Store best practices in JSON
- `get_learnings` - Retrieve learnings by topic/date

**Key Prompts**:
- `update_toolkit` - Complete workflow: scan → compare → suggest → download
- `research_topic` - Research best practices for specific topic
- `scan_all_resources` - Comprehensive scan of ALL Anthropic resources

**Example**:
```
# Update toolkit with latest Anthropic skills
"Use the update_toolkit prompt to scan for new skills"

# Research specific topic
"Use research_topic prompt for 'prompt engineering'"

# Scan all resources
"Use scan_all_resources prompt"

# Manual workflow
"Scan Anthropic skills repository"
"Compare with toolkit skills at .claude/skills"
"Suggest skill updates based on comparison"
"Download skill: mcp-builder to .claude/skills/"
```

**Automation**:
```bash
# Set up daily auto-updates (2 AM)
cd /path/to/toolkit/.claude/mcp-servers
./auto_update_toolkit.sh --setup

# Check status
./auto_update_toolkit.sh --status

# Manual scan
./auto_update_toolkit.sh
```

**Storage**: `~/.claude_memory/learnings/`
- `anthropic_skills.json` - Scanned skills catalog
- `anthropic_cookbooks.json` - Cookbooks catalog
- `best_practices.json` - Stored learnings by topic

**Benefits**:
- ✅ Toolkit stays current with Anthropic's latest practices
- ✅ Automatic gap detection between toolkit and official skills
- ✅ Access to 27.6k+ stars of cookbook examples
- ✅ Structured learning storage for research
- ✅ Scheduled automation for hands-off updates

---

## MCP Prompts - Reusable Workflow Templates

> **NEW**: MCP Prompts provide structured, context-aware workflows for common tasks

### What Are MCP Prompts?

MCP Prompts are **reusable templates** that provide Claude with structured instructions for complex workflows. Unlike tools (which perform actions), prompts guide Claude through systematic processes while automatically loading relevant project context.

**Benefits**:
- 🎯 **Structured workflows** - Ensure thorough, systematic execution
- 📊 **Context-aware** - Automatically load project objective, status, decisions
- ♻️ **Reusable** - Same prompt works across all projects
- 🔗 **Tool integration** - Prompts reference MCP tools to call
- 📝 **Templated** - Consistent format and quality every time

### Available Prompts (10 Total)

#### Project Management Prompts (4)

**1. `plan_feature`** - Break down feature into small tasks
```
Usage: /mcp__project__plan_feature
Arguments:
  - feature: "user authentication"
  - project_path: "/path/to/project"

What it does:
- Loads project objective for alignment checking
- Breaks feature into tasks ≤30 lines, ≤15 min each
- Validates each task with MCP tools
- Identifies risks and edge cases
- Provides execution order with dependencies
```

**2. `daily_standup`** - Review project status and identify blockers
```
Usage: /mcp__project__daily_standup
Arguments:
  - project_path: "/path/to/project"

What it does:
- Loads current task status (completed, in progress, pending)
- Reviews recent completions
- Identifies blockers and risks
- Checks if tasks align with objective
- Suggests next steps and priorities
```

**3. `refocus`** - Cut non-essential work and realign with objective
```
Usage: /mcp__project__refocus
Arguments:
  - project_path: "/path/to/project"

What it does:
- Loads objective and all tasks
- Identifies scope creep (non-essential tasks)
- Reviews each task against objective
- Recommends what to cut, keep, or refine
- Calls refocus_on_objective to reorder tasks
```

**4. `task_breakdown`** - Break large task into smaller sub-tasks
```
Usage: /mcp__project__task_breakdown
Arguments:
  - task_description: "Implement payment processing"
  - project_path: "/path/to/project"

What it does:
- Validates if task is too large
- Breaks down by logical steps, components, layers
- Ensures each sub-task ≤30 lines
- Validates alignment and size for each sub-task
- Provides execution order
```

#### Quality Assurance Prompts (3)

**5. `code_review`** - Systematic code review for quality and security
```
Usage: /mcp__quality__code_review
Arguments:
  - file_paths: "src/auth.py,src/models.py"
  - project_path: "/path/to/project"

What it does:
- Runs automated quality checks first
- Reviews structure, naming, documentation
- Checks error handling and security (OWASP Top 10)
- Evaluates performance and testing
- Provides actionable feedback with line numbers
```

**6. `pre_commit_check`** - Run all quality checks before committing
```
Usage: /mcp__quality__pre_commit_check
Arguments:
  - project_path: "/path/to/project"
  - changed_files: "src/auth.py,tests/test_auth.py"

What it does:
- Calls run_quality_gate (MANDATORY)
- Validates changelog updated
- Checks comments/docstrings added
- Ensures tests pass
- Verifies no sensitive data
- Confirms commit message ready
```

**7. `security_audit`** - Security-focused audit for vulnerabilities
```
Usage: /mcp__quality__security_audit
Arguments:
  - project_path: "/path/to/project"

What it does:
- Reviews all OWASP Top 10 categories
- Provides grep commands to find issues
- Checks for hardcoded secrets
- Validates authentication/authorization
- Identifies insecure dependencies
- Prioritized action items by severity
```

#### Session Management Prompts (3)

**8. `session_start`** - Load context and plan session
```
Usage: /mcp__memory__session_start
Arguments:
  - project_path: "/path/to/project"

What it does:
- Loads project objective and clarity score
- Shows recent sessions (last 3)
- Lists key decisions made
- Displays next steps from last session
- Identifies current blockers
- Helps set goals for this session
```

**9. `session_end`** - Guided session summary before ending
```
Usage: /mcp__memory__session_end
Arguments:
  - project_path: "/path/to/project"

What it does:
- Guides through session summary creation
- Prompts for accomplishments
- Captures decisions made
- Identifies next steps
- Documents blockers
- Calls save_session_summary with structured data
```

**10. `document_decision`** - Record architectural/technical decision
```
Usage: /mcp__memory__document_decision
Arguments:
  - project_path: "/path/to/project"
  - topic: "database choice"

What it does:
- Structures decision documentation
- Captures options considered with pros/cons
- Records rationale and trade-offs
- Documents constraints
- Defines review triggers (when to reconsider)
- Calls save_decision to persist
```

### How to Use Prompts

**Method 1: Via Slash Commands** (Easiest)
```
/mcp__project__plan_feature
/mcp__quality__code_review
/mcp__memory__session_start
```

**Method 2: Ask Claude Directly**
```
"Use the plan_feature prompt to break down user authentication"
"Run the pre_commit_check prompt for this project"
"Start session using the session_start prompt"
```

**Method 3: Claude Auto-Selects**
When appropriate, Claude will automatically use prompts for structured workflows.

### Prompt Workflows

#### New Feature Development
```
1. /mcp__project__plan_feature → Break down feature
2. Implement first task
3. /mcp__quality__code_review → Review code
4. /mcp__quality__pre_commit_check → Before commit
5. Repeat for each task
6. /mcp__memory__session_end → Save progress
```

#### Session Management
```
# Start of day
1. /mcp__memory__session_start → Load context

# During work
2. /mcp__project__daily_standup → Check status
3. /mcp__memory__document_decision → Record decisions

# End of day
4. /mcp__memory__session_end → Save summary
```

#### Refocusing Project
```
1. /mcp__project__daily_standup → See current state
2. /mcp__project__refocus → Cut non-essential work
3. /mcp__memory__document_decision → Record why we cut tasks
```

#### Quality Assurance
```
1. /mcp__quality__code_review → Review files
2. Fix issues found
3. /mcp__quality__security_audit → Check security
4. Fix vulnerabilities
5. /mcp__quality__pre_commit_check → Final check
6. Commit
```

### Prompts vs Tools

**Tools** (perform actions):
- `save_session_summary` - Saves data
- `run_quality_gate` - Runs checks
- `validate_task_alignment` - Validates alignment

**Prompts** (guide workflows):
- `session_end` - Guides through creating summary, then calls save_session_summary
- `pre_commit_check` - Guides through quality checks, calls run_quality_gate
- `plan_feature` - Guides through planning, calls validate_task_alignment

**Use tools when**: You know exactly what action to take
**Use prompts when**: You want structured guidance through a workflow

### Tips for Using Prompts

1. **Let prompts guide you** - They include checklists and frameworks
2. **Answer all sections** - Prompts ensure nothing is missed
3. **Call suggested tools** - Prompts reference specific MCP tools to call
4. **Follow output format** - Prompts provide markdown templates
5. **Customize as needed** - Edit prompt code in `*_mcp.py` files

---

## Workflows

### New Project Workflow

```
1. "Clarify project objective: [brief description]"
   ↓
2. Answer comprehensive questions until clarity score >80
   ↓
3. "Define project objective"
   ↓
4. "Create task breakdown"
   ↓
5. "Get current status" - See objective and tasks
   ↓
6. Start working on highest priority task
   ↓
7. "Run quality gate" - Before completion
   ↓
8. "Mark task complete" (if quality gate passed)
   ↓
9. Repeat steps 6-8 for each task
   ↓
10. Every 10 tasks: "Identify scope creep"
```

### Existing Project Workflow

```
1. Run retrofit tools (see RETROFIT_METHODOLOGY.md)
   ↓
2. "Extract objective from existing code"
   ↓
3. Refine objective via clarification
   ↓
4. "Sync plan to reality"
   ↓
5. Continue with normal workflow
```

### Daily Development Workflow

```
# Session start
1. "Load project context"
2. "Get current status"
3. See objective and current task

# During work
4. "Validate task alignment" - Before starting new task
5. "Challenge task priority" - Is this most important?
6. Work on task (TDD: test → implement → refactor)
7. "Run quality gate"

# Session end
8. "Mark task complete" (if quality gate passed)
9. "Save session summary"
```

---

## Integration with Best Practices

### Minimal Root Structure

Quality MCP enforces:
- ✅ Root folders ≤5
- ✅ All operational data in `artifacts/`
- ✅ No forbidden folders (logs, temp, etc. in root)
- ✅ Files in correct locations

### Quality Gates

Quality MCP blocks progression without:
- ✅ Tests passing (≥80% coverage)
- ✅ Zero linting errors (Ruff)
- ✅ Zero type errors (MyPy)
- ✅ No security issues (Bandit)
- ✅ Low complexity (Radon ≤10)
- ✅ Docstrings present (≥80%)

### Objective Alignment

Project MCP ensures:
- ✅ Objective clarity score >80 before starting
- ✅ Every task alignment score ≥70
- ✅ Automatic scope creep detection
- ✅ Priority challenges
- ✅ Always-current PROJECT_PLAN.md

---

## Troubleshooting

### MCPs Not Showing Up

```bash
# Check MCP files exist
ls -la ~/.mcp-servers/

# Check permissions
chmod +x ~/.mcp-servers/*.py

# Check Python path in config
which python3

# Update config with correct path
```

### Quality Gate Fails

```bash
# Check if quality tools installed
cd your-project
ls .ai-validation/

# Install quality tools
cp -r /path/to/best-practice/.ai-validation/ .
bash .ai-validation/install_tools.sh

# Run quality gate manually
bash .ai-validation/check_quality.sh
```

### Objective Clarity Score Low

```
# Continue answering questions
"Answer objective question [question_id]: [more specific answer]"

# Check score
"Score objective clarity"

# Identify weak areas
# The tool will tell you which areas need more detail

# Provide more specific answers for weak areas
```

### Task Blocked - Not Aligned

```
# Check alignment score
"Validate task alignment: [task description]"

# If score <70, task doesn't serve objective
# Options:
# 1. Defer task
# 2. Cut task
# 3. Refine task to better serve objective
```

---

## Advanced Configuration

### Gradual Quality Enforcement

Edit Quality MCP to add enforcement levels:

```python
# In quality_mcp.py
ENFORCEMENT_LEVEL = os.getenv("QUALITY_ENFORCEMENT", "full")
# Options: soft, partial, full

# soft - reports but never blocks
# partial - blocks only critical issues
# full - blocks on any failure
```

Set environment variable:
```bash
export QUALITY_ENFORCEMENT=soft  # Week 1
export QUALITY_ENFORCEMENT=partial  # Week 2-3
export QUALITY_ENFORCEMENT=full  # Week 4+
```

### Custom Quality Standards

Edit Quality MCP standards:

```python
QUALITY_STANDARDS = {
    "function_max_lines": 30,  # Adjust as needed
    "test_coverage_min": 80,
    "complexity_max": 10,
    "docstring_coverage_min": 80
}
```

### Objective Scoring Weights

Edit Project MCP scoring:

```python
# In _calculate_clarity_score method
score = (
    problem_score * 0.3 +  # Adjust weights
    user_score * 0.2 +
    solution_score * 0.2 +
    metrics_score * 0.2 +
    constraints_score * 0.1
)
```

---

## Storage Locations

### Memory MCP

```
~/.claude_memory/
├── project1.json
├── project2.json
└── ...
```

Each project gets own JSON file with:
- Session summaries
- Decisions
- Objective
- Tech stack

### Project MCP

```
your-project/
├── .project_manager/
│   └── project_data.json
├── docs/
│   └── notes/
│       └── PROJECT_PLAN.md
└── artifacts/
    └── logs/
        └── completed-actions.log
```

### Quality MCP

No persistent storage - uses project's `.ai-validation/` scripts

---

## Uninstallation

```bash
# Remove MCP servers
rm -rf ~/.mcp-servers/

# Remove Claude config
# Edit and remove mcpServers section from:
# ~/.config/claude/claude_desktop_config.json

# Remove memory storage (optional)
rm -rf ~/.claude_memory/

# Remove project-specific data (per project)
rm -rf your-project/.project_manager/
```

---

## FAQ

**Q: Do I need all three MCPs?**
A: No. You can enable them individually:
- Just Quality MCP → Code quality enforcement only
- Just Project MCP → Objective-driven management only
- All three → Complete system

**Q: Can I use with existing projects?**
A: Yes! See RETROFIT_METHODOLOGY.md for complete guide.

**Q: What if I disagree with a priority challenge?**
A: You can override. MCPs suggest, you decide. But consider the reasoning.

**Q: Can I modify the MCPs?**
A: Yes! They're Python scripts. Customize to your needs.

**Q: Will quality gates slow me down?**
A: Initially, yes. Long-term, they speed you up by preventing technical debt.

**Q: What if objective changes mid-project?**
A: Run objective clarification again, update objective, revalidate tasks.

**Q: How much disk space do MCPs use?**
A: Minimal. ~1MB for servers, ~1KB per project for memory.

---

## Support

**Issues**: Create issue at [repository]
**Documentation**: See other markdown files in this directory
**Updates**: Check for new versions periodically

---

## License

MIT License - Use freely in your projects

---

## Version History

- **v1.0** (2025-10-29) - Initial release
  - Memory MCP with objective storage
  - Quality MCP with structure enforcement
  - Project MCP with objective clarification

---

**Ready to enforce excellence in your projects!** 🚀
