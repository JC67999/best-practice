#!/bin/bash

# Interactive Retrofit Script
# Applies best practices to an existing project

set -e

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

echo -e "${BLUE}════════════════════════════════════════════════════════${NC}"
echo -e "${BLUE}    Best Practice Retrofit - Interactive Mode${NC}"
echo -e "${BLUE}════════════════════════════════════════════════════════${NC}"
echo ""

# Check if we're in a project directory
if [ ! -d ".git" ]; then
    echo -e "${YELLOW}⚠️  Warning: Not a git repository${NC}"
    echo "It's recommended to run this in a git repository for safety."
    read -p "Continue anyway? (y/N): " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        exit 1
    fi
fi

PROJECT_DIR=$(pwd)
TOOLKIT_DIR="/home/jc/CascadeProjects/best-practice"

echo -e "${GREEN}📁 Project Directory:${NC} $PROJECT_DIR"
echo ""

# Step 1: Safety Checkpoint
echo -e "${BLUE}Step 1: Safety Checkpoint${NC}"
echo "Creating a safety checkpoint so you can rollback if needed..."
echo ""

if [ -d ".git" ]; then
    # Check for uncommitted changes
    if ! git diff-index --quiet HEAD -- 2>/dev/null; then
        echo -e "${YELLOW}⚠️  You have uncommitted changes${NC}"
        echo "It's recommended to commit or stash them first."
        read -p "Continue anyway? (y/N): " -n 1 -r
        echo
        if [[ ! $REPLY =~ ^[Yy]$ ]]; then
            exit 1
        fi
    fi

    # Create safety tag
    echo "Creating safety tag 'retrofit-start'..."
    git tag -f retrofit-start
    echo -e "${GREEN}✅ Safety checkpoint created${NC}"
    echo "You can rollback with: git reset --hard retrofit-start"
else
    echo -e "${YELLOW}⚠️  No git repository - creating one${NC}"
    git init
    git add .
    git commit -m "Initial commit before retrofit"
    git tag retrofit-start
    echo -e "${GREEN}✅ Git repository initialized${NC}"
fi
echo ""

# Step 2: Assessment
echo -e "${BLUE}Step 2: Project Assessment${NC}"
echo "Analyzing your project structure..."
echo ""

python3 "$TOOLKIT_DIR/retrofit-tools/retrofit_assess.py" "$PROJECT_DIR" > /tmp/retrofit_assessment.txt
cat /tmp/retrofit_assessment.txt
echo ""

read -p "Press Enter to continue..."
echo ""

# Step 3: Choose Mode
echo -e "${BLUE}Step 3: Choose Retrofit Mode${NC}"
echo ""
echo "1) Light    - Minimal changes (docs organization only, ~10 min)"
echo "2) Standard - Recommended (+ quality tools, ~30 min)"
echo "3) Full     - Complete retrofit (+ tests, MCP setup, ~60 min)"
echo ""
read -p "Choose mode (1-3): " -n 1 -r MODE
echo ""

# Step 4: Extract/Clarify Objective
echo ""
echo -e "${BLUE}Step 4: Project Objective${NC}"
echo ""

if [ -f "docs/notes/PROJECT_PLAN.md" ]; then
    echo "Found existing PROJECT_PLAN.md"
    read -p "Keep existing objective? (Y/n): " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Nn]$ ]]; then
        CLARIFY_OBJECTIVE=true
    else
        CLARIFY_OBJECTIVE=false
    fi
else
    echo "No PROJECT_PLAN.md found."
    echo ""
    echo "Option A: Extract from existing docs (auto-detect)"
    echo "Option B: Interactive clarification (10-15 questions)"
    echo ""
    read -p "Choose (A/B): " -n 1 -r
    echo

    if [[ $REPLY =~ ^[Bb]$ ]]; then
        CLARIFY_OBJECTIVE=true
    else
        echo "Attempting to extract objective from existing documentation..."
        python3 "$TOOLKIT_DIR/retrofit-tools/retrofit_extract_objective.py" "$PROJECT_DIR"
        CLARIFY_OBJECTIVE=false
    fi
fi

if [ "$CLARIFY_OBJECTIVE" = true ]; then
    echo ""
    echo -e "${GREEN}Let's clarify your project objective...${NC}"
    echo ""

    # Simple interactive questions
    read -p "What problem does this project solve? " PROBLEM
    read -p "Who are the target users? " TARGET_USERS
    read -p "What is your solution? " SOLUTION
    read -p "What does success look like? (metric) " SUCCESS_METRIC

    # Create docs/notes directory
    mkdir -p docs/notes

    # Create basic PROJECT_PLAN.md
    cat > docs/notes/PROJECT_PLAN.md <<EOF
# Project Plan

> **Last Updated**: $(date +%Y-%m-%d)
> **Status**: In Development

## 🎯 Project Objective

### Problem
$PROBLEM

### Target Users
$TARGET_USERS

### Solution
$SOLUTION

### Success Metrics
- $SUCCESS_METRIC

### Constraints
- (Add your constraints here)

---

## 📊 Current Status

**Phase**: Development

**What's Working**:
- (Add what's working)

**What Needs Work**:
- (Add what needs improvement)

---

## 🗺️ Roadmap

### Phase 1: Current
- (Add current tasks)

### Phase 2: Next
- (Add upcoming tasks)

---

**Created**: $(date +%Y-%m-%d)
**Objective Clarity**: To be scored after full clarification
EOF

    echo -e "${GREEN}✅ Created basic PROJECT_PLAN.md${NC}"
    echo "You can enhance it later with full clarification."
fi

echo ""

# Step 5: Structure Migration
echo -e "${BLUE}Step 5: Structure Migration${NC}"
echo "Organizing files into best-practice structure..."
echo ""

# Create directory structure
mkdir -p docs/design
mkdir -p docs/guides
mkdir -p docs/analysis
mkdir -p docs/references
mkdir -p docs/notes
mkdir -p tests
mkdir -p .ai-validation

echo -e "${GREEN}✅ Created directory structure${NC}"

# Move documentation files
echo "Moving documentation files to docs/..."

# Find and move markdown files (except README.md and CLAUDE.md)
for file in *.md; do
    if [ -f "$file" ] && [ "$file" != "README.md" ] && [ "$file" != "CLAUDE.md" ]; then
        # Determine subdirectory based on name
        if [[ $file =~ DESIGN|ARCHITECTURE|IMPLEMENTATION ]]; then
            git mv "$file" docs/design/ 2>/dev/null || mv "$file" docs/design/
        elif [[ $file =~ GUIDE|METHODOLOGY|ROADMAP|SETUP ]]; then
            git mv "$file" docs/guides/ 2>/dev/null || mv "$file" docs/guides/
        elif [[ $file =~ ANALYSIS|SUMMARY|ASSESSMENT ]]; then
            git mv "$file" docs/analysis/ 2>/dev/null || mv "$file" docs/analysis/
        else
            git mv "$file" docs/ 2>/dev/null || mv "$file" docs/
        fi
        echo "  Moved: $file"
    fi
done

echo -e "${GREEN}✅ Documentation organized${NC}"
echo ""

# Step 6: Add Standards (if Standard or Full mode)
if [ "$MODE" = "2" ] || [ "$MODE" = "3" ]; then
    echo -e "${BLUE}Step 6: Adding Project Standards${NC}"

    # Copy CLAUDE.md template
    if [ ! -f "CLAUDE.md" ]; then
        cp "$TOOLKIT_DIR/CLAUDE.md" CLAUDE.md
        echo "Edit CLAUDE.md to customize for your project"
        echo -e "${GREEN}✅ Created CLAUDE.md${NC}"
    else
        echo "CLAUDE.md already exists (skipping)"
    fi

    # Copy quality gate
    if [ ! -f ".ai-validation/check_quality.sh" ]; then
        cp "$TOOLKIT_DIR/.ai-validation/check_quality.sh" .ai-validation/
        chmod +x .ai-validation/check_quality.sh
        echo -e "${GREEN}✅ Added quality gate script${NC}"
    else
        echo "Quality gate already exists (skipping)"
    fi

    # Create .gitignore if needed
    if [ ! -f ".gitignore" ]; then
        cp "$TOOLKIT_DIR/.gitignore" .gitignore
        echo -e "${GREEN}✅ Created .gitignore${NC}"
    fi

    echo ""
fi

# Step 7: Test Setup (if Full mode)
if [ "$MODE" = "3" ]; then
    echo -e "${BLUE}Step 7: Test Setup${NC}"

    # Copy test templates
    if [ ! -f "tests/conftest.py" ]; then
        cp "$TOOLKIT_DIR/tests/conftest.py" tests/
        echo -e "${GREEN}✅ Created test configuration${NC}"
    fi

    # Create basic test file
    if [ ! -f "tests/test_basic.py" ]; then
        cat > tests/test_basic.py <<'EOF'
"""
Basic tests for project.
"""
import pytest


class TestBasic:
    """Basic test suite."""

    def test_placeholder(self):
        """Placeholder test."""
        assert True

    # TODO: Add your tests here
EOF
        echo -e "${GREEN}✅ Created test template${NC}"
    fi

    echo ""
fi

# Step 8: Create simple README if needed
if [ ! -f "README.md" ]; then
    PROJECT_NAME=$(basename "$PROJECT_DIR")
    cat > README.md <<EOF
# $PROJECT_NAME

> Brief project description here

## Quick Start

(Add installation/usage instructions)

## Documentation

See [docs/](docs/) for complete documentation:
- [Project Plan](docs/notes/PROJECT_PLAN.md) - Objectives and roadmap
- [Standards](CLAUDE.md) - Project standards and guidelines

## Status

(Add current status)

---

**Last Updated**: $(date +%Y-%m-%d)
EOF
    echo -e "${GREEN}✅ Created README.md${NC}"
fi

# Step 9: Commit
echo ""
echo -e "${BLUE}Step 9: Commit Changes${NC}"
echo ""

git add -A
git status

echo ""
read -p "Commit these changes? (Y/n): " -n 1 -r
echo

if [[ ! $REPLY =~ ^[Nn]$ ]]; then
    git commit -m "feat: retrofit project with best-practice structure

Applied best-practice toolkit:
- Organized documentation into docs/ structure
- Created PROJECT_PLAN.md with objective
- Added project standards (CLAUDE.md)
- Added quality gate (.ai-validation/)
- Created test structure

Mode: $([ "$MODE" = "1" ] && echo "Light" || [ "$MODE" = "2" ] && echo "Standard" || echo "Full")

🤖 Generated with [Claude Code](https://claude.com/claude-code)

Co-Authored-By: Claude <noreply@anthropic.com>"

    git tag retrofit-complete

    echo ""
    echo -e "${GREEN}✅ Changes committed and tagged${NC}"
else
    echo ""
    echo -e "${YELLOW}Skipped commit - you can commit manually later${NC}"
fi

echo ""
echo -e "${BLUE}════════════════════════════════════════════════════════${NC}"
echo -e "${GREEN}✅ Retrofit Complete!${NC}"
echo -e "${BLUE}════════════════════════════════════════════════════════${NC}"
echo ""
echo "Next steps:"
echo "1. Review docs/notes/PROJECT_PLAN.md and enhance if needed"
echo "2. Customize CLAUDE.md for your project"
echo "3. Run quality gate: .ai-validation/check_quality.sh"
if [ "$MODE" = "3" ]; then
    echo "4. Implement tests in tests/ directory"
fi
echo ""
echo "To rollback: git reset --hard retrofit-start"
echo ""
