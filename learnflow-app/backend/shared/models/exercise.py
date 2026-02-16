"""
Exercise Models

Models for coding exercises, test cases, and student attempts.
"""

from datetime import datetime
from enum import Enum
from typing import Optional
from uuid import UUID, uuid4

from pydantic import BaseModel, Field


class Difficulty(str, Enum):
    """Exercise difficulty levels matching mastery levels."""

    BEGINNER = "beginner"
    LEARNING = "learning"
    PROFICIENT = "proficient"
    MASTERED = "mastered"


class TestCase(BaseModel):
    """A test case for auto-grading exercises."""

    input: str
    expected_output: str
    hidden: bool = True  # Hidden from students
    weight: float = Field(default=1.0, ge=0)
    description: Optional[str] = None


class Exercise(BaseModel):
    """A coding exercise/challenge."""

    exercise_id: UUID = Field(default_factory=uuid4)
    title: str = Field(min_length=1, max_length=200)
    description: str  # Markdown formatted
    topic_id: str
    difficulty: Difficulty
    starter_code: str = Field(default="")
    expected_output_hint: Optional[str] = None
    test_cases: list[TestCase] = Field(min_length=1)
    time_limit_seconds: int = Field(default=5, ge=1, le=30)
    created_at: datetime = Field(default_factory=datetime.utcnow)

    @property
    def total_weight(self) -> float:
        """Calculate total weight of all test cases."""
        return sum(tc.weight for tc in self.test_cases)


class TestResult(BaseModel):
    """Result of running a single test case."""

    test_index: int
    passed: bool
    actual_output: Optional[str] = None
    expected_output: Optional[str] = None
    error: Optional[str] = None
    execution_time_ms: Optional[int] = None


class GradeResult(BaseModel):
    """Result of grading a student submission."""

    exercise_id: UUID
    student_id: UUID
    passed: bool = False
    score: float = Field(default=0.0, ge=0.0, le=100.0)
    test_results: list[TestResult] = Field(default_factory=list)
    feedback: str = ""
    encouragement: str = ""
    next_steps: list[str] = Field(default_factory=list)

    @property
    def tests_passed(self) -> int:
        return sum(1 for r in self.test_results if r.passed)

    @property
    def tests_total(self) -> int:
        return len(self.test_results)


class ExerciseAttempt(BaseModel):
    """A student's attempt at completing an exercise."""

    attempt_id: UUID = Field(default_factory=uuid4)
    exercise_id: UUID
    student_id: UUID
    code: str
    passed: bool = False
    score: float = Field(default=0, ge=0, le=1)  # 0-1 scale
    test_results: list[TestResult] = Field(default_factory=list)
    feedback: Optional[str] = None
    time_spent_seconds: int = Field(ge=0)
    started_at: datetime
    submitted_at: datetime = Field(default_factory=datetime.utcnow)

    @property
    def tests_passed(self) -> int:
        """Count of passed tests."""
        return sum(1 for r in self.test_results if r.passed)

    @property
    def tests_total(self) -> int:
        """Total number of tests."""
        return len(self.test_results)
