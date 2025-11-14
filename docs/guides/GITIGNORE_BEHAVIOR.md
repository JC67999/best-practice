# Gitignore Behavior - All Toolkit Folders

> **NEW DEFAULT**: All toolkit folders are gitignored (clean git history)

## Summary

**As of latest version**: `smart_install.sh` adds **ALL** toolkit folders to `.gitignore`

**Rationale**: Toolkit files don't add value to the end product - they're pure development tooling that should stay local.

---

## What Gets Gitignored

### Default Installation (Local-Only)

```bash
cd /path/to/project
/path/to/best-practice/retrofit-tools/smart_install.sh
```

**Automatically adds to .gitignore**:
```gitignore
# Best Practice Toolkit - gitignored
.claude/
docs/
CLAUDE.md
tests/        # FULL mode only
```

**Result**:
```bash
git status
# On branch main
# nothing to commit, working tree clean

# ← Perfect! No toolkit clutter
```

---

## Folder-by-Folder Details

| Folder/File  | Gitignored | Why                                           |
|--------------|------------|-----------------------------------------------|
| `.claude/`   | ✅ YES     | Toolkit files - personal to each developer    |
| `docs/`      | ✅ YES     | Internal documentation - not product docs     |
| `tests/`     | ✅ YES     | Toolkit tests - not product tests            |
| `CLAUDE.md`  | ✅ YES     | Standards reference - personal tool          |

**All toolkit-created folders** = **Zero git footprint**

---

## Visual: Before and After

### Before Installation

```bash
git status
# On branch main
# nothing to commit, working tree clean
```

### After Installation (Default)

```bash
git status
# On branch main
# nothing to commit, working tree clean

# ← Still clean! Toolkit is invisible to git
```

### What's in .gitignore

```bash
cat .gitignore

# Best Practice Toolkit - gitignored
.claude/
docs/
CLAUDE.md
tests/
```

---

## Rationale

### Why Gitignore Everything?

**1. Clean Git History**
```
❌ Before:
commit a1b2c3d "feat: add user auth"
commit e4f5g6h "chore: update toolkit standards"  ← Noise
commit i7j8k9l "fix: validation bug"
commit m1n2o3p "docs: update PROJECT_PLAN"        ← Noise
commit q4r5s6t "feat: add profile page"

✅ After:
commit a1b2c3d "feat: add user auth"
commit i7j8k9l "fix: validation bug"
commit q4r5s6t "feat: add profile page"
# Clean! Only product code
```

**2. No Merge Conflicts**
```
❌ Before:
# Alice updates docs/notes/PROJECT_PLAN.md
# Bob updates docs/notes/PROJECT_PLAN.md
# Merge conflict!

✅ After:
# docs/ is gitignored
# Alice has her version locally
# Bob has his version locally
# No conflicts!
```

**3. Toolkit ≠ Product**
```
Product code:
  src/           ← git tracks this
  package.json   ← git tracks this
  README.md      ← git tracks this

Toolkit (development tools):
  .claude/       ← git IGNORES this
  docs/          ← git IGNORES this
  tests/         ← git IGNORES this
```

**4. Each Developer Independent**
```
Alice:
  .claude/skills/  ← Her customizations
  docs/notes/      ← Her planning docs

Bob:
  .claude/skills/  ← His customizations
  docs/notes/      ← His planning docs

No conflicts, no pollution!
```

**5. Toolkit Updates Don't Affect Git**
```
# Update toolkit
cp /path/to/best-practice/.claude/* .claude/

# Git status
nothing to commit, working tree clean

# ← No git noise from toolkit updates!
```

---

## Override: Commit Toolkit (Team Scenario)

**If you want shared toolkit** (not recommended):

```bash
cd /path/to/project
/path/to/best-practice/retrofit-tools/smart_install.sh --commit
```

**What happens**:
1. Removes toolkit entries from .gitignore
2. Stages all toolkit files
3. Creates git commit
4. Team shares same toolkit

**Result**:
```bash
git status
# On branch main
# Changes to be committed:
#   new file:   .claude/best-practice.md
#   new file:   docs/notes/PROJECT_PLAN.md
#   new file:   tests/test_basic.py
```

**Use when**:
- Team wants versioned toolkit
- Shared standards enforcement
- Reviewable toolkit changes

**Drawbacks**:
- ❌ Git pollution
- ❌ Merge conflicts possible
- ❌ Toolkit updates create git noise
- ❌ Less flexibility per developer

---

## Common Questions

### Q: But don't teams need shared docs?

**A: Product docs ≠ Toolkit docs**

```
Product documentation:
  README.md              ← git tracks (product overview)
  API.md                 ← git tracks (API reference)
  CONTRIBUTING.md        ← git tracks (how to contribute)

Toolkit documentation:
  docs/notes/PROJECT_PLAN.md    ← gitignored (personal planning)
  docs/design/ARCHITECTURE.md   ← gitignored (design scratchpad)
  .claude/USER_GUIDE.md         ← gitignored (toolkit usage)
```

**Keep product docs in root** (git tracked)
**Toolkit docs are personal** (gitignored)

---

### Q: What about tests?

**A: Product tests ≠ Toolkit test structure**

```
Product tests:
  src/components/__tests__/    ← git tracks (product tests)
  src/utils/test_helpers.ts    ← git tracks (test utilities)

Toolkit test structure:
  tests/test_basic.py           ← gitignored (toolkit starter)
```

**Your actual product tests**: Keep where they belong (git tracked)
**Toolkit test structure**: Just a starter (gitignored)

---

### Q: Can I selectively gitignore?

**Yes! Edit .gitignore manually**:

```gitignore
# Best Practice Toolkit
.claude/               ← Keep gitignored
# docs/                ← Comment out to track
CLAUDE.md              ← Keep gitignored
# tests/               ← Comment out to track
```

**Or create product docs separately**:
```
docs/                  ← Gitignored (toolkit)
documentation/         ← Git tracked (product)
```

---

### Q: How do I see what's gitignored?

```bash
# See ignored files
git status --ignored

# See .gitignore contents
cat .gitignore

# Check specific folder
git check-ignore -v .claude/
# Output: .gitignore:2:.claude/    .claude/
```

---

### Q: What if I accidentally committed toolkit files?

**Undo commit, add to gitignore**:

```bash
# If not pushed yet
git reset HEAD~1

# Add to .gitignore
echo ".claude/" >> .gitignore
echo "docs/" >> .gitignore
echo "CLAUDE.md" >> .gitignore

# Remove from git tracking (keep files)
git rm -r --cached .claude/ docs/ CLAUDE.md

# Commit
git add .gitignore
git commit -m "chore: gitignore toolkit folders"
```

---

## Verification

### Check Installation Worked

```bash
# 1. .gitignore exists
ls -la .gitignore

# 2. Contains toolkit folders
cat .gitignore
# Should show:
# # Best Practice Toolkit - gitignored
# .claude/
# docs/
# CLAUDE.md

# 3. Git status is clean
git status
# Should show:
# nothing to commit, working tree clean

# 4. Toolkit folders exist
ls .claude/ docs/
# Should show files (they exist locally)
```

---

## Benefits Summary

**✅ Clean Git History**
- Only product code in git
- No toolkit noise in commits
- Easy to review changes

**✅ Zero Conflicts**
- No merge conflicts from toolkit
- Each developer independent
- Toolkit updates don't affect git

**✅ Fast Operations**
- No large toolkit files in git
- Faster clones
- Smaller repository

**✅ Flexibility**
- Customize toolkit personally
- Update toolkit independently
- No team coordination needed

**✅ Clear Separation**
- Product code = git tracked
- Development tools = gitignored
- Clear mental model

---

## Migration Guide

### If You Have Old Installation (Only .claude/ Gitignored)

**Update to new behavior**:

```bash
# Add missing entries to .gitignore
echo "docs/" >> .gitignore
echo "CLAUDE.md" >> .gitignore
echo "tests/" >> .gitignore  # If FULL mode

# Remove from git (keep files locally)
git rm -r --cached docs/ CLAUDE.md tests/

# Commit
git add .gitignore
git commit -m "chore: gitignore all toolkit folders"
```

**Verify**:
```bash
git status
# Should be clean now
```

---

## Summary

**Default behavior**: Everything gitignored
**Override with**: --commit flag
**Rationale**: Toolkit = development tool, not product
**Result**: Clean git history, zero conflicts

---

**Last Updated**: 2025-11-14
**Related**: INJECTION_GUIDE.md, smart_install.sh
