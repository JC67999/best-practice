#!/usr/bin/env bash
#
# Uninstall Best Practice Toolkit
# Removes all toolkit files while preserving your code
#
set -e

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

echo ""
echo "════════════════════════════════════════════════════════"
echo -e "  ${YELLOW}Best Practice Toolkit - Uninstall${NC}"
echo "════════════════════════════════════════════════════════"
echo ""

# Confirm uninstallation
echo -e "${YELLOW}This will remove:${NC}"
echo "  • .claude/ folder (all toolkit files)"
echo "  • CLAUDE.md"
echo "  • Git hooks (pre-commit, commit-msg, pre-push)"
echo "  • Gitignore entries for toolkit"
echo ""
echo -e "${GREEN}Your code will NOT be touched.${NC}"
echo ""

read -p "Proceed with uninstall? (y/N): " -n 1 -r
echo ""
if [[ ! $REPLY =~ ^[Yy]$ ]]; then
    echo "Uninstall cancelled"
    exit 0
fi

echo ""
echo "────────────────────────────────────────────────────────"
echo -e "${BLUE}Removing toolkit files...${NC}"
echo "────────────────────────────────────────────────────────"
echo ""

REMOVED=0

# Remove .claude/ folder
if [ -d ".claude" ]; then
    echo -e "${YELLOW}Removing:${NC} .claude/"
    rm -rf .claude/
    echo -e "  ${GREEN}✓${NC} Removed .claude/"
    REMOVED=$((REMOVED + 1))
else
    echo -e "${YELLOW}⚠${NC} .claude/ not found (already removed)"
fi

# Remove CLAUDE.md
if [ -f "CLAUDE.md" ]; then
    echo -e "${YELLOW}Removing:${NC} CLAUDE.md"
    rm CLAUDE.md
    echo -e "  ${GREEN}✓${NC} Removed CLAUDE.md"
    REMOVED=$((REMOVED + 1))
else
    echo -e "${YELLOW}⚠${NC} CLAUDE.md not found"
fi

# Remove git hooks
echo ""
echo -e "${BLUE}Removing git hooks...${NC}"
HOOKS=("pre-commit" "commit-msg" "pre-push")
for hook in "${HOOKS[@]}"; do
    if [ -f ".git/hooks/$hook" ]; then
        # Check if it's our hook (contains "Quality Gate" or "Best Practice")
        if grep -q "Quality Gate\|Best Practice" ".git/hooks/$hook" 2>/dev/null; then
            echo -e "${YELLOW}Removing:${NC} .git/hooks/$hook"

            # Restore backup if exists
            if [ -f ".git/hooks/$hook.backup" ]; then
                mv ".git/hooks/$hook.backup" ".git/hooks/$hook"
                echo -e "  ${GREEN}✓${NC} Restored original $hook"
            else
                rm ".git/hooks/$hook"
                echo -e "  ${GREEN}✓${NC} Removed $hook"
            fi
            REMOVED=$((REMOVED + 1))
        else
            echo -e "${YELLOW}⚠${NC} $hook exists but not from toolkit (skipping)"
        fi
    fi
done

# Remove gitignore entries
if [ -f ".gitignore" ]; then
    echo ""
    echo -e "${BLUE}Cleaning .gitignore...${NC}"

    # Create backup
    cp .gitignore .gitignore.backup

    # Remove toolkit entries
    sed -i '/# Best Practice Toolkit/d' .gitignore 2>/dev/null || true
    sed -i '/^\.claude\//d' .gitignore 2>/dev/null || true
    sed -i '/^CLAUDE\.md$/d' .gitignore 2>/dev/null || true
    sed -i '/^docs\//d' .gitignore 2>/dev/null || true
    sed -i '/^tests\//d' .gitignore 2>/dev/null || true

    echo -e "  ${GREEN}✓${NC} Cleaned .gitignore (backup: .gitignore.backup)"
    REMOVED=$((REMOVED + 1))
fi

# Remove docs/ and tests/ if they were added by toolkit
echo ""
read -p "Remove docs/ folder? (y/N): " -n 1 -r
echo ""
if [[ $REPLY =~ ^[Yy]$ ]] && [ -d "docs" ]; then
    echo -e "${YELLOW}Removing:${NC} docs/"
    rm -rf docs/
    echo -e "  ${GREEN}✓${NC} Removed docs/"
    REMOVED=$((REMOVED + 1))
fi

read -p "Remove tests/ folder? (y/N): " -n 1 -r
echo ""
if [[ $REPLY =~ ^[Yy]$ ]] && [ -d "tests" ]; then
    echo -e "${YELLOW}Removing:${NC} tests/"
    rm -rf tests/
    echo -e "  ${GREEN}✓${NC} Removed tests/"
    REMOVED=$((REMOVED + 1))
fi

# Summary
echo ""
echo "════════════════════════════════════════════════════════"
echo -e "  ${GREEN}✅ Uninstall Complete${NC}"
echo "════════════════════════════════════════════════════════"
echo ""
echo -e "${GREEN}Removed $REMOVED toolkit components${NC}"
echo ""
echo -e "${BLUE}Backups created:${NC}"
echo "  .gitignore.backup (if .gitignore was modified)"
echo ""
echo -e "${BLUE}Your project code is intact.${NC}"
echo ""
echo -e "${YELLOW}To reinstall:${NC}"
echo "  /path/to/best-practice/inject.sh ."
echo ""
