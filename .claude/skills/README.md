# Claude Skills - Toolkit and Project-Specific Knowledge

**Location**: `.claude/skills/` (automatically gitignored by Claude Code)
**Purpose**: Progressive disclosure of domain knowledge for token efficiency and modular maintenance

---

## 🎯 Important: Gitignored by Default

All toolkit files are installed to `.claude/` folder which is **automatically gitignored by Claude Code**. This means:
- ✅ Toolkit files won't pollute your git commits
- ✅ Each developer can have toolkit locally without affecting others
- ✅ No "best-practice" folder in your repo
- ✅ Clean project structure

---

## What Are Skills?

Skills are folders containing instructions and resources that Claude discovers and loads dynamically when relevant to a task.

**Benefits**:
- **Progressive disclosure**: Load metadata first (~100 tokens), full instructions when needed (<5KB)
- **Token efficiency**: Load only relevant skills vs entire 49KB CLAUDE.md
- **Auto-discovery**: Triggered by keywords in conversation
- **Modular maintenance**: Update individual skills without touching others

---

## Two-Tier Architecture

### Tier 1: Toolkit Skills (Provided)

**Universal best practices** shipped with best-practice toolkit:

```
.claude/skills/
├── quality-standards/      - Code quality, testing, documentation
├── tdd-workflow/           - Test-driven development (Red-Green-Refactor)
├── problem-solving/        - 10 systematic debugging techniques
├── git-workflow/           - Commits, checkpoints, branch strategy
├── file-placement/         - Minimal root structure rules
├── planning-mode/          - Discovery-first planning (Shift+Tab×2)
├── mcp-usage/              - When/how to use MCP tools
└── context-management/     - 60% rule and token optimization
```

### Tier 2: Project Skills (You Create)

**Domain-specific knowledge** for YOUR project:

```
.claude/skills/
├── api-design/             - Your API conventions
├── authentication/         - Your auth implementation
├── database-schema/        - Your DB patterns
├── deployment-workflow/    - Your deploy procedures
└── [your-domain]/          - Your specific patterns
```

---

## Discovery Order

Claude loads skills in priority order:
1. **Project skills first** (priority: project) - Highest priority
2. **Toolkit skills second** (priority: toolkit) - Fallback/foundation

This ensures your project-specific patterns override general best practices when conflicts arise.

---

## Creating a Project Skill

### Step 1: Copy Template

```bash
cp .claude/skills/template/skill.md .claude/skills/your-skill-name/skill.md
```

### Step 2: Update Metadata

```markdown
---
name: Your Skill Name
description: Brief description of what this skill provides
tags: keyword1, keyword2, keyword3
auto_load_triggers: keyword1, keyword2, specific-term
priority: project  # Always "project" for your skills
---
```

**Trigger keywords**:
- Use specific, unique terms from your domain
- Keywords that appear in typical requests
- Avoid generic words like "code" or "function"

### Step 3: Fill in Sections

**Required sections**:
- **Purpose**: What Claude learns from this skill
- **When to Use**: Scenarios where this is relevant
- **Instructions**: Detailed patterns and rules
- **Code Examples**: Real examples from your project
- **Resources**: Links to your project docs

### Step 4: Test the Skill

```
1. Use trigger keywords in a prompt
2. Verify skill loads (check context if visible)
3. Validate Claude follows your patterns
4. Refine triggers if needed
```

### Step 5: Maintain the Skill

- Update when patterns change
- Add new examples as discovered
- Remove outdated information
- Review quarterly for accuracy

---

## Skill File Structure

Each skill folder contains:

```
skill-name/
├── skill.md          - Main skill content (REQUIRED)
└── resources/        - Additional files (OPTIONAL)
    ├── examples/
    ├── references/
    └── diagrams/
```

**skill.md format**:
```markdown
---
[metadata: name, description, tags, auto_load_triggers, priority]
---

# Skill Name

## Purpose
[What this teaches]

## When to Use
[Scenarios]

## Instructions
[Detailed patterns]

## Code Examples
[Real examples]

## Resources
[Links to docs]
```

---

## Example Project Skills

### E-commerce: Product Catalog

```markdown
---
name: Product Catalog Patterns
description: Product data modeling and API conventions
tags: products, catalog, inventory, variant
auto_load_triggers: product, catalog, inventory, variant
priority: project
---

# Product Catalog Patterns

## Purpose
Teaches Claude about our product catalog service architecture,
including variants, inventory management, and pricing rules.

## Instructions

**Data Model**:
- Product (base entity)
- ProductVariant (SKU-level)
- InventoryRecord (stock levels)
- PriceRule (dynamic pricing)

**API Conventions**:
- Endpoint pattern: `/api/v1/catalog/{resource}/{id}`
- Always use `variantId` not `productId` for cart operations
- ALWAYS check inventory before allowing add-to-cart

[Continue with code examples...]
```

### ML Project: Model Training

```markdown
---
name: Model Training Workflow
description: MLOps patterns for training, evaluation, deployment
tags: ml, training, mlops, models
auto_load_triggers: model, training, dataset, evaluation
priority: project
---

# Model Training Workflow

## Purpose
Standardizes model training workflow including data versioning,
experiment tracking, and model registry integration.

## Instructions

**Training Pipeline**:
1. Load versioned dataset (DVC)
2. Run experiment with MLflow tracking
3. Evaluate on validation set
4. Log metrics and artifacts
5. Register model if metrics improve
6. Deploy to staging environment

**Always track experiments**:
```python
import mlflow

with mlflow.start_run(run_name=f"experiment_{timestamp}"):
    mlflow.log_params({"learning_rate": lr})
    # Train model
    mlflow.log_metrics({"accuracy": accuracy})
    mlflow.sklearn.log_model(model, "model")
```

[Continue with patterns...]
```

---

## Best Practices

### DO

- ✅ Keep skills ≤5KB (split large domains into multiple skills)
- ✅ Use specific, unique trigger keywords
- ✅ Include code examples (not just descriptions)
- ✅ Link to project docs for details (don't duplicate)
- ✅ Update skills when patterns change
- ✅ Review skills in code reviews
- ✅ Document skill creation in project README

### DON'T

- ❌ Duplicate toolkit skill content (they're already available)
- ❌ Create skills for temporary requirements
- ❌ Use vague trigger keywords (too broad)
- ❌ Write entire documentation in skill (link instead)
- ❌ Let skills become stale (set review schedule)
- ❌ Create one giant skill (split by domain)

---

## Integration with Toolkit

**Toolkit skills provide foundation**:
- Quality standards (testing, documentation)
- TDD workflow (red-green-refactor)
- Problem-solving (debugging techniques)
- Git workflow (commits, checkpoints)
- File placement (structure rules)
- Planning mode (discovery-first)
- MCP usage (tool integration)
- Context management (60% rule)

**Project skills provide specialization**:
- Domain-specific patterns (your business logic)
- API conventions (your endpoints)
- Data models (your schema)
- Deployment procedures (your infrastructure)
- Team coding standards (your preferences)

**They work together**:
```
User: "Add payment processing to checkout"

Claude loads:
1. Project skill: Payment Processing (your specific patterns)
2. Toolkit skill: TDD Workflow (write tests first)
3. Toolkit skill: Quality Standards (pre-commit checks)
4. Toolkit skill: Git Workflow (commit format)

Result:
- Follows your payment patterns
- Uses TDD approach
- Meets quality standards
- Commits properly
```

---

## Troubleshooting

### Skill Not Loading

**Check**:
- Trigger keywords are in your prompt
- Metadata is valid YAML (check dashes, colons)
- File is named `skill.md` (not `skill.txt`)
- File is in `.claude/skills/[name]/` folder

### Skill Conflicts

**If project skill conflicts with toolkit skill**:
- Project skills have higher priority
- They override toolkit patterns
- Document the override in your skill

### Skill Too Large

**If skill >5KB**:
- Split into multiple skills by sub-domain
- Keep core patterns in main skill
- Link to detailed docs in resources/

---

## Maintenance Schedule

**Review skills**:
- **Every sprint**: Check if new patterns emerged
- **Every quarter**: Validate all skills still accurate
- **When onboarding**: Use as teaching material
- **After post-mortems**: Add learnings to skills

**Update triggers**:
- Add keywords if skill not loading when expected
- Remove keywords if loading too frequently
- Refine specificity based on usage

---

## Installation

Skills are installed via `smart_install.sh` to `.claude/skills/`:
```bash
bash retrofit-tools/smart_install.sh [LIGHT|FULL]
```

**Installed structure**:
```.claude/
├── best-practice.md    # Project standards (renamed from CLAUDE.md)
├── TASKS.md            # Live task list
├── skills/             # This folder - 9 toolkit skills + template
├── commands/           # Slash commands
├── quality-gate/       # Quality gate scripts (FULL mode)
└── mcp-servers/        # MCP servers (FULL mode)
```

All automatically gitignored - won't appear in your commits!

---

## Resources

- **Architecture Review**: See toolkit's `/docs/analysis/ARCHITECTURE_REVIEW_SKILLS_MODEL.md`
- **Skills Explained**: See toolkit's `/docs/references/claude-skills-explained.md`
- **Template**: Use `.claude/skills/template/skill.md`
- **Standards**: `.claude/best-practice.md` (full project standards)

---

**Last Updated**: 2025-11-14
**Review**: Update this README when adding new toolkit skills or changing architecture
