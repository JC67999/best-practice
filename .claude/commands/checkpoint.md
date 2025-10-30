---
description: Create git checkpoint before risky operations
---

# Create Checkpoint: $ARGUMENTS

Creating safety checkpoint for: "$ARGUMENTS"

## Step 1: Verify Clean State

```bash
git status
```

**Check for**:
- Uncommitted changes
- Untracked files

**If dirty**:
```bash
git add -A
git commit -m "checkpoint: save current state before $ARGUMENTS"
```

## Step 2: Create Descriptive Checkpoint Tag

```bash
git tag checkpoint-$(date +%Y%m%d-%H%M%S)-$ARGUMENTS
```

**Format**: `checkpoint-YYYYMMDD-HHMMSS-description`

**Example**: `checkpoint-20251030-143022-auth-refactor`

## Step 3: Confirm Checkpoint Created

```bash
git tag -l "checkpoint-*" | tail -5
```

Should show your new checkpoint tag.

## Step 4: Document Rollback Command

Save this command for easy rollback:

```bash
# Rollback command (use if needed):
git reset --hard checkpoint-$(date +%Y%m%d)-$ARGUMENTS
```

Copy this to your terminal history or save to notes.

## Now Work Fearlessly

You can now proceed with risky changes knowing:
- Instant rollback available
- No work will be lost
- Can return to this exact state anytime

## When Done

**If changes successful**:
```bash
# Keep working
git tag -d checkpoint-$(date +%Y%m%d)-$ARGUMENTS  # Delete checkpoint
```

**If changes failed**:
```bash
# Instant rollback
git reset --hard checkpoint-$(date +%Y%m%d)-$ARGUMENTS
git clean -fd  # Remove untracked files
```

## Checkpoint Best Practices

**Create checkpoints before**:
- Large refactoring (>30 lines)
- Experimental features
- Complex bug fixes
- Database migrations
- Dependency upgrades
- Merge operations
- Any risky changes

**Checkpoint frequency**:
- Every risky operation
- Every hour during complex work
- Before each major step in multi-step process
- At end of each work session

## View All Checkpoints

```bash
git tag -l "checkpoint-*"
```

## Delete Old Checkpoints

```bash
# List checkpoints older than 7 days
git tag -l "checkpoint-*" | head -n -7

# Delete old checkpoints
git tag -l "checkpoint-*" | head -n -7 | xargs git tag -d
```

## Automated Checkpointing

For automatic checkpoints before every file write, add to settings.json:

```json
{
  "hooks": {
    "PreToolUse": [
      {
        "matcher": "Write|Edit|MultiEdit",
        "command": "git add -A && git commit -m 'auto-checkpoint: ${tool} on ${file}'"
      }
    ]
  }
}
```

**Benefits**:
- No manual checkpoint management
- Granular undo capability
- Time-travel debugging
- Never lose work

## Emergency Rollback

If things go very wrong:

```bash
# Show recent checkpoints
git tag -l "checkpoint-*" | tail -10

# View what changed since checkpoint
git diff checkpoint-YYYYMMDD-HHMMSS-name

# Rollback to checkpoint
git reset --hard checkpoint-YYYYMMDD-HHMMSS-name

# Clean untracked files
git clean -fd
```

Checkpoint created. Proceed with confidence!
