# Injection Methods - Two Ways to Install

> **Choose your method**: Run from toolkit OR run from target project

## Overview

There are **two ways** to inject the best-practice toolkit into a project:

1. **Method 1: inject.sh** - Run from toolkit project (RECOMMENDED)
2. **Method 2: smart_install.sh** - Run from target project (classic)

Both produce identical results, just different workflows.

---

## Method 1: inject.sh (Recommended)

**Run FROM the toolkit project**

### Usage

```bash
# Navigate to toolkit
cd /path/to/best-practice

# Inject into target project
./inject.sh /path/to/target-project

# Or with commit flag
./inject.sh /path/to/target-project --commit
```

### Example

```bash
# You are in best-practice toolkit
cd ~/CascadeProjects/best-practice

# Inject into Angular app
./inject.sh ~/projects/my-angular-app

# What happens:
┌────────────────────────────────────────────────────┐
│ Best Practice Toolkit - Injection                  │
├────────────────────────────────────────────────────┤
│                                                     │
│ Toolkit:    /home/jc/CascadeProjects/best-practice │
│ Target:     /home/jc/projects/my-angular-app       │
│ Project:    my-angular-app                          │
│                                                     │
│ ✓ Git repository detected                          │
│ ✓ Working tree clean                               │
│                                                     │
│ Proceed with injection? (Y/n): Y                   │
│                                                     │
│ [Running injection...]                             │
│                                                     │
│ ✅ Injection Complete                              │
│                                                     │
│ Next steps:                                        │
│   1. cd /home/jc/projects/my-angular-app           │
│   2. Review: docs/notes/PROJECT_PLAN.md            │
│   3. Open in Claude Code: code .                   │
│                                                     │
└────────────────────────────────────────────────────┘
```

### Benefits

**✅ Cleaner workflow**
- Run from toolkit (one location)
- Target path as argument (explicit)
- Returns to toolkit after injection

**✅ Better for multiple projects**
```bash
cd ~/best-practice

./inject.sh ~/projects/app1
./inject.sh ~/projects/app2
./inject.sh ~/projects/app3
# All from same location
```

**✅ Easier to remember**
```bash
./inject.sh <target>
# vs
cd <target> && /path/to/toolkit/retrofit-tools/smart_install.sh
```

**✅ Safer**
- Validates paths before injection
- Clear confirmation prompt
- Returns to original directory on error

---

## Method 2: smart_install.sh (Classic)

**Run FROM the target project**

### Usage

```bash
# Navigate to target project
cd /path/to/target-project

# Run installer from toolkit
/path/to/best-practice/retrofit-tools/smart_install.sh

# Or with commit flag
/path/to/best-practice/retrofit-tools/smart_install.sh --commit
```

### Example

```bash
# Navigate to target
cd ~/projects/my-angular-app

# Run smart_install.sh
~/CascadeProjects/best-practice/retrofit-tools/smart_install.sh

# What happens:
┌────────────────────────────────────────────────────┐
│ Best Practice Toolkit - Smart Install              │
│ Mode: LOCAL ONLY (default - toolkit files NOT      │
│       committed)                                    │
├────────────────────────────────────────────────────┤
│                                                     │
│ 🔍 Analyzing project...                            │
│   - Checking git activity... 15 commits/30d        │
│   - Checking deployment configs... none            │
│   - Checking CI/CD... none                         │
│   - Checking production env... none                │
│                                                     │
│ 🟢 DEVELOPMENT detected (score: 0/4)               │
│                                                     │
│ Will install: FULL mode (complete best practices)  │
│                                                     │
│ Proceed? (Y/n): Y                                  │
│                                                     │
│ [Running installation...]                          │
│                                                     │
│ ✅ Installation complete                           │
│                                                     │
└────────────────────────────────────────────────────┘
```

### Benefits

**✅ Traditional approach**
- Run from where you're working
- Follows standard install patterns
- Works in scripts easily

---

## Comparison

| Aspect                    | inject.sh (Method 1)        | smart_install.sh (Method 2) |
|---------------------------|-----------------------------|-----------------------------|
| **Run from**              | Toolkit directory           | Target directory            |
| **Command**               | `./inject.sh <target>`      | `/path/to/smart_install.sh` |
| **Workflow**              | Stay in toolkit             | Navigate to each project    |
| **Path argument**         | Required (explicit)         | Implicit (pwd)              |
| **Multiple projects**     | Easy (one location)         | Tedious (cd each time)      |
| **Returns to directory**  | Yes (original)              | No (stays in target)        |
| **Error handling**        | Enhanced                    | Standard                    |
| **Help text**             | Built-in (`-h`)             | None                        |
| **Validation**            | Pre-flight checks           | Basic                       |
| **Recommendation**        | ✅ Preferred                | ✅ Works fine              |

---

## When to Use Each Method

### Use inject.sh (Method 1) When:

**✅ Managing multiple projects**
```bash
cd ~/best-practice
./inject.sh ~/projects/app1
./inject.sh ~/projects/app2
./inject.sh ~/projects/app3
```

**✅ Want better UX**
- Built-in help (`./inject.sh --help`)
- Colored output
- Clear error messages
- Returns to toolkit after injection

**✅ Prefer explicit arguments**
```bash
./inject.sh /full/path/to/project --commit
# Clear what's happening
```

---

### Use smart_install.sh (Method 2) When:

**✅ Already in target project**
```bash
# Working on project, want toolkit
cd ~/projects/my-app
~/best-practice/retrofit-tools/smart_install.sh
```

**✅ Scripting automation**
```bash
#!/bin/bash
for project in projects/*/; do
    cd "$project"
    ~/best-practice/retrofit-tools/smart_install.sh
    cd ..
done
```

**✅ Following documentation**
- Older guides use this method
- Classic installation pattern

---

## Both Methods Produce Identical Results

**No difference in outcome**:
- Same files created
- Same folders gitignored
- Same mode detection (LIGHT/FULL)
- Same .gitignore entries
- Same validation

**Only difference**: Where you run the command from.

---

## Examples

### Example 1: Inject into Multiple Projects (Method 1)

```bash
# Stay in toolkit
cd ~/best-practice

# Inject into three projects
./inject.sh ~/projects/frontend-app
./inject.sh ~/projects/backend-api
./inject.sh ~/projects/mobile-app

# Still in toolkit
pwd
# /home/user/best-practice
```

**Fast and clean!**

---

### Example 2: Add Toolkit to Current Project (Method 2)

```bash
# You're working on a project
cd ~/projects/my-app

# Add toolkit quickly
~/best-practice/retrofit-tools/smart_install.sh

# Continue working
code .
```

**Convenient when already there!**

---

### Example 3: Relative Paths (Method 1)

```bash
cd ~/best-practice

# Inject into sibling directory
./inject.sh ../other-project

# Inject into parent directory project
./inject.sh ../../../some-other-location/project

# Works with any valid path
```

---

## Advanced Usage

### With Commit Flag

**Method 1**:
```bash
./inject.sh /path/to/project --commit
```

**Method 2**:
```bash
cd /path/to/project
/path/to/best-practice/retrofit-tools/smart_install.sh --commit
```

Both commit toolkit files to git (override gitignore behavior).

---

### Help Text

**Method 1**:
```bash
./inject.sh --help
# Shows detailed usage, examples, options
```

**Method 2**:
```bash
# No built-in help
# Refer to documentation
```

---

### Dry Run / Validation

**Method 1**:
```bash
# Path validation before execution
./inject.sh /invalid/path
# Error: Target project not found: /invalid/path
# (Fails fast)
```

**Method 2**:
```bash
# Validation happens during execution
cd /invalid/path
# bash: cd: /invalid/path: No such file or directory
```

---

## Migration Between Methods

**Both methods are interchangeable** - use whichever fits your workflow.

**Switching is easy**:
```bash
# Using Method 2
cd ~/projects/app1
~/best-practice/retrofit-tools/smart_install.sh

# Switching to Method 1 for next project
cd ~/best-practice
./inject.sh ~/projects/app2
```

---

## Recommendation

**For daily use**: Method 1 (`inject.sh`)
- Better UX
- Easier workflow
- Handles multiple projects well

**For quick additions**: Method 2 (`smart_install.sh`)
- When already in project directory
- Scripting automation
- Following old documentation

**Both work perfectly** - choose based on preference!

---

## Quick Reference

### inject.sh (Run from toolkit)

```bash
cd /path/to/best-practice
./inject.sh <target-project> [--commit]
./inject.sh --help
```

### smart_install.sh (Run from target)

```bash
cd /path/to/target-project
/path/to/best-practice/retrofit-tools/smart_install.sh [--commit]
```

---

## Troubleshooting

### inject.sh: "Target project not found"

**Cause**: Invalid path
**Fix**: Use absolute path or verify directory exists
```bash
# Verify target exists
ls -d /path/to/target

# Use absolute path
./inject.sh ~/projects/app  # Not ./projects/app
```

---

### smart_install.sh: "smart_install.sh not found"

**Cause**: Wrong path to script
**Fix**: Use full path to toolkit
```bash
# Find toolkit location
find ~ -name "smart_install.sh" -type f

# Use full path
/full/path/to/best-practice/retrofit-tools/smart_install.sh
```

---

### Both: "Not a git repository"

**Cause**: Target needs git
**Fix**: Script will offer to initialize
```
⚠️  Not a git repository
Initialize git? (Y/n): Y
✅ Git initialized
```

---

## Summary

**Two methods, same result**:

| Method             | Command                         | Best For                |
|--------------------|---------------------------------|-------------------------|
| inject.sh          | `./inject.sh <target>`          | Multiple projects       |
| smart_install.sh   | `cd <target> && /path/to/...`   | Quick additions         |

**Recommendation**: Use `inject.sh` for better UX

---

**Last Updated**: 2025-11-14
**See Also**: INJECTION_GUIDE.md, INJECTION_QUICK_REF.md
