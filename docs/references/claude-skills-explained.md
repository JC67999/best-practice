# Skills Explained: How Skills Compare to Prompts, Projects, MCP, and Subagents

**Source**: https://claude.com/blog/skills-explained
**Added**: 2025-11-14
**Purpose**: Reference guide for understanding Claude's agentic ecosystem components

---

## Overview

This article explains Claude's agentic ecosystem components and how they work together. Skills are specialized folders containing instructions and resources that Claude dynamically discovers when relevant to tasks.

---

## What Are Skills?

Skills function as domain-specific knowledge packages. According to the article:

> "Skills are folders containing instructions, scripts, and resources that Claude discovers and loads dynamically when relevant to a task."

### Progressive Disclosure Model

Skills employ a progressive loading strategy to optimize token usage:

1. **Metadata first** (~100 tokens) - Basic skill information
2. **Full instructions when needed** (<5k tokens) - Complete skill details
3. **Bundled files only as required** - Resources loaded on demand

### Ideal Use Cases

- **Organizational workflows**: Brand guidelines, compliance procedures
- **Domain expertise**: Excel formulas, PDF manipulation
- **Personal preferences**: Note-taking systems, coding patterns

---

## Comparison With Other Tools

### Prompts

**What**: Natural language instructions provided during conversations

**Characteristics**:
- Conversational and reactive
- Useful for one-off requests
- Provides immediate context
- Does NOT persist across sessions

**Best for**: Ad-hoc instructions, immediate guidance

---

### Projects

**What**: Self-contained workspaces with chat histories and knowledge bases

**Characteristics**:
- 200K context window per project
- Expandable to 10x via RAG mode
- Persistent context across sessions
- Workspace organization

**Best for**: Long-term work, background knowledge, persistent context

---

### Subagents

**What**: Specialized AI assistants with independent context windows

**Characteristics**:
- Custom prompts and instructions
- Specific tool permissions
- Independent context isolation
- Available in Claude Code and Agent SDK

**Best for**: Task delegation, specialized workflows, context isolation

---

### MCP (Model Context Protocol)

**What**: Open standard connecting Claude to external systems

**Characteristics**:
- Connects to databases, business tools, development environments
- Handles data connectivity (not procedural knowledge)
- Enables real-time data access
- Extensible via custom servers

**Best for**: External system integration, data connectivity

---

## How They Work Together

The article emphasizes combining these components for powerful workflows:

| Component | Role |
|-----------|------|
| **Skills** | Teach expertise (how to analyze competitively) |
| **MCP** | Provide connectivity (access to data sources) |
| **Projects** | Maintain context (background knowledge) |
| **Subagents** | Execute tasks (independent specialization) |
| **Prompts** | Guide conversations (moment-to-moment direction) |

### Integration Philosophy

These components are designed to work synergistically:
- Skills provide the "how-to" knowledge
- MCP provides the "where" (data access)
- Projects provide the "what" (context)
- Subagents provide the "who" (specialized execution)
- Prompts provide the "when" (immediate direction)

---

## Practical Example: Research Agent Workflow

The article demonstrates integration with a research agent:

1. **Projects** hold background research and context
2. **MCP** connects to Google Drive and GitHub for data access
3. **Skills** provide analytical frameworks and methodologies
4. **Subagents** handle specialized analysis tasks
5. **Prompts** refine directions moment-to-moment

**Flow**:
```
User prompt → Claude loads relevant Skill → Skill uses MCP for data →
Subagent executes specialized analysis → Results stored in Project context
```

---

## Key Takeaways

1. **Progressive disclosure**: Skills load only what's needed when needed
2. **Complementary design**: Each component serves a distinct purpose
3. **Integration power**: Combining components creates sophisticated workflows
4. **Context optimization**: Use Projects for persistence, Subagents for isolation
5. **Data vs Knowledge**: MCP handles connectivity, Skills handle expertise

---

## Implications for Best Practice Toolkit

**Relevant to our toolkit**:
- Our MCP servers align with this model (Memory, Quality, Project MCPs)
- CLAUDE.md functions similarly to a Skill (procedural knowledge)
- Slash commands could be enhanced with Skills
- Subagents for exploration already in use (Task tool with Explore subagent)

**Opportunities**:
- Create Skills for common workflows (TDD, debugging, refactoring)
- Use Skills for organization-specific coding standards
- Combine Skills + MCP for powerful quality gates
- Consider Skills as alternative/complement to slash commands

---

## Related Documentation

- **MCP Implementation**: See `/docs/design/MCP_IMPLEMENTATION_APPROACH.md`
- **Slash Commands**: See CLAUDE.md section on workflow automation
- **Subagents**: See CLAUDE.md Task tool usage guidelines

---

**Last Updated**: 2025-11-14
**Review**: Consider when evaluating new Claude features or workflow automation opportunities
