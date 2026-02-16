"""
Mastery Level Adapters

Adapters that customize AI responses based on student mastery level.
"""

from abc import ABC, abstractmethod
from typing import Optional


class MasteryAdapter(ABC):
    """Base class for mastery level adapters."""

    @abstractmethod
    def get_instructions(self) -> str:
        """Get AI instructions for this mastery level."""
        pass

    @abstractmethod
    def get_vocabulary_guidelines(self) -> list[str]:
        """Get vocabulary guidelines for this level."""
        pass

    @abstractmethod
    def get_example_complexity(self) -> str:
        """Get description of appropriate example complexity."""
        pass


class BeginnerAdapter(MasteryAdapter):
    """Adapter for beginner-level students (0-40% mastery)."""

    def get_instructions(self) -> str:
        return """For BEGINNER level students:
- Use simple, everyday analogies to explain concepts
- Avoid technical jargon; when you must use it, define it clearly
- Break down complex ideas into very small steps
- Provide more examples than usual, starting with the simplest possible
- Use encouraging language and celebrate small wins
- Connect new concepts to things they already know
- Include "What to remember" bullet points"""

    def get_vocabulary_guidelines(self) -> list[str]:
        return [
            "Use 'container' instead of 'data structure'",
            "Use 'runs the code' instead of 'executes'",
            "Use 'gives back' instead of 'returns'",
            "Explain 'parameter' when first used",
            "Avoid 'iterate' - say 'go through each item'",
        ]

    def get_example_complexity(self) -> str:
        return "Very simple: single operations, print statements, basic math"


class LearningAdapter(MasteryAdapter):
    """Adapter for learning-level students (41-70% mastery)."""

    def get_instructions(self) -> str:
        return """For LEARNING level students:
- Introduce technical terms but still provide brief definitions
- Show comparisons between different approaches
- Explain the "why" behind best practices
- Include both simple and moderately complex examples
- Point out common mistakes and how to avoid them
- Connect concepts to practical use cases
- Encourage experimentation and modification of examples"""

    def get_vocabulary_guidelines(self) -> list[str]:
        return [
            "Can use 'function' and 'method' with brief distinction",
            "Introduce 'iterate' with quick reminder of meaning",
            "Use proper Python terminology with context",
            "Reference documentation conventions",
        ]

    def get_example_complexity(self) -> str:
        return "Moderate: functions, simple loops, basic conditionals, small programs"


class ProficientAdapter(MasteryAdapter):
    """Adapter for proficient-level students (71-90% mastery)."""

    def get_instructions(self) -> str:
        return """For PROFICIENT level students:
- Use technical terminology freely
- Discuss edge cases and potential pitfalls
- Compare different implementation approaches with trade-offs
- Mention performance considerations where relevant
- Show real-world application patterns
- Include industry best practices
- Reference Python documentation and PEP conventions"""

    def get_vocabulary_guidelines(self) -> list[str]:
        return [
            "Use standard Python terminology",
            "Reference PEP-8 conventions",
            "Mention type hints and annotations",
            "Discuss time/space complexity when relevant",
        ]

    def get_example_complexity(self) -> str:
        return "Complex: classes, decorators, context managers, multi-file patterns"


class MasteredAdapter(MasteryAdapter):
    """Adapter for mastered-level students (91-100% mastery)."""

    def get_instructions(self) -> str:
        return """For MASTERED level students:
- Assume comprehensive understanding of fundamentals
- Focus on advanced patterns and optimizations
- Discuss internal implementation details when relevant
- Compare with implementations in other languages
- Reference CPython internals where interesting
- Suggest contributions to open source or advanced projects
- Challenge them with edge cases and brain teasers
- Discuss when NOT to use certain patterns"""

    def get_vocabulary_guidelines(self) -> list[str]:
        return [
            "Use expert-level terminology freely",
            "Reference CPython implementation details",
            "Discuss metaclasses, descriptors, protocols",
            "Mention performance benchmarking approaches",
        ]

    def get_example_complexity(self) -> str:
        return "Advanced: metaclasses, descriptors, async patterns, C extensions interface"


def get_mastery_adapter(mastery_level: str) -> MasteryAdapter:
    """
    Get the appropriate adapter for a mastery level.

    Args:
        mastery_level: One of Beginner, Learning, Proficient, Mastered

    Returns:
        MasteryAdapter instance for the given level
    """
    adapters = {
        "Beginner": BeginnerAdapter(),
        "Learning": LearningAdapter(),
        "Proficient": ProficientAdapter(),
        "Mastered": MasteredAdapter(),
    }

    return adapters.get(mastery_level, BeginnerAdapter())
