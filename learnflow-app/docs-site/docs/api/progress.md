---
sidebar_position: 6
---

# Progress Service API

The Progress Service tracks student mastery across topics and provides detailed performance analytics.

**Base URL:** `http://localhost:8006/api/v1`

## Endpoints

| Method | Path | Description |
|--------|------|-------------|
| GET | `/health` | Health check |
| GET | `/progress/:student_id` | Get overall progress summary |
| GET | `/progress/:student_id/topic/:topic_id` | Get topic-specific mastery |
| GET | `/progress/:student_id/topics` | List all topics with mastery levels |

## GET /progress/:student_id

Retrieves overall progress summary for a student across all topics.

**Response (200 OK):**
```json
{
  "student_id": "student_123",
  "overall_mastery": 72.5,
  "mastery_level": "proficient",
  "topics_completed": 8,
  "total_topics": 24,
  "exercises_completed": 32,
  "total_exercises": 85,
  "quiz_average": 78,
  "streak": 12,
  "total_learning_hours": 24.5,
  "recent_activity": "2025-02-03T14:30:00Z",
  "summary": {
    "beginner_topics": {
      "mastered": 5,
      "proficient": 2,
      "learning": 1,
      "beginner": 0
    },
    "intermediate_topics": {
      "mastered": 2,
      "proficient": 3,
      "learning": 4,
      "beginner": 1
    }
  }
}
```

## GET /progress/:student_id/topic/:topic_id

Retrieves detailed mastery data for a specific topic.

**Response (200 OK):**
```json
{
  "student_id": "student_123",
  "topic_id": "list_comprehension",
  "topic_name": "List Comprehensions",
  "mastery_percentage": 85,
  "mastery_level": "proficient",
  "breakdown": {
    "exercise_completion": 35,
    "quiz_scores": 27,
    "code_quality": 18,
    "consistency_streak": 5
  },
  "exercises": {
    "completed": 5,
    "total": 6,
    "average_score": 88
  },
  "quizzes": {
    "completed": 2,
    "total": 2,
    "average_score": 92
  },
  "code_quality_ratings": [
    {"submission_id": "sub_456", "rating": 85, "feedback": "Good"},
    {"submission_id": "sub_457", "rating": 95, "feedback": "Excellent"}
  ],
  "learning_streak": 7,
  "last_activity": "2025-02-03T14:30:00Z",
  "estimated_mastery_date": "2025-02-10T00:00:00Z"
}
```

## GET /progress/:student_id/topics

Lists all topics with the student's mastery level in each.

**Response (200 OK):**
```json
{
  "student_id": "student_123",
  "topics": [
    {
      "topic_id": "variables",
      "name": "Variables & Data Types",
      "mastery_percentage": 95,
      "mastery_level": "mastered",
      "color": "blue",
      "exercises_completed": 6,
      "last_activity": "2025-02-02T10:15:00Z"
    },
    {
      "topic_id": "loops",
      "name": "For and While Loops",
      "mastery_percentage": 78,
      "mastery_level": "proficient",
      "color": "green",
      "exercises_completed": 5,
      "last_activity": "2025-02-03T14:30:00Z"
    },
    {
      "topic_id": "functions",
      "name": "Functions and Scope",
      "mastery_percentage": 45,
      "mastery_level": "learning",
      "color": "yellow",
      "exercises_completed": 2,
      "last_activity": "2025-02-01T16:45:00Z"
    }
  ],
  "total_topics": 24,
  "mastery_distribution": {
    "mastered": 3,
    "proficient": 5,
    "learning": 4,
    "beginner": 12
  },
  "sorted_by": "last_activity"
}
```

## Mastery Calculation Formula

```
Topic Mastery =
  (Exercise Completion × 0.40) +
  (Quiz Scores × 0.30) +
  (Code Quality × 0.20) +
  (Consistency/Streak × 0.10)
```

### Mastery Levels

| Range | Level | Color |
|-------|-------|-------|
| 0-40% | Beginner | Red |
| 41-70% | Learning | Yellow |
| 71-90% | Proficient | Green |
| 91-100% | Mastered | Blue |

## Error Responses

**404 Not Found:**
```json
{
  "error": "Student not found",
  "student_id": "student_999"
}
```

**400 Bad Request:**
```json
{
  "error": "Invalid topic ID",
  "topic_id": "unknown_topic"
}
```
