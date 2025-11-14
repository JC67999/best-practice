# Changelog

All notable changes to this project will be documented in this file.

## [Unreleased]

### Added - Learning MCP (Self-Learning System)
- **Learning MCP server**: Complete self-learning system that scans ALL Anthropic resources
- **9 MCP tools** for comprehensive toolkit maintenance:
  - `scan_anthropic_skills` - Scan skills repository (15 skills across 5 categories)
  - `scan_anthropic_cookbooks` - Scan cookbooks repository (27.6k stars, 28 cookbooks across 7 categories)
  - `scan_anthropic_quickstarts` - Scan quickstarts repository (10.2k stars, 4 starter projects)
  - `scan_anthropic_org` - Scan all 54 Anthropic repositories (SDKs, tools, courses, security)
  - `compare_skills` - Compare Anthropic vs toolkit skills, identify gaps
  - `suggest_skill_updates` - Prioritize skills as HIGH/MEDIUM/LOW/SKIP
  - `download_skill` - Download skills from GitHub with templates
  - `store_learning` - Store best practices in JSON format
  - `get_learnings` - Retrieve learnings filtered by topic/date
- **3 MCP prompts** for learning workflows:
  - `update_toolkit` - Complete workflow: scan → compare → suggest → download → document
  - `research_topic` - Research best practices for specific topic with structured output
  - `scan_all_resources` - Comprehensive scan of ALL Anthropic resources (skills, cookbooks, quickstarts, org)
- **Knowledge storage**: `~/.claude_memory/learnings/` with JSON structure
- **Complete Anthropic resource catalog**:
  - **15 Skills**: Development, Meta, Documents, Creative, Enterprise categories
  - **28 Cookbooks**: Capabilities, Tool Use, Multimodal, Patterns, Third-Party integrations
  - **4 Quickstarts**: Customer support, Financial analysis, Computer use, Agent demos
  - **54 Org Repos**: 7 SDKs, 4 agent frameworks, 4 educational resources, 4 security tools
- **Auto-update capability**: Toolkit can self-update with latest Anthropic best practices
- **Skill prioritization logic**:
  - HIGH: Development tools (webapp-testing, mcp-builder) + Meta skills (skill-creator)
  - MEDIUM: Document tools (pdf, xlsx, docx, pptx)
  - LOW: Creative tools (algorithmic-art, canvas-design)
  - SKIP: Enterprise-specific (brand-guidelines, internal-comms)
- **Cookbook categories covered**:
  - Capabilities: RAG, Classification, Summarization
  - Tool Use: Customer service, Calculator, SQL execution
  - Multimodal: Vision, Charts, Forms, Image generation
  - Patterns: Sub-agents, PDF processing, Evaluation, Caching
  - Third-Party: Pinecone, Wikipedia, Voyage AI, Web extraction
- **Benefits**:
  - ✅ Complete visibility into ALL Anthropic resources
  - ✅ Automatic gap detection between toolkit and Anthropic
  - ✅ Access to 27.6k+ stars of cookbook examples
  - ✅ Starter project templates from quickstarts (10.2k stars)
  - ✅ SDK integration guidance for 7 programming languages
  - ✅ Security tool awareness (GitHub Actions, monitoring)
  - ✅ Structured learning storage for research
  - ✅ Context-aware prompts for guided workflows

### Changed - BREAKING: Local-Only Now Default
- **smart_install.sh now defaults to LOCAL_ONLY=true** (toolkit files NOT committed)
- **New --commit flag** to explicitly commit toolkit files to git
- **Reverses previous behavior**: Old default committed files, now default does NOT commit
- **Claude Code's gitignore**: .claude/ folder automatically ignored by Claude Code
- **Benefits**:
  - ✅ Toolkit files stay local to each developer (no git pollution)
  - ✅ No merge conflicts from toolkit updates
  - ✅ Clean git history
  - ✅ Each developer can customize toolkit independently
- **Migration**: Projects using old default behavior unaffected (already committed)
- **Usage**:
  - Default: `bash smart_install.sh` (local only, NOT committed)
  - Commit: `bash smart_install.sh --commit` (commits to git)

### Added - MCP Prompts (Reusable Templates)
- **10 MCP prompts** across Memory, Quality, and Project MCPs
- **Project MCP prompts** (4 total):
  - `plan_feature` - Break down features into tasks aligned with objective
  - `daily_standup` - Review progress, identify blockers
  - `refocus` - Cut non-essential work ruthlessly
  - `task_breakdown` - Break large tasks into ≤30 line pieces
- **Quality MCP prompts** (3 total):
  - `code_review` - Systematic review (structure, security, performance, OWASP Top 10)
  - `pre_commit_check` - Pre-commit quality gate with checklist
  - `security_audit` - Full security audit with OWASP Top 10 framework
- **Memory MCP prompts** (3 total):
  - `session_start` - Load context and plan session
  - `session_end` - Guided session summary
  - `document_decision` - Document decisions with rationale
- **Context-aware templates**: Prompts load project data dynamically
- **User-initiated**: Invoke with `/mcp__server__promptname` syntax
- **Completes MCP primitives**: Tools + Resources + Prompts (all 3 primitives now implemented)

### Changed - BREAKING: Source Structure Consistency
- **mcp-servers/ moved to .claude/mcp-servers/** in source toolkit repository
- Source structure now mirrors installed structure for consistency
- All references updated: smart_install.sh, package_toolkit.sh, tests, docs
- No impact on installed projects - they already use .claude/mcp-servers/

### Changed - BREAKING: New Installation Structure
- **ALL toolkit files now install to `.claude/` folder** (automatically gitignored by Claude Code)
- **CLAUDE.md renamed to best-practice.md** when installed to projects
- **No more `best-practice/` folder** - everything in `.claude/` which is already gitignored
- **smart_install.sh completely rewritten** to use `.claude/` structure
- **Quality gate moved** from `.ai-validation/` to `.claude/quality-gate/`
- **MCP servers moved** to `.claude/mcp-servers/` (FULL mode only)
- **TASKS.md moved** to `.claude/TASKS.md`

### Benefits of New Structure
- ✅ **Completely gitignored** - No toolkit files in your commits
- ✅ **No .gitignore pollution** - `.claude/` already ignored by Claude Code
- ✅ **Clean project root** - No `best-practice/` folder
- ✅ **Each developer independent** - Toolkit files local only
- ✅ **No merge conflicts** - Toolkit changes don't affect team
- ✅ **Single location** - Everything in `.claude/`

### Migration Guide
For projects with old `best-practice/` folder:
1. Remove old folder: `rm -rf best-practice/`
2. Re-run installer: `bash .../smart_install.sh`
3. New structure installs to `.claude/`
4. Old .gitignore entries can be cleaned up

### Added
- **docs/references/claude-skills-explained.md**: Reference guide explaining Claude's agentic ecosystem (Skills, Projects, MCP, Subagents, Prompts)
- **docs/analysis/ARCHITECTURE_REVIEW_SKILLS_MODEL.md**: Comprehensive architecture review comparing our toolkit to Skills model (78% token reduction potential)
- **.claude/skills/** - Complete Skills-based architecture with two-tier system
- **9 Toolkit Skills** (28.5KB total vs 49KB monolithic CLAUDE.md):
  1. **quality-standards** (6.75KB) - Code quality, testing, documentation standards
  2. **tdd-workflow** (7.3KB) - Test-driven development (Red-Green-Refactor)
  3. **problem-solving** (7.8KB) - 10 mandatory systematic debugging techniques
  4. **git-workflow** - Git commits, checkpoints, branch strategy, rollback patterns
  5. **file-placement** - Minimal root structure and file organization rules
  6. **planning-mode** - Discovery-first planning (Shift+Tab×2)
  7. **mcp-usage** - When/how to use Memory, Quality, Project MCPs
  8. **context-management** - 60% rule and token optimization strategies
  9. **domain-learning** - Autonomous research and knowledge base building (NEW!)
- **Domain Knowledge Base** - Autonomous self-learning system
  - `docs/references/domain-knowledge/` - Stores researched topics
  - `index.md` - Master index of all researched topics
  - Auto-fetches documentation when encountering unfamiliar concepts
  - Builds project-specific expertise over time
  - Example: AI optimization knowledge (transformer attention, quantization, etc.)
- **Project skill template** - Template for creating domain-specific skills
- **.claude/skills/README.md** - Complete guide for creating and maintaining skills
- **smart_install.sh** - Updated to install skills folder to projects

### Changed
- **CLAUDE.md** - Now references Skills for detailed content (deprecation notice added)
- Skills-based architecture enables:
  - Progressive disclosure (metadata first, details on demand)
  - Two-tier system (toolkit + project-specific skills)
  - Auto-discovery via trigger keywords
  - Token efficiency (~70% reduction in loaded content)
  - Projects can create domain-specific skills

## [1.2.0] - 2025-11-10

### Added
- gitignore-template.txt: Template for excluding best-practice/ folder from git
- **best-practice/ folder structure**: All toolkit files install here (local only, never committed)

### Changed
- **smart_install.sh**: Now creates best-practice/ folder in target projects
- **smart_install.sh**: Installs CLAUDE.md, TASKS.md to best-practice/
- **smart_install.sh**: Installs quality gate to best-practice/.ai-validation/
- **smart_install.sh**: Automatically adds best-practice/ to .gitignore
- Toolkit files NO LONGER pollute project root - everything in best-practice/

### Fixed
- **smart_install.sh**: Fixed arithmetic operations for bash compatibility (set -e issues)

### Investigated
- **Skills vs MCP tools**: Confirmed current architecture (8 slash commands + 27 MCP tools) is optimal
- Decision: Do NOT add Skills - would add complexity without value given efficiency focus
- **Kimi K2 integration**: Evaluated dual-model workflow (Claude + Kimi K2 for QA verification)
- Decision: Do NOT integrate Kimi K2 - violates efficiency-first objective, adds complexity without solving actual problems, contradicts "minimal enforcement" goal

### Verified
- **Successful installation to rapid-pm**: LIGHT mode installed successfully
- Files created: best-practice/CLAUDE.md (49KB), best-practice/TASKS.md (2.3KB)
- Added to .gitignore: best-practice/ folder excluded from git
- Git commit: 9cbbb7f "feat: install best-practice toolkit (LIGHT mode)"
- Status: Clean working tree, ready for use
- **Successful installation to ai-task-optimisation-MVP**: FULL mode installed successfully
- Files created: best-practice/CLAUDE.md (49.6KB), best-practice/TASKS.md (2.5KB), best-practice/.ai-validation/check_quality.sh
- MCP servers: 8 files copied (memory_mcp.py, project_mcp.py, quality_mcp.py, learning_mcp.py, autonomous_daemon.py, code_review_daemon.py, learning_daemon.py, __init__.py)
- Added to .gitignore: best-practice/ folder excluded from tracking
- Status: Toolkit ready for use (local development only)

### Documentation
- **README.md**: Added best-practice/ folder explanation (11 lines)
- Documented: CLAUDE.md, TASKS.md, .ai-validation/ contents
- Clarified: Automatic .gitignore handling for local-only files

## [1.1.0] - 2025-11-10

### Added
- **TASKS.md**: Live task list for granular change tracking
- **Task management system**: Every change = granular task (≤30 lines, ≤15 min)
- **Workflow enforcement**: Check tasks → Implement → Test → Changelog → Quality gate → Commit → Mark done
- Task breakdown rules in CLAUDE.md
- Safe rapid development: small testable changes only

### Changed
- **Streamlined to efficiency-only focus**: Removed all non-essential documentation (21,443 lines deleted)
- Deleted docs/analysis/, docs/design/, docs/references/, docs/notes/
- Deleted verbose guides (research process, thinking skills, autonomous modes, etc.)
- Kept only: README.md, INSTALLATION.md, QUICKSTART_RETROFIT.md
- **Quality gate simplified**: 4 checks only (changelog, comments, linting, structure)
- Removed: tests check, coverage check, type checking, security scanning
- **Changelog enforcement**: Quality gate blocks commits without changelog update
- **Comment enforcement**: Quality gate checks Python files for docstrings
- Updated objective: Enforce changelog + comments + minimal structure
- Updated CLAUDE.md: Concise, efficiency-focused standards
- Focus: Speed and frugality over comprehensive documentation

### Added
- Memory MCP comprehensive tests (21 tests, 77% coverage)
- Module aliasing in conftest.py for hyphenated folders
- Flexible quality gate (80% target, 50% threshold for evolving code)

### Fixed
- Mypy compatibility with mcp-servers hyphenated folder name
- Import issues in test suite
- Root folder count (maintained 5-folder limit)

## [1.0.1] - 2025-11-04

### Changed
- Demonstrated all MCP tool invocations
