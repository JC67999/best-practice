# Best Practice Toolkit - Complete Installation Guide

> **Purpose**: Step-by-step instructions for installing the toolkit
> **Last Updated**: 2025-10-30
> **Time Required**: 10-15 minutes

---

## 🎯 Overview

Two installation methods available:

1. **Quick Retrofit** (Recommended) - One question, automatic setup
2. **Manual Installation** - Full control over installation

Both methods install the same components - choose based on your preference.

---

## 🚀 Method 1: Quick Retrofit (Recommended)

**Best for**: Quick setup, existing projects, minimal decisions

### Prerequisites

```bash
# Required
- Git installed
- Bash shell
- Project you want to retrofit

# Optional (for full mode)
- Python 3.10+
- pytest (for running tests)
```

### Installation Steps

#### Step 1: Navigate to Your Project

```bash
cd /path/to/your/project
```

**Example**:
```bash
cd ~/projects/my-web-app
```

#### Step 2: Run the Quick Retrofit Script

```bash
/home/jc/CascadeProjects/best-practice/retrofit-tools/quick_retrofit.sh
```

Or if you cloned the toolkit elsewhere:
```bash
/path/to/best-practice-toolkit/retrofit-tools/quick_retrofit.sh
```

#### Step 3: Answer ONE Question

The script asks: **"Is this a production system?"**

**Choose "Yes" (Production)** if:
- Code is currently deployed/running
- Users depend on it
- Breaking changes are risky
- You want minimal disruption

**Result**: Light touch retrofit
- Organizes docs into `docs/` subdirectories
- Creates `PROJECT_PLAN.md` with objective
- Adds `CLAUDE.md` project standards
- Installs MCP servers
- ~10 minutes
- Safe for production

**Choose "No" (Not Production)** if:
- Project is in development
- No users yet
- You can refactor freely
- You want full best practices

**Result**: Full implementation
- Everything from Light touch +
- Quality gate (`.ai-validation/`)
- Test structure (`tests/`)
- `.gitignore` file
- ~15 minutes
- Ready for excellence

#### Step 4: Review Results

Script will:
1. Create safety checkpoint (git tag: `retrofit-start`)
2. Organize your project structure
3. Create `PROJECT_PLAN.md` (asks 3 quick questions)
4. Add `CLAUDE.md` standards
5. Install MCP servers
6. Commit all changes
7. Validate installation

**Output looks like**:
```
✅  Retrofit Complete!

What Changed:
  📁 Structure:
     • docs/ - All documentation organized
     • docs/notes/PROJECT_PLAN.md - Your objective
     • CLAUDE.md - Project standards
     • mcp-servers/ - MCP servers installed

Git Tags:
  • retrofit-start - Before changes (rollback point)
  • retrofit-complete - After changes (current)

Next Steps:
  1. Review: docs/notes/PROJECT_PLAN.md
  2. Customize: CLAUDE.md for your project
  3. Run quality gate: .ai-validation/check_quality.sh (full mode)
```

#### Step 5: Rollback (If Needed)

If something went wrong:
```bash
git reset --hard retrofit-start
git tag -d retrofit-complete
```

This restores your project to exactly how it was before.

---

## 🔧 Method 2: Manual Installation

**Best for**: Maximum control, understanding each step, custom setups

### Step 1: Get the Toolkit

#### Option A: Clone the Repository
```bash
git clone https://github.com/your-org/best-practice-toolkit.git
cd best-practice-toolkit
```

#### Option B: Download Release
```bash
# Download from releases page
wget https://github.com/your-org/best-practice-toolkit/archive/v1.0.0.tar.gz
tar -xzf v1.0.0.tar.gz
cd best-practice-toolkit-1.0.0
```

#### Option C: Use Existing Local Copy
```bash
cd /home/jc/CascadeProjects/best-practice
# Or wherever you have it
```

### Step 2: Run Install Script

```bash
# From toolkit directory, install to target project
./install.sh /path/to/your/project

# Or from your project directory
/path/to/toolkit/install.sh .
```

**What this does**:
- Creates directory structure (docs/notes, .ai-validation, mcp-servers)
- Copies MCP server files
- Copies quality gate script
- Copies CLAUDE.md template (if not exists)

### Step 3: Manual Setup Tasks

After install.sh completes, do these manually:

#### A. Create PROJECT_PLAN.md

```bash
cd /path/to/your/project
```

Create `docs/notes/PROJECT_PLAN.md`:
```markdown
# Project Plan - [Your Project]

> **Created**: 2025-10-30
> **Status**: Development
> **Clarity Score**: To be refined

---

## 🎯 Project Objective

### Problem
[What problem does this project solve?]

### Target Users
[Who are the users?]

### Solution
[What's your solution?]

### Success Metrics
- [Add measurable success metrics]

### Constraints
- [Add constraints]

---

## 📊 Current Status

**What's Working Well**:
- [List what's working]

**What Needs Improvement**:
- [List areas for improvement]

---

## 🗺️ Roadmap

### Current Focus
- [Current sprint/milestone]

### Next Steps
- [Upcoming work]

---

**Last Updated**: 2025-10-30
```

#### B. Organize Documentation (Optional)

Move markdown files to appropriate locations:

```bash
# Design documents
mv ARCHITECTURE.md docs/design/
mv IMPLEMENTATION.md docs/design/

# Guides
mv SETUP_GUIDE.md docs/guides/
mv HOWTO.md docs/guides/

# Analysis
mv REVIEW.md docs/analysis/
mv ASSESSMENT.md docs/analysis/

# Notes
mv TODO.md docs/notes/
mv CHANGELOG.md docs/notes/
```

#### C. Create Test Structure (Optional - Full Mode)

```bash
mkdir -p tests

# Create conftest.py
cat > tests/conftest.py <<'EOF'
"""
Pytest configuration and fixtures.
"""
import pytest

# Add your fixtures here
EOF

# Create basic test
cat > tests/test_basic.py <<'EOF'
"""Basic tests."""
import pytest


class TestBasic:
    """Basic test suite."""

    def test_placeholder(self):
        """Placeholder test."""
        assert True
EOF
```

#### D. Commit Changes

```bash
git add -A
git commit -m "feat: install best-practice toolkit

- Added MCP servers (memory, quality, project)
- Added quality gate (.ai-validation/)
- Created PROJECT_PLAN.md
- Added CLAUDE.md standards

🤖 Generated with [Claude Code](https://claude.com/claude-code)

Co-Authored-By: Claude <noreply@anthropic.com>"
```

---

## 📦 What Gets Installed

### All Modes

#### 1. MCP Servers (`mcp-servers/`)
Three Python MCP servers:
- **memory_mcp.py** - Context persistence across sessions
- **quality_mcp.py** - Quality enforcement and validation
- **project_mcp.py** - Objective-driven task management
- **learning_mcp.py** - Code review and self-learning (bonus)

#### 2. Project Standards (`CLAUDE.md`)
- File placement rules
- Development workflow
- Quality standards
- Git conventions
- **MANDATORY MCP Usage** directives

#### 3. Documentation Structure (`docs/`)
```
docs/
├── design/         # Architecture, implementation docs
├── guides/         # How-to guides, methodologies
├── analysis/       # Assessments, summaries, reviews
├── references/     # Reference materials
└── notes/          # Planning, TODOs, changelogs
    └── PROJECT_PLAN.md  # Your project objective
```

### Full Mode Only

#### 4. Quality Gate (`.ai-validation/check_quality.sh`)
Automated quality checks:
- Test coverage (≥80% required)
- Linting (Ruff)
- Type checking (MyPy)
- Security (Bandit)
- Structure compliance

#### 5. Test Structure (`tests/`)
```
tests/
├── conftest.py      # Pytest configuration
├── test_basic.py    # Example test
└── README.md        # Testing docs
```

#### 6. Git Configuration (`.gitignore`)
Sensible defaults for:
- Python (\_\_pycache\_\_, *.pyc)
- IDEs (VS Code, PyCharm)
- OS files (.DS_Store)
- Build artifacts

---

## 🔌 MCP Server Configuration

After installation, configure Claude Code to use the MCP servers:

### Step 1: Find MCP Server Paths

```bash
# Quick retrofit installs to project/mcp-servers/
ls -la mcp-servers/
# Should show: memory_mcp.py, quality_mcp.py, project_mcp.py
```

### Step 2: Configure Claude Desktop

Edit `~/.config/claude/claude_desktop_config.json`:

```json
{
  "mcpServers": {
    "memory": {
      "command": "python3",
      "args": [
        "/home/YOUR_USERNAME/.mcp-servers/memory_mcp.py"
      ],
      "disabled": false
    },
    "quality": {
      "command": "python3",
      "args": [
        "/home/YOUR_USERNAME/.mcp-servers/quality_mcp.py"
      ],
      "disabled": false
    },
    "project": {
      "command": "python3",
      "args": [
        "/home/YOUR_USERNAME/.mcp-servers/project_mcp.py"
      ],
      "disabled": false
    }
  }
}
```

**Note**: Replace `/home/YOUR_USERNAME/` with your actual home directory.

### Step 3: Copy MCPs to Home Directory

For Claude Desktop to find them:

```bash
mkdir -p ~/.mcp-servers
cp mcp-servers/*.py ~/.mcp-servers/
chmod +x ~/.mcp-servers/*.py
```

### Step 4: Restart Claude

Restart Claude Code/Desktop to load the new MCP servers.

### Step 5: Verify

In Claude, ask: "List available MCP tools"

You should see tools from all three MCPs.

---

## ✅ Validation Checklist

After installation, verify everything is working:

### Files Created

- [ ] `CLAUDE.md` exists in project root
- [ ] `docs/notes/PROJECT_PLAN.md` exists
- [ ] `docs/` directory structure created
- [ ] `mcp-servers/` directory with 3-4 .py files
- [ ] `.ai-validation/check_quality.sh` exists (full mode)
- [ ] `tests/` directory exists (full mode)
- [ ] `.gitignore` exists (full mode)

### MCP Servers

- [ ] MCPs copied to `~/.mcp-servers/`
- [ ] Claude Desktop config updated
- [ ] Claude restarted
- [ ] "List MCP tools" shows memory/quality/project tools

### Git

- [ ] Changes committed
- [ ] Tag `retrofit-start` exists (quick retrofit only)
- [ ] Tag `retrofit-complete` exists (quick retrofit only)

### Documentation

- [ ] PROJECT_PLAN.md has project objective
- [ ] CLAUDE.md customized for your project
- [ ] Markdown files organized in docs/ (if any existed)

---

## 🐛 Troubleshooting

### Issue: Script Permission Denied

**Problem**: `bash: permission denied: quick_retrofit.sh`

**Solution**:
```bash
chmod +x /path/to/retrofit-tools/quick_retrofit.sh
# Then run again
```

---

### Issue: Not a Git Repository

**Problem**: "Cannot retrofit without git"

**Solution**:
```bash
git init
git add .
git commit -m "Initial commit"
# Then run retrofit script again
```

---

### Issue: Uncommitted Changes

**Problem**: "Uncommitted changes detected"

**Solution**:
Choose one:
```bash
# Option 1: Stash changes (script will offer this)
git stash

# Option 2: Commit changes
git add .
git commit -m "WIP: before retrofit"

# Option 3: Discard changes (careful!)
git reset --hard HEAD
```

---

### Issue: MCPs Not Showing in Claude

**Problem**: "List MCP tools" doesn't show memory/quality/project

**Solutions**:

1. **Check MCP files exist**:
   ```bash
   ls -la ~/.mcp-servers/
   # Should show: memory_mcp.py, quality_mcp.py, project_mcp.py
   ```

2. **Check Claude config**:
   ```bash
   cat ~/.config/claude/claude_desktop_config.json
   # Should have mcpServers section
   ```

3. **Check Python path**:
   ```bash
   which python3
   # Use this path in Claude config
   ```

4. **Restart Claude**:
   Quit and restart Claude Desktop/Code completely

5. **Check permissions**:
   ```bash
   chmod +x ~/.mcp-servers/*.py
   ```

---

### Issue: Quality Gate Fails

**Problem**: `.ai-validation/check_quality.sh` fails

**Solution**:
```bash
# Install quality tools
pip install pytest ruff mypy bandit

# Check what's failing
cd .ai-validation
bash check_quality.sh

# Fix issues one by one
```

---

### Issue: Wrong Mode Applied

**Problem**: Chose wrong mode (light/full)

**Solution - Quick Retrofit**:
```bash
# Rollback
git reset --hard retrofit-start
git tag -d retrofit-complete

# Run again with correct choice
/path/to/quick_retrofit.sh
```

**Solution - Manual Install**:
Just run install.sh again - it won't overwrite existing files.

---

## 🔄 Upgrading

### To Upgrade an Existing Installation

```bash
# 1. Backup current setup
git tag backup-before-upgrade

# 2. Get latest toolkit
cd /path/to/best-practice-toolkit
git pull origin main

# 3. Re-run installation
cd /path/to/your/project
/path/to/best-practice-toolkit/retrofit-tools/quick_retrofit.sh

# Script will detect existing files and skip/update appropriately
```

---

## 📚 Next Steps After Installation

### 1. Refine Your Objective

Edit `docs/notes/PROJECT_PLAN.md`:
- Make problem statement specific
- Define measurable success metrics
- Add concrete constraints
- Target clarity score: >80

### 2. Customize CLAUDE.md

Update `CLAUDE.md` for your project:
- Adjust file placement rules if needed
- Add project-specific conventions
- Update quality standards thresholds
- Customize workflow for your team

### 3. Test MCP Integration

Try these commands with Claude:
```
"Load project context"
"Get current status"
"Validate task alignment for: add user authentication"
"Run quality gate"
```

### 4. Add Real Tests (Full Mode)

Replace placeholder test in `tests/test_basic.py`:
```python
def test_something_real(self):
    """Test real functionality."""
    result = my_function()
    assert result == expected_value
```

### 5. Run Quality Gate (Full Mode)

```bash
cd .ai-validation
bash check_quality.sh
```

Fix any issues it finds.

### 6. Start Using Best Practices

From now on:
- Claude will automatically use MCPs (per CLAUDE.md)
- Quality gates block commits with issues
- Tasks validated for objective alignment
- Context persists across sessions

---

## 📊 Installation Summary

| Method | Time | Control | Best For |
|--------|------|---------|----------|
| **Quick Retrofit** | 10-15 min | Low | Most users, existing projects |
| **Manual Install** | 20-30 min | High | Custom setups, learning |

| Mode | Components | Safety | Best For |
|------|-----------|--------|----------|
| **Light Touch** | Docs, standards, MCPs | Production-safe | Live systems, minimal changes |
| **Full Implementation** | Everything + quality gate + tests | Development | New projects, full best practices |

---

## 🆘 Getting Help

**Issues**: File at [repository issues](https://github.com/your-org/best-practice-toolkit/issues)

**Questions**:
- Review `docs/README.md` for full documentation
- Check `docs/guides/MCP_USAGE_EXAMPLES.md` for MCP usage
- Read `docs/guides/RETROFIT_METHODOLOGY.md` for methodology

**Common Resources**:
- Installation: This file
- MCP Usage: `docs/guides/MCP_USAGE_EXAMPLES.md`
- Project Standards: `CLAUDE.md`
- Retrofit Process: `docs/guides/RETROFIT_METHODOLOGY.md`

---

**Installation complete! Your project now follows best practices. 🚀**

---

**Last Updated**: 2025-10-30
**Version**: 1.0.0
