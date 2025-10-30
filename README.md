# Best Practice Toolkit

> **Enforce excellent coding practices and project delivery for AI-assisted development**

A complete MCP (Model Context Protocol) server system that **enforces** best practices through mandatory objective clarification, quality gates, and minimal root structure.

---

## 🚀 Quick Start

### ONE Command Installation

**Option 1: Full Install (commits to git)**
```bash
cd /path/to/your/project
/home/jc/CascadeProjects/best-practice/retrofit-tools/smart_install.sh
```

**Option 2: Local Only (for live projects - NO git commits)**
```bash
cd /path/to/your/live/project
/home/jc/CascadeProjects/best-practice/retrofit-tools/smart_install.sh --local-only
```

**That's it.** Script auto-detects production vs development, asks for confirmation, installs everything safely.

**What it does**:
- Checks git safety (uncommitted changes, etc)
- Auto-detects if production (deployment configs, CI/CD, low activity)
- Asks: "Proceed?" and "Override mode?"
- Creates safety checkpoint (git tag) - UNLESS --local-only
- Installs toolkit
- Commits changes - OR adds to .gitignore if --local-only
- Shows rollback command

**Takes 2 minutes.**

---

### When to Use --local-only

**Use --local-only for**:
- Live/production projects
- Projects you don't want to modify in git
- Personal development tooling only
- Testing the toolkit without commitment

**What --local-only does**:
- Installs all toolkit files locally
- Adds toolkit to .gitignore automatically
- Does NOT create git commits
- Does NOT create git tags
- Files stay local, never pushed to GitHub

**Perfect for**: Using best practices on live projects without changing the repository.

---

## ✨ Key Features

**🎯 Mandatory Objective Clarification**
- 10-15 question interrogation before any work
- Vague answer detection with drill-down
- Clarity score >80 required

**✅ Quality Gates That Block**
- Tests ≥80% coverage (enforced)
- Zero linting/type/security errors
- Structure compliance validation
- Cannot proceed without passing

**📁 Minimal Root Structure**
- 4-5 folders maximum enforced
- Automatic file placement validation
- Prevents codebase clutter

**💾 Persistent Context**
- Sessions preserved across conversations
- No context loss between sessions
- Project objectives stored permanently

**🎨 Retrofittable**
- Works with existing projects
- Non-destructive migration
- Gradual enforcement (light → full)

---

## 📊 Results

**3-5x productivity increase** while maintaining:
- 80%+ test coverage
- Zero blocking errors
- Minimal root structure
- Clear project objectives

---

## 📚 Documentation

**Full documentation**: [docs/README.md](docs/README.md)

**Quick Links**:
- [Installation Guide](docs/README.md#installation)
- [MCP Implementation](docs/design/MCP_IMPLEMENTATION_APPROACH.md)
- [Retrofit Methodology](docs/guides/RETROFIT_METHODOLOGY.md)
- [Project Plan](docs/notes/PROJECT_PLAN.md)

---

## 🏗️ What's Included

**MCP Servers** (4):
- `memory_mcp.py` - Context persistence
- `quality_mcp.py` - Quality enforcement
- `project_mcp.py` - Objective clarification
- `learning_mcp.py` - Adaptive learning from feedback

**Slash Commands** (8):
- `/brainstorm` - Structured brainstorming (divergent → convergent)
- `/plan` - Planning Mode with task breakdown
- `/spec` - Feature specifications with scope reduction
- `/tdd` - Test-driven development (RED-GREEN-REFACTOR)
- `/execute-plan` - Execute plans with auto checkpoints
- `/debug` - Systematic debugging (root cause → fix)
- `/checkpoint` - Git safety checkpoints
- `/mcp` - Scaffold new MCP servers

**Retrofit Tools** (3):
- `retrofit_assess.py` - Project health assessment
- `retrofit_extract_objective.py` - Objective extraction
- `retrofit_structure.py` - Structure migration

**Documentation** (180KB+):
- Complete implementation guide
- Retrofit methodology
- CSO framework integration
- Autonomous mode roadmap

---

## 🔧 Requirements

- Claude Code CLI
- Python 3.10+
- Git

---

## 📝 Project Standards

See [CLAUDE.md](CLAUDE.md) for:
- File placement rules
- Development workflow
- Code quality standards
- Git conventions

---

## 🗺️ Roadmap

- ✅ **Phase 1**: Core MCP system (COMPLETE)
- ⏳ **Phase 2**: Self-retrofit + test suite (IN PROGRESS)
- 📋 **Phase 3**: Autonomous mode (PLANNED)
- 📋 **Phase 4**: Community testing
- 📋 **Phase 5**: Production v2.0

---

## 🤝 Contributing

This project practices what it preaches - it uses its own best practices:
- Minimal root structure
- Quality gates enforced
- Clear objectives (see [PROJECT_PLAN.md](docs/notes/PROJECT_PLAN.md))
- Test coverage >80%

---

## 📄 License

MIT License - see [LICENSE](LICENSE) for details

---

## 🔗 Links

- **Documentation**: [docs/README.md](docs/README.md)
- **MCP Servers**: [mcp-servers/](mcp-servers/)
- **Project Plan**: [docs/notes/PROJECT_PLAN.md](docs/notes/PROJECT_PLAN.md)
- **Standards**: [CLAUDE.md](CLAUDE.md)

---

**Current Version**: 1.0.0 (Self-retrofit in progress)
**Status**: Production-ready MCPs, Phase 2 self-application ongoing
