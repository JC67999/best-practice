# Self-Learning System Activation Guide

> **Status**: ✅ ACTIVATED (2025-11-14)

## What Was Done

### 1. Learning MCP Configured ✅

**Added to Claude Code configuration**:
```bash
Location: ~/.config/claude/claude_desktop_config.json
Server: learning-mcp (9 tools, 3 prompts)
Status: Enabled
```

### 2. MCP Servers Updated ✅

**Updated all installed MCPs** with latest toolkit versions:
```bash
Location: ~/.mcp-servers/
Files: memory_mcp.py, quality_mcp.py, project_mcp.py, learning_mcp.py
Size: 41KB (learning_mcp.py)
```

### 3. Automation Script Created ✅

**Created auto-update script**:
```bash
Location: .claude/mcp-servers/auto_update_toolkit.sh
Features:
  - Manual scan triggering
  - Cron job setup (daily at 2 AM)
  - Status monitoring
  - Logging to ~/.claude_memory/learnings/auto_update.log
```

### 4. Documentation Updated ✅

**Updated README.md** with:
- Learning MCP section (tools, prompts, examples)
- Automation instructions
- Storage locations
- Configuration examples

**Updated CHANGELOG.md** with activation details

---

## How to Use

### Quick Start

**Method 1: Use MCP Prompts** (Recommended)
```
# In Claude Code
/mcp__learning__scan_all_resources
/mcp__learning__update_toolkit
/mcp__learning__research_topic
```

**Method 2: Use MCP Tools Directly**
```
# In Claude Code
"Scan Anthropic skills repository"
"Scan Anthropic cookbooks repository"
"Compare Anthropic skills with toolkit skills at .claude/skills"
"Suggest skill updates based on comparison"
```

**Method 3: Automated Scanning**
```bash
# Set up daily scans at 2 AM
cd /home/jc/CascadeProjects/best-practice/.claude/mcp-servers
./auto_update_toolkit.sh --setup

# Check status
./auto_update_toolkit.sh --status

# Manual scan
./auto_update_toolkit.sh
```

---

## Available Learning Tools (9 Total)

### Scanning Tools
1. **scan_anthropic_skills** - Scan 15 official skills across 5 categories
2. **scan_anthropic_cookbooks** - Scan 28 cookbooks (27.6k stars)
3. **scan_anthropic_quickstarts** - Scan 4 quickstart projects (10.2k stars)
4. **scan_anthropic_org** - Scan all 54 Anthropic repositories

### Analysis Tools
5. **compare_skills** - Compare Anthropic vs toolkit skills
6. **suggest_skill_updates** - Prioritize updates (HIGH/MEDIUM/LOW/SKIP)

### Download Tools
7. **download_skill** - Download skills from GitHub with templates

### Storage Tools
8. **store_learning** - Store best practices in JSON format
9. **get_learnings** - Retrieve learnings filtered by topic/date

---

## Available Learning Prompts (3 Total)

### 1. update_toolkit
**Complete update workflow**:
1. Scan all Anthropic resources
2. Compare with toolkit
3. Suggest priorities
4. Download recommended skills
5. Document learnings

**Usage**:
```
/mcp__learning__update_toolkit
```

### 2. research_topic
**Research best practices for specific topic**:
- Scans relevant Anthropic resources
- Extracts best practices
- Provides structured summary
- Stores learnings for future reference

**Usage**:
```
/mcp__learning__research_topic
# Then provide topic: "prompt engineering", "testing", "MCP development", etc.
```

### 3. scan_all_resources
**Comprehensive scan of ALL Anthropic resources**:
- Skills repository (15 skills)
- Cookbooks repository (28 cookbooks)
- Quickstarts repository (4 projects)
- Organization repositories (54 total)

**Usage**:
```
/mcp__learning__scan_all_resources
```

---

## What Gets Scanned

### Anthropic Skills (15 Total)
**Development** (5):
- artifacts-builder, cline-mcp-server, mcp-builder, pr-reviewer, webapp-testing

**Meta** (2):
- self-learning, skill-creator

**Documents** (5):
- docx, pdf, pptx, txt-to-speech, xlsx

**Creative** (2):
- algorithmic-art, canvas-design

**Enterprise** (1):
- brand-guidelines, internal-comms

### Anthropic Cookbooks (28 Total)
**Categories**:
- Capabilities: RAG, classification, summarization
- Tool Use: Customer service, calculator, SQL
- Multimodal: Vision, charts, forms, image generation
- Patterns: Sub-agents, PDF processing, evaluation
- Third-Party: Pinecone, Wikipedia, Voyage AI

### Anthropic Quickstarts (4 Total)
- Customer support agent
- Financial analysis
- Computer use demos
- Agent framework examples

### Anthropic Organization (54 Repositories)
**Categories**:
- 7 SDKs (Python, TypeScript, Go, etc.)
- 4 Agent frameworks
- 4 Educational resources (courses, guides)
- 4 Security tools (GitHub Actions, monitoring)
- 35+ Other tools and examples

---

## Storage Locations

### Learning Data
```
~/.claude_memory/learnings/
├── anthropic_skills.json        # Skills catalog
├── anthropic_cookbooks.json     # Cookbooks catalog
├── anthropic_quickstarts.json   # Quickstarts catalog
├── anthropic_org.json           # Org repositories catalog
├── best_practices.json          # Stored learnings by topic
└── auto_update.log              # Automation logs
```

### MCP Servers
```
~/.mcp-servers/
├── learning_mcp.py              # 41KB - Learning server
├── memory_mcp.py                # 27KB - Memory server
├── quality_mcp.py               # 43KB - Quality server
└── project_mcp.py               # 58KB - Project server
```

---

## Skill Prioritization Logic

When `suggest_skill_updates` is called, skills are prioritized:

**HIGH Priority**:
- Development tools (webapp-testing, mcp-builder, pr-reviewer)
- Meta skills (skill-creator, self-learning)

**MEDIUM Priority**:
- Document tools (pdf, xlsx, docx, pptx)
- Analysis tools (cline-mcp-server)

**LOW Priority**:
- Creative tools (algorithmic-art, canvas-design)

**SKIP**:
- Enterprise-specific (brand-guidelines, internal-comms)
- Already in toolkit

---

## Automation Details

### Cron Job Setup
```bash
# Run daily at 2 AM
0 2 * * * /path/to/auto_update_toolkit.sh >> ~/.claude_memory/learnings/auto_update.log 2>&1
```

### Manual Commands
```bash
# Check system status
./auto_update_toolkit.sh --status

# Run manual scan
./auto_update_toolkit.sh

# Set up automation
./auto_update_toolkit.sh --setup

# View logs
tail -f ~/.claude_memory/learnings/auto_update.log
```

---

## Verification Steps

### 1. Check Learning MCP is Configured
```bash
grep -A5 "learning" ~/.config/claude/claude_desktop_config.json
```

**Expected**: Should see learning server configuration

### 2. Check MCP Server Exists
```bash
ls -lh ~/.mcp-servers/learning_mcp.py
```

**Expected**: 41K file

### 3. Check Learning Tools Available
```
# In Claude Code
"List all learning MCP tools"
```

**Expected**: 9 tools listed

### 4. Run Test Scan
```
# In Claude Code
"Scan Anthropic skills repository"
```

**Expected**: JSON with 15 skills across 5 categories

### 5. Check Storage Created
```bash
ls -la ~/.claude_memory/learnings/
```

**Expected**: anthropic_skills.json file created

---

## Troubleshooting

### Learning MCP Not Showing Up

**Check configuration**:
```bash
cat ~/.config/claude/claude_desktop_config.json | grep -A5 learning
```

**Restart Claude Code** after config changes

### Scans Failing

**Check Python dependencies**:
```bash
pip install mcp
```

**Check file permissions**:
```bash
chmod +x ~/.mcp-servers/learning_mcp.py
```

### No Learnings Stored

**Run a scan first**:
```
# In Claude Code
"Scan Anthropic skills repository"
```

**Check directory exists**:
```bash
mkdir -p ~/.claude_memory/learnings
```

### Automation Not Working

**Check cron job**:
```bash
crontab -l | grep auto_update
```

**Check logs**:
```bash
tail ~/.claude_memory/learnings/auto_update.log
```

---

## Benefits of Self-Learning

### 1. Always Up-to-Date
- Toolkit automatically learns from Anthropic's latest releases
- No manual checking required
- Scheduled scans catch new skills/cookbooks immediately

### 2. Gap Detection
- Identifies missing best practices in toolkit
- Compares with official Anthropic skills
- Prioritizes what to add first

### 3. Knowledge Accumulation
- Stores learnings in structured JSON
- Searchable by topic and date
- Builds institutional knowledge over time

### 4. Zero Maintenance
- Set up once, runs automatically
- Logs all activity
- Alerts if scans fail

---

## Next Steps

### Immediate (Today)
1. ✅ Learning MCP configured
2. ✅ Documentation updated
3. ✅ Automation script created
4. ⏳ **Run first scan**: `/mcp__learning__scan_all_resources`
5. ⏳ **Review learnings**: Check `~/.claude_memory/learnings/`

### Short-term (This Week)
6. ⏳ Set up automation: `./auto_update_toolkit.sh --setup`
7. ⏳ Download 1-2 HIGH priority skills
8. ⏳ Test update_toolkit prompt end-to-end

### Long-term (Ongoing)
9. ⏳ Weekly review of new learnings
10. ⏳ Integrate new skills into toolkit
11. ⏳ Expand to scan other sources (GitHub trending, etc.)

---

## Summary

**Self-learning system is NOW ACTIVE and ready to use!**

**Quick commands**:
```bash
# Status
./auto_update_toolkit.sh --status

# Manual scan
# In Claude Code: /mcp__learning__scan_all_resources

# Set up automation
./auto_update_toolkit.sh --setup
```

**Storage**: `~/.claude_memory/learnings/`
**Logs**: `~/.claude_memory/learnings/auto_update.log`
**Config**: `~/.config/claude/claude_desktop_config.json`

---

**Last Updated**: 2025-11-14
**Status**: ✅ OPERATIONAL
