---
sidebar_position: 4
---

# Debug Service API

The Debug Service analyzes error messages, identifies root causes, and provides hints before revealing full solutions.

**Base URL:** `http://localhost:8004/api/v1`

## Endpoints

| Method | Path | Description |
|--------|------|-------------|
| GET | `/health` | Health check |
| POST | `/debug/analyze` | Analyze error and provide hints |
| POST | `/debug/solution` | Get complete solution explanation |

## POST /debug/analyze

Analyzes an error and provides pedagogical hints without revealing the solution.

**Request:**
```json
{
  "error_message": "TypeError: 'int' object is not subscriptable",
  "error_type": "TypeError",
  "code_context": "for item in numbers[i]:",
  "student_id": "student_123",
  "hint_level": 1
}
```

**Response (200 OK):**
```json
{
  "error_type": "TypeError",
  "root_cause": "Attempting to index an integer instead of a list",
  "hint_level": 1,
  "hints": [
    "What type is the variable 'numbers'?",
    "What type is the variable 'i'?"
  ],
  "diagnostic": {
    "likely_issue": "Using integer index as the iterable instead of the collection",
    "common_mistake": "Confusing 'numbers[i]' (an element) with 'numbers' (the list)"
  },
  "related_concepts": ["indexing", "iteration", "lists"],
  "attempt_count": 2,
  "next_hint_available": true
}
```

## POST /debug/solution

Provides complete solution explanation after student has attempted fixes or requested full help.

**Request:**
```json
{
  "error_message": "TypeError: 'int' object is not subscriptable",
  "error_type": "TypeError",
  "code_context": "for item in numbers[i]:",
  "student_id": "student_123",
  "attempt_count": 3
}
```

**Response (200 OK):**
```json
{
  "error_type": "TypeError",
  "explanation": "You're trying to index an integer. This error occurs when...",
  "root_cause": "Variable 'i' is an integer, not a subscriptable object",
  "common_causes": [
    "Using a number instead of a collection in brackets",
    "Confusing the index with the value"
  ],
  "correct_approach": "Iterate directly over the collection, not the index",
  "corrected_code": "for item in numbers:\n    print(item)",
  "explanation_detail": "When iterating, use 'for item in list' not 'for item in list[i]'",
  "similar_errors": [
    {"error": "TypeError: 'str' object is not subscriptable", "cause": "Same pattern with strings"},
    {"error": "IndexError: list index out of range", "cause": "Index too large"}
  ],
  "resources": ["iteration", "list_comprehension", "enumerate"]
}
```

## Error Responses

**400 Bad Request:**
```json
{
  "error": "Invalid error type",
  "valid_types": ["TypeError", "ValueError", "NameError", "IndexError", "SyntaxError"]
}
```

**404 Not Found:**
```json
{
  "error": "Error pattern not recognized",
  "message": "Unable to analyze this error type"
}
```
