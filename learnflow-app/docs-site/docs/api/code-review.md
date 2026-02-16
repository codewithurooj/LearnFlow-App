---
sidebar_position: 7
---

# Code Review Service API

The Code Review Service analyzes submitted code for correctness, style compliance, efficiency, and best practices.

**Base URL:** `http://localhost:8007/api/v1`

## Endpoints

| Method | Path | Description |
|--------|------|-------------|
| GET | `/health` | Health check |
| POST | `/review/analyze` | Analyze code quality |

## POST /review/analyze

Performs comprehensive code review including style, efficiency, and best practices.

**Request:**
```json
{
  "code": "def factorial(n):\n    if n<=1:\n        return 1\n    else:\n        return n*factorial(n-1)",
  "student_id": "student_123",
  "topic": "recursion",
  "reference_standard": "pep8"
}
```

**Response (200 OK):**
```json
{
  "student_id": "student_123",
  "review_id": "rev_123",
  "overall_score": 78,
  "summary": "Good implementation but needs style improvements",
  "analysis": {
    "correctness": {
      "score": 95,
      "status": "passed",
      "issues": []
    },
    "style": {
      "score": 65,
      "status": "issues_found",
      "issues": [
        {
          "line": 2,
          "issue": "Missing spaces around operators",
          "pattern": "n<=1",
          "suggestion": "n <= 1",
          "severity": "minor"
        },
        {
          "line": 1,
          "issue": "Missing docstring",
          "suggestion": "Add a docstring explaining function purpose",
          "severity": "minor"
        }
      ]
    },
    "efficiency": {
      "score": 60,
      "status": "issues_found",
      "issues": [
        {
          "type": "performance_concern",
          "issue": "Recursive solution has exponential time complexity",
          "severity": "major",
          "suggestion": "Consider iterative approach or memoization for better performance"
        }
      ]
    },
    "best_practices": {
      "score": 85,
      "status": "minor_issues",
      "recommendations": [
        "Consider adding input validation to check n >= 0",
        "Add type hints for better code documentation"
      ]
    }
  },
  "improved_code": "def factorial(n: int) -> int:\n    \"\"\"Calculate the factorial of n using recursion.\"\"\"\n    if n < 0:\n        raise ValueError('n must be non-negative')\n    if n <= 1:\n        return 1\n    return n * factorial(n - 1)",
  "learning_resources": [
    {"topic": "recursion", "url": "/docs/api/concepts#recursion"},
    {"topic": "time_complexity", "url": "/docs/api/concepts#complexity"}
  ]
}
```

**Response (200 OK - Excellent Code):**
```json
{
  "student_id": "student_123",
  "review_id": "rev_124",
  "overall_score": 96,
  "summary": "Excellent code quality! Well-structured and efficient.",
  "analysis": {
    "correctness": {
      "score": 100,
      "status": "passed",
      "issues": []
    },
    "style": {
      "score": 98,
      "status": "passed",
      "issues": []
    },
    "efficiency": {
      "score": 94,
      "status": "passed",
      "issues": []
    },
    "best_practices": {
      "score": 100,
      "status": "passed",
      "recommendations": []
    }
  },
  "feedback": "This is high-quality code that demonstrates mastery. Consider exploring related advanced patterns.",
  "next_challenges": [
    "Decorator patterns",
    "Generator functions",
    "Advanced list comprehensions"
  ]
}
```

## Scoring Breakdown

| Category | Weight | Criteria |
|----------|--------|----------|
| **Correctness** | 40% | Logic correctness, edge case handling |
| **Style** | 20% | PEP 8 compliance, formatting, naming |
| **Efficiency** | 25% | Time/space complexity, optimization |
| **Best Practices** | 15% | Documentation, error handling, maintainability |

## Error Responses

**400 Bad Request:**
```json
{
  "error": "Invalid code format",
  "details": "Code contains syntax errors and cannot be analyzed"
}
```

**413 Payload Too Large:**
```json
{
  "error": "Code exceeds maximum size",
  "max_size_bytes": 10000
}
```

**500 Internal Server Error:**
```json
{
  "error": "Review analysis failed",
  "review_id": "rev_123",
  "message": "Unable to complete code analysis"
}
```
