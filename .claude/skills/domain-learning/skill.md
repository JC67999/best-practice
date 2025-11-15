---
name: Domain Learning
description: Project-objective-driven autonomous research and knowledge building
tags: research, learning, knowledge-base, domain-expertise, objective-driven
auto_load_triggers: research, learn, unknown, unfamiliar, how does, what is
priority: toolkit
---

# Domain Learning Skill

## Purpose

**Project-Objective-Driven Research**: Adapts to the objective of whatever project it's injected into and continuously researches that project's specific domain to support achieving that objective.

**Examples**:
- **rapid-pm**: Researches project management methodologies, PM tools, artifacts, best practices
- **ai-task-optimisation-MVP**: Researches optimization algorithms, solver techniques, performance strategies
- **document-generator**: Researches documentation methodologies, exemplar templates, methodology-specific best practices
- **best-practice**: Researches Claude Code best practices, MCP patterns, skills usage, development workflows

**How it works**: When encountering unfamiliar concepts in the project domain, this skill triggers domain-specific research, fetches relevant documentation, and builds a local knowledge base that directly supports the project's objective. It becomes a domain expert for whatever domain it's deployed in.

---

## When to Use

**Automatically triggers when**:
- Encountering unfamiliar domain concepts
- User mentions "research" or "learn about"
- Working on domain-specific features without context
- User asks "what is [domain concept]" or "how does [domain thing] work"

**Manual trigger**:
- User: "Research [topic] for this project"
- User: "Build knowledge base on [domain]"

---

## Research Workflow

### Step 1: Identify Knowledge Gap

**When encountering unfamiliar concept**:
```
User: "Optimize the transformer attention mechanism"
Claude detects: "transformer attention mechanism" - unfamiliar
Trigger: Domain Learning skill
```

### Step 2: Research Strategy

**Determine what to research**:
1. Extract key concepts from request
2. Check if already in knowledge base (`docs/references/domain-knowledge/`)
3. If missing, initiate research workflow

### Step 3: Execute Research

**Use available tools**:

**WebSearch** for overview:
```
WebSearch: "transformer attention mechanism optimization techniques 2025"
→ Find: Latest papers, blog posts, documentation
→ Filter: Most relevant, recent, authoritative sources
```

**WebFetch** for deep dives:
```
For top 3-5 results:
WebFetch: [URL]
→ Extract: Key concepts, techniques, code examples
→ Summarize: Core ideas in 500-1000 words
→ Save: To local knowledge base
```

### Step 4: Store Knowledge

**Create structured knowledge base**:

```
docs/references/domain-knowledge/
├── index.md                           # Master index of all topics
├── ai-optimization/
│   ├── transformer-attention.md       # Fetched and summarized
│   ├── model-quantization.md
│   ├── inference-optimization.md
│   └── sources.json                   # Track sources
├── machine-learning/
│   ├── gradient-descent.md
│   └── regularization.md
└── [other-domains]/
```

**Document format**:
```markdown
# [Topic Name]

**Last Updated**: [Date]
**Sources**: [URLs]
**Relevance**: [Why this matters for our project]

## Overview
[2-3 sentence summary]

## Key Concepts
- Concept 1: [Explanation]
- Concept 2: [Explanation]

## Techniques
1. **[Technique Name]**
   - Description: [What it is]
   - Use case: [When to use]
   - Example: [Code/pseudocode]

## Best Practices
- [Practice 1]
- [Practice 2]

## Common Pitfalls
- [Pitfall 1]
- [Pitfall 2]

## Code Examples
```python
# Example implementation
def example():
    pass
```

## Resources
- [Source 1 - URL]
- [Source 2 - URL]

## Related Topics
- [Related Topic 1] → See: [link]
- [Related Topic 2] → See: [link]
```

### Step 5: Create Domain Skill (Optional)

**For frequently used domains, create a dedicated skill**:

```bash
# Create domain-specific skill
mkdir -p .claude/skills/ai-optimization/resources
cp docs/references/domain-knowledge/ai-optimization/* \
   .claude/skills/ai-optimization/resources/

# Create skill.md that references the knowledge base
cat > .claude/skills/ai-optimization/skill.md <<EOF
---
name: AI Optimization
description: Transformer optimization, quantization, inference techniques
tags: ai, optimization, transformers, inference
auto_load_triggers: optimize, transformer, quantization, inference
priority: project
---

# AI Optimization

## Purpose
Project-specific knowledge about AI model optimization techniques.

## Knowledge Base
See resources/ folder for detailed documentation on:
- Transformer attention optimization
- Model quantization techniques
- Inference optimization
- [etc]

[Include key patterns and examples directly in skill]
EOF
```

---

## Implementation Pattern

### Automatic Research Trigger

```python
# Pseudo-code for Claude's decision process
def handle_user_request(request):
    # Extract key concepts
    concepts = extract_concepts(request)

    # Check knowledge base
    for concept in concepts:
        if not in_knowledge_base(concept):
            if is_domain_specific(concept):
                # Trigger research
                research_and_store(concept)

    # Proceed with request using augmented knowledge
    execute_request(request)

def research_and_store(concept):
    # 1. Search for information
    search_results = WebSearch(f"{concept} best practices 2025")

    # 2. Fetch top sources
    content = []
    for url in search_results[:3]:
        content.append(WebFetch(url, f"Explain {concept} with examples"))

    # 3. Synthesize and store
    summary = synthesize(content)
    save_to_knowledge_base(concept, summary)

    # 4. Update index
    update_index(concept)
```

### Manual Research Command

**User can explicitly request research**:
```
User: "Research transformer attention optimization for this project"

Claude:
1. Searches for transformer attention optimization
2. Fetches top 5 resources
3. Creates docs/references/domain-knowledge/ai-optimization/transformer-attention.md
4. Updates docs/references/domain-knowledge/index.md
5. Reports: "Added transformer attention optimization to knowledge base"
6. Optionally: Creates ai-optimization skill for future auto-loading
```

---

## Knowledge Base Index

**Master index** (`docs/references/domain-knowledge/index.md`):

```markdown
# Domain Knowledge Base

**Purpose**: Project-specific domain knowledge accumulated through research
**Last Updated**: 2025-11-14

## Categories

### AI Optimization (8 topics)
- [Transformer Attention Optimization](ai-optimization/transformer-attention.md) - Added: 2025-11-14
- [Model Quantization](ai-optimization/model-quantization.md) - Added: 2025-11-14
- [Inference Optimization](ai-optimization/inference-optimization.md) - Added: 2025-11-10

### Machine Learning (5 topics)
- [Gradient Descent Variants](machine-learning/gradient-descent.md)
- [Regularization Techniques](machine-learning/regularization.md)

## Quick Reference

**Most Referenced Topics**:
1. Transformer Attention Optimization (12 references)
2. Model Quantization (8 references)
3. Batch Processing (6 references)

## Research Queue

**Topics to research next**:
- [ ] ONNX Runtime optimization
- [ ] TensorRT integration
- [ ] Multi-GPU training strategies
```

---

## Integration with Project Skills

**Project skills reference knowledge base**:

```markdown
# Project Skill: AI Model Optimization

## Resources
- Knowledge Base: docs/references/domain-knowledge/ai-optimization/
- See: [Transformer Attention](../../../docs/references/domain-knowledge/ai-optimization/transformer-attention.md)
- See: [Quantization](../../../docs/references/domain-knowledge/ai-optimization/model-quantization.md)

## Instructions
When optimizing models:
1. Check knowledge base for relevant techniques
2. Apply techniques documented in resources/
3. Document new learnings back to knowledge base
```

---

## Research Strategies by Domain

### AI/ML Projects

**Focus areas**:
- Model architectures
- Optimization techniques
- Training strategies
- Inference optimization
- Deployment patterns

**Sources**:
- arXiv papers
- Hugging Face documentation
- PyTorch/TensorFlow guides
- Research blogs (Google AI, OpenAI, etc.)

### Web Development Projects

**Focus areas**:
- Framework best practices
- Performance optimization
- Security patterns
- API design

**Sources**:
- Official documentation
- MDN Web Docs
- Framework guides
- Community best practices

### DevOps/Infrastructure Projects

**Focus areas**:
- Container orchestration
- CI/CD patterns
- Monitoring strategies
- Infrastructure as code

**Sources**:
- Cloud provider docs (AWS, GCP, Azure)
- Kubernetes documentation
- Tool-specific guides
- SRE resources

---

## Workflow Example

**Scenario**: Building AI optimization tool

```
User: "Add support for ONNX model optimization"

Claude (Domain Learning skill triggered):
1. Detects: "ONNX model optimization" - not in knowledge base
2. Searches: "ONNX Runtime optimization best practices 2025"
3. Fetches: Top 3 resources (ONNX docs, optimization guides, tutorials)
4. Creates: docs/references/domain-knowledge/ai-optimization/onnx-optimization.md
5. Summarizes: Key techniques (graph optimization, quantization, provider selection)
6. Updates: index.md with new topic
7. Proceeds: Implements ONNX optimization using researched knowledge
8. Documents: Actual implementation patterns back to knowledge base
```

---

## Best Practices

**DO**:
- ✅ Research before implementing unfamiliar concepts
- ✅ Store knowledge in structured format
- ✅ Update index after each research session
- ✅ Link related topics together
- ✅ Include source URLs for verification
- ✅ Date all knowledge base entries
- ✅ Create domain skills for frequently used topics

**DON'T**:
- ❌ Research without storing results (waste of effort)
- ❌ Store raw fetched content (summarize and structure)
- ❌ Ignore existing knowledge base (check first)
- ❌ Create duplicate entries (update existing)
- ❌ Forget to update index
- ❌ Skip source attribution

---

## Maintenance

**Weekly**:
- Review research queue
- Update stale entries (>6 months old)
- Add new topics as encountered

**Monthly**:
- Audit knowledge base for accuracy
- Remove outdated information
- Consolidate related topics
- Create domain skills for mature topic areas

**Quarterly**:
- Major knowledge base reorganization if needed
- Identify knowledge gaps
- Plan research sprints for critical missing topics

---

## Autonomous Learning Loop

**Continuous improvement**:

```
1. Encounter unfamiliar concept
   ↓
2. Research and store knowledge
   ↓
3. Apply knowledge to task
   ↓
4. Document actual results/learnings
   ↓
5. Update knowledge base with real-world insights
   ↓
6. Create/update domain skill if frequently used
   ↓
7. Next time: Use existing knowledge (no re-research)
```

**Over time**:
- Knowledge base grows with project
- Domain skills become more comprehensive
- Less research needed (reuse existing knowledge)
- Project-specific expertise accumulates
- Team onboarding becomes faster (knowledge base as reference)

---

## MCP Integration

**Save research sessions**:
```
mcp__memory__save_decision
Args:
  decision = "Researched [topic] and added to knowledge base"
  rationale = "Needed for [feature] implementation"
```

**Track research activity**:
```
mcp__memory__save_session_summary
Args:
  summary = "Researched 3 AI optimization topics, added to knowledge base"
  decisions = ["Using technique X for optimization based on research"]
  next_steps = ["Research [next topic] for upcoming feature"]
```

---

## Resources

- **WebSearch tool**: Find resources on topics
- **WebFetch tool**: Retrieve and summarize content
- **Knowledge base**: docs/references/domain-knowledge/
- **Domain skills**: .claude/skills/[domain-name]/
- **Template**: Use this skill as template for domain-specific learning

---

**Last Updated**: 2025-11-14
**Use Case**: AI optimization, ML projects, any domain requiring continuous learning
**Status**: Active - autonomously builds knowledge as project evolves
