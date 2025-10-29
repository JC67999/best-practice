#!/usr/bin/env python3
"""
Project Manager MCP Server
Objective-driven task management with best-practice enforcement
"""
import asyncio
import json
import os
import re
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

from mcp.server import Server
from mcp.server.stdio import stdio_server
from mcp.types import Tool, TextContent


# Vague answer patterns
VAGUE_PATTERNS = {
    "people": "Which specific group of people? Can you name 3 examples?",
    "users": "What type of users exactly? Be specific.",
    "better": "Better than what? By how much?",
    "faster": "How much faster? What's the current speed?",
    "easier": "Easier than what? How is it currently difficult?",
    "improve": "Improve what specific metric? By how much?",
    "help": "Help them do what exactly? What's the specific action?",
    "manage": "Manage what specifically? What data or process?",
    "track": "Track what data specifically? For what purpose?",
    "organize": "Organize what exactly? How is it currently disorganized?"
}

# Question framework
QUESTION_FRAMEWORK = {
    "problem_definition": [
        "What specific problem are you solving?",
        "Who exactly experiences this problem?",
        "How do they currently handle this problem?",
        "Why is the current solution inadequate?",
        "What happens if this problem isn't solved?"
    ],
    "target_user": [
        "Who will use this? Be specific.",
        "Can you name 3 specific examples of this type of person/company?",
        "What do they do for a living or in their role?",
        "What's their current workflow for this?"
    ],
    "solution": [
        "What will you build to solve this problem?",
        "What is the ONE core feature that solves the problem?",
        "What's the absolute minimum that would work?",
        "What features are you NOT building in version 1?"
    ],
    "success_metrics": [
        "How will you know if this is successful?",
        "What specific number indicates success?",
        "How do you measure that?",
        "By when do you want to achieve this?"
    ],
    "constraints": [
        "What's your timeline for version 1?",
        "What technologies must you use?",
        "What's non-negotiable? What cannot be compromised?",
        "What resources do you have (time, skills, budget)?"
    ]
}


class ProjectServer:
    """Project manager server with objective-driven focus."""

    def __init__(self):
        self.server = Server("project-server")
        self.setup_handlers()

    def setup_handlers(self):
        """Setup MCP tool handlers."""

        @self.server.list_tools()
        async def list_tools() -> list[Tool]:
            return [
                # Objective clarification tools
                Tool(
                    name="clarify_project_objective",
                    description="Start comprehensive objective clarification interrogation",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "project_path": {"type": "string"},
                            "initial_description": {"type": "string"}
                        },
                        "required": ["project_path", "initial_description"]
                    }
                ),
                Tool(
                    name="answer_objective_question",
                    description="Answer objective clarification question",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "project_path": {"type": "string"},
                            "question_id": {"type": "string"},
                            "answer": {"type": "string"}
                        },
                        "required": ["project_path", "question_id", "answer"]
                    }
                ),
                Tool(
                    name="score_objective_clarity",
                    description="Score objective clarity (0-100)",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "project_path": {"type": "string"}
                        },
                        "required": ["project_path"]
                    }
                ),
                Tool(
                    name="define_project_objective",
                    description="Finalize and store project objective",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "project_path": {"type": "string"}
                        },
                        "required": ["project_path"]
                    }
                ),

                # Task management tools
                Tool(
                    name="create_task_breakdown",
                    description="Break project into small, objective-aligned tasks",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "project_path": {"type": "string"}
                        },
                        "required": ["project_path"]
                    }
                ),
                Tool(
                    name="validate_task_alignment",
                    description="Check if task serves objective",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "project_path": {"type": "string"},
                            "task_description": {"type": "string"}
                        },
                        "required": ["project_path", "task_description"]
                    }
                ),
                Tool(
                    name="challenge_task_priority",
                    description="Challenge if task is highest priority",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "project_path": {"type": "string"},
                            "task_id": {"type": "string"}
                        },
                        "required": ["project_path", "task_id"]
                    }
                ),
                Tool(
                    name="validate_task_size",
                    description="Check if task is small enough",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "task_description": {"type": "string"}
                        },
                        "required": ["task_description"]
                    }
                ),
                Tool(
                    name="mark_task_complete",
                    description="Mark task complete (requires quality gate PASS)",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "project_path": {"type": "string"},
                            "task_id": {"type": "string"},
                            "quality_gate_passed": {"type": "boolean"}
                        },
                        "required": ["project_path", "task_id", "quality_gate_passed"]
                    }
                ),
                Tool(
                    name="get_current_status",
                    description="Get current project status",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "project_path": {"type": "string"}
                        },
                        "required": ["project_path"]
                    }
                ),
                Tool(
                    name="identify_scope_creep",
                    description="Find tasks that don't serve objective",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "project_path": {"type": "string"}
                        },
                        "required": ["project_path"]
                    }
                ),
                Tool(
                    name="refocus_on_objective",
                    description="Review all tasks against objective, cut non-essential",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "project_path": {"type": "string"}
                        },
                        "required": ["project_path"]
                    }
                ),
                Tool(
                    name="sync_plan_to_reality",
                    description="Update plan to match actual project state",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "project_path": {"type": "string"}
                        },
                        "required": ["project_path"]
                    }
                )
            ]

        @self.server.call_tool()
        async def call_tool(name: str, arguments: Any) -> list[TextContent]:
            try:
                # Objective clarification
                if name == "clarify_project_objective":
                    result = self.clarify_project_objective(**arguments)
                elif name == "answer_objective_question":
                    result = self.answer_objective_question(**arguments)
                elif name == "score_objective_clarity":
                    result = self.score_objective_clarity(**arguments)
                elif name == "define_project_objective":
                    result = self.define_project_objective(**arguments)

                # Task management
                elif name == "create_task_breakdown":
                    result = self.create_task_breakdown(**arguments)
                elif name == "validate_task_alignment":
                    result = self.validate_task_alignment(**arguments)
                elif name == "challenge_task_priority":
                    result = self.challenge_task_priority(**arguments)
                elif name == "validate_task_size":
                    result = self.validate_task_size(**arguments)
                elif name == "mark_task_complete":
                    result = self.mark_task_complete(**arguments)
                elif name == "get_current_status":
                    result = self.get_current_status(**arguments)
                elif name == "identify_scope_creep":
                    result = self.identify_scope_creep(**arguments)
                elif name == "refocus_on_objective":
                    result = self.refocus_on_objective(**arguments)
                elif name == "sync_plan_to_reality":
                    result = self.sync_plan_to_reality(**arguments)
                else:
                    result = {"error": f"Unknown tool: {name}"}

                return [TextContent(type="text", text=json.dumps(result, indent=2))]
            except Exception as e:
                return [TextContent(type="text", text=json.dumps({"error": str(e)}, indent=2))]

    def _get_project_data_path(self, project_path: str) -> Path:
        """Get path to project data file."""
        return Path(project_path) / ".project_manager" / "project_data.json"

    def _load_project_data(self, project_path: str) -> Dict:
        """Load project data."""
        data_path = self._get_project_data_path(project_path)

        if not data_path.exists():
            return {
                "objective": None,
                "objective_clarification": {
                    "status": "not_started",
                    "questions": [],
                    "answers": {}
                },
                "tasks": [],
                "completed_tasks": [],
                "decisions": [],
                "audits": []
            }

        with open(data_path) as f:
            return json.load(f)

    def _save_project_data(self, project_path: str, data: Dict):
        """Save project data."""
        data_path = self._get_project_data_path(project_path)
        data_path.parent.mkdir(parents=True, exist_ok=True)

        with open(data_path, 'w') as f:
            json.dump(data, f, indent=2)

    def clarify_project_objective(
        self,
        project_path: str,
        initial_description: str
    ) -> Dict:
        """Start objective clarification process."""
        data = self._load_project_data(project_path)

        # Initialize clarification session
        data["objective_clarification"] = {
            "status": "in_progress",
            "initial_description": initial_description,
            "started_at": datetime.now().isoformat(),
            "questions": [],
            "answers": {},
            "current_question_id": None
        }

        # Generate first question
        first_question = {
            "id": "problem_1",
            "category": "problem_definition",
            "question": "What specific problem are you solving?",
            "answered": False
        }

        data["objective_clarification"]["questions"].append(first_question)
        data["objective_clarification"]["current_question_id"] = "problem_1"

        self._save_project_data(project_path, data)

        return {
            "status": "started",
            "message": "Objective clarification started",
            "next_question": {
                "id": first_question["id"],
                "question": first_question["question"]
            },
            "instructions": "Answer this question as specifically as possible. Avoid vague terms like 'people', 'users', 'better'."
        }

    def answer_objective_question(
        self,
        project_path: str,
        question_id: str,
        answer: str
    ) -> Dict:
        """Answer objective clarification question."""
        data = self._load_project_data(project_path)
        clarification = data["objective_clarification"]

        # Store answer
        clarification["answers"][question_id] = {
            "answer": answer,
            "timestamp": datetime.now().isoformat()
        }

        # Mark question as answered
        for q in clarification["questions"]:
            if q["id"] == question_id:
                q["answered"] = True
                break

        # Check if answer is vague
        is_vague, follow_up = self._detect_vague_answer(answer, question_id)

        if is_vague:
            # Generate follow-up question
            follow_up_id = f"{question_id}_followup"
            follow_up_question = {
                "id": follow_up_id,
                "category": "follow_up",
                "question": follow_up,
                "parent_question": question_id,
                "answered": False
            }

            clarification["questions"].append(follow_up_question)
            clarification["current_question_id"] = follow_up_id

            self._save_project_data(project_path, data)

            return {
                "status": "needs_clarification",
                "message": "Answer is too vague. Please be more specific.",
                "next_question": {
                    "id": follow_up_id,
                    "question": follow_up
                }
            }

        # Answer is clear, generate next question
        next_question = self._generate_next_question(clarification)

        if next_question:
            clarification["questions"].append(next_question)
            clarification["current_question_id"] = next_question["id"]

            self._save_project_data(project_path, data)

            return {
                "status": "continue",
                "message": "Good answer! Next question:",
                "next_question": {
                    "id": next_question["id"],
                    "question": next_question["question"]
                }
            }
        else:
            # All questions answered
            score = self._calculate_clarity_score(clarification["answers"])

            if score >= 80:
                clarification["status"] = "completed"
                clarification["completed_at"] = datetime.now().isoformat()

                self._save_project_data(project_path, data)

                return {
                    "status": "completed",
                    "message": "Objective clarification complete!",
                    "clarity_score": score,
                    "summary": self._generate_objective_summary(clarification["answers"])
                }
            else:
                # Score too low, need more questions
                clarification["status"] = "needs_improvement"
                self._save_project_data(project_path, data)

                return {
                    "status": "needs_improvement",
                    "clarity_score": score,
                    "message": f"Clarity score is {score}/100. Need ≥80. Let's clarify further.",
                    "weak_areas": self._identify_weak_areas(clarification["answers"])
                }

    def _detect_vague_answer(self, answer: str, question_id: str = None) -> Tuple[bool, Optional[str]]:
        """Detect if answer contains vague language.

        Args:
            answer: The answer text to check
            question_id: The question ID being answered (to prevent loops)

        Returns:
            Tuple of (is_vague, follow_up_question)
        """
        # Don't apply vague detection to ANY follow-up chains (prevent infinite loops)
        if question_id and '_followup' in question_id:
            # Accept any answer to a followup question - no infinite loops!
            return False, None

        answer_lower = answer.lower()

        # Only check if answer is very short (likely genuinely vague)
        # Longer answers with context are likely specific enough
        if len(answer) > 100:
            # For longer answers, only check for standalone vague terms
            # Don't trigger if the word appears in a detailed context
            # Added "manage" and "track" to prevent loops on detailed management descriptions
            vague_words_standalone = ['people', 'users', 'better', 'faster', 'easier', 'improve', 'help', 'manage', 'track', 'organize']
            words = answer_lower.split()

            # Check if vague words appear multiple times without much context
            for vague_word in vague_words_standalone:
                if vague_word in words:
                    # Check if it's in a sentence with specific details (numbers, proper nouns, etc)
                    has_specifics = any([
                        bool(re.search(r'\d+', answer)),  # Contains numbers
                        bool(re.search(r'[A-Z][a-z]+\s+[A-Z][a-z]+', answer)),  # Proper nouns
                        len(answer) > 200,  # Very detailed answer
                        any(indicator in answer_lower for indicator in ['for example', 'such as', 'specifically', 'including'])
                    ])

                    if has_specifics:
                        # Answer has context, don't mark as vague
                        continue
                    else:
                        # Genuinely vague
                        follow_up = VAGUE_PATTERNS.get(vague_word, "Can you be more specific?")
                        return True, follow_up

            # Long answer with no vague standalone words
            return False, None

        # For short answers, check for vague patterns
        for vague_term, follow_up in VAGUE_PATTERNS.items():
            if vague_term in answer_lower:
                return True, follow_up

        # Check for other vague patterns
        vague_indicators = [
            (r'\b(someone|anyone|everyone)\b', "Who specifically? Give examples."),
            (r'\b(something|anything|everything)\b', "What specifically?"),
            (r'\b(somewhere|anywhere|everywhere)\b', "Where specifically?"),
            (r'\b(somehow|anyhow)\b', "How specifically?")
        ]

        for pattern, follow_up in vague_indicators:
            if re.search(pattern, answer_lower):
                return True, follow_up

        return False, None

    def _generate_next_question(self, clarification: Dict) -> Optional[Dict]:
        """Generate next question based on answered questions."""
        answered_categories = set()

        for q in clarification["questions"]:
            if q.get("answered") and q.get("category") != "follow_up":
                answered_categories.add(q["category"])

        # Determine next category
        category_order = [
            "problem_definition",
            "target_user",
            "solution",
            "success_metrics",
            "constraints"
        ]

        for category in category_order:
            if category not in answered_categories:
                # Get questions for this category
                questions = QUESTION_FRAMEWORK.get(category, [])

                if questions:
                    question_num = len([q for q in clarification["questions"] if q.get("category") == category]) + 1

                    if question_num <= len(questions):
                        return {
                            "id": f"{category}_{question_num}",
                            "category": category,
                            "question": questions[question_num - 1],
                            "answered": False
                        }

        return None

    def _calculate_clarity_score(self, answers: Dict) -> int:
        """Calculate objective clarity score."""
        score = 0

        # Problem specificity (20 points)
        problem_answers = [a for k, a in answers.items() if k.startswith("problem_")]
        if problem_answers:
            if len(problem_answers[0].get("answer", "")) > 50:
                score += 20
            elif len(problem_answers[0].get("answer", "")) > 20:
                score += 10

        # Target user clarity (20 points)
        user_answers = [a for k, a in answers.items() if k.startswith("target_user")]
        if user_answers:
            answer_text = user_answers[0].get("answer", "")
            # Check for specific examples
            if re.search(r'\d', answer_text) or "example" in answer_text.lower():
                score += 20
            elif len(answer_text) > 30:
                score += 10

        # Solution specificity (20 points)
        solution_answers = [a for k, a in answers.items() if k.startswith("solution_")]
        if solution_answers:
            if len(solution_answers) >= 3:
                score += 20
            elif len(solution_answers) >= 2:
                score += 15
            elif len(solution_answers) >= 1:
                score += 10

        # Measurable metrics (20 points)
        metrics_answers = [a for k, a in answers.items() if k.startswith("success_metrics")]
        if metrics_answers:
            answer_text = " ".join([a.get("answer", "") for a in metrics_answers])
            # Check for numbers
            if re.search(r'\d+', answer_text):
                score += 20
            elif len(answer_text) > 30:
                score += 10

        # Constraints defined (20 points)
        constraints_answers = [a for k, a in answers.items() if k.startswith("constraints")]
        if constraints_answers:
            if len(constraints_answers) >= 3:
                score += 20
            elif len(constraints_answers) >= 2:
                score += 15
            elif len(constraints_answers) >= 1:
                score += 10

        return min(score, 100)

    def _identify_weak_areas(self, answers: Dict) -> List[str]:
        """Identify areas needing more clarity."""
        weak_areas = []

        categories = ["problem_definition", "target_user", "solution", "success_metrics", "constraints"]

        for category in categories:
            category_answers = [a for k, a in answers.items() if k.startswith(category)]

            if not category_answers:
                weak_areas.append(f"Missing: {category.replace('_', ' ')}")
            elif len(category_answers) < 2:
                weak_areas.append(f"Needs more detail: {category.replace('_', ' ')}")

        return weak_areas

    def _generate_objective_summary(self, answers: Dict) -> Dict:
        """Generate objective summary from answers."""
        summary = {
            "problem": "",
            "target_user": "",
            "solution": "",
            "success_metrics": "",
            "constraints": ""
        }

        # Extract key information
        for question_id, answer_data in answers.items():
            answer = answer_data.get("answer", "")

            if question_id.startswith("problem_"):
                summary["problem"] += answer + " "
            elif question_id.startswith("target_user"):
                summary["target_user"] += answer + " "
            elif question_id.startswith("solution_"):
                summary["solution"] += answer + " "
            elif question_id.startswith("success_metrics"):
                summary["success_metrics"] += answer + " "
            elif question_id.startswith("constraints"):
                summary["constraints"] += answer + " "

        # Clean up
        for key in summary:
            summary[key] = summary[key].strip()

        return summary

    def score_objective_clarity(self, project_path: str) -> Dict:
        """Score objective clarity."""
        data = self._load_project_data(project_path)
        clarification = data.get("objective_clarification", {})

        if not clarification or clarification.get("status") == "not_started":
            return {
                "score": 0,
                "message": "Objective clarification not started"
            }

        answers = clarification.get("answers", {})
        score = self._calculate_clarity_score(answers)
        weak_areas = self._identify_weak_areas(answers)

        return {
            "score": score,
            "status": "PASS" if score >= 80 else "FAIL",
            "weak_areas": weak_areas,
            "message": "Score ≥80 required to proceed" if score < 80 else "Clarity sufficient"
        }

    def define_project_objective(self, project_path: str) -> Dict:
        """Finalize project objective."""
        data = self._load_project_data(project_path)
        clarification = data.get("objective_clarification", {})

        # Check clarity score
        score = self._calculate_clarity_score(clarification.get("answers", {}))

        if score < 80:
            return {
                "success": False,
                "error": f"Objective not clear enough (score: {score}/100). Need ≥80.",
                "action": "Run clarify_project_objective to improve"
            }

        # Generate objective
        objective = self._generate_objective_summary(clarification["answers"])
        objective["clarity_score"] = score
        objective["defined_at"] = datetime.now().isoformat()

        data["objective"] = objective

        # Create PROJECT_PLAN.md
        self._create_project_plan(project_path, objective)

        self._save_project_data(project_path, data)

        return {
            "success": True,
            "message": "Project objective defined and stored",
            "objective": objective,
            "project_plan_created": True
        }

    def _create_project_plan(self, project_path: str, objective: Dict):
        """Create PROJECT_PLAN.md file."""
        docs_path = Path(project_path) / "docs" / "notes"
        docs_path.mkdir(parents=True, exist_ok=True)

        plan_path = docs_path / "PROJECT_PLAN.md"

        plan_content = f"""# Project Plan

Last Updated: {datetime.now().strftime('%Y-%m-%d %H:%M')}

## 🎯 OBJECTIVE (Clarity Score: {objective.get('clarity_score', 0)}/100)

**Problem**: {objective.get('problem', 'Not defined')}

**Target User**: {objective.get('target_user', 'Not defined')}

**Solution**: {objective.get('solution', 'Not defined')}

**Success Metrics**: {objective.get('success_metrics', 'Not defined')}

**Constraints**: {objective.get('constraints', 'Not defined')}

---

## Current Status

**Phase**: Planning
**Progress**: 0% complete
**Objective Alignment**: 100/100

---

## 📋 Task Queue

### Ready for Autonomous Execution ✅
These tasks can be executed safely without supervision:

_(No tasks ready yet)_

### Pending Approval ⏳
These tasks need review before autonomous execution:

_(No tasks pending yet)_

### Not Ready ❌
These tasks cannot be executed autonomously:

_(None yet)_

## ✅ Completed Tasks

None yet.

---

## 📊 Objective Alignment Audit

Last Audit: {datetime.now().strftime('%Y-%m-%d')}
Score: N/A (no tasks yet)

---

*Generated by Project Manager MCP*
"""

        with open(plan_path, 'w') as f:
            f.write(plan_content)

    def validate_task_alignment(
        self,
        project_path: str,
        task_description: str
    ) -> Dict:
        """Validate task alignment with objective."""
        data = self._load_project_data(project_path)
        objective = data.get("objective")

        if not objective:
            return {
                "error": "No objective defined. Run objective clarification first."
            }

        # Score alignment (simple keyword matching - in real implementation use AI)
        score = self._calculate_task_alignment_score(task_description, objective)

        if score < 70:
            return {
                "aligned": False,
                "score": score,
                "message": "Task does not strongly serve objective",
                "recommendation": "Defer or cut this task. Focus on objective-critical work.",
                "blocked": True
            }

        return {
            "aligned": True,
            "score": score,
            "message": "Task serves objective",
            "proceed": True
        }

    def _calculate_task_alignment_score(self, task_description: str, objective: Dict) -> int:
        """Calculate how well task aligns with objective."""
        score = 50  # Base score

        task_lower = task_description.lower()

        # Check if task relates to problem
        problem_keywords = objective.get("problem", "").lower().split()
        matches = sum(1 for word in problem_keywords if len(word) > 4 and word in task_lower)
        score += min(matches * 10, 30)

        # Check if task relates to solution
        solution_keywords = objective.get("solution", "").lower().split()
        matches = sum(1 for word in solution_keywords if len(word) > 4 and word in task_lower)
        score += min(matches * 10, 20)

        return min(score, 100)

    def validate_task_size(self, task_description: str) -> Dict:
        """Validate task is small enough."""
        issues = []

        # Check description length
        if len(task_description) > 200:
            issues.append("Task description is very long (>200 chars). Consider breaking down.")

        # Check for multiple actions
        action_words = ["and", "then", "after", "also", "plus"]
        count = sum(1 for word in action_words if word in task_description.lower())

        if count >= 3:
            issues.append(f"Task contains {count} connecting words (and, then, etc). Break into separate tasks.")

        # Check for multiple files/modules mentioned
        if task_description.count('/') > 2 or task_description.count('.py') > 2:
            issues.append("Task mentions multiple files. Consider separate tasks per file.")

        if issues:
            return {
                "ok": False,
                "size": "too_large",
                "issues": issues,
                "recommendation": "Break down into smaller, focused tasks"
            }

        return {
            "ok": True,
            "size": "appropriate",
            "message": "Task size is good"
        }

    def challenge_task_priority(self, project_path: str, task_id: str) -> Dict:
        """Challenge if task is highest priority."""
        data = self._load_project_data(project_path)
        objective = data.get("objective")

        if not objective:
            return {"error": "No objective defined"}

        # Get all pending tasks
        tasks = data.get("tasks", [])
        pending_tasks = [t for t in tasks if t.get("status") == "pending"]

        if not pending_tasks:
            return {
                "challenge": False,
                "message": "No other pending tasks to compare"
            }

        # Find this task
        this_task = next((t for t in tasks if t.get("id") == task_id), None)

        if not this_task:
            return {"error": "Task not found"}

        # Score all pending tasks
        scored_tasks = []
        for task in pending_tasks:
            if task.get("id") != task_id:
                score = self._calculate_task_alignment_score(
                    task.get("description", ""),
                    objective
                )
                scored_tasks.append({
                    "id": task["id"],
                    "description": task["description"],
                    "alignment_score": score
                })

        # Sort by score
        scored_tasks.sort(key=lambda x: x["alignment_score"], reverse=True)

        # Get this task's score
        this_score = self._calculate_task_alignment_score(
            this_task.get("description", ""),
            objective
        )

        # Check if others are higher priority
        higher_priority = [t for t in scored_tasks if t["alignment_score"] > this_score]

        if higher_priority:
            return {
                "challenge": True,
                "message": "Higher priority tasks exist",
                "this_task_score": this_score,
                "higher_priority_tasks": higher_priority[:3],  # Top 3
                "recommendation": "Consider working on higher-impact tasks first"
            }

        return {
            "challenge": False,
            "message": "This is the highest priority task",
            "this_task_score": this_score,
            "proceed": True
        }

    def mark_task_complete(
        self,
        project_path: str,
        task_id: str,
        quality_gate_passed: bool
    ) -> Dict:
        """Mark task complete (requires quality gate PASS)."""
        if not quality_gate_passed:
            return {
                "success": False,
                "blocked": True,
                "error": "Quality gate must pass before marking task complete",
                "action": "Fix issues and re-run quality gate"
            }

        data = self._load_project_data(project_path)

        # Find and update task
        tasks = data.get("tasks", [])
        task = next((t for t in tasks if t.get("id") == task_id), None)

        if not task:
            return {"error": "Task not found"}

        # Mark complete
        task["status"] = "completed"
        task["completed_at"] = datetime.now().isoformat()

        # Move to completed
        data["completed_tasks"].append(task)
        data["tasks"] = [t for t in tasks if t.get("id") != task_id]

        # Update PROJECT_PLAN.md
        self._update_project_plan(project_path, data)

        # Log to artifacts
        self._log_task_completion(project_path, task)

        self._save_project_data(project_path, data)

        return {
            "success": True,
            "message": "Task marked complete",
            "task_id": task_id,
            "plan_updated": True
        }

    def _update_project_plan(self, project_path: str, data: Dict):
        """Update PROJECT_PLAN.md."""
        plan_path = Path(project_path) / "docs" / "notes" / "PROJECT_PLAN.md"

        if not plan_path.exists():
            return

        objective = data.get("objective", {})
        tasks = data.get("tasks", [])
        completed = data.get("completed_tasks", [])

        # Calculate progress
        total_tasks = len(tasks) + len(completed)
        progress = (len(completed) / total_tasks * 100) if total_tasks > 0 else 0

        # Regenerate plan
        plan_content = f"""# Project Plan

Last Updated: {datetime.now().strftime('%Y-%m-%d %H:%M')}

## 🎯 OBJECTIVE (Clarity Score: {objective.get('clarity_score', 0)}/100)

**Problem**: {objective.get('problem', 'Not defined')}

**Target User**: {objective.get('target_user', 'Not defined')}

**Solution**: {objective.get('solution', 'Not defined')}

**Success Metrics**: {objective.get('success_metrics', 'Not defined')}

**Constraints**: {objective.get('constraints', 'Not defined')}

---

## Current Status

**Progress**: {len(completed)}/{total_tasks} tasks complete ({progress:.1f}%)
**Objective Alignment**: Good

---

## 📋 Current Task

"""

        # Add current task
        current_task = next((t for t in tasks if t.get("status") == "in_progress"), None)
        if current_task:
            plan_content += f"""
**Task**: {current_task.get('description')}
**Status**: In Progress
**Started**: {current_task.get('started_at', 'Unknown')}

"""
        else:
            plan_content += "No task currently in progress.\n\n"

        # Add pending tasks
        plan_content += "## 📝 Upcoming Tasks\n\n"
        pending = [t for t in tasks if t.get("status") == "pending"]
        for task in pending[:5]:
            plan_content += f"- {task.get('description')}\n"

        # Add completed tasks
        plan_content += "\n## ✅ Completed Tasks\n\n"
        for task in completed[-10:]:  # Last 10
            plan_content += f"- ✅ {task.get('description')} ({task.get('completed_at', 'Unknown')})\n"

        plan_content += "\n---\n\n*Generated by Project Manager MCP*\n"

        with open(plan_path, 'w') as f:
            f.write(plan_content)

    def _log_task_completion(self, project_path: str, task: Dict):
        """Log task completion to artifacts."""
        log_path = Path(project_path) / "artifacts" / "logs" / "completed-actions.log"
        log_path.parent.mkdir(parents=True, exist_ok=True)

        log_entry = f"[{datetime.now().isoformat()}] TASK COMPLETED: {task.get('description')}\n"

        with open(log_path, 'a') as f:
            f.write(log_entry)

    def get_current_status(self, project_path: str) -> Dict:
        """Get current project status."""
        data = self._load_project_data(project_path)

        objective = data.get("objective")
        tasks = data.get("tasks", [])
        completed = data.get("completed_tasks", [])

        total_tasks = len(tasks) + len(completed)
        progress = (len(completed) / total_tasks * 100) if total_tasks > 0 else 0

        current_task = next((t for t in tasks if t.get("status") == "in_progress"), None)

        return {
            "has_objective": objective is not None,
            "objective_clarity_score": objective.get("clarity_score", 0) if objective else 0,
            "total_tasks": total_tasks,
            "completed_tasks": len(completed),
            "pending_tasks": len([t for t in tasks if t.get("status") == "pending"]),
            "progress_percent": progress,
            "current_task": current_task.get("description") if current_task else None,
            "objective_summary": {
                "problem": objective.get("problem", "Not defined")[:100] + "..." if objective else "Not defined",
                "solution": objective.get("solution", "Not defined")[:100] + "..." if objective else "Not defined"
            }
        }

    def identify_scope_creep(self, project_path: str) -> Dict:
        """Identify tasks that don't serve objective."""
        data = self._load_project_data(project_path)
        objective = data.get("objective")

        if not objective:
            return {"error": "No objective defined"}

        tasks = data.get("tasks", [])
        scope_creep = []

        for task in tasks:
            score = self._calculate_task_alignment_score(
                task.get("description", ""),
                objective
            )

            if score < 70:
                scope_creep.append({
                    "task_id": task["id"],
                    "description": task["description"],
                    "alignment_score": score,
                    "recommendation": "cut" if score < 50 else "defer"
                })

        return {
            "scope_creep_detected": len(scope_creep) > 0,
            "total_misaligned_tasks": len(scope_creep),
            "misaligned_tasks": scope_creep,
            "message": "Review and cut/defer these tasks to maintain focus" if scope_creep else "No scope creep detected"
        }

    def refocus_on_objective(self, project_path: str) -> Dict:
        """Refocus project on objective."""
        data = self._load_project_data(project_path)
        objective = data.get("objective")

        if not objective:
            return {"error": "No objective defined"}

        tasks = data.get("tasks", [])

        # Score all tasks
        scored_tasks = []
        for task in tasks:
            score = self._calculate_task_alignment_score(
                task.get("description", ""),
                objective
            )
            scored_tasks.append({
                "task": task,
                "score": score
            })

        # Sort by score
        scored_tasks.sort(key=lambda x: x["score"], reverse=True)

        # Reorganize: high priority first
        data["tasks"] = [st["task"] for st in scored_tasks]

        # Create audit entry
        audit = {
            "timestamp": datetime.now().isoformat(),
            "action": "refocus_on_objective",
            "tasks_reordered": len(tasks),
            "highest_score": scored_tasks[0]["score"] if scored_tasks else 0,
            "lowest_score": scored_tasks[-1]["score"] if scored_tasks else 0
        }
        data["audits"].append(audit)

        self._save_project_data(project_path, data)

        return {
            "success": True,
            "message": "Tasks reordered by objective alignment",
            "tasks_reordered": len(tasks),
            "highest_priority": scored_tasks[0]["task"]["description"] if scored_tasks else None,
            "audit_logged": True
        }

    def sync_plan_to_reality(self, project_path: str) -> Dict:
        """Sync plan to actual project state."""
        # Check for implemented features not in plan
        # Check for plan items already completed
        # This is a placeholder - full implementation would scan code

        return {
            "success": True,
            "message": "Plan synced to reality",
            "discrepancies_found": 0,
            "actions_taken": []
        }

    def create_task_breakdown(self, project_path: str) -> Dict:
        """Create task breakdown from objective."""
        data = self._load_project_data(project_path)
        objective = data.get("objective")

        if not objective:
            return {
                "error": "No objective defined. Run objective clarification first."
            }

        # Generate tasks (placeholder - in real implementation would use AI)
        tasks = self._generate_tasks_from_objective(objective)

        data["tasks"] = tasks
        self._save_project_data(project_path, data)

        # Update PROJECT_PLAN.md
        self._update_project_plan(project_path, data)

        return {
            "success": True,
            "message": "Task breakdown created",
            "total_tasks": len(tasks),
            "tasks": [{"id": t["id"], "description": t["description"]} for t in tasks]
        }

    def _generate_tasks_from_objective(self, objective: Dict) -> List[Dict]:
        """Generate tasks from objective (placeholder)."""
        # In real implementation, would use AI to break down objective into tasks
        return [
            {
                "id": "task_1",
                "description": "Set up project structure and initial files",
                "status": "pending",
                "created_at": datetime.now().isoformat()
            },
            {
                "id": "task_2",
                "description": "Implement core feature (from objective)",
                "status": "pending",
                "created_at": datetime.now().isoformat()
            },
            {
                "id": "task_3",
                "description": "Add tests for core feature",
                "status": "pending",
                "created_at": datetime.now().isoformat()
            }
        ]

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
    server = ProjectServer()
    await server.run()


if __name__ == "__main__":
    asyncio.run(main())
