# Tasks: LearnFlow AI Agent System

**Input**: Design documents from `specs/ai-agents/`
**Prerequisites**: plan.md (required), spec.md (required for user stories), research findings on OpenAI Agents SDK

**Tests**: Not explicitly requested in spec. Test tasks omitted.

**Organization**: Tasks grouped by user story for independent implementation.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1 = Triage Routing)
- All paths relative to `learnflow-app/backend/`

---

## Phase 1: Setup (Agent Infrastructure)

**Purpose**: Initialize shared agent infrastructure

- [ ] T001 Create `shared/agent_base.py` — base agent class with OpenAI SDK setup, prompt loading, response formatting
- [ ] T002 [P] Create `shared/prompts/` directory for all 6 system prompt markdown files
- [ ] T003 [P] Update `shared/models.py` — add agent-specific models: AgentConfig, RoutingDecision, StudentSession, Message, ErrorRecord, MilestoneEvent
- [ ] T004 [P] Update `shared/config.py` — add OPENAI_MODEL (default: gpt-4o-mini), OPENAI_TEMPERATURE, MAX_TOKENS settings

---

## Phase 2: Foundational (System Prompts & Agent Base)

**Purpose**: Create all system prompts and agent base that all user stories depend on

**CRITICAL**: No agent implementation can begin until system prompts are ready

- [ ] T005 Create `shared/prompts/triage.md` — system prompt: classify student intent, route to specialist, confidence scoring
- [ ] T006 [P] Create `shared/prompts/concepts.md` — system prompt: Python tutor, adapt to mastery level, include runnable code examples, cover 8 modules
- [ ] T007 [P] Create `shared/prompts/debug.md` — system prompt: parse tracebacks, progressive disclosure (hints first), identify root cause
- [ ] T008 [P] Create `shared/prompts/code-review.md` — system prompt: evaluate correctness/style/efficiency/readability, star rating 1-5, encouraging feedback
- [ ] T009 [P] Create `shared/prompts/exercise.md` — system prompt: generate exercises by type and difficulty, include test cases, grade submissions
- [ ] T010 [P] Create `shared/prompts/progress.md` — system prompt: summarize mastery, celebrate milestones, suggest improvements
- [ ] T011 Implement `shared/agent_base.py` — load prompt from file, initialize OpenAI client, create Agent with tools and handoffs
- [ ] T012 [P] Create agent configuration registry — map agent names to configs (model, prompt path, temperature, max tokens)

**Checkpoint**: Agent infrastructure ready — specialist implementations can begin

---

## Phase 3: User Story 1 — Triage Routing (Priority: P0) MVP

**Goal**: Triage routes 95%+ of queries to correct specialist

**Independent Test**: Send 20+ diverse queries, measure routing accuracy

- [ ] T013 [US1] Implement `triage-service/classifier.py` — keyword matching rules for 5 specialists
- [ ] T014 [US1] Implement LLM fallback in `triage-service/classifier.py` — OpenAI classification for ambiguous queries with confidence score
- [ ] T015 [US1] Implement `triage-service/agent.py` — OpenAI Agents SDK Agent with handoffs to all specialists
- [ ] T016 [US1] Wire up triage routing in `triage-service/main.py` — POST /api/chat → classify → route via Dapr service invocation
- [ ] T017 [US1] Implement session context in triage — load/save conversation history from Dapr state per session_id
- [ ] T018 [US1] Publish routing decisions to `learning.questions` Kafka topic via Dapr pub/sub
- [ ] T019 [US1] Test routing accuracy — 20+ test queries covering all 5 specialists
- [ ] T020 [US1] Test LLM fallback — ambiguous queries correctly classified
- [ ] T021 [US1] Verify 95%+ accuracy target — document results

**Checkpoint**: US1 complete — triage routes queries with high accuracy

---

## Phase 4: User Story 2 — Adaptive Concepts (Priority: P0)

**Goal**: Concepts Agent adapts explanations to student mastery level

**Independent Test**: Same topic query at beginner vs. proficient level produces different complexity

- [ ] T022 [US2] Implement `concepts-service/modules.py` — define 8 Python modules with subtopics and difficulty progression
- [ ] T023 [US2] Implement `concepts-service/agent.py` — OpenAI agent that reads student mastery level and adjusts response complexity
- [ ] T024 [US2] Implement adaptive logic — beginner: simple vocabulary, basic examples; proficient: advanced patterns, edge cases
- [ ] T025 [US2] Wire up `concepts-service/main.py` — receive routed question, lookup mastery from Dapr state, invoke agent
- [ ] T026 [US2] Publish responses to `learning.responses` Kafka topic
- [ ] T027 [US2] Test level adaptation — same query at beginner vs. proficient produces measurably different responses
- [ ] T028 [US2] Verify code examples — all responses include at least one runnable Python snippet

**Checkpoint**: US2 complete — concepts adapt to student level

---

## Phase 5: User Story 3 — Struggle Detection (Priority: P1)

**Goal**: Debug Agent detects patterns, provides hints, alerts teachers

**Independent Test**: 3 same-type errors trigger struggle alert

- [ ] T029 [US3] Implement `debug-service/parser.py` — extract error type, line number, context from Python tracebacks
- [ ] T030 [US3] Implement `debug-service/agent.py` — progressive disclosure: hint mode (default) and solution mode (on request)
- [ ] T031 [US3] Implement `debug-service/struggle.py` — sliding window (last 10 errors per student), count same-type errors, threshold at 3
- [ ] T032 [US3] Wire up `debug-service/main.py` — receive error, parse, invoke agent, check struggle pattern, publish alert if triggered
- [ ] T033 [US3] Implement Dapr state for struggle tracking — key: `struggle:{student_id}`, value: list of ErrorRecord
- [ ] T034 [US3] Publish struggle alerts to `struggle.detected` Kafka topic
- [ ] T035 [US3] Test hint before solution — verify first response is hint, second reveals fix
- [ ] T036 [US3] Test struggle detection — 3 NameErrors → alert, 2 → no alert
- [ ] T037 [US3] Test sliding window — old errors expire from window correctly

**Checkpoint**: US3 complete — errors parsed, hints given, teacher alerted

---

## Phase 6: User Story 4 — Exercise Generation & Grading (Priority: P1)

**Goal**: Exercises generated by difficulty, auto-graded with test cases

**Independent Test**: Request exercise at mastery level → correct difficulty, submit solution → score returned

- [ ] T038 [US4] Implement `exercise-service/difficulty.py` — mastery-to-difficulty mapping: <40% → easy, 40-70% → medium, >70% → hard
- [ ] T039 [US4] Implement `exercise-service/agent.py` — generate exercises of 4 types based on topic and difficulty
- [ ] T040 [US4] Implement `exercise-service/grader.py` — execute student code against test cases, calculate score, generate feedback
- [ ] T041 [US4] Wire up `exercise-service/main.py` — POST /api/generate-exercise, POST /api/grade-exercise
- [ ] T042 [US4] Test difficulty selection — beginner gets easy, proficient gets hard
- [ ] T043 [US4] Test auto-grading — correct solution scores 100%, partial gets proportional score
- [ ] T044 [US4] Test feedback — failed tests provide hints without revealing answer

**Checkpoint**: US4 complete — exercises generated and graded correctly

---

## Phase 7: User Story 5 — Code Review (Priority: P2)

**Goal**: Code reviewed on 4 criteria with star ratings

**Independent Test**: Submit code → receive ratings and suggestions

- [ ] T045 [US5] Implement `code-review-service/rubric.py` — define scoring criteria: correctness, PEP 8 style, efficiency, readability
- [ ] T046 [US5] Implement `code-review-service/agent.py` — OpenAI agent evaluates code against rubric, provides star rating per criterion
- [ ] T047 [US5] Wire up `code-review-service/main.py` — POST /api/review receives code, invokes agent, returns CriterionScore[] and overall rating
- [ ] T048 [US5] Test rating consistency — same code scores within 0.5 stars across 3 runs
- [ ] T049 [US5] Test feedback quality — suggestions are actionable and encouraging

**Checkpoint**: US5 complete — code review with ratings and suggestions

---

## Phase 8: User Story 6 — Progress & Milestones (Priority: P2)

**Goal**: Mastery tracked with EMA, milestones celebrated

**Independent Test**: Complete exercise → mastery updates, cross threshold → milestone

- [ ] T050 [US6] Implement `progress-service/mastery.py` — EMA calculation: alpha=0.3, weights: exercises(40%)+quizzes(30%)+quality(20%)+streak(10%)
- [ ] T051 [US6] Implement `progress-service/milestones.py` — detect level transitions, generate celebration messages for each transition
- [ ] T052 [US6] Wire up `progress-service/main.py` — POST /api/update-progress, GET /api/progress/{student_id}, GET /api/progress/{student_id}/{topic}
- [ ] T053 [US6] Subscribe to grade results from Kafka — auto-update mastery when exercises are graded
- [ ] T054 [US6] Publish mastery updates to `progress.updated` Kafka topic
- [ ] T055 [US6] Test EMA calculation — verify formula with known inputs matches expected outputs
- [ ] T056 [US6] Test milestones — 40%→41% triggers Beginner→Learning celebration

**Checkpoint**: US6 complete — mastery tracked, milestones celebrated

---

## Phase 9: Polish & Integration

**Purpose**: Cross-agent testing and optimization

- [ ] T057 [P] Test full agent pipeline — question → triage → specialist → response → mastery update
- [ ] T058 End-to-end integration — deploy all 7 agents on Minikube with Dapr, test complete flows
