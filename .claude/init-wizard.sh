#!/usr/bin/env bash
#
# Best Practice Toolkit - Post-Injection Initialization Wizard
# Interactive setup after toolkit injection
#
set -e

# Colors
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m'

clear
echo "════════════════════════════════════════════════════════"
echo -e "  ${GREEN}Best Practice Toolkit - Initialization Wizard${NC}"
echo "════════════════════════════════════════════════════════"
echo ""
echo "This wizard will configure the toolkit for your project."
echo ""

# Detect project root
PROJECT_ROOT="$(pwd)"
PROJECT_NAME="$(basename "$PROJECT_ROOT")"

echo -e "${BLUE}Project:${NC} $PROJECT_NAME"
echo -e "${BLUE}Path:${NC}    $PROJECT_ROOT"
echo ""

# Step 1: Detect project type
echo "────────────────────────────────────────────────────────"
echo -e "${GREEN}Step 1: Detecting Project Type${NC}"
echo "────────────────────────────────────────────────────────"
echo ""

detect_project_type() {
    # Check for various project markers
    if [ -f "pyproject.toml" ] || [ -f "setup.py" ] || [ -f "requirements.txt" ]; then
        echo "python"
    elif [ -f "package.json" ]; then
        if grep -q "\"react\"" package.json 2>/dev/null; then
            echo "javascript-react"
        elif grep -q "\"@angular\"" package.json 2>/dev/null; then
            echo "javascript-angular"
        else
            echo "javascript"
        fi
    elif [ -f "go.mod" ]; then
        echo "go"
    elif [ -f "Cargo.toml" ]; then
        echo "rust"
    elif [ -f "pom.xml" ] || [ -f "build.gradle" ]; then
        echo "java"
    else
        echo "unknown"
    fi
}

DETECTED_TYPE=$(detect_project_type)
echo -e "Detected type: ${YELLOW}$DETECTED_TYPE${NC}"
echo ""

# Confirm or override
read -p "Is this correct? (Y/n): " -n 1 -r
echo ""
if [[ $REPLY =~ ^[Nn]$ ]]; then
    echo ""
    echo "Available types:"
    echo "  1) Python"
    echo "  2) JavaScript/TypeScript"
    echo "  3) Go"
    echo "  4) Rust"
    echo "  5) Java"
    echo "  6) Other"
    echo ""
    read -p "Select project type (1-6): " -n 1 -r TYPE_CHOICE
    echo ""
    case $TYPE_CHOICE in
        1) PROJECT_TYPE="python" ;;
        2) PROJECT_TYPE="javascript" ;;
        3) PROJECT_TYPE="go" ;;
        4) PROJECT_TYPE="rust" ;;
        5) PROJECT_TYPE="java" ;;
        6) PROJECT_TYPE="other" ;;
        *) PROJECT_TYPE="unknown" ;;
    esac
else
    PROJECT_TYPE="$DETECTED_TYPE"
fi

echo ""
echo -e "${GREEN}✓${NC} Project type: $PROJECT_TYPE"
echo ""

# Step 2: Team configuration
echo "────────────────────────────────────────────────────────"
echo -e "${GREEN}Step 2: Team Configuration${NC}"
echo "────────────────────────────────────────────────────────"
echo ""

echo "Team size:"
echo "  1) Solo developer"
echo "  2) Small team (2-5)"
echo "  3) Large team (6+)"
echo ""
read -p "Select (1-3): " -n 1 -r TEAM_SIZE_CHOICE
echo ""

case $TEAM_SIZE_CHOICE in
    1) TEAM_SIZE="solo" ;;
    2) TEAM_SIZE="small" ;;
    3) TEAM_SIZE="large" ;;
    *) TEAM_SIZE="solo" ;;
esac

echo -e "${GREEN}✓${NC} Team size: $TEAM_SIZE"
echo ""

# Step 3: CI/CD setup
echo "────────────────────────────────────────────────────────"
echo -e "${GREEN}Step 3: CI/CD Configuration${NC}"
echo "────────────────────────────────────────────────────────"
echo ""

read -p "Do you use CI/CD? (Y/n): " -n 1 -r
echo ""
if [[ $REPLY =~ ^[Nn]$ ]]; then
    CI_CD="none"
else
    echo ""
    echo "CI/CD platform:"
    echo "  1) GitHub Actions"
    echo "  2) GitLab CI"
    echo "  3) Jenkins"
    echo "  4) Other"
    echo ""
    read -p "Select (1-4): " -n 1 -r CI_CHOICE
    echo ""
    case $CI_CHOICE in
        1) CI_CD="github-actions" ;;
        2) CI_CD="gitlab-ci" ;;
        3) CI_CD="jenkins" ;;
        4) CI_CD="other" ;;
        *) CI_CD="none" ;;
    esac
fi

echo -e "${GREEN}✓${NC} CI/CD: $CI_CD"
echo ""

# Step 4: Create configuration
echo "────────────────────────────────────────────────────────"
echo -e "${GREEN}Step 4: Creating Configuration${NC}"
echo "────────────────────────────────────────────────────────"
echo ""

# Create .claude/config.json
cat > .claude/config.json <<EOF
{
  "project": {
    "name": "$PROJECT_NAME",
    "type": "$PROJECT_TYPE",
    "team_size": "$TEAM_SIZE",
    "ci_cd": "$CI_CD"
  },
  "standards": {
    "max_task_lines": 30,
    "max_task_minutes": 15,
    "test_coverage_minimum": 80,
    "commit_message_format": "conventional"
  },
  "quality_gate": {
    "enabled": true,
    "auto_fix": true,
    "block_commit_on_failure": true
  },
  "git_hooks": {
    "pre_commit": true,
    "commit_msg": true,
    "pre_push": true
  },
  "skills": {
    "auto_load": true
  }
}
EOF

echo -e "${GREEN}✓${NC} Created .claude/config.json"
echo ""

# Step 5: Install git hooks
echo "────────────────────────────────────────────────────────"
echo -e "${GREEN}Step 5: Installing Git Hooks${NC}"
echo "────────────────────────────────────────────────────────"
echo ""

read -p "Install git hooks for quality enforcement? (Y/n): " -n 1 -r
echo ""
if [[ ! $REPLY =~ ^[Nn]$ ]]; then
    if [ -f ".claude/hooks/install-hooks.sh" ]; then
        bash .claude/hooks/install-hooks.sh
        echo ""
        echo -e "${GREEN}✓${NC} Git hooks installed"
    else
        echo -e "${YELLOW}⚠${NC} Git hooks not found (will be created soon)"
    fi
else
    echo -e "${YELLOW}⚠${NC} Skipped git hooks installation"
fi
echo ""

# Step 6: Initialize project objective (if MCP available)
echo "────────────────────────────────────────────────────────"
echo -e "${GREEN}Step 6: Project Objective${NC}"
echo "────────────────────────────────────────────────────────"
echo ""

echo "Would you like to define your project objective now?"
echo "(This helps AI assistants stay focused on your goals)"
echo ""
read -p "Define project objective? (Y/n): " -n 1 -r
echo ""

if [[ ! $REPLY =~ ^[Nn]$ ]]; then
    echo ""
    echo "Please answer these questions in Claude Code:"
    echo ""
    echo "  1. What problem does this project solve?"
    echo "  2. Who are the target users?"
    echo "  3. What is the core solution?"
    echo "  4. What defines success?"
    echo ""
    echo "After answering, run in Claude Code:"
    echo "  mcp__project__clarify_project_objective"
    echo ""
else
    echo -e "${YELLOW}⚠${NC} Skipped project objective (can set later)"
fi
echo ""

# Step 7: Create initial TASKS.md
echo "────────────────────────────────────────────────────────"
echo -e "${GREEN}Step 7: Creating Initial Tasks${NC}"
echo "────────────────────────────────────────────────────────"
echo ""

if [ ! -f ".claude/TASKS.md" ]; then
    cat > .claude/TASKS.md <<EOF
# Project Tasks

> **Last Updated**: $(date +%Y-%m-%d)

## Current Sprint: Initial Setup

### 🔄 In Progress
- [ ] Complete toolkit initialization wizard
- [ ] Review and customize .claude/config.json
- [ ] Set up project objective in Claude Code

### 📋 Todo
- [ ] Run initial quality audit: \`mcp__quality__audit_project_structure\`
- [ ] Review file placement rules in .claude/skills/file-placement/
- [ ] Set up testing framework (if not present)
- [ ] Create first checkpoint: \`git tag checkpoint-initial-setup\`
- [ ] Review CLAUDE.md standards

### ✅ Completed
- [x] Run toolkit injection
- [x] Complete initialization wizard
- [x] Create project configuration

## Guidelines

- Task size: ≤30 lines of code, ≤15 minutes
- One task at a time: Complete, test, commit
- Break large tasks into smaller sub-tasks
- Update this file as you work

## Resources

- Standards: \`CLAUDE.md\`
- Skills: \`.claude/skills/\`
- Quality gate: \`bash .claude/quality-gate/check_quality.sh\`
EOF
    echo -e "${GREEN}✓${NC} Created .claude/TASKS.md"
else
    echo -e "${YELLOW}⚠${NC} TASKS.md already exists (not overwritten)"
fi
echo ""

# Step 8: Summary
echo "════════════════════════════════════════════════════════"
echo -e "  ${GREEN}✅ Initialization Complete${NC}"
echo "════════════════════════════════════════════════════════"
echo ""
echo -e "${BLUE}Configuration Created:${NC}"
echo "  • .claude/config.json - Project settings"
echo "  • .claude/TASKS.md - Initial task list"
if [[ ! $REPLY =~ ^[Nn]$ ]]; then
    echo "  • Git hooks installed"
fi
echo ""
echo -e "${BLUE}Next Steps:${NC}"
echo "  1. Review: .claude/config.json"
echo "  2. Review: .claude/TASKS.md"
echo "  3. Open in Claude Code: code ."
echo "  4. Set project objective (if skipped)"
echo "  5. Start first task!"
echo ""
echo -e "${BLUE}Quick Commands:${NC}"
echo "  cat .claude/config.json           # View configuration"
echo "  cat .claude/TASKS.md              # View tasks"
echo "  cat CLAUDE.md                     # View standards"
echo "  bash .claude/quality-gate/check_quality.sh  # Run quality gate"
echo ""
echo -e "${GREEN}Happy coding! 🚀${NC}"
echo ""
