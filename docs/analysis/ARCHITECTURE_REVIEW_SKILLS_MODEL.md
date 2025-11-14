# Architecture Review: Best Practice Toolkit vs Claude Skills Model

**Date**: 2025-11-14
**Purpose**: Evaluate our toolkit architecture against Claude's agentic ecosystem (Skills, Projects, MCP, Subagents)
**Reference**: docs/references/claude-skills-explained.md

---

## Executive Summary

**Current State**: Our toolkit is well-aligned with Claude's ecosystem but doesn't use Skills feature
**Assessment**: ✅ Strong MCP implementation, ✅ Good subagent use, ⚠️ Opportunity to adopt Skills
**Recommendation**: **Consider hybrid approach** - Convert CLAUDE.md sections into Skills while maintaining MCP servers

---

## Current Architecture Mapping

### What We Have vs Claude's Ecosystem

| Component | Our Implementation | Alignment | Grade |
|-----------|-------------------|-----------|-------|
| **Skills** | CLAUDE.md (49KB monolithic) | ⚠️ Partial | B |
| **Prompts** | Natural conversation + slash commands | ✅ Good | A |
| **Projects** | Rely on Claude Code project context | ✅ Good | A |
| **Subagents** | Task tool with Explore subagent | ✅ Good | A- |
| **MCP** | 3 custom servers (Memory, Quality, Project) | ✅ Excellent | A+ |

---

## Detailed Component Analysis

### 1. Skills (Current: CLAUDE.md Monolith)

**Current Implementation**:
- Single 49KB CLAUDE.md file
- Contains ALL procedural knowledge
- Loaded entirely into context every session
- No progressive disclosure
- No dynamic discovery

**Skills Model Benefits We're Missing**:
- ❌ Progressive disclosure (~100 tokens metadata first)
- ❌ Dynamic discovery (load only relevant skills)
- ❌ Modular organization (domain-specific packages)
- ❌ Token efficiency (load <5k when needed, not 49KB always)
- ❌ Composability (mix and match skills per task)

**What We Do Well**:
- ✅ Comprehensive standards documentation
- ✅ Clear workflow instructions
- ✅ Integration with MCP tools
- ✅ Problem-solving techniques documented

**Opportunity**: **Convert CLAUDE.md into modular Skills**

---

### 2. Prompts (Current: Slash Commands)

**Current Implementation**:
- 8 slash commands in `.claude/commands/`
  - `/spec` - Feature specification with scope reduction
  - `/plan` - Planning Mode entry
  - `/tdd` - Test-driven development cycle
  - `/checkpoint` - Git checkpoint creation
  - `/brainstorm` - Structured brainstorming
  - `/debug` - Systematic debugging
  - `/execute-plan` - Plan execution with quality gates
  - `/mcp` - MCP server scaffolding

**Skills Model Comparison**:
- Slash commands = Reactive prompts (good for workflows)
- Skills = Proactive knowledge (loaded when relevant)
- **They're complementary, not competitive**

**What We Do Well**:
- ✅ Well-defined workflows
- ✅ Reusable patterns
- ✅ Checked into git (team sharing)
- ✅ Focused commands (single purpose)

**Recommendation**: **Keep slash commands, add Skills for domain knowledge**

---

### 3. Projects (Current: Claude Code Native)

**Current Implementation**:
- Rely on Claude Code's project feature
- 200K context window
- Persistent chat history
- File-based knowledge (CLAUDE.md, TASKS.md)

**Skills Model Alignment**:
- ✅ Using Projects correctly
- ✅ Persistent context across sessions
- ✅ Background knowledge in docs/

**What We Do Well**:
- ✅ Well-organized docs/ structure
- ✅ PROJECT_PLAN.md for current status
- ✅ Memory MCP for cross-session persistence

**Recommendation**: **No changes needed - well-architected**

---

### 4. Subagents (Current: Task Tool)

**Current Implementation**:
- Use Task tool with specialized subagents:
  - `Explore` subagent for codebase exploration
  - `Plan` subagent for planning tasks
- Independent context windows
- Task delegation for complex searches

**Skills Model Alignment**:
- ✅ Using subagents correctly
- ✅ Context isolation working well
- ✅ Task delegation effective

**What We Do Well**:
- ✅ Proactive subagent use for exploration
- ✅ Context preservation in main conversation
- ✅ CLAUDE.md documents when to use subagents

**Opportunity**: **Create specialized subagents for quality gate, refactoring**

---

### 5. MCP Servers (Current: 3 Custom Servers)

**Current Implementation**:
- **Memory MCP**: Context persistence across sessions
  - Session summaries
  - Decision tracking
  - Project context loading
  - 77% test coverage

- **Quality MCP**: Standards enforcement
  - Code quality checks
  - Structure validation
  - Quality gate execution
  - Documentation updates

- **Project MCP**: Objective-driven development
  - Objective clarification
  - Task alignment validation
  - Scope creep detection
  - Priority challenges

**Skills Model Alignment**:
- ✅ Excellent MCP implementation
- ✅ Clear separation: MCP = data/connectivity, Skills = knowledge
- ✅ 27 MCP tools available
- ✅ Well-tested (Memory MCP)

**What We Do Exceptionally Well**:
- ✅ Custom MCPs for project-specific needs
- ✅ Integration with quality gates
- ✅ Persistent memory across sessions
- ✅ Objective-driven workflows

**Recommendation**: **No changes - this is our strength**

---

## Integration Model Analysis

### Current Integration Flow

```
User prompt
    ↓
CLAUDE.md loaded (49KB - all sections)
    ↓
Slash command triggered (if used)
    ↓
MCP tools called (Memory, Quality, Project)
    ↓
Subagent launched (if needed for exploration)
    ↓
Results returned
```

**Issues**:
- CLAUDE.md loaded entirely every time (49KB)
- No progressive disclosure
- Relevant + irrelevant sections loaded

### Skills-Enhanced Integration Flow

```
User prompt
    ↓
Relevant Skills discovered dynamically
    ↓
Metadata loaded (~100 tokens per skill)
    ↓
Full skill instructions loaded if needed (<5k tokens)
    ↓
Slash command triggered (workflow automation)
    ↓
MCP tools called (data access)
    ↓
Subagent launched (specialized execution)
    ↓
Results returned
```

**Benefits**:
- Progressive disclosure (load only what's needed)
- Token efficiency (100 tokens vs 49KB)
- Composability (mix relevant skills)
- Faster context loading

---

## Recommendations

### Option 1: Status Quo (Keep Current Architecture)

**Pros**:
- Already working well
- No migration effort
- Familiar to users
- Well-documented

**Cons**:
- 49KB CLAUDE.md loaded every session
- No progressive disclosure
- Token inefficiency
- Harder to maintain as it grows

**When to choose**: If "ain't broke, don't fix it" philosophy preferred

---

### Option 2: Hybrid Approach (Recommended)

**Convert CLAUDE.md into modular Skills while keeping MCP**:

**Proposed Skill Structure**:
```
.claude/skills/
├── quality-standards/
│   ├── skill.md (metadata + instructions)
│   └── resources/
│       └── quality-checklist.md
├── tdd-workflow/
│   ├── skill.md
│   └── resources/
│       └── test-patterns.md
├── problem-solving/
│   ├── skill.md
│   └── resources/
│       └── thinking-skills.md
├── git-workflow/
│   ├── skill.md
│   └── resources/
│       └── commit-patterns.md
├── file-placement/
│   ├── skill.md
│   └── resources/
│       └── folder-structure.md
└── planning-mode/
    ├── skill.md
    └── resources/
        └── discovery-framework.md
```

**Migration Strategy**:
1. Break CLAUDE.md into 6-8 focused Skills
2. Each Skill ≤5KB (vs current 49KB)
3. Dynamic loading based on task context
4. Keep MCP servers unchanged
5. Keep slash commands unchanged

**Benefits**:
- ✅ Progressive disclosure (token efficiency)
- ✅ Modular maintenance (easier updates)
- ✅ Composability (load only relevant skills)
- ✅ Keep MCP strengths
- ✅ Preserve slash commands

**Effort**: Medium (1-2 days to migrate and test)

---

### Option 3: Full Skills Adoption

**Migrate everything to Skills, reduce MCP reliance**:

**When to choose**: Never (violates our strengths)

**Why not**:
- MCP servers are our competitive advantage
- Skills can't replace data persistence (Memory MCP)
- Skills can't replace quality enforcement (Quality MCP)
- Skills don't handle cross-session state

**Verdict**: ❌ Don't do this

---

## Proposed Skill Breakdown

### Skill 1: Quality Standards (~3KB)

**Metadata**:
- Name: Quality Standards
- Description: Code quality, testing, and documentation standards
- Tags: quality, testing, documentation
- Auto-load triggers: test, quality, coverage, lint

**Instructions**:
- Pre-commit checklist
- Test coverage requirements (≥80%)
- Code style (PEP 8, type hints, docstrings)
- Quality gate workflow

**Resources**:
- Quality checklist
- Example test patterns

---

### Skill 2: TDD Workflow (~2KB)

**Metadata**:
- Name: TDD Workflow
- Description: Test-driven development cycle and best practices
- Tags: tdd, testing, red-green-refactor
- Auto-load triggers: test, tdd, failing

**Instructions**:
- Red-Green-Refactor cycle
- Write tests first
- See tests fail
- Minimal implementation
- Refactor while green

**Resources**:
- Test structure (Given-When-Then)
- Example test suites

---

### Skill 3: Problem-Solving Techniques (~5KB)

**Metadata**:
- Name: Problem-Solving Techniques
- Description: Systematic debugging and problem-solving methods
- Tags: debugging, problem-solving, troubleshooting
- Auto-load triggers: error, bug, stuck, debug

**Instructions**:
- 10 mandatory techniques (First Principles, Binary Search, etc.)
- When to apply each technique
- Quick wins checklist
- Anti-patterns to avoid

**Resources**:
- Full thinking skills guide (docs/guides/thinking skills.md)

---

### Skill 4: Git Workflow (~2KB)

**Metadata**:
- Name: Git Workflow
- Description: Git commit, checkpoint, and rollback patterns
- Tags: git, version-control, checkpoint
- Auto-load triggers: commit, checkpoint, rollback

**Instructions**:
- Commit message format
- Checkpoint creation
- Rewind/rollback procedures
- Commit frequency rules

**Resources**:
- Commit message examples
- Conventional commits guide

---

### Skill 5: File Placement Rules (~2KB)

**Metadata**:
- Name: File Placement Rules
- Description: Minimal root structure and file organization
- Tags: structure, organization, files
- Auto-load triggers: create, new file, folder

**Instructions**:
- Root directory limits (≤5 folders)
- Documentation structure (docs/)
- Forbidden files in root
- Where to place new files

**Resources**:
- Allowed folder structure
- Placement decision tree

---

### Skill 6: Planning Mode (~3KB)

**Metadata**:
- Name: Planning Mode
- Description: Discovery-first planning for new features
- Tags: planning, discovery, requirements
- Auto-load triggers: plan, feature, new

**Instructions**:
- When to use Planning Mode (Shift+Tab×2)
- Requirements discovery process
- Plan creation workflow
- Get approval before coding

**Resources**:
- Discovery framework
- Planning templates

---

### Skill 7: MCP Usage (~3KB)

**Metadata**:
- Name: MCP Usage
- Description: When and how to use Memory, Quality, Project MCPs
- Tags: mcp, tools, workflow
- Auto-load triggers: session, quality gate, objective

**Instructions**:
- Session start (load_project_context, get_current_status)
- Before tasks (validate_task_alignment)
- Before completion (run_quality_gate)
- Session end (save_session_summary)

**Resources**:
- MCP tool reference
- Integration examples

---

### Skill 8: Context Management (~2KB)

**Metadata**:
- Name: Context Management
- Description: 60% rule and context optimization
- Tags: context, token-management, memory
- Auto-load triggers: context, compact, clear

**Instructions**:
- 60% context rule
- When to use /clear vs /compact
- Selective file loading
- Progressive context building

**Resources**:
- Context management patterns
- Anti-patterns

---

## Token Efficiency Analysis

### Current State (Monolithic CLAUDE.md)

- **CLAUDE.md**: 49KB ≈ 12,250 tokens
- **Loaded**: Every session, in full
- **Relevant**: 20-30% per task (estimated)
- **Waste**: 70-80% of loaded content unused

### Skills Model (Progressive Disclosure)

**Scenario: User asks to write tests**

**Current**:
- Load entire CLAUDE.md: 12,250 tokens
- Relevant sections: TDD, Quality, Problem-Solving ≈ 3,000 tokens
- **Wasted**: 9,250 tokens (75%)

**With Skills**:
- Load metadata for all 8 skills: 8 × 25 = 200 tokens
- Load TDD Workflow skill: 500 tokens
- Load Quality Standards skill: 750 tokens
- Load Problem-Solving (if stuck): 1,250 tokens
- **Total**: 2,700 tokens
- **Savings**: 9,550 tokens (78% reduction)

**Extrapolated Savings**:
- Per session: ~10,000 tokens saved
- Per 10 sessions: ~100,000 tokens saved
- **Faster loading**, **more room for code context**

---

## Migration Effort Estimation

### Phase 1: Structure Creation (2-4 hours)
- Create `.claude/skills/` directory structure
- Create 8 skill folders
- Create skill.md templates
- Create resources/ subfolders

### Phase 2: Content Migration (4-6 hours)
- Extract sections from CLAUDE.md
- Refactor into skill instructions
- Create metadata for each skill
- Link to existing docs in resources/

### Phase 3: Testing (2-3 hours)
- Test skill discovery
- Verify progressive loading
- Ensure MCP integration still works
- Test slash commands compatibility

### Phase 4: Documentation (1-2 hours)
- Update README
- Update CHANGELOG
- Add migration guide
- Document skill usage

**Total Effort**: 9-15 hours (1-2 days)

---

## Risk Assessment

### Risks of Migration

| Risk | Severity | Mitigation |
|------|----------|------------|
| Breaking existing workflows | Medium | Keep CLAUDE.md as fallback during migration |
| Incomplete skill coverage | Low | Validate all sections migrated |
| MCP integration issues | Low | MCPs work independently of Skills |
| User confusion | Medium | Clear documentation + migration guide |
| Token limit during migration | Low | Use git checkpoints frequently |

### Risks of Status Quo

| Risk | Severity | Impact |
|------|----------|--------|
| CLAUDE.md grows beyond maintainable | High | Already 49KB, will grow |
| Context window waste | Medium | 75% token waste per session |
| Slower context loading | Medium | 12K tokens every session |
| Harder to update specific sections | Medium | Must edit monolithic file |

---

## Decision Matrix

### Factors to Consider

| Factor | Status Quo | Hybrid (Skills + MCP) | Full Skills |
|--------|------------|---------------------|-------------|
| **Token efficiency** | ❌ Poor | ✅ Excellent | ✅ Excellent |
| **Maintenance effort** | ⚠️ Medium | ✅ Good | ⚠️ High |
| **Migration cost** | ✅ None | ⚠️ Medium | ❌ High |
| **MCP preservation** | ✅ Yes | ✅ Yes | ❌ No |
| **Slash commands** | ✅ Keep | ✅ Keep | ⚠️ Replace |
| **Learning curve** | ✅ None | ⚠️ Small | ❌ Large |
| **Composability** | ❌ None | ✅ Good | ✅ Excellent |
| **Progressive disclosure** | ❌ No | ✅ Yes | ✅ Yes |

---

## Final Recommendation

### ✅ Adopt Two-Tier Skills Architecture

**Hybrid approach with project-specific skills support**

**Why**:
1. **Token efficiency**: 78% reduction in wasted tokens
2. **Maintain MCP strengths**: Don't lose our competitive advantage
3. **Keep slash commands**: Proven workflow automation
4. **Moderate effort**: 1-2 days vs months of refactoring
5. **Composability**: Load only relevant knowledge per task
6. **Future-proof**: Easier to add new skills than extend monolith
7. **Project-specific**: Each project creates domain-specific skills

### Two-Tier Architecture

**Tier 1: Toolkit Skills** (shipped with best-practice/)
```
best-practice/
└── .claude/
    └── skills/
        ├── quality-standards/      # Core quality enforcement
        ├── tdd-workflow/           # Test-driven development
        ├── problem-solving/        # Debugging techniques
        ├── git-workflow/           # Version control patterns
        ├── file-placement/         # Structure rules
        ├── planning-mode/          # Discovery-first planning
        ├── mcp-usage/              # MCP tool integration
        └── context-management/     # Token optimization
```

**Tier 2: Project Skills** (created per-project)
```
project-root/
└── .claude/
    └── skills/
        ├── api-design/             # Project-specific API patterns
        ├── authentication/         # Auth implementation details
        ├── database-schema/        # DB conventions
        ├── frontend-components/    # Component architecture
        └── deployment-workflow/    # Deploy procedures
```

**Discovery Order**:
1. Load project skills first (highest priority)
2. Load toolkit skills second (fallback/foundation)
3. Progressive disclosure for both tiers

**Benefits**:
- ✅ Toolkit skills = Universal best practices
- ✅ Project skills = Domain-specific knowledge
- ✅ Projects customize without modifying toolkit
- ✅ Clear separation of concerns
- ✅ Toolkit updates don't overwrite project skills

### Skill Creation Template

**For projects to create their own skills**:

```markdown
# Skill Template (.claude/skills/[name]/skill.md)

---
name: [Skill Name]
description: [Brief description of what this skill provides]
tags: [tag1, tag2, tag3]
auto_load_triggers: [keyword1, keyword2]
priority: project  # or "toolkit"
---

## Purpose

[What this skill teaches Claude about your project]

## When to Use

[Specific scenarios where this skill is relevant]

## Instructions

[Detailed procedural knowledge for Claude to follow]

## Examples

[Code examples, patterns, or use cases]

## Resources

- Link to: resources/[reference-file].md
- Link to: project docs
```

**Action Plan**:
1. Create toolkit skills in `best-practice/.claude/skills/`
2. Migrate CLAUDE.md into 8 focused toolkit skills
3. Create skill creation template
4. Document how to create project skills
5. Add skill template to smart_install.sh
6. Test two-tier discovery
7. Monitor token usage improvements

**Success Criteria**:
- [ ] Each toolkit skill ≤5KB
- [ ] Metadata ≤100 tokens per skill
- [ ] Progressive loading working
- [ ] Two-tier discovery (project > toolkit)
- [ ] MCP integration preserved
- [ ] Slash commands functional
- [ ] Template for project skill creation
- [ ] Documentation for creating project skills
- [ ] 70%+ token reduction measured

---

## Project-Specific Skills Guide

### When to Create Project Skills

**Create project skills when**:
- Project has unique domain knowledge (e.g., healthcare compliance, fintech regulations)
- Specific API patterns or conventions (e.g., REST endpoint naming)
- Custom architecture patterns (e.g., event-driven, microservices)
- Deployment or infrastructure procedures
- Team-specific coding standards
- Business logic patterns that repeat

**Don't create project skills for**:
- General best practices (covered by toolkit skills)
- One-off instructions (use prompts instead)
- Temporary requirements (document in project README)

### Example: E-commerce Project Skills

**Skill 1: Product Catalog Patterns**
```markdown
---
name: Product Catalog Patterns
description: Product data modeling and API conventions for catalog service
tags: products, catalog, api, data-model
auto_load_triggers: product, catalog, inventory, variant
priority: project
---

## Purpose

Teaches Claude how to work with our product catalog service architecture,
including product variants, inventory management, and pricing rules.

## Data Model

Products have this structure:
- Product (base entity)
- ProductVariant (SKU-level)
- InventoryRecord (stock levels)
- PriceRule (dynamic pricing)

## API Conventions

**Endpoint pattern**: `/api/v1/catalog/{resource}/{id}`

**Variant selection**: Always use `variantId` not `productId` for cart operations

**Inventory checks**: ALWAYS check inventory before allowing add-to-cart

## Code Patterns

\`\`\`python
# Right way to add to cart
variant = get_product_variant(variant_id)
if variant.inventory.available_quantity > 0:
    cart.add_item(variant_id, quantity=1)
else:
    raise OutOfStockError(f"Variant {variant_id} out of stock")

# Wrong - don't use product_id for cart
cart.add_item(product_id, quantity=1)  # ❌
\`\`\`

## Resources

- See: docs/architecture/product-catalog.md
- See: api-specs/catalog-api.yaml
```

**Skill 2: Payment Processing**
```markdown
---
name: Payment Processing
description: Stripe integration patterns and payment workflow
tags: payments, stripe, transactions, checkout
auto_load_triggers: payment, checkout, stripe, transaction
priority: project
---

## Purpose

Ensures Claude follows our payment processing patterns including
idempotency, webhook handling, and PCI compliance.

## Payment Flow

1. Create PaymentIntent (idempotent with `idempotency_key`)
2. Collect payment method from customer
3. Confirm PaymentIntent
4. Handle webhook for async updates
5. Update order status

## Critical Rules

**ALWAYS use idempotency keys**:
\`\`\`python
payment_intent = stripe.PaymentIntent.create(
    amount=total_cents,
    currency="usd",
    idempotency_key=f"order_{order_id}"  # REQUIRED
)
\`\`\`

**NEVER store raw card data**:
- Use Stripe Elements (frontend)
- Use PaymentMethod tokens only
- PCI compliance violation otherwise

**ALWAYS verify webhook signatures**:
\`\`\`python
try:
    event = stripe.Webhook.construct_event(
        payload, sig_header, webhook_secret
    )
except stripe.error.SignatureVerificationError:
    return 400  # Invalid signature
\`\`\`

## Resources

- See: docs/guides/payment-integration.md
- See: .env.example (webhook secret configuration)
```

### Example: Machine Learning Project Skills

**Skill: Model Training Workflow**
```markdown
---
name: Model Training Workflow
description: MLOps patterns for model training, evaluation, and deployment
tags: ml, training, mlops, models
auto_load_triggers: model, training, dataset, evaluation
priority: project
---

## Purpose

Standardizes model training workflow including data versioning,
experiment tracking, and model registry integration.

## Training Pipeline

1. Load versioned dataset (DVC)
2. Run experiment with MLflow tracking
3. Evaluate on validation set
4. Log metrics and artifacts
5. Register model if metrics improve
6. Deploy to staging environment

## Code Patterns

**Always track experiments**:
\`\`\`python
import mlflow

with mlflow.start_run(run_name=f"experiment_{timestamp}"):
    # Log parameters
    mlflow.log_params({
        "learning_rate": lr,
        "batch_size": batch_size,
        "epochs": epochs
    })

    # Train model
    model = train(data, params)

    # Log metrics
    mlflow.log_metrics({
        "accuracy": accuracy,
        "f1_score": f1,
        "loss": loss
    })

    # Log model
    mlflow.sklearn.log_model(model, "model")
\`\`\`

**Always use data versioning**:
\`\`\`bash
# Pull specific dataset version
dvc pull data/train.csv.dvc --rev v2.1.0

# Don't train on unversioned data
\`\`\`

## Resources

- See: docs/ml-ops/training-guide.md
- See: mlflow_config.yaml
```

### Skill Creation Workflow

**Step 1: Identify Domain Knowledge**
```
Ask yourself:
- What does Claude need to know about THIS project specifically?
- What patterns do we repeat that aren't general best practices?
- What mistakes could Claude make without project context?
```

**Step 2: Create Skill Structure**
```bash
cd project-root
mkdir -p .claude/skills/[skill-name]/resources
touch .claude/skills/[skill-name]/skill.md
```

**Step 3: Write Skill Content**
```markdown
Use template:
1. Metadata (name, description, tags, triggers)
2. Purpose (what this teaches)
3. Instructions (how to use)
4. Examples (code patterns)
5. Resources (links to docs)
```

**Step 4: Test Skill Loading**
```
1. Use trigger keywords in prompt
2. Verify skill loads (check context)
3. Validate Claude follows patterns
4. Refine triggers if needed
```

**Step 5: Document in Project README**
```markdown
## Project Skills

This project uses custom Claude skills for:
- Product catalog patterns (`.claude/skills/product-catalog/`)
- Payment processing (`.claude/skills/payments/`)

To add new skills, see: `.claude/skills/README.md`
```

### Best Practices for Project Skills

**DO**:
- ✅ Keep skills ≤5KB (split large domains)
- ✅ Use specific, unique trigger keywords
- ✅ Include code examples (not just descriptions)
- ✅ Link to project docs for details
- ✅ Update skills when patterns change
- ✅ Review skills in code reviews

**DON'T**:
- ❌ Duplicate toolkit skill content
- ❌ Create skills for temporary things
- ❌ Use vague trigger keywords (e.g., "code")
- ❌ Write entire documentation in skill (link instead)
- ❌ Let skills become stale

### Integration with Toolkit

**Toolkit skills provide foundation**:
- Quality standards (testing, documentation)
- TDD workflow (red-green-refactor)
- Problem-solving (debugging techniques)
- Git workflow (commits, checkpoints)

**Project skills provide specialization**:
- Domain-specific patterns (your business logic)
- API conventions (your endpoints)
- Data models (your schema)
- Deployment procedures (your infrastructure)

**They work together**:
```
User: "Add payment processing to checkout"

Claude loads:
1. Project skill: Payment Processing (specific patterns)
2. Toolkit skill: TDD Workflow (write tests first)
3. Toolkit skill: Quality Standards (pre-commit checks)

Result:
- Follows your payment patterns
- Uses TDD approach
- Meets quality standards
```

### Skill Maintenance

**When to update project skills**:
- API changes (new endpoints, changed contracts)
- Architecture refactoring (new patterns adopted)
- New team members join (common mistakes observed)
- Post-mortems (issues that could be prevented)

**Review schedule**:
- Every sprint: Check if new patterns emerged
- Every quarter: Validate all skills still accurate
- When onboarding: Use as teaching material

### Smart Install Integration

**Proposal**: smart_install.sh creates skill template

```bash
# After installing toolkit, create project skill template
mkdir -p .claude/skills/example-skill/resources
cat > .claude/skills/example-skill/skill.md <<'EOF'
---
name: Example Skill
description: Replace with your project-specific knowledge
tags: example, replace-me
auto_load_triggers: example
priority: project
---

## Purpose

[What this skill teaches Claude about your project]

## Instructions

[Detailed patterns and conventions]

## Examples

[Code examples]

## Resources

- Link to project docs
EOF

echo "✅ Created example skill template at .claude/skills/example-skill/"
echo "   Customize it for your project's domain knowledge"
```

---

## Next Steps

1. **Decision**: User approval for two-tier skills architecture
2. **Planning**: Create detailed migration plan (use `/plan`)
3. **Implementation**: Migrate CLAUDE.md into 8 toolkit skills
4. **Template**: Create skill creation template and docs
5. **Install**: Update smart_install.sh to create project skill template
6. **Testing**: Validate two-tier discovery works
7. **Documentation**: Write guide for creating project skills
8. **Measurement**: Track token usage before/after

---

## Appendix: Skills vs Slash Commands

**When to use Skills**:
- Domain knowledge (TDD principles, quality standards)
- Coding patterns (file placement, git workflow)
- Problem-solving techniques (debugging methods)
- Context-dependent loading (only when relevant)

**When to use Slash Commands**:
- Workflow automation (/plan, /tdd, /checkpoint)
- User-initiated actions (/spec, /debug)
- Sequential processes (/execute-plan)
- Explicit invocation preferred

**They're Complementary**:
- Slash command triggers workflow
- Skill provides domain knowledge
- MCP handles data access
- Subagent executes specialized tasks

**Example**:
```
User: /tdd implement user authentication

Flow:
1. Slash command: /tdd triggered
2. Skill loaded: TDD Workflow (auto-discovered)
3. Skill loaded: Quality Standards (context-relevant)
4. MCP called: validate_task_alignment
5. Implementation: Red-Green-Refactor cycle
6. MCP called: run_quality_gate
7. Complete: Task finished
```

---

**Last Updated**: 2025-11-14
**Review**: Present to user for decision
**Approval Needed**: Yes - migration requires user buy-in
