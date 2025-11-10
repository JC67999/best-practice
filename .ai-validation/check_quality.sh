#!/bin/bash

# Quality Gate Script - Minimal Efficiency Focus
# Enforces: Changelog, Comments, Linting, Structure

set -e

echo "🔍 Quality Gate (Fast & Essential)"
echo ""

RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

FAILED=0

report_check() {
    local check_name=$1
    local status=$2
    local details=$3

    if [ "$status" = "PASS" ]; then
        echo -e "${GREEN}✅ $check_name${NC}"
    else
        echo -e "${RED}❌ $check_name${NC}"
        [ -n "$details" ] && echo -e "${RED}   $details${NC}"
        FAILED=1
    fi
}

# Check 1: Changelog Updated
echo "Checking CHANGELOG.md..."
if git diff --cached --name-only | grep -q "CHANGELOG.md"; then
    report_check "Changelog updated" "PASS"
elif git diff --name-only | grep -q "CHANGELOG.md"; then
    report_check "Changelog" "FAIL" "CHANGELOG.md modified but not staged. Run: git add CHANGELOG.md"
else
    # Check if there are code changes
    CODE_CHANGES=$(git diff --cached --name-only | grep -E '\.(py|js|ts|md)$' || true)
    if [ -n "$CODE_CHANGES" ]; then
        report_check "Changelog" "FAIL" "Code changes detected but CHANGELOG.md not updated"
    else
        echo -e "${YELLOW}⚠️  No code changes detected${NC}"
    fi
fi

# Check 2: Code Comments (Python files only for now)
echo "Checking code comments..."
PYTHON_FILES=$(git diff --cached --name-only --diff-filter=AM | grep '\.py$' || true)
if [ -n "$PYTHON_FILES" ]; then
    UNCOMMENTED=0
    for file in $PYTHON_FILES; do
        if [ -f "$file" ]; then
            # Check for functions without docstrings
            FUNCTIONS=$(grep -c "^def " "$file" 2>/dev/null || echo "0")
            DOCSTRINGS=$(grep -c '"""' "$file" 2>/dev/null || echo "0")

            if [ "$FUNCTIONS" -gt 0 ] && [ "$DOCSTRINGS" -eq 0 ]; then
                echo -e "${YELLOW}   $file: Has functions but no docstrings${NC}"
                UNCOMMENTED=$((UNCOMMENTED + 1))
            fi
        fi
    done

    if [ "$UNCOMMENTED" -eq 0 ]; then
        report_check "Code comments present" "PASS"
    else
        report_check "Code comments" "FAIL" "$UNCOMMENTED file(s) need docstrings"
    fi
else
    echo -e "${YELLOW}⚠️  No Python files to check${NC}"
fi

# Check 3: Linting
echo "Running linting..."
if ruff check mcp-servers/ > /tmp/ruff_output.txt 2>&1; then
    report_check "No linting errors" "PASS"
else
    report_check "Linting" "FAIL" "$(cat /tmp/ruff_output.txt)"
fi

# Check 4: Structure Compliance
echo "Checking structure..."
ROOT_FOLDERS=$(ls -d */ 2>/dev/null | grep -v "^\\." | wc -l)

if [ "$ROOT_FOLDERS" -le 5 ]; then
    report_check "Root folders ≤5 ($ROOT_FOLDERS)" "PASS"
else
    report_check "Structure" "FAIL" "Too many root folders: $ROOT_FOLDERS (max: 5)"
fi

# Summary
echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
if [ $FAILED -eq 0 ]; then
    echo -e "${GREEN}✅ Quality Gate: PASS${NC}"
    echo "Ready to commit."
    exit 0
else
    echo -e "${RED}❌ Quality Gate: FAIL${NC}"
    echo "Fix issues above before committing."
    exit 1
fi
