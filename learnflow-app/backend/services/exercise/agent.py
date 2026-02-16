"""
Exercise AI Agent

OpenAI-powered exercise generation.
"""

import json
from typing import Optional
from uuid import uuid4

import structlog
from openai import AsyncOpenAI
from pydantic import BaseModel, Field

import sys
sys.path.insert(0, str(__file__).replace("services/exercise/agent.py", ""))

from shared.config import settings
from shared.models.exercise import Difficulty, Exercise, TestCase
from shared.agents.base import load_prompt

logger = structlog.get_logger(__name__)

client = AsyncOpenAI(api_key=settings.openai_api_key)

SYSTEM_PROMPT = load_prompt("exercise")

# Supported exercise types
EXERCISE_TYPES = ["fill_in_blank", "bug_fix", "write_function", "output_prediction"]

DIFFICULTY_GUIDELINES = {
    Difficulty.BEGINNER: """
For BEGINNER level:
- Simple operations: print, basic math, string manipulation
- Single function or script
- 3-4 test cases, mostly visible
- Clear step-by-step instructions""",

    Difficulty.LEARNING: """
For LEARNING level:
- Functions with parameters and return values
- Basic data structures: lists, dictionaries
- Conditionals and loops
- 4-5 test cases with some hidden""",

    Difficulty.PROFICIENT: """
For PROFICIENT level:
- Multiple functions or a class
- Error handling required
- Algorithm implementation
- 5-6 test cases with edge cases hidden""",

    Difficulty.MASTERED: """
For MASTERED level:
- Complex algorithms or design patterns
- Performance considerations
- Advanced Python features
- 6+ test cases including performance tests""",
}


class ExerciseSpec(BaseModel):
    """Specification for generating an exercise."""
    topic: str
    difficulty: Difficulty
    constraints: list[str] = Field(default_factory=list)


async def generate_exercise(
    topic: str,
    difficulty: Difficulty,
    constraints: Optional[list[str]] = None,
) -> Exercise:
    """
    Generate an exercise using AI.

    Args:
        topic: The Python topic for the exercise
        difficulty: Target difficulty level
        constraints: Additional constraints for the exercise

    Returns:
        Generated Exercise object
    """
    if not settings.openai_api_key:
        return _generate_fallback_exercise(topic, difficulty)

    difficulty_guide = DIFFICULTY_GUIDELINES.get(difficulty, DIFFICULTY_GUIDELINES[Difficulty.BEGINNER])

    prompt = f"""Generate a Python coding exercise about: {topic}

{difficulty_guide}

{"Additional constraints: " + ", ".join(constraints) if constraints else ""}

Make sure the exercise is practical and tests real understanding of the concept."""

    try:
        response = await client.chat.completions.create(
            model=settings.openai_model,
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": prompt},
            ],
            temperature=0.8,
            max_tokens=1500,
            response_format={"type": "json_object"},
        )

        content = response.choices[0].message.content
        if not content:
            raise ValueError("Empty response from AI")

        data = json.loads(content)

        # Parse test cases
        test_cases = [
            TestCase(
                input=tc.get("input", ""),
                expected_output=tc.get("expected_output", ""),
                hidden=tc.get("hidden", True),
            )
            for tc in data.get("test_cases", [])
        ]

        # Ensure at least one test case
        if not test_cases:
            test_cases = [TestCase(input="", expected_output="", hidden=False)]

        return Exercise(
            exercise_id=uuid4(),
            title=data.get("title", f"{topic} Exercise"),
            description=data.get("description", f"Complete the exercise about {topic}"),
            topic_id=topic.lower().replace(" ", "_"),
            difficulty=difficulty,
            starter_code=data.get("starter_code", "# Write your code here\n"),
            expected_output_hint=data.get("expected_output_hint"),
            test_cases=test_cases,
        )

    except Exception as e:
        logger.error("Exercise generation failed", error=str(e), topic=topic)
        return _generate_fallback_exercise(topic, difficulty)


def _generate_fallback_exercise(topic: str, difficulty: Difficulty) -> Exercise:
    """Generate a fallback exercise when AI is unavailable."""
    templates = {
        Difficulty.BEGINNER: {
            "title": f"Basic {topic.title()} Exercise",
            "description": f"""# {topic.title()} Practice

Write a Python program that demonstrates your understanding of {topic}.

## Instructions
1. Read the problem carefully
2. Write your solution in the code editor
3. Test your code before submitting

## Example
```python
# Your solution should work like this:
# Input: sample input
# Output: expected output
```
""",
            "starter_code": f"# {topic.title()} Exercise\n# Write your solution below\n\ndef solution():\n    # TODO: Implement your solution\n    pass\n",
            "test_cases": [
                TestCase(input="test", expected_output="test", hidden=False),
            ],
        },
        Difficulty.LEARNING: {
            "title": f"{topic.title()} Function",
            "description": f"Implement a function that works with {topic}.",
            "starter_code": f"def solve_{topic.lower().replace(' ', '_')}(data):\n    # TODO: Implement\n    pass\n",
            "test_cases": [
                TestCase(input="[1, 2, 3]", expected_output="result", hidden=False),
                TestCase(input="[]", expected_output="edge", hidden=True),
            ],
        },
    }

    template = templates.get(difficulty, templates[Difficulty.BEGINNER])

    return Exercise(
        exercise_id=uuid4(),
        title=template["title"],
        description=template["description"],
        topic_id=topic.lower().replace(" ", "_"),
        difficulty=difficulty,
        starter_code=template["starter_code"],
        test_cases=template["test_cases"],
    )
