---
sidebar_position: 3
---

# Code Runner Service API

The Code Runner Service executes Python code in a sandboxed environment with strict resource limits.

**Base URL:** `http://localhost:8003/api/v1`

## Endpoints

| Method | Path | Description |
|--------|------|-------------|
| GET | `/health` | Health check |
| POST | `/code/execute` | Execute Python code safely |

## POST /code/execute

Executes user-submitted Python code in an isolated sandbox environment.

**Sandbox Constraints:**
- Timeout: 5 seconds
- Memory: 50 MB
- No network access
- Standard library only (MVP)

**Request:**
```json
{
  "code": "def fibonacci(n):\n    if n <= 1:\n        return n\n    return fibonacci(n-1) + fibonacci(n-2)\n\nprint(fibonacci(10))",
  "student_id": "student_123",
  "execution_id": "exec_456",
  "timeout_seconds": 5
}
```

**Response (200 OK - Success):**
```json
{
  "execution_id": "exec_456",
  "status": "success",
  "output": "55",
  "stderr": "",
  "execution_time_ms": 125,
  "memory_used_mb": 8.5,
  "exit_code": 0
}
```

**Response (200 OK - Runtime Error):**
```json
{
  "execution_id": "exec_456",
  "status": "error",
  "output": "",
  "stderr": "Traceback (most recent call last):\n  File \"<stdin>\", line 2, in <module>\nTypeError: unsupported operand type(s) for +: 'str' and 'int'",
  "execution_time_ms": 42,
  "memory_used_mb": 2.1,
  "exit_code": 1,
  "error_type": "TypeError",
  "error_line": 2
}
```

**Response (408 Timeout):**
```json
{
  "execution_id": "exec_456",
  "status": "timeout",
  "output": "Partial output before timeout...",
  "error": "Code execution exceeded 5 second timeout",
  "execution_time_ms": 5000
}
```

## Error Responses

**413 Payload Too Large:**
```json
{
  "error": "Code exceeds maximum size",
  "max_size_bytes": 10000,
  "received_bytes": 15000
}
```

**400 Bad Request:**
```json
{
  "error": "Invalid code format",
  "details": "Code field is required and must be a string"
}
```
