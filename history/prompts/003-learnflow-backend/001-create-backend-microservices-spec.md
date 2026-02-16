---
id: 001
title: Create Backend Microservices Spec
stage: spec
date: 2026-01-24
surface: project
model: claude-opus-4-5
feature: 003-learnflow-backend
branch: 003-learnflow-backend
user: pc1
command: /sp.specify
labels: [spec, backend, microservices, fastapi, dapr]
links:
  spec: specs/003-learnflow-backend/spec.md
  ticket: null
  adr: null
  pr: null
files:
  - path: specs/003-learnflow-backend/spec.md
    action: created
  - path: specs/003-learnflow-backend/checklists/requirements.md
    action: created
tests:
  - null
---

## Prompt

```text
write spec in current directory and number it as 003 /sp.specify

  Create specification for LearnFlow backend microservices.

  Context:
  - FastAPI + OpenAI SDK for each service
  - Dapr sidecar for pub/sub and state
  - Each AI agent is a separate microservice

  Services Required:
  1. Triage Service (port 8001)
     - Routes queries to specialist agents
     - Keywords: "explain"→concepts, "error"→debug, "review"→code_review

  2. Concepts Service (port 8002)
     - Explains Python concepts with examples
     - Adapts to student mastery level

  3. Code Runner Service (port 8003)
     - Sandbox: 5s timeout, 50MB memory, no network
     - Returns execution result or error

  4. Debug Service (port 8004)
     - Parses tracebacks, identifies root cause
     - Detects struggle patterns (3+ same errors)

  5. Exercise Service (port 8005)
     - Generates coding challenges
     - Auto-grades submissions

  6. Progress Service (port 8006)
     - Calculates mastery: exercises(40%) + quizzes(30%) + quality(20%) + streak(10%)
     - Mastery levels: 0-40% Beginner, 41-70% Learning, 71-90% Proficient, 91-100% Mastered

  User Stories:
  - US1: Student asks question, gets routed to correct agent
  - US2: Student runs code, gets sandboxed execution result
  - US3: Student struggles, teacher receives alert
  - US4: Student completes exercise, mastery updates

  API contracts needed for all endpoints with Pydantic models.
```

## Response snapshot

Created comprehensive specification for LearnFlow backend microservices with:

1. **Four prioritized user stories** covering:
   - P1: Student question routing to specialist agents
   - P1: Sandboxed code execution with security constraints
   - P2: Struggle detection and teacher alerting
   - P2: Exercise completion and mastery tracking

2. **37 functional requirements** organized by service:
   - Triage Service (FR-001 to FR-005)
   - Concepts Service (FR-006 to FR-009)
   - Code Runner Service (FR-010 to FR-016)
   - Debug Service (FR-017 to FR-021)
   - Exercise Service (FR-022 to FR-026)
   - Progress Service (FR-027 to FR-031)
   - Cross-cutting (FR-032 to FR-037)

3. **Complete API contracts** for all six services with request/response schemas

4. **8 success criteria** with measurable metrics

5. **Quality checklist** - all items passed validation

## Outcome

- ✅ Impact: Complete backend microservices spec created with all requested details
- 🧪 Tests: N/A (specification phase)
- 📁 Files: 2 files created (spec.md, requirements.md checklist)
- 🔁 Next prompts: /sp.plan to create architecture plan, /sp.tasks to generate implementation tasks
- 🧠 Reflection: Spec includes detailed API contracts as requested; all user stories mapped to acceptance scenarios

## Evaluation notes (flywheel)

- Failure modes observed: None
- Graders run and results (PASS/FAIL): All checklist items PASS
- Prompt variant (if applicable): N/A
- Next experiment (smallest change to try): N/A
