#!/usr/bin/env python3
"""
Code Quality Guardian MCP Server
Automated quality enforcement and best-practice validation
"""
import asyncio
import json
import os
import subprocess
import re
from typing import Any, Dict, List, Optional

from mcp.server import Server
from mcp.server.stdio import stdio_server
from mcp.types import Tool, TextContent, Prompt, PromptArgument, GetPromptResult, PromptMessage


class QualityServer:
    """Code quality guardian server."""

    def __init__(self):
        self.server = Server("quality-server")
        self.setup_handlers()

    def setup_handlers(self):
        """Setup MCP tool handlers."""

        @self.server.list_tools()
        async def list_tools() -> list[Tool]:
            return [
                Tool(
                    name="check_code_quality",
                    description="Check code quality for specific files",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "file_paths": {
                                "type": "array",
                                "items": {"type": "string"},
                                "description": "List of file paths to check"
                            }
                        },
                        "required": ["file_paths"]
                    }
                ),
                Tool(
                    name="add_missing_docstrings",
                    description="Generate and add docstrings to functions/classes",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "file_paths": {
                                "type": "array",
                                "items": {"type": "string"},
                                "description": "List of file paths"
                            }
                        },
                        "required": ["file_paths"]
                    }
                ),
                Tool(
                    name="find_obsolete_files",
                    description="Detect unused imports, orphaned files, commented code",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "project_path": {
                                "type": "string",
                                "description": "Path to project"
                            }
                        },
                        "required": ["project_path"]
                    }
                ),
                Tool(
                    name="update_documentation",
                    description="Update README.md with new features/changes",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "project_path": {
                                "type": "string",
                                "description": "Path to project"
                            },
                            "changes_description": {
                                "type": "string",
                                "description": "Description of changes"
                            }
                        },
                        "required": ["project_path", "changes_description"]
                    }
                ),
                Tool(
                    name="update_changelog",
                    description="Append entry to CHANGELOG.md",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "project_path": {
                                "type": "string",
                                "description": "Path to project"
                            },
                            "entry": {
                                "type": "string",
                                "description": "Changelog entry"
                            },
                            "version": {
                                "type": "string",
                                "description": "Version number"
                            }
                        },
                        "required": ["project_path", "entry", "version"]
                    }
                ),
                Tool(
                    name="verify_standards",
                    description="Comprehensive standards check",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "project_path": {
                                "type": "string",
                                "description": "Path to project"
                            }
                        },
                        "required": ["project_path"]
                    }
                ),
                Tool(
                    name="run_quality_gate",
                    description="MANDATORY quality gate before task completion",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "project_path": {
                                "type": "string",
                                "description": "Path to project"
                            },
                            "changes_made": {
                                "type": "array",
                                "items": {"type": "string"},
                                "description": "List of changes made"
                            }
                        },
                        "required": ["project_path"]
                    }
                ),
                Tool(
                    name="audit_project_structure",
                    description="Audit project for minimal root compliance",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "project_path": {
                                "type": "string",
                                "description": "Path to project"
                            }
                        },
                        "required": ["project_path"]
                    }
                ),
                Tool(
                    name="validate_file_placement",
                    description="Validate files are in correct locations per best practices",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "project_path": {
                                "type": "string",
                                "description": "Path to project"
                            }
                        },
                        "required": ["project_path"]
                    }
                ),
                Tool(
                    name="validate_autonomous_safety",
                    description="Validate task is safe for autonomous execution",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "project_path": {
                                "type": "string",
                                "description": "Path to project"
                            },
                            "task_description": {
                                "type": "string",
                                "description": "Task description to validate"
                            },
                            "file_changes": {
                                "type": "array",
                                "items": {"type": "string"},
                                "description": "List of files to be modified"
                            }
                        },
                        "required": ["project_path", "task_description", "file_changes"]
                    }
                )
            ]

        @self.server.call_tool()
        async def call_tool(name: str, arguments: Any) -> list[TextContent]:
            try:
                if name == "check_code_quality":
                    result = self.check_code_quality(**arguments)
                elif name == "add_missing_docstrings":
                    result = self.add_missing_docstrings(**arguments)
                elif name == "find_obsolete_files":
                    result = self.find_obsolete_files(**arguments)
                elif name == "update_documentation":
                    result = self.update_documentation(**arguments)
                elif name == "update_changelog":
                    result = self.update_changelog(**arguments)
                elif name == "verify_standards":
                    result = self.verify_standards(**arguments)
                elif name == "run_quality_gate":
                    result = self.run_quality_gate(**arguments)
                elif name == "audit_project_structure":
                    result = self.audit_project_structure(**arguments)
                elif name == "validate_file_placement":
                    result = self.validate_file_placement(**arguments)
                elif name == "validate_autonomous_safety":
                    result = self.validate_autonomous_safety(**arguments)
                else:
                    result = {"error": f"Unknown tool: {name}"}

                return [TextContent(type="text", text=json.dumps(result, indent=2))]
            except Exception as e:
                return [TextContent(type="text", text=json.dumps({"error": str(e)}, indent=2))]

        @self.server.list_prompts()
        async def list_prompts() -> list[Prompt]:
            """List available quality prompts."""
            return [
                Prompt(
                    name="code_review",
                    description="Systematic code review for quality, security, and best practices",
                    arguments=[
                        PromptArgument(
                            name="file_paths",
                            description="Comma-separated list of files to review",
                            required=True
                        ),
                        PromptArgument(
                            name="project_path",
                            description="Absolute path to project directory",
                            required=True
                        )
                    ]
                ),
                Prompt(
                    name="pre_commit_check",
                    description="Run all pre-commit quality checks before committing",
                    arguments=[
                        PromptArgument(
                            name="project_path",
                            description="Absolute path to project directory",
                            required=True
                        ),
                        PromptArgument(
                            name="changed_files",
                            description="Comma-separated list of changed files",
                            required=True
                        )
                    ]
                ),
                Prompt(
                    name="security_audit",
                    description="Security-focused code audit for vulnerabilities",
                    arguments=[
                        PromptArgument(
                            name="project_path",
                            description="Absolute path to project directory",
                            required=True
                        )
                    ]
                )
            ]

        @self.server.get_prompt()
        async def get_prompt(name: str, arguments: dict[str, str] | None) -> GetPromptResult:
            """Get a specific prompt template."""
            if arguments is None:
                arguments = {}

            if name == "code_review":
                file_paths = arguments.get("file_paths", "").split(",")
                project_path = arguments.get("project_path", "")

                prompt_text = f"""You are conducting a systematic code review for files:
{chr(10).join(f"- {fp.strip()}" for fp in file_paths if fp.strip())}

## Code Review Framework

### 1. Automated Quality Checks
First, call these MCP tools to get automated analysis:
- `check_code_quality` with file_paths: {file_paths}
- Review the automated findings before manual review

### 2. Code Quality Review

**For each file, check**:

#### Structure & Organization
- [ ] Clear module/class/function organization
- [ ] Appropriate file size (≤500 lines)
- [ ] Logical grouping of related code
- [ ] No duplicate code

#### Naming & Readability
- [ ] Descriptive variable/function names
- [ ] Consistent naming conventions
- [ ] No magic numbers or strings
- [ ] Clear intent without needing comments

#### Documentation
- [ ] All public functions have docstrings
- [ ] Complex logic has explanatory comments
- [ ] API documentation is accurate
- [ ] Examples provided for non-obvious usage

#### Error Handling
- [ ] All error cases handled
- [ ] No bare except clauses
- [ ] Errors logged appropriately
- [ ] User-friendly error messages

### 3. Security Review

**Check for OWASP Top 10**:
- [ ] No SQL injection vulnerabilities
- [ ] No XSS vulnerabilities
- [ ] No command injection risks
- [ ] Proper input validation
- [ ] Secure authentication/authorization
- [ ] No hardcoded secrets
- [ ] Secure data storage
- [ ] CSRF protection (web apps)

### 4. Performance Review
- [ ] No obvious performance bottlenecks
- [ ] Appropriate data structures used
- [ ] Database queries optimized
- [ ] Caching used where appropriate
- [ ] No N+1 query problems

### 5. Testing
- [ ] Unit tests exist and pass
- [ ] Edge cases tested
- [ ] Error cases tested
- [ ] Test coverage ≥80%

### 6. Best Practices
- [ ] DRY principle followed
- [ ] SOLID principles applied
- [ ] No premature optimization
- [ ] Appropriate design patterns

### Output Format

```markdown
## Code Review: {', '.join(file_paths)}

### Summary
- Files reviewed: {len(file_paths)}
- Overall assessment: [APPROVED / NEEDS WORK / BLOCKED]
- Critical issues: [count]
- Warnings: [count]

### Automated Findings
[Results from check_code_quality tool]

### Manual Review

#### {file_paths[0] if file_paths else "file"}
**Structure**: [assessment]
**Quality**: [assessment]
**Security**: [assessment]
**Performance**: [assessment]

**Issues Found**:
1. [CRITICAL/WARNING/INFO] [description] (line X)
   - Recommendation: [fix]
2. ...

[Repeat for each file...]

### Action Items
- [ ] [action 1]
- [ ] [action 2]

### Approval
- [ ] All critical issues resolved
- [ ] All tests passing
- [ ] Ready to commit
```

**Now begin the code review.**
"""

                return GetPromptResult(
                    description=f"Code review for: {', '.join(file_paths)}",
                    messages=[
                        PromptMessage(
                            role="user",
                            content=TextContent(type="text", text=prompt_text)
                        )
                    ]
                )

            elif name == "pre_commit_check":
                project_path = arguments.get("project_path", "")
                changed_files = arguments.get("changed_files", "").split(",")

                prompt_text = f"""You are running pre-commit quality checks before committing code.

**Project**: {project_path}
**Changed Files** ({len(changed_files)}):
{chr(10).join(f"- {cf.strip()}" for cf in changed_files if cf.strip())}

## Pre-Commit Quality Gate

### Required Checks (All Must Pass)

**Step 1: Run Quality Gate**
Call `run_quality_gate` with:
- project_path: {project_path}
- changes_made: {changed_files}

**Result**: If FAILED, STOP and fix issues before proceeding.

### Step 2: Manual Validation

#### Changelog Updated?
- [ ] CHANGELOG.md has entry for these changes
- [ ] Entry describes WHAT changed and WHY
- [ ] Entry follows format (feat:/fix:/refactor:)

#### Comments Added?
- [ ] New functions have docstrings
- [ ] Complex logic has explanatory comments
- [ ] No TODO comments left behind

#### Tests Added/Updated?
- [ ] New features have tests
- [ ] Bug fixes have regression tests
- [ ] All tests pass locally

#### No Sensitive Data?
- [ ] No API keys or passwords
- [ ] No .env files being committed
- [ ] No credentials in code
- [ ] No debugging code left in

#### Commit Message Ready?
- [ ] Descriptive commit message drafted
- [ ] Follows conventional commits format
- [ ] References issue numbers if applicable

### Step 3: Final Checklist

Before running `git commit`, verify:
- [ ] Quality gate: PASSED
- [ ] Changelog: UPDATED
- [ ] Tests: PASSING
- [ ] Comments: ADDED
- [ ] Secrets: NONE
- [ ] Commit message: READY

### Output Format

```markdown
## Pre-Commit Check Results

### Quality Gate Status
[Result from run_quality_gate]

### Validation Results
- Changelog: [✅/❌]
- Comments: [✅/❌]
- Tests: [✅/❌]
- Secrets: [✅/❌]
- Commit message: [✅/❌]

### Issues Found
1. [issue description]
   - Fix: [recommendation]
2. ...

### Verdict
- [ ] **APPROVED** - Ready to commit
- [ ] **BLOCKED** - Fix issues first

### Next Steps
{f'Fix {len([x for x in []])} issues before committing' if False else 'Run: git commit -m "your message"'}
```

**Run the pre-commit checks now.**
"""

                return GetPromptResult(
                    description="Pre-commit quality checks",
                    messages=[
                        PromptMessage(
                            role="user",
                            content=TextContent(type="text", text=prompt_text)
                        )
                    ]
                )

            elif name == "security_audit":
                project_path = arguments.get("project_path", "")

                prompt_text = f"""You are conducting a security audit for the project at: {project_path}

## Security Audit Framework

### OWASP Top 10 Review

#### 1. Injection Vulnerabilities
**Check for**:
- SQL injection (raw SQL queries)
- Command injection (os.system, subprocess without validation)
- Code injection (eval, exec, compile)
- LDAP injection
- XML injection

**Find with grep**:
```bash
# SQL injection risks
grep -r "execute\|cursor\|raw" --include="*.py" {project_path}

# Command injection risks
grep -r "os.system\|subprocess\|eval\|exec" --include="*.py" {project_path}
```

#### 2. Broken Authentication
**Check for**:
- Weak password requirements
- Missing session timeout
- No account lockout
- Insecure password storage
- Session fixation vulnerabilities

#### 3. Sensitive Data Exposure
**Check for**:
- Hardcoded secrets (API keys, passwords)
- Unencrypted data storage
- Unencrypted data transmission
- Logging sensitive data
- Exposing secrets in error messages

**Find with grep**:
```bash
# Hardcoded secrets
grep -ri "password\s*=\|api_key\s*=\|secret\s*=" --include="*.py" {project_path}
grep -r "os.environ.get" --include="*.py" {project_path}  # Check if properly using env vars
```

#### 4. XML External Entities (XXE)
**Check for**:
- XML parsing without disabling external entities
- Unsafe XML libraries

#### 5. Broken Access Control
**Check for**:
- Missing authorization checks
- IDOR (Insecure Direct Object Reference)
- Path traversal vulnerabilities
- Elevation of privilege

#### 6. Security Misconfiguration
**Check for**:
- Debug mode enabled in production
- Default credentials
- Unnecessary features enabled
- Missing security headers
- Verbose error messages

**Check**:
```python
# Look for DEBUG = True
grep -r "DEBUG\s*=\s*True" --include="*.py" {project_path}
```

#### 7. Cross-Site Scripting (XSS)
**Check for**:
- Unescaped user input in templates
- innerHTML usage
- Unsafe rendering of user data

#### 8. Insecure Deserialization
**Check for**:
- pickle.loads without validation
- eval on user data
- YAML loading without safe_load

```bash
grep -r "pickle.loads\|yaml.load[^_]" --include="*.py" {project_path}
```

#### 9. Using Components with Known Vulnerabilities
**Check**:
- Run dependency audit
- Check requirements.txt for outdated packages

```bash
pip list --outdated
safety check  # If safety is installed
```

#### 10. Insufficient Logging & Monitoring
**Check for**:
- Security events not logged
- Logs not monitored
- No alerting on suspicious activity

### Output Format

```markdown
## Security Audit: {project_path}

### Executive Summary
- Severity: [CRITICAL / HIGH / MEDIUM / LOW]
- Vulnerabilities Found: [count]
- Recommendations: [count]

### Findings by OWASP Category

#### 1. Injection
- Status: [✅ Secure / ⚠️ Warnings / ❌ Vulnerable]
- Issues: [count]
- Details:
  - [file:line] [description]
  - Recommendation: [fix]

[Repeat for all 10 categories...]

### Critical Vulnerabilities
1. **[Type]** in [file:line]
   - Risk: [description]
   - Impact: [what could happen]
   - Fix: [specific recommendation]

### Action Items (Prioritized)
1. [CRITICAL] [action]
2. [HIGH] [action]
3. [MEDIUM] [action]

### Clean Bill of Health
- [ ] No hardcoded secrets
- [ ] All inputs validated
- [ ] Authentication secure
- [ ] Authorization in place
- [ ] Data encrypted
- [ ] Dependencies up to date
- [ ] Logging enabled
- [ ] Error handling secure
```

**Begin the security audit now.**
"""

                return GetPromptResult(
                    description="Security audit",
                    messages=[
                        PromptMessage(
                            role="user",
                            content=TextContent(type="text", text=prompt_text)
                        )
                    ]
                )

            else:
                raise ValueError(f"Unknown prompt: {name}")

    def check_code_quality(self, file_paths: List[str]) -> Dict:
        """Check code quality for specific files."""
        issues = []

        for file_path in file_paths:
            if not os.path.exists(file_path):
                issues.append({
                    "file": file_path,
                    "severity": "error",
                    "issue": "File not found"
                })
                continue

            # Check docstrings
            docstring_issues = self._check_docstrings(file_path)
            issues.extend(docstring_issues)

            # Check naming conventions
            naming_issues = self._check_naming(file_path)
            issues.extend(naming_issues)

            # Check error handling
            error_handling_issues = self._check_error_handling(file_path)
            issues.extend(error_handling_issues)

            # Check complexity (simple heuristic)
            complexity_issues = self._check_complexity(file_path)
            issues.extend(complexity_issues)

        return {
            "total_issues": len(issues),
            "issues": issues,
            "summary": self._summarize_issues(issues)
        }

    def _check_docstrings(self, file_path: str) -> List[Dict]:
        """Check for missing docstrings."""
        issues = []

        try:
            with open(file_path) as f:
                content = f.read()

            # Find functions/classes without docstrings
            lines = content.split('\n')
            for i, line in enumerate(lines):
                # Check for function definitions
                if re.match(r'^\s*def \w+', line) and not line.startswith('    '):
                    # Check if next non-empty line is docstring
                    next_line_idx = i + 1
                    while next_line_idx < len(lines) and not lines[next_line_idx].strip():
                        next_line_idx += 1

                    if next_line_idx < len(lines):
                        next_line = lines[next_line_idx].strip()
                        if not next_line.startswith('"""') and not next_line.startswith("'''"):
                            match = re.search(r'def (\w+)', line)
                            if match:
                                func_name = match.group(1)
                                if not func_name.startswith('_'):  # Public functions only
                                    issues.append({
                                        "file": file_path,
                                        "line": i + 1,
                                        "severity": "warning",
                                        "issue": f"Missing docstring for function '{func_name}'",
                                        "suggestion": "Add Google-style docstring"
                                    })

                # Check for class definitions
                if re.match(r'^\s*class \w+', line):
                    next_line_idx = i + 1
                    while next_line_idx < len(lines) and not lines[next_line_idx].strip():
                        next_line_idx += 1

                    if next_line_idx < len(lines):
                        next_line = lines[next_line_idx].strip()
                        if not next_line.startswith('"""') and not next_line.startswith("'''"):
                            match = re.search(r'class (\w+)', line)
                            if match:
                                class_name = match.group(1)
                                issues.append({
                                    "file": file_path,
                                    "line": i + 1,
                                    "severity": "warning",
                                    "issue": f"Missing docstring for class '{class_name}'",
                                    "suggestion": "Add Google-style docstring"
                                })

        except Exception as e:
            issues.append({
                "file": file_path,
                "severity": "error",
                "issue": f"Error checking docstrings: {str(e)}"
            })

        return issues

    def _check_naming(self, file_path: str) -> List[Dict]:
        """Check naming conventions."""
        issues = []

        try:
            with open(file_path) as f:
                content = f.read()

            lines = content.split('\n')
            for i, line in enumerate(lines):
                # Check for camelCase in function names (should be snake_case)
                if re.search(r'def [a-z]+[A-Z]', line):
                    issues.append({
                        "file": file_path,
                        "line": i + 1,
                        "severity": "info",
                        "issue": "Function name appears to use camelCase",
                        "suggestion": "Use snake_case for function names"
                    })

        except Exception:
            pass

        return issues

    def _check_error_handling(self, file_path: str) -> List[Dict]:
        """Check for proper error handling."""
        issues = []

        try:
            with open(file_path) as f:
                content = f.read()

            # Check for bare except clauses
            if re.search(r'except\s*:', content):
                issues.append({
                    "file": file_path,
                    "severity": "warning",
                    "issue": "Found bare 'except:' clause",
                    "suggestion": "Specify exception types or use 'except Exception as e:'"
                })

        except Exception:
            pass

        return issues

    def _check_complexity(self, file_path: str) -> List[Dict]:
        """Check function complexity (simple heuristic)."""
        issues = []

        try:
            with open(file_path) as f:
                content = f.read()

            lines = content.split('\n')
            in_function = False
            func_name = ""
            func_start = 0
            func_lines = 0

            for i, line in enumerate(lines):
                if re.match(r'^\s*def \w+', line):
                    # Start of function
                    match = re.search(r'def (\w+)', line)
                    if match:
                        in_function = True
                        func_name = match.group(1)
                        func_start = i + 1
                        func_lines = 0
                elif in_function:
                    # Check if function ended
                    if line and not line[0].isspace() and line.strip():
                        # Function ended
                        if func_lines > 30:
                            issues.append({
                                "file": file_path,
                                "line": func_start,
                                "severity": "warning",
                                "issue": f"Function '{func_name}' is {func_lines} lines (max: 30)",
                                "suggestion": "Break into smaller functions"
                            })
                        in_function = False
                    else:
                        func_lines += 1

        except Exception:
            pass

        return issues

    def _summarize_issues(self, issues: List[Dict]) -> Dict:
        """Summarize issues by severity."""
        summary = {"error": 0, "warning": 0, "info": 0}
        for issue in issues:
            severity = issue.get("severity", "info")
            summary[severity] = summary.get(severity, 0) + 1
        return summary

    def add_missing_docstrings(self, file_paths: List[str]) -> Dict:
        """Generate and add docstrings (placeholder - would use AI in real implementation)."""
        modified_files = []

        for file_path in file_paths:
            # In real implementation, would use AI to generate appropriate docstrings
            # For now, just identify where they're needed
            docstring_issues = self._check_docstrings(file_path)

            if docstring_issues:
                modified_files.append({
                    "file": file_path,
                    "locations": [issue["line"] for issue in docstring_issues]
                })

        return {
            "success": True,
            "message": "In real implementation, would generate docstrings using AI",
            "files_needing_docstrings": modified_files,
            "suggestion": "Use Claude Code to generate appropriate docstrings for each function/class"
        }

    def find_obsolete_files(self, project_path: str) -> Dict:
        """Find obsolete files and code."""
        obsolete_items: Dict[str, list] = {
            "unused_imports": [],
            "orphaned_files": [],
            "commented_code": [],
            "old_versions": []
        }

        # Find Python files
        py_files = self._find_python_files(project_path)

        for py_file in py_files:
            try:
                with open(py_file) as f:
                    content = f.read()

                # Check for large commented blocks
                commented_lines = [line for line in content.split('\n') if line.strip().startswith('#')]
                if len(commented_lines) > 10:
                    obsolete_items["commented_code"].append({
                        "file": py_file,
                        "commented_lines": len(commented_lines),
                        "recommendation": "Remove or move to .archive/"
                    })

                # Check for files with "old", "deprecated", "backup" in name
                file_name = os.path.basename(py_file).lower()
                if any(x in file_name for x in ['old', 'deprecated', 'backup', 'tmp', 'temp']):
                    obsolete_items["old_versions"].append({
                        "file": py_file,
                        "recommendation": "Move to artifacts/.archive/ or delete"
                    })

            except Exception:
                pass

        return {
            "total_obsolete_items": sum(len(v) for v in obsolete_items.values()),
            "obsolete_items": obsolete_items,
            "recommendation": "Clean up to maintain code hygiene"
        }

    def _find_python_files(self, path: str) -> List[str]:
        """Find all Python files in project."""
        py_files = []
        for root, dirs, files in os.walk(path):
            # Skip venv, __pycache__, etc.
            dirs[:] = [d for d in dirs if d not in ['venv', '__pycache__', '.git', 'node_modules']]
            py_files.extend([os.path.join(root, f) for f in files if f.endswith('.py')])
        return py_files

    def update_documentation(self, project_path: str, changes_description: str) -> Dict:
        """Update README.md with changes."""
        readme_path = os.path.join(project_path, "README.md")

        if not os.path.exists(readme_path):
            return {
                "success": False,
                "error": "README.md not found",
                "suggestion": "Create README.md first"
            }

        # In real implementation, would intelligently update README
        return {
            "success": True,
            "message": "In real implementation, would update README.md",
            "changes": changes_description,
            "suggestion": "Use Claude Code to update README.md with changes"
        }

    def update_changelog(self, project_path: str, entry: str, version: str) -> Dict:
        """Update CHANGELOG.md."""
        changelog_path = os.path.join(project_path, "CHANGELOG.md")

        # Create if doesn't exist
        if not os.path.exists(changelog_path):
            with open(changelog_path, 'w') as f:
                f.write("# Changelog\n\nAll notable changes to this project will be documented in this file.\n\n")

        # Append entry
        timestamp = subprocess.run(
            ['date', '+%Y-%m-%d'],
            capture_output=True,
            text=True
        ).stdout.strip()

        entry_text = f"\n## [{version}] - {timestamp}\n\n{entry}\n"

        with open(changelog_path, 'a') as f:
            f.write(entry_text)

        return {
            "success": True,
            "message": f"Added entry for version {version}",
            "changelog_path": changelog_path
        }

    def verify_standards(self, project_path: str) -> Dict:
        """Comprehensive standards verification."""
        results = {
            "structure": self.audit_project_structure(project_path),
            "file_placement": self.validate_file_placement(project_path),
            "code_quality": {"message": "Run check_code_quality for specific files"},
            "obsolete_files": self.find_obsolete_files(project_path)
        }

        # Calculate overall score
        structure_score = 100 - (len(results["structure"].get("violations", [])) * 10)
        placement_score = 100 - (len(results["file_placement"].get("violations", [])) * 10)

        overall_score = (structure_score + placement_score) / 2

        return {
            "overall_score": max(0, overall_score),
            "results": results,
            "passed": overall_score >= 80
        }

    def run_quality_gate(self, project_path: str, changes_made: Optional[List[str]] = None) -> Dict:
        """Run MANDATORY quality gate."""
        # Check if quality script exists
        quality_script = os.path.join(project_path, ".ai-validation/check_quality.sh")

        if not os.path.exists(quality_script):
            return {
                "status": "FAIL",
                "error": "Quality script not found",
                "message": "Run setup to install quality tools",
                "blocked": True
            }

        # Run quality script
        try:
            result = subprocess.run(
                ["bash", quality_script],
                cwd=project_path,
                capture_output=True,
                text=True,
                timeout=300
            )

            # Parse results
            passed = result.returncode == 0

            # Additional checks
            structure_audit = self.audit_project_structure(project_path)
            structure_violations = structure_audit.get("violations", [])

            placement_check = self.validate_file_placement(project_path)
            placement_violations = placement_check.get("violations", [])

            all_passed = passed and len(structure_violations) == 0 and len(placement_violations) == 0

            return {
                "status": "PASS" if all_passed else "FAIL",
                "quality_script_output": result.stdout,
                "quality_script_passed": passed,
                "structure_violations": structure_violations,
                "placement_violations": placement_violations,
                "blocked": not all_passed,
                "message": "All checks passed" if all_passed else "Issues must be fixed before proceeding"
            }

        except subprocess.TimeoutExpired:
            return {
                "status": "FAIL",
                "error": "Quality checks timed out",
                "blocked": True
            }
        except Exception as e:
            return {
                "status": "FAIL",
                "error": str(e),
                "blocked": True
            }

    def audit_project_structure(self, project_path: str) -> Dict:
        """Audit project structure for minimal root compliance."""
        violations = []

        try:
            root_items = os.listdir(project_path)

            # Count visible folders
            visible_folders = [
                f for f in root_items
                if os.path.isdir(os.path.join(project_path, f))
                and not f.startswith('.')
                and f not in ['venv', 'node_modules']
            ]

            if len(visible_folders) > 5:
                violations.append({
                    "severity": "warning",
                    "issue": f"Too many root folders: {len(visible_folders)} (target: 4-5)",
                    "folders": visible_folders
                })

            # Check for forbidden folders
            forbidden = ["logs", "temp", "tmp", "scripts", "import", "export", "output", "input", "config"]
            for folder in forbidden:
                if folder in visible_folders:
                    violations.append({
                        "severity": "error",
                        "issue": f"Forbidden root folder: {folder}/",
                        "suggestion": f"Move to artifacts/{folder}/"
                    })

            # Check for required folders
            required = ["src", "tests", "docs", "artifacts"]
            for folder in required:
                if folder not in root_items:
                    violations.append({
                        "severity": "warning",
                        "issue": f"Missing recommended folder: {folder}/",
                        "suggestion": f"Create {folder}/ directory"
                    })

        except Exception as e:
            violations.append({
                "severity": "error",
                "issue": f"Error auditing structure: {str(e)}"
            })

        return {
            "compliant": len(violations) == 0,
            "violations": violations,
            "structure_score": max(0, 100 - (len(violations) * 15))
        }

    def validate_file_placement(self, project_path: str) -> Dict:
        """Validate file placement per best practices."""
        violations = []

        try:
            # Check for Python files in root
            root_py_files = [
                f for f in os.listdir(project_path)
                if f.endswith('.py')
                and f not in ['setup.py', 'manage.py']
            ]

            for py_file in root_py_files:
                violations.append({
                    "severity": "warning",
                    "file": py_file,
                    "issue": "Python file in root directory",
                    "suggestion": "Move to src/ or artifacts/temp/"
                })

            # Check for log files in root
            root_log_files = [f for f in os.listdir(project_path) if f.endswith('.log')]
            for log_file in root_log_files:
                violations.append({
                    "severity": "warning",
                    "file": log_file,
                    "issue": "Log file in root directory",
                    "suggestion": "Move to artifacts/logs/"
                })

        except Exception as e:
            violations.append({
                "severity": "error",
                "issue": f"Error validating file placement: {str(e)}"
            })

        return {
            "compliant": len(violations) == 0,
            "violations": violations,
            "placement_score": max(0, 100 - (len(violations) * 20))
        }

    def validate_autonomous_safety(
        self,
        project_path: str,
        task_description: str,
        file_changes: List[str]
    ) -> Dict:
        """Validate task is safe for autonomous execution.

        Checks task against safety constraints from docs/autonomous-constraints.md.
        Blocks forbidden operations like file deletions, config changes, and
        dangerous database operations.

        Returns dict with safety status and any violations found.
        """
        violations = []

        # Forbidden file patterns (from docs/autonomous-constraints.md)
        forbidden_patterns = [
            (r'\.env', "Modifying .env file"),
            (r'docker-compose\.yml', "Modifying Docker config"),
            (r'Dockerfile', "Modifying Docker config"),
            (r'\.github/workflows', "Modifying CI/CD"),
            (r'requirements\.txt', "Adding dependencies"),
            (r'package\.json', "Adding dependencies"),
            (r'\.gitignore', "Modifying git ignore"),
        ]

        # Check file changes for forbidden patterns
        for pattern, reason in forbidden_patterns:
            for file_path in file_changes:
                if re.search(pattern, file_path):
                    violations.append({
                        "severity": "CRITICAL",
                        "violation": reason,
                        "file": file_path,
                        "blocked": True
                    })

        # Forbidden code patterns in task description
        forbidden_words = [
            "delete file", "remove file", "drop table", "truncate",
            "remove column", "add dependency", "install package",
            "stripe", "payment", "deploy", "push to remote"
        ]

        task_lower = task_description.lower()
        for word in forbidden_words:
            if word in task_lower:
                violations.append({
                    "severity": "HIGH",
                    "violation": f"Task mentions forbidden operation: {word}",
                    "blocked": True
                })

        # Validate file paths in approved directories
        approved_dirs = ["src/", "tests/", "docs/", "mcp-servers/"]
        for file_path in file_changes:
            # Check if file is in approved directory
            if not any(file_path.startswith(d) for d in approved_dirs):
                violations.append({
                    "severity": "HIGH",
                    "violation": f"File outside approved directories: {file_path}",
                    "blocked": True
                })

        return {
            "safe_for_autonomous": len(violations) == 0,
            "violations": violations,
            "can_proceed": len([v for v in violations if v.get("blocked", False)]) == 0
        }

    async def run(self):
        """Run the MCP server."""
        async with stdio_server() as (read_stream, write_stream):
            await self.server.run(
                read_stream,
                write_stream,
                self.server.create_initialization_options()
            )


async def main():
    """Main entry point."""
    server = QualityServer()
    await server.run()


if __name__ == "__main__":
    asyncio.run(main())
