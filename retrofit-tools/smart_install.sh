#!/bin/bash
# Smart Install - ONE command, safe installation with smart questions

set -e

TOOLKIT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
PROJECT_DIR=$(pwd)
PROJECT_NAME=$(basename "$PROJECT_DIR")

# Parse flags
LOCAL_ONLY=false
if [[ "$1" == "--local-only" ]]; then
    LOCAL_ONLY=true
fi

clear
echo "════════════════════════════════════════════════════════"
echo "  Best Practice Toolkit - Smart Install"
if [ "$LOCAL_ONLY" = true ]; then
    echo "  Mode: LOCAL ONLY (no git commits)"
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
        ((production_score++))
        reasons+=("Low activity ($recent_commits commits/30d)")
    fi
else
    echo "no git"
fi

# Deployment configs
echo -n "  Checking deployment configs... "
if [ -f "Dockerfile" ] || [ -f "docker-compose.yml" ]; then
    ((production_score++))
    reasons+=("Has deployment config")
    echo "found"
else
    echo "none"
fi

# CI/CD
echo -n "  Checking CI/CD... "
if [ -d ".github/workflows" ] || [ -f ".gitlab-ci.yml" ] || [ -f "Jenkinsfile" ]; then
    ((production_score++))
    reasons+=("Has CI/CD")
    echo "found"
else
    echo "none"
fi

# Production env files
echo -n "  Checking production env... "
if [ -f ".env.production" ] || [ -f "config/production.yml" ]; then
    ((production_score++))
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
if [ "$MODE" = "FULL" ]; then
    mkdir -p tests .ai-validation
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
echo "[4/5] Installing toolkit files..."

# CLAUDE.md (always update/overwrite for upgrades)
if [ -f "CLAUDE.md" ]; then
    echo -n "CLAUDE.md (updating)... "
    cp "$TOOLKIT_DIR/CLAUDE.md" CLAUDE.md
    sed -i "s/Best Practice Toolkit/$PROJECT_NAME/g" CLAUDE.md 2>/dev/null || true
    echo "✅"
else
    echo -n "CLAUDE.md (new)... "
    cp "$TOOLKIT_DIR/CLAUDE.md" CLAUDE.md
    sed -i "s/Best Practice Toolkit/$PROJECT_NAME/g" CLAUDE.md 2>/dev/null || true
    echo "✅"
fi

# MCP servers (always update/overwrite for upgrades)
mkdir -p mcp-servers
echo -n "MCP servers... "
if cp "$TOOLKIT_DIR/mcp-servers/"*.py mcp-servers/ 2>/dev/null; then
    mcp_count=$(ls -1 mcp-servers/*.py 2>/dev/null | wc -l)
    echo "✅ ($mcp_count files)"
else
    echo "⚠️  MCP files not found at $TOOLKIT_DIR/mcp-servers/"
fi

# Slash commands (always update/overwrite for upgrades)
mkdir -p .claude/commands
echo -n "Slash commands... "
if cp "$TOOLKIT_DIR/.claude/commands/"*.md .claude/commands/ 2>/dev/null; then
    cmd_count=$(ls -1 .claude/commands/*.md 2>/dev/null | wc -l)
    echo "✅ ($cmd_count commands)"
else
    echo "⚠️  Slash commands not found at $TOOLKIT_DIR/.claude/commands/"
fi

# Full mode extras
if [ "$MODE" = "FULL" ]; then
    if [ ! -f ".ai-validation/check_quality.sh" ]; then
        cp "$TOOLKIT_DIR/.ai-validation/check_quality.sh" .ai-validation/ 2>/dev/null || true
        chmod +x .ai-validation/check_quality.sh 2>/dev/null || true
        echo "✅ Quality gate"
    fi

    if [ ! -f ".gitignore" ]; then
        cp "$TOOLKIT_DIR/.gitignore" . 2>/dev/null || echo "*.pyc
__pycache__/
.pytest_cache/
.coverage
*.log" > .gitignore
        echo "✅ .gitignore"
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

# Commit or add to .gitignore
if [ "$LOCAL_ONLY" = true ]; then
    echo "[5/5] Adding to .gitignore..."

    # Check if .gitignore exists, create if not
    if [ ! -f ".gitignore" ]; then
        touch .gitignore
    fi

    # Add toolkit files to .gitignore (only if not already there)
    if ! grep -q "Best Practice Toolkit" .gitignore 2>/dev/null; then
        cat >> .gitignore <<'GITIGNORE_EOF'

# Best Practice Toolkit (local development only)
CLAUDE.md
.claude/
mcp-servers/
docs/notes/PROJECT_PLAN.md
.ai-validation/
GITIGNORE_EOF
        echo "✅ Added toolkit to .gitignore"
    else
        echo "✅ Toolkit already in .gitignore"
    fi

    echo ""
    echo "⚠️  Files installed locally but NOT tracked by git"
else
    echo "[5/5] Committing changes..."
    git add -A

    if git diff --cached --quiet; then
        echo "✅ No changes (already installed)"
    else
        git commit -m "feat: install best-practice toolkit ($MODE mode)

- PROJECT_PLAN.md created
- CLAUDE.md standards
- MCP servers
$([ "$MODE" = "FULL" ] && echo "- Quality gate
- Test structure")

🤖 Generated with [Claude Code](https://claude.com/claude-code)

Co-Authored-By: Claude <noreply@anthropic.com>"

        git tag -f retrofit-complete 2>/dev/null || true
        echo "✅ Committed"
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
    ((validation_errors++))
fi

# Check PROJECT_PLAN.md
echo -n "PROJECT_PLAN.md ... "
if [ -f "docs/notes/PROJECT_PLAN.md" ]; then
    size=$(wc -c < "docs/notes/PROJECT_PLAN.md")
    echo "✅ ($size bytes)"
else
    echo "❌ MISSING"
    ((validation_errors++))
fi

# Check docs structure
echo -n "docs/ structure ... "
if [ -d "docs/notes" ]; then
    echo "✅"
else
    echo "❌ MISSING"
    ((validation_errors++))
fi

# Check mcp-servers
echo -n "mcp-servers/ ... "
if [ -d "mcp-servers" ]; then
    mcp_count=$(ls -1 mcp-servers/*.py 2>/dev/null | wc -l)
    if [ "$mcp_count" -gt 0 ]; then
        echo "✅ ($mcp_count files)"
        ls mcp-servers/*.py 2>/dev/null | xargs -n 1 basename | sed 's/^/  - /'
    else
        echo "⚠️  directory exists but empty"
        ((validation_warnings++))
    fi
else
    echo "❌ MISSING"
    ((validation_errors++))
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
        ((validation_warnings++))
    fi
else
    echo "❌ MISSING"
    ((validation_errors++))
fi

# Check .gitignore (local-only mode)
if [ "$LOCAL_ONLY" = true ]; then
    echo -n ".gitignore config ... "
    if grep -q "Best Practice Toolkit" .gitignore 2>/dev/null; then
        echo "✅"
    else
        echo "❌ NOT CONFIGURED"
        ((validation_errors++))
    fi
fi

# Check full mode extras
if [ "$MODE" = "FULL" ]; then
    echo -n "tests/ structure ... "
    if [ -d "tests" ]; then
        echo "✅"
    else
        echo "⚠️  missing"
        ((validation_warnings++))
    fi

    echo -n ".ai-validation/ ... "
    if [ -d ".ai-validation" ] && [ -f ".ai-validation/check_quality.sh" ]; then
        echo "✅"
    else
        echo "⚠️  missing"
        ((validation_warnings++))
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
echo "  2. Copy MCPs: cp mcp-servers/*.py ~/.mcp-servers/"
$([ "$MODE" = "FULL" ] && echo "  3. Run: .ai-validation/check_quality.sh")
echo ""
if [ "$LOCAL_ONLY" = true ]; then
    echo "⚠️  Toolkit installed locally only"
    echo "   Files will NOT be pushed to git"
    echo "   Added to .gitignore for safety"
    echo ""
    echo "To verify:"
    echo "  git status    # Should not show toolkit files"
else
    echo "Rollback: git reset --hard retrofit-start"
fi
echo ""
