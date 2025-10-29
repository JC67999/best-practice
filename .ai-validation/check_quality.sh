#!/bin/bash

# Quality Gate Script - Best Practice Toolkit
# Enforces quality standards before allowing commit

set -e  # Exit on first error

echo "🔍 Running Quality Gate..."
echo ""

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

FAILED=0

# Function to report check status
report_check() {
    local check_name=$1
    local status=$2
    local details=$3

    if [ "$status" = "PASS" ]; then
        echo -e "${GREEN}✅ $check_name${NC}"
    else
        echo -e "${RED}❌ $check_name${NC}"
        if [ -n "$details" ]; then
            echo -e "${RED}   $details${NC}"
        fi
        FAILED=1
    fi
}

# Check 1: Tests
echo "Running tests..."
if pytest tests/ -v --tb=short > /tmp/pytest_output.txt 2>&1; then
    report_check "All tests pass" "PASS"
else
    report_check "Tests" "FAIL" "$(tail -20 /tmp/pytest_output.txt)"
fi

# Check 2: Test Coverage
echo "Checking test coverage..."
if pytest tests/ --cov=mcp-servers --cov-report=term-missing --cov-fail-under=80 > /tmp/coverage_output.txt 2>&1; then
    COVERAGE=$(grep "TOTAL" /tmp/coverage_output.txt | awk '{print $NF}')
    report_check "Test coverage ≥80% ($COVERAGE)" "PASS"
else
    COVERAGE=$(grep "TOTAL" /tmp/coverage_output.txt | awk '{print $NF}' || echo "unknown")
    report_check "Test coverage" "FAIL" "Coverage is $COVERAGE (minimum: 80%)"
fi

# Check 3: Linting
echo "Running linting checks..."
if ruff check mcp-servers/ > /tmp/ruff_output.txt 2>&1; then
    report_check "No linting errors" "PASS"
else
    report_check "Linting" "FAIL" "$(cat /tmp/ruff_output.txt)"
fi

# Check 4: Type checking
echo "Running type checks..."
if mypy mcp-servers/ --ignore-missing-imports > /tmp/mypy_output.txt 2>&1; then
    report_check "No type errors" "PASS"
else
    report_check "Type checking" "FAIL" "$(cat /tmp/mypy_output.txt)"
fi

# Check 5: Security check
echo "Running security checks..."
if bandit -r mcp-servers/ -ll > /tmp/bandit_output.txt 2>&1; then
    report_check "No security issues" "PASS"
else
    report_check "Security" "FAIL" "$(cat /tmp/bandit_output.txt)"
fi

# Check 6: Structure compliance
echo "Checking project structure..."
ROOT_FOLDERS=$(ls -d */ 2>/dev/null | grep -v "^\\." | wc -l)
ROOT_FILES=$(ls -p | grep -v / | grep -v "^\\." | wc -l)

if [ "$ROOT_FOLDERS" -le 5 ]; then
    report_check "Root folders ≤5 (found: $ROOT_FOLDERS)" "PASS"
else
    report_check "Root structure" "FAIL" "Too many root folders: $ROOT_FOLDERS (max: 5)"
fi

# Check for forbidden items in root
FORBIDDEN=$(ls -1 | grep -E "\\.log$|\\.tmp$|^temp$|^logs$|^cache$" || true)
if [ -z "$FORBIDDEN" ]; then
    report_check "No forbidden files in root" "PASS"
else
    report_check "Forbidden files" "FAIL" "Found: $FORBIDDEN"
fi

# Summary
echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
if [ $FAILED -eq 0 ]; then
    echo -e "${GREEN}✅ Quality Gate: PASS${NC}"
    echo "All checks passed. Ready to commit!"
    exit 0
else
    echo -e "${RED}❌ Quality Gate: FAIL${NC}"
    echo "Fix the issues above before committing."
    exit 1
fi
