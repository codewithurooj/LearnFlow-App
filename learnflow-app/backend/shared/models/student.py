"""
Student and Session Models

Models for student entities and learning sessions.
"""

from datetime import datetime
from typing import Optional
from uuid import UUID, uuid4

from pydantic import BaseModel, EmailStr, Field

from . import Message


class Student(BaseModel):
    """Student entity representing a learner on the platform."""

    id: UUID = Field(default_factory=uuid4)
    email: EmailStr
    name: str
    role: str = Field(default="student", pattern="^(student|teacher|admin)$")
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    class Config:
        from_attributes = True


class StudentSession(BaseModel):
    """Active learning session with conversation history."""

    session_id: UUID = Field(default_factory=uuid4)
    student_id: UUID
    mastery_level: str = Field(
        default="Beginner",
        pattern="^(Beginner|Learning|Proficient|Mastered)$",
    )
    conversation_history: list[Message] = Field(default_factory=list)
    current_topic: Optional[str] = None
    started_at: datetime = Field(default_factory=datetime.utcnow)
    last_activity: datetime = Field(default_factory=datetime.utcnow)

    def add_message(self, role: str, content: str, agent_type: Optional[str] = None) -> None:
        """Add a message to the conversation history."""
        self.conversation_history.append(
            Message(role=role, content=content, agent_type=agent_type)
        )
        self.last_activity = datetime.utcnow()

    def get_recent_messages(self, count: int = 10) -> list[Message]:
        """Get the most recent messages from the conversation."""
        return self.conversation_history[-count:]
