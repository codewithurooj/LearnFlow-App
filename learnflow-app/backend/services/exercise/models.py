"""
Exercise Service Models

Request and response models for the Exercise API.
"""

from typing import Optional
from uuid import UUID

from pydantic import BaseModel, Field

import sys
sys.path.insert(0, str(__file__).replace("services/exercise/models.py", ""))

from shared.models.exercise import Difficulty, TestResult


class ExerciseGenerateRequest(BaseModel):
    """Request for exercise generation (query parameters)."""

    student_id: UUID
    topic: str = Field(min_length=1, max_length=100)
    difficulty: Optional[Difficulty] = None


class ExerciseGenerateResponse(BaseModel):
    """Response with generated exercise."""

    exercise_id: UUID
    title: str
    description: str = Field(description="Markdown-formatted problem statement")
    starter_code: str
    expected_output_hint: Optional[str] = None


class ExerciseSubmitRequest(BaseModel):
    """Request for exercise submission."""

    student_id: UUID
    exercise_id: UUID
    code: str = Field(min_length=1, max_length=50000)


class ExerciseSubmitResponse(BaseModel):
    """Response from exercise grading."""

    passed: bool = Field(description="Whether all tests passed")
    score: float = Field(ge=0, le=1, description="Score from 0 to 1")
    test_results: list[TestResult] = Field(
        description="Results for each test case"
    )
    feedback: str = Field(description="Feedback message for the student")
    time_spent_seconds: int = Field(
        description="Time spent on the exercise"
    )
