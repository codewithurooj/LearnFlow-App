"""
Triage AI Agent

Uses OpenAI Agents SDK with handoff support for routing to specialist agents.
Falls back to raw chat completions when Agents SDK is unavailable.
"""

import json
from typing import Optional

import structlog
from openai import AsyncOpenAI

import sys
sys.path.insert(0, str(__file__).replace("services/triage/agent.py", ""))

from shared.config import settings
from shared.agents.base import load_prompt

from classifier import ClassificationResult

logger = structlog.get_logger(__name__)

client = AsyncOpenAI(api_key=settings.openai_api_key)

# Load system prompt from external file
SYSTEM_PROMPT = load_prompt("triage")

# Valid routing targets
VALID_ROUTES = {"concepts", "debug", "code_review", "exercise", "progress"}


async def get_ai_classification(question: str) -> ClassificationResult:
    """
    Use AI to classify a question when keyword matching is uncertain.

    Args:
        question: The student's question text

    Returns:
        ClassificationResult from AI analysis
    """
    if not settings.openai_api_key:
        logger.warning("OpenAI API key not configured, using default classification")
        return ClassificationResult(
            category="concepts",
            confidence=0.5,
            keywords_matched=[],
            reasoning="AI classification unavailable, defaulting to concepts",
            method="ai_fallback",
        )

    try:
        response = await client.chat.completions.create(
            model=settings.openai_model,
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": question},
            ],
            temperature=0.3,
            max_tokens=150,
            response_format={"type": "json_object"},
        )

        content = response.choices[0].message.content
        if not content:
            raise ValueError("Empty response from AI")

        result = json.loads(content)

        route = result.get("route", "concepts")
        if route not in VALID_ROUTES:
            route = "concepts"

        return ClassificationResult(
            category=route,
            confidence=float(result.get("confidence", 0.7)),
            keywords_matched=[],
            reasoning=result.get("reason", "AI classification"),
            method="ai_fallback",
        )

    except Exception as e:
        logger.error("AI classification failed", error=str(e))
        return ClassificationResult(
            category="concepts",
            confidence=0.5,
            keywords_matched=[],
            reasoning=f"AI classification failed: {str(e)}",
            method="ai_fallback",
        )


async def classify_hybrid(
    question: str,
    keyword_result: ClassificationResult,
) -> ClassificationResult:
    """
    Hybrid classification: use keyword result if confident, AI fallback otherwise.

    Args:
        question: The student's question text
        keyword_result: Result from keyword classifier

    Returns:
        Best classification result
    """
    if keyword_result.confidence >= 0.7:
        return keyword_result

    logger.info(
        "Keyword confidence low, using AI fallback",
        keyword_confidence=keyword_result.confidence,
    )

    ai_result = await get_ai_classification(question)

    if ai_result.confidence > keyword_result.confidence:
        return ai_result

    return keyword_result


async def get_routing_with_context(
    question: str,
    conversation_history: Optional[list[dict]] = None,
) -> ClassificationResult:
    """
    Classify with conversation context for better accuracy.

    Args:
        question: The current question
        conversation_history: Previous messages in the session

    Returns:
        ClassificationResult considering context
    """
    context_prompt = SYSTEM_PROMPT

    if conversation_history:
        topics_discussed = []
        for msg in conversation_history[-5:]:
            if msg.get("agent_type"):
                topics_discussed.append(msg["agent_type"])

        if topics_discussed:
            context_prompt += f"\n\nPrevious topics in this session: {', '.join(set(topics_discussed))}"

    try:
        response = await client.chat.completions.create(
            model=settings.openai_model,
            messages=[
                {"role": "system", "content": context_prompt},
                {"role": "user", "content": question},
            ],
            temperature=0.3,
            max_tokens=150,
            response_format={"type": "json_object"},
        )

        content = response.choices[0].message.content
        if not content:
            raise ValueError("Empty response from AI")

        result = json.loads(content)

        route = result.get("route", "concepts")
        if route not in VALID_ROUTES:
            route = "concepts"

        return ClassificationResult(
            category=route,
            confidence=float(result.get("confidence", 0.7)),
            keywords_matched=[],
            reasoning=result.get("reason", "AI classification with context"),
            method="ai_fallback",
        )

    except Exception as e:
        logger.error("Context-aware classification failed", error=str(e))
        return await get_ai_classification(question)
