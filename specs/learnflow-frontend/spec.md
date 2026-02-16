# Feature Specification: LearnFlow Frontend

**Feature Branch**: `learnflow-frontend`
**Created**: 2026-02-14
**Status**: Draft
**Input**: User description: "LearnFlow Frontend - Next.js 14 application with App Router, TypeScript strict mode, Monaco Editor for in-browser Python coding, Better Auth for authentication, Zustand for state management, Tailwind CSS for styling. Pages: auth (login/signup), student dashboard, code editor with Monaco, learn/chat with AI tutors, quizzes, progress tracking, teacher dashboard with struggle alerts. Connects to backend microservices: triage (8001), concepts (8002), code-runner (8003), debug (8004), exercise (8005), progress (8006), code-review (8007). Must include Dockerfile for docker-compose integration."

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Student Authentication (Priority: P1)

A new student visits LearnFlow and creates an account with email and password. An existing student logs in to resume their learning session. After authentication, the student is redirected to their personal dashboard.

**Why this priority**: Authentication is the gateway to all other features. Without it, no personalized learning experience is possible.

**Independent Test**: Can be fully tested by creating an account, logging in, and verifying the student reaches the dashboard with their identity preserved across page refreshes.

**Acceptance Scenarios**:

1. **Given** a new visitor, **When** they fill in email, password, and confirm password on the signup page, **Then** an account is created and they are redirected to the student dashboard.
2. **Given** an existing student, **When** they enter valid credentials on the login page, **Then** they are authenticated and redirected to the student dashboard.
3. **Given** an unauthenticated user, **When** they attempt to access any protected page, **Then** they are redirected to the login page.
4. **Given** an authenticated student, **When** they click "Sign Out", **Then** their session is ended and they are redirected to the login page.

---

### User Story 2 - Chat with AI Tutor (Priority: P1)

A student navigates to the Learn page and types a Python question (e.g., "How do list comprehensions work?"). The system routes the question to the appropriate AI specialist and displays a conversational response with code examples. The student can continue the conversation for follow-up questions.

**Why this priority**: The AI chat is the core learning experience of the platform. It delivers the primary value proposition.

**Independent Test**: Can be tested by sending a question and verifying a contextual response appears in the chat interface with code examples rendered properly.

**Acceptance Scenarios**:

1. **Given** an authenticated student on the Learn page, **When** they type a question and press send, **Then** the question appears in the chat and a loading indicator is shown while waiting for a response.
2. **Given** a question has been sent, **When** the AI responds, **Then** the response is displayed with properly formatted text, code blocks with syntax highlighting, and related topic suggestions.
3. **Given** an ongoing conversation, **When** the student asks a follow-up question, **Then** the response takes the conversation history into account.
4. **Given** a network error occurs, **When** the student sends a question, **Then** a user-friendly error message is displayed with a retry option.

---

### User Story 3 - Write and Run Code (Priority: P1)

A student opens the Code Editor page and writes Python code in a full-featured editor with syntax highlighting, autocompletion, and line numbers. They click "Run" to execute the code and see the output (stdout/stderr) in a results panel below the editor.

**Why this priority**: Hands-on coding is essential to learning programming. The code editor is the second pillar of the learning experience alongside AI chat.

**Independent Test**: Can be tested by writing a simple Python program (e.g., `print("Hello")`), running it, and verifying "Hello" appears in the output panel.

**Acceptance Scenarios**:

1. **Given** a student on the Code Editor page, **When** the page loads, **Then** a Monaco editor is displayed with Python syntax highlighting, line numbers, and autocompletion enabled.
2. **Given** code is written in the editor, **When** the student clicks "Run", **Then** the code is sent for execution and a loading indicator is shown.
3. **Given** code executes successfully, **When** results return, **Then** stdout is displayed in the output panel with execution time.
4. **Given** code has an error, **When** results return, **Then** stderr is displayed with the error message highlighted, and a "Get Help" button is available to send the error to the Debug agent.
5. **Given** code exceeds the 5-second timeout, **When** results return, **Then** a timeout message is displayed explaining the execution limit.

---

### User Story 4 - Take Coding Exercises (Priority: P2)

A student navigates to the Exercises page, selects a topic and difficulty level, and receives a generated coding challenge. They write a solution in the embedded editor and submit it for auto-grading. They receive a score, test results, and feedback.

**Why this priority**: Exercises reinforce learning and contribute to mastery tracking. Important for engagement but requires chat and code execution to be functional first.

**Independent Test**: Can be tested by generating an exercise, submitting a solution, and verifying the grading response shows score, pass/fail for test cases, and feedback.

**Acceptance Scenarios**:

1. **Given** a student on the Exercises page, **When** they select a topic and difficulty, **Then** a coding exercise is generated with a title, description, and optional starter code.
2. **Given** an exercise is displayed, **When** the student writes code and clicks "Submit", **Then** the solution is graded and results are shown (score, test case pass/fail, feedback).
3. **Given** the student passes an exercise, **When** results are shown, **Then** a success message is displayed and the student can generate a new exercise.
4. **Given** the student fails an exercise, **When** results are shown, **Then** feedback highlights what went wrong and hints are provided without revealing the full solution.

---

### User Story 5 - Track Learning Progress (Priority: P2)

A student visits the Progress page and sees an overview of their mastery across all Python topics. Each topic shows a mastery percentage, color-coded level (Beginner/Learning/Proficient/Mastered), and breakdown of contributing factors. The student can drill into individual topics for detailed progress.

**Why this priority**: Progress visibility motivates continued learning and helps students identify weak areas.

**Independent Test**: Can be tested by viewing the progress page after completing some exercises and verifying mastery scores, levels, and color coding are displayed correctly.

**Acceptance Scenarios**:

1. **Given** a student on the Progress page, **When** the page loads, **Then** an overall mastery score is displayed along with current streak and total activity counts.
2. **Given** progress data exists, **When** topics are rendered, **Then** each topic shows mastery percentage, level name, and the corresponding color (Red: 0-40%, Yellow: 41-70%, Green: 71-90%, Blue: 91-100%).
3. **Given** a student clicks on a topic, **When** the detail view opens, **Then** a breakdown is shown (exercises 40%, quizzes 30%, code quality 20%, streak 10%) with improvement suggestions.

---

### User Story 6 - Get Code Review (Priority: P2)

A student submits code for review from the Code Editor. The AI reviews the code against correctness, style (PEP 8), efficiency, and readability criteria. Results are displayed as a star rating (1-5) with per-criterion scores and actionable suggestions.

**Why this priority**: Code review teaches best practices and contributes to mastery scoring. Enhances the code editor experience.

**Independent Test**: Can be tested by submitting code and verifying a review response with overall rating, four criterion scores, and suggestions is displayed.

**Acceptance Scenarios**:

1. **Given** code in the editor, **When** the student clicks "Review Code", **Then** the code is sent to the review service and a loading indicator is shown.
2. **Given** a review is complete, **When** results are displayed, **Then** an overall star rating (1-5) and per-criterion scores (correctness, style, efficiency, readability) are shown with feedback for each.
3. **Given** a review has suggestions, **When** the student views results, **Then** a list of strengths and actionable improvement suggestions are displayed.

---

### User Story 7 - Teacher Dashboard (Priority: P3)

A teacher logs in and accesses the Teacher Dashboard. They see a class overview with aggregated progress data, a list of students with their mastery levels, and real-time struggle alerts. When a student struggles (same error 3+ times, stuck >10 min, quiz <50%), the teacher receives a highlighted alert.

**Why this priority**: Teacher features are secondary to the core student experience but essential for classroom adoption.

**Independent Test**: Can be tested by viewing the teacher dashboard and verifying class overview data, student list, and struggle alerts are displayed.

**Acceptance Scenarios**:

1. **Given** a teacher is authenticated, **When** they navigate to the Teacher Dashboard, **Then** a class overview is displayed with aggregated mastery data and active student count.
2. **Given** students are enrolled, **When** the dashboard loads, **Then** a sortable list of students is shown with name, overall mastery, level, and last activity.
3. **Given** a student triggers a struggle condition, **When** the alert is received, **Then** a highlighted notification appears on the dashboard with the student name, struggle type, and timestamp.
4. **Given** a teacher clicks on a struggle alert, **When** the detail view opens, **Then** the student's recent activity, error patterns, and suggested interventions are shown.

---

### Edge Cases

- What happens when the backend services are unavailable? The frontend displays a connection error with service status and retry options.
- What happens when a student's session expires mid-activity? The frontend detects the expired session, preserves any unsaved code in local storage, and redirects to login with a message to re-authenticate.
- What happens when code execution returns no output? The output panel displays "Program executed successfully with no output" with the execution time.
- What happens when a student has no progress data? The Progress page shows a welcome state with suggested starting topics.
- What happens when the Monaco editor fails to load? A fallback plain textarea is displayed with a warning that advanced features are unavailable.

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: System MUST provide signup and login pages using Better Auth with email/password authentication.
- **FR-002**: System MUST protect all pages except login and signup behind authentication, redirecting unauthenticated users to login.
- **FR-003**: System MUST provide a student dashboard showing a summary of recent activity, mastery overview, and quick navigation to all features.
- **FR-004**: System MUST embed a Monaco Editor configured for Python with syntax highlighting, autocompletion, line numbers, and minimap.
- **FR-005**: System MUST send code to the Code Runner service (port 8003) for execution and display stdout, stderr, execution time, and timeout status in an output panel.
- **FR-006**: System MUST provide a chat interface that sends questions to the Triage service (port 8001) and renders responses with Markdown formatting and syntax-highlighted code blocks.
- **FR-007**: System MUST display conversation history within a session and support follow-up questions.
- **FR-008**: System MUST provide an Exercises page where students select a topic and difficulty to generate exercises from the Exercise service (port 8005) and submit solutions for auto-grading.
- **FR-009**: System MUST provide a Progress page displaying per-topic mastery scores, levels, color coding, and a detailed breakdown view using data from the Progress service (port 8006).
- **FR-010**: System MUST provide a "Review Code" action in the Code Editor that sends code to the Code Review service (port 8007) and displays star ratings, per-criterion scores, and suggestions.
- **FR-011**: System MUST provide a "Get Help" action on code errors that sends the code and error to the Debug service (port 8004) and displays hints before full solutions.
- **FR-012**: System MUST provide a Teacher Dashboard accessible to teacher-role users showing class overview, student list with mastery levels, and struggle alerts.
- **FR-013**: System MUST persist unsaved code in local storage so it survives page refreshes and session re-authentication.
- **FR-014**: System MUST include a Dockerfile and be compatible with the existing docker-compose.yml (exposed on port 3000, connecting to backend services).
- **FR-015**: System MUST be responsive and functional on desktop browsers (minimum 1024px width).

### Key Entities

- **Student**: A learner with an account, mastery scores per topic, exercise history, and chat sessions. Has a unique ID (UUID), email, and display name.
- **Teacher**: A user with elevated permissions who monitors class progress and receives struggle alerts. Distinguished by role.
- **Chat Session**: A conversation between a student and AI tutor containing ordered messages with text and optional code blocks.
- **Exercise**: A generated coding challenge with title, description, starter code, and expected behavior. Has a unique ID and is associated with a topic and difficulty.
- **Progress Record**: A per-topic mastery score for a student, composed of exercise (40%), quiz (30%), code quality (20%), and streak (10%) components.
- **Struggle Alert**: A notification triggered when a student meets struggle criteria, containing student ID, struggle type, confidence score, and timestamp.

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: Students can create an account and reach the dashboard in under 60 seconds.
- **SC-002**: Students can write code, run it, and see output in under 3 seconds (excluding code execution time).
- **SC-003**: Students can ask a question and see an AI response begin streaming in under 2 seconds.
- **SC-004**: Students can generate an exercise, write a solution, and receive grading feedback in a single uninterrupted flow.
- **SC-005**: Progress page renders all topic mastery data with correct color coding within 2 seconds of navigation.
- **SC-006**: Teachers can identify struggling students within 10 seconds of viewing the dashboard.
- **SC-007**: The application loads and becomes interactive within 3 seconds on a standard broadband connection.
- **SC-008**: All core flows (auth, chat, code, exercises, progress) are functional when deployed via docker-compose alongside backend services.

## Assumptions

- Better Auth is used for authentication with email/password (no SSO/OAuth in MVP).
- The frontend communicates directly with backend services via HTTP REST (through the API URL configured as environment variable), not through Kafka.
- Teacher vs student role distinction is handled via a role field on the user record managed by Better Auth.
- The Monaco Editor is loaded client-side only (not SSR compatible) using dynamic imports.
- The frontend does not implement real-time WebSocket connections in MVP; struggle alerts on the teacher dashboard are fetched via polling or on page load.
- Standard library Python imports only are supported in code execution (per sandbox rules).
- The frontend targets modern evergreen browsers (Chrome, Firefox, Edge, Safari latest 2 versions).
