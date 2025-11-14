# Injection Quick Reference

> **One-page visual guide to toolkit injection**

## 🚀 One Command Installation

```bash
cd /path/to/your-project
/path/to/best-practice/retrofit-tools/smart_install.sh
```

---

## 📁 Folder Structure: Before → After

### LIGHT Mode (Production-Safe)

```
BEFORE                          AFTER
══════                          ═════

my-project/                     my-project/
├── src/                        ├── src/
├── README.md                   ├── .claude/              ← NEW (GITIGNORED)
├── package.json                │   ├── best-practice.md  (49KB standards)
└── ...                         │   ├── TASKS.md          (task list)
                                │   ├── USER_GUIDE.md     (toolkit guide)
                                │   └── skills/           (10 skills)
                                ├── docs/                 ← NEW (organized)
                                │   ├── design/
                                │   ├── guides/
                                │   ├── analysis/
                                │   ├── references/
                                │   └── notes/
                                │       └── PROJECT_PLAN.md
                                ├── CLAUDE.md             ← NEW (root ref)
                                ├── README.md             (unchanged)
                                ├── package.json          (unchanged)
                                └── ...                   (unchanged)
```

### FULL Mode (Development)

```
BEFORE                          AFTER
══════                          ═════

my-project/                     my-project/
├── src/                        ├── src/
├── README.md                   ├── .claude/              ← NEW (GITIGNORED)
└── ...                         │   ├── best-practice.md
                                │   ├── TASKS.md
                                │   ├── USER_GUIDE.md
                                │   ├── skills/           (10 skills)
                                │   ├── quality-gate/     ← FULL only
                                │   │   └── check_quality.sh
                                │   └── mcp-servers/      ← FULL only
                                │       ├── memory_mcp.py
                                │       ├── quality_mcp.py
                                │       ├── project_mcp.py
                                │       ├── learning_mcp.py
                                │       └── README.md
                                ├── docs/
                                │   └── notes/
                                │       └── PROJECT_PLAN.md
                                ├── tests/                ← FULL only
                                │   └── test_basic.py
                                ├── CLAUDE.md
                                ├── README.md
                                └── ...
```

---

## 🎯 What Gets Installed

### Files by Size

| File                              | Size   | Mode  | Git Status     |
|-----------------------------------|--------|-------|----------------|
| `.claude/best-practice.md`        | 49KB   | Both  | GITIGNORED ✅  |
| `.claude/USER_GUIDE.md`           | 35KB   | Both  | GITIGNORED ✅  |
| `.claude/skills/` (10 files)      | 26KB   | Both  | GITIGNORED ✅  |
| `.claude/TASKS.md`                | 1KB    | Both  | GITIGNORED ✅  |
| `.claude/mcp-servers/` (4 files)  | 170KB  | FULL  | GITIGNORED ✅  |
| `.claude/quality-gate/`           | 5KB    | FULL  | GITIGNORED ✅  |
| `CLAUDE.md`                       | 2KB    | Both  | GITIGNORED ✅  |
| `docs/notes/PROJECT_PLAN.md`      | 2KB    | Both  | GITIGNORED ✅  |
| `tests/test_basic.py`             | 1KB    | FULL  | GITIGNORED ✅  |

**Total** (ALL GITIGNORED):
- **LIGHT**: ~115KB (all local, zero git footprint)
- **FULL**: ~291KB (all local, zero git footprint)

---

## 🔄 Two Modes Comparison

### Auto-Detection

```
┌──────────────────────────────────────────────────────────┐
│ Project Analysis                                          │
├──────────────────────────────────────────────────────────┤
│                                                           │
│  ✓ Low activity (<5 commits/30d)        = +1 point       │
│  ✓ Deployment config (Docker)           = +1 point       │
│  ✓ CI/CD (.github/workflows)            = +1 point       │
│  ✓ Production env (.env.production)     = +1 point       │
│                                                           │
│  Score: 3/4                                               │
│                                                           │
│  ≥2 points → LIGHT mode (production-safe)                │
│  <2 points → FULL mode (complete retrofit)               │
│                                                           │
└──────────────────────────────────────────────────────────┘
```

### Mode Differences

| Feature                    | LIGHT | FULL |
|----------------------------|-------|------|
| Standards (CLAUDE.md)      | ✅    | ✅   |
| Skills (10 files)          | ✅    | ✅   |
| USER_GUIDE.md              | ✅    | ✅   |
| TASKS.md                   | ✅    | ✅   |
| PROJECT_PLAN.md            | ✅    | ✅   |
| Quality gate               | ❌    | ✅   |
| MCP servers (4)            | ❌    | ✅   |
| Test structure             | ❌    | ✅   |
| **Enforcement**            | None  | Full |
| **Risk**                   | Zero  | Low  |

---

## 🔐 Git Behavior

### Default: Local-Only (Recommended)

```
┌──────────────────────────────────────────────────────────┐
│ ALL toolkit folders = GITIGNORED (automatic)             │
├──────────────────────────────────────────────────────────┤
│                                                           │
│  $ git status                                             │
│  On branch main                                           │
│  nothing to commit, working tree clean                    │
│                                                           │
│  Gitignored folders:                                      │
│    • .claude/ (standards, skills, MCPs)                   │
│    • docs/ (project documentation)                        │
│    • tests/ (test structure, FULL mode)                   │
│    • CLAUDE.md (root reference)                           │
│                                                           │
│  Benefits:                                                │
│  ✅ Zero git pollution                                    │
│  ✅ Clean git history (only product code)                 │
│  ✅ No merge conflicts                                    │
│  ✅ Each developer independent                            │
│  ✅ Toolkit updates don't create git noise               │
│                                                           │
└──────────────────────────────────────────────────────────┘
```

### With --commit Flag

```bash
/path/to/best-practice/retrofit-tools/smart_install.sh --commit
```

```
┌──────────────────────────────────────────────────────────┐
│ .claude/ folder = COMMITTED (tracked in git)             │
├──────────────────────────────────────────────────────────┤
│                                                           │
│  $ git status                                             │
│  On branch main                                           │
│  Changes to be committed:                                 │
│    new file:   .claude/best-practice.md                   │
│    new file:   .claude/skills/quality-standards.md       │
│    ...                                                    │
│                                                           │
│  Benefits:                                                │
│  ✅ Shared team standards                                │
│  ✅ Versioned toolkit                                     │
│  ✅ Reviewable in PRs                                     │
│  ✅ No configuration drift                                │
│                                                           │
└──────────────────────────────────────────────────────────┘
```

---

## 💻 How Projects Use Toolkit

### Automatic Discovery

```
Developer opens Claude Code in project
           ↓
Claude Code automatically reads:
           ↓
    ┌──────────────────────────────────┐
    │ 1. CLAUDE.md (root reference)    │
    │ 2. .claude/best-practice.md      │
    │ 3. .claude/skills/ (on-demand)   │
    │ 4. .claude/TASKS.md              │
    └──────────────────────────────────┘
           ↓
Standards enforced automatically
No manual configuration required
```

### Skills Loading (Progressive Disclosure)

```
User: "How do I test this?"
           ↓
Claude loads: .claude/skills/tdd-workflow.md (~3KB)
           ↓
User gets TDD guidance


User: "Where should this file go?"
           ↓
Claude loads: .claude/skills/file-placement.md (~2KB)
           ↓
User gets file placement rules


User: "Debug this error"
           ↓
Claude loads: .claude/skills/problem-solving.md (~4KB)
           ↓
User gets 10 debugging techniques
```

**vs loading entire CLAUDE.md**: 49KB every time
**Savings**: 94% token reduction

---

## 🛡️ Safety Features

### 1. Git Checkpoint

```bash
✅ Before: git tag retrofit-start
✅ Rollback: git reset --hard retrofit-start
```

### 2. Non-Destructive

```
NEVER:
❌ Deletes existing files
❌ Modifies source code
❌ Changes config files
❌ Alters build process

ONLY:
✅ Creates new folders
✅ Moves documentation
✅ Adds toolkit files
```

### 3. Validation

```
After installation:
✅ All files created
✅ Sizes correct
✅ Permissions set
✅ No errors
```

---

## ⚡ Quick Commands

### Install

```bash
# Default (LIGHT/FULL auto-detected, local-only)
cd /path/to/project
/path/to/best-practice/retrofit-tools/smart_install.sh

# Force FULL mode + commit to git
/path/to/best-practice/retrofit-tools/smart_install.sh --commit
```

### Verify

```bash
# Check installation
ls .claude/
ls docs/notes/PROJECT_PLAN.md

# Check gitignore status
git status

# View standards
cat CLAUDE.md
cat .claude/best-practice.md
```

### Use

```bash
# Open project in Claude Code
code .

# Claude automatically sees:
# - CLAUDE.md
# - .claude/best-practice.md
# - .claude/skills/
# - .claude/TASKS.md

# No manual configuration needed
```

### Rollback (if needed)

```bash
git reset --hard retrofit-start
git clean -fd
git tag -d retrofit-start
```

---

## 📊 Typical Timeline

```
┌─────────────────────────────────────────────────────────┐
│ Installation Timeline                                    │
├─────────────────────────────────────────────────────────┤
│                                                          │
│  0:00  Run smart_install.sh                             │
│  0:05  Analyze project (auto-detect mode)               │
│  0:10  Confirm settings                                  │
│  0:15  Create structure                                  │
│  0:30  Organize docs                                     │
│  0:45  Install toolkit files                             │
│  1:00  Verify installation                               │
│  1:30  Validation complete                               │
│                                                          │
│  Total: <2 minutes                                       │
│                                                          │
└─────────────────────────────────────────────────────────┘
```

---

## 🎯 Decision Tree

```
┌─────────────────────────────────────────────────────────┐
│ Which mode should I use?                                 │
└─────────────────────────────────────────────────────────┘
                      ↓
        Is project in production?
                      ↓
          ┌───────────┴───────────┐
          │                       │
         YES                     NO
          │                       │
    ┌─────▼──────┐          ┌────▼──────┐
    │ LIGHT mode │          │ FULL mode │
    │  (safe)    │          │ (complete)│
    └────────────┘          └───────────┘
          │                       │
          ▼                       ▼
    No disruption          Quality gates
    Standards only         MCP automation
    Skills available       Full enforcement


┌─────────────────────────────────────────────────────────┐
│ Should I use --commit flag?                              │
└─────────────────────────────────────────────────────────┘
                      ↓
        Working in a team?
                      ↓
          ┌───────────┴───────────┐
          │                       │
         YES                     NO
          │                       │
    Want shared standards?   Want independent
          │                   customization?
          ▼                       │
    ┌─────────────┐              ▼
    │ Use --commit│        ┌──────────────┐
    │             │        │ DON'T use    │
    │ Toolkit in  │        │ --commit     │
    │ git         │        │              │
    └─────────────┘        │ Toolkit      │
                           │ local-only   │
                           └──────────────┘
```

---

## 📚 Further Reading

**Detailed Guides**:
- [INJECTION_GUIDE.md](./INJECTION_GUIDE.md) - Complete injection documentation
- [RETROFIT_METHODOLOGY.md](./RETROFIT_METHODOLOGY.md) - Retrofit methodology
- [USER_GUIDE.md](../../.claude/USER_GUIDE.md) - Toolkit usage guide

**Configuration**:
- [.claude/mcp-servers/README.md](../../.claude/mcp-servers/README.md) - MCP configuration

**Standards**:
- [CLAUDE.md](../../CLAUDE.md) - Root standards reference
- [.claude/best-practice.md](../../.claude/best-practice.md) - Full standards

---

**Last Updated**: 2025-11-14
