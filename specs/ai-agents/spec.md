# Feature Specification: LearnFlow AI Agent System

**Feature Branch**: `005-ai-agents`
**Created**: 2026-01-25
**Status**: Draft
**Input**: User description: "Create specification for LearnFlow AI agent system. Multi-agent architecture with specialist agents. OpenAI SDK for LLM interactions. Agents communicate via Kafka topics."

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Triage Correctly Routes Queries (Priority: P0)

The Triage Agent receives a student message and routes it to the correct specialist agent with 95%+ accuracy. Routing uses keyword matching as primary strategy with LLM-based classification as fallback for ambiguous queries.

**Why this priority**: Triage is the entry point for all student interactions. Incorrect routing degrades the entire learning experience.

**Independent Test**: Can be tested by sending 20+ diverse queries (explain, error, review, exercise, progress) and measuring routing accuracy.

**Acceptance Scenarios**:

1. **Given** a student asks "How do dictionaries work in Python?", **When** the Triage Agent processes it, **Then** it routes to the Concepts Agent with confidence > 0.8.
2. **Given** a student sends "I keep getting IndexError", **When** processed, **Then** it routes to the Debug Agent.
3. **Given** an ambiguous message "Help me with my code", **When** keyword matching is inconclusive, **Then** LLM classification is used as fallback.
4. **Given** a student asks "What's my progress on OOP?", **When** processed, **Then** it routes to the Progress Agent.
5. **Given** 20 diverse test queries, **When** routed, **Then** at least 19 (95%) reach the correct specialist.

---

### User Story 2 - Concepts Agent Adapts to Student Level (Priority: P0)

The Concepts Agent explains Python concepts with examples tailored to the student's mastery level. A beginner gets simple explanations with basic examples; a proficient student gets advanced patterns and edge cases.

**Why this priority**: Adaptive teaching is the core value proposition of the AI tutoring system.

**Independent Test**: Can be tested by querying the same topic ("loops") with different mastery levels and verifying response complexity adapts appropriately.

**Acceptance Scenarios**:

1. **Given** a beginner student asks about loops, **When** the Concepts Agent responds, **Then** the explanation uses simple vocabulary, basic `for` loop examples, and avoids advanced concepts.
2. **Given** a proficient student asks about loops, **When** the Concepts Agent responds, **Then** it covers list comprehensions, generator expressions, and performance considerations.
3. **Given** any mastery level, **When** the Concepts Agent responds, **Then** the response includes at least one runnable Python code example.
4. **Given** the 8 Python modules, **When** any module topic is queried, **Then** the Concepts Agent provides accurate, relevant content.

---

### User Story 3 - Debug Agent Detects Struggle and Alerts Teacher (Priority: P1)

The Debug Agent parses Python tracebacks, provides progressive hints (hints before solutions), and tracks error patterns. When a student makes the same error type 3+ times, a struggle alert is published to `struggle.detected` for the teacher dashboard.

**Why this priority**: Struggle detection enables teacher intervention, a key differentiator for classroom adoption.

**Independent Test**: Can be tested by submitting 3 identical error types for a student and verifying a struggle alert is published.

**Acceptance Scenarios**:

1. **Given** a student submits code with a NameError, **When** the Debug Agent processes it, **Then** it identifies the error type, line number, and provides a hint without revealing the fix.
2. **Given** a student requests "show me the solution", **When** after receiving the hint, **Then** the Debug Agent provides the full explanation and fix.
3. **Given** a student triggers 3 NameError exceptions, **When** the third error is processed, **Then** a struggle alert `{student_id, error_type: "NameError", count: 3, timestamp}` is published.
4. **Given** a struggle alert is published, **When** the teacher dashboard receives it, **Then** the alert includes the student's recent error history and suggested intervention.

---

### User Story 4 - Exercise Agent Generates Appropriate Difficulty (Priority: P1)

The Exercise Agent generates coding exercises based on the student's topic selection and mastery level. It selects appropriate difficulty (easy for beginners, hard for proficient) and exercise type. Submissions are auto-graded with test cases.

**Why this priority**: Exercises reinforce learning and drive mastery progression.

**Independent Test**: Can be tested by requesting exercises at different mastery levels and verifying difficulty and complexity scale appropriately.

**Acceptance Scenarios**:

1. **Given** a beginner student requests a "loops" exercise, **When** the Exercise Agent generates it, **Then** the exercise is easy difficulty with a fill-in-blank or output-prediction type.
2. **Given** a proficient student requests a "loops" exercise, **When** generated, **Then** the exercise is medium/hard difficulty with a write-function or bug-fix type.
3. **Given** a student submits a solution, **When** auto-graded, **Then** each test case result (pass/fail) and an overall score are returned.
4. **Given** a failed submission, **When** feedback is generated, **Then** hints identify which test cases failed without revealing the expected output.

---

### User Story 5 - Code Review Agent Provides Quality Feedback (Priority: P2)

The Code Review Agent analyzes student code for correctness, PEP 8 style, efficiency, and readability. It provides a star rating (1-5) per criterion and overall, with encouraging feedback and actionable improvement suggestions.

**Why this priority**: Code review teaches best practices but is not critical for the core learning loop.

**Independent Test**: Can be tested by submitting code of varying quality and verifying ratings and suggestions match expected assessments.

**Acceptance Scenarios**:

1. **Given** clean, efficient code, **When** reviewed, **Then** the overall rating is 4-5 stars with specific praise.
2. **Given** code with PEP 8 violations, **When** reviewed, **Then** the style criterion scores low with specific line references.
3. **Given** any code submission, **When** reviewed, **Then** the response includes: overall rating, 4 criterion scores, strengths, and improvement suggestions.

---

### User Story 6 - Progress Agent Tracks Mastery and Celebrates Milestones (Priority: P2)

The Progress Agent tracks per-topic mastery scores using the weighted formula, provides progress summaries, and celebrates milestones (e.g., reaching "Proficient" level).

**Why this priority**: Progress tracking motivates learning but depends on exercises and grading being functional.

**Independent Test**: Can be tested by simulating exercise completions and verifying mastery scores calculate correctly and milestones trigger.

**Acceptance Scenarios**:

1. **Given** a student completes an exercise on "loops" scoring 80%, **When** the Progress Agent updates, **Then** the loops mastery score increases using the weighted EMA formula.
2. **Given** a student's mastery crosses 71% on a topic, **When** the level changes from "Learning" to "Proficient", **Then** a milestone celebration message is generated.
3. **Given** a student requests their progress, **When** the Progress Agent responds, **Then** a summary shows all 8 topic mastery scores, levels, and an overall average.

---

### Edge Cases

- What happens when the OpenAI API rate limits the agent? The agent retries with exponential backoff (max 3 retries) and returns a friendly "I'm thinking..." message.
- What happens when a student sends code in a non-Python language? The Triage Agent detects non-Python and suggests the student write Python code.
- What happens when the Debug Agent cannot parse a traceback? It asks the student to share the full error message and provides general debugging tips.
- What happens when exercise auto-grading times out? The Exercise Agent returns partial results with available test case outcomes.
- What happens when mastery data is missing for a new student? All topics start at 0% (Beginner level) and the Progress Agent provides a welcome message with suggested starting topics.

## Requirements *(mandatory)*

### Functional Requirements

**Triage Agent (FR-001 to FR-003)**:
- **FR-001**: System MUST classify student queries using keyword matching (primary) with LLM fallback (secondary).
- **FR-002**: System MUST route to 5 specialists: Concepts, Debug, Code Review, Exercise, Progress.
- **FR-003**: System MUST achieve 95%+ routing accuracy across standard query types.

**Concepts Agent (FR-004 to FR-006)**:
- **FR-004**: System MUST adapt explanation complexity based on student mastery level.
- **FR-005**: System MUST include runnable Python code examples in every response.
- **FR-006**: System MUST cover 8 Python modules: Basics, Control Flow, Data Structures, Functions, OOP, Files, Errors, Libraries.

**Debug Agent (FR-007 to FR-009)**:
- **FR-007**: System MUST parse Python tracebacks and identify error type, line, and root cause.
- **FR-008**: System MUST provide hints before full solutions (progressive disclosure).
- **FR-009**: System MUST publish struggle alert to `struggle.detected` after 3+ same error types.

**Code Review Agent (FR-010 to FR-011)**:
- **FR-010**: System MUST evaluate code on 4 criteria: correctness, PEP 8 style, efficiency, readability.
- **FR-011**: System MUST provide star rating (1-5) per criterion and overall with actionable feedback.

**Exercise Agent (FR-012 to FR-014)**:
- **FR-012**: System MUST generate 4 exercise types: fill-in-blank, bug-fix, write-function, output-prediction.
- **FR-013**: System MUST select difficulty (easy/medium/hard) based on student mastery level.
- **FR-014**: System MUST auto-grade with test cases and return per-test results.

**Progress Agent (FR-015 to FR-017)**:
- **FR-015**: System MUST calculate mastery: exercises(40%) + quizzes(30%) + code_quality(20%) + streak(10%).
- **FR-016**: System MUST classify levels: 0-40% Beginner, 41-70% Learning, 71-90% Proficient, 91-100% Mastered.
- **FR-017**: System MUST detect and celebrate milestone transitions (level changes).

### Key Entities

- **AgentConfig**: Configuration for each agent including model, system prompt path, temperature, and max tokens.
- **RoutingDecision**: Triage output with target agent, confidence score, and matched keywords.
- **StudentSession**: Conversation context with student_id, session_id, message history, and mastery level.
- **Message**: A chat message with role (student/agent), content, code blocks, and timestamp.
- **StudentStruggleState**: Per-student error tracking with sliding window of recent errors.
- **ErrorRecord**: Parsed error with type, line number, context, and timestamp.
- **StruggleAlert**: Detection event with student_id, struggle type, confidence, and error history.
- **Exercise**: Generated challenge with type, difficulty, description, starter_code, and test_cases.
- **TestCase**: A test with input, expected_output, and name for auto-grading.
- **GradeResult**: Grading output with score, per-test results, and feedback text.
- **MasteryScore**: Per-topic score with exercise, quiz, quality, and streak components.
- **ProgressSummary**: All-topic overview with mastery scores, levels, overall average, and streak.

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: Triage routes 95%+ of queries correctly across 50+ test cases.
- **SC-002**: Concepts Agent adapts responses measurably between beginner and proficient levels.
- **SC-003**: Debug Agent identifies error type and line number in 90%+ of standard Python tracebacks.
- **SC-004**: Struggle detection fires within 5 seconds of the third same-type error.
- **SC-005**: Exercise auto-grading produces correct scores for known test cases.
- **SC-006**: Code Review ratings are consistent (same code scores within 0.5 stars across runs).
- **SC-007**: Mastery calculation matches expected values using the weighted formula.
- **SC-008**: All agents respond within 5 seconds for standard queries.
- **SC-009**: System prompts load from external markdown files (not hardcoded).
- **SC-010**: All agents function as independent FastAPI microservices with Dapr sidecars.

## Assumptions

- OpenAI API key is available and gpt-4o-mini is the default model for cost efficiency.
- OpenAI Agents SDK is used for multi-agent orchestration with handoffs.
- Each agent runs as a separate FastAPI microservice with Dapr sidecar.
- System prompts are stored as external markdown files for easy iteration.
- Kafka topics from infrastructure (002) are available for inter-agent communication.
- PostgreSQL from infrastructure (002) stores state via Dapr state store.
- Code Review Agent runs on port 8007 as a 7th microservice.
- Python 3.11+ runtime for all agent services.
