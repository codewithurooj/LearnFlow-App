# Implementation Plan: LearnFlow Backend Microservices

**Branch**: `003-learnflow-backend` | **Date**: 2026-01-26 | **Spec**: [spec.md](./spec.md)
**Input**: Feature specification from `specs/learnflow-backend/spec.md`

## Summary

Build 6 FastAPI microservices forming the LearnFlow backend: Triage (8001), Concepts (8002), Code Runner (8003), Debug (8004), Exercise (8005), and Progress (8006). Each service runs with a Dapr sidecar for pub/sub (Kafka), state management (PostgreSQL), and service invocation. AI agents use OpenAI SDK with gpt-4o-mini for cost-efficient LLM interactions.

## Technical Context

**Language/Version**: Python 3.11+, FastAPI 0.100+, Pydantic v2
**Primary Dependencies**: FastAPI, uvicorn, openai, dapr-ext-fastapi, pydantic, RestrictedPython
**Storage**: PostgreSQL via Dapr state store; Kafka via Dapr pub/sub
**Testing**: pytest, httpx (for async test client)
**Target Platform**: Kubernetes (Minikube), Docker containers with Dapr sidecars
**Project Type**: Microservices (6 independent services)
**Performance Goals**: < 3s response for simple queries, 50 concurrent requests, < 3GB total RAM
**Constraints**: Sandbox: 5s timeout, 50MB memory, no network; stateless services
**Scale/Scope**: 6 services, ~30 endpoints, ~20 Pydantic models, 6 Dockerfiles

## Constitution Check

| Principle | Status | Notes |
|-----------|--------|-------|
| I. Skills-First | PASS | Services scaffolded via fastapi-dapr-agent skill |
| II. Token Efficiency | PASS | Skill-based scaffolding, not manual coding |
| III. Cloud-Native | PASS | Docker containers on K8s with Dapr sidecars |
| IV. Microservices | PASS | 6 independent services with Kafka pub/sub |
| V. Security | PASS | Sandboxed code execution, JWT auth, no hardcoded secrets |
| VI. SDD | PASS | Spec → Plan → Tasks workflow |
| VII. Cross-Agent | PASS | Standard Python/FastAPI, no agent-specific code |
| VIII. Observability | PASS | /health endpoints, structured JSON logs |

## Project Structure

### Documentation (this feature)

```text
specs/learnflow-backend/
├── plan.md              # This file
├── tasks.md             # Implementation tasks
├── checklists/
│   └── requirements.md  # Quality checklist
```

### Source Code

```text
learnflow-app/backend/
├── shared/
│   ├── models.py            # Shared Pydantic models
│   ├── dapr_utils.py        # Dapr pub/sub and state helpers
│   ├── config.py            # Environment configuration
│   └── logging_config.py    # Structured JSON logging setup
├── triage-service/
│   ├── main.py              # FastAPI app, routing logic
│   ├── router.py            # Query classification (keywords + LLM)
│   ├── models.py            # Service-specific models
│   ├── Dockerfile
│   └── requirements.txt
├── concepts-service/
│   ├── main.py              # FastAPI app
│   ├── agent.py             # OpenAI SDK agent with system prompt
│   ├── prompts/
│   │   └── concepts.md      # External system prompt
│   ├── models.py
│   ├── Dockerfile
│   └── requirements.txt
├── code-runner-service/
│   ├── main.py              # FastAPI app
│   ├── sandbox.py           # RestrictedPython + subprocess sandbox
│   ├── models.py
│   ├── Dockerfile
│   └── requirements.txt
├── debug-service/
│   ├── main.py              # FastAPI app
│   ├── agent.py             # OpenAI SDK agent with debug prompt
│   ├── parser.py            # Traceback parser
│   ├── struggle.py          # Sliding window struggle detector
│   ├── prompts/
│   │   └── debug.md
│   ├── models.py
│   ├── Dockerfile
│   └── requirements.txt
├── exercise-service/
│   ├── main.py              # FastAPI app
│   ├── agent.py             # OpenAI SDK agent for generation
│   ├── grader.py            # Auto-grading with test cases
│   ├── prompts/
│   │   └── exercise.md
│   ├── models.py
│   ├── Dockerfile
│   └── requirements.txt
├── progress-service/
│   ├── main.py              # FastAPI app
│   ├── mastery.py           # Weighted formula + EMA calculation
│   ├── milestones.py        # Milestone detection
│   ├── models.py
│   ├── Dockerfile
│   └── requirements.txt
└── helm/
    └── learnflow-backend/
        ├── Chart.yaml
        ├── values.yaml
        └── templates/
            ├── deployment.yaml
            ├── service.yaml
            └── dapr-annotations.yaml
```

## Research Findings

### OpenAI Agent Patterns with FastAPI
- Use Chat Completions API with function calling for structured outputs
- System prompt loaded from external markdown files for easy iteration
- Async client: `openai.AsyncOpenAI()` for non-blocking I/O
- gpt-4o-mini: $0.15/1M input, $0.60/1M output — cost-efficient for tutoring

### Dapr Pub/Sub Integration
- Package: `dapr-ext-fastapi` provides `DaprApp` class
- Publish: `dapr_client.publish_event(pubsub_name="pubsub", topic_name="...", data=...)`
- Subscribe: `@app.subscribe(pubsub="pubsub", topic="...")` decorator
- Topic handler receives CloudEvent envelope

### Python Sandbox Execution
- RestrictedPython compiles code with restricted builtins
- subprocess with `resource` limits (RLIMIT_AS for memory, timeout for time)
- `/tmp` only filesystem access
- Blocked imports: anything not in `sys.stdlib_module_names`

### Mastery Calculation (EMA)
- Formula: `new_score = alpha * current_event + (1 - alpha) * old_score`
- Alpha = 0.3 (recent events weighted more heavily)
- Components: exercises(40%) + quizzes(30%) + code_quality(20%) + streak(10%)
- Level thresholds: 0-40 Beginner, 41-70 Learning, 71-90 Proficient, 91-100 Mastered

### Struggle Detection (Sliding Window)
- Maintain last 10 errors per student in Dapr state
- Pattern: 3+ same error type within window → trigger alert
- Additional triggers: stuck > 10 min, quiz < 50%, explicit "I don't understand"
- Publish to `struggle.detected` Kafka topic

### FastAPI + Pydantic v2
- Use `model_config = ConfigDict(from_attributes=True)` for ORM mode
- `Field(...)` for validation, `model_validator` for cross-field checks
- Async endpoints with `async def` for all I/O operations
- OpenAPI docs auto-generated at `/docs`

## Pydantic Models (Core)

| Model | Fields | Used By |
|-------|--------|---------|
| ChatRequest | message, session_id, student_id | Triage |
| ChatResponse | response, agent_type, code_blocks[] | All agents |
| RoutingDecision | target_agent, confidence, keywords | Triage |
| CodeExecuteRequest | code, student_id | Code Runner |
| CodeExecuteResult | stdout, stderr, execution_time, timed_out, memory_exceeded | Code Runner |
| ExerciseRequest | topic, difficulty, student_mastery | Exercise |
| Exercise | type, title, description, starter_code, test_cases[] | Exercise |
| GradeRequest | exercise_id, solution, student_id | Exercise |
| GradeResult | score, test_results[], feedback, passed | Exercise |
| MasteryScore | topic, score, level, exercises, quizzes, quality, streak | Progress |
| StruggleAlert | student_id, type, error_history[], confidence, timestamp | Debug |

## Complexity Tracking

No constitution violations — no complexity justification needed.
