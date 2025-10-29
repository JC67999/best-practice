#!/bin/bash
# Smart Installer - Auto-detects production vs non-production projects
# Chooses light mode (safe) or full mode (complete retrofit) automatically

set -e

echo "🔍 Analyzing project..."

# Detection: Check for production indicators
is_production=false

# Check 1: Recent commits (last 7 days)
if [ -d ".git" ]; then
    recent_commits=$(git log --since="7 days ago" --oneline 2>/dev/null | wc -l)
    if [ "$recent_commits" -gt 5 ]; then
        echo "  📊 Active development detected ($recent_commits commits in 7 days)"
        is_production=true
    fi
fi

# Check 2: Deployment configs
if [ -f "Dockerfile" ] || [ -f "docker-compose.yml" ] || [ -d ".github/workflows" ]; then
    echo "  🚀 Deployment configuration found"
    is_production=true
fi

# Report detection
echo ""
if [ "$is_production" = true ]; then
    echo "✅ PRODUCTION project detected"
    echo "   Mode: LIGHT (safe, minimal changes)"
    echo ""
    echo "Installing light mode:"
    echo "  - CLAUDE.md standards file"
    echo "  - Quality gate script"
    echo "  - Project objective setup"
else
    echo "✅ NON-PRODUCTION project detected"
    echo "   Mode: FULL (complete best practices)"
    echo ""
    echo "Installing full mode:"
    echo "  - All light mode features"
    echo "  - Complete retrofit (structure, docs, tests)"
fi

echo ""
echo "📦 Starting installation..."

# Get toolkit directory
TOOLKIT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"

# Run appropriate retrofit
if [ "$is_production" = true ]; then
    # Light mode: Basic installation only
    bash "$TOOLKIT_DIR/install.sh" "$(pwd)"
else
    # Full mode: Complete retrofit
    bash "$TOOLKIT_DIR/retrofit-tools/quick_retrofit.sh"
fi
