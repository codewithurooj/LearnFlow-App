"""
Resource Limiter

Utilities for enforcing resource limits on code execution.
"""

import os
import sys
from dataclasses import dataclass
from typing import Optional

import structlog

logger = structlog.get_logger(__name__)


@dataclass
class ResourceLimits:
    """Resource limits for code execution."""
    timeout_seconds: int = 5
    memory_limit_mb: int = 50
    max_output_bytes: int = 100_000  # 100KB
    max_file_size_bytes: int = 0  # No file writing allowed


class ResourceLimiter:
    """
    Manages resource limits for sandboxed execution.

    Note: Full resource limiting requires platform-specific code.
    This implementation provides basic limits that work cross-platform.
    """

    def __init__(self, limits: Optional[ResourceLimits] = None):
        self.limits = limits or ResourceLimits()

    def apply_limits(self) -> bool:
        """
        Apply resource limits to the current process.

        Returns True if limits were applied successfully.
        """
        try:
            self._apply_memory_limit()
            self._apply_file_size_limit()
            return True
        except Exception as e:
            logger.warning(f"Failed to apply some resource limits: {e}")
            return False

    def _apply_memory_limit(self) -> None:
        """Apply memory limit using resource module (Unix only)."""
        try:
            import resource

            # Set virtual memory limit
            memory_bytes = self.limits.memory_limit_mb * 1024 * 1024
            soft, hard = resource.getrlimit(resource.RLIMIT_AS)
            resource.setrlimit(resource.RLIMIT_AS, (memory_bytes, hard))

            logger.debug(f"Applied memory limit: {self.limits.memory_limit_mb}MB")

        except (ImportError, AttributeError):
            # resource module not available on Windows
            logger.debug("Memory limiting not available on this platform")
        except (ValueError, resource.error) as e:
            logger.warning(f"Could not set memory limit: {e}")

    def _apply_file_size_limit(self) -> None:
        """Apply file size limit using resource module (Unix only)."""
        try:
            import resource

            # Set file size limit to 0 (no file writing)
            resource.setrlimit(
                resource.RLIMIT_FSIZE,
                (self.limits.max_file_size_bytes, self.limits.max_file_size_bytes),
            )

            logger.debug("Applied file size limit: 0 bytes (no writing)")

        except (ImportError, AttributeError):
            logger.debug("File size limiting not available on this platform")
        except (ValueError, resource.error) as e:
            logger.warning(f"Could not set file size limit: {e}")

    def truncate_output(self, output: str) -> str:
        """Truncate output to maximum allowed size."""
        max_chars = self.limits.max_output_bytes
        if len(output) > max_chars:
            return output[:max_chars] + f"\n\n... (output truncated at {max_chars} characters)"
        return output

    def get_limits_summary(self) -> dict:
        """Get a summary of current limits."""
        return {
            "timeout_seconds": self.limits.timeout_seconds,
            "memory_limit_mb": self.limits.memory_limit_mb,
            "max_output_bytes": self.limits.max_output_bytes,
            "max_file_size_bytes": self.limits.max_file_size_bytes,
        }


def create_sandbox_env() -> dict[str, str]:
    """
    Create a sanitized environment for sandbox execution.

    Returns a dictionary of environment variables safe for sandboxed code.
    """
    # Start with minimal environment
    safe_env = {
        "PATH": "/usr/bin:/bin",
        "LANG": "C.UTF-8",
        "LC_ALL": "C.UTF-8",
        "PYTHONDONTWRITEBYTECODE": "1",
        "PYTHONUNBUFFERED": "1",
        "PYTHONHASHSEED": "0",  # Deterministic hashing
    }

    # Add Python path if needed
    python_home = os.environ.get("PYTHONHOME")
    if python_home:
        safe_env["PYTHONHOME"] = python_home

    return safe_env


def estimate_memory_usage(code: str) -> int:
    """
    Estimate memory usage for code (very rough estimate).

    This is a heuristic based on code characteristics.
    Actual usage will vary greatly based on execution.

    Returns estimated MB.
    """
    # Base memory for Python interpreter
    base_mb = 10

    # Count potential memory-heavy operations
    large_data_indicators = [
        "range(1000000",  # Large ranges
        "* 1000000",  # Large multiplications
        "[" * 3,  # Nested lists
        "while True",  # Infinite loops risk
    ]

    estimated_mb = base_mb

    for indicator in large_data_indicators:
        if indicator in code:
            estimated_mb += 10

    # Code length heuristic
    estimated_mb += len(code) // 10000  # 1MB per 10KB of code

    return min(estimated_mb, 50)  # Cap at limit
