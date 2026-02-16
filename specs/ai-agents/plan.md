# Implementation Plan: LearnFlow AI Agent System

**Branch**: `005-ai-agents` | **Date**: 2026-02-01 | **Spec**: [spec.md](./spec.md)
**Input**: Feature specification from `specs/ai-agents/spec.md`

## Summary

Implement a multi-agent AI tutoring system using OpenAI Agents SDK with handoff-based orchestration. 7 specialist agents (Triage, Concepts, Debug, Code Review, Exercise, Progress, plus shared infrastructure) run as FastAPI microservices with Dapr sidecars. Each agent uses external markdown system prompts and communicates via Kafka topics for async operations with sync HTTP for direct user responses.

## Technical Context

**Language/Version**: Python 3.11+, FastAPI 0.100+
**Primary Dependencies**: openai (Agents SDK), fastapi, dapr-ext-fastapi, pydantic v2
**Storage**: PostgreSQL via Dapr state store for session/struggle state
**Testing**: pytest, httpx async test client
**Target Platform**: Kubernetes (Minikube) with Dapr sidecars
**Project Type**: Multi-agent system (7 microservices)
**Performance Goals**: < 5s response for standard queries, < 3s for triage routing
**Constraints**: gpt-4o-mini for cost efficiency, stateless agents, external system prompts
**Scale/Scope**: 7 agent services, 12 domain entities, 6 system prompts, 7 Kafka event schemas

## Constitution Check

| Principle | Status | Notes |
|-----------|--------|-------|
| I. Skills-First | PASS | Agent services scaffolded via fastapi-dapr-agent skill |
| II. Token Efficiency | PASS | System prompts in external .md files, not in SKILL.md |
| III. Cloud-Native | PASS | Docker containers on K8s with Dapr sidecars |
| IV. Microservices | PASS | 7 independent agent services |
| V. Security | PASS | No hardcoded API keys, JWT auth, sandboxed execution |
| VI. SDD | PASS | Spec → Plan → Tasks workflow |
| VII. Cross-Agent | PASS | Standard Python/FastAPI code |
| VIII. Observability | PASS | /health endpoints, structured logs, struggle detection alerts |

## Project Structure

### Documentation (this feature)

```text
specs/ai-agents/
├── plan.md              # This file
├── tasks.md             # Implementation tasks
├── checklists/
│   └── requirements.md  # Quality checklist
```

### Source Code

```text
learnflow-app/backend/
├── shared/
│   ├── agent_base.py        # Base agent class with OpenAI SDK setup
│   ├── models.py            # Shared Pydantic models (extended from 003)
│   ├── dapr_utils.py        # Dapr pub/sub and state helpers
│   ├── prompts/
│   │   ├── triage.md        # Triage system prompt
│   │   ├── concepts.md      # Concepts tutor prompt
│   │   ├── debug.md         # Debug assistant prompt
│   │   ├── code-review.md   # Code reviewer prompt
│   │   ├── exercise.md      # Exercise generator prompt
│   │   └── progress.md      # Progress tracker prompt
│   └── config.py
├── triage-service/          # Port 8001 - Routes to specialists
│   ├── main.py
│   ├── agent.py             # OpenAI Agents SDK with handoffs
│   ├── classifier.py        # Keyword + LLM intent classification
│   └── ...
├── concepts-service/        # Port 8002 - Python concept explanations
│   ├── main.py
│   ├── agent.py             # Adaptive teaching agent
│   ├── modules.py           # 8 Python module definitions
│   └── ...
├── debug-service/           # Port 8004 - Error parsing & hints
│   ├── main.py
│   ├── agent.py             # Progressive disclosure agent
│   ├── parser.py            # Traceback parser
│   ├── struggle.py          # Sliding window detector
│   └── ...
├── code-review-service/     # Port 8007 - Quality feedback
│   ├── main.py
│   ├── agent.py             # 4-criterion evaluator
│   ├── rubric.py            # Scoring rubric definitions
│   └── ...
├── exercise-service/        # Port 8005 - Challenge generation
│   ├── main.py
│   ├── agent.py             # Exercise generator with grading
│   ├── grader.py            # Test case execution
│   ├── difficulty.py        # Mastery-based difficulty selection
│   └── ...
└── progress-service/        # Port 8006 - Mastery tracking
    ├── main.py
    ├── mastery.py           # EMA-based calculation
    ├── milestones.py        # Level transition detection
    └── ...
```

## Research Findings

### OpenAI Agents SDK Multi-Agent Patterns
- `Agent` class with `name`, `instructions`, `model`, and `tools`
- Handoffs: `agent.handoff(target_agent)` for Triage → Specialist routing
- Runner: `Runner.run(agent, messages)` for execution
- Function tools: `@function_tool` decorator for structured actions
- Streaming: `Runner.run_streamed()` for real-time responses

### System Prompt Engineering
- External markdown files loaded at startup: `Path("prompts/concepts.md").read_text()`
- Prompts include: role, behavior rules, output format, examples
- Temperature: 0.7 for creative responses, 0.3 for classification
- Max tokens: 1000 for explanations, 500 for routing decisions

### Sliding Window Struggle Detection
- Dapr state key: `struggle:{student_id}` → list of last 10 errors
- Error record: `{type, line, timestamp, code_snippet}`
- Detection: count same `type` in window ≥ 3 → trigger alert
- Additional triggers tracked via timestamp comparisons (stuck > 10 min)

### Exercise Auto-Grading with Partial Credit
- Test cases: `{input, expected_output, name, weight}`
- Run student code with each test case input
- Compare actual vs expected output (exact match or regex)
- Score = sum(passed_weight) / sum(total_weight) * 100
- Feedback per test case: pass/fail with hints for failures

### EMA-Based Mastery Calculation
- `new_mastery = alpha * event_score + (1 - alpha) * current_mastery`
- Alpha = 0.3 (balances recency with stability)
- Component weights: exercises(0.4) + quizzes(0.3) + quality(0.2) + streak(0.1)
- Level thresholds: 0-40 Beginner, 41-70 Learning, 71-90 Proficient, 91-100 Mastered

### Dapr Event Pipeline
- Triage publishes routing decision to `learning.questions`
- Specialist subscribes, processes, publishes response to `learning.responses`
- Frontend subscribes to `learning.responses` for display
- Debug publishes to `struggle.detected` when patterns match
- Progress publishes to `progress.updated` on mastery changes

## Domain Entities

| Entity | Key Fields | Used By |
|--------|-----------|---------|
| AgentConfig | name, model, prompt_path, temperature, max_tokens | All agents |
| RoutingDecision | target_agent, confidence, keywords, fallback_used | Triage |
| StudentSession | student_id, session_id, messages[], mastery_level | All agents |
| Message | role, content, code_blocks[], timestamp | All agents |
| StudentStruggleState | student_id, errors[], last_activity, exercise_start | Debug |
| ErrorRecord | type, line, context, timestamp, code_snippet | Debug |
| StruggleAlert | student_id, type, count, error_history[], confidence | Debug |
| Exercise | type, difficulty, title, description, starter_code, test_cases[] | Exercise |
| TestCase | name, input, expected_output, weight | Exercise |
| GradeResult | score, test_results[], feedback, passed | Exercise |
| MasteryScore | topic, score, level, components{} | Progress |
| ProgressSummary | topics[], overall_average, streak, milestones[] | Progress |

## Complexity Tracking

| Decision | Why Needed | Simpler Alternative Rejected |
|----------|------------|------------------------------|
| Code Review as 7th service (port 8007) | Distinct evaluation rubric, separate scaling needs | Combining with Concepts would mix teaching and evaluation concerns |
