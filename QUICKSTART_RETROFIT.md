# Quick Start - Retrofit Your Project

> **Goal**: Apply best practices to an existing project in 10-60 minutes

---

## 🚀 Three Ways to Retrofit

### Option 1: Interactive Script (Recommended)

**Best for**: Most users, guided step-by-step

```bash
# Navigate to your project
cd /path/to/your/project

# Run interactive retrofit
/home/jc/CascadeProjects/best-practice/retrofit-tools/retrofit_project.sh
```

**What it does**:
- Creates safety checkpoint (git tag)
- Assesses current state
- Asks for your preferences (Light/Standard/Full)
- Organizes documentation
- Adds quality tools
- Creates PROJECT_PLAN.md
- Commits changes

**Time**: 10-60 minutes depending on mode

---

### Option 2: Manual Claude Code Session

**Best for**: When you want AI assistance during retrofit

```bash
# 1. Navigate to your project
cd /path/to/your/project

# 2. Start Claude Code
claude-code

# 3. Tell Claude:
```

**Prompt to use**:
```
I want to retrofit this project with best practices.

Use the retrofit methodology from:
/home/jc/CascadeProjects/best-practice/docs/guides/RETROFIT_METHODOLOGY.md

Start with:
1. Safety checkpoint (git tag retrofit-start)
2. Assess current structure
3. Create docs/ organization
4. Create PROJECT_PLAN.md with objective
5. Add CLAUDE.md standards
6. Add quality gate (.ai-validation/)

Use Standard mode (30 min) unless I specify otherwise.
```

**Time**: 30-60 minutes with AI assistance

---

### Option 3: Just Copy Templates

**Best for**: You know what you want, just need the files

```bash
# Navigate to your project
cd /path/to/your/project

# Create directories
mkdir -p docs/{design,guides,analysis,references,notes}
mkdir -p tests
mkdir -p .ai-validation

# Copy templates
cp /home/jc/CascadeProjects/best-practice/CLAUDE.md ./
cp /home/jc/CascadeProjects/best-practice/.ai-validation/check_quality.sh ./.ai-validation/
cp /home/jc/CascadeProjects/best-practice/.gitignore ./
cp /home/jc/CascadeProjects/best-practice/tests/conftest.py ./tests/

# Move your docs to docs/ subdirectories
# Create PROJECT_PLAN.md in docs/notes/
# Customize CLAUDE.md for your project
```

**Time**: 10-20 minutes + customization

---

## 📋 What Gets Changed

### Minimal Changes (Light Mode)
```
Before:
your-project/
├── many_files.md
├── scattered_docs.md
└── stuff_everywhere/

After:
your-project/
├── docs/
│   ├── design/
│   ├── guides/
│   ├── analysis/
│   └── notes/
│       └── PROJECT_PLAN.md
└── README.md
```

### Standard Changes (Recommended)
```
Everything from Light, plus:

├── CLAUDE.md                  # Project standards
├── .ai-validation/
│   └── check_quality.sh      # Quality gate
└── .gitignore                 # Git ignores
```

### Full Changes (Complete Retrofit)
```
Everything from Standard, plus:

├── tests/
│   ├── conftest.py           # Test fixtures
│   └── test_*.py             # Test templates
└── (MCP integration optional)
```

---

## ✅ Success Checklist

After retrofit, you should have:

**Structure**:
- [ ] Root folders ≤5-7
- [ ] All docs organized in docs/ subdirectories
- [ ] Clear purpose for each folder

**Documentation**:
- [ ] PROJECT_PLAN.md with formalized objective
- [ ] CLAUDE.md with project standards
- [ ] README.md with quick links

**Quality**:
- [ ] .ai-validation/check_quality.sh script
- [ ] .gitignore configured
- [ ] Git history preserved with retrofit-start tag

**Optional (Full mode)**:
- [ ] tests/ directory with structure
- [ ] Quality gate passing
- [ ] MCP servers configured

---

## 🔄 Before/After Examples

### Example: Web Application Project

**Before**:
```
my-web-app/
├── src/
├── public/
├── node_modules/
├── ARCHITECTURE.md
├── API_DOCS.md
├── SETUP_GUIDE.md
├── CHANGELOG.md
├── CONTRIBUTING.md
├── TODO.md
├── package.json
├── README.md
└── ... (13 root items)
```

**After (Standard Mode)**:
```
my-web-app/
├── src/
├── public/
├── tests/
├── docs/
│   ├── design/
│   │   └── ARCHITECTURE.md
│   ├── guides/
│   │   ├── SETUP_GUIDE.md
│   │   └── CONTRIBUTING.md
│   ├── analysis/
│   │   └── CHANGELOG.md
│   └── notes/
│       ├── PROJECT_PLAN.md
│       └── TODO.md
├── .ai-validation/
│   └── check_quality.sh
├── CLAUDE.md
├── README.md
├── package.json
└── .gitignore

(9 root items - 30% reduction)
```

---

## 🛟 Safety & Rollback

### Safety First
Every retrofit creates a safety checkpoint:
```bash
git tag retrofit-start    # Created automatically
```

### Rollback If Needed
```bash
# See what changed
git diff retrofit-start

# Undo everything
git reset --hard retrofit-start
git clean -fd

# Remove the tag
git tag -d retrofit-start
```

### Partial Rollback
```bash
# Undo just the last commit
git reset --soft HEAD~1

# Undo but keep files
git reset --mixed HEAD~1
```

---

## 🎯 Next Steps After Retrofit

### Immediate (Do Today)
1. **Review PROJECT_PLAN.md**
   - Is the objective clear?
   - Are success metrics defined?
   - Is current status accurate?

2. **Customize CLAUDE.md**
   - Update file placement rules for your tech stack
   - Add project-specific conventions
   - Set your quality standards

3. **Test Quality Gate**
   ```bash
   .ai-validation/check_quality.sh
   ```

### Short-term (This Week)
4. **Add Real Tests**
   - If you chose Full mode
   - Target: 80%+ coverage
   - Start with core functionality

5. **Update Internal Links**
   - Fix any broken links to moved files
   - Update import statements if needed

6. **Share with Team**
   - Explain the new structure
   - Get buy-in on standards
   - Update CI/CD if needed

### Long-term (This Month)
7. **Run Full Objective Clarification**
   - Use Project MCP for detailed questions
   - Aim for 80+ clarity score
   - Document in PROJECT_PLAN.md

8. **Implement Quality Gates in CI**
   - Add to GitHub Actions / GitLab CI
   - Block merges on failures
   - Track quality metrics

9. **Consider Autonomous Mode**
   - See docs/guides/AUTONOMOUS_MODE_ROADMAP.md
   - Enable overnight coding (optional)

---

## 💡 Tips & Best Practices

### 1. Start Small
Don't retrofit everything at once:
- Week 1: Structure only (Light mode)
- Week 2: Add quality tools (Standard mode)
- Week 3: Add tests and full setup (Full mode)

### 2. Get Team Buy-In
Before retrofitting a team project:
- Share the assessment results
- Explain the benefits
- Get consensus on which mode to use
- Do it together in a mob session

### 3. Commit Frequently
During retrofit:
- Commit after each major step
- Use descriptive commit messages
- Tag important milestones
- Easy to rollback specific changes

### 4. Don't Break Things
- Keep the retrofit non-breaking
- Update imports/links as you move files
- Test after each phase
- CI/CD should still work

### 5. Customize, Don't Copy Blindly
Templates are starting points:
- CLAUDE.md needs your project specifics
- Quality gate needs your tech stack
- PROJECT_PLAN.md needs your actual objective

---

## 🔍 Troubleshooting

### "Script says not a git repository"
```bash
# Initialize git first
cd your-project
git init
git add .
git commit -m "Initial commit before retrofit"
```

### "Quality gate fails after retrofit"
This is normal! Fix issues one by one:
```bash
# See what's failing
.ai-validation/check_quality.sh

# Fix tests first
pytest tests/

# Then linting
ruff check --fix .

# Then types
mypy .
```

### "Too many files to move manually"
Use the interactive script - it handles moving files automatically:
```bash
/home/jc/CascadeProjects/best-practice/retrofit-tools/retrofit_project.sh
```

### "Team doesn't like new structure"
- Start with Light mode (minimal disruption)
- Show the before/after assessment scores
- Do a pilot on one project first
- Gather feedback and adjust

---

## 📞 Getting Help

### Check Documentation
1. [RETROFIT_METHODOLOGY.md](docs/guides/RETROFIT_METHODOLOGY.md) - Detailed process
2. [PROJECT_PLAN.md](docs/notes/PROJECT_PLAN.md) - This project's plan (as example)
3. [CLAUDE.md](CLAUDE.md) - Standards reference

### Run Assessment
```bash
python /home/jc/CascadeProjects/best-practice/retrofit-tools/retrofit_assess.py /path/to/project
```

### Ask Claude Code
```
I'm retrofitting my project at /path/to/project using the best-practice toolkit.

The retrofit script created these files but I need help with:
[describe your issue]

Context:
- Mode used: [Light/Standard/Full]
- Current issue: [what's not working]
- Error message: [if any]
```

---

## 📊 Expected Results

### Structure Improvements
- Root items reduced by 20-40%
- Clear organization (no hunting for docs)
- Easy onboarding for new developers

### Quality Improvements
- Quality gate prevents bad commits
- Test coverage visible and tracked
- Security issues caught early

### Productivity Improvements
- 3-5x faster with AI assistance
- Clear objectives reduce wasted work
- Context preserved between sessions

---

**Ready to retrofit?**

Choose your path:
- **Quick & Easy**: Run `retrofit_project.sh`
- **AI Assisted**: Use Claude Code with retrofit prompt
- **DIY**: Copy templates and customize

All paths lead to better project structure! 🚀
