---
sidebar_position: 1
---

# Triage Service API

The Triage Service routes student questions to appropriate specialist agents based on query classification.

**Base URL:** `http://localhost:8001/api/v1`

## Endpoints

| Method | Path | Description |
|--------|------|-------------|
| GET | `/health` | Health check |
| POST | `/triage/classify` | Classify incoming question |
| POST | `/triage/route` | Route to specialist agent |

## POST /triage/classify

Analyzes a student question and determines its category.

**Request:**
```json
{
  "question": "How do I fix this TypeError: 'int' object is not subscriptable?",
  "student_id": "student_123",
  "context": "In a for loop processing a list"
}
```

**Response (200 OK):**
```json
{
  "classification": "debug",
  "confidence": 0.92,
  "category": "error_analysis",
  "specialist": "debug_agent",
  "reasoning": "Error message detected with TypeError"
}
```

## POST /triage/route

Routes the classified question to the appropriate specialist service.

**Request:**
```json
{
  "classification": "debug",
  "question": "Why is my list returning an error?",
  "student_id": "student_123"
}
```

**Response (200 OK):**
```json
{
  "routed_to": "debug_agent",
  "service_url": "http://localhost:8004/api/v1",
  "request_id": "req_12345",
  "status": "routed"
}
```

## Error Responses

**400 Bad Request:**
```json
{
  "error": "Invalid question format",
  "details": "Question field is required"
}
```

**500 Internal Server Error:**
```json
{
  "error": "Classification failed",
  "request_id": "req_12345"
}
```
