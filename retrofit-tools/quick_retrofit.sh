#!/bin/bash

# Quick Retrofit - Simple Question, Smart Implementation
# Asks one question: Production or Not? Then does the right thing.

set -e

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
BOLD='\033[1m'
NC='\033[0m'

clear
echo -e "${BOLD}${BLUE}"
echo "╔════════════════════════════════════════════════════════╗"
echo "║                                                        ║"
echo "║         Best Practice Retrofit - Quick Mode           ║"
echo "║                                                        ║"
echo "╚════════════════════════════════════════════════════════╝"
echo -e "${NC}"
echo ""

# Check if we're in a project directory
if [ ! -d ".git" ]; then
    echo -e "${YELLOW}⚠️  Warning: Not a git repository${NC}"
    echo ""
    read -p "Initialize git repository? (Y/n): " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Nn]$ ]]; then
        git init
        git add .
        git commit -m "Initial commit before retrofit"
        echo -e "${GREEN}✅ Git initialized${NC}"
    else
        echo -e "${RED}Cannot retrofit without git (for safety). Exiting.${NC}"
        exit 1
    fi
fi

PROJECT_DIR=$(pwd)
PROJECT_NAME=$(basename "$PROJECT_DIR")
TOOLKIT_DIR="/home/jc/CascadeProjects/best-practice"

echo -e "${BLUE}Project:${NC} $PROJECT_NAME"
echo -e "${BLUE}Path:${NC} $PROJECT_DIR"
echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""

# THE QUESTION
echo -e "${BOLD}${YELLOW}Is this a production system?${NC}"
echo ""
echo "  ${BOLD}Yes${NC} → Light touch (minimal disruption, safe for production)"
echo "         • Organize docs only"
echo "         • Create PROJECT_PLAN.md"
echo "         • Add CLAUDE.md"
echo "         • ~10 minutes"
echo ""
echo "  ${BOLD}No${NC}  → Full implementation (all best practices)"
echo "         • Everything from Light +"
echo "         • Quality gate (.ai-validation/)"
echo "         • Test structure"
echo "         • .gitignore"
echo "         • Ready for excellence"
echo "         • ~15 minutes"
echo ""
read -p "Production system? (y/N): " -n 1 -r IS_PRODUCTION
echo ""
echo ""

# Determine mode
if [[ $IS_PRODUCTION =~ ^[Yy]$ ]]; then
    MODE="LIGHT"
    MODE_NAME="Light Touch (Production Safe)"
    echo -e "${YELLOW}Mode: ${MODE_NAME}${NC}"
else
    MODE="FULL"
    MODE_NAME="Full Implementation"
    echo -e "${GREEN}Mode: ${MODE_NAME}${NC}"
fi

echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""

# Safety checkpoint
echo -e "${BLUE}[1/6]${NC} Creating safety checkpoint..."

# Check for uncommitted changes
if ! git diff-index --quiet HEAD -- 2>/dev/null; then
    echo -e "${YELLOW}⚠️  Uncommitted changes detected${NC}"
    read -p "Stash changes and continue? (Y/n): " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Nn]$ ]]; then
        git stash
        STASHED=true
        echo -e "${GREEN}✅ Changes stashed${NC}"
    else
        echo -e "${RED}Please commit or stash changes first. Exiting.${NC}"
        exit 1
    fi
fi

git tag -f retrofit-start
echo -e "${GREEN}✅ Safety checkpoint created (tag: retrofit-start)${NC}"
echo "   Rollback: git reset --hard retrofit-start"
echo ""

# Create directory structure
echo -e "${BLUE}[2/6]${NC} Creating directory structure..."
mkdir -p docs/design
mkdir -p docs/guides
mkdir -p docs/analysis
mkdir -p docs/references
mkdir -p docs/notes

if [ "$MODE" = "FULL" ]; then
    mkdir -p tests
    mkdir -p .ai-validation
fi

echo -e "${GREEN}✅ Directories created${NC}"
echo ""

# Move documentation files
echo -e "${BLUE}[3/6]${NC} Organizing documentation..."

# Count files to move
MD_COUNT=$(find . -maxdepth 1 -name "*.md" ! -name "README.md" ! -name "CLAUDE.md" 2>/dev/null | wc -l)

if [ "$MD_COUNT" -gt 0 ]; then
    echo "   Found $MD_COUNT documentation files to organize"

    for file in *.md; do
        if [ -f "$file" ] && [ "$file" != "README.md" ] && [ "$file" != "CLAUDE.md" ]; then
            # Smart categorization
            if [[ $file =~ DESIGN|ARCHITECTURE|IMPLEMENTATION|APPROACH|INTEGRATION ]]; then
                git mv "$file" docs/design/ 2>/dev/null || mv "$file" docs/design/
                echo "   → docs/design/$file"
            elif [[ $file =~ GUIDE|METHODOLOGY|ROADMAP|SETUP|HOWTO|TUTORIAL ]]; then
                git mv "$file" docs/guides/ 2>/dev/null || mv "$file" docs/guides/
                echo "   → docs/guides/$file"
            elif [[ $file =~ ANALYSIS|SUMMARY|ASSESSMENT|REPORT|REVIEW ]]; then
                git mv "$file" docs/analysis/ 2>/dev/null || mv "$file" docs/analysis/
                echo "   → docs/analysis/$file"
            elif [[ $file =~ CHANGELOG|TODO|NOTES ]]; then
                git mv "$file" docs/notes/ 2>/dev/null || mv "$file" docs/notes/
                echo "   → docs/notes/$file"
            else
                git mv "$file" docs/ 2>/dev/null || mv "$file" docs/
                echo "   → docs/$file"
            fi
        fi
    done
    echo -e "${GREEN}✅ Documentation organized${NC}"
else
    echo "   No markdown files to organize"
    echo -e "${GREEN}✅ Documentation structure ready${NC}"
fi
echo ""

# Create PROJECT_PLAN.md
echo -e "${BLUE}[4/6]${NC} Creating PROJECT_PLAN.md..."

if [ -f "docs/notes/PROJECT_PLAN.md" ]; then
    echo "   PROJECT_PLAN.md already exists (skipping)"
else
    echo ""
    echo "   Quick objective questions (press Enter to skip):"
    echo ""
    read -p "   What problem does this solve? " PROBLEM
    read -p "   Who are the users? " USERS
    read -p "   What's the solution? " SOLUTION

    if [ -z "$PROBLEM" ]; then PROBLEM="[Define the problem this project solves]"; fi
    if [ -z "$USERS" ]; then USERS="[Define target users]"; fi
    if [ -z "$SOLUTION" ]; then SOLUTION="[Describe your solution]"; fi

    cat > docs/notes/PROJECT_PLAN.md <<EOF
# Project Plan - $PROJECT_NAME

> **Created**: $(date +%Y-%m-%d)
> **Status**: $([ "$MODE" = "LIGHT" ] && echo "Production" || echo "Development")
> **Clarity Score**: To be refined

---

## 🎯 Project Objective

### Problem
$PROBLEM

### Target Users
$USERS

### Solution
$SOLUTION

### Success Metrics
- [Add measurable success metrics]
- [e.g., "Users save 50% time on task X"]
- [e.g., "99.9% uptime maintained"]

### Constraints
- $([ "$MODE" = "LIGHT" ] && echo "Production system - changes must be non-breaking" || echo "Development system - can refactor freely")
- [Add technical constraints]
- [Add resource constraints]

---

## 📊 Current Status

**What's Working Well**:
- [List what's working]

**What Needs Improvement**:
- [List areas for improvement]

**Recent Changes**:
- $(date +%Y-%m-%d): Retrofitted with best-practice structure ($MODE_NAME)

---

## 🗺️ Roadmap

### Current Focus
- [Current sprint/milestone]

### Next Steps
- [Upcoming work]

### Future Plans
- [Long-term vision]

---

## 📋 Notes

**Retrofit Applied**: $MODE_NAME
- Documentation organized into docs/
- Project standards documented
$([ "$MODE" = "FULL" ] && echo "- Quality gates configured
- Test structure created")

**Next Actions**:
1. Review and enhance this objective
2. Define specific success metrics
3. Update current status regularly
$([ "$MODE" = "FULL" ] && echo "4. Implement tests in tests/
5. Run quality gate: .ai-validation/check_quality.sh")

---

**Last Updated**: $(date +%Y-%m-%d)
EOF

    echo -e "${GREEN}✅ PROJECT_PLAN.md created${NC}"
fi
echo ""

# Add CLAUDE.md and other files
echo -e "${BLUE}[5/6]${NC} Adding project standards..."

if [ ! -f "CLAUDE.md" ]; then
    cp "$TOOLKIT_DIR/CLAUDE.md" CLAUDE.md
    # Customize for project
    sed -i "s/Best Practice Toolkit/$PROJECT_NAME/g" CLAUDE.md
    echo -e "${GREEN}✅ CLAUDE.md created${NC}"
else
    echo "   CLAUDE.md already exists (skipping)"
fi

if [ "$MODE" = "FULL" ]; then
    # Quality gate
    if [ ! -f ".ai-validation/check_quality.sh" ]; then
        cp "$TOOLKIT_DIR/.ai-validation/check_quality.sh" .ai-validation/
        chmod +x .ai-validation/check_quality.sh
        echo -e "${GREEN}✅ Quality gate added${NC}"
    fi

    # .gitignore
    if [ ! -f ".gitignore" ]; then
        cp "$TOOLKIT_DIR/.gitignore" .gitignore
        echo -e "${GREEN}✅ .gitignore created${NC}"
    fi

    # Test structure
    if [ ! -f "tests/conftest.py" ]; then
        cp "$TOOLKIT_DIR/tests/conftest.py" tests/
        cat > tests/test_basic.py <<'EOF'
"""
Basic tests.
"""
import pytest


class TestBasic:
    """Basic test suite."""

    def test_placeholder(self):
        """Placeholder test - replace with real tests."""
        assert True
EOF
        cat > tests/README.md <<EOF
# Tests

## Running Tests

\`\`\`bash
pytest tests/ -v
\`\`\`

## Adding Tests

Add test files following the pattern:
- \`test_*.py\` - Test modules
- \`class Test*\` - Test classes
- \`def test_*()\` - Test functions

See conftest.py for available fixtures.
EOF
        echo -e "${GREEN}✅ Test structure created${NC}"
    fi
fi

# Create simple README if missing
if [ ! -f "README.md" ]; then
    cat > README.md <<EOF
# $PROJECT_NAME

> [Brief project description]

## Quick Start

[Add installation/usage instructions]

## Documentation

- [Project Plan](docs/notes/PROJECT_PLAN.md) - Objectives and roadmap
- [Standards](CLAUDE.md) - Development standards
- [Full Documentation](docs/) - Complete docs

## Status

**Environment**: $([ "$MODE" = "LIGHT" ] && echo "Production" || echo "Development")

---

Last updated: $(date +%Y-%m-%d)
EOF
    echo -e "${GREEN}✅ README.md created${NC}"
fi

echo ""

# Install MCP servers
echo -e "${BLUE}[6/7]${NC} Installing MCP servers..."
TOOLKIT_DIR="/home/jc/CascadeProjects/best-practice"
if [ -d "$TOOLKIT_DIR/mcp-servers" ]; then
    mkdir -p mcp-servers
    cp -r "$TOOLKIT_DIR/mcp-servers/"* mcp-servers/
    echo -e "${GREEN}✅ MCP servers installed${NC}"
    echo "   - memory_mcp.py (Context persistence)"
    echo "   - quality_mcp.py (Quality enforcement)"
    echo "   - project_mcp.py (Objective clarification)"
    echo "   - learning_mcp.py (Self-learning + code review)"
else
    echo -e "${YELLOW}⚠️  MCP servers not found at $TOOLKIT_DIR${NC}"
fi

echo ""

# Commit changes
echo -e "${BLUE}[7/7]${NC} Committing changes..."
echo ""

git add -A

echo "Changes to be committed:"
git status --short | head -20
if [ "$(git status --short | wc -l)" -gt 20 ]; then
    echo "   ... and $(($(git status --short | wc -l) - 20)) more files"
fi
echo ""

git commit -m "feat: retrofit with best-practice structure ($MODE_NAME)

Applied $([ "$MODE" = "LIGHT" ] && echo "light touch retrofit (production safe)" || echo "full best-practice implementation"):

Structure:
- Organized documentation into docs/ subdirectories
- Created PROJECT_PLAN.md with objective
- Added CLAUDE.md project standards
- Installed MCP servers (memory, quality, project, learning)
$([ "$MODE" = "FULL" ] && echo "- Added quality gate (.ai-validation/)
- Created test structure (tests/)
- Added .gitignore")

Mode: $MODE_NAME
Reason: $([ "$MODE" = "LIGHT" ] && echo "Production system - minimal disruption" || echo "Development system - full implementation")

Can rollback with: git reset --hard retrofit-start

🤖 Generated with [Claude Code](https://claude.com/claude-code)

Co-Authored-By: Claude <noreply@anthropic.com>"

git tag retrofit-complete

echo -e "${GREEN}✅ Changes committed and tagged${NC}"
echo ""

# Restore stashed changes if any
if [ "$STASHED" = true ]; then
    echo "Restoring stashed changes..."
    git stash pop
    echo ""
fi

# Validation checklist
echo ""
echo -e "${BLUE}Validating installation...${NC}"
echo ""

validation_errors=0

# Check CLAUDE.md
if [ -f "CLAUDE.md" ]; then
    echo -e "${GREEN}✅${NC} CLAUDE.md (Project standards)"
else
    echo -e "${RED}❌${NC} CLAUDE.md missing"
    ((validation_errors++))
fi

# Check PROJECT_PLAN.md
if [ -f "docs/notes/PROJECT_PLAN.md" ]; then
    echo -e "${GREEN}✅${NC} PROJECT_PLAN.md (Project objective)"
else
    echo -e "${RED}❌${NC} PROJECT_PLAN.md missing"
    ((validation_errors++))
fi

# Check docs structure
if [ -d "docs/notes" ]; then
    echo -e "${GREEN}✅${NC} docs/notes/ directory"
else
    echo -e "${RED}❌${NC} docs/notes/ directory missing"
    ((validation_errors++))
fi

# Check MCP servers
if [ -d "mcp-servers" ]; then
    echo -e "${GREEN}✅${NC} mcp-servers/ directory"

    # Check individual MCPs
    for mcp in memory_mcp.py quality_mcp.py project_mcp.py learning_mcp.py; do
        if [ -f "mcp-servers/$mcp" ]; then
            echo -e "${GREEN}   ✅${NC} $mcp"
        else
            echo -e "${RED}   ❌${NC} $mcp missing"
            ((validation_errors++))
        fi
    done
else
    echo -e "${RED}❌${NC} mcp-servers/ directory missing"
    ((validation_errors++))
fi

# Check full mode components
if [ "$MODE" = "FULL" ]; then
    # Check quality gate
    if [ -f ".ai-validation/check_quality.sh" ]; then
        echo -e "${GREEN}✅${NC} .ai-validation/check_quality.sh"
    else
        echo -e "${RED}❌${NC} Quality gate missing"
        ((validation_errors++))
    fi

    # Check tests directory
    if [ -d "tests" ]; then
        echo -e "${GREEN}✅${NC} tests/ directory"
    else
        echo -e "${RED}❌${NC} tests/ directory missing"
        ((validation_errors++))
    fi

    # Check .gitignore
    if [ -f ".gitignore" ]; then
        echo -e "${GREEN}✅${NC} .gitignore"
    else
        echo -e "${RED}❌${NC} .gitignore missing"
        ((validation_errors++))
    fi
fi

echo ""
if [ $validation_errors -eq 0 ]; then
    echo -e "${GREEN}${BOLD}All components installed successfully!${NC}"
else
    echo -e "${RED}${BOLD}⚠️  $validation_errors component(s) missing${NC}"
    echo "   Please check the installation"
fi

# Summary
echo ""
echo -e "${BOLD}${GREEN}"
echo "╔════════════════════════════════════════════════════════╗"
echo "║                                                        ║"
echo "║              ✅  Retrofit Complete!                    ║"
echo "║                                                        ║"
echo "╚════════════════════════════════════════════════════════╝"
echo -e "${NC}"
echo ""

echo -e "${BOLD}What Changed:${NC}"
echo ""
echo "  📁 Structure:"
echo "     • docs/ - All documentation organized"
echo "     • docs/notes/PROJECT_PLAN.md - Your objective"
echo "     • CLAUDE.md - Project standards"

if [ "$MODE" = "FULL" ]; then
    echo "     • .ai-validation/ - Quality gate"
    echo "     • tests/ - Test structure"
    echo "     • .gitignore - Git ignores"
fi

echo ""
echo -e "${BOLD}Git Tags:${NC}"
echo "  • retrofit-start - Before changes (rollback point)"
echo "  • retrofit-complete - After changes (current)"
echo ""
echo -e "${BOLD}Next Steps:${NC}"
echo ""
echo "  1. Review: docs/notes/PROJECT_PLAN.md"
echo "  2. Customize: CLAUDE.md for your project"

if [ "$MODE" = "LIGHT" ]; then
    echo "  3. ${YELLOW}Production Safe:${NC} Changes are minimal, non-breaking"
    echo "  4. ${YELLOW}Optional:${NC} Add quality tools when ready:"
    echo "     Run again and choose 'No' to production question"
else
    echo "  3. Run quality gate: .ai-validation/check_quality.sh"
    echo "  4. Add real tests in: tests/"
    echo "  5. Start building with best practices! 🚀"
fi

echo ""
echo -e "${BOLD}Rollback:${NC}"
echo "  git reset --hard retrofit-start"
echo "  git tag -d retrofit-complete"
echo ""
echo -e "${GREEN}Done! Your project now follows best practices.${NC}"
echo ""
