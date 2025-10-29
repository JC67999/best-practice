# Retrofit Methodology - Apply Best Practices to Existing Projects

> **Purpose**: Non-destructive method to retrofit best practices and MCP enforcement into ANY existing Claude project
> **Version**: 1.0
> **Date**: 2025-10-29
> **Philosophy**: Meet projects where they are, improve incrementally, maintain safety

---

## Executive Summary

This methodology allows you to apply the complete MCP + Best Practice system to existing projects WITHOUT:
- ❌ Breaking existing code
- ❌ Forcing immediate large refactors
- ❌ Losing project history
- ❌ Disrupting active development

Instead, you get:
- ✅ **Gradual adoption** - Phases in improvements over time
- ✅ **Safety first** - All changes are reversible
- ✅ **Objective extraction** - Reverse-engineers objective from existing code
- ✅ **Structure migration** - Non-destructive consolidation
- ✅ **Quality baseline** - Measures current state, tracks improvement
- ✅ **Flexible enforcement** - Choose what to enforce when

---

## Table of Contents

1. [Quick Start - Retrofit in 10 Minutes](#quick-start-retrofit-in-10-minutes)
2. [Retrofit Phases Overview](#retrofit-phases-overview)
3. [Phase 0: Safety Checkpoint](#phase-0-safety-checkpoint)
4. [Phase 1: Assessment](#phase-1-assessment)
5. [Phase 2: Objective Extraction](#phase-2-objective-extraction)
6. [Phase 3: Structure Migration](#phase-3-structure-migration)
7. [Phase 4: Quality Baseline](#phase-4-quality-baseline)
8. [Phase 5: Gradual Enforcement](#phase-5-gradual-enforcement)
9. [Phase 6: Full Integration](#phase-6-full-integration)
10. [Retrofit Tools](#retrofit-tools)
11. [Common Scenarios](#common-scenarios)
12. [Rollback Procedures](#rollback-procedures)

---

## Quick Start - Retrofit in 10 Minutes

**For the impatient - minimum viable retrofit:**

```bash
# 1. SAFETY FIRST (2 minutes)
cd your-existing-project
git status
git add .
git commit -m "Safe state before retrofit"
git tag retrofit-start

# 2. RUN ASSESSMENT (2 minutes)
curl -O https://[URL]/retrofit_assess.py
python retrofit_assess.py .
# Review: assessment_report.md

# 3. EXTRACT OBJECTIVE (3 minutes)
python retrofit_extract_objective.py .
# Review and refine: OBJECTIVE.md

# 4. LIGHT MIGRATION (3 minutes)
python retrofit_structure.py . --mode=light
# Creates artifacts/, consolidates logs/temp, preserves everything else

# DONE - You now have:
# ✅ Project objective documented
# ✅ Cleaner root structure
# ✅ Assessment baseline
# ✅ Rollback point (git tag)
```

**Next steps**: Review `RETROFIT_PLAN.md` for gradual improvement path.

---

## Retrofit Phases Overview

### Phase Structure

```
Phase 0: Safety Checkpoint (5 min)
   ↓
Phase 1: Assessment (10 min)
   - Analyze structure
   - Measure quality
   - Identify issues
   ↓
Phase 2: Objective Extraction (15 min)
   - Reverse-engineer objective
   - Clarify through interrogation
   - Document in OBJECTIVE.md
   ↓
Phase 3: Structure Migration (30 min)
   - Consolidate to minimal root
   - Non-destructive moves
   - Update references
   ↓
Phase 4: Quality Baseline (15 min)
   - Install quality tools
   - Run initial checks
   - Document current state
   ↓
Phase 5: Gradual Enforcement (ongoing)
   - Phase in quality gates
   - Improve incrementally
   - Track progress
   ↓
Phase 6: Full Integration (1 hour)
   - Enable all MCPs
   - Full quality enforcement
   - Complete best practice compliance
```

**Timeline Options**:
- **Express**: Phases 0-4 in 1 hour, Phase 5 over 1 week
- **Standard**: Phases 0-4 in 1 day, Phase 5 over 2 weeks
- **Cautious**: Phases 0-4 over 1 week, Phase 5 over 1 month

---

## Phase 0: Safety Checkpoint

**ALWAYS start here. No exceptions.**

### Step 1: Verify Git State

```bash
cd your-project

# Check status
git status

# Should see: "nothing to commit, working tree clean"
# If not: commit or stash changes first
```

### Step 2: Create Rollback Points

```bash
# Create backup branch
git branch retrofit-backup

# Create starting tag
git tag retrofit-start

# Verify
git log --oneline -1
git tag
```

### Step 3: Document Current State

```bash
# Count files
find . -type f | wc -l > .retrofit/pre_retrofit_file_count.txt

# List root items
ls -la > .retrofit/pre_retrofit_root_listing.txt

# Capture structure
tree -L 2 -d > .retrofit/pre_retrofit_structure.txt 2>/dev/null || \
  find . -type d -maxdepth 2 > .retrofit/pre_retrofit_structure.txt
```

### Step 4: Verify Tests Pass

```bash
# Run existing tests (if any)
pytest tests/ -v || python -m unittest discover || echo "No tests found"

# Save results
# If tests pass: proceed
# If tests fail: fix first OR document as baseline
```

### Safety Checklist

- [ ] Git status clean OR changes committed
- [ ] Backup branch created
- [ ] Rollback tag created
- [ ] Current state documented
- [ ] Tests passing OR baseline documented
- [ ] **Can rollback**: `git reset --hard retrofit-start`

**ONLY proceed when all checkboxes ✅**

---

## Phase 1: Assessment

**Goal**: Understand current project state without making changes.

### Assessment Tool

**Create/run**: `retrofit_assess.py`

```python
#!/usr/bin/env python3
"""
Retrofit Assessment Tool - Analyzes existing project structure.
"""
import os
import json
from pathlib import Path
from collections import defaultdict

def assess_project(project_path):
    """Comprehensive project assessment."""
    results = {
        "structure": assess_structure(project_path),
        "quality": assess_quality(project_path),
        "objective": assess_objective_clarity(project_path),
        "recommendations": []
    }

    generate_recommendations(results)
    return results

def assess_structure(project_path):
    """Assess directory structure."""
    root_items = os.listdir(project_path)

    # Count folders
    folders = [f for f in root_items
               if os.path.isdir(os.path.join(project_path, f))
               and not f.startswith('.')]

    # Identify structure type
    has_src = 'src' in folders
    has_tests = 'tests' in folders or 'test' in folders
    has_docs = 'docs' in folders or 'documentation' in folders

    # Check for clutter
    clutter_indicators = [
        'logs', 'temp', 'tmp', 'output', 'input',
        'import', 'export', 'data', 'cache', 'scripts'
    ]
    clutter = [f for f in folders if f.lower() in clutter_indicators]

    # Check for minimal root compliance
    minimal_root_folders = ['src', 'tests', 'docs', 'artifacts', 'migrations']
    unknown_folders = [f for f in folders
                       if f not in minimal_root_folders
                       and not f.startswith('.')
                       and not f.startswith('venv')]

    return {
        "total_root_folders": len(folders),
        "has_src_structure": has_src,
        "has_tests": has_tests,
        "has_docs": has_docs,
        "clutter_folders": clutter,
        "unknown_folders": unknown_folders,
        "minimal_root_compliant": len(folders) <= 5 and has_src,
        "structure_score": calculate_structure_score(
            len(folders), has_src, has_tests, len(clutter)
        )
    }

def assess_quality(project_path):
    """Assess code quality indicators."""

    # Find Python files
    py_files = find_python_files(project_path)

    # Check for existing quality tools
    quality_tools = {
        "pytest": os.path.exists(os.path.join(project_path, "pytest.ini")) or
                  os.path.exists(os.path.join(project_path, "pyproject.toml")),
        "ruff": check_for_tool_config(project_path, "ruff"),
        "mypy": check_for_tool_config(project_path, "mypy"),
        "black": check_for_tool_config(project_path, "black"),
    }

    # Estimate test coverage (rough)
    test_files = find_test_files(project_path)
    test_to_code_ratio = len(test_files) / max(len(py_files), 1)

    # Check for docstrings (sample)
    docstring_coverage = estimate_docstring_coverage(project_path, py_files[:10])

    return {
        "total_python_files": len(py_files),
        "total_test_files": len(test_files),
        "test_to_code_ratio": round(test_to_code_ratio, 2),
        "has_quality_tools": quality_tools,
        "estimated_docstring_coverage": docstring_coverage,
        "quality_score": calculate_quality_score(
            quality_tools, test_to_code_ratio, docstring_coverage
        )
    }

def assess_objective_clarity(project_path):
    """Assess if project has clear objective."""

    # Check for objective documentation
    objective_files = [
        "README.md", "OBJECTIVE.md", "SPECIFICATION.md",
        "CLAUDE.md", "PROJECT.md"
    ]

    found_docs = []
    clarity_indicators = []

    for filename in objective_files:
        filepath = os.path.join(project_path, filename)
        if os.path.exists(filepath):
            found_docs.append(filename)
            clarity = analyze_objective_clarity_in_file(filepath)
            if clarity:
                clarity_indicators.extend(clarity)

    has_clear_objective = len(clarity_indicators) >= 3

    return {
        "found_documentation": found_docs,
        "clarity_indicators": clarity_indicators,
        "has_clear_objective": has_clear_objective,
        "objective_score": min(len(clarity_indicators) * 20, 100)
    }

def generate_recommendations(results):
    """Generate specific recommendations."""
    recs = []

    # Structure recommendations
    if results["structure"]["total_root_folders"] > 7:
        recs.append({
            "priority": "HIGH",
            "category": "Structure",
            "issue": f"{results['structure']['total_root_folders']} root folders (target: 4-5)",
            "action": "Run structure migration to consolidate into artifacts/"
        })

    if results["structure"]["clutter_folders"]:
        recs.append({
            "priority": "MEDIUM",
            "category": "Structure",
            "issue": f"Clutter folders: {', '.join(results['structure']['clutter_folders'])}",
            "action": "Move to artifacts/ directory"
        })

    # Quality recommendations
    if results["quality"]["test_to_code_ratio"] < 0.3:
        recs.append({
            "priority": "HIGH",
            "category": "Quality",
            "issue": "Low test coverage (estimated)",
            "action": "Add tests incrementally following TDD"
        })

    if not any(results["quality"]["has_quality_tools"].values()):
        recs.append({
            "priority": "HIGH",
            "category": "Quality",
            "issue": "No quality tools configured",
            "action": "Install quality gates (.ai-validation/)"
        })

    # Objective recommendations
    if results["objective"]["objective_score"] < 60:
        recs.append({
            "priority": "CRITICAL",
            "category": "Objective",
            "issue": "No clear project objective documented",
            "action": "Run objective extraction tool"
        })

    results["recommendations"] = recs

def calculate_structure_score(folder_count, has_src, has_tests, clutter_count):
    """Calculate structure health score."""
    score = 100

    # Penalize for too many folders
    if folder_count > 5:
        score -= (folder_count - 5) * 10

    # Reward for good structure
    if has_src:
        score += 10
    if has_tests:
        score += 10

    # Penalize clutter
    score -= clutter_count * 15

    return max(min(score, 100), 0)

def calculate_quality_score(tools, test_ratio, docstring_coverage):
    """Calculate quality health score."""
    score = 0

    # Tools configured
    score += sum(tools.values()) * 15

    # Test coverage
    if test_ratio > 0.5:
        score += 30
    elif test_ratio > 0.3:
        score += 20
    elif test_ratio > 0.1:
        score += 10

    # Docstrings
    score += min(docstring_coverage, 30)

    return min(score, 100)

# Helper functions
def find_python_files(path):
    """Find all Python files."""
    py_files = []
    for root, dirs, files in os.walk(path):
        # Skip venv, __pycache__, etc.
        dirs[:] = [d for d in dirs if d not in ['venv', '__pycache__', '.git', 'node_modules']]
        py_files.extend([os.path.join(root, f) for f in files if f.endswith('.py')])
    return py_files

def find_test_files(path):
    """Find test files."""
    test_files = []
    for root, dirs, files in os.walk(path):
        if 'test' in root.lower():
            test_files.extend([f for f in files if f.endswith('.py')])
    return test_files

def check_for_tool_config(path, tool):
    """Check if tool is configured."""
    pyproject = os.path.join(path, "pyproject.toml")
    if os.path.exists(pyproject):
        with open(pyproject) as f:
            content = f.read()
            if f"[tool.{tool}]" in content:
                return True

    # Check for dedicated config files
    config_files = {
        "ruff": ["ruff.toml", ".ruff.toml"],
        "mypy": ["mypy.ini", ".mypy.ini"],
        "black": [".black", "black.toml"]
    }

    if tool in config_files:
        for config in config_files[tool]:
            if os.path.exists(os.path.join(path, config)):
                return True

    return False

def estimate_docstring_coverage(path, sample_files):
    """Estimate docstring coverage from sample."""
    if not sample_files:
        return 0

    total_functions = 0
    documented_functions = 0

    for filepath in sample_files:
        try:
            with open(filepath) as f:
                content = f.read()
                # Simple heuristic: count "def " and '"""'
                total_functions += content.count('def ')
                documented_functions += content.count('"""')
        except:
            pass

    if total_functions == 0:
        return 0

    return round((documented_functions / total_functions) * 100)

def analyze_objective_clarity_in_file(filepath):
    """Look for objective clarity indicators in file."""
    indicators = []

    try:
        with open(filepath) as f:
            content = f.read().lower()

            # Look for key phrases
            if "objective" in content or "purpose" in content:
                indicators.append("has_objective_statement")

            if "problem" in content and "solv" in content:
                indicators.append("defines_problem")

            if "user" in content or "customer" in content:
                indicators.append("identifies_users")

            if "goal" in content or "target" in content or "metric" in content:
                indicators.append("has_success_metrics")
    except:
        pass

    return indicators

def write_assessment_report(results, output_path):
    """Write human-readable assessment report."""
    report = f"""# Project Retrofit Assessment Report

Generated: {Path.ctime(Path(output_path))}

---

## Overall Scores

- **Structure Health**: {results['structure']['structure_score']}/100
- **Quality Health**: {results['quality']['quality_score']}/100
- **Objective Clarity**: {results['objective']['objective_score']}/100

**Overall Project Health**: {calculate_overall_score(results)}/100

---

## Structure Assessment

**Current State**:
- Total root folders: {results['structure']['total_root_folders']} (target: 4-5)
- Has src/ structure: {"✅" if results['structure']['has_src_structure'] else "❌"}
- Has tests/: {"✅" if results['structure']['has_tests'] else "❌"}
- Has docs/: {"✅" if results['structure']['has_docs'] else "❌"}
- Minimal root compliant: {"✅" if results['structure']['minimal_root_compliant'] else "❌"}

**Clutter Folders** (should move to artifacts/):
{format_list(results['structure']['clutter_folders']) or "None"}

**Unknown Folders**:
{format_list(results['structure']['unknown_folders']) or "None (good!)"}

---

## Quality Assessment

**Current State**:
- Python files: {results['quality']['total_python_files']}
- Test files: {results['quality']['total_test_files']}
- Test-to-code ratio: {results['quality']['test_to_code_ratio']} (target: >0.5)
- Estimated docstring coverage: {results['quality']['estimated_docstring_coverage']}% (target: >80%)

**Quality Tools Configured**:
"""

    for tool, configured in results['quality']['has_quality_tools'].items():
        report += f"- {tool}: {"✅" if configured else "❌"}\n"

    report += f"""
---

## Objective Clarity Assessment

**Current State**:
- Documentation found: {', '.join(results['objective']['found_documentation']) or "None"}
- Clear objective: {"✅" if results['objective']['has_clear_objective'] else "❌"}

**Clarity Indicators**:
{format_list(results['objective']['clarity_indicators']) or "None found"}

---

## Recommendations

Priority order: CRITICAL → HIGH → MEDIUM → LOW

"""

    for rec in sorted(results['recommendations'],
                     key=lambda x: {"CRITICAL": 0, "HIGH": 1, "MEDIUM": 2, "LOW": 3}.get(x['priority'], 4)):
        report += f"""
### [{rec['priority']}] {rec['category']}

**Issue**: {rec['issue']}
**Action**: {rec['action']}
"""

    report += """
---

## Next Steps

### Immediate (Phase 2)
1. Extract/clarify project objective
2. Document in OBJECTIVE.md

### Short-term (Phase 3)
1. Consolidate structure (move to artifacts/)
2. Reduce root folders to 4-5

### Medium-term (Phase 4-5)
1. Install quality gates
2. Add missing tests
3. Improve docstring coverage

### Long-term (Phase 6)
1. Enable full MCP integration
2. Achieve 100% compliance

---

## Rollback

If needed, rollback to pre-retrofit state:

```bash
git reset --hard retrofit-start
git clean -fd
```

Your backup branch: `retrofit-backup`

"""

    with open(output_path, 'w') as f:
        f.write(report)

def calculate_overall_score(results):
    """Calculate overall project health."""
    return round((
        results['structure']['structure_score'] * 0.3 +
        results['quality']['quality_score'] * 0.4 +
        results['objective']['objective_score'] * 0.3
    ))

def format_list(items):
    """Format list for report."""
    if not items:
        return ""
    return "\n".join(f"- {item}" for item in items)

# Main execution
if __name__ == "__main__":
    import sys

    if len(sys.argv) < 2:
        print("Usage: python retrofit_assess.py <project_path>")
        sys.exit(1)

    project_path = sys.argv[1]

    print("🔍 Assessing project...")
    results = assess_project(project_path)

    # Create .retrofit directory
    retrofit_dir = os.path.join(project_path, ".retrofit")
    os.makedirs(retrofit_dir, exist_ok=True)

    # Write JSON results
    with open(os.path.join(retrofit_dir, "assessment.json"), 'w') as f:
        json.dump(results, f, indent=2)

    # Write markdown report
    report_path = os.path.join(project_path, "ASSESSMENT_REPORT.md")
    write_assessment_report(results, report_path)

    print(f"✅ Assessment complete!")
    print(f"📊 Report: {report_path}")
    print(f"📈 Overall Health: {calculate_overall_score(results)}/100")
    print(f"\nPriority issues: {len([r for r in results['recommendations'] if r['priority'] in ['CRITICAL', 'HIGH']])}")
```

### Running Assessment

```bash
# Download or copy retrofit_assess.py to your project
cd your-project
python retrofit_assess.py .

# Review results
cat ASSESSMENT_REPORT.md
```

### Assessment Checklist

- [ ] Assessment report generated
- [ ] Overall health score calculated
- [ ] Recommendations reviewed
- [ ] Priority issues identified
- [ ] Baseline metrics recorded in .retrofit/

---

## Phase 2: Objective Extraction

**Goal**: Reverse-engineer the project objective from existing code and docs.

### Automatic Extraction Tool

**Create/run**: `retrofit_extract_objective.py`

```python
#!/usr/bin/env python3
"""
Objective Extraction Tool - Reverse-engineers project objective.
"""
import os
import re
from pathlib import Path

def extract_objective(project_path):
    """Extract objective from existing documentation and code."""

    extraction = {
        "from_readme": extract_from_readme(project_path),
        "from_code": extract_from_code(project_path),
        "from_docs": extract_from_docs(project_path),
        "synthesized": {}
    }

    # Synthesize objective
    extraction["synthesized"] = synthesize_objective(extraction)

    return extraction

def extract_from_readme(project_path):
    """Extract objective indicators from README."""
    readme_path = os.path.join(project_path, "README.md")

    if not os.path.exists(readme_path):
        return {"found": False}

    with open(readme_path) as f:
        content = f.read()

    # Look for key sections
    problem = extract_section(content, ["problem", "challenge", "issue"])
    solution = extract_section(content, ["solution", "approach", "overview"])
    features = extract_section(content, ["features", "capabilities"])

    return {
        "found": True,
        "problem": problem,
        "solution": solution,
        "features": features
    }

def extract_from_code(project_path):
    """Extract objective from code structure and patterns."""

    # Find main module/package
    src_path = os.path.join(project_path, "src")
    if not os.path.exists(src_path):
        src_path = project_path

    # Look for main entry points
    entry_points = find_entry_points(src_path)

    # Analyze module names for domain
    modules = find_modules(src_path)
    domain_hints = analyze_domain_from_modules(modules)

    # Look for models/entities
    entities = find_entities(src_path)

    return {
        "entry_points": entry_points,
        "domain_hints": domain_hints,
        "entities": entities
    }

def extract_from_docs(project_path):
    """Extract from other documentation."""
    docs_path = os.path.join(project_path, "docs")

    if not os.path.exists(docs_path):
        return {"found": False}

    # Look for spec/design docs
    specs = []
    for root, dirs, files in os.walk(docs_path):
        for file in files:
            if file.endswith('.md'):
                filepath = os.path.join(root, file)
                with open(filepath) as f:
                    content = f.read()
                    if any(keyword in content.lower()
                          for keyword in ["objective", "goal", "purpose", "problem"]):
                        specs.append({
                            "file": file,
                            "content_preview": content[:500]
                        })

    return {
        "found": len(specs) > 0,
        "relevant_docs": specs
    }

def synthesize_objective(extraction):
    """Synthesize objective from all sources."""

    objective = {
        "problem": "UNCLEAR - Needs user input",
        "target_user": "UNCLEAR - Needs user input",
        "solution": "UNCLEAR - Needs user input",
        "confidence": "low"
    }

    # Try to infer from README
    if extraction["from_readme"]["found"]:
        if extraction["from_readme"]["problem"]:
            objective["problem"] = extraction["from_readme"]["problem"]
            objective["confidence"] = "medium"

        if extraction["from_readme"]["solution"]:
            objective["solution"] = extraction["from_readme"]["solution"]

    # Try to infer from code
    if extraction["from_code"]["domain_hints"]:
        domain = extraction["from_code"]["domain_hints"][0]
        objective["domain"] = domain

    if extraction["from_code"]["entities"]:
        objective["entities"] = extraction["from_code"]["entities"][:5]

    return objective

def extract_section(content, keywords):
    """Extract section matching keywords."""
    lines = content.split('\n')

    for i, line in enumerate(lines):
        if any(keyword in line.lower() for keyword in keywords):
            # Found section header
            section_content = []
            j = i + 1
            while j < len(lines) and not lines[j].startswith('#'):
                section_content.append(lines[j])
                j += 1
                if j - i > 10:  # Limit extraction
                    break

            return '\n'.join(section_content).strip()

    return None

def find_entry_points(path):
    """Find main entry points."""
    entry_points = []

    candidates = ["main.py", "app.py", "cli.py", "__main__.py", "run.py"]
    for candidate in candidates:
        filepath = os.path.join(path, candidate)
        if os.path.exists(filepath):
            entry_points.append(candidate)

    return entry_points

def find_modules(path):
    """Find Python modules."""
    modules = []
    for root, dirs, files in os.walk(path):
        for file in files:
            if file.endswith('.py') and file != '__init__.py':
                modules.append(file[:-3])  # Remove .py
    return modules

def analyze_domain_from_modules(modules):
    """Infer domain from module names."""
    # Common domain patterns
    domains = {
        "web": ["api", "server", "web", "http", "route"],
        "data": ["parser", "processor", "etl", "transform", "import"],
        "ml": ["model", "train", "predict", "feature"],
        "cli": ["cli", "command", "terminal"],
        "database": ["db", "database", "schema", "migration"]
    }

    domain_scores = {domain: 0 for domain in domains}

    for module in modules:
        module_lower = module.lower()
        for domain, keywords in domains.items():
            if any(kw in module_lower for kw in keywords):
                domain_scores[domain] += 1

    # Return top domains
    sorted_domains = sorted(domain_scores.items(), key=lambda x: x[1], reverse=True)
    return [d[0] for d in sorted_domains if d[1] > 0]

def find_entities(path):
    """Find entity/model classes."""
    entities = []

    for root, dirs, files in os.walk(path):
        for file in files:
            if file.endswith('.py'):
                filepath = os.path.join(root, file)
                try:
                    with open(filepath) as f:
                        content = f.read()
                        # Look for class definitions
                        classes = re.findall(r'class (\w+)', content)
                        entities.extend(classes)
                except:
                    pass

    return list(set(entities))[:10]  # Unique, limited

def write_objective_template(extraction, output_path):
    """Write OBJECTIVE.md template for user to complete."""

    synth = extraction["synthesized"]

    template = f"""# Project Objective (NEEDS CLARIFICATION)

> **Status**: EXTRACTED - Requires user review and refinement
> **Confidence**: {synth.get('confidence', 'low')}
> **Next Step**: Run MCP objective clarification to improve

---

## Extracted Information

### From Documentation

**Problem** (extracted):
{synth.get('problem', 'Not found in documentation')}

**Solution** (extracted):
{synth.get('solution', 'Not found in documentation')}

### From Code Analysis

**Domain**: {', '.join(synth.get('domain', ['Unknown']))}

**Entry Points**: {', '.join(extraction['from_code']['entry_points']) or 'None found'}

**Key Entities/Models**:
{format_entity_list(synth.get('entities', []))}

---

## OBJECTIVE TEMPLATE (Complete This)

### 🎯 Problem Statement

**What specific problem does this project solve?**
[FILL IN - Be specific about the problem]

**Who experiences this problem?**
[FILL IN - Define target users specifically]

**How do they currently handle this problem?**
[FILL IN - What's the current solution?]

**Why is the current solution inadequate?**
[FILL IN - What pain points exist?]

### 💡 Solution

**What does this project do to solve the problem?**
[FILL IN - Core functionality]

**What is the ONE core feature?**
[FILL IN - The single most important capability]

**What is the absolute minimum that works?**
[FILL IN - MVP definition]

### 🎯 Success Metrics

**How will you know this is successful?**
[FILL IN - Specific, measurable metrics]

**What numbers indicate success?**
[FILL IN - Concrete targets]

**By when?**
[FILL IN - Timeline]

### 🚫 Out of Scope (v1)

**What are you NOT building?**
- [FILL IN - Feature 1]
- [FILL IN - Feature 2]
- [FILL IN - Feature 3]

### 🔧 Technical Details

**Tech Stack**:
{extract_tech_stack(extraction)}

**Non-Negotiable Requirements**:
[FILL IN - What cannot be compromised?]

---

## Next Steps

1. **Review extracted information above**
2. **Fill in all [FILL IN] sections**
3. **Run MCP objective clarification for comprehensive questioning**
4. **Achieve clarity score >80**
5. **Move to Phase 3 (Structure Migration)**

---

## Clarity Checklist

Before proceeding, ensure:
- [ ] Problem is specific (not "improve" or "help users")
- [ ] Target users are specific (not "people" or "users")
- [ ] Solution is concrete (not vague)
- [ ] Success metrics are measurable (numbers, not feelings)
- [ ] Timeline is defined
- [ ] Out-of-scope items are explicit

**Current Clarity Score**: [Run scoring tool after completing]

"""

    with open(output_path, 'w') as f:
        f.write(template)

def format_entity_list(entities):
    """Format entity list."""
    if not entities:
        return "None found"
    return "\n".join(f"- {entity}" for entity in entities)

def extract_tech_stack(extraction):
    """Extract technology stack."""
    # Simple heuristic: look for imports and config files
    # In real implementation, scan requirements.txt, pyproject.toml, etc.
    return "[Auto-detect from requirements.txt and imports]"

# Main execution
if __name__ == "__main__":
    import sys

    if len(sys.argv) < 2:
        print("Usage: python retrofit_extract_objective.py <project_path>")
        sys.exit(1)

    project_path = sys.argv[1]

    print("🔍 Extracting objective from project...")
    extraction = extract_objective(project_path)

    # Write template
    output_path = os.path.join(project_path, "OBJECTIVE.md")
    write_objective_template(extraction, output_path)

    # Also save raw extraction
    import json
    with open(os.path.join(project_path, ".retrofit/objective_extraction.json"), 'w') as f:
        json.dump(extraction, f, indent=2)

    print(f"✅ Objective template created: {output_path}")
    print(f"📝 Review and complete all [FILL IN] sections")
    print(f"💡 Then run MCP clarification for comprehensive questioning")
```

### Running Objective Extraction

```bash
cd your-project
python retrofit_extract_objective.py .

# Review and edit
nano OBJECTIVE.md

# OR run MCP clarification (when MCPs installed)
# MCP will interrogate you with comprehensive questions
```

### Objective Extraction Checklist

- [ ] Objective template generated
- [ ] Extracted information reviewed
- [ ] User completed [FILL IN] sections
- [ ] **OR** scheduled MCP interrogation session
- [ ] Clarity score checked (target >80)
- [ ] OBJECTIVE.md committed to git

---

## Phase 3: Structure Migration

**Goal**: Non-destructively consolidate to minimal root structure.

### Migration Modes

**Choose based on your project state:**

1. **Light Mode** - Minimal changes, maximum safety
   - Creates `artifacts/` folder
   - Moves `logs/`, `temp/`, `output/`, `input/`
   - Preserves everything else
   - **Recommended for first retrofit**

2. **Standard Mode** - Balanced approach
   - Light mode changes PLUS:
   - Consolidates scattered operational folders
   - Updates common file references
   - **Recommended for most projects**

3. **Full Mode** - Complete transformation
   - Standard mode changes PLUS:
   - Creates `src/` if missing
   - Organizes `docs/`
   - Handles migrations/ placement
   - **Recommended for committed retrofits**

### Structure Migration Tool

**Create/run**: `retrofit_structure.py`

```python
#!/usr/bin/env python3
"""
Structure Migration Tool - Consolidates to minimal root structure.
"""
import os
import shutil
from pathlib import Path

def migrate_structure(project_path, mode="light", dry_run=False):
    """Migrate project structure to minimal root."""

    print(f"🔄 Running structure migration in {mode} mode")
    if dry_run:
        print("🔍 DRY RUN - No changes will be made")

    actions = []

    if mode in ["light", "standard", "full"]:
        actions.extend(create_artifacts_folder(project_path, dry_run))

    if mode in ["light", "standard", "full"]:
        actions.extend(move_operational_folders(project_path, dry_run))

    if mode in ["standard", "full"]:
        actions.extend(consolidate_scattered_data(project_path, dry_run))

    if mode == "full":
        actions.extend(organize_source_code(project_path, dry_run))
        actions.extend(organize_documentation(project_path, dry_run))
        actions.extend(handle_migrations(project_path, dry_run))

    # Update references
    if not dry_run and actions:
        update_file_references(project_path, actions)

    return actions

def create_artifacts_folder(project_path, dry_run):
    """Create artifacts/ directory structure."""
    actions = []

    artifacts_path = os.path.join(project_path, "artifacts")
    subdirs = ["logs", "temp", "input", "output", ".archive"]

    if not os.path.exists(artifacts_path):
        action = {
            "type": "create_folder",
            "path": "artifacts/",
            "reason": "Central location for operational data"
        }
        actions.append(action)

        if not dry_run:
            os.makedirs(artifacts_path)
            print(f"✅ Created artifacts/")
        else:
            print(f"[DRY RUN] Would create artifacts/")

    for subdir in subdirs:
        subdir_path = os.path.join(artifacts_path, subdir)
        if not os.path.exists(subdir_path):
            if not dry_run:
                os.makedirs(subdir_path)
            actions.append({
                "type": "create_folder",
                "path": f"artifacts/{subdir}/",
                "reason": f"Organized {subdir} storage"
            })

    return actions

def move_operational_folders(project_path, dry_run):
    """Move operational folders to artifacts/."""
    actions = []

    # Folders to move
    move_map = {
        "logs": "artifacts/logs",
        "temp": "artifacts/temp",
        "tmp": "artifacts/temp",
        "output": "artifacts/output",
        "input": "artifacts/input",
        "import": "artifacts/input",
        "export": "artifacts/output",
        "data": "artifacts/data",
        "cache": "artifacts/cache"
    }

    for src_folder, dest_folder in move_map.items():
        src_path = os.path.join(project_path, src_folder)
        dest_path = os.path.join(project_path, dest_folder)

        if os.path.exists(src_path) and os.path.isdir(src_path):
            action = {
                "type": "move_folder",
                "from": f"{src_folder}/",
                "to": f"{dest_folder}/",
                "reason": f"Consolidate operational data"
            }
            actions.append(action)

            if not dry_run:
                # Ensure destination parent exists
                os.makedirs(os.path.dirname(dest_path), exist_ok=True)

                # Move folder
                if os.path.exists(dest_path):
                    # Merge contents
                    merge_folders(src_path, dest_path)
                    shutil.rmtree(src_path)
                else:
                    shutil.move(src_path, dest_path)

                print(f"✅ Moved {src_folder}/ → {dest_folder}/")
            else:
                print(f"[DRY RUN] Would move {src_folder}/ → {dest_folder}/")

    return actions

def consolidate_scattered_data(project_path, dry_run):
    """Find and consolidate scattered data files."""
    actions = []

    # Look for scattered log files in root
    for item in os.listdir(project_path):
        item_path = os.path.join(project_path, item)

        if os.path.isfile(item_path):
            # Move log files
            if item.endswith('.log') or 'log' in item.lower():
                dest = os.path.join(project_path, "artifacts/logs", item)
                actions.append({
                    "type": "move_file",
                    "from": item,
                    "to": f"artifacts/logs/{item}",
                    "reason": "Consolidate logs"
                })

                if not dry_run:
                    shutil.move(item_path, dest)
                    print(f"✅ Moved {item} → artifacts/logs/")

            # Move temp/scratch files
            elif any(x in item.lower() for x in ['temp', 'tmp', 'scratch', 'test_']):
                dest = os.path.join(project_path, "artifacts/temp", item)
                actions.append({
                    "type": "move_file",
                    "from": item,
                    "to": f"artifacts/temp/{item}",
                    "reason": "Consolidate temporary files"
                })

                if not dry_run:
                    shutil.move(item_path, dest)
                    print(f"✅ Moved {item} → artifacts/temp/")

    return actions

def organize_source_code(project_path, dry_run):
    """Organize source code into src/ if needed."""
    actions = []

    src_path = os.path.join(project_path, "src")

    # Check if src/ exists
    if os.path.exists(src_path):
        return actions  # Already organized

    # Look for Python modules in root
    py_modules = []
    for item in os.listdir(project_path):
        item_path = os.path.join(project_path, item)
        if os.path.isdir(item_path) and not item.startswith('.') and item not in ['tests', 'docs', 'artifacts']:
            # Check if it looks like a Python package
            init_py = os.path.join(item_path, '__init__.py')
            if os.path.exists(init_py):
                py_modules.append(item)

    if py_modules:
        action = {
            "type": "create_folder",
            "path": "src/",
            "reason": "Organize source code"
        }
        actions.append(action)

        if not dry_run:
            os.makedirs(src_path)
            print(f"✅ Created src/")

        # Move modules to src/
        for module in py_modules:
            src_module = os.path.join(project_path, module)
            dest_module = os.path.join(src_path, module)

            actions.append({
                "type": "move_folder",
                "from": f"{module}/",
                "to": f"src/{module}/",
                "reason": "Organize source into src/"
            })

            if not dry_run:
                shutil.move(src_module, dest_module)
                print(f"✅ Moved {module}/ → src/{module}/")

    return actions

def organize_documentation(project_path, dry_run):
    """Organize documentation into docs/."""
    actions = []

    docs_path = os.path.join(project_path, "docs")

    # Create docs/ if doesn't exist
    if not os.path.exists(docs_path):
        action = {
            "type": "create_folder",
            "path": "docs/",
            "reason": "Organize documentation"
        }
        actions.append(action)

        if not dry_run:
            os.makedirs(docs_path)
            os.makedirs(os.path.join(docs_path, "design"))
            os.makedirs(os.path.join(docs_path, "notes"))
            os.makedirs(os.path.join(docs_path, "specifications"))
            print(f"✅ Created docs/ structure")

    # Look for documentation folders to move
    doc_folders = ["documentation", "SPECIFICATION", "design", "specs"]

    for folder in doc_folders:
        folder_path = os.path.join(project_path, folder)
        if os.path.exists(folder_path) and os.path.isdir(folder_path):
            # Determine destination
            if folder.lower() in ["specification", "specs"]:
                dest = os.path.join(docs_path, "specifications")
            elif folder.lower() == "design":
                dest = os.path.join(docs_path, "design")
            else:
                dest = os.path.join(docs_path, folder)

            actions.append({
                "type": "move_folder",
                "from": f"{folder}/",
                "to": f"docs/{os.path.basename(dest)}/",
                "reason": "Consolidate documentation"
            })

            if not dry_run:
                if os.path.exists(dest):
                    merge_folders(folder_path, dest)
                    shutil.rmtree(folder_path)
                else:
                    shutil.move(folder_path, dest)
                print(f"✅ Moved {folder}/ → docs/")

    return actions

def handle_migrations(project_path, dry_run):
    """Handle migrations/ folder placement."""
    actions = []

    migrations_path = os.path.join(project_path, "migrations")

    # Check if migrations exist
    if not os.path.exists(migrations_path):
        return actions

    # Check if database project (heuristic)
    is_db_project = detect_database_project(project_path)

    if is_db_project:
        # Keep in root (convention)
        actions.append({
            "type": "keep",
            "path": "migrations/",
            "reason": "Database project - follows Django/Alembic convention"
        })
        print(f"ℹ️  Keeping migrations/ in root (database project)")
    else:
        # Move to artifacts
        dest = os.path.join(project_path, "artifacts/migrations")
        actions.append({
            "type": "move_folder",
            "from": "migrations/",
            "to": "artifacts/migrations/",
            "reason": "Non-database project - minimal root"
        })

        if not dry_run:
            shutil.move(migrations_path, dest)
            print(f"✅ Moved migrations/ → artifacts/migrations/")

    return actions

def detect_database_project(project_path):
    """Detect if project is database-centric."""
    # Check for Django
    if os.path.exists(os.path.join(project_path, "manage.py")):
        return True

    # Check for Alembic
    if os.path.exists(os.path.join(project_path, "alembic.ini")):
        return True

    # Check requirements for database libraries
    req_files = ["requirements.txt", "pyproject.toml"]
    db_indicators = ["django", "alembic", "sqlalchemy", "psycopg", "pymongo"]

    for req_file in req_files:
        req_path = os.path.join(project_path, req_file)
        if os.path.exists(req_path):
            with open(req_path) as f:
                content = f.read().lower()
                if any(indicator in content for indicator in db_indicators):
                    return True

    return False

def merge_folders(src, dest):
    """Merge contents of src folder into dest folder."""
    for item in os.listdir(src):
        src_item = os.path.join(src, item)
        dest_item = os.path.join(dest, item)

        if os.path.isdir(src_item):
            if os.path.exists(dest_item):
                merge_folders(src_item, dest_item)
            else:
                shutil.move(src_item, dest_item)
        else:
            if os.path.exists(dest_item):
                # File exists, add suffix
                base, ext = os.path.splitext(dest_item)
                dest_item = f"{base}_merged{ext}"
            shutil.move(src_item, dest_item)

def update_file_references(project_path, actions):
    """Update file path references in code."""
    print("🔄 Updating file references...")

    # Build replacement map
    replacements = {}
    for action in actions:
        if action["type"] in ["move_folder", "move_file"]:
            old_path = action["from"].rstrip('/')
            new_path = action["to"].rstrip('/')
            replacements[old_path] = new_path

    if not replacements:
        return

    # Update Python files
    py_files = find_python_files(project_path)

    for py_file in py_files:
        try:
            with open(py_file, 'r') as f:
                content = f.read()

            modified = content
            for old, new in replacements.items():
                # Update string paths
                modified = modified.replace(f'"{old}', f'"{new}')
                modified = modified.replace(f"'{old}", f"'{new}")

            if modified != content:
                with open(py_file, 'w') as f:
                    f.write(modified)
                print(f"✅ Updated references in {os.path.relpath(py_file, project_path)}")
        except:
            pass

    # Update config files
    config_files = [".gitignore", "pyproject.toml", "CLAUDE.md", "README.md"]
    for config_file in config_files:
        config_path = os.path.join(project_path, config_file)
        if os.path.exists(config_path):
            try:
                with open(config_path, 'r') as f:
                    content = f.read()

                modified = content
                for old, new in replacements.items():
                    modified = modified.replace(old, new)

                if modified != content:
                    with open(config_path, 'w') as f:
                        f.write(modified)
                    print(f"✅ Updated references in {config_file}")
            except:
                pass

def find_python_files(path):
    """Find all Python files."""
    py_files = []
    for root, dirs, files in os.walk(path):
        # Skip venv, node_modules, etc.
        dirs[:] = [d for d in dirs if d not in ['venv', '__pycache__', '.git', 'node_modules', 'artifacts']]
        py_files.extend([os.path.join(root, f) for f in files if f.endswith('.py')])
    return py_files

def write_migration_report(actions, project_path):
    """Write migration report."""
    report_path = os.path.join(project_path, "MIGRATION_REPORT.md")

    report = f"""# Structure Migration Report

Total actions: {len(actions)}

## Changes Made

"""

    for action in actions:
        if action["type"] == "create_folder":
            report += f"- ✅ Created `{action['path']}`\n"
        elif action["type"] == "move_folder":
            report += f"- ✅ Moved `{action['from']}` → `{action['to']}`\n"
        elif action["type"] == "move_file":
            report += f"- ✅ Moved `{action['from']}` → `{action['to']}`\n"
        elif action["type"] == "keep":
            report += f"- ℹ️  Kept `{action['path']}` ({action['reason']})\n"

    report += f"""

## File References Updated

All path references in Python code and config files have been automatically updated.

## Rollback

If needed, rollback with:

```bash
git reset --hard retrofit-start
git clean -fd
```

## Next Steps

1. Review changes: `git diff retrofit-start`
2. Run tests: `pytest`
3. Commit changes: `git commit -m "Retrofit: Migrate to minimal root structure"`
4. Proceed to Phase 4 (Quality Baseline)

"""

    with open(report_path, 'w') as f:
        f.write(report)

# Main execution
if __name__ == "__main__":
    import sys
    import argparse

    parser = argparse.ArgumentParser(description="Migrate project structure")
    parser.add_argument("project_path", help="Path to project")
    parser.add_argument("--mode", choices=["light", "standard", "full"],
                       default="light", help="Migration mode")
    parser.add_argument("--dry-run", action="store_true",
                       help="Show what would be done without making changes")

    args = parser.parse_args()

    # Run migration
    actions = migrate_structure(args.project_path, args.mode, args.dry_run)

    if args.dry_run:
        print(f"\n📋 {len(actions)} actions would be performed")
        print("Run without --dry-run to apply changes")
    else:
        print(f"\n✅ Migration complete! {len(actions)} actions performed")
        write_migration_report(actions, args.project_path)
        print(f"📊 Report: MIGRATION_REPORT.md")
```

### Running Structure Migration

```bash
# DRY RUN FIRST (see what would happen)
python retrofit_structure.py . --mode=light --dry-run

# Review proposed changes, then run for real
python retrofit_structure.py . --mode=light

# Review changes
git diff
git status

# Test that nothing broke
pytest

# Commit
git add .
git commit -m "Retrofit Phase 3: Migrate to minimal root structure"
```

### Structure Migration Checklist

- [ ] Dry run completed and reviewed
- [ ] Migration mode selected (light/standard/full)
- [ ] Migration executed
- [ ] File references updated automatically
- [ ] Tests still pass
- [ ] Git diff reviewed
- [ ] Migration committed
- [ ] Root folder count reduced to 4-5

---

## Phase 4: Quality Baseline

**Goal**: Install quality tools and establish current baseline.

### Quality Tools Installation

```bash
cd your-project

# Download quality tools setup
curl -O https://[URL]/install_quality_tools.sh

# Run installation
bash install_quality_tools.sh

# This creates:
# .ai-validation/check_quality.sh
# .ai-validation/install_tools.sh
# Updates pyproject.toml with tool configs
```

**OR use existing setup_project.sh script from best-practice folder:**

```bash
# Copy quality tools from a fresh project
/path/to/best-practice/setup_project.sh temp-project
cp -r temp-project/.ai-validation/ your-project/
rm -rf temp-project

# Install tools
cd your-project
bash .ai-validation/install_tools.sh
```

### Run Initial Quality Check

```bash
# Run quality gate (will likely fail on first run)
bash .ai-validation/check_quality.sh

# Save baseline
bash .ai-validation/check_quality.sh > .retrofit/quality_baseline.txt 2>&1

# Review issues
cat .retrofit/quality_baseline.txt
```

### Document Quality Baseline

Create `.retrofit/QUALITY_BASELINE.md`:

```markdown
# Quality Baseline (Pre-Retrofit)

Date: [DATE]

## Current Metrics

- **Test Coverage**: X%
- **Linting Errors**: X
- **Type Errors**: X
- **Security Issues**: X
- **Complexity Violations**: X
- **Docstring Coverage**: X%

## Improvement Targets

### Immediate (Phase 5 Week 1)
- [ ] Fix critical security issues
- [ ] Add docstrings to public functions
- [ ] Fix obvious linting errors

### Short-term (Phase 5 Week 2-4)
- [ ] Increase test coverage to 50%
- [ ] Fix all type errors
- [ ] Reduce complexity violations

### Long-term (Phase 6)
- [ ] Achieve 80% test coverage
- [ ] 100% docstring coverage
- [ ] Zero linting/type/security errors
- [ ] Full quality gate compliance

## Notes

[Add any context about why certain metrics are low, technical debt, etc.]
```

### Quality Baseline Checklist

- [ ] Quality tools installed (.ai-validation/)
- [ ] Initial quality check run
- [ ] Baseline metrics documented
- [ ] Improvement targets set
- [ ] Baseline committed to git

---

## Phase 5: Gradual Enforcement

**Goal**: Incrementally improve code quality without disrupting development.

### Gradual Enforcement Strategy

**Week 1: Soft Enforcement**
- Quality gate runs but doesn't block
- Team sees results, understands standards
- Focus: Quick wins (docstrings, obvious fixes)

**Week 2-3: Partial Enforcement**
- Critical checks block (security, tests exist)
- Other checks warn
- Focus: Test coverage, fix security issues

**Week 4+: Full Enforcement**
- All checks block
- Quality gate must pass before task completion
- Focus: Achieve full compliance

### Gradual Enforcement Configuration

Edit `.ai-validation/check_quality.sh` to add enforcement levels:

```bash
#!/bin/bash
# Quality Gate with Gradual Enforcement

# Read enforcement level from config
ENFORCEMENT_LEVEL="${QUALITY_ENFORCEMENT:-soft}"  # soft, partial, full

echo "🔍 Running quality checks (enforcement: $ENFORCEMENT_LEVEL)"

# ... existing checks ...

# Enforcement logic
case "$ENFORCEMENT_LEVEL" in
  soft)
    # Just report, never fail
    echo "ℹ️  Soft enforcement: Issues reported, not blocking"
    exit 0
    ;;

  partial)
    # Block on critical issues only
    if [ $SECURITY_ISSUES -gt 0 ] || [ $TESTS_FAILED -eq 1 ]; then
      echo "❌ BLOCKED: Critical issues must be fixed"
      exit 1
    else
      echo "⚠️  Non-critical issues found, but not blocking"
      exit 0
    fi
    ;;

  full)
    # Block on any failure
    if [ $ALL_PASSED -eq 0 ]; then
      echo "❌ BLOCKED: All checks must pass"
      exit 1
    else
      echo "✅ All checks passed"
      exit 0
    fi
    ;;
esac
```

### Set Enforcement Level

```bash
# Week 1: Soft
export QUALITY_ENFORCEMENT=soft
echo "export QUALITY_ENFORCEMENT=soft" >> ~/.bashrc

# Week 2: Partial
export QUALITY_ENFORCEMENT=partial

# Week 4: Full
export QUALITY_ENFORCEMENT=full
```

### Weekly Improvement Sprint

**Template for weekly improvement:**

```markdown
# Week X Improvement Sprint

## Focus Area
[e.g., "Increase test coverage" or "Fix type errors"]

## Baseline
- Current metric: X
- Target metric: Y

## Tasks
- [ ] Task 1
- [ ] Task 2
- [ ] Task 3

## Results
- Achieved: Z
- Remaining: W
```

### Gradual Enforcement Checklist

- [ ] Enforcement levels configured
- [ ] Week 1: Soft enforcement active
- [ ] Quick wins completed
- [ ] Week 2-3: Partial enforcement
- [ ] Critical issues resolved
- [ ] Week 4+: Full enforcement
- [ ] All quality gates passing

---

## Phase 6: Full Integration

**Goal**: Enable all MCPs and achieve full best-practice compliance.

### MCP Integration Steps

1. **Install MCPs**
   ```bash
   # Copy MCPs to home directory
   cp memory_mcp.py ~/.mcp-servers/
   cp quality_mcp.py ~/.mcp-servers/
   cp project_mcp.py ~/.mcp-servers/

   # Configure Claude Code
   # Edit ~/.config/claude/claude_desktop_config.json
   ```

2. **Run Objective Clarification**
   ```
   # In Claude Code
   "Run MCP objective clarification on this project"
   # Answer comprehensive questions
   # Achieve clarity score >80
   ```

3. **Generate PROJECT_PLAN.md**
   ```
   "Create PROJECT_PLAN.md based on clarified objective"
   # MCP generates plan in docs/notes/PROJECT_PLAN.md
   ```

4. **Enable Quality Gate Integration**
   ```
   "Enable quality gate enforcement for task completion"
   # MCP now blocks task completion without passing quality gate
   ```

5. **Enable Structure Audits**
   ```
   "Enable automatic structure audits every 5 tasks"
   # MCP monitors minimal root compliance
   ```

6. **Enable Scope Creep Detection**
   ```
   "Enable objective alignment audits every 10 tasks"
   # MCP challenges tasks that don't serve objective
   ```

### Full Integration Checklist

- [ ] All MCPs installed and configured
- [ ] Objective clarified (score >80)
- [ ] PROJECT_PLAN.md generated
- [ ] Quality gate integration active
- [ ] Structure audits enabled
- [ ] Scope creep detection enabled
- [ ] **Full best-practice compliance achieved**

---

## Retrofit Tools Summary

### Tool 1: Assessment Tool
**File**: `retrofit_assess.py`
**Purpose**: Analyze current project state
**Output**: `ASSESSMENT_REPORT.md`, `.retrofit/assessment.json`

### Tool 2: Objective Extraction
**File**: `retrofit_extract_objective.py`
**Purpose**: Reverse-engineer project objective
**Output**: `OBJECTIVE.md`, `.retrofit/objective_extraction.json`

### Tool 3: Structure Migration
**File**: `retrofit_structure.py`
**Purpose**: Consolidate to minimal root
**Output**: `MIGRATION_REPORT.md`, updated structure
**Modes**: light, standard, full

### Tool 4: Quality Baseline
**Script**: From best-practice `.ai-validation/`
**Purpose**: Establish quality baseline
**Output**: `.retrofit/quality_baseline.txt`, `QUALITY_BASELINE.md`

---

## Common Scenarios

### Scenario 1: Legacy Project with 20+ Root Folders

```bash
# Phase 0: Safety
git commit -m "Safe state"
git tag retrofit-start

# Phase 1: Assess
python retrofit_assess.py .
# Result: Structure score 25/100, many clutter folders

# Phase 2: Extract objective
python retrofit_extract_objective.py .
# Fill in OBJECTIVE.md

# Phase 3: Structure migration (FULL mode)
python retrofit_structure.py . --mode=full --dry-run  # Review
python retrofit_structure.py . --mode=full
# Result: 20 folders → 5 folders

# Phase 4: Quality baseline
bash .ai-validation/check_quality.sh
# Result: Baseline documented

# Phase 5: Gradual improvement (4 weeks)
export QUALITY_ENFORCEMENT=soft   # Week 1
export QUALITY_ENFORCEMENT=partial  # Week 2
export QUALITY_ENFORCEMENT=full   # Week 4

# Phase 6: Full MCP integration
# Enable all MCPs, achieve full compliance
```

### Scenario 2: Recent Project, Needs Quality Gates

```bash
# Already has good structure, just needs quality enforcement

# Phase 0: Safety checkpoint
git commit -m "Safe state"

# Phase 1: Quick assessment
python retrofit_assess.py .
# Result: Structure 80/100, Quality 40/100

# Phase 2: Clarify objective
python retrofit_extract_objective.py .
# Already fairly clear, just formalize

# Phase 3: Skip (structure already good)

# Phase 4: Install quality tools
cp -r /path/to/.ai-validation/ .
bash .ai-validation/install_tools.sh

# Phase 5: 2-week gradual enforcement
# Focus on adding tests and docstrings

# Phase 6: Enable MCPs
# Quick integration, already compliant
```

### Scenario 3: Active Project, Can't Disrupt Development

```bash
# Need minimal disruption during retrofit

# Use LIGHT mode for structure migration
python retrofit_structure.py . --mode=light

# Only move logs/ and temp/ to artifacts/
# Leave everything else untouched

# Install quality tools but keep enforcement SOFT
export QUALITY_ENFORCEMENT=soft

# Improve gradually over 8 weeks (slower pace)
# Only enforce fully when team is ready
```

---

## Rollback Procedures

### Rollback Structure Migration

```bash
# Complete rollback to pre-retrofit state
git reset --hard retrofit-start
git clean -fd

# Verify
git status  # Should be clean
ls -la  # Should match original structure
```

### Partial Rollback (Keep Some Changes)

```bash
# Rollback but keep quality tools
git reset --hard retrofit-start
git checkout HEAD -- .ai-validation/

# OR rollback but keep objective
git reset --hard retrofit-start
git checkout HEAD -- OBJECTIVE.md

# Commit selective restoration
git add .
git commit -m "Partial rollback: keeping [X]"
```

### Rollback Checklist

- [ ] Verified backup tag exists (`retrofit-start`)
- [ ] Verified backup branch exists (`retrofit-backup`)
- [ ] Ran rollback command
- [ ] Verified structure restored
- [ ] Tests still pass
- [ ] Team notified of rollback

---

## Success Criteria for Retrofit

### Structure Success
- ✅ Root folders reduced to 4-5
- ✅ All operational data in artifacts/
- ✅ Source code organized (src/, tests/, docs/)
- ✅ Migrations/ in correct location
- ✅ No clutter in root

### Quality Success
- ✅ Quality tools installed (.ai-validation/)
- ✅ Baseline documented
- ✅ Improvement trajectory established
- ✅ Quality gate passing (or clear path to passing)
- ✅ Test coverage improving

### Objective Success
- ✅ Objective documented and clear (score >80)
- ✅ Problem, solution, metrics defined
- ✅ Out-of-scope items explicit
- ✅ Success criteria measurable
- ✅ PROJECT_PLAN.md exists

### Process Success
- ✅ All changes reversible (git tags/branches)
- ✅ Tests still passing
- ✅ Development not disrupted
- ✅ Team understands new structure
- ✅ Gradual enforcement working

### Integration Success
- ✅ MCPs installed and configured
- ✅ Quality gate blocks task completion
- ✅ Structure audits running
- ✅ Scope creep detected
- ✅ **Full best-practice compliance achieved**

---

## Conclusion

This retrofit methodology allows ANY existing Claude project to adopt the complete MCP + Best Practice system gradually and safely.

**Key Principles**:
1. **Safety First** - All changes reversible
2. **Gradual Adoption** - Phase in improvements
3. **Non-Disruptive** - Development continues
4. **Measurable Progress** - Track improvement
5. **Flexible Enforcement** - Choose when to enforce

**Timeline**: Express (1-2 weeks) to Cautious (4-8 weeks)

**Result**: Projects transformed to have clear objectives, minimal structure, quality enforcement, and MCP-powered excellence.

---

**Ready to retrofit your first project!**
