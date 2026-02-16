"""
Exercise Grader

Auto-grades student submissions against test cases.
"""

import asyncio
from dataclasses import dataclass
from typing import Any

import structlog

import sys
sys.path.insert(0, str(__file__).replace("services/exercise/grader.py", ""))

from shared.config import settings
from shared.models.exercise import TestResult

logger = structlog.get_logger(__name__)


@dataclass
class GradeResult:
    """Result of grading an exercise submission."""
    passed: bool
    score: float  # 0-1
    test_results: list[TestResult]
    execution_error: str | None = None


async def grade_submission(
    code: str,
    test_cases: list[dict[str, Any]],
    timeout: int = 5,
) -> GradeResult:
    """
    Grade a student's code against test cases.

    Args:
        code: Student's submitted code
        test_cases: List of test case definitions
        timeout: Maximum time per test in seconds

    Returns:
        GradeResult with pass/fail and detailed results
    """
    if not test_cases:
        return GradeResult(
            passed=True,
            score=1.0,
            test_results=[],
        )

    results: list[TestResult] = []
    total_weight = sum(tc.get("weight", 1.0) for tc in test_cases)
    weighted_score = 0.0

    for i, test_case in enumerate(test_cases):
        try:
            result = await _run_test_case(
                code=code,
                test_input=test_case.get("input", ""),
                expected_output=test_case.get("expected_output", ""),
                timeout=timeout,
            )

            weight = test_case.get("weight", 1.0)
            if result.passed:
                weighted_score += weight

            results.append(TestResult(
                test_index=i,
                passed=result.passed,
                actual_output=result.actual_output,
                expected_output=test_case.get("expected_output") if not test_case.get("hidden") else None,
                error=result.error,
            ))

        except Exception as e:
            logger.error(f"Test case {i} execution error", error=str(e))
            results.append(TestResult(
                test_index=i,
                passed=False,
                error=str(e),
            ))

    # Calculate final score
    score = weighted_score / total_weight if total_weight > 0 else 0.0
    passed = all(r.passed for r in results)

    return GradeResult(
        passed=passed,
        score=round(score, 2),
        test_results=results,
    )


@dataclass
class TestRunResult:
    """Result of running a single test."""
    passed: bool
    actual_output: str | None
    error: str | None = None


async def _run_test_case(
    code: str,
    test_input: str,
    expected_output: str,
    timeout: int,
) -> TestRunResult:
    """
    Run a single test case.

    Args:
        code: The code to test
        test_input: Input for the test
        expected_output: Expected output
        timeout: Maximum execution time

    Returns:
        TestRunResult with pass/fail and actual output
    """
    # Wrap code with test input handling
    test_code = f"""
import sys
from io import StringIO

# Capture output
_output = StringIO()
_old_stdout = sys.stdout
sys.stdout = _output

# Set up input
_input = StringIO({test_input!r})
_old_stdin = sys.stdin
sys.stdin = _input

try:
{chr(10).join('    ' + line for line in code.split(chr(10)))}
finally:
    sys.stdout = _old_stdout
    sys.stdin = _old_stdin

print("__OUTPUT__:" + _output.getvalue())
"""

    try:
        process = await asyncio.create_subprocess_exec(
            sys.executable if hasattr(sys, 'executable') else 'python',
            '-c', test_code,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE,
        )

        try:
            stdout, stderr = await asyncio.wait_for(
                process.communicate(),
                timeout=timeout,
            )

            stdout_str = stdout.decode('utf-8', errors='replace')
            stderr_str = stderr.decode('utf-8', errors='replace')

            if stderr_str and process.returncode != 0:
                return TestRunResult(
                    passed=False,
                    actual_output=None,
                    error=stderr_str[:500],
                )

            # Extract output
            actual_output = ""
            if "__OUTPUT__:" in stdout_str:
                actual_output = stdout_str.split("__OUTPUT__:")[1].strip()
            else:
                actual_output = stdout_str.strip()

            # Compare outputs (flexible matching)
            passed = _compare_outputs(actual_output, expected_output)

            return TestRunResult(
                passed=passed,
                actual_output=actual_output,
            )

        except asyncio.TimeoutError:
            process.kill()
            return TestRunResult(
                passed=False,
                actual_output=None,
                error=f"Execution timed out after {timeout}s",
            )

    except Exception as e:
        return TestRunResult(
            passed=False,
            actual_output=None,
            error=str(e),
        )


def _compare_outputs(actual: str, expected: str) -> bool:
    """
    Compare actual and expected outputs with flexible matching.

    Handles:
    - Whitespace differences
    - Trailing newlines
    - Case sensitivity (for specific patterns)
    """
    # Normalize whitespace
    actual_normalized = " ".join(actual.split())
    expected_normalized = " ".join(expected.split())

    # Exact match
    if actual_normalized == expected_normalized:
        return True

    # Case-insensitive match for some patterns
    if actual_normalized.lower() == expected_normalized.lower():
        return True

    # Numeric comparison
    try:
        if float(actual_normalized) == float(expected_normalized):
            return True
    except ValueError:
        pass

    return False


def calculate_partial_credit(
    results: list[TestResult],
    test_cases: list[dict[str, Any]],
) -> float:
    """
    Calculate partial credit based on passed tests.

    Args:
        results: Test results
        test_cases: Test case definitions with weights

    Returns:
        Score from 0.0 to 1.0
    """
    if not results:
        return 0.0

    total_weight = sum(tc.get("weight", 1.0) for tc in test_cases)
    earned_weight = sum(
        test_cases[r.test_index].get("weight", 1.0)
        for r in results
        if r.passed
    )

    return earned_weight / total_weight if total_weight > 0 else 0.0


# Import sys for the subprocess
import sys
