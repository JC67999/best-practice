#!/usr/bin/env bash
#
# Verify Git Cleanliness After Toolkit Injection
# Proves that toolkit doesn't pollute project's GitHub
#
set -e

# Colors
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

echo ""
echo "════════════════════════════════════════════════════════"
echo -e "  ${BLUE}Git Cleanliness Verification${NC}"
echo "════════════════════════════════════════════════════════"
echo ""

FAILED=0

# Check 1: Git status should be clean
echo -e "${BLUE}Check 1: Git Status${NC}"
echo "────────────────────────────────────────────────────────"

if git diff-index --quiet HEAD -- 2>/dev/null; then
    echo -e "${GREEN}✅ Working tree is clean${NC}"
    echo "   No uncommitted changes"
else
    echo -e "${RED}❌ Uncommitted changes detected${NC}"
    echo ""
    git status --short
    echo ""
    echo "These files are NOT gitignored properly:"
    FAILED=1
fi
echo ""

# Check 2: Toolkit folders are gitignored
echo -e "${BLUE}Check 2: Gitignore Entries${NC}"
echo "────────────────────────────────────────────────────────"

TOOLKIT_FOLDERS=(".claude/" "docs/")
ALL_IGNORED=true

for folder in "${TOOLKIT_FOLDERS[@]}"; do
    if grep -qxF "$folder" .gitignore 2>/dev/null; then
        echo -e "${GREEN}✅${NC} $folder is gitignored"
    else
        echo -e "${RED}❌${NC} $folder NOT in .gitignore"
        ALL_IGNORED=false
        FAILED=1
    fi
done

if [ "$ALL_IGNORED" = true ]; then
    echo -e "${GREEN}✅ All toolkit folders gitignored${NC}"
fi
echo ""

# Check 3: No toolkit files tracked by git
echo -e "${BLUE}Check 3: Tracked Files${NC}"
echo "────────────────────────────────────────────────────────"

TRACKED_TOOLKIT=$(git ls-files | grep -E "^\.claude/|^docs/" || true)

if [ -z "$TRACKED_TOOLKIT" ]; then
    echo -e "${GREEN}✅ No toolkit files tracked by git${NC}"
    echo "   Toolkit is completely local"
else
    echo -e "${RED}❌ Toolkit files are tracked:${NC}"
    echo "$TRACKED_TOOLKIT"
    FAILED=1
fi
echo ""

# Check 4: Nothing would be pushed to GitHub
echo -e "${BLUE}Check 4: What Would Be Pushed${NC}"
echo "────────────────────────────────────────────────────────"

# Check if there are unpushed commits
if git log origin/$(git branch --show-current)..HEAD --oneline 2>/dev/null | grep -q "toolkit\|Best Practice"; then
    echo -e "${YELLOW}⚠${NC} Toolkit-related commits would be pushed"
    echo ""
    git log origin/$(git branch --show-current)..HEAD --oneline | grep -i "toolkit\|best practice" || true
    echo ""
    echo "This is OK if you used --commit flag intentionally"
else
    echo -e "${GREEN}✅ No toolkit commits would be pushed${NC}"
fi
echo ""

# Check 5: Root directory is minimal
echo -e "${BLUE}Check 5: Root Directory${NC}"
echo "────────────────────────────────────────────────────────"

# Count non-hidden folders in root (excluding .git, .claude, etc.)
ROOT_FOLDERS=$(ls -d */ 2>/dev/null | grep -v "^\." | wc -l)

echo -e "Root folders (visible): ${GREEN}$ROOT_FOLDERS${NC}"
ls -d */ 2>/dev/null | grep -v "^\." | sed 's/^/  - /'

if [ "$ROOT_FOLDERS" -le 5 ]; then
    echo -e "${GREEN}✅ Root directory is minimal (≤5 folders)${NC}"
else
    echo -e "${YELLOW}⚠${NC} Root has $ROOT_FOLDERS folders (recommend ≤5)"
fi
echo ""

# Check 6: Toolkit files exist locally
echo -e "${BLUE}Check 6: Local Toolkit Files${NC}"
echo "────────────────────────────────────────────────────────"

REQUIRED_FILES=(
    ".claude/best-practice.md"
    ".claude/TASKS.md"
    ".claude/skills/INDEX.md"
    ".claude/hooks/pre-commit"
    ".claude/quality-gate/check_quality.sh"
)

ALL_EXIST=true
for file in "${REQUIRED_FILES[@]}"; do
    if [ -f "$file" ]; then
        echo -e "${GREEN}✅${NC} $file"
    else
        echo -e "${RED}❌${NC} $file MISSING"
        ALL_EXIST=false
    fi
done

if [ "$ALL_EXIST" = true ]; then
    echo -e "${GREEN}✅ All toolkit files installed locally${NC}"
fi
echo ""

# Summary
echo "════════════════════════════════════════════════════════"
if [ $FAILED -eq 0 ]; then
    echo -e "  ${GREEN}✅ VERIFICATION PASSED${NC}"
    echo "════════════════════════════════════════════════════════"
    echo ""
    echo -e "${GREEN}Toolkit is completely hidden from git!${NC}"
    echo ""
    echo "✅ No files will appear in GitHub"
    echo "✅ Clean git status"
    echo "✅ Toolkit is local development tool only"
    echo "✅ Safe for team projects"
    echo ""
    exit 0
else
    echo -e "  ${RED}❌ VERIFICATION FAILED${NC}"
    echo "════════════════════════════════════════════════════════"
    echo ""
    echo -e "${RED}Some toolkit files are NOT properly gitignored!${NC}"
    echo ""
    echo "This should NOT happen with default installation."
    echo "If you used --commit flag, this is expected."
    echo ""
    echo "To fix:"
    echo "  1. Check .gitignore for toolkit folders"
    echo "  2. Run: git rm --cached -r .claude docs"
    echo "  3. Verify: git status"
    echo ""
    exit 1
fi
