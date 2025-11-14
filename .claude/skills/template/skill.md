---
name: Example Project Skill
description: Replace this with your project-specific knowledge
tags: example, replace-me, your-domain
auto_load_triggers: example, replace
priority: project
---

# Example Project Skill

> **This is a template** - Copy and customize for your project's domain-specific knowledge

## Purpose

[Explain what this skill teaches Claude about YOUR specific project]

Examples:
- API conventions for your service
- Data model patterns
- Business logic rules
- Deployment procedures
- Team coding standards

---

## When to Use

[Describe scenarios where this skill is relevant]

Examples:
- When working with user authentication in this project
- When creating API endpoints following our conventions
- When implementing payment processing
- When deploying to our infrastructure

---

## Instructions

[Detailed procedural knowledge for Claude to follow]

### Pattern 1: [Name]

**Description**: [What this pattern is for]

**Example**:
```python
# Right way
def example_function():
    # Your project-specific implementation pattern
    pass

# Wrong way - what NOT to do
def bad_example():
    pass  # Anti-pattern
```

### Pattern 2: [Name]

**Critical Rules**:
- ALWAYS [do this]
- NEVER [do that]
- CHECK [this condition]

---

## Code Examples

### Example 1: [Scenario]

```python
# Your project-specific code example
class UserProfile:
    """Example from your project."""
    def __init__(self, user_id: str):
        self.user_id = user_id
        # Project-specific implementation
```

### Example 2: [Scenario]

```python
# Another relevant example
def process_payment(amount: float):
    # Your project's payment processing pattern
    pass
```

---

## Common Mistakes to Avoid

**DON'T**:
- ❌ [Common mistake in your project]
- ❌ [Another anti-pattern]
- ❌ [What developers often get wrong]

**DO**:
- ✅ [Correct approach for your project]
- ✅ [Best practice in your domain]
- ✅ [What works well]

---

## Resources

- Link to: docs/architecture/[your-design-doc].md
- Link to: api-specs/[your-api-spec].yaml
- Link to: [your-project-specific-documentation]

---

## How to Use This Template

1. **Copy this file** to a new skill folder:
   ```bash
   cp .claude/skills/template/skill.md .claude/skills/your-skill-name/skill.md
   ```

2. **Update metadata** (top section):
   - Change `name` to your skill name
   - Update `description` with what this skill provides
   - Replace `tags` with relevant keywords
   - Update `auto_load_triggers` with keywords that should load this skill
   - Keep `priority: project` (higher than toolkit)

3. **Fill in sections**:
   - Purpose: What Claude learns from this skill
   - When to Use: Scenarios where this is relevant
   - Instructions: Detailed patterns and rules
   - Code Examples: Real examples from your project
   - Common Mistakes: Anti-patterns to avoid
   - Resources: Links to your project docs

4. **Test the skill**:
   - Use trigger keywords in prompts
   - Verify skill loads automatically
   - Check Claude follows your patterns

5. **Maintain the skill**:
   - Update when patterns change
   - Add new examples as discovered
   - Remove outdated information
   - Review quarterly for accuracy

---

## Example Skills for Different Projects

### E-commerce Project
```
Skill: Product Catalog Patterns
Triggers: product, catalog, inventory, variant
Purpose: Product data modeling and API conventions
```

### ML/AI Project
```
Skill: Model Training Workflow
Triggers: model, training, dataset, evaluation
Purpose: MLOps patterns for training and deployment
```

### API Service
```
Skill: API Design Standards
Triggers: endpoint, api, rest, graphql
Purpose: API conventions and patterns
```

### DevOps/Infrastructure
```
Skill: Deployment Procedures
Triggers: deploy, deployment, release, infrastructure
Purpose: How to deploy and manage infrastructure
```

---

## Best Practices for Project Skills

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

---

## Integration with Toolkit Skills

**This skill works together with toolkit skills**:
- **Quality Standards**: Your patterns + toolkit quality checks
- **TDD Workflow**: Your tests + toolkit TDD approach
- **File Placement**: Your files + toolkit structure rules
- **Git Workflow**: Your commits + toolkit git patterns

**Together they ensure**:
- Claude follows your project patterns
- Meets general quality standards
- Uses proper git workflow
- Maintains clean structure

---

**Last Updated**: [Date]
**Maintained By**: [Team/Person]
**Review Schedule**: [Frequency]
