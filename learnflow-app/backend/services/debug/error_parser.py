"""
Error Parser

Parses Python tracebacks to extract error information.
"""

import re
from dataclasses import dataclass
from typing import Optional


@dataclass
class ErrorInfo:
    """Parsed error information."""
    error_type: str
    message: str
    line_number: Optional[int]
    file_name: Optional[str]
    code_context: Optional[str]
    full_traceback: str


# Common Python error types and their patterns
ERROR_PATTERNS = {
    "SyntaxError": r"SyntaxError:\s*(.+)",
    "IndentationError": r"IndentationError:\s*(.+)",
    "NameError": r"NameError:\s*name '(\w+)' is not defined",
    "TypeError": r"TypeError:\s*(.+)",
    "ValueError": r"ValueError:\s*(.+)",
    "IndexError": r"IndexError:\s*(.+)",
    "KeyError": r"KeyError:\s*(.+)",
    "AttributeError": r"AttributeError:\s*(.+)",
    "ImportError": r"ImportError:\s*(.+)",
    "ModuleNotFoundError": r"ModuleNotFoundError:\s*(.+)",
    "ZeroDivisionError": r"ZeroDivisionError:\s*(.+)",
    "FileNotFoundError": r"FileNotFoundError:\s*(.+)",
    "RecursionError": r"RecursionError:\s*(.+)",
    "RuntimeError": r"RuntimeError:\s*(.+)",
}

# Pattern to extract line number from traceback
LINE_PATTERN = r'File "(.+?)", line (\d+)'
CODE_CONTEXT_PATTERN = r"^\s{4}(.+)$"


def parse_traceback(traceback_text: str) -> ErrorInfo:
    """
    Parse a Python traceback and extract error details.

    Args:
        traceback_text: The full traceback text

    Returns:
        ErrorInfo with parsed details
    """
    lines = traceback_text.strip().split("\n")

    # Find error type and message
    error_type = "UnknownError"
    message = ""

    for error_name, pattern in ERROR_PATTERNS.items():
        match = re.search(pattern, traceback_text)
        if match:
            error_type = error_name
            message = match.group(1) if match.groups() else ""
            break

    # If no specific pattern matched, try to extract from last line
    if error_type == "UnknownError" and lines:
        last_line = lines[-1]
        for known_error in ERROR_PATTERNS.keys():
            if known_error in last_line:
                error_type = known_error
                # Extract message after colon
                if ":" in last_line:
                    message = last_line.split(":", 1)[1].strip()
                break

    # Extract line number and file
    line_number = None
    file_name = None
    code_context = None

    line_matches = re.findall(LINE_PATTERN, traceback_text)
    if line_matches:
        # Get the last (most relevant) match
        file_name, line_str = line_matches[-1]
        line_number = int(line_str)

    # Extract code context (line following "File" line in traceback)
    for i, line in enumerate(lines):
        if "File" in line and "line" in line and i + 1 < len(lines):
            next_line = lines[i + 1]
            if next_line.strip() and not next_line.strip().startswith("File"):
                code_context = next_line.strip()

    return ErrorInfo(
        error_type=error_type,
        message=message,
        line_number=line_number,
        file_name=file_name,
        code_context=code_context,
        full_traceback=traceback_text,
    )


def get_error_explanation(error_type: str) -> str:
    """
    Get a beginner-friendly explanation of an error type.

    Args:
        error_type: The Python error type name

    Returns:
        Human-readable explanation
    """
    explanations = {
        "SyntaxError": (
            "Python couldn't understand your code because something is written incorrectly. "
            "Common causes: missing colons, unmatched brackets, or typos."
        ),
        "IndentationError": (
            "Python uses indentation (spaces at the start of lines) to understand code structure. "
            "Make sure your code is indented consistently with 4 spaces."
        ),
        "NameError": (
            "You're trying to use a variable or function that Python doesn't recognize. "
            "Check for typos or make sure you defined it before using it."
        ),
        "TypeError": (
            "You're trying to do an operation with the wrong type of data. "
            "For example, adding a string to a number without converting."
        ),
        "ValueError": (
            "The data you provided is the right type but wrong value. "
            "For example, trying to convert 'hello' to an integer."
        ),
        "IndexError": (
            "You're trying to access a position in a list that doesn't exist. "
            "Remember: Python counts from 0, and the last index is len(list) - 1."
        ),
        "KeyError": (
            "You're trying to access a dictionary key that doesn't exist. "
            "Check the key spelling or use .get() for safer access."
        ),
        "AttributeError": (
            "You're trying to use a method or property that doesn't exist on this object. "
            "Check the object type and available methods."
        ),
        "ImportError": (
            "Python can't find the module you're trying to import. "
            "Make sure the module name is correct and installed."
        ),
        "ZeroDivisionError": (
            "You can't divide by zero in mathematics or programming. "
            "Check your divisor and add a check to prevent zero division."
        ),
        "RecursionError": (
            "Your function calls itself too many times without stopping. "
            "Make sure you have a proper base case to end the recursion."
        ),
    }

    return explanations.get(
        error_type,
        f"A {error_type} occurred. Check the error message for details.",
    )


def suggest_common_fixes(error_type: str, message: str) -> list[str]:
    """
    Suggest common fixes based on error type and message.

    Args:
        error_type: The Python error type
        message: The error message

    Returns:
        List of suggested fixes
    """
    suggestions = []

    if error_type == "SyntaxError":
        if "EOL" in message:
            suggestions.append("Check if you closed all your quotes and parentheses")
        if "invalid syntax" in message:
            suggestions.append("Check the line above for missing colons or operators")
        suggestions.append("Make sure all brackets match: (), [], {}")

    elif error_type == "NameError":
        suggestions.append("Check the spelling of your variable name")
        suggestions.append("Make sure you defined the variable before using it")
        suggestions.append("Check if the variable is in the right scope")

    elif error_type == "TypeError":
        if "unsupported operand" in message:
            suggestions.append("Convert data types before operating: str(), int(), float()")
        if "argument" in message:
            suggestions.append("Check the number and types of arguments in your function call")

    elif error_type == "IndexError":
        suggestions.append("Check your loop bounds - are you going one past the end?")
        suggestions.append("Use len(list) to check the list size before accessing")
        suggestions.append("Remember: indices start at 0")

    elif error_type == "KeyError":
        suggestions.append("Use .get(key, default) instead of [key] for safer access")
        suggestions.append("Check if the key exists with 'if key in dict:'")
        suggestions.append("Print the dictionary keys to see what's available")

    return suggestions[:3]  # Return top 3 suggestions
