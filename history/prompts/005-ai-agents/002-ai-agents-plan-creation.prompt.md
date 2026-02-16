---
id: 002
title: AI Agents Implementation Plan Creation
stage: plan
date: 2026-02-01
surface: project
model: claude-opus-4-5
feature: 005-ai-agents
branch: 005-ai-agents
user: pc1
command: /sp.plan
labels: [plan, ai-agents, multi-agent, openai-agents-sdk]
links:
  spec: specs/005-ai-agents/spec.md
  ticket: ~
  adr: ~
  pr: ~
files:
  - path: specs/005-ai-agents/plan.md
    action: created
  - path: specs/005-ai-agents/research.md
    action: created
  - path: specs/005-ai-agents/data-model.md
    action: created
  - path: specs/005-ai-agents/quickstart.md
    action: created
  - path: specs/005-ai-agents/contracts/triage-agent.yaml
    action: created
  - path: specs/005-ai-agents/contracts/concepts-agent.yaml
    action: created
  - path: specs/005-ai-agents/contracts/debug-agent.yaml
    action: created
  - path: specs/005-ai-agents/contracts/code-review-agent.yaml
    action: created
  - path: specs/005-ai-agents/contracts/exercise-agent.yaml
    action: created
  - path: specs/005-ai-agents/contracts/progress-agent.yaml
    action: created
tests:
  ~
---

## Prompt

ai-agents at this location C:\Users\pc1\Desktop\reusable-intelligence\specs\005-ai-agents in current directory

## Response snapshot

Executed `/sp.plan` for 005-ai-agents feature. Generated complete Phase 0 (research) and Phase 1 (design & contracts) artifacts:

1. **plan.md** — Implementation plan covering Technical Context (Python 3.11+, OpenAI Agents SDK, FastAPI, Dapr), Constitution Check (all 8 principles PASS), Project Structure (7 services including new code-review), hybrid sync/async architecture, and 3 architectural decisions.

2. **research.md** — Phase 0 research resolving 6 unknowns: OpenAI Agents SDK multi-agent patterns with handoffs, system prompt engineering best practices, sliding window struggle detection, Dapr event pipeline wiring, exercise auto-grading with partial credit, and EMA-based mastery calculation.

3. **data-model.md** — 12 domain entities: AgentConfig, RoutingDecision, StudentSession, Message, StudentStruggleState, ErrorRecord, StruggleAlert, Exercise, TestCase, GradeResult, MasteryScore, ProgressSummary, MilestoneEvent. Includes Kafka event schemas and Dapr state store key patterns.

4. **contracts/** — 6 OpenAPI 3.0.3 specs for triage, concepts, debug, code-review, exercise, and progress agent services.

5. **quickstart.md** — Local dev guide with environment setup, running individual/all services with Dapr, testing endpoints, and Kubernetes deployment.

Key decisions: OpenAI Agents SDK for multi-agent orchestration (handoffs), external markdown system prompts, Code Review as separate 7th microservice (Port 8007), hybrid sync/async API pattern.

## Outcome

- ✅ Impact: Complete plan with all Phase 0 and Phase 1 artifacts generated
- 🧪 Tests: N/A (planning phase, no code written)
- 📁 Files: 10 files created (plan.md, research.md, data-model.md, quickstart.md, 6 contract YAMLs)
- 🔁 Next prompts: `/sp.tasks` to generate implementation tasks, `/sp.adr agent-framework-selection`, `/sp.adr code-review-service-separation`
- 🧠 Reflection: Leveraged existing 003-backend analysis to identify gaps (missing code-review service, incomplete event pipeline, no progress agent logic). OpenAI Agents SDK handoffs map cleanly to triage routing pattern.

## Evaluation notes (flywheel)

- Failure modes observed: Agent context update script failed (missing template file); non-blocking
- Graders run and results (PASS/FAIL): Constitution Check PASS (all 8 principles), Post-Design Re-Check PASS
- Prompt variant (if applicable): ~
- Next experiment (smallest change to try): ~
