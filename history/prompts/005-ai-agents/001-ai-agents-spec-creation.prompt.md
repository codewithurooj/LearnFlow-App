---
id: 001
title: AI Agents System Specification Creation
stage: spec
date: 2026-01-25
surface: project
model: claude-opus-4-5
feature: 005-ai-agents
branch: 005-ai-agents
user: developer
command: /sp.specify
labels: [spec, ai-agents, multi-agent, openai-sdk, kafka]
links:
  spec: specs/005-ai-agents/spec.md
  ticket: null
  adr: null
  pr: null
files:
  - path: specs/005-ai-agents/spec.md
    action: created
  - path: specs/005-ai-agents/checklists/requirements.md
    action: created
tests:
  - null
---

## Prompt

Create specification for LearnFlow AI agent system.

Context:
- Multi-agent architecture with specialist agents
- OpenAI SDK for LLM interactions
- Agents communicate via Kafka topics

Agents Required:

1. Triage Agent
   - Input: Student message
   - Output: Route to specialist (concepts/debug/code_review/exercise/progress)
   - Routing rules based on keywords

2. Concepts Agent
   - System prompt: Python tutor, adapts to level, provides examples
   - Must include runnable code examples
   - Covers 8 modules: Basics, Control Flow, Data Structures, Functions, OOP, Files, Errors, Libraries

3. Debug Agent
   - Parses Python tracebacks
   - Provides hints BEFORE solutions
   - Triggers struggle alert after 3+ same errors

4. Code Review Agent
   - Checks: correctness, PEP 8 style, efficiency, readability
   - Rating: 1-5 stars
   - Encouraging feedback

5. Exercise Agent
   - Types: fill-in-blank, bug-fix, write-function, output-prediction
   - Difficulty: easy/medium/hard
   - Auto-grading with test cases

6. Progress Agent
   - Tracks mastery per topic
   - Calculates weighted scores
   - Celebrates milestones

User Stories:
- US1: Triage correctly routes 95%+ of queries
- US2: Concepts adapts explanation to beginner vs proficient
- US3: Debug detects struggle and alerts teacher
- US4: Exercise generates appropriate difficulty based on mastery

Include system prompts for each agent.

Technical Requirements:
- Each agent is a FastAPI microservice with Dapr sidecar
- OpenAI SDK with gpt-4o-mini for cost efficiency
- Kafka topics: learning.questions, learning.responses, struggle.detected
- Stateless agents, state stored in PostgreSQL via Dapr
- MCP server for context provision

Output spec to: specs/005-ai-agents/spec.md

## Response snapshot

Created comprehensive specification for LearnFlow AI Agent System with:
- 6 specialist agents (Triage, Concepts, Debug, Code Review, Exercise, Progress)
- Detailed system prompts for each agent with behavior rules
- 6 prioritized user stories with acceptance scenarios
- 17 functional requirements (FR-001 to FR-017)
- 7 message topics for inter-agent communication
- 10 measurable success criteria
- Edge cases, assumptions, and out-of-scope items
- Requirements checklist validating spec quality

## Outcome

- Impact: Created feature branch 005-ai-agents and complete specification for multi-agent AI tutoring system
- Tests: N/A (specification phase)
- Files: 2 files created (spec.md, requirements.md checklist)
- Next prompts: /sp.plan to create architecture plan, /sp.tasks to generate implementation tasks
- Reflection: Comprehensive system prompts enable autonomous agent behavior; message topic design supports loose coupling

## Evaluation notes (flywheel)

- Failure modes observed: None - spec generated successfully with all required sections
- Graders run and results (PASS/FAIL): Checklist validation PASS - all items checked
- Prompt variant (if applicable): N/A
- Next experiment (smallest change to try): Consider adding agent interaction diagrams in plan phase
