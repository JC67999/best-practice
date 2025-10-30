---
description: Scaffold new MCP server boilerplate with best practices
---

# Create MCP: $ARGUMENTS

Create MCP server for: "$ARGUMENTS"

## Step 1: MCP Information Gathering

**MCP Name**: $ARGUMENTS (e.g., "database", "analytics", "deployment")

**Purpose**: [What does this MCP do?]

**Tools to expose**: [List of tool names]
1. `mcp__[name]__[tool1]` - [Description]
2. `mcp__[name]__[tool2]` - [Description]
3. `mcp__[name]__[tool3]` - [Description]

**Dependencies**: [Required packages]
- [package1]
- [package2]

**Storage needs**: [Does it need persistent storage?]
- ✅ Yes - [What to store]
- ❌ No - Stateless

## Step 2: Create MCP File Structure

```bash
# Create MCP file
touch mcp-servers/${ARGUMENTS}_mcp.py

# Create test file
touch tests/test_${ARGUMENTS}_mcp.py

# Create MCP documentation
mkdir -p docs/mcp
touch docs/mcp/${ARGUMENTS}_mcp.md
```

## Step 3: Generate MCP Server Boilerplate

**Create**: `mcp-servers/${ARGUMENTS}_mcp.py`

```python
"""
MCP Server: ${ARGUMENTS}
Purpose: [Brief description of what this MCP does]

Tools:
- mcp__${ARGUMENTS}__[tool1] - [Description]
- mcp__${ARGUMENTS}__[tool2] - [Description]
"""

from typing import Dict, List, Optional, Any
import asyncio
import logging
from pathlib import Path

logger = logging.getLogger(__name__)


class ${ARGUMENTS^}MCP:
    """${ARGUMENTS^} MCP server for [purpose]."""

    def __init__(self, config: Optional[Dict] = None):
        """Initialize ${ARGUMENTS} MCP server.

        Args:
            config: Optional configuration dictionary
                - storage_dir: Directory for persistent storage
                - [other config options]
        """
        self.config = config or {}
        self.storage_dir = Path(self.config.get(
            "storage_dir",
            Path.home() / ".claude_memory" / "${ARGUMENTS}"
        ))
        self.storage_dir.mkdir(parents=True, exist_ok=True)

        logger.info(f"${ARGUMENTS^} MCP initialized: {self.storage_dir}")

    async def handle_tool_call(
        self,
        tool_name: str,
        arguments: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Handle MCP tool calls.

        Args:
            tool_name: Name of the tool to execute
            arguments: Tool arguments

        Returns:
            Dictionary with tool results:
                - success: Boolean indicating success/failure
                - data: Tool output data
                - error: Error message if failed
                - message: Human-readable status message
        """
        handlers = {
            "mcp__${ARGUMENTS}__[tool1]": self._handle_[tool1],
            "mcp__${ARGUMENTS}__[tool2]": self._handle_[tool2],
            "mcp__${ARGUMENTS}__[tool3]": self._handle_[tool3],
        }

        handler = handlers.get(tool_name)
        if not handler:
            return {
                "success": False,
                "error": f"Unknown tool: {tool_name}",
                "message": f"Tool '{tool_name}' not found in ${ARGUMENTS} MCP"
            }

        try:
            result = await handler(arguments)
            return result

        except Exception as e:
            logger.exception(f"Error in {tool_name}")
            return {
                "success": False,
                "error": str(e),
                "error_type": type(e).__name__,
                "message": f"Failed to execute {tool_name}: {str(e)}"
            }

    async def _handle_[tool1](self, args: Dict[str, Any]) -> Dict[str, Any]:
        """Handle [tool1] tool.

        Args:
            args: Tool arguments
                - [arg1]: [Description]
                - [arg2]: [Description]

        Returns:
            Dictionary with:
                - success: True if succeeded
                - data: [Result data]
                - message: Status message
        """
        # Validate required arguments
        required = ["[arg1]", "[arg2]"]
        missing = [arg for arg in required if arg not in args]
        if missing:
            return {
                "success": False,
                "error": f"Missing required arguments: {missing}",
                "message": f"Please provide: {', '.join(missing)}"
            }

        # Extract arguments
        arg1 = args["[arg1]"]
        arg2 = args.get("[arg2]", "default_value")

        # Implement tool logic
        try:
            # TODO: Implement tool logic here
            result = self._do_[tool1](arg1, arg2)

            return {
                "success": True,
                "data": result,
                "message": f"[Tool1] completed successfully"
            }

        except ValueError as e:
            logger.error(f"Validation error in [tool1]: {e}")
            return {
                "success": False,
                "error": str(e),
                "error_type": "validation",
                "message": f"Invalid input: {str(e)}"
            }

        except Exception as e:
            logger.exception(f"Unexpected error in [tool1]")
            return {
                "success": False,
                "error": str(e),
                "error_type": "internal",
                "message": f"Internal error: {str(e)}"
            }

    def _do_[tool1](self, arg1: Any, arg2: Any) -> Any:
        """Internal implementation of [tool1].

        Args:
            arg1: [Description]
            arg2: [Description]

        Returns:
            [Return value description]
        """
        # TODO: Implement core logic
        pass

    async def _handle_[tool2](self, args: Dict[str, Any]) -> Dict[str, Any]:
        """Handle [tool2] tool.

        Args:
            args: Tool arguments

        Returns:
            Dictionary with success status and data
        """
        # TODO: Implement tool handler
        return {
            "success": True,
            "data": {},
            "message": "[Tool2] not yet implemented"
        }

    async def _handle_[tool3](self, args: Dict[str, Any]) -> Dict[str, Any]:
        """Handle [tool3] tool.

        Args:
            args: Tool arguments

        Returns:
            Dictionary with success status and data
        """
        # TODO: Implement tool handler
        return {
            "success": True,
            "data": {},
            "message": "[Tool3] not yet implemented"
        }


# MCP Server Entry Point
async def main():
    """Main entry point for MCP server."""
    mcp = ${ARGUMENTS^}MCP()

    # Example usage
    logger.info("${ARGUMENTS^} MCP server started")

    # Test tool calls
    test_args = {
        "[arg1]": "test_value"
    }

    result = await mcp.handle_tool_call(
        "mcp__${ARGUMENTS}__[tool1]",
        test_args
    )

    logger.info(f"Test result: {result}")


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    asyncio.run(main())
```

## Step 4: Generate Test Boilerplate

**Create**: `tests/test_${ARGUMENTS}_mcp.py`

```python
"""
Tests for ${ARGUMENTS^} MCP server.
"""

import pytest
import asyncio
from pathlib import Path
from mcp_servers.${ARGUMENTS}_mcp import ${ARGUMENTS^}MCP


@pytest.fixture
def mcp(tmp_path):
    """Create ${ARGUMENTS} MCP instance with temp storage."""
    config = {
        "storage_dir": str(tmp_path / "${ARGUMENTS}_test")
    }
    return ${ARGUMENTS^}MCP(config=config)


@pytest.fixture
def event_loop():
    """Create event loop for async tests."""
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


class Test${ARGUMENTS^}MCPInitialization:
    """Tests for MCP initialization."""

    def test_initialization_default_config(self, tmp_path):
        """Test MCP initializes with default config."""
        mcp = ${ARGUMENTS^}MCP()
        assert mcp.storage_dir.exists()

    def test_initialization_custom_config(self, tmp_path):
        """Test MCP initializes with custom config."""
        storage_dir = tmp_path / "custom_storage"
        config = {"storage_dir": str(storage_dir)}
        mcp = ${ARGUMENTS^}MCP(config=config)
        assert mcp.storage_dir == storage_dir
        assert storage_dir.exists()


class Test${ARGUMENTS^}MCPTool1:
    """Tests for [tool1] tool."""

    @pytest.mark.asyncio
    async def test_tool1_success(self, mcp):
        """Test [tool1] succeeds with valid input."""
        args = {
            "[arg1]": "test_value",
            "[arg2]": "test_value2"
        }

        result = await mcp.handle_tool_call(
            "mcp__${ARGUMENTS}__[tool1]",
            args
        )

        assert result["success"] is True
        assert "data" in result
        assert "message" in result

    @pytest.mark.asyncio
    async def test_tool1_missing_required_arg(self, mcp):
        """Test [tool1] fails with missing required argument."""
        args = {}  # Missing required args

        result = await mcp.handle_tool_call(
            "mcp__${ARGUMENTS}__[tool1]",
            args
        )

        assert result["success"] is False
        assert "error" in result
        assert "Missing required arguments" in result["error"]

    @pytest.mark.asyncio
    async def test_tool1_invalid_input(self, mcp):
        """Test [tool1] handles invalid input gracefully."""
        args = {
            "[arg1]": None,  # Invalid value
            "[arg2]": "valid"
        }

        result = await mcp.handle_tool_call(
            "mcp__${ARGUMENTS}__[tool1]",
            args
        )

        assert result["success"] is False
        assert result.get("error_type") == "validation"


class Test${ARGUMENTS^}MCPErrorHandling:
    """Tests for error handling."""

    @pytest.mark.asyncio
    async def test_unknown_tool(self, mcp):
        """Test handling of unknown tool name."""
        result = await mcp.handle_tool_call(
            "mcp__${ARGUMENTS}__nonexistent",
            {}
        )

        assert result["success"] is False
        assert "Unknown tool" in result["error"]

    @pytest.mark.asyncio
    async def test_exception_handling(self, mcp):
        """Test MCP handles exceptions gracefully."""
        # TODO: Test exception handling
        # Trigger an exception in tool handler
        # Verify graceful error response
        pass
```

## Step 5: Generate Documentation

**Create**: `docs/mcp/${ARGUMENTS}_mcp.md`

```markdown
# ${ARGUMENTS^} MCP Server

## Overview

**Purpose**: [What this MCP does]

**Use cases**:
- [Use case 1]
- [Use case 2]
- [Use case 3]

## Installation

```bash
# Copy to MCP directory
cp mcp-servers/${ARGUMENTS}_mcp.py ~/.mcp-servers/

# Install dependencies (if any)
pip install [dependencies]

# Restart Claude Code to load MCP
```

## Tools

### mcp__${ARGUMENTS}__[tool1]

**Description**: [What this tool does]

**Arguments**:
- `[arg1]` (required): [Description]
- `[arg2]` (optional): [Description] (default: [default])

**Returns**:
```json
{
  "success": true,
  "data": {
    "[field1]": "[value]",
    "[field2]": "[value]"
  },
  "message": "Success message"
}
```

**Example usage**:
```python
result = await mcp.handle_tool_call(
    "mcp__${ARGUMENTS}__[tool1]",
    {
        "[arg1]": "example_value",
        "[arg2]": "optional_value"
    }
)
```

**When to use**:
- [Use case description]

**Error handling**:
- Missing required args → Returns `success: false` with error details
- Invalid input → Returns `success: false` with validation error
- Internal error → Returns `success: false` with exception details

### mcp__${ARGUMENTS}__[tool2]

[Same structure as tool1]

## Configuration

**Default config**:
```python
{
    "storage_dir": "~/.claude_memory/${ARGUMENTS}",
    # Add other config options
}
```

**Custom config**:
```python
config = {
    "storage_dir": "/custom/path",
    # Custom options
}
mcp = ${ARGUMENTS^}MCP(config=config)
```

## Testing

```bash
# Run tests
pytest tests/test_${ARGUMENTS}_mcp.py -v

# Run with coverage
pytest tests/test_${ARGUMENTS}_mcp.py --cov=mcp_servers.${ARGUMENTS}_mcp --cov-report=term-missing
```

## Examples

### Example 1: [Common use case]

```python
# Example code
```

### Example 2: [Another use case]

```python
# Example code
```

## Troubleshooting

**Issue**: [Common problem]
**Solution**: [How to fix]

**Issue**: [Another problem]
**Solution**: [How to fix]

## API Reference

See code documentation in `mcp-servers/${ARGUMENTS}_mcp.py`
```

## Step 6: Update MCP Requirements

```bash
# If new dependencies needed
echo "[package1]" >> mcp-servers/requirements.txt
echo "[package2]" >> mcp-servers/requirements.txt
```

## Step 7: Run Initial Tests

```bash
# Run the boilerplate tests
pytest tests/test_${ARGUMENTS}_mcp.py -v

# Expected: Tests should pass (or be marked as TODO)
```

## Step 8: Implement Core Logic

**Now implement the TODOs**:
1. Fill in `_do_[tool1]()` implementation
2. Fill in `_handle_[tool2]()` implementation
3. Fill in `_handle_[tool3]()` implementation
4. Update tests to match actual behavior
5. Add edge case tests

**Use TDD**:
1. Write test for feature
2. See it fail
3. Implement feature
4. See test pass
5. Refactor

## Step 9: Integration Testing

```bash
# Test MCP with Claude Code
cp mcp-servers/${ARGUMENTS}_mcp.py ~/.mcp-servers/

# Restart Claude Code

# Test in conversation:
# "Use mcp__${ARGUMENTS}__[tool1] with [arg1]='test'"
```

## Step 10: Documentation Update

Update main MCP README:

```bash
# Add to mcp-servers/README.md
echo "
## ${ARGUMENTS^} MCP

**Purpose**: [Brief description]

**Tools**: [tool1], [tool2], [tool3]

**Installation**: \`cp ${ARGUMENTS}_mcp.py ~/.mcp-servers/\`

**Docs**: See docs/mcp/${ARGUMENTS}_mcp.md
" >> mcp-servers/README.md
```

## Step 11: Quality Gate

```bash
# Run all checks
pytest tests/test_${ARGUMENTS}_mcp.py -v --cov=mcp_servers.${ARGUMENTS}_mcp
ruff check mcp-servers/${ARGUMENTS}_mcp.py
mypy mcp-servers/${ARGUMENTS}_mcp.py
```

**Requirements**:
- [ ] All tests pass
- [ ] Coverage ≥80%
- [ ] No linting errors
- [ ] No type errors
- [ ] Documentation complete

## Step 12: Commit

```bash
git add mcp-servers/${ARGUMENTS}_mcp.py tests/test_${ARGUMENTS}_mcp.py docs/mcp/${ARGUMENTS}_mcp.md
git commit -m "feat: add ${ARGUMENTS} MCP server

- Implements [tool1], [tool2], [tool3]
- Full test coverage ([X%])
- Documentation included

🤖 Generated with [Claude Code](https://claude.com/claude-code)

Co-Authored-By: Claude <noreply@anthropic.com>"
```

## MCP Best Practices

**DO**:
- Return consistent response format (success, data, message, error)
- Validate all inputs before processing
- Handle exceptions gracefully with specific error types
- Log important operations for debugging
- Use async for I/O operations
- Write tests for all tools and edge cases
- Document all tools with examples

**DON'T**:
- Raise exceptions to caller (catch and return error dict)
- Skip input validation
- Return inconsistent response formats
- Forget to handle edge cases
- Skip documentation
- Skip tests

## MCP Naming Conventions

**Tool names**: `mcp__[server]__[action]_[object]`
- Examples:
  - `mcp__database__query_table`
  - `mcp__analytics__compute_metrics`
  - `mcp__deployment__trigger_deploy`

**Response format**:
```python
{
    "success": bool,        # Required
    "data": dict,          # Required (can be empty {})
    "message": str,        # Required (human-readable)
    "error": str,          # Optional (only if success=false)
    "error_type": str      # Optional (validation, internal, etc)
}
```

MCP scaffolded! Implement TODOs and run tests.
