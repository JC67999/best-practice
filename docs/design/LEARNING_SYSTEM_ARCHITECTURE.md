# Learning System Architecture

> **Purpose**: Self-learning system that continuously improves best practices
> **Status**: Design Phase (V2)
> **Last Updated**: 2025-10-29

---

## Overview

The Learning System enables the Best Practice Toolkit to continuously improve by researching the latest best practices from the internet and updating quality standards accordingly.

## Goals

1. **Automated Research**: Regularly search for best practices in key technology areas
2. **Knowledge Storage**: Store learnings in structured, searchable format
3. **Standards Updates**: Automatically suggest updates to CLAUDE.md and quality gates
4. **Continuous Improvement**: Self-improve over time based on latest industry practices

## Architecture

### Components

#### 1. Learning MCP Server (`learning_mcp.py`)

**Location**: `mcp-servers/learning_mcp.py`

**MCP Tools**:
- `search_best_practices` - Search web for best practices on specific topics
- `store_learning` - Store discovered best practices
- `get_learnings` - Retrieve stored learnings by topic/date
- `generate_report` - Create summary report of recent learnings

**Dependencies**:
- requests (web search)
- beautifulsoup4 (HTML parsing)
- Memory MCP (storage integration)

#### 2. Learning Daemon (`learning_daemon.py`)

**Location**: Root directory (or scripts/)

**Purpose**: Scheduled execution of learning tasks

**Features**:
- Configurable schedule (daily/weekly)
- Topic rotation (Python → Angular → Redis → etc.)
- Safe execution with error handling
- Session logging

#### 3. Storage Format

**Location**: `~/.claude_memory/learnings/`

**Structure**:
```
learnings/
├── python/
│   ├── 2025-10-29_coding-standards.json
│   └── 2025-10-25_testing-practices.json
├── angular/
├── redis/
└── ...
```

**JSON Format**:
```json
{
  "topic": "python",
  "subtopic": "coding-standards",
  "date": "2025-10-29",
  "source_url": "https://...",
  "learnings": [
    {
      "practice": "Use type hints for all public functions",
      "reasoning": "Improves IDE support and catches errors early",
      "confidence": "high",
      "applicable_to": ["best-practice-toolkit"]
    }
  ],
  "suggested_updates": {
    "CLAUDE.md": ["Add type hints requirement to code style"],
    "quality_mcp.py": ["Add type hint validation check"]
  }
}
```

## Research Topics

### Priority Topics

1. **Python** - Language best practices, typing, testing
2. **Claude AI** - Prompt engineering, token optimization, API usage
3. **Testing** - pytest best practices, coverage strategies, TDD
4. **Git** - Commit conventions, workflow patterns
5. **Documentation** - Markdown standards, API docs, READMEs

### Secondary Topics

6. **Angular** - Component design, state management
7. **Redis** - Caching strategies, performance
8. **Nginx** - Configuration, security
9. **Docker** - Container best practices
10. **CI/CD** - GitHub Actions, deployment strategies

## Web Search Strategy

### Search Queries

For each topic, use targeted queries:
- "[Topic] best practices 2025"
- "[Topic] coding standards latest"
- "how to improve [topic] code quality"
- "[topic] common mistakes to avoid"
- "[topic] performance optimization"

### Source Prioritization

**Trusted sources** (high confidence):
1. Official documentation sites
2. Tech company engineering blogs (Google, Netflix, etc.)
3. Authoritative community resources (Real Python, Angular.io)

**Community sources** (medium confidence):
4. Stack Overflow top answers
5. Dev.to articles with high engagement
6. GitHub repos with >1k stars

**General sources** (low confidence):
7. Medium articles
8. Personal blogs (verify with other sources)

### Content Extraction

1. Parse HTML to extract main content
2. Identify best practice recommendations
3. Extract code examples
4. Note source URL and date
5. Calculate confidence score based on source type

## Integration with Existing MCPs

### Memory MCP

**Usage**: Store learnings persistently

```python
# Store learning
memory_mcp.save_learning(
    project_path=toolkit_path,
    topic="python",
    learning_data={...}
)

# Retrieve learnings
learnings = memory_mcp.get_learnings(
    topic="python",
    since="2025-10-01"
)
```

### Quality MCP

**Usage**: Apply learnings to quality checks

```python
# Get applicable learnings
learnings = learning_mcp.get_learnings(topic="python")

# Update quality standards
quality_mcp.update_standards(learnings)
```

### Project MCP

**Usage**: Suggest learnings during task planning

```python
# Get relevant learnings for current task
task = "Add email validation function"
relevant_learnings = learning_mcp.search_learnings(
    query="python validation best practices"
)
```

## Safety Considerations

### Web Request Safety

- **Rate limiting**: Max 10 requests per hour
- **Timeout**: 10 seconds per request
- **Retry logic**: Max 3 retries with exponential backoff
- **User agent**: Identify as Best Practice Toolkit
- **Respect robots.txt**: Check before scraping

### Content Validation

- **Sanity checks**: Reject obviously incorrect advice
- **Cross-reference**: Verify practices across multiple sources
- **Confidence scoring**: Flag low-confidence learnings
- **Human review**: Mark suggestions for manual review

### Standards Updates

- **Never auto-apply**: Always suggest, never automatically update CLAUDE.md
- **Version control**: All updates via git commits with clear messages
- **Rollback**: Keep previous versions for comparison
- **Testing**: Validate updated standards don't break existing projects

## Workflow

### Automated Learning Cycle

```
1. Daemon triggers (daily/weekly)
   ↓
2. Select topic (rotate through list)
   ↓
3. Search web for best practices
   ↓
4. Extract and parse content
   ↓
5. Store learnings in Memory MCP
   ↓
6. Generate suggested updates
   ↓
7. Create review report
   ↓
8. Notify user (optional)
```

### Manual Review Workflow

```
1. User reviews learning report
   ↓
2. Accepts/rejects suggestions
   ↓
3. Approved updates applied to CLAUDE.md
   ↓
4. Quality gate validates changes
   ↓
5. Commit updates to git
   ↓
6. Learning marked as applied
```

## Implementation Phases

### Phase 1: Foundation (v2_learn_1-2)

- ✅ Architecture design (this document)
- Create learning_mcp.py skeleton
- Define tool interfaces
- Set up storage structure

### Phase 2: Web Search (v2_learn_3)

- Implement search_best_practices tool
- Add web scraping logic
- Parse and extract content
- Calculate confidence scores

### Phase 3: Storage & Retrieval (v2_learn_4)

- Implement store_learning tool
- Integrate with Memory MCP
- Add get_learnings retrieval
- Create generate_report tool

### Phase 4: Automation (v2_learn_5)

- Create learning_daemon.py
- Add scheduling logic
- Implement topic rotation
- Add session logging

### Phase 5: Integration (Future)

- Connect to Quality MCP
- Suggest CLAUDE.md updates
- Add CLI commands
- User notification system

## Success Metrics

### Learning Quality

- **Accuracy**: >90% of learnings validated as correct
- **Relevance**: >80% applicable to toolkit projects
- **Freshness**: Learnings <6 months old
- **Coverage**: All priority topics covered monthly

### System Performance

- **Uptime**: >99% daemon availability
- **Response time**: <30s per search
- **Storage efficiency**: <1MB per month of learnings
- **Error rate**: <5% failed searches

### Impact

- **Standards updates**: ≥1 meaningful CLAUDE.md update per month
- **Quality improvements**: Measurable improvement in code quality scores
- **User adoption**: >50% of suggested updates accepted
- **Self-improvement**: Toolkit quality score increases over time

## Configuration

### Learning Daemon Config

```json
{
  "schedule": "daily",
  "topics": ["python", "claude-ai", "testing"],
  "max_searches_per_day": 10,
  "confidence_threshold": 0.7,
  "auto_report": true,
  "notify_user": false
}
```

### MCP Server Config

```json
{
  "rate_limit": 10,
  "timeout": 10,
  "max_retries": 3,
  "cache_duration": 86400,
  "user_agent": "BestPracticeToolkit/2.0"
}
```

## Future Enhancements

### V3 Features

- **AI Analysis**: Use Claude to analyze best practices
- **Trend Detection**: Identify emerging practices
- **Comparative Analysis**: Compare practices across languages
- **Community Integration**: Share learnings with community
- **Feedback Loop**: Learn from project outcomes

### Advanced Features

- **Custom Topics**: User-defined research topics
- **Priority Learning**: Focus on frequently used technologies
- **Conflict Resolution**: Handle conflicting best practices
- **Historical Tracking**: Track evolution of practices over time

---

**Status**: Design complete, ready for implementation
**Next**: v2_learn_2 - Create learning_mcp.py skeleton
