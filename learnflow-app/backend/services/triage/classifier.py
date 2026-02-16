"""
Question Classifier

Keyword-based classification with AI fallback for routing student questions.
"""

import re
from dataclasses import dataclass
from typing import Optional


@dataclass
class ClassificationResult:
    """Result of question classification."""
    category: str  # concepts, debug, code_review, exercise, progress
    confidence: float
    keywords_matched: list[str]
    reasoning: str
    method: str = "keyword"  # "keyword" | "ai_fallback"


# Keyword patterns for each category
ROUTING_PATTERNS = {
    "concepts": {
        "keywords": [
            "explain", "what is", "what are", "how does", "how do",
            "why", "define", "definition", "meaning", "understand",
            "concept", "tell me about", "describe", "difference between",
            "when to use", "purpose of", "learn about", "teach me",
        ],
        "weight": 1.0,
    },
    "debug": {
        "keywords": [
            "error", "exception", "traceback", "bug", "not working",
            "doesn't work", "fails", "failed", "broken", "wrong",
            "fix", "issue", "problem", "crash", "unexpected",
            "syntaxerror", "nameerror", "typeerror", "indexerror",
            "keyerror", "valueerror", "attributeerror", "importerror",
        ],
        "weight": 1.2,
    },
    "code_review": {
        "keywords": [
            "review", "check my code", "look at my code", "is this correct",
            "better way", "improve", "optimize", "best practice",
            "feedback", "suggestions", "clean up", "refactor",
            "style", "pep8", "pythonic", "is this good",
        ],
        "weight": 1.0,
    },
    "exercise": {
        "keywords": [
            "practice", "exercise", "challenge", "problem to solve",
            "give me a task", "test me", "quiz", "assignment",
            "project idea", "homework", "try", "hands-on",
        ],
        "weight": 1.0,
    },
    "progress": {
        "keywords": [
            "progress", "how am i doing", "mastery", "score",
            "streak", "my level", "improvement", "how far",
            "my performance", "my stats",
        ],
        "weight": 1.1,
    },
}

# Frustration keywords for struggle detection
FRUSTRATION_KEYWORDS = [
    "i don't understand", "i'm stuck", "i am stuck",
    "confused", "help me", "i give up", "makes no sense",
    "don't get it", "too hard",
]


def classify_question(question: str) -> ClassificationResult:
    """
    Classify a question using keyword matching.

    Args:
        question: The student's question text

    Returns:
        ClassificationResult with category, confidence, and matched keywords
    """
    question_lower = question.lower()

    scores: dict[str, float] = {}
    matches: dict[str, list[str]] = {}

    for category, config in ROUTING_PATTERNS.items():
        matched_keywords = []
        for keyword in config["keywords"]:
            if keyword in question_lower:
                matched_keywords.append(keyword)

        if matched_keywords:
            score = len(matched_keywords) * config["weight"]
            scores[category] = score
            matches[category] = matched_keywords

    if not scores:
        return ClassificationResult(
            category="concepts",
            confidence=0.3,
            keywords_matched=[],
            reasoning="No specific keywords matched, defaulting to concept explanation",
            method="keyword",
        )

    best_category = max(scores, key=lambda k: scores[k])
    best_score = scores[best_category]
    total_matches = sum(len(m) for m in matches.values())

    if total_matches > 0:
        exclusivity = len(matches[best_category]) / total_matches
        confidence = min(0.5 + (best_score * 0.1 * exclusivity), 0.95)
    else:
        confidence = 0.3

    return ClassificationResult(
        category=best_category,
        confidence=round(confidence, 2),
        keywords_matched=matches[best_category],
        reasoning=f"Matched keywords: {', '.join(matches[best_category])}",
        method="keyword",
    )


def detect_frustration(question: str) -> bool:
    """Check if the question contains frustration keywords."""
    question_lower = question.lower()
    return any(kw in question_lower for kw in FRUSTRATION_KEYWORDS)


def extract_topic(question: str) -> Optional[str]:
    """
    Extract the main topic from a question.

    Args:
        question: The student's question text

    Returns:
        The extracted topic or None
    """
    patterns = [
        r"(?:explain|what (?:is|are)|how (?:does|do)|tell me about)\s+(.+?)(?:\?|$)",
        r"(?:learn about|understand)\s+(.+?)(?:\?|$)",
        r"(.+?)\s+(?:error|exception|not working)",
    ]

    for pattern in patterns:
        match = re.search(pattern, question, re.IGNORECASE)
        if match:
            topic = match.group(1).strip()
            topic = re.sub(r"\s+in\s+python$", "", topic, flags=re.IGNORECASE)
            return topic

    return None
