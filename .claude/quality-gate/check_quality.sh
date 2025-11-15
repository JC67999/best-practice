#!/usr/bin/env bash
#
# Smart Quality Gate - Language-Aware Quality Checks
# Auto-detects project type and runs appropriate tools
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
echo -e "  ${BLUE}Quality Gate - Running Checks${NC}"
echo "════════════════════════════════════════════════════════"
echo ""

FAILED=0

# Helper functions
report_check() {
    local check_name=$1
    local status=$2
    local details=$3

    if [ "$status" = "PASS" ]; then
        echo -e "${GREEN}✅ $check_name${NC}"
    elif [ "$status" = "SKIP" ]; then
        echo -e "${YELLOW}⚠  $check_name${NC} (skipped)"
    else
        echo -e "${RED}❌ $check_name${NC}"
        [ -n "$details" ] && echo -e "${RED}   $details${NC}"
        FAILED=1
    fi
}

# Detect project type
detect_project_type() {
    if [ -f "pyproject.toml" ] || [ -f "setup.py" ] || [ -f "requirements.txt" ]; then
        echo "python"
    elif [ -f "package.json" ]; then
        echo "javascript"
    elif [ -f "go.mod" ]; then
        echo "go"
    elif [ -f "Cargo.toml" ]; then
        echo "rust"
    else
        echo "unknown"
    fi
}

PROJECT_TYPE=$(detect_project_type)
echo -e "${BLUE}Project type:${NC} $PROJECT_TYPE"
echo ""

# Load config if exists
if [ -f ".claude/config.json" ]; then
    echo -e "${BLUE}Loading project config...${NC}"
    # Would parse config here for custom settings
fi

# ============================================================================
# Check 1: Git Status (Universal)
# ============================================================================
echo "────────────────────────────────────────────────────────"
echo -e "${BLUE}Check 1: Git Repository${NC}"
echo "────────────────────────────────────────────────────────"

if [ -d ".git" ]; then
    report_check "Git repository detected" "PASS"
else
    report_check "Git repository" "SKIP" "Not a git repository"
fi
echo ""

# ============================================================================
# Check 2: Linting (Language-Specific)
# ============================================================================
echo "────────────────────────────────────────────────────────"
echo -e "${BLUE}Check 2: Linting${NC}"
echo "────────────────────────────────────────────────────────"

case $PROJECT_TYPE in
    python)
        if command -v ruff &> /dev/null; then
            if ruff check . --quiet 2>/dev/null; then
                report_check "Python linting (ruff)" "PASS"
            else
                ERRORS=$(ruff check . 2>&1 | head -10)
                report_check "Python linting (ruff)" "FAIL" "$ERRORS"
            fi
        else
            report_check "Python linting" "SKIP" "ruff not installed"
        fi
        ;;
    javascript)
        if [ -f "package.json" ] && grep -q "\"lint\"" package.json; then
            if npm run lint --silent 2>/dev/null; then
                report_check "JavaScript linting" "PASS"
            else
                report_check "JavaScript linting" "FAIL" "Run: npm run lint"
            fi
        else
            report_check "JavaScript linting" "SKIP" "No lint script in package.json"
        fi
        ;;
    go)
        if command -v golangci-lint &> /dev/null; then
            if golangci-lint run ./... 2>/dev/null; then
                report_check "Go linting (golangci-lint)" "PASS"
            else
                report_check "Go linting" "FAIL" "Run: golangci-lint run"
            fi
        else
            report_check "Go linting" "SKIP" "golangci-lint not installed"
        fi
        ;;
    *)
        report_check "Linting" "SKIP" "Unknown project type"
        ;;
esac
echo ""

# ============================================================================
# Check 3: Type Checking (Language-Specific)
# ============================================================================
echo "────────────────────────────────────────────────────────"
echo -e "${BLUE}Check 3: Type Checking${NC}"
echo "────────────────────────────────────────────────────────"

case $PROJECT_TYPE in
    python)
        if command -v mypy &> /dev/null; then
            if mypy . --no-error-summary 2>/dev/null; then
                report_check "Python type checking (mypy)" "PASS"
            else
                report_check "Python type checking" "FAIL" "Run: mypy ."
            fi
        else
            report_check "Python type checking" "SKIP" "mypy not installed"
        fi
        ;;
    javascript)
        if [ -f "tsconfig.json" ]; then
            if npx tsc --noEmit 2>/dev/null; then
                report_check "TypeScript checking" "PASS"
            else
                report_check "TypeScript checking" "FAIL" "Run: npx tsc --noEmit"
            fi
        else
            report_check "TypeScript checking" "SKIP" "No tsconfig.json"
        fi
        ;;
    *)
        report_check "Type checking" "SKIP" "Not applicable"
        ;;
esac
echo ""

# ============================================================================
# Check 4: Tests (Language-Specific)
# ============================================================================
echo "────────────────────────────────────────────────────────"
echo -e "${BLUE}Check 4: Tests${NC}"
echo "────────────────────────────────────────────────────────"

if [ ! -d "tests" ] && [ ! -d "test" ]; then
    report_check "Tests" "SKIP" "No tests directory"
else
    case $PROJECT_TYPE in
        python)
            if command -v pytest &> /dev/null; then
                if pytest -q --tb=no 2>/dev/null; then
                    report_check "Python tests (pytest)" "PASS"
                else
                    report_check "Python tests" "FAIL" "Run: pytest -v"
                fi
            else
                report_check "Python tests" "SKIP" "pytest not installed"
            fi
            ;;
        javascript)
            if [ -f "package.json" ] && grep -q "\"test\"" package.json; then
                if npm test --silent 2>/dev/null; then
                    report_check "JavaScript tests" "PASS"
                else
                    report_check "JavaScript tests" "FAIL" "Run: npm test"
                fi
            else
                report_check "JavaScript tests" "SKIP" "No test script"
            fi
            ;;
        go)
            if go test ./... -short 2>/dev/null; then
                report_check "Go tests" "PASS"
            else
                report_check "Go tests" "FAIL" "Run: go test ./..."
            fi
            ;;
        *)
            report_check "Tests" "SKIP" "Unknown test framework"
            ;;
    esac
fi
echo ""

# ============================================================================
# Check 5: Code Coverage (Optional)
# ============================================================================
echo "────────────────────────────────────────────────────────"
echo -e "${BLUE}Check 5: Test Coverage${NC}"
echo "────────────────────────────────────────────────────────"

MIN_COVERAGE=80

case $PROJECT_TYPE in
    python)
        if command -v pytest &> /dev/null && pip list 2>/dev/null | grep -q pytest-cov; then
            COVERAGE=$(pytest --cov --cov-report=term-missing 2>/dev/null | grep "TOTAL" | awk '{print $4}' | sed 's/%//' || echo "0")
            if [ "$COVERAGE" -ge "$MIN_COVERAGE" ]; then
                report_check "Test coverage ($COVERAGE% >= $MIN_COVERAGE%)" "PASS"
            else
                report_check "Test coverage" "FAIL" "Coverage $COVERAGE% < $MIN_COVERAGE%"
            fi
        else
            report_check "Test coverage" "SKIP" "pytest-cov not installed"
        fi
        ;;
    *)
        report_check "Test coverage" "SKIP" "Not implemented for $PROJECT_TYPE"
        ;;
esac
echo ""

# ============================================================================
# Check 6: Security (Language-Specific)
# ============================================================================
echo "────────────────────────────────────────────────────────"
echo -e "${BLUE}Check 6: Security Scan${NC}"
echo "────────────────────────────────────────────────────────"

case $PROJECT_TYPE in
    python)
        if command -v bandit &> /dev/null; then
            if bandit -r . -ll -q 2>/dev/null; then
                report_check "Security scan (bandit)" "PASS"
            else
                report_check "Security scan" "FAIL" "Run: bandit -r ."
            fi
        else
            report_check "Security scan" "SKIP" "bandit not installed"
        fi
        ;;
    javascript)
        if npm audit --audit-level=moderate 2>/dev/null; then
            report_check "Security scan (npm audit)" "PASS"
        else
            report_check "Security scan" "FAIL" "Run: npm audit fix"
        fi
        ;;
    *)
        report_check "Security scan" "SKIP" "Not implemented"
        ;;
esac
echo ""

# ============================================================================
# Check 7: Structure Compliance (Universal)
# ============================================================================
echo "────────────────────────────────────────────────────────"
echo -e "${BLUE}Check 7: Project Structure${NC}"
echo "────────────────────────────────────────────────────────"

# Count root folders (excluding hidden)
ROOT_FOLDERS=$(ls -d */ 2>/dev/null | grep -v "^\." | wc -l)
MAX_ROOT_FOLDERS=5

if [ "$ROOT_FOLDERS" -le "$MAX_ROOT_FOLDERS" ]; then
    report_check "Root folders ($ROOT_FOLDERS <= $MAX_ROOT_FOLDERS)" "PASS"
else
    FOLDERS=$(ls -d */ 2>/dev/null | grep -v "^\." | head -10 | tr '\n' ' ')
    report_check "Root structure" "FAIL" "Too many folders ($ROOT_FOLDERS): $FOLDERS"
fi
echo ""

# ============================================================================
# Summary
# ============================================================================
echo "════════════════════════════════════════════════════════"
if [ $FAILED -eq 0 ]; then
    echo -e "  ${GREEN}✅ Quality Gate: PASSED${NC}"
    echo "════════════════════════════════════════════════════════"
    echo ""
    echo -e "${GREEN}All checks passed. Ready to commit!${NC}"
    echo ""
    exit 0
else
    echo -e "  ${RED}❌ Quality Gate: FAILED${NC}"
    echo "════════════════════════════════════════════════════════"
    echo ""
    echo -e "${RED}Fix the issues above before committing.${NC}"
    echo ""
    echo -e "${YELLOW}Resources:${NC}"
    echo "  • Standards: cat CLAUDE.md"
    echo "  • Quality skill: cat .claude/skills/quality-standards/skill.md"
    echo "  • Troubleshooting: cat .claude/TROUBLESHOOTING.md"
    echo ""
    exit 1
fi
