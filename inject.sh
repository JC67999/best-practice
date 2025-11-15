#!/usr/bin/env bash
#
# Best Practice Toolkit - Injectable Installation
# Run from toolkit project to inject into target project
#
# Usage:
#   ./inject.sh /path/to/target-project              # Default (gitignored)
#   ./inject.sh /path/to/target-project --commit     # Commit to git
#
set -e
set -o pipefail

TOOLKIT_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SCRIPT_NAME="$(basename "${BASH_SOURCE[0]}")"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Help text
show_help() {
    cat <<EOF
${GREEN}Best Practice Toolkit - Injectable Installation${NC}

${BLUE}USAGE:${NC}
  $SCRIPT_NAME <target-project-path> [--commit]

${BLUE}ARGUMENTS:${NC}
  target-project-path    Path to project to inject toolkit into
  --commit               Commit toolkit files to git (optional)

${BLUE}EXAMPLES:${NC}
  # Inject into Angular app (default: gitignored)
  $SCRIPT_NAME ~/projects/my-angular-app

  # Inject and commit to git
  $SCRIPT_NAME ~/projects/my-app --commit

  # Inject into current directory's sibling
  $SCRIPT_NAME ../other-project

${BLUE}WHAT IT DOES:${NC}
  1. Validates target project exists
  2. Changes to target directory
  3. Runs smart_install.sh from toolkit
  4. Installs all toolkit files
  5. Returns to original directory

${BLUE}DEFAULT BEHAVIOR:${NC}
  • Auto-detects LIGHT or FULL mode
  • All toolkit folders gitignored (clean git)
  • Zero git pollution
  • Local-only installation

${BLUE}FILES CREATED:${NC}
  .claude/              Standards, skills, MCP servers (gitignored)
  docs/                 Documentation (gitignored)
  tests/                Test structure, FULL mode only (gitignored)
  CLAUDE.md             Root reference (gitignored)
  .gitignore            Updated with toolkit folders

${BLUE}MORE INFO:${NC}
  docs/guides/INJECTION_GUIDE.md
  docs/guides/INJECTION_QUICK_REF.md

EOF
}

# Check arguments
if [ $# -eq 0 ]; then
    echo -e "${RED}Error: No target project specified${NC}"
    echo ""
    show_help
    exit 1
fi

if [[ "$1" == "-h" ]] || [[ "$1" == "--help" ]]; then
    show_help
    exit 0
fi

TARGET_PROJECT="$1"
COMMIT_FLAG="${2:-}"

# Validate target project path
if [ ! -d "$TARGET_PROJECT" ]; then
    echo -e "${RED}Error: Target project not found: $TARGET_PROJECT${NC}"
    echo ""
    echo "Please provide a valid project directory path."
    exit 1
fi

# Get absolute path
TARGET_PROJECT_ABS="$(cd "$TARGET_PROJECT" && pwd)"
TARGET_PROJECT_NAME="$(basename "$TARGET_PROJECT_ABS")"

# Validate toolkit has smart_install.sh
SMART_INSTALL="$TOOLKIT_ROOT/retrofit-tools/smart_install.sh"
if [ ! -f "$SMART_INSTALL" ]; then
    echo -e "${RED}Error: smart_install.sh not found${NC}"
    echo "Expected at: $SMART_INSTALL"
    echo ""
    echo "Are you running this from the best-practice toolkit root?"
    exit 1
fi

# Save original directory
ORIGINAL_DIR="$(pwd)"

# Display injection plan
clear
echo "════════════════════════════════════════════════════════"
echo -e "  ${GREEN}Best Practice Toolkit - Injection${NC}"
echo "════════════════════════════════════════════════════════"
echo ""
echo -e "${BLUE}Toolkit:${NC}    $TOOLKIT_ROOT"
echo -e "${BLUE}Target:${NC}     $TARGET_PROJECT_ABS"
echo -e "${BLUE}Project:${NC}    $TARGET_PROJECT_NAME"
echo ""

# Check if target is git repo
if [ -d "$TARGET_PROJECT_ABS/.git" ]; then
    echo -e "${GREEN}✓${NC} Git repository detected"
else
    echo -e "${YELLOW}⚠${NC} Not a git repository (will be initialized if needed)"
fi

# Check current git status if it's a repo
if [ -d "$TARGET_PROJECT_ABS/.git" ]; then
    cd "$TARGET_PROJECT_ABS"
    if ! git diff-index --quiet HEAD -- 2>/dev/null; then
        echo -e "${YELLOW}⚠${NC} Uncommitted changes detected"
    else
        echo -e "${GREEN}✓${NC} Working tree clean"
    fi
    cd "$ORIGINAL_DIR"
fi

echo ""
echo "────────────────────────────────────────────────────────"
echo ""

# Confirm injection
read -p "Proceed with injection? (Y/n): " -n 1 -r
echo ""
if [[ $REPLY =~ ^[Nn]$ ]]; then
    echo "Injection cancelled"
    exit 0
fi

echo ""
echo "════════════════════════════════════════════════════════"
echo -e "  ${GREEN}Injecting Toolkit...${NC}"
echo "════════════════════════════════════════════════════════"
echo ""

# Change to target directory
cd "$TARGET_PROJECT_ABS"

# Run smart_install.sh with proper arguments
if [ -n "$COMMIT_FLAG" ]; then
    bash "$SMART_INSTALL" "$COMMIT_FLAG"
else
    bash "$SMART_INSTALL"
fi

INSTALL_EXIT_CODE=$?

# Return to original directory
cd "$ORIGINAL_DIR"

# Report results
echo ""
echo "════════════════════════════════════════════════════════"
if [ $INSTALL_EXIT_CODE -eq 0 ]; then
    echo -e "  ${GREEN}✅ Injection Complete${NC}"
    echo "════════════════════════════════════════════════════════"
    echo ""
    echo -e "${GREEN}Successfully injected toolkit into:${NC}"
    echo "  $TARGET_PROJECT_ABS"
    echo ""

    # Offer to run init wizard
    echo "────────────────────────────────────────────────────────"
    echo -e "${YELLOW}Would you like to run the initialization wizard?${NC}"
    echo ""
    echo "The wizard will:"
    echo "  • Detect project type (Python/JS/Go/etc.)"
    echo "  • Create project-specific configuration"
    echo "  • Install git hooks for quality enforcement"
    echo "  • Set up initial tasks and project objective"
    echo "  • Customize toolkit for your project"
    echo ""
    read -p "Run initialization wizard now? (Y/n): " -n 1 -r
    echo ""
    echo ""

    if [[ ! $REPLY =~ ^[Nn]$ ]]; then
        # Change to target directory and run wizard
        cd "$TARGET_PROJECT_ABS"

        if [ -f ".claude/init-wizard.sh" ]; then
            bash .claude/init-wizard.sh
            WIZARD_EXIT_CODE=$?
            cd "$ORIGINAL_DIR"

            if [ $WIZARD_EXIT_CODE -eq 0 ]; then
                echo ""
                echo "════════════════════════════════════════════════════════"
                echo -e "  ${GREEN}🎉 Setup Complete - Ready to Code!${NC}"
                echo "════════════════════════════════════════════════════════"
                echo ""
            fi
        else
            echo -e "${RED}Error: init-wizard.sh not found${NC}"
            cd "$ORIGINAL_DIR"
        fi
    else
        echo -e "${YELLOW}Skipped initialization wizard${NC}"
        echo ""
        echo -e "${BLUE}To run later:${NC}"
        echo "  cd $TARGET_PROJECT_ABS"
        echo "  bash .claude/init-wizard.sh"
        echo ""
    fi

    echo -e "${BLUE}Next steps:${NC}"
    echo "  1. cd $TARGET_PROJECT_ABS"
    echo "  2. Review: .claude/config.json (if wizard ran)"
    echo "  3. Review: .claude/TASKS.md"
    echo "  4. Open in Claude Code: code ."
    echo ""
    echo -e "${BLUE}Verify:${NC}"
    echo "  git status     # Should be clean (all gitignored)"
    echo "  ls .claude/    # Toolkit files exist locally"
    echo "  cat .gitignore # Toolkit folders listed"
    echo ""
    echo -e "${BLUE}Resources:${NC}"
    echo "  cat CLAUDE.md                    # Project standards"
    echo "  cat .claude/skills/INDEX.md      # Skill catalog"
    echo "  bash .claude/hooks/install-hooks.sh  # Install git hooks"
    echo ""
else
    echo -e "  ${RED}❌ Injection Failed${NC}"
    echo "════════════════════════════════════════════════════════"
    echo ""
    echo -e "${RED}Installation encountered errors${NC}"
    echo ""
    echo "Troubleshooting:"
    echo "  1. Check error messages above"
    echo "  2. Ensure target is valid project"
    echo "  3. Run with debug: bash -x $SCRIPT_NAME $TARGET_PROJECT"
    echo ""
    exit 1
fi
