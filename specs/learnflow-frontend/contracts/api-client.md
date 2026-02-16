# API Contracts: LearnFlow Frontend → Backend Services

**Date**: 2026-02-14

## Base Configuration

```
NEXT_PUBLIC_API_URL = http://localhost:8001  (in docker-compose)
```

For MVP, the frontend calls backend services directly by port. In production, Kong API Gateway routes all traffic.

## Service Endpoints Consumed by Frontend

### 1. Triage Service (port 8001)

**Chat - Route Question**
```
POST /api/v1/triage/route
Content-Type: application/json

Request:
{
  "student_id": "uuid",
  "question": "string (1-5000 chars)",
  "session_id": "string (optional)",
  "mastery_level": "string (optional)"
}

Response 200:
{
  "routed_to": "concepts|debug|code_review|exercise|progress",
  "confidence": 0.95,
  "response": "markdown string",
  "sources": ["string"],
  "processing_time_ms": 1200
}
```

### 2. Concepts Service (port 8002)

**Explain Topic**
```
POST /api/v1/concepts/explain
Content-Type: application/json

Request:
{
  "student_id": "uuid",
  "topic": "string (1-500 chars)",
  "mastery_level": "Beginner|Learning|Proficient|Mastered (optional)",
  "context": "string (optional)"
}

Response 200:
{
  "explanation": "markdown string",
  "code_examples": [
    { "title": "string", "code": "string", "explanation": "string" }
  ],
  "related_topics": ["string"],
  "difficulty_adapted": true
}
```

**List Topics**
```
GET /api/v1/concepts/topics

Response 200:
{
  "basics": ["variables", "data_types", ...],
  "control_flow": ["if_else", "loops", ...],
  ...
}
```

### 3. Code Runner Service (port 8003)

**Execute Code**
```
POST /api/v1/code/execute
Content-Type: application/json

Request:
{
  "student_id": "uuid",
  "code": "string (1-50000 chars)",
  "exercise_id": "string (optional)"
}

Response 200:
{
  "stdout": "string",
  "stderr": "string",
  "exit_code": 0,
  "execution_time_ms": 150,
  "memory_used_mb": 5.2,
  "timed_out": false,
  "error_type": "SyntaxError (optional)"
}
```

### 4. Debug Service (port 8004)

**Analyze Error**
```
POST /api/v1/debug/analyze
Content-Type: application/json

Request:
{
  "student_id": "uuid",
  "code": "string",
  "error_output": "string",
  "traceback": "string (optional)"
}

Response 200:
{
  "error_type": "SyntaxError",
  "error_line": 5,
  "root_cause": "string",
  "hint": "string",
  "solution": "string (optional)",
  "struggle_detected": false
}
```

**Get Full Solution**
```
POST /api/v1/debug/solution

Request: (same as analyze)

Response 200:
{
  "solution": "markdown string",
  "corrected_code": "string"
}
```

### 5. Exercise Service (port 8005)

**Generate Exercise**
```
GET /api/v1/exercises/generate?student_id=uuid&topic=loops&difficulty=beginner

Response 200:
{
  "exercise_id": "uuid",
  "title": "string",
  "description": "markdown string",
  "starter_code": "string (optional)",
  "expected_output_hint": "string (optional)"
}
```

**Submit Solution**
```
POST /api/v1/exercises/submit
Content-Type: application/json

Request:
{
  "student_id": "uuid",
  "exercise_id": "uuid",
  "code": "string"
}

Response 200:
{
  "passed": true,
  "score": 0.85,
  "test_results": [
    { "name": "test_basic", "passed": true, "message": null }
  ],
  "feedback": "markdown string",
  "time_spent_seconds": 120
}
```

**List Topics**
```
GET /api/v1/exercises/topics

Response 200:
{
  "beginner": ["variables", "strings", ...],
  "intermediate": ["list_comprehensions", ...],
  "advanced": ["decorators", ...]
}
```

### 6. Progress Service (port 8006)

**Get Summary**
```
GET /api/v1/progress/{student_id}

Response 200:
{
  "student_id": "uuid",
  "overall_mastery": 65.5,
  "overall_level": "Learning",
  "topics": [
    {
      "topic_id": "string",
      "topic_name": "Variables",
      "mastery_score": 85.0,
      "mastery_level": "Proficient",
      "level_color": "#22c55e"
    }
  ],
  "current_streak": 5,
  "last_activity": "2026-02-14T10:00:00Z",
  "total_exercises": 42,
  "total_quizzes": 15
}
```

**Get Topic Detail**
```
GET /api/v1/progress/{student_id}/topic/{topic_id}

Response 200:
{
  "topic_id": "string",
  "topic_name": "Variables",
  "mastery_score": 85.0,
  "mastery_level": "Proficient",
  "level_color": "#22c55e",
  "breakdown": {
    "exercises": 90.0,
    "quizzes": 80.0,
    "code_quality": 75.0,
    "streak": 100.0
  },
  "improvement_suggestions": ["string"],
  "last_activity": "2026-02-14T10:00:00Z"
}
```

### 7. Code Review Service (port 8007)

**Analyze Code**
```
POST /api/v1/review/analyze
Content-Type: application/json

Request:
{
  "student_id": "uuid",
  "code": "string (1-10000 chars)",
  "context": "string (optional)"
}

Response 200:
{
  "rating": 4,
  "correctness": { "score": 5, "feedback": "string" },
  "style": { "score": 3, "feedback": "string" },
  "efficiency": { "score": 4, "feedback": "string" },
  "readability": { "score": 4, "feedback": "string" },
  "strengths": ["string"],
  "suggestions": ["string"],
  "encouragement": "string"
}
```

### 8. MCP Context Server (port 8008) — Teacher Dashboard Only

**Class Overview**
```
GET /api/v1/context/class/overview

Response 200:
{
  "total_students": 30,
  "active_students": 25,
  "average_mastery": 55.0,
  "topic_distribution": { "Beginner": 10, "Learning": 12, ... },
  "recent_struggles": [
    {
      "student_id": "uuid",
      "student_name": "string",
      "struggle_type": "repeated_error",
      "confidence": 0.85,
      "timestamp": "2026-02-14T10:00:00Z"
    }
  ]
}
```

**Student Struggles**
```
GET /api/v1/context/student/{student_id}/struggles

Response 200:
{
  "struggles": [...],
  "patterns": [...]
}
```

## Error Responses (All Services)

```
Response 422 (Validation Error):
{
  "detail": [
    { "loc": ["body", "code"], "msg": "string", "type": "value_error" }
  ]
}

Response 500 (Server Error):
{
  "detail": "Internal server error"
}
```

## CORS

All backend services include CORS middleware allowing cross-origin requests. In docker-compose, the frontend (port 3000) communicates with backends on their respective ports.
