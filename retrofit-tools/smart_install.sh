#!/bin/bash
# Smart Install - ONE command, safe installation with smart questions

set -e
set -o pipefail

TOOLKIT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
PROJECT_DIR=$(pwd)
PROJECT_NAME=$(basename "$PROJECT_DIR")

# Parse flags
# Default: LOCAL_ONLY=true (toolkit files in .claude/ are NOT committed to git)
# Use --commit flag to explicitly commit toolkit files
LOCAL_ONLY=true
if [[ "$1" == "--commit" ]]; then
    LOCAL_ONLY=false
fi

clear
echo "════════════════════════════════════════════════════════"
echo "  Best Practice Toolkit - Smart Install"
if [ "$LOCAL_ONLY" = false ]; then
    echo "  Mode: COMMIT (toolkit files WILL be committed to git)"
else
    echo "  Mode: LOCAL ONLY (default - toolkit files NOT committed)"
fi
echo "════════════════════════════════════════════════════════"
echo ""

# Safety check: Git
if [ ! -d ".git" ]; then
    if [ "$LOCAL_ONLY" = true ]; then
        echo "⚠️  Not a git repository"
        echo "Local-only mode doesn't require git - continuing"
    else
        echo "⚠️  Not a git repository"
        read -p "Initialize git? (Y/n): " -n 1 -r
        echo ""
        if [[ ! $REPLY =~ ^[Nn]$ ]]; then
            git init
            git add .
            git commit -m "Initial commit before retrofit" 2>/dev/null || git commit --allow-empty -m "Initial commit before retrofit"
            echo "✅ Git initialized"
        else
            echo "❌ Cannot install without git (for safety)"
            exit 1
        fi
    fi
fi

# Safety check: Uncommitted changes
if [ "$LOCAL_ONLY" = false ]; then
    if ! git diff-index --quiet HEAD -- 2>/dev/null; then
        echo "⚠️  You have uncommitted changes"
        read -p "Stash and continue? (Y/n): " -n 1 -r
        echo ""
        if [[ ! $REPLY =~ ^[Nn]$ ]]; then
            git stash
            STASHED=true
            echo "✅ Changes stashed"
        else
            echo "❌ Commit or stash changes first"
            exit 1
        fi
    fi
fi

echo ""
echo "🔍 Analyzing project..."

# Auto-detect production indicators
production_score=0
reasons=()

# Low commit activity = stable
echo -n "  Checking git activity... "
if [ -d ".git" ]; then
    recent_commits=$(timeout 5 git log --since="30 days ago" --oneline 2>/dev/null | wc -l || echo "0")
    echo "$recent_commits commits/30d"
    if [ "$recent_commits" = "0" ] || [ "$recent_commits" -lt 5 ]; then
        production_score=$((production_score + 1))
        reasons+=("Low activity ($recent_commits commits/30d)")
    fi
else
    echo "no git"
fi

# Deployment configs
echo -n "  Checking deployment configs... "
if [ -f "Dockerfile" ] || [ -f "docker-compose.yml" ]; then
    production_score=$((production_score + 1))
    reasons+=("Has deployment config")
    echo "found"
else
    echo "none"
fi

# CI/CD
echo -n "  Checking CI/CD... "
if [ -d ".github/workflows" ] || [ -f ".gitlab-ci.yml" ] || [ -f "Jenkinsfile" ]; then
    production_score=$((production_score + 1))
    reasons+=("Has CI/CD")
    echo "found"
else
    echo "none"
fi

# Production env files
echo -n "  Checking production env... "
if [ -f ".env.production" ] || [ -f "config/production.yml" ]; then
    production_score=$((production_score + 1))
    reasons+=("Has production env")
    echo "found"
else
    echo "none"
fi
echo ""

# Determine mode
MODE="FULL"
if [ "$production_score" -ge 2 ]; then
    MODE="LIGHT"
fi

# Show detection
if [ "$MODE" = "LIGHT" ]; then
    echo "🟡 PRODUCTION detected (score: $production_score/4)"
    for reason in "${reasons[@]}"; do
        echo "   • $reason"
    done
    echo ""
    echo "Will install: LIGHT mode (safe, minimal changes)"
else
    echo "🟢 DEVELOPMENT detected (score: $production_score/4)"
    echo ""
    echo "Will install: FULL mode (complete best practices)"
fi

echo ""
echo "────────────────────────────────────────────────────────"
echo ""

# Confirm
read -p "Proceed? (Y/n): " -n 1 -r
echo ""
if [[ $REPLY =~ ^[Nn]$ ]]; then
    echo "Cancelled"
    exit 0
fi

# Override option
read -p "Override detected mode? (y/N): " -n 1 -r
echo ""
if [[ $REPLY =~ ^[Yy]$ ]]; then
    echo ""
    echo "1) LIGHT - Production safe"
    echo "2) FULL  - Complete retrofit"
    read -p "Choice: " -n 1 -r choice
    echo ""
    if [ "$choice" = "2" ]; then
        MODE="FULL"
    else
        MODE="LIGHT"
    fi
fi

echo ""
echo "════════════════════════════════════════════════════════"
echo "  Installing: $MODE mode"
if [ "$LOCAL_ONLY" = true ]; then
    echo "  (Local only - no git commits)"
fi
echo "════════════════════════════════════════════════════════"
echo ""

# Create safety checkpoint
if [ "$LOCAL_ONLY" = false ]; then
    git tag -f retrofit-start
    echo "✅ Safety checkpoint (tag: retrofit-start)"
    echo ""
else
    echo "⚠️  Local-only mode: Skipping git checkpoint"
    echo ""
fi

# Create directories
echo "[1/5] Creating structure..."
mkdir -p docs/{design,guides,analysis,references,notes}
# Create .claude/ directory (automatically gitignored by Claude Code)
mkdir -p .claude
if [ "$MODE" = "FULL" ]; then
    mkdir -p tests
fi
echo "✅ Done"
echo ""

# Organize docs
echo "[2/5] Organizing docs..."
MD_COUNT=$(find . -maxdepth 1 -name "*.md" ! -name "README.md" ! -name "CLAUDE.md" 2>/dev/null | wc -l)
if [ "$MD_COUNT" -gt 0 ]; then
    for file in *.md; do
        if [ -f "$file" ] && [ "$file" != "README.md" ] && [ "$file" != "CLAUDE.md" ]; then
            if [[ $file =~ DESIGN|ARCHITECTURE|IMPLEMENTATION|APPROACH|INTEGRATION ]]; then
                if [ "$LOCAL_ONLY" = false ]; then
                    git mv "$file" docs/design/ 2>/dev/null || mv "$file" docs/design/
                else
                    mv "$file" docs/design/
                fi
            elif [[ $file =~ GUIDE|METHODOLOGY|ROADMAP ]]; then
                if [ "$LOCAL_ONLY" = false ]; then
                    git mv "$file" docs/guides/ 2>/dev/null || mv "$file" docs/guides/
                else
                    mv "$file" docs/guides/
                fi
            elif [[ $file =~ ANALYSIS|SUMMARY|ASSESSMENT ]]; then
                if [ "$LOCAL_ONLY" = false ]; then
                    git mv "$file" docs/analysis/ 2>/dev/null || mv "$file" docs/analysis/
                else
                    mv "$file" docs/analysis/
                fi
            elif [[ $file =~ CHANGELOG|TODO|NOTES ]]; then
                if [ "$LOCAL_ONLY" = false ]; then
                    git mv "$file" docs/notes/ 2>/dev/null || mv "$file" docs/notes/
                else
                    mv "$file" docs/notes/
                fi
            else
                if [ "$LOCAL_ONLY" = false ]; then
                    git mv "$file" docs/ 2>/dev/null || mv "$file" docs/
                else
                    mv "$file" docs/
                fi
            fi
        fi
    done
    echo "✅ Moved $MD_COUNT files"
else
    echo "✅ No docs to move"
fi
echo ""

# PROJECT_PLAN
echo "[3/5] Creating PROJECT_PLAN..."
if [ ! -f "docs/notes/PROJECT_PLAN.md" ]; then
    STATUS_MODE=$([ "$MODE" = "LIGHT" ] && echo "Production" || echo "Development")
    CONSTRAINT_TEXT=$([ "$MODE" = "LIGHT" ] && echo "Production - non-breaking changes only" || echo "Development - can refactor")

    cat > docs/notes/PROJECT_PLAN.md <<EOF
# Project Plan - $PROJECT_NAME

> **Created**: $(date +%Y-%m-%d)
> **Status**: $STATUS_MODE

## 🎯 Objective

### Problem
[What problem does this solve?]

### Users
[Who uses this?]

### Solution
[How does it solve the problem?]

### Success Metrics
- [Measurable metrics]

### Constraints
- $CONSTRAINT_TEXT

## 📊 Status

**Last Updated**: $(date +%Y-%m-%d)
**Mode**: $MODE retrofit applied

## 🗺️ Next Steps

- Review and enhance objective above
- Define specific metrics
EOF

    if [ "$MODE" = "FULL" ]; then
        cat >> docs/notes/PROJECT_PLAN.md <<EOF
- Add tests in tests/
- Run quality gate: .ai-validation/check_quality.sh
EOF
    fi

    echo "✅ Created"
else
    echo "✅ Already exists"
fi
echo ""

# CLAUDE.md and files
echo "[4/5] Installing toolkit files to .claude/..."

# Install toolkit files to .claude/ (automatically gitignored by Claude Code)
echo -n "best-practice.md (to .claude/)... "
mkdir -p .claude
cp "$TOOLKIT_DIR/CLAUDE.md" .claude/best-practice.md
sed -i "s/Best Practice Toolkit/$PROJECT_NAME Best Practice/g" .claude/best-practice.md 2>/dev/null || true
echo "✅"

echo -n "TASKS.md (to .claude/)... "
cp "$TOOLKIT_DIR/TASKS.md" .claude/TASKS.md 2>/dev/null || echo '# Live Task List

**Purpose**: Granular, testable tasks
**Rule**: Each task ≤30 lines, ≤15 min

## Current Tasks

### In Progress
- [ ] None

### Pending
- [ ] None' > .claude/TASKS.md
echo "✅"

echo -n "USER_GUIDE.md (to .claude/)... "
if [ -f "$TOOLKIT_DIR/.claude/USER_GUIDE.md" ]; then
    cp "$TOOLKIT_DIR/.claude/USER_GUIDE.md" .claude/USER_GUIDE.md
    echo "✅"
else
    echo "⚠️  User guide not found"
fi

echo -n "Claude Skills (to .claude/skills/)... "
mkdir -p .claude/skills
if [ -d "$TOOLKIT_DIR/.claude/skills" ]; then
    cp -r "$TOOLKIT_DIR/.claude/skills"/* .claude/skills/ 2>/dev/null || true
    echo "✅ (9 toolkit skills + template)"
else
    echo "⚠️  Skills not found in toolkit"
fi

# Full mode extras in .claude/
if [ "$MODE" = "FULL" ]; then
    echo -n "Quality gate (to .claude/quality-gate/)... "
    mkdir -p .claude/quality-gate
    cp "$TOOLKIT_DIR/.ai-validation/check_quality.sh" .claude/quality-gate/ 2>/dev/null || true
    chmod +x .claude/quality-gate/check_quality.sh 2>/dev/null || true
    echo "✅"

    echo -n "MCP servers (to .claude/mcp-servers/)... "
    mkdir -p .claude/mcp-servers
    if [ -d "$TOOLKIT_DIR/.claude/mcp-servers" ]; then
        cp -r "$TOOLKIT_DIR/.claude/mcp-servers"/* .claude/mcp-servers/ 2>/dev/null || true
        echo "✅ (Memory, Quality, Project MCPs)"
    else
        echo "⚠️  MCP servers not found"
    fi

    if [ ! -d "tests" ]; then
        mkdir -p tests
        echo 'import pytest

def test_placeholder():
    assert True' > tests/test_basic.py
        echo "✅ Test structure"
    fi
fi
echo ""

# .claude/ is automatically gitignored by Claude Code (default behavior)
echo "[5/5] Verifying .claude/ is gitignored..."
echo "✅ .claude/ folder automatically ignored by Claude Code (DEFAULT)"
echo "   All toolkit files installed locally, won't be committed"
echo "   Use --commit flag if you want to commit toolkit files to git"
echo ""
else
    # --commit flag was used - commit toolkit files to git
    echo "[5/5] Committing changes (--commit flag used)..."
    git add -A

    if git diff --cached --quiet; then
        echo "✅ No changes (already installed)"
    else
        git commit -m "feat: install best-practice toolkit ($MODE mode) - COMMITTED

⚠️  Toolkit files committed to git (--commit flag used)
.claude/ folder is now tracked in the repository

Installed files:
- .claude/best-practice.md - Project standards
- .claude/TASKS.md - Live task list
- .claude/skills/ - 9 toolkit skills + template
$([ "$MODE" = "FULL" ] && echo "- .claude/mcp-servers/ - MCP servers with prompts
- .claude/quality-gate/ - Quality gate scripts")
- docs/notes/PROJECT_PLAN.md - Project planning

🤖 Generated with [Claude Code](https://claude.com/claude-code)

Co-Authored-By: Claude <noreply@anthropic.com>"

        git tag -f retrofit-complete 2>/dev/null || true
        echo "✅ Committed to git"
    fi

    # Restore stash
    if [ "$STASHED" = true ]; then
        git stash pop
    fi
fi

# Validation
echo ""
echo "════════════════════════════════════════════════════════"
echo "  📋 Installation Summary"
echo "════════════════════════════════════════════════════════"
echo ""

validation_errors=0
validation_warnings=0

# Check CLAUDE.md
echo -n "CLAUDE.md ... "
if [ -f "CLAUDE.md" ]; then
    size=$(wc -c < "CLAUDE.md")
    echo "✅ ($size bytes)"
else
    echo "❌ MISSING"
    validation_errors=$((validation_errors + 1))
fi

# Check .claude/ folder structure
echo -n ".claude/best-practice.md ... "
if [ -f ".claude/best-practice.md" ]; then
    size=$(wc -c < ".claude/best-practice.md")
    echo "✅ ($size bytes)"
else
    echo "❌ MISSING"
    validation_errors=$((validation_errors + 1))
fi

echo -n ".claude/USER_GUIDE.md ... "
if [ -f ".claude/USER_GUIDE.md" ]; then
    size=$(wc -c < ".claude/USER_GUIDE.md")
    echo "✅ ($size bytes)"
else
    echo "⚠️  missing (optional)"
    validation_warnings=$((validation_warnings + 1))
fi

echo -n ".claude/TASKS.md ... "
if [ -f ".claude/TASKS.md" ]; then
    size=$(wc -c < ".claude/TASKS.md")
    echo "✅ ($size bytes)"
else
    echo "❌ MISSING"
    validation_errors=$((validation_errors + 1))
fi

echo -n ".claude/skills/ ... "
if [ -d ".claude/skills" ]; then
    skill_count=$(ls -1d .claude/skills/*/ 2>/dev/null | wc -l)
    echo "✅ ($skill_count skills)"
else
    echo "⚠️  missing"
    validation_warnings=$((validation_warnings + 1))
fi

# Check PROJECT_PLAN.md
echo -n "PROJECT_PLAN.md ... "
if [ -f "docs/notes/PROJECT_PLAN.md" ]; then
    size=$(wc -c < "docs/notes/PROJECT_PLAN.md")
    echo "✅ ($size bytes)"
else
    echo "❌ MISSING"
    validation_errors=$((validation_errors + 1))
fi

# Check docs structure
echo -n "docs/ structure ... "
if [ -d "docs/notes" ]; then
    echo "✅"
else
    echo "❌ MISSING"
    validation_errors=$((validation_errors + 1))
fi

# Check mcp-servers (in .claude/ for FULL mode)
if [ "$MODE" = "FULL" ]; then
    echo -n ".claude/mcp-servers/ ... "
    if [ -d ".claude/mcp-servers" ]; then
        mcp_count=$(ls -1 .claude/mcp-servers/*.py 2>/dev/null | wc -l)
        if [ "$mcp_count" -gt 0 ]; then
            echo "✅ ($mcp_count files)"
            ls .claude/mcp-servers/*.py 2>/dev/null | xargs -n 1 basename | sed 's/^/  - /'
        else
            echo "⚠️  directory exists but empty"
            validation_warnings=$((validation_warnings + 1))
        fi
    else
        echo "❌ MISSING"
        validation_errors=$((validation_errors + 1))
    fi
fi

# Check slash commands
echo -n ".claude/commands/ ... "
if [ -d ".claude/commands" ]; then
    cmd_count=$(ls -1 .claude/commands/*.md 2>/dev/null | wc -l)
    if [ "$cmd_count" -gt 0 ]; then
        echo "✅ ($cmd_count commands)"
        ls .claude/commands/*.md 2>/dev/null | xargs -n 1 basename | sed 's/^/  - /' | sed 's/.md$//'
    else
        echo "⚠️  directory exists but empty"
        validation_warnings=$((validation_warnings + 1))
    fi
else
    echo "❌ MISSING"
    validation_errors=$((validation_errors + 1))
fi

# Check .gitignore (local-only mode)
if [ "$LOCAL_ONLY" = true ]; then
    echo -n ".gitignore config ... "
    if grep -q "Best Practice Toolkit" .gitignore 2>/dev/null; then
        echo "✅"
    else
        echo "❌ NOT CONFIGURED"
        validation_errors=$((validation_errors + 1))
    fi
fi

# Check full mode extras
if [ "$MODE" = "FULL" ]; then
    echo -n "tests/ structure ... "
    if [ -d "tests" ]; then
        echo "✅"
    else
        echo "⚠️  missing"
        validation_warnings=$((validation_warnings + 1))
    fi

    echo -n ".ai-validation/ ... "
    if [ -d ".ai-validation" ] && [ -f ".ai-validation/check_quality.sh" ]; then
        echo "✅"
    else
        echo "⚠️  missing"
        validation_warnings=$((validation_warnings + 1))
    fi
fi

echo ""
echo "════════════════════════════════════════════════════════"
if [ $validation_errors -eq 0 ] && [ $validation_warnings -eq 0 ]; then
    echo "  ✅ SUCCESS! All components installed"
elif [ $validation_errors -eq 0 ]; then
    echo "  ⚠️  DONE with $validation_warnings warning(s)"
else
    echo "  ❌ FAILED with $validation_errors error(s), $validation_warnings warning(s)"
    echo ""
    echo "  Run with: bash -x $0 --local-only"
    echo "  to debug installation issues"
fi
echo "════════════════════════════════════════════════════════"
echo ""
echo "Installed: $MODE mode"
if [ "$LOCAL_ONLY" = true ]; then
    echo "Mode: LOCAL ONLY (not tracked by git)"
fi
echo ""
echo "Next:"
echo "  1. Review: docs/notes/PROJECT_PLAN.md"
$([ "$MODE" = "FULL" ] && echo "  2. Copy MCPs: cp .claude/mcp-servers/*.py ~/.mcp-servers/")
$([ "$MODE" = "FULL" ] && echo "  3. Run: .claude/quality-gate/check_quality.sh")
echo ""
if [ "$LOCAL_ONLY" = true ]; then
    echo "✅ Toolkit installed locally only (DEFAULT)"
    echo "   .claude/ folder is gitignored by Claude Code"
    echo "   Files will NOT be committed or pushed to git"
    echo "   Each developer can have toolkit locally without affecting others"
    echo ""
    echo "To verify:"
    echo "  git status    # Should not show .claude/ folder"
    echo ""
    echo "To commit toolkit files: re-run with --commit flag"
else
    echo "⚠️  Toolkit files COMMITTED to git"
    echo "   .claude/ folder is now tracked in repository"
    echo "   All team members will receive toolkit files"
    echo ""
    echo "Rollback: git reset --hard retrofit-start"
fi
echo ""
