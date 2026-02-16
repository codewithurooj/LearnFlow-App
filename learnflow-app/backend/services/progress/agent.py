"""
Progress AI Agent

Generates natural language progress summaries and recommendations
using external system prompt from shared/agents/prompts/progress.md.
"""

import json
from typing import Any

import structlog
from openai import AsyncOpenAI

import sys
sys.path.insert(0, str(__file__).replace("services/progress/agent.py", ""))

from shared.config import settings
from shared.agents.base import load_prompt

logger = structlog.get_logger(__name__)

client = AsyncOpenAI(api_key=settings.openai_api_key)

SYSTEM_PROMPT = load_prompt("progress")


async def generate_progress_summary(
    student_data: dict[str, Any],
) -> dict[str, Any]:
    """
    Generate a natural language progress summary.

    Args:
        student_data: Dict with overall_mastery, topics, streak, etc.

    Returns:
        Dict with summary text, recommendations, and milestones
    """
    if not settings.openai_api_key:
        return _generate_fallback_summary(student_data)

    user_prompt = f"""Generate a progress summary for this student:

Overall mastery: {student_data.get('overall_mastery', 0)}%
Current streak: {student_data.get('current_streak', 0)} days
Topics: {json.dumps(student_data.get('topics', []), indent=2)}

Provide an encouraging summary with specific recommendations."""

    try:
        response = await client.chat.completions.create(
            model=settings.openai_model,
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": user_prompt},
            ],
            temperature=0.5,
            max_tokens=1000,
            response_format={"type": "json_object"},
        )

        content = response.choices[0].message.content
        if not content:
            raise ValueError("Empty response from AI")

        return json.loads(content)

    except Exception as e:
        logger.error("Progress summary generation failed", error=str(e))
        return _generate_fallback_summary(student_data)


def _generate_fallback_summary(student_data: dict[str, Any]) -> dict[str, Any]:
    """Generate fallback summary when AI is unavailable."""
    overall = student_data.get("overall_mastery", 0)
    streak = student_data.get("current_streak", 0)
    topics = student_data.get("topics", [])

    recommendations = []
    if overall < 40:
        recommendations.append("Focus on completing more exercises to build fundamentals")
    elif overall < 70:
        recommendations.append("Great progress! Try tackling more challenging topics")
    else:
        recommendations.append("Excellent work! Consider exploring advanced Python concepts")

    if streak == 0:
        recommendations.append("Start a daily practice streak to maintain momentum")
    elif streak >= 7:
        recommendations.append(f"Amazing {streak}-day streak! Keep it up!")

    milestones = []
    if streak == 7:
        milestones.append("A whole week of learning! Incredible dedication!")

    return {
        "overall_mastery": overall,
        "recent_activity": f"Current streak: {streak} days",
        "current_streak": streak,
        "milestones": milestones,
        "recommendations": recommendations,
    }
