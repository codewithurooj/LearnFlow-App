---
id: 002
title: Backend Microservices Implementation Plan
stage: plan
date: 2026-01-26
surface: project
model: claude-opus-4-5-20251101
feature: 003-learnflow-backend
branch: 002-platinum-tier
user: pc1
command: /sp.plan
labels: [plan, backend, microservices, fastapi, dapr, openai]
links:
  spec: specs/003-learnflow-backend/spec.md
  ticket:
  adr:
  pr:
files:
  - path: specs/003-learnflow-backend/plan.md
    action: created
  - path: specs/003-learnflow-backend/research.md
    action: created
  - path: specs/003-learnflow-backend/data-model.md
    action: created
  - path: specs/003-learnflow-backend/quickstart.md
    action: created
  - path: specs/003-learnflow-backend/contracts/triage-api.yaml
    action: created
  - path: specs/003-learnflow-backend/contracts/concepts-api.yaml
    action: created
  - path: specs/003-learnflow-backend/contracts/code-runner-api.yaml
    action: created
  - path: specs/003-learnflow-backend/contracts/debug-api.yaml
    action: created
  - path: specs/003-learnflow-backend/contracts/exercise-api.yaml
    action: created
  - path: specs/003-learnflow-backend/contracts/progress-api.yaml
    action: created
tests:
  - none (planning phase)
---

## Prompt

/sp.plan learn-flow-backend in my current directory at this location C:\Users\pc1\Desktop\reusable-intelligence\specs

## Response snapshot

Created complete implementation plan for LearnFlow Backend Microservices including:

**Phase 0: Research** - Researched 6 key areas:
1. OpenAI Agent Patterns with FastAPI (Chat Completions API + Function Calling)
2. Dapr Pub/Sub Integration (dapr-ext-fastapi package)
3. Python Sandbox Execution (RestrictedPython + subprocess + resource limits)
4. Mastery Calculation Algorithms (40/30/20/10 weighted formula with EMA)
5. Struggle Detection Patterns (sliding window pattern detector)
6. FastAPI + Pydantic v2 Best Practices

**Phase 1: Design & Contracts** - Created:
- Data model with 10+ Pydantic models (Student, Session, Question, CodeSubmission, Exercise, MasteryScore, etc.)
- 6 Kafka event schemas (questions, responses, code submissions/results, struggle detected, progress updated)
- 6 OpenAPI contracts for each service (Triage, Concepts, Code Runner, Debug, Exercise, Progress)
- Quickstart guide with local dev and K8s deployment instructions

**Architecture Decision Surfaced**: API Response Pattern - recommended hybrid approach (sync for user-facing chat, async for background tasks).

## Outcome

- ✅ Impact: Complete implementation plan ready for /sp.tasks
- 🧪 Tests: N/A (planning phase)
- 📁 Files: 10 files created (plan.md, research.md, data-model.md, quickstart.md, 6 API contracts)
- 🔁 Next prompts: `/sp.tasks` to generate implementation tasks, `/sp.adr api-response-pattern` if ADR documentation desired
- 🧠 Reflection: Plan covers all 6 services with detailed Pydantic models, OpenAI integration patterns, and Dapr pub/sub configuration. Sandbox security implementation follows best practices with RestrictedPython.

## Evaluation notes (flywheel)

- Failure modes observed: Agent context update script failed due to missing template file
- Graders run and results (PASS/FAIL): N/A
- Prompt variant (if applicable): N/A
- Next experiment (smallest change to try): Add agent-file-template.md to .specify/templates/
