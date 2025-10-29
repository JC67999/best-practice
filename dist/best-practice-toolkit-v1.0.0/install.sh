#!/bin/bash
# Best Practice Toolkit - Installation Script
# Version: 1.0

set -e

echo "🎯 Best Practice Toolkit - Installation"
echo "========================================"
echo ""

# Check Python version
echo "🔍 Checking Python version..."
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 not found. Please install Python 3.10 or higher."
    exit 1
fi

PYTHON_VERSION=$(python3 --version | awk '{print $2}')
echo "✅ Found Python $PYTHON_VERSION"

# Install MCP SDK
echo ""
echo "📦 Installing MCP SDK..."
pip3 install mcp || {
    echo "⚠️  MCP SDK installation failed. You can install it later with: pip3 install mcp"
}

# Install MCP servers
echo ""
echo "📋 Installing MCP servers..."
mkdir -p ~/.mcp-servers
cp mcp-servers/*.py ~/.mcp-servers/
chmod +x ~/.mcp-servers/*.py
echo "✅ MCP servers installed to ~/.mcp-servers/"

# Create memory directory
mkdir -p ~/.claude_memory
echo "✅ Memory directory created at ~/.claude_memory/"

# Detect OS and config location
echo ""
echo "🔧 Detecting Claude Code configuration location..."
if [[ "$OSTYPE" == "darwin"* ]]; then
    CONFIG_DIR="$HOME/Library/Application Support/Claude"
    CONFIG_FILE="$CONFIG_DIR/claude_desktop_config.json"
    echo "📍 macOS detected: $CONFIG_FILE"
elif [[ "$OSTYPE" == "msys" || "$OSTYPE" == "win32" ]]; then
    CONFIG_DIR="$APPDATA/Claude"
    CONFIG_FILE="$CONFIG_DIR/claude_desktop_config.json"
    echo "📍 Windows detected: $CONFIG_FILE"
else
    CONFIG_DIR="$HOME/.config/claude"
    CONFIG_FILE="$CONFIG_DIR/claude_desktop_config.json"
    echo "📍 Linux detected: $CONFIG_FILE"
fi

# Provide configuration instructions
echo ""
echo "⚙️  Configuration Required"
echo "=========================="
echo ""
echo "Add this to your Claude Code configuration file:"
echo "File: $CONFIG_FILE"
echo ""
cat << 'CONFIG_EOF'
{
  "mcpServers": {
    "memory": {
      "command": "python3",
      "args": ["HOME_DIR/.mcp-servers/memory_mcp.py"],
      "disabled": false
    },
    "quality": {
      "command": "python3",
      "args": ["HOME_DIR/.mcp-servers/quality_mcp.py"],
      "disabled": false
    },
    "project": {
      "command": "python3",
      "args": ["HOME_DIR/.mcp-servers/project_mcp.py"],
      "disabled": false
    }
  }
}
CONFIG_EOF

echo ""
echo "⚠️  IMPORTANT: Replace HOME_DIR with your actual home directory:"
echo "   $HOME"
echo ""

# Summary
echo ""
echo "✅ Installation Complete!"
echo "========================"
echo ""
echo "📁 Installed Components:"
echo "   - MCP Servers: ~/.mcp-servers/"
echo "   - Memory Storage: ~/.claude_memory/"
echo ""
echo "📖 Next Steps:"
echo "   1. Configure Claude Code (see above)"
echo "   2. Restart Claude Code"
echo "   3. Test: Ask Claude 'List available MCP tools'"
echo "   4. Read: README.md for usage guide"
echo ""
echo "📚 Documentation:"
echo "   - README.md - Complete overview"
echo "   - docs/ - Detailed guides"
echo "   - mcp-servers/README.md - MCP usage"
echo ""
echo "🚀 Ready to enforce excellence!"
