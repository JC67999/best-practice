# MCP Servers - Installation and Configuration Guide

> **Complete MCP setup for objective-driven development with best practices**
> **Version**: 1.0
> **Date**: 2025-10-29

---

## Overview

Three production-ready MCP servers that enforce excellent coding practices:

1. **Memory MCP** - Persistent context across sessions
2. **Quality MCP** - Automated quality enforcement
3. **Project MCP** - Objective-driven task management

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
