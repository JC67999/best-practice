---
name: File Placement Rules
description: Minimal root structure and file organization standards
tags: structure, organization, files, folders, placement
auto_load_triggers: create, new file, folder, where to put, structure
priority: toolkit
---

# File Placement Rules

## Purpose

Enforces minimal root directory structure (≤5 folders) and proper file organization to prevent sprawl and maintain clean project structure.

---

## Root Directory Rules

### Allowed Folders (5 Maximum)

```
/mcp-servers/     - MCP server implementations
/tests/           - Test suite for all code
/docs/            - ALL documentation
/dist/            - Distribution packages (generated)
/retrofit-tools/  - Retrofit assessment scripts
```

### Allowed Files (Keep Minimal)

```
/README.md        - Brief project overview (link to docs/)
/CLAUDE.md        - Project standards
/package_toolkit.sh - Build script
/.gitignore       - Git ignore rules
/LICENSE          - MIT license (generated)
```

### FORBIDDEN in Root

- ❌ Documentation files (*.md except README.md and CLAUDE.md)
- ❌ Configuration files (move to .config/ or appropriate subdir)
- ❌ Data files (move to docs/references/ or artifacts/)
- ❌ Log files (use /logs if needed, add to .gitignore)
- ❌ Temporary files (use /temp if needed, add to .gitignore)

---

## Documentation Structure

**ALL documentation goes in `/docs/`**:

```
/docs/
├── README.md          - Comprehensive documentation index
├── design/            - Architecture and system design
├── guides/            - How-to guides and methodology
├── analysis/          - Assessments and analysis
├── references/        - Reference materials and examples
└── notes/             - Planning and status
```

---

## Source Code Structure

**MCP Servers** (`/mcp-servers/`):
```
/mcp-servers/
├── memory_mcp.py       - Context persistence MCP
├── quality_mcp.py      - Quality enforcement MCP
├── project_mcp.py      - Objective clarification MCP
├── requirements.txt    - Python dependencies
└── README.md           - Installation and usage
```

**Tests** (`/tests/`):
```
/tests/
├── test_memory_mcp.py
├── test_quality_mcp.py
├── test_project_mcp.py
├── conftest.py         - Pytest configuration
└── README.md           - Testing documentation
```

---

## Hidden Directories

**Configuration**:
```
/.claude/            - Claude Code configuration
/.ai-validation/     - Quality gate scripts
/.git/               - Git repository
```

---

## Decision Tree: Where to Put New Files

**Creating new file? Ask**:

1. **Is it documentation?**
   - YES → `/docs/[category]/filename.md`
   - NO → Continue

2. **Is it source code?**
   - MCP server → `/mcp-servers/`
   - Test file → `/tests/`
   - Build script → Root (if essential)
   - NO → Continue

3. **Is it configuration?**
   - YES → `/.config/` or appropriate hidden dir
   - NO → Continue

4. **Is it temporary/generated?**
   - YES → `/temp/` or `/dist/` + add to .gitignore
   - NO → Continue

5. **Still unsure?**
   - **Challenge the need** - Do you really need this file?
   - If yes, ask user for placement decision

---

## Enforcement

**Before creating any new file**:
1. Check root folder count (must be ≤5)
2. Verify file belongs in target location
3. If creating new root folder → **STOP and challenge**

**Use MCP tools**:
```
mcp__quality__validate_file_placement
Args: project_path = current working directory

mcp__quality__audit_project_structure
Args: project_path = current working directory
```

---

## Success Metrics

**Structure compliance**:
- Root folders ≤5
- All docs in docs/
- No forbidden files in root

---

## Resources

- **CLAUDE.md**: Full file placement rules (section: File Placement Rules)
- **Quality MCP**: validate_file_placement, audit_project_structure tools
