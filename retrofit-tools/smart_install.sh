#!/bin/bash
# Smart Installer - Auto-detects production vs non-production projects
# Chooses light mode (safe) or full mode (complete retrofit) automatically

set -e

echo "🔍 Analyzing project..."
echo ""

# Detection: Score production indicators
# Higher score = more likely to be production/stable
production_score=0

# Check 1: Recent activity (LOW activity suggests stable/production)
if [ -d ".git" ]; then
    recent_commits=$(git log --since="30 days ago" --oneline 2>/dev/null | wc -l)
    if [ "$recent_commits" -lt 3 ]; then
        echo "  💤 Stable/low activity ($recent_commits commits in 30 days)"
        ((production_score++))
    else
        echo "  📊 Active development ($recent_commits commits in 30 days)"
    fi
fi

# Check 2: Deployment configs (suggests production-ready)
if [ -f "Dockerfile" ] || [ -f "docker-compose.yml" ]; then
    echo "  🐳 Deployment configuration found"
    ((production_score++))
fi

# Check 3: CI/CD configuration (suggests production-ready)
if [ -d ".github/workflows" ] || [ -f ".gitlab-ci.yml" ] || [ -f "Jenkinsfile" ]; then
    echo "  🔄 CI/CD configuration found"
    ((production_score++))
fi

# Check 4: Production environment files
if [ -f ".env.production" ] || [ -f "config/production.yml" ]; then
    echo "  ⚙️  Production environment configuration found"
    ((production_score++))
fi

# Determine mode (2+ indicators = production)
is_production=false
if [ "$production_score" -ge 2 ]; then
    is_production=true
fi

# Report detection
echo ""
if [ "$is_production" = true ]; then
    echo "✅ PRODUCTION project detected (score: $production_score/4)"
    echo "   Mode: LIGHT (safe, minimal changes)"
    echo ""
    echo "Installing light mode:"
    echo "  - CLAUDE.md standards file"
    echo "  - PROJECT_PLAN.md with objective"
    echo "  - MCP servers"
    echo "  - Quality gate script"
else
    echo "✅ DEVELOPMENT project detected (score: $production_score/4)"
    echo "   Mode: FULL (complete best practices)"
    echo ""
    echo "Installing full mode:"
    echo "  - All light mode features"
    echo "  - Complete retrofit (structure, docs, tests)"
fi

# Interactive confirmation
echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo ""
read -p "Proceed with installation? (Y/n): " -n 1 -r
echo ""
if [[ $REPLY =~ ^[Nn]$ ]]; then
    echo "Installation cancelled."
    exit 0
fi

# Option to override mode
echo ""
read -p "Override mode? (y/N): " -n 1 -r
echo ""
if [[ $REPLY =~ ^[Yy]$ ]]; then
    echo ""
    echo "Select mode:"
    echo "  1) LIGHT - Safe for production"
    echo "  2) FULL  - Complete retrofit"
    read -p "Choice (1/2): " -n 1 -r mode_choice
    echo ""
    if [ "$mode_choice" = "2" ]; then
        is_production=false
    else
        is_production=true
    fi
fi

echo ""
echo "📦 Starting installation..."
echo ""

# Get toolkit directory
TOOLKIT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"

# Validate toolkit
if [ ! -f "$TOOLKIT_DIR/retrofit-tools/quick_retrofit.sh" ]; then
    echo "❌ Error: Cannot find retrofit script at $TOOLKIT_DIR"
    exit 1
fi

# Run quick_retrofit with appropriate answer piped in
if [ "$is_production" = true ]; then
    # Answer "y" to production question (Light mode)
    echo "y" | bash "$TOOLKIT_DIR/retrofit-tools/quick_retrofit.sh"
else
    # Answer "n" to production question (Full mode)
    echo "n" | bash "$TOOLKIT_DIR/retrofit-tools/quick_retrofit.sh"
fi
