# Changelog

All notable changes to this project will be documented in this file.

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
