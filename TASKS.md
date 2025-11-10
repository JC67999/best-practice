# Live Task List

**Purpose**: Granular, testable tasks for safe, rapid development
**Updated**: Every change
**Rule**: Each task ≤30 lines of code, fully testable before next task

---

## Current Tasks

### In Progress
- [ ] None

### Pending
- [ ] None

### Completed Today
- [x] Create TASKS.md for live task tracking

---

## Task Rules

### Size Limits
- **Maximum**: 30 lines of code per task
- **Maximum**: 15 minutes per task
- **Required**: Must be testable independently

### Task Breakdown
If task feels too large:
1. STOP - Don't implement
2. Break into ≤30 line sub-tasks
3. Add sub-tasks here
4. Complete each independently

### Workflow
```
1. Read task from TASKS.md
2. Implement (≤30 lines)
3. Test change works
4. Update CHANGELOG.md
5. Run quality gate
6. Commit
7. Mark task complete
8. Move to next task
```

### Validation
- [ ] Task ≤30 lines?
- [ ] Task testable independently?
- [ ] Task described clearly?
- [ ] Success criteria defined?

---

## Example: Good vs Bad Tasks

### ❌ Bad (Too Large)
- "Implement user authentication system"
- "Refactor MCP servers"
- "Add test coverage"

### ✅ Good (Granular)
- "Add function to validate email format (10 lines)"
- "Add docstring to save_session_summary function"
- "Extract project_id logic to separate function (8 lines)"

---

## Daily Pattern

1. **Start**: Review pending tasks
2. **Work**: Complete 1 task at a time
3. **Test**: Verify each task works
4. **Commit**: After each task passes quality gate
5. **Repeat**: Until session ends or tasks complete

---

## Emergency: Task Too Large Mid-Work

If you realize task is too large AFTER starting:

1. **STOP** coding immediately
2. **Commit** what you have (if it works)
3. **Break down** remaining work into smaller tasks
4. **Update** TASKS.md with new tasks
5. **Continue** with first small task
