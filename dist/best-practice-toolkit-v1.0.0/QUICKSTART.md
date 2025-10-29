# Quick Start Guide

## 1. Install (5 minutes)

```bash
cd best-practice-toolkit-v1.0.0
./install.sh
```

Follow the instructions to configure Claude Code.

## 2. Choose Your Path

### Path A: New Project

```bash
# Copy project setup
cp -r project-setup/setup_project.sh ~/
cp -r project-setup/.ai-validation ~/

# Create project
cd ~
./setup_project.sh my-new-project

# Start Claude Code
# Say: "Clarify project objective: [your idea]"
```

### Path B: Existing Project

```bash
# Read retrofit guide
cat docs/RETROFIT_METHODOLOGY.md

# Or quick retrofit:
cd your-existing-project
git commit -m "Safe state"
# Then use MCPs to assess and improve
```

## 3. Daily Workflow

```
# Session start
"Load project context"
"Get current status"

# Development
"Validate task alignment: [task]"
"Challenge task priority for task_X"
[Work on task - TDD cycle]
"Run quality gate"

# Session end
"Mark task complete (quality gate passed: true)"
"Save session summary"
```

## 4. Read More

- `README.md` - Complete system overview
- `docs/` - Detailed guides
- `mcp-servers/README.md` - MCP documentation

## Success!

You're now using objective-driven development with enforced best practices! 🚀
