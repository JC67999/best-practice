#!/usr/bin/env bash
#
# Install Git Hooks
# Copies hooks from .claude/hooks/ to .git/hooks/
#
set -e

# Colors
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m'

echo ""
echo "════════════════════════════════════════════════════════"
echo -e "  ${GREEN}Installing Git Hooks${NC}"
echo "════════════════════════════════════════════════════════"
echo ""

# Check if .git exists
if [ ! -d ".git" ]; then
    echo -e "${RED}Error: Not a git repository${NC}"
    echo "Run 'git init' first"
    exit 1
fi

# Check if hooks directory exists
if [ ! -d ".claude/hooks" ]; then
    echo -e "${RED}Error: .claude/hooks directory not found${NC}"
    exit 1
fi

# Install hooks
HOOKS=("pre-commit" "commit-msg" "pre-push")
INSTALLED=0

for hook in "${HOOKS[@]}"; do
    if [ -f ".claude/hooks/$hook" ]; then
        echo -e "${YELLOW}Installing:${NC} $hook"

        # Backup existing hook if present
        if [ -f ".git/hooks/$hook" ]; then
            if [ ! -f ".git/hooks/$hook.backup" ]; then
                cp ".git/hooks/$hook" ".git/hooks/$hook.backup"
                echo -e "  ${YELLOW}→${NC} Backed up existing hook to $hook.backup"
            fi
        fi

        # Copy hook
        cp ".claude/hooks/$hook" ".git/hooks/$hook"
        chmod +x ".git/hooks/$hook"
        echo -e "  ${GREEN}✓${NC} Installed $hook"
        INSTALLED=$((INSTALLED + 1))
    else
        echo -e "${YELLOW}⚠${NC} Hook not found: $hook (skipping)"
    fi
done

echo ""
echo "════════════════════════════════════════════════════════"
echo -e "  ${GREEN}✅ Installation Complete${NC}"
echo "════════════════════════════════════════════════════════"
echo ""
echo -e "${GREEN}Installed $INSTALLED hooks${NC}"
echo ""
echo -e "${YELLOW}What these hooks do:${NC}"
echo ""
echo "  pre-commit:  Run quality gate before each commit"
echo "  commit-msg:  Validate commit message format"
echo "  pre-push:    Final checks before pushing to remote"
echo ""
echo -e "${YELLOW}To bypass hooks (NOT recommended):${NC}"
echo "  git commit --no-verify"
echo "  git push --no-verify"
echo ""
echo -e "${YELLOW}To uninstall:${NC}"
echo "  rm .git/hooks/pre-commit"
echo "  rm .git/hooks/commit-msg"
echo "  rm .git/hooks/pre-push"
echo ""
