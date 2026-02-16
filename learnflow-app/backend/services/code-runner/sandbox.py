"""
Python Sandbox

Secure sandboxed execution of Python code with resource limits.
"""

import ast
import asyncio
import subprocess
import sys
import tempfile
import os
from dataclasses import dataclass
from typing import Optional

import structlog

logger = structlog.get_logger(__name__)

# Allowed imports for sandbox
ALLOWED_IMPORTS = {
    "math", "random", "string", "collections", "itertools",
    "functools", "json", "re", "datetime", "typing",
    "decimal", "fractions", "statistics", "copy",
    "operator", "heapq", "bisect", "array",
}

# Blocked builtins and operations
BLOCKED_BUILTINS = {
    "open", "exec", "eval", "compile", "__import__",
    "input", "breakpoint", "help", "credits", "license",
}

BLOCKED_MODULES = {
    "os", "sys", "subprocess", "socket", "http", "urllib",
    "ftplib", "smtplib", "telnetlib", "ssl", "ctypes",
    "multiprocessing", "threading", "asyncio", "signal",
    "shutil", "pathlib", "glob", "tempfile", "pickle",
    "shelve", "dbm", "sqlite3", "importlib",
}


@dataclass
class SandboxResult:
    """Result of sandboxed code execution."""
    stdout: str
    stderr: str
    exit_code: int
    execution_time_ms: int
    memory_used_mb: float
    timed_out: bool
    error_type: Optional[str] = None


def validate_code(code: str) -> tuple[bool, Optional[str]]:
    """
    Validate code for security before execution.

    Args:
        code: Python code to validate

    Returns:
        Tuple of (is_valid, error_message)
    """
    try:
        tree = ast.parse(code)
    except SyntaxError as e:
        return False, f"SyntaxError: {e.msg} at line {e.lineno}"

    for node in ast.walk(tree):
        # Check for import statements
        if isinstance(node, ast.Import):
            for alias in node.names:
                module = alias.name.split(".")[0]
                if module in BLOCKED_MODULES:
                    return False, f"Import of '{module}' is not allowed"
                if module not in ALLOWED_IMPORTS:
                    return False, f"Import of '{module}' is not in the allowed list"

        elif isinstance(node, ast.ImportFrom):
            module = (node.module or "").split(".")[0]
            if module in BLOCKED_MODULES:
                return False, f"Import from '{module}' is not allowed"
            if module and module not in ALLOWED_IMPORTS:
                return False, f"Import from '{module}' is not in the allowed list"

        # Check for blocked function calls
        elif isinstance(node, ast.Call):
            if isinstance(node.func, ast.Name):
                if node.func.id in BLOCKED_BUILTINS:
                    return False, f"Use of '{node.func.id}' is not allowed"

        # Check for attribute access that might be dangerous
        elif isinstance(node, ast.Attribute):
            if node.attr.startswith("_"):
                return False, f"Access to private attributes ('{node.attr}') is not allowed"

    return True, None


def extract_error_type(stderr: str) -> Optional[str]:
    """Extract the Python error type from stderr."""
    error_types = [
        "SyntaxError", "NameError", "TypeError", "ValueError",
        "IndexError", "KeyError", "AttributeError", "ImportError",
        "ZeroDivisionError", "RuntimeError", "RecursionError",
        "MemoryError", "TimeoutError", "IndentationError",
    ]

    for error_type in error_types:
        if error_type in stderr:
            return error_type

    if "Traceback" in stderr:
        return "RuntimeError"

    return None


async def execute_code(
    code: str,
    timeout: int = 5,
    memory_limit_mb: int = 50,
) -> SandboxResult:
    """
    Execute Python code in a sandboxed environment.

    Args:
        code: Python code to execute
        timeout: Maximum execution time in seconds
        memory_limit_mb: Maximum memory usage in MB

    Returns:
        SandboxResult with execution results
    """
    # Validate code first
    is_valid, error = validate_code(code)
    if not is_valid:
        return SandboxResult(
            stdout="",
            stderr=error or "Code validation failed",
            exit_code=1,
            execution_time_ms=0,
            memory_used_mb=0,
            timed_out=False,
            error_type="SecurityError",
        )

    # Create wrapper code with safety measures
    wrapper_code = f'''
import sys
import resource

# Set memory limit (Unix only, Windows will skip)
try:
    soft, hard = resource.getrlimit(resource.RLIMIT_AS)
    resource.setrlimit(resource.RLIMIT_AS, ({memory_limit_mb} * 1024 * 1024, hard))
except (AttributeError, ValueError, resource.error):
    pass  # Windows or limit already set

# Block dangerous builtins
import builtins
_blocked = {BLOCKED_BUILTINS!r}
for name in _blocked:
    if hasattr(builtins, name):
        delattr(builtins, name)

# Execute user code
try:
{chr(10).join("    " + line for line in code.split(chr(10)))}
except Exception as e:
    print(f"{{type(e).__name__}}: {{e}}", file=sys.stderr)
    sys.exit(1)
'''

    # Write to temporary file
    with tempfile.NamedTemporaryFile(
        mode="w",
        suffix=".py",
        delete=False,
    ) as f:
        f.write(wrapper_code)
        temp_file = f.name

    try:
        # Execute with subprocess
        process = await asyncio.create_subprocess_exec(
            sys.executable,
            temp_file,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE,
            env={**os.environ, "PYTHONDONTWRITEBYTECODE": "1"},
        )

        try:
            stdout, stderr = await asyncio.wait_for(
                process.communicate(),
                timeout=timeout,
            )

            return SandboxResult(
                stdout=stdout.decode("utf-8", errors="replace")[:10000],
                stderr=stderr.decode("utf-8", errors="replace")[:10000],
                exit_code=process.returncode or 0,
                execution_time_ms=0,  # Would need timing wrapper
                memory_used_mb=0,  # Would need monitoring
                timed_out=False,
                error_type=extract_error_type(stderr.decode("utf-8", errors="replace")),
            )

        except asyncio.TimeoutError:
            process.kill()
            await process.wait()

            return SandboxResult(
                stdout="",
                stderr=f"Execution timed out after {timeout} seconds",
                exit_code=1,
                execution_time_ms=timeout * 1000,
                memory_used_mb=0,
                timed_out=True,
                error_type="TimeoutError",
            )

    finally:
        # Clean up temp file
        try:
            os.unlink(temp_file)
        except OSError:
            pass
