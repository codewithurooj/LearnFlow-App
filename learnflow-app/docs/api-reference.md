# LearnFlow API Reference

All services expose interactive OpenAPI docs at `/docs` (Swagger UI) and `/redoc` (ReDoc).

Base URLs (local development):

| Service | URL |
|---------|-----|
| Triage | `http://localhost:8001/api/v1` |
| Concepts | `http://localhost:8002/api/v1` |
| Code Runner | `http://localhost:8003/api/v1` |
| Debug | `http://localhost:8004/api/v1` |
| Exercise | `http://localhost:8005/api/v1` |
| Progress | `http://localhost:8006/api/v1` |
| Code Review | `http://localhost:8007/api/v1` |

---

## Triage Service (port 8001)

Routes student questions to the appropriate specialist agent.

### `POST /triage/classify`

Classify a question without routing.

**Request:**
```json
{
  "student_id": "uuid",
  "question": "string (1-5000 chars)",
  "session_id": "uuid (optional)",
  "mastery_level": "Beginner | Learning | Proficient | Mastered"
}
```

**Response:**
```json
{
  "routed_to": "concepts | debug | code_review | exercise | progress",
  "confidence": 0.92,
  "method": "keyword | ai | hybrid",
  "keywords_matched": ["explain"],
  "clarifying_question": "string | null"
}
```

### `POST /triage/route`

Classify and route to specialist, returning the specialist's response.

**Response:**
```json
{
  "routed_to": "concepts",
  "confidence": 0.92,
  "response": "string",
  "sources": ["string"],
  "processing_time_ms": 245
}
```

---

## Concepts Service (port 8002)

Explains Python concepts adapted to student mastery level.

### `POST /concepts/explain`

**Request:**
```json
{
  "student_id": "uuid",
  "topic": "string (1-500 chars)",
  "mastery_level": "Beginner (default)",
  "context": [{"role": "user", "content": "..."}]
}
```

**Response:**
```json
{
  "explanation": "string",
  "code_examples": [
    { "title": "string", "code": "string", "explanation": "string" }
  ],
  "related_topics": ["lists", "tuples"],
  "difficulty_adapted": true
}
```

### `GET /concepts/topics`

Returns available Python topics grouped by category.

---

## Code Runner Service (port 8003)

Executes Python code in a secure sandbox (5s timeout, 50MB memory, no network).

### `POST /code/execute`

**Request:**
```json
{
  "student_id": "uuid",
  "code": "string (1-50000 chars)",
  "exercise_id": "uuid (optional)"
}
```

**Response:**
```json
{
  "stdout": "Hello World\n",
  "stderr": "",
  "exit_code": 0,
  "execution_time_ms": 42,
  "memory_used_mb": 12.5,
  "timed_out": false,
  "error_type": "null | SyntaxError | TypeError | ..."
}
```

**Side effects:** Publishes `code.results` event. If 5+ consecutive failures, publishes `struggle.detected`.

---

## Debug Service (port 8004)

Parses errors, identifies root causes, provides hints before solutions.

### `POST /debug/analyze`

**Request:**
```json
{
  "student_id": "uuid",
  "code": "string",
  "error_output": "string",
  "traceback": "string (optional)"
}
```

**Response:**
```json
{
  "error_type": "TypeError",
  "error_line": 5,
  "root_cause": "string",
  "hint": "string",
  "solution": "string | null",
  "struggle_detected": false
}
```

### `POST /debug/solution`

Returns full solution with corrected code (only after hint was shown).

**Response:**
```json
{
  "solution": "string",
  "corrected_code": "string"
}
```

---

## Exercise Service (port 8005)

Generates and grades coding exercises.

### `GET /exercises/generate?student_id={uuid}&topic={string}&difficulty={string}`

Generates a new exercise.

**Response:**
```json
{
  "exercise_id": "uuid",
  "title": "string",
  "description": "string",
  "starter_code": "def solution():\n    pass",
  "expected_output_hint": "string | null"
}
```

### `POST /exercises/submit`

Submit solution for grading.

**Request:**
```json
{
  "student_id": "uuid",
  "exercise_id": "uuid",
  "code": "string"
}
```

**Response:**
```json
{
  "passed": true,
  "score": 0.85,
  "test_results": [
    { "name": "test_basic", "passed": true, "message": "" }
  ],
  "feedback": "string",
  "time_spent_seconds": 120
}
```

### `GET /exercises/topics`

Returns available exercise topics grouped by difficulty.

---

## Progress Service (port 8006)

Tracks mastery scores across all topics.

### `GET /progress/{student_id}`

**Response:**
```json
{
  "student_id": "uuid",
  "overall_mastery": 72.5,
  "overall_level": "Proficient",
  "topics": [
    {
      "topic_id": "variables",
      "topic_name": "Variables",
      "mastery_score": 85.0,
      "mastery_level": "Proficient",
      "level_color": "green"
    }
  ],
  "current_streak": 5,
  "last_activity": "2026-02-03T10:00:00Z",
  "total_exercises": 15,
  "total_quizzes": 8
}
```

### `GET /progress/{student_id}/topic/{topic_id}`

Returns detailed mastery breakdown for a single topic.

**Response:**
```json
{
  "topic_id": "variables",
  "topic_name": "Variables",
  "mastery_score": 85.0,
  "mastery_level": "Proficient",
  "level_color": "green",
  "breakdown": {
    "exercises_score": 0.8,
    "quizzes_score": 0.7,
    "code_quality_score": 0.9,
    "streak_bonus": 0.5,
    "exercises_completed": 5,
    "quizzes_taken": 3
  },
  "improvement_suggestions": ["string"],
  "last_activity": "2026-02-03T10:00:00Z"
}
```

### `GET /progress/{student_id}/topics`

Returns topics grouped by mastery level (`Mastered`, `Proficient`, `Learning`, `Beginner`).

---

## Code Review Service (port 8007)

Analyzes code for correctness, style (PEP 8), efficiency, and readability.

### `POST /review/analyze`

**Request:**
```json
{
  "student_id": "uuid",
  "code": "string (1-10000 chars)",
  "context": "string (optional)"
}
```

**Response:**
```json
{
  "rating": 4,
  "correctness": { "score": 5, "feedback": "string" },
  "style": { "score": 3, "feedback": "string" },
  "efficiency": { "score": 4, "feedback": "string" },
  "readability": { "score": 4, "feedback": "string" },
  "strengths": ["Good variable names"],
  "suggestions": ["Add docstrings"],
  "encouragement": "string"
}
```

---

## Common

### Health Check (all services)

`GET /health`

```json
{
  "status": "healthy | degraded",
  "service": "string",
  "version": "1.0.0",
  "dapr_connected": true
}
```

### Mastery Levels

| Score | Level | Color |
|-------|-------|-------|
| 0-40% | Beginner | Red |
| 41-70% | Learning | Yellow |
| 71-90% | Proficient | Green |
| 91-100% | Mastered | Blue |

### Kafka Events (Dapr pub/sub)

| Topic | Publisher | Schema |
|-------|----------|--------|
| `learning.questions` | Frontend | `QuestionEvent` |
| `learning.responses` | Triage | `ResponseEvent` |
| `code.submissions` | Frontend | `CodeSubmissionEvent` |
| `code.results` | Code Runner | `CodeResultEvent` |
| `struggle.detected` | Debug, Code Runner, Progress | `StruggleDetectedEvent` |
| `progress.updated` | Progress | `ProgressUpdatedEvent` |
