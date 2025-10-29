#!/usr/bin/env bash
#
# Best Practice Toolkit - Installation Script
# Installs toolkit into target project in under 10 minutes
#

set -e

PROJECT_DIR="${1:-.}"
TOOLKIT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

echo "📦 Installing Best Practice Toolkit..."
echo "Target project: $PROJECT_DIR"

# Create directory structure
mkdir -p "$PROJECT_DIR/docs/notes"
mkdir -p "$PROJECT_DIR/.ai-validation"
mkdir -p "$PROJECT_DIR/mcp-servers"

# Copy MCP servers
cp -r "$TOOLKIT_DIR/mcp-servers/"* "$PROJECT_DIR/mcp-servers/"
echo "✅ MCP servers installed"

# Copy quality gate
cp "$TOOLKIT_DIR/.ai-validation/check_quality.sh" "$PROJECT_DIR/.ai-validation/"
chmod +x "$PROJECT_DIR/.ai-validation/check_quality.sh"
echo "✅ Quality gate installed"

# Copy templates
cp "$TOOLKIT_DIR/CLAUDE.md" "$PROJECT_DIR/CLAUDE.md" 2>/dev/null || echo "ℹ️  CLAUDE.md already exists"

echo ""
echo "🎉 Installation complete!"
echo "Next steps:"
echo "  1. Define project objective"
echo "  2. Run quality gate: cd .ai-validation && bash check_quality.sh"
