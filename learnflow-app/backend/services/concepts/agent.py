"""
Concepts AI Agent

OpenAI-powered concept explanation with mastery adaptation.
Uses external system prompt from shared/agents/prompts/concepts.md.
"""

import json
from typing import Any, Optional

import structlog
from openai import AsyncOpenAI

import sys
sys.path.insert(0, str(__file__).replace("services/concepts/agent.py", ""))

from shared.config import settings
from shared.models import Message
from shared.agents.base import load_prompt
from shared.dapr import get_state

from adapters import MasteryAdapter

logger = structlog.get_logger(__name__)

client = AsyncOpenAI(api_key=settings.openai_api_key)

# Load system prompt from external file
BASE_SYSTEM_PROMPT = load_prompt("concepts")


async def explain_concept(
    topic: str,
    mastery_level: str,
    context: list[Message],
    adapter: MasteryAdapter,
) -> dict[str, Any]:
    """
    Generate a concept explanation adapted to mastery level.

    Args:
        topic: The Python concept to explain
        mastery_level: Student's current mastery level
        context: Conversation history for continuity
        adapter: Mastery adapter with level-specific instructions

    Returns:
        Dict with explanation, code_example, key_takeaway, related_concepts
    """
    if not settings.openai_api_key:
        logger.warning("OpenAI API key not configured")
        return _generate_fallback_response(topic, mastery_level)

    # Build system prompt with mastery adaptation
    system_prompt = f"""{BASE_SYSTEM_PROMPT}

Student mastery level: {mastery_level}

{adapter.get_instructions()}

Vocabulary guidelines: {', '.join(adapter.get_vocabulary_guidelines())}
Example complexity: {adapter.get_example_complexity()}

Remember to adapt your language and examples to this level."""

    messages = [{"role": "system", "content": system_prompt}]

    for msg in context[-5:]:
        messages.append({
            "role": msg.role,
            "content": msg.content,
        })

    messages.append({
        "role": "user",
        "content": f"Please explain: {topic}",
    })

    try:
        response = await client.chat.completions.create(
            model=settings.openai_model,
            messages=messages,
            temperature=0.7,
            max_tokens=2000,
            response_format={"type": "json_object"},
        )

        content = response.choices[0].message.content
        if not content:
            raise ValueError("Empty response from AI")

        result = json.loads(content)

        return {
            "explanation": result.get("explanation", f"Let me explain {topic}..."),
            "code_example": result.get("code_example", ""),
            "key_takeaway": result.get("key_takeaway", ""),
            "examples": result.get("examples", []),
            "related_topics": result.get("related_concepts", result.get("related_topics", [])),
        }

    except Exception as e:
        logger.error("Concept explanation failed", error=str(e), topic=topic)
        return _generate_fallback_response(topic, mastery_level)


async def explain_with_mastery_lookup(
    student_id: str,
    topic: str,
    context: list[Message],
    adapter: MasteryAdapter,
) -> dict[str, Any]:
    """
    Explain a concept after loading the student's mastery level from Dapr state.

    Args:
        student_id: The student's ID for state lookup
        topic: The Python concept to explain
        context: Conversation history
        adapter: Mastery adapter (may be overridden by state)

    Returns:
        Dict with explanation
    """
    mastery_level = "Beginner"

    try:
        mastery_data = await get_state(f"mastery:{student_id}:{topic}")
        if mastery_data:
            score = mastery_data.get("total_score", 0)
            if score >= 91:
                mastery_level = "Mastered"
            elif score >= 71:
                mastery_level = "Proficient"
            elif score >= 41:
                mastery_level = "Learning"
    except Exception as e:
        logger.warning("Could not load mastery state", error=str(e))

    return await explain_concept(topic, mastery_level, context, adapter)


def _generate_fallback_response(topic: str, mastery_level: str) -> dict[str, Any]:
    """Generate a fallback response when AI is unavailable."""
    return {
        "explanation": f"""# {topic.title()}

I apologize, but I'm having trouble generating a detailed explanation right now.

Here's a brief overview of {topic} in Python:

{topic.title()} is an important concept in Python programming. To learn more about it:

1. Check the official Python documentation
2. Try experimenting with code examples
3. Practice with small exercises

I'll be happy to help once the connection is restored!""",
        "code_example": f"# Example for {topic}\n# Try experimenting with Python!",
        "key_takeaway": f"Practice is key to understanding {topic}.",
        "examples": [
            {
                "title": "Basic Example",
                "code": f"# Example for {topic}\n# Try experimenting with Python!",
                "explanation": "This is a placeholder example.",
            }
        ],
        "related_topics": ["Python basics", "Documentation", "Practice exercises"],
    }


async def get_follow_up_explanation(
    original_topic: str,
    follow_up_question: str,
    previous_explanation: str,
    mastery_level: str,
) -> dict[str, Any]:
    """Generate a follow-up explanation based on student's question."""
    if not settings.openai_api_key:
        return _generate_fallback_response(follow_up_question, mastery_level)

    system_prompt = f"""{BASE_SYSTEM_PROMPT}

Context: The student was learning about "{original_topic}" and received this explanation:
---
{previous_explanation[:500]}...
---

Now they have a follow-up question. Answer it while maintaining continuity with the previous explanation.
Student level: {mastery_level}"""

    try:
        response = await client.chat.completions.create(
            model=settings.openai_model,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": follow_up_question},
            ],
            temperature=0.7,
            max_tokens=1500,
            response_format={"type": "json_object"},
        )

        content = response.choices[0].message.content
        if not content:
            raise ValueError("Empty response from AI")

        return json.loads(content)

    except Exception as e:
        logger.error("Follow-up explanation failed", error=str(e))
        return _generate_fallback_response(follow_up_question, mastery_level)
