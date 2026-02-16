"""
Code Review AI Agent

OpenAI-powered code review with 4-criteria evaluation and 1-5 star rating.
Uses external system prompt from shared/agents/prompts/code_review.md.
"""

import json
from typing import Any

import structlog
from openai import AsyncOpenAI

import sys
sys.path.insert(0, str(__file__).replace("services/code-review/agent.py", ""))

from shared.config import settings
from shared.agents.base import load_prompt

logger = structlog.get_logger(__name__)

client = AsyncOpenAI(api_key=settings.openai_api_key)

SYSTEM_PROMPT = load_prompt("code_review")


async def review_code(
    code: str,
    context: str = "",
) -> dict[str, Any]:
    """
    Review Python code against 4 criteria with a star rating.

    Args:
        code: The student's Python code
        context: Optional context about what the code should do

    Returns:
        Dict with rating, per-criterion feedback, strengths, suggestions, encouragement
    """
    if not settings.openai_api_key:
        logger.warning("OpenAI API key not configured")
        return _generate_fallback_review(code)

    user_prompt = f"Review this Python code:\n\n```python\n{code[:3000]}\n```"
    if context:
        user_prompt += f"\n\nContext: {context}"

    try:
        response = await client.chat.completions.create(
            model=settings.openai_model,
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": user_prompt},
            ],
            temperature=0.6,
            max_tokens=2000,
            response_format={"type": "json_object"},
        )

        content = response.choices[0].message.content
        if not content:
            raise ValueError("Empty response from AI")

        result = json.loads(content)

        rating = max(1, min(5, int(result.get("rating", 3))))

        return {
            "rating": rating,
            "correctness": result.get("correctness", {"score": 3, "feedback": "Unable to fully assess correctness."}),
            "style": result.get("style", {"score": 3, "feedback": "Style review pending."}),
            "efficiency": result.get("efficiency", {"score": 3, "feedback": "Efficiency review pending."}),
            "readability": result.get("readability", {"score": 3, "feedback": "Readability review pending."}),
            "strengths": result.get("strengths", ["Code submitted for review"]),
            "suggestions": result.get("suggestions", ["Consider adding comments"]),
            "encouragement": result.get("encouragement", "Keep coding and learning!"),
        }

    except Exception as e:
        logger.error("Code review failed", error=str(e))
        return _generate_fallback_review(code)


def _generate_fallback_review(code: str) -> dict[str, Any]:
    """Generate a fallback review when AI is unavailable."""
    lines = code.strip().split("\n")
    has_comments = any(line.strip().startswith("#") for line in lines)
    has_functions = any("def " in line for line in lines)

    strengths = []
    suggestions = []

    if has_comments:
        strengths.append("Good job including comments in your code")
    else:
        suggestions.append("Consider adding comments to explain your logic")

    if has_functions:
        strengths.append("Nice use of functions to organize your code")
    else:
        suggestions.append("Consider breaking your code into functions for better organization")

    if not strengths:
        strengths.append("Thanks for submitting your code for review")

    return {
        "rating": 3,
        "correctness": {"score": 3, "feedback": "AI review unavailable. Please check your code runs correctly."},
        "style": {"score": 3, "feedback": "AI review unavailable. Follow PEP 8 style guidelines."},
        "efficiency": {"score": 3, "feedback": "AI review unavailable. Consider if there are simpler approaches."},
        "readability": {"score": 3, "feedback": "AI review unavailable. Use descriptive variable names."},
        "strengths": strengths,
        "suggestions": suggestions,
        "encouragement": "I'm having trouble connecting right now, but keep up the great work! Review your code against PEP 8 guidelines while I reconnect.",
    }
