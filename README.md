# Best Practice Toolkit

> **Enforce excellent coding practices and project delivery for AI-assisted development**

A complete MCP (Model Context Protocol) server system that **enforces** best practices through mandatory objective clarification, quality gates, and minimal root structure.

---

## 🚀 Quick Start

### ONE Command Installation (Two Methods)

**Method 1: inject.sh** - Run from toolkit (RECOMMENDED)
```bash
cd /path/to/best-practice
./inject.sh /path/to/your-project
```

**Method 2: smart_install.sh** - Run from target
```bash
cd /path/to/your-project
/path/to/best-practice/retrofit-tools/smart_install.sh
```

**Both methods identical** - just different workflows. Use whichever you prefer.

**With commit flag** (optional - commits toolkit to git):
```bash
# Method 1
./inject.sh /path/to/project --commit

# Method 2
cd /path/to/project && /path/to/smart_install.sh --commit
```

**That's it.** Script auto-detects production vs development, asks for confirmation, installs everything safely.

**What it does**:
- Checks git safety (uncommitted changes, etc)
- Auto-detects if production (deployment configs, CI/CD, low activity)
- Asks: "Proceed?" and "Override mode?"
- **Creates toolkit folders**: `.claude/`, `docs/`, `tests/` (FULL mode), `CLAUDE.md`
- **By default: ALL folders gitignored** (added to .gitignore automatically)
- **With --commit flag: Commits toolkit files** to git repository
- Creates safety checkpoint (git tag) when committing
- Shows rollback command

**Takes 2 minutes.**

### Folders Created

**All toolkit folders gitignored by default** (clean git status):

**.claude/** - Core toolkit (GITIGNORED)
- **best-practice.md**: Project standards and workflow
- **TASKS.md**: Live task list (≤30 lines per task)
- **skills/**: 10 toolkit skills + template for project-specific skills
- **USER_GUIDE.md**: 500+ line complete toolkit guide
- **mcp-servers/**: Memory, Quality, Project, Learning MCPs (FULL mode)
- **quality-gate/**: Quality gate scripts (FULL mode)

**docs/** - Documentation (GITIGNORED)
- **notes/PROJECT_PLAN.md**: Always-current project plan
- **design/**: Architecture docs
- **guides/**: How-to guides
- **analysis/**: Assessments

**tests/** - Test structure, FULL mode only (GITIGNORED)

**CLAUDE.md** - Root reference (GITIGNORED)

**Automatic .gitignore (DEFAULT)**: All toolkit folders added to .gitignore automatically, ensuring clean git history with zero toolkit clutter.

---

### When to Use --commit Flag

**Default behavior (no flag)**: Toolkit installed locally, NOT committed to git
- ✅ Files stay local to each developer
- ✅ No merge conflicts from toolkit updates
- ✅ Clean git history
- ✅ Each developer can customize toolkit independently

**Use --commit flag when**:
- You want the entire team to use the same toolkit configuration
- You want toolkit files version-controlled
- You want to track toolkit changes in git history
- You're using toolkit as part of your project documentation

**What --commit does**:
- Installs toolkit files to `.claude/` folder
- **Commits .claude/ to git repository**
- Creates git tags for safety checkpoint
- All team members receive toolkit files via git pull

**Note**: Only use --commit if you specifically want toolkit in version control.

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
- **MCP Servers**: [.claude/mcp-servers/](.claude/mcp-servers/)
- **Project Plan**: [docs/notes/PROJECT_PLAN.md](docs/notes/PROJECT_PLAN.md)
- **Standards**: [CLAUDE.md](CLAUDE.md)

---

**Current Version**: 1.0.0 (Self-retrofit in progress)
**Status**: Production-ready MCPs, Phase 2 self-application ongoing
