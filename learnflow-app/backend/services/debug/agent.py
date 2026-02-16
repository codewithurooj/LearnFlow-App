"""
Debug AI Agent

OpenAI-powered debugging assistance with hints-before-solutions approach.
"""

import json
from typing import Any, Optional

import structlog
from openai import AsyncOpenAI

import sys
sys.path.insert(0, str(__file__).replace("services/debug/agent.py", ""))

from shared.config import settings
from shared.agents.base import load_prompt

from error_parser import ErrorInfo, get_error_explanation, suggest_common_fixes

logger = structlog.get_logger(__name__)

client = AsyncOpenAI(api_key=settings.openai_api_key)

# Load system prompt from external file
SYSTEM_PROMPT = load_prompt("debug")


async def analyze_error(
    code: str,
    error_info: ErrorInfo,
    error_output: str,
    include_solution: bool = False,
) -> dict[str, Any]:
    """
    Analyze an error and provide debugging assistance.

    Args:
        code: The student's code
        error_info: Parsed error information
        error_output: Raw error output
        include_solution: Whether to include the solution

    Returns:
        Dict with analysis, hints, and optionally solution
    """
    if not settings.openai_api_key:
        return _generate_fallback_analysis(error_info)

    # Build context for the AI
    context = f"""
Error Type: {error_info.error_type}
Error Message: {error_info.message}
Line Number: {error_info.line_number or 'Unknown'}
Code Context: {error_info.code_context or 'Not available'}

Full Error:
{error_output[:500]}

Student's Code:
```python
{code[:2000]}
```
"""

    user_prompt = "Analyze this error and help the student understand what went wrong."
    if include_solution:
        user_prompt += " Please include the solution and corrected code."

    try:
        response = await client.chat.completions.create(
            model=settings.openai_model,
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": context + "\n\n" + user_prompt},
            ],
            temperature=0.5,
            max_tokens=1000,
            response_format={"type": "json_object"},
        )

        content = response.choices[0].message.content
        if not content:
            raise ValueError("Empty response from AI")

        result = json.loads(content)

        # If not including solution, remove it from response
        if not include_solution:
            result.pop("solution", None)
            result.pop("corrected_code", None)

        return result

    except Exception as e:
        logger.error("AI analysis failed", error=str(e))
        return _generate_fallback_analysis(error_info)


def _generate_fallback_analysis(error_info: ErrorInfo) -> dict[str, Any]:
    """Generate fallback analysis when AI is unavailable."""
    explanation = get_error_explanation(error_info.error_type)
    suggestions = suggest_common_fixes(error_info.error_type, error_info.message)

    hint = suggestions[0] if suggestions else "Check your code carefully at the error location"

    return {
        "root_cause": f"{error_info.error_type}: {explanation}",
        "hint": hint,
        "concepts_to_review": [error_info.error_type.replace("Error", "")],
    }


async def explain_error_type(error_type: str) -> str:
    """
    Get a detailed explanation of an error type.

    Useful for students who want to understand the error category better.
    """
    if not settings.openai_api_key:
        return get_error_explanation(error_type)

    try:
        response = await client.chat.completions.create(
            model=settings.openai_model,
            messages=[
                {
                    "role": "system",
                    "content": "You are a Python teacher. Explain errors simply.",
                },
                {
                    "role": "user",
                    "content": f"Explain {error_type} in Python for a beginner. Include common causes and how to avoid it.",
                },
            ],
            temperature=0.7,
            max_tokens=500,
        )

        return response.choices[0].message.content or get_error_explanation(error_type)

    except Exception as e:
        logger.error("Error explanation failed", error=str(e))
        return get_error_explanation(error_type)
