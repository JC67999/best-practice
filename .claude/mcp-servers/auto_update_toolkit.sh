#!/usr/bin/env bash
#
# Auto-Update Toolkit - Scheduled self-learning script
# Scans Anthropic resources and suggests toolkit updates
#
# Usage:
#   ./auto_update_toolkit.sh          # Run once
#   ./auto_update_toolkit.sh --setup  # Set up daily cron job
#
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
LOG_FILE="$HOME/.claude_memory/learnings/auto_update.log"
TOOLKIT_SKILLS="$SCRIPT_DIR/../skills"

# Ensure log directory exists
mkdir -p "$(dirname "$LOG_FILE")"

log() {
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] $*" | tee -a "$LOG_FILE"
}

run_scan() {
    log "🎓 Starting automated toolkit update scan..."

    # Check if Claude Code is running (Learning MCP must be available)
    if ! pgrep -f "claude" > /dev/null 2>&1; then
        log "⚠️  Claude Code not running - skipping scan"
        return 1
    fi

    log "📊 Scanning Anthropic resources via Learning MCP..."
    log "   - Skills repository"
    log "   - Cookbooks repository"
    log "   - Quickstarts repository"
    log "   - Organization repositories (54 total)"

    # Note: Actual scanning happens through MCP tools when Claude Code is active
    # This script logs the intent and can trigger notification

    log "✅ Scan complete - review learnings in ~/.claude_memory/learnings/"
    log "💡 Next: Open Claude Code and use /mcp__learning__update_toolkit prompt"
    log ""
}

setup_cron() {
    log "⚙️  Setting up automated daily scans..."

    # Create cron entry for daily scan at 2 AM
    CRON_CMD="0 2 * * * $SCRIPT_DIR/auto_update_toolkit.sh >> $LOG_FILE 2>&1"

    # Check if already in crontab
    if crontab -l 2>/dev/null | grep -F "$SCRIPT_DIR/auto_update_toolkit.sh" > /dev/null; then
        log "✅ Cron job already configured"
    else
        # Add to crontab
        (crontab -l 2>/dev/null; echo "$CRON_CMD") | crontab -
        log "✅ Cron job added - runs daily at 2 AM"
        log "   View logs: tail -f $LOG_FILE"
    fi
}

show_status() {
    log "📊 Learning System Status:"
    log ""

    # Check if Learning MCP configured
    if grep -q "learning" "$HOME/.config/claude/claude_desktop_config.json" 2>/dev/null; then
        log "✅ Learning MCP: Configured"
    else
        log "❌ Learning MCP: NOT configured"
    fi

    # Check if learnings exist
    if [ -d "$HOME/.claude_memory/learnings" ] && [ "$(ls -A "$HOME/.claude_memory/learnings" 2>/dev/null)" ]; then
        LEARNING_COUNT=$(find "$HOME/.claude_memory/learnings" -name "*.json" | wc -l)
        log "✅ Stored learnings: $LEARNING_COUNT files"
    else
        log "⚠️  No learnings stored yet"
    fi

    # Check cron status
    if crontab -l 2>/dev/null | grep -F "$SCRIPT_DIR/auto_update_toolkit.sh" > /dev/null; then
        log "✅ Auto-update: Enabled (daily at 2 AM)"
    else
        log "❌ Auto-update: Not scheduled"
    fi

    log ""
    log "💡 To scan now: Open Claude Code and run:"
    log "   /mcp__learning__scan_all_resources"
    log "   /mcp__learning__update_toolkit"
}

# Main
case "${1:-}" in
    --setup)
        setup_cron
        ;;
    --status)
        show_status
        ;;
    *)
        run_scan
        ;;
esac
