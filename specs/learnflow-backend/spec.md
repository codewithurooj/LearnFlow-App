# Feature Specification: LearnFlow Backend Microservices

**Feature Branch**: `003-learnflow-backend`
**Created**: 2026-01-24
**Status**: Draft
**Input**: User description: "Create specification for LearnFlow backend microservices. FastAPI + OpenAI SDK for each service. Dapr sidecar for pub/sub and state. Each AI agent is a separate microservice."

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Student Question Routing (Priority: P1)

A student sends a Python question through the chat interface. The Triage Service receives the question, analyzes it using keyword matching and LLM classification, and routes it to the appropriate specialist agent (Concepts, Debug, Code Review, Exercise, or Progress). The specialist processes the question and returns a contextual response.

**Why this priority**: Question routing is the core interaction loop. Without it, no learning can happen.

**Independent Test**: Can be tested by sending questions with different intents and verifying they route to the correct specialist and return appropriate responses.

**Acceptance Scenarios**:

1. **Given** a student sends "How do list comprehensions work?", **When** the Triage Service receives it, **Then** it routes to the Concepts Service and a response explaining list comprehensions with code examples is returned.
2. **Given** a student sends "I'm getting a NameError", **When** the Triage Service receives it, **Then** it routes to the Debug Service.
3. **Given** a student sends "Review my code", **When** the Triage Service receives it, **Then** it routes to the Code Review Service.
4. **Given** routing completes, **When** the specialist responds, **Then** the response is published to `learning.responses` Kafka topic within 3 seconds.

---

### User Story 2 - Sandboxed Code Execution (Priority: P1)

A student writes Python code and clicks "Run". The Code Runner Service receives the code, executes it in a sandboxed environment (5s timeout, 50MB memory, no network, standard library only), and returns stdout, stderr, and execution metadata.

**Why this priority**: Code execution is the second pillar of the learning experience. Students need to practice coding.

**Independent Test**: Can be tested by submitting code snippets (valid, error, timeout, memory-exceeding) and verifying correct output and constraint enforcement.

**Acceptance Scenarios**:

1. **Given** valid Python code `print("Hello")`, **When** submitted to Code Runner, **Then** stdout contains "Hello" and execution time is reported.
2. **Given** code with a syntax error, **When** submitted, **Then** stderr contains the traceback and error type.
3. **Given** code with an infinite loop, **When** submitted, **Then** execution is killed after 5 seconds and a timeout message is returned.
4. **Given** code attempting `import requests`, **When** submitted, **Then** a ModuleNotFoundError is returned (network libraries blocked).
5. **Given** code exceeding 50MB memory, **When** submitted, **Then** execution is killed and a memory limit message is returned.

---

### User Story 3 - Struggle Detection and Teacher Alert (Priority: P2)

When a student makes the same type of error 3+ times, is stuck on an exercise for more than 10 minutes, scores below 50% on a quiz, or explicitly says "I don't understand", the system detects a struggle pattern and publishes an alert to the `struggle.detected` Kafka topic for the teacher dashboard.

**Why this priority**: Struggle detection enables proactive teacher intervention, but the core learning loop (US1, US2) must work first.

**Independent Test**: Can be tested by simulating 3+ identical errors and verifying a struggle alert appears on the `struggle.detected` topic.

**Acceptance Scenarios**:

1. **Given** a student triggers 3 NameError exceptions, **When** the Debug Service processes the third error, **Then** a struggle alert is published with `error_type: "NameError"` and `count: 3`.
2. **Given** a student is stuck on an exercise for 10+ minutes, **When** the timer fires, **Then** a struggle alert is published with `type: "stuck_on_exercise"`.
3. **Given** a student says "I don't understand", **When** the Triage Service detects the phrase, **Then** a struggle alert is published immediately.
4. **Given** 5+ consecutive failed code executions, **When** the Code Runner tracks the pattern, **Then** a struggle alert is published.

---

### User Story 4 - Exercise Completion and Mastery Update (Priority: P2)

A student completes a coding exercise. The Exercise Service auto-grades the submission using test cases and returns a score. The Progress Service receives the result, recalculates the topic mastery score using the weighted formula (exercises 40%, quizzes 30%, code quality 20%, streak 10%), and publishes the update.

**Why this priority**: Mastery tracking closes the learning loop and motivates continued engagement, but depends on the exercise and code execution infrastructure.

**Independent Test**: Can be tested by submitting an exercise solution and verifying the grade is returned and mastery score is updated correctly.

**Acceptance Scenarios**:

1. **Given** a student submits a correct solution, **When** the Exercise Service grades it, **Then** a score of 100% is returned with all test cases passing.
2. **Given** a partially correct solution, **When** graded, **Then** the score reflects the percentage of passing test cases with feedback on failures.
3. **Given** a graded exercise, **When** the Progress Service receives the result, **Then** the topic mastery score is recalculated using the weighted formula.
4. **Given** mastery is updated, **When** the student crosses a level threshold (e.g., 40% → 41%), **Then** the new level is recorded and a `progress.updated` event is published.

---

### Edge Cases

- What happens when the OpenAI API is unavailable? Services return a friendly error message with a retry suggestion; the request is not lost (Kafka provides durability).
- What happens when a student sends an empty message? The Triage Service returns a prompt asking the student to describe their question.
- What happens when code execution produces no output? The Code Runner returns "Program executed successfully with no output" with execution time.
- What happens when Dapr sidecar is not available? Services detect missing sidecar and fall back to direct HTTP calls with a warning log.
- What happens when mastery score calculation produces rounding errors? Scores are stored as floats with 2 decimal precision, capped at 0.00 and 100.00.

## Requirements *(mandatory)*

### Functional Requirements

**Triage Service (FR-001 to FR-005)**:
- **FR-001**: System MUST accept student questions via POST `/api/chat` with `{message, session_id, student_id}`.
- **FR-002**: System MUST classify questions using keyword matching with LLM fallback for ambiguous queries.
- **FR-003**: System MUST route to specialist: "explain/how/what" → Concepts, "error/traceback/bug" → Debug, "review/check" → Code Review, "exercise/practice" → Exercise, "progress/score" → Progress.
- **FR-004**: System MUST publish routed questions to `learning.questions` Kafka topic via Dapr pub/sub.
- **FR-005**: System MUST maintain session context for multi-turn conversations.

**Concepts Service (FR-006 to FR-009)**:
- **FR-006**: System MUST explain Python concepts using OpenAI SDK (gpt-4o-mini) with a tutor system prompt.
- **FR-007**: System MUST adapt explanations based on student mastery level (beginner/learning/proficient/mastered).
- **FR-008**: System MUST include runnable Python code examples in responses.
- **FR-009**: System MUST cover 8 modules: Basics, Control Flow, Data Structures, Functions, OOP, Files, Errors, Libraries.

**Code Runner Service (FR-010 to FR-016)**:
- **FR-010**: System MUST accept code via POST `/api/execute` with `{code, student_id}`.
- **FR-011**: System MUST execute code in a sandbox with 5-second timeout.
- **FR-012**: System MUST enforce 50MB memory limit.
- **FR-013**: System MUST block network access during execution.
- **FR-014**: System MUST restrict imports to Python standard library only.
- **FR-015**: System MUST return `{stdout, stderr, execution_time, timed_out, memory_exceeded}`.
- **FR-016**: System MUST publish results to `code.results` Kafka topic.

**Debug Service (FR-017 to FR-021)**:
- **FR-017**: System MUST parse Python tracebacks and identify error type, line number, and root cause.
- **FR-018**: System MUST provide hints BEFORE revealing the full solution.
- **FR-019**: System MUST track error patterns per student using a sliding window.
- **FR-020**: System MUST trigger struggle alert after 3+ same error types.
- **FR-021**: System MUST publish struggle alerts to `struggle.detected` Kafka topic.

**Exercise Service (FR-022 to FR-026)**:
- **FR-022**: System MUST generate exercises of types: fill-in-blank, bug-fix, write-function, output-prediction.
- **FR-023**: System MUST support difficulty levels: easy, medium, hard.
- **FR-024**: System MUST generate exercises appropriate to the student's mastery level.
- **FR-025**: System MUST auto-grade submissions using test cases.
- **FR-026**: System MUST return `{score, test_results[], feedback, passed}`.

**Progress Service (FR-027 to FR-031)**:
- **FR-027**: System MUST calculate mastery using weighted formula: exercises(40%) + quizzes(30%) + code_quality(20%) + streak(10%).
- **FR-028**: System MUST classify mastery levels: 0-40% Beginner (Red), 41-70% Learning (Yellow), 71-90% Proficient (Green), 91-100% Mastered (Blue).
- **FR-029**: System MUST track mastery per topic across 8 Python modules.
- **FR-030**: System MUST use Exponential Moving Average (EMA) for score smoothing.
- **FR-031**: System MUST publish mastery updates to `progress.updated` Kafka topic.

**Cross-Cutting (FR-032 to FR-037)**:
- **FR-032**: All services MUST expose a `/health` endpoint returning `{status, service_name, version}`.
- **FR-033**: All services MUST use Dapr sidecar for pub/sub, state, and service invocation.
- **FR-034**: All services MUST use Pydantic v2 models for request/response validation.
- **FR-035**: All services MUST emit structured JSON logs.
- **FR-036**: All services MUST include a Dockerfile with multi-stage build.
- **FR-037**: All services MUST be stateless; state stored in PostgreSQL via Dapr state store.

### Key Entities

- **Student**: A user with id, email, name, mastery scores per topic, and session history.
- **Session**: A conversation context with session_id, student_id, and ordered message history.
- **Question**: A student query with message text, session context, and routing metadata.
- **CodeSubmission**: Code to execute with student_id, source code, and execution constraints.
- **ExecutionResult**: Sandbox output with stdout, stderr, execution_time, and limit flags.
- **Exercise**: A coding challenge with type, difficulty, description, starter_code, and test_cases.
- **GradeResult**: Auto-grading output with score, per-test results, and feedback.
- **MasteryScore**: Per-topic score with component breakdown (exercises, quizzes, quality, streak).
- **StruggleAlert**: Detection event with student_id, type, pattern details, and confidence.

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: Triage correctly routes 95%+ of queries to the appropriate specialist.
- **SC-002**: Code execution completes within the 5-second timeout for valid programs.
- **SC-003**: Struggle detection fires within 5 seconds of the triggering event.
- **SC-004**: Mastery scores update within 3 seconds of exercise completion.
- **SC-005**: All services start and pass health checks within 10 seconds.
- **SC-006**: All services handle 50 concurrent requests without errors.
- **SC-007**: Specialist agent responses stream back within 3 seconds for simple queries.
- **SC-008**: All 6 services deploy on Minikube within total 3GB RAM budget.

## Assumptions

- OpenAI API key is available as environment variable `OPENAI_API_KEY`.
- gpt-4o-mini is used for cost efficiency in all agent services.
- Kafka and PostgreSQL are already deployed (via infrastructure skills from 002).
- Dapr is installed and components are configured (via 002-k8s-infrastructure).
- Python 3.11+ is the runtime for all backend services.
- FastAPI 0.100+ with Pydantic v2 is the web framework.
- dapr-ext-fastapi package is used for Dapr integration.
- Services run on ports 8001-8006 as defined in the architecture.
