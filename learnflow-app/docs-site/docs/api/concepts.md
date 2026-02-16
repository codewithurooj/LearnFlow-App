---
sidebar_position: 2
---

# Concepts Service API

The Concepts Service explains Python concepts, provides examples, and adapts explanations to student skill levels.

**Base URL:** `http://localhost:8002/api/v1`

## Endpoints

| Method | Path | Description |
|--------|------|-------------|
| GET | `/health` | Health check |
| POST | `/concepts/explain` | Explain a Python concept |
| GET | `/concepts/topics` | List available topics |

## POST /concepts/explain

Provides an adaptive explanation of a Python concept with examples.

**Request:**
```json
{
  "topic": "list_comprehension",
  "student_id": "student_123",
  "skill_level": "intermediate",
  "examples_count": 2
}
```

**Response (200 OK):**
```json
{
  "topic": "list_comprehension",
  "explanation": "A list comprehension is a concise way to create lists...",
  "examples": [
    {
      "code": "[x*2 for x in range(5)]",
      "output": "[0, 2, 4, 6, 8]",
      "explanation": "Creates a new list by multiplying each number by 2"
    },
    {
      "code": "[x for x in range(10) if x % 2 == 0]",
      "output": "[0, 2, 4, 6, 8]",
      "explanation": "Filters to include only even numbers"
    }
  ],
  "difficulty": "intermediate",
  "related_topics": ["lists", "loops", "lambda"],
  "mastery_hint": "Practice with nested list comprehensions next"
}
```

## GET /concepts/topics

Lists all available Python concepts organized by difficulty level.

**Response (200 OK):**
```json
{
  "topics": [
    {
      "id": "variables",
      "name": "Variables & Data Types",
      "difficulty": "beginner",
      "description": "Learn about Python's data types and variable assignment"
    },
    {
      "id": "list_comprehension",
      "name": "List Comprehensions",
      "difficulty": "intermediate",
      "description": "Master concise list creation patterns"
    }
  ],
  "total": 24,
  "grouped_by_difficulty": {
    "beginner": 8,
    "intermediate": 10,
    "advanced": 6
  }
}
```

## Error Responses

**404 Not Found:**
```json
{
  "error": "Topic not found",
  "topic": "unknown_topic"
}
```

**400 Bad Request:**
```json
{
  "error": "Invalid skill level",
  "valid_levels": ["beginner", "intermediate", "advanced"]
}
```
