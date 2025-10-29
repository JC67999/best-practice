#!/bin/bash
# Retrofit Validation Script
# Validates that Best Practice Toolkit retrofit was successful

echo "🔍 Validating Best Practice Retrofit..."
errors=0

# Check git repository
if [ ! -d ".git" ]; then
    echo "❌ No git repository found"
    ((errors++))
else
    echo "✅ Git repository initialized"
fi

# Check required files
required_files=("CLAUDE.md" ".ai-validation/check_quality.sh" "docs/notes/PROJECT_PLAN.md")
for file in "${required_files[@]}"; do
    if [ -f "$file" ]; then
        echo "✅ $file exists"
    else
        echo "❌ $file missing"
        ((errors++))
    fi
done

# Check minimal root structure
root_folders=$(find . -maxdepth 1 -type d ! -name '.*' ! -name '.' | wc -l)
if [ "$root_folders" -le 5 ]; then
    echo "✅ Root structure minimal ($root_folders folders)"
else
    echo "⚠️  Root has $root_folders folders (target: ≤5)"
fi

# Summary
echo ""
if [ $errors -eq 0 ]; then
    echo "✅ Retrofit validation passed!"
    exit 0
else
    echo "❌ Retrofit validation failed ($errors errors)"
    exit 1
fi
