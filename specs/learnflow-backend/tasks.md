# Tasks: LearnFlow Backend Microservices

**Input**: Design documents from `specs/learnflow-backend/`
**Prerequisites**: plan.md (required), spec.md (required for user stories)

**Tests**: Not explicitly requested in spec. Test tasks omitted.

**Organization**: Tasks grouped by user story for independent implementation.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1, US2)
- All paths relative to `learnflow-app/backend/`

---

## Phase 1: Setup (Project Structure)

**Purpose**: Initialize the backend monorepo structure

- [ ] T001 Create backend directory structure: `shared/`, 6 service directories, `helm/`
- [ ] T002 [P] Create root `requirements-shared.txt` with common dependencies (fastapi, uvicorn, openai, pydantic, dapr-ext-fastapi)
- [ ] T003 [P] Create `.env.example` with OPENAI_API_KEY, DAPR_HTTP_PORT, SERVICE_PORT, LOG_LEVEL
- [ ] T004 [P] Create root `docker-compose.dev.yaml` for local development (all 6 services + Dapr sidecars)
- [ ] T005 [P] Create `.gitignore` for Python projects

---

## Phase 2: Foundational (Shared Infrastructure)

**Purpose**: Core shared code and service scaffolds that ALL user stories depend on

**CRITICAL**: No user story work can begin until this phase is complete

### Shared Models & Utilities

- [ ] T006 Create `shared/models.py` — all shared Pydantic v2 models: ChatRequest, ChatResponse, CodeExecuteRequest, CodeExecuteResult, ExerciseRequest, Exercise, GradeRequest, GradeResult, MasteryScore, StruggleAlert, HealthResponse
- [ ] T007 Create `shared/dapr_utils.py` — Dapr helpers: publish_event(), get_state(), save_state(), invoke_service()
- [ ] T008 [P] Create `shared/config.py` — environment configuration using pydantic-settings (service port, Dapr port, OpenAI key, log level)
- [ ] T009 [P] Create `shared/logging_config.py` — structured JSON logging setup with service name, request ID

### Service Scaffolds (via fastapi-dapr-agent skill pattern)

- [ ] T010 [P] Scaffold `triage-service/` — main.py (FastAPI app, /health, /api/chat), models.py, Dockerfile, requirements.txt
- [ ] T011 [P] Scaffold `concepts-service/` — main.py, models.py, Dockerfile, requirements.txt
- [ ] T012 [P] Scaffold `code-runner-service/` — main.py, models.py, Dockerfile, requirements.txt
- [ ] T013 [P] Scaffold `debug-service/` — main.py, models.py, Dockerfile, requirements.txt
- [ ] T014 [P] Scaffold `exercise-service/` — main.py, models.py, Dockerfile, requirements.txt
- [ ] T015 [P] Scaffold `progress-service/` — main.py, models.py, Dockerfile, requirements.txt

### Health Endpoints

- [ ] T016 [P] Implement /health endpoint in triage-service returning {status, service_name: "triage", version}
- [ ] T017 [P] Implement /health endpoint in concepts-service
- [ ] T018 [P] Implement /health endpoint in code-runner-service
- [ ] T019 [P] Implement /health endpoint in debug-service
- [ ] T020 [P] Implement /health endpoint in exercise-service
- [ ] T021 [P] Implement /health endpoint in progress-service

### Dapr Integration

- [ ] T022 Configure Dapr pub/sub subscription handlers in each service main.py (subscribe to relevant topics)
- [ ] T023 Configure Dapr state store access in services that need state (debug-service for struggle tracking, progress-service for mastery)

**Checkpoint**: Foundation ready — all services start, health checks pass

---

## Phase 3: User Story 1 — Question Routing (Priority: P1) MVP

**Goal**: Student asks question → Triage routes → Concepts responds

**Independent Test**: POST /api/chat with "How do lists work?" → response with Python explanation

- [ ] T024 [US1] Implement `triage-service/router.py` — keyword matching: "explain/how/what" → concepts, "error/traceback/bug" → debug, "review/check" → code_review, "exercise/practice" → exercise, "progress/score" → progress
- [ ] T025 [US1] Implement LLM fallback in `triage-service/router.py` — when keywords are ambiguous, use OpenAI to classify intent
- [ ] T026 [US1] Implement routing logic in `triage-service/main.py` — POST /api/chat receives question, classifies, routes via Dapr service invocation
- [ ] T027 [US1] Implement session management in `triage-service/main.py` — maintain conversation context per session_id using Dapr state
- [ ] T028 [US1] Create `concepts-service/prompts/concepts.md` — system prompt: Python tutor, adapt to level, include code examples
- [ ] T029 [US1] Implement `concepts-service/agent.py` — OpenAI SDK agent with system prompt, processes questions about 8 Python modules
- [ ] T030 [US1] Implement `concepts-service/main.py` — POST /api/explain receives routed question, invokes agent, returns response
- [ ] T031 [US1] Implement adaptive responses in `concepts-service/agent.py` — adjust complexity based on student mastery level from Dapr state
- [ ] T032 [US1] Implement Kafka publishing in triage-service — publish routing decisions to `learning.questions`
- [ ] T033 [US1] Implement Kafka publishing in concepts-service — publish responses to `learning.responses`
- [ ] T034 [US1] Wire up triage → concepts end-to-end — test full routing flow
- [ ] T035 [US1] Verify session context — multi-turn conversation maintains context
- [ ] T036 [US1] Test routing accuracy — verify keyword matching for 10+ sample queries

**Checkpoint**: US1 complete — question → routing → response works

---

## Phase 4: User Story 2 — Code Execution (Priority: P1) MVP

**Goal**: Student submits code → sandboxed execution → results returned

**Independent Test**: POST /api/execute with `print("Hello")` → stdout "Hello"

- [ ] T037 [US2] Implement `code-runner-service/sandbox.py` — RestrictedPython compilation, subprocess execution with resource limits
- [ ] T038 [US2] Implement timeout enforcement in sandbox.py — kill process after 5 seconds, return timed_out=true
- [ ] T039 [US2] Implement memory limit in sandbox.py — RLIMIT_AS set to 50MB, detect and report memory_exceeded
- [ ] T040 [US2] Implement import restriction in sandbox.py — block non-standard-library imports
- [ ] T041 [US2] Implement `code-runner-service/main.py` — POST /api/execute receives code, runs sandbox, returns CodeExecuteResult
- [ ] T042 [US2] Implement Kafka publishing — publish results to `code.results` topic
- [ ] T043 [US2] Test sandbox with valid code — print, loops, functions
- [ ] T044 [US2] Test sandbox limits — timeout, memory, blocked imports, no network

**Checkpoint**: US2 complete — code execution works with all sandbox constraints

---

## Phase 5: User Story 3 — Struggle Detection (Priority: P2)

**Goal**: Debug service detects patterns and alerts teachers

**Independent Test**: Submit 3 same-type errors → struggle alert on Kafka topic

- [ ] T045 [US3] Create `debug-service/prompts/debug.md` — system prompt: parse errors, provide hints first, identify root cause
- [ ] T046 [US3] Implement `debug-service/parser.py` — extract error type, line number, and context from Python tracebacks
- [ ] T047 [US3] Implement `debug-service/agent.py` — OpenAI SDK agent with progressive disclosure (hint → solution)
- [ ] T048 [US3] Implement `debug-service/struggle.py` — sliding window tracker: store last 10 errors per student in Dapr state, detect 3+ same type
- [ ] T049 [US3] Implement `debug-service/main.py` — POST /api/debug receives code + error, parses, invokes agent, checks struggle patterns
- [ ] T050 [US3] Implement struggle alert publishing — publish to `struggle.detected` Kafka topic when pattern detected
- [ ] T051 [US3] Wire up code-runner → debug flow — failed execution triggers debug analysis
- [ ] T052 [US3] Test struggle detection — 3 NameErrors → alert; 2 NameErrors → no alert
- [ ] T053 [US3] Test progressive disclosure — verify hint comes before solution

**Checkpoint**: US3 complete — errors parsed, hints given, struggle detected

---

## Phase 6: User Story 4 — Mastery Update (Priority: P2)

**Goal**: Exercises graded, mastery scores calculated and published

**Independent Test**: Complete exercise → mastery score updates with correct formula

- [ ] T054 [US4] Create `exercise-service/prompts/exercise.md` — system prompt: generate exercises by type and difficulty
- [ ] T055 [US4] Implement `exercise-service/agent.py` — OpenAI SDK agent for exercise generation (4 types: fill-in-blank, bug-fix, write-function, output-prediction)
- [ ] T056 [US4] Implement `exercise-service/grader.py` — auto-grading: run student code against test cases, calculate score, generate feedback
- [ ] T057 [US4] Implement `exercise-service/main.py` — POST /api/generate-exercise, POST /api/grade-exercise
- [ ] T058 [US4] Implement difficulty selection based on mastery level — easy for <40%, medium for 40-70%, hard for >70%
- [ ] T059 [US4] Implement `progress-service/mastery.py` — weighted EMA formula: exercises(40%) + quizzes(30%) + quality(20%) + streak(10%)
- [ ] T060 [US4] Implement `progress-service/milestones.py` — detect level transitions (Beginner→Learning, etc.), generate celebration messages
- [ ] T061 [US4] Implement `progress-service/main.py` — POST /api/update-progress, GET /api/progress/{student_id}
- [ ] T062 [US4] Implement Kafka subscription in progress-service — subscribe to grade results, auto-update mastery
- [ ] T063 [US4] Implement Kafka publishing in progress-service — publish to `progress.updated` on mastery changes
- [ ] T064 [US4] Test mastery calculation — verify formula produces expected scores with known inputs
- [ ] T065 [US4] Test milestone detection — verify level transition triggers celebration
- [ ] T066 [US4] Wire up exercise → grading → progress flow end-to-end

**Checkpoint**: US4 complete — exercise → grade → mastery update works

---

## Phase 7: Polish & Cross-Cutting

**Purpose**: Dockerization, Helm charts, and documentation

- [ ] T067 [P] Build and test all 6 Dockerfiles — verify images build and containers start
- [ ] T068 [P] Create `helm/learnflow-backend/Chart.yaml` — Helm chart metadata
- [ ] T069 Create `helm/learnflow-backend/values.yaml` — service configs, resource limits, image tags
- [ ] T070 Create `helm/learnflow-backend/templates/deployment.yaml` — parameterized deployment with Dapr annotations
- [ ] T071 [P] Create `helm/learnflow-backend/templates/service.yaml` — K8s services for all 6 backends
- [ ] T072 Test Helm deployment on Minikube — deploy all services, verify health checks
- [ ] T073 [P] Add structured JSON logging to all services — verify log format
- [ ] T074 [P] Create backend README.md — service descriptions, local dev setup, API docs links
- [ ] T075 [P] Verify all services work with Dapr on Minikube — pub/sub, state, invocation
- [ ] T076 End-to-end integration test — question → triage → concepts → response, code → execute → result
- [ ] T077 [P] Document API endpoints for all 6 services — request/response examples
- [ ] T078 [P] Verify OpenAI SDK integration — all agent services generate meaningful responses
- [ ] T079 [P] Performance check — verify 50 concurrent requests handled without errors
- [ ] T080 [P] Memory check — verify total backend memory < 3GB on Minikube
- [ ] T081 Final deployment verification — fresh Minikube, deploy infrastructure + backend, run all checks

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies
- **Foundational (Phase 2)**: Depends on Phase 1 — BLOCKS all user stories
- **US1 Routing (Phase 3)**: Depends on Phase 2
- **US2 Code Execution (Phase 4)**: Depends on Phase 2, can run in parallel with Phase 3
- **US3 Struggle Detection (Phase 5)**: Depends on Phase 4 (code-runner)
- **US4 Mastery Update (Phase 6)**: Depends on Phase 2, can start in parallel with Phase 3
- **Polish (Phase 7)**: Depends on Phases 3-6

### MVP Scope

Phases 1-4 (Setup + Foundational + US1 + US2) = 44 tasks

---

## Notes

- [P] tasks = different files, no dependencies
- 33 tasks marked [P] for parallel execution
- Each service follows the fastapi-dapr-agent skill pattern
- OpenAI SDK with gpt-4o-mini for cost efficiency
- All state via Dapr (no direct DB access from services)
