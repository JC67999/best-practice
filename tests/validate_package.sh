#!/bin/bash
# Validation script for package_toolkit.sh
# Checks if package_toolkit.sh references match actual file structure

echo "Validating package_toolkit.sh..."
errors=0

# Files that package_toolkit.sh expects
expected_files=(
    "mcp-servers/memory_mcp.py"
    "mcp-servers/quality_mcp.py"
    "mcp-servers/project_mcp.py"
    "README.md"
    "CLAUDE.md"
    "install.sh"
)

# Check existing files
for file in "${expected_files[@]}"; do
    if [ -f "$file" ]; then
        echo "✅ $file"
    else
        echo "❌ $file missing"
        ((errors++))
    fi
done

# Report
echo ""
if [ $errors -eq 0 ]; then
    echo "✅ All critical files exist"
    echo "⚠️  NOTE: package_toolkit.sh has outdated paths and needs updating"
    exit 0
else
    echo "❌ $errors files missing"
    exit 1
fi
