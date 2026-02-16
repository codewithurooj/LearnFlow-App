"""
Struggle Detector

Detects patterns indicating a student is struggling.
"""

from collections import defaultdict
from dataclasses import dataclass, field
from datetime import datetime, timedelta
from typing import Optional
from uuid import UUID

import structlog

import sys
sys.path.insert(0, str(__file__).replace("services/debug/struggle_detector.py", ""))

from shared.config import settings

logger = structlog.get_logger(__name__)


@dataclass
class ErrorRecord:
    """Record of a single error occurrence."""
    error_type: str
    timestamp: datetime = field(default_factory=datetime.utcnow)


@dataclass
class StudentErrorHistory:
    """Error history for a single student."""
    errors: list[ErrorRecord] = field(default_factory=list)
    last_cleanup: datetime = field(default_factory=datetime.utcnow)


class StruggleDetector:
    """
    Detects struggle patterns using a sliding window approach.

    Patterns detected:
    - Same error type 3+ times within 30 minutes
    - 5+ total errors within 10 minutes (frustration)
    """

    def __init__(
        self,
        error_threshold: int = 3,
        window_minutes: int = 30,
        frustration_threshold: int = 5,
        frustration_window_minutes: int = 10,
    ):
        self.error_threshold = error_threshold or settings.struggle_error_threshold
        self.window_minutes = window_minutes
        self.frustration_threshold = frustration_threshold
        self.frustration_window = frustration_window_minutes

        # Student ID -> ErrorHistory
        self._history: dict[str, StudentErrorHistory] = defaultdict(StudentErrorHistory)

    def record_error(
        self,
        student_id: UUID,
        error_type: str,
    ) -> bool:
        """
        Record an error and check for struggle patterns.

        Args:
            student_id: The student's ID
            error_type: The type of error encountered

        Returns:
            True if a struggle pattern was detected
        """
        key = str(student_id)
        now = datetime.utcnow()

        # Get or create history
        history = self._history[key]

        # Cleanup old entries periodically
        if now - history.last_cleanup > timedelta(minutes=5):
            self._cleanup_old_entries(history, now)

        # Add new error
        history.errors.append(ErrorRecord(error_type=error_type, timestamp=now))

        # Check for patterns
        return self._check_patterns(history, error_type, now)

    def _cleanup_old_entries(
        self,
        history: StudentErrorHistory,
        now: datetime,
    ) -> None:
        """Remove entries older than the window."""
        cutoff = now - timedelta(minutes=self.window_minutes)
        history.errors = [e for e in history.errors if e.timestamp > cutoff]
        history.last_cleanup = now

    def _check_patterns(
        self,
        history: StudentErrorHistory,
        current_error: str,
        now: datetime,
    ) -> bool:
        """Check for struggle patterns in the history."""
        window_start = now - timedelta(minutes=self.window_minutes)
        frustration_start = now - timedelta(minutes=self.frustration_window)

        # Count same error type within window
        same_error_count = sum(
            1 for e in history.errors
            if e.error_type == current_error and e.timestamp > window_start
        )

        if same_error_count >= self.error_threshold:
            logger.info(
                "Same error pattern detected",
                error_type=current_error,
                count=same_error_count,
            )
            return True

        # Count total errors within frustration window
        recent_error_count = sum(
            1 for e in history.errors
            if e.timestamp > frustration_start
        )

        if recent_error_count >= self.frustration_threshold:
            logger.info(
                "High error frequency detected",
                count=recent_error_count,
                window_minutes=self.frustration_window,
            )
            return True

        return False

    def get_error_count(
        self,
        student_id: UUID,
        error_type: str,
    ) -> int:
        """Get the count of a specific error type for a student."""
        key = str(student_id)
        history = self._history.get(key)

        if not history:
            return 0

        now = datetime.utcnow()
        window_start = now - timedelta(minutes=self.window_minutes)

        return sum(
            1 for e in history.errors
            if e.error_type == error_type and e.timestamp > window_start
        )

    def get_student_summary(self, student_id: UUID) -> dict:
        """Get a summary of errors for a student."""
        key = str(student_id)
        history = self._history.get(key)

        if not history:
            return {"total_errors": 0, "error_types": {}}

        now = datetime.utcnow()
        window_start = now - timedelta(minutes=self.window_minutes)

        recent_errors = [e for e in history.errors if e.timestamp > window_start]

        # Count by type
        type_counts: dict[str, int] = defaultdict(int)
        for error in recent_errors:
            type_counts[error.error_type] += 1

        return {
            "total_errors": len(recent_errors),
            "error_types": dict(type_counts),
            "window_minutes": self.window_minutes,
        }

    def clear_history(self, student_id: UUID) -> None:
        """Clear error history for a student (e.g., after session ends)."""
        key = str(student_id)
        if key in self._history:
            del self._history[key]
