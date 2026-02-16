---
sidebar_position: 5
---

# Exercise Service API

The Exercise Service generates coding challenges, auto-grades submissions, and provides feedback.

**Base URL:** `http://localhost:8005/api/v1`

## Endpoints

| Method | Path | Description |
|--------|------|-------------|
| GET | `/health` | Health check |
| GET | `/exercises/generate` | Generate a new exercise |
| POST | `/exercises/submit` | Submit solution for grading |
| GET | `/exercises/topics` | List available exercise topics |

## GET /exercises/generate

Generates a new coding exercise adapted to the student's skill level.

**Query Parameters:**
- `topic` (required): Exercise topic
- `student_id` (required): Student identifier
- `difficulty` (optional): "beginner", "intermediate", or "advanced"

**Request:** `GET /exercises/generate?topic=loops&student_id=student_123&difficulty=intermediate`

**Response (200 OK):**
```json
{
  "exercise_id": "ex_789",
  "topic": "loops",
  "difficulty": "intermediate",
  "title": "Sum Even Numbers",
  "description": "Write a function that returns the sum of all even numbers in a list",
  "requirements": [
    "Use a for loop to iterate through the list",
    "Check if each number is even",
    "Return the sum"
  ],
  "starter_code": "def sum_even_numbers(numbers):\n    total = 0\n    # TODO: implement\n    return total",
  "test_cases": [
    {"input": "[1, 2, 3, 4, 5, 6]", "expected_output": "12"},
    {"input": "[1, 3, 5]", "expected_output": "0"},
    {"input": "[]", "expected_output": "0"}
  ],
  "hints": [
    "Use the modulo operator (%) to check if a number is even",
    "A number is even if n % 2 == 0"
  ]
}
```

## POST /exercises/submit

Submits a solution for auto-grading and receives feedback.

**Request:**
```json
{
  "exercise_id": "ex_789",
  "student_id": "student_123",
  "solution_code": "def sum_even_numbers(numbers):\n    total = 0\n    for n in numbers:\n        if n % 2 == 0:\n            total += n\n    return total",
  "submission_time_seconds": 240
}
```

**Response (200 OK - All Tests Pass):**
```json
{
  "submission_id": "sub_456",
  "exercise_id": "ex_789",
  "status": "passed",
  "score": 100,
  "test_results": [
    {
      "test_case": 1,
      "input": "[1, 2, 3, 4, 5, 6]",
      "expected": "12",
      "actual": "12",
      "passed": true
    },
    {
      "test_case": 2,
      "input": "[1, 3, 5]",
      "expected": "0",
      "actual": "0",
      "passed": true
    },
    {
      "test_case": 3,
      "input": "[]",
      "expected": "0",
      "actual": "0",
      "passed": true
    }
  ],
  "feedback": "Excellent! Your solution is correct and efficient.",
  "code_quality": {
    "pep8_compliant": true,
    "readable": true,
    "efficient": true,
    "suggestions": []
  },
  "mastery_gain": 8.5
}
```

**Response (200 OK - Partial Pass):**
```json
{
  "submission_id": "sub_457",
  "exercise_id": "ex_789",
  "status": "partial",
  "score": 66,
  "test_results": [
    {"test_case": 1, "passed": true},
    {"test_case": 2, "passed": false, "expected": "0", "actual": "3"},
    {"test_case": 3, "passed": true}
  ],
  "feedback": "Good progress! One test case is failing. Check the logic for the case when no even numbers exist.",
  "code_quality": {
    "pep8_compliant": true,
    "readable": true,
    "suggestions": ["Consider using sum() with a generator expression"]
  }
}
```

## GET /exercises/topics

Lists available exercise topics organized by difficulty.

**Response (200 OK):**
```json
{
  "topics": [
    {
      "id": "variables",
      "name": "Variables & Assignment",
      "difficulty": "beginner",
      "exercise_count": 5
    },
    {
      "id": "loops",
      "name": "For and While Loops",
      "difficulty": "intermediate",
      "exercise_count": 8
    }
  ],
  "total": 32,
  "by_difficulty": {
    "beginner": 12,
    "intermediate": 15,
    "advanced": 5
  }
}
```

## Error Responses

**400 Bad Request:**
```json
{
  "error": "Missing required parameter",
  "missing": ["student_id"]
}
```

**404 Not Found:**
```json
{
  "error": "Exercise not found",
  "exercise_id": "ex_999"
}
```
