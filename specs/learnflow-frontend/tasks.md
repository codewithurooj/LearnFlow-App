# Tasks: LearnFlow Frontend

**Input**: Design documents from `specs/learnflow-frontend/`
**Prerequisites**: plan.md, spec.md, research.md, data-model.md, contracts/api-client.md

**Tests**: Not explicitly requested in spec. Test tasks omitted.

**Organization**: Tasks grouped by user story for independent implementation and testing.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1, US2)
- All paths relative to `learnflow-app/frontend/`

---

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Initialize Next.js project with all dependencies and configuration

- [ ] T001 Initialize Next.js 14 project with TypeScript strict mode, App Router, and Tailwind CSS in `learnflow-app/frontend/`
- [ ] T002 Install dependencies: `@monaco-editor/react`, `better-auth`, `zustand`, `react-markdown`, `rehype-highlight`, `@better-auth/next`
- [ ] T003 [P] Configure `tsconfig.json` with strict mode and path aliases (`@/` → `src/`)
- [ ] T004 [P] Configure `tailwind.config.ts` with custom mastery level colors (red, yellow, green, blue)
- [ ] T005 [P] Create `.env.example` with `NEXT_PUBLIC_API_URL`, `BETTER_AUTH_SECRET`, `BETTER_AUTH_URL`, `DATABASE_URL`
- [ ] T006 [P] Create `.dockerignore` with `node_modules`, `.next`, `.env.local`
- [ ] T007 [P] Configure ESLint and Prettier for TypeScript strict rules

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Core infrastructure that MUST be complete before ANY user story can be implemented

**CRITICAL**: No user story work can begin until this phase is complete

- [ ] T008 Create all TypeScript interfaces in `src/types/index.ts` (User, ChatMessage, CodeExecutionResult, Exercise, ExerciseResult, ProgressSummary, TopicMastery, TopicDetail, CodeReviewResult, CriterionScore, DebugResult, ClassOverview, StruggleAlert, MasteryLevel)
- [ ] T009 Create base API client with fetch wrapper, error handling, and auth header injection in `src/lib/api.ts`
- [ ] T010 [P] Configure Better Auth server in `src/lib/auth-server.ts` (email/password provider, PostgreSQL adapter, user role field)
- [ ] T011 [P] Configure Better Auth client in `src/lib/auth.ts` (session hooks, sign in/out methods)
- [ ] T012 Create Better Auth API route handler in `src/app/api/auth/[...all]/route.ts`
- [ ] T013 Create auth middleware in `src/middleware.ts` (protect all routes except `/auth/*` and `/api/auth/*`, check teacher role for `/teacher/*`)
- [ ] T014 [P] Create reusable UI components in `src/components/ui/` — Button.tsx, Card.tsx, Input.tsx, Loading.tsx, ErrorMessage.tsx, StarRating.tsx
- [ ] T015 Create Navbar component in `src/components/layout/Navbar.tsx` (logo, nav links, user menu with sign out, role-aware links)
- [ ] T016 Create AuthGuard wrapper component in `src/components/layout/AuthGuard.tsx` (redirect to login if unauthenticated)
- [ ] T017 Create root layout in `src/app/layout.tsx` (Tailwind globals, Navbar, AuthGuard provider, metadata)
- [ ] T018 Create landing page in `src/app/page.tsx` (redirect authenticated users to `/dashboard`, unauthenticated to `/auth/login`)
- [ ] T019 [P] Create health check API route in `src/app/api/health/route.ts` (return service status)

**Checkpoint**: Foundation ready — user story implementation can now begin

---

## Phase 3: User Story 1 — Student Authentication (Priority: P1) MVP

**Goal**: Students can sign up, log in, access protected pages, and sign out

**Independent Test**: Create account → log in → see dashboard → sign out → redirected to login

### Implementation for User Story 1

- [ ] T020 [P] [US1] Create authStore in `src/stores/authStore.ts` (user session state, loading, sign in/out actions)
- [ ] T021 [P] [US1] Create LoginForm component in `src/components/auth/LoginForm.tsx` (email, password fields, submit, error display, link to signup)
- [ ] T022 [P] [US1] Create SignupForm component in `src/components/auth/SignupForm.tsx` (email, password, confirm password, name, submit, error display, link to login)
- [ ] T023 [US1] Create login page in `src/app/auth/login/page.tsx` (render LoginForm, redirect if already authenticated)
- [ ] T024 [US1] Create signup page in `src/app/auth/signup/page.tsx` (render SignupForm, redirect if already authenticated)
- [ ] T025 [US1] Create student dashboard page in `src/app/dashboard/page.tsx` (welcome message with user name, quick navigation cards to Learn, Code, Exercises, Progress)

**Checkpoint**: User Story 1 complete — signup/login/dashboard/signout functional

---

## Phase 4: User Story 3 — Write and Run Code (Priority: P1)

**Goal**: Students write Python code in Monaco editor, run it, and see output

**Independent Test**: Write `print("Hello")` → click Run → see "Hello" in output panel

### Implementation for User Story 3

- [ ] T026 [P] [US3] Create Code Runner API client in `src/lib/api/code-runner.ts` (POST `/api/v1/code/execute`)
- [ ] T027 [P] [US3] Create editorStore in `src/stores/editorStore.ts` (code state, execution results, review results, debug results, localStorage persistence for code via FR-013)
- [ ] T028 [US3] Create CodeEditor component in `src/components/editor/CodeEditor.tsx` (Monaco with dynamic import `ssr: false`, Python language, syntax highlighting, autocompletion, line numbers, minimap)
- [ ] T029 [US3] Create OutputPanel component in `src/components/editor/OutputPanel.tsx` (display stdout, stderr with error highlighting, execution time, timeout message, "no output" message, "Get Help" button on errors)
- [ ] T030 [US3] Create code editor page in `src/app/code/page.tsx` (CodeEditor + Run button + OutputPanel, wire editorStore, load/save code from localStorage)

**Checkpoint**: User Story 3 complete — write code, run, see output, code persists across refresh

---

## Phase 5: User Story 2 — Chat with AI Tutor (Priority: P1)

**Goal**: Students ask Python questions and receive AI responses with formatted code examples

**Independent Test**: Send "How do list comprehensions work?" → see formatted response with code blocks

### Implementation for User Story 2

- [ ] T031 [P] [US2] Create Triage API client in `src/lib/api/triage.ts` (POST `/api/v1/triage/route`)
- [ ] T032 [P] [US2] Create chatStore in `src/stores/chatStore.ts` (messages array, loading state, send message action, session management)
- [ ] T033 [US2] Create ChatMessage component in `src/components/chat/ChatMessage.tsx` (user/assistant bubble, render Markdown with react-markdown, syntax-highlighted code blocks via rehype-highlight, related topics as clickable chips)
- [ ] T034 [US2] Create ChatInput component in `src/components/chat/ChatInput.tsx` (text input, send button, Enter to send, disabled while loading)
- [ ] T035 [US2] Create ChatInterface component in `src/components/chat/ChatInterface.tsx` (message list with auto-scroll, ChatInput at bottom, loading indicator, error with retry)
- [ ] T036 [US2] Create learn page in `src/app/learn/page.tsx` (render ChatInterface, wire chatStore)

**Checkpoint**: User Story 2 complete — send questions, receive formatted AI responses

---

## Phase 6: User Story 4 — Take Coding Exercises (Priority: P2)

**Goal**: Students generate exercises, write solutions, and receive auto-grading feedback

**Independent Test**: Select topic → generate exercise → write solution → submit → see score and feedback

### Implementation for User Story 4

- [ ] T037 [P] [US4] Create Exercise API client in `src/lib/api/exercise.ts` (GET `/api/v1/exercises/generate`, POST `/api/v1/exercises/submit`, GET `/api/v1/exercises/topics`)
- [ ] T038 [P] [US4] Create exerciseStore in `src/stores/exerciseStore.ts` (current exercise, submission state, grading results, available topics)
- [ ] T039 [US4] Create TopicSelector component in `src/components/exercises/TopicSelector.tsx` (topic dropdown grouped by difficulty, difficulty selector, "Generate" button)
- [ ] T040 [US4] Create ExerciseCard component in `src/components/exercises/ExerciseCard.tsx` (title, description in Markdown, starter code pre-filled in Monaco editor, expected output hint)
- [ ] T041 [US4] Create GradingResult component in `src/components/exercises/GradingResult.tsx` (pass/fail badge, score bar, test results list with green/red indicators, feedback in Markdown, "Try Again" and "New Exercise" buttons)
- [ ] T042 [US4] Create exercises page in `src/app/exercises/page.tsx` (TopicSelector → ExerciseCard with embedded Monaco + Submit button → GradingResult, wire exerciseStore)

**Checkpoint**: User Story 4 complete — generate, solve, and grade exercises independently

---

## Phase 7: User Story 5 — Track Learning Progress (Priority: P2)

**Goal**: Students view mastery scores per topic with color-coded levels and breakdowns

**Independent Test**: View progress page → see overall mastery → click topic → see breakdown

### Implementation for User Story 5

- [ ] T043 [P] [US5] Create Progress API client in `src/lib/api/progress.ts` (GET `/api/v1/progress/{studentId}`, GET `/api/v1/progress/{studentId}/topic/{topicId}`)
- [ ] T044 [P] [US5] Create progressStore in `src/stores/progressStore.ts` (summary data, topic details, loading states)
- [ ] T045 [US5] Create MasteryOverview component in `src/components/progress/MasteryOverview.tsx` (overall percentage with circular progress, level badge with color, streak count, total exercises/quizzes)
- [ ] T046 [US5] Create TopicCard component in `src/components/progress/TopicCard.tsx` (topic name, mastery percentage bar with level color — Red: 0-40%, Yellow: 41-70%, Green: 71-90%, Blue: 91-100%, level label, clickable)
- [ ] T047 [US5] Create TopicDetail component in `src/components/progress/TopicDetail.tsx` (modal or slide-over with breakdown: exercises 40%, quizzes 30%, code quality 20%, streak 10% as stacked bar, improvement suggestions list)
- [ ] T048 [US5] Create progress page in `src/app/progress/page.tsx` (MasteryOverview at top, grid of TopicCards, TopicDetail on click, empty state for new students, wire progressStore)

**Checkpoint**: User Story 5 complete — view mastery, drill into topics

---

## Phase 8: User Story 6 — Get Code Review (Priority: P2)

**Goal**: Students get their code reviewed with star ratings and per-criterion feedback

**Independent Test**: Write code → click "Review Code" → see star rating and 4 criterion scores

### Implementation for User Story 6

- [ ] T049 [P] [US6] Create Code Review API client in `src/lib/api/code-review.ts` (POST `/api/v1/review/analyze`)
- [ ] T050 [P] [US6] Create Debug API client in `src/lib/api/debug.ts` (POST `/api/v1/debug/analyze`, POST `/api/v1/debug/solution`)
- [ ] T051 [US6] Create ReviewPanel component in `src/components/editor/ReviewPanel.tsx` (overall star rating using StarRating UI component, 4 criterion scores with individual ratings and feedback, strengths list, suggestions list, encouragement text)
- [ ] T052 [US6] Create DebugPanel component in `src/components/editor/DebugPanel.tsx` (error type badge, error line highlight, root cause explanation, hint text, "Show Solution" button that reveals full solution and corrected code)
- [ ] T053 [US6] Update code editor page `src/app/code/page.tsx` — add "Review Code" button wired to code-review API and ReviewPanel, add "Get Help" button on errors wired to debug API and DebugPanel, update editorStore integration

**Checkpoint**: User Story 6 complete — code review and debug help functional from code editor

---

## Phase 9: User Story 7 — Teacher Dashboard (Priority: P3)

**Goal**: Teachers see class overview, student list, and struggle alerts

**Independent Test**: Log in as teacher → see class stats → see student list → see struggle alerts

### Implementation for User Story 7

- [ ] T054 [P] [US7] Create MCP Context API client in `src/lib/api/mcp-context.ts` (GET `/api/v1/context/class/overview`, GET `/api/v1/context/student/{studentId}/struggles`)
- [ ] T055 [US7] Create ClassOverview component in `src/components/teacher/ClassOverview.tsx` (total students, active students, average mastery gauge, mastery level distribution bar chart)
- [ ] T056 [US7] Create StudentList component in `src/components/teacher/StudentList.tsx` (sortable table with columns: name, overall mastery, level with color, last activity, actions; click to view student detail)
- [ ] T057 [US7] Create StruggleAlert component in `src/components/teacher/StruggleAlert.tsx` (alert card with student name, struggle type icon/label, confidence score, timestamp, expandable detail with recent activity and error patterns)
- [ ] T058 [US7] Create teacher dashboard page in `src/app/teacher/page.tsx` (role guard — redirect non-teachers, ClassOverview at top, StruggleAlert list with polling every 30s via setInterval, StudentList below, wire mcp-context API client)

**Checkpoint**: User Story 7 complete — teacher can monitor class and identify struggling students

---

## Phase 10: Polish & Cross-Cutting Concerns

**Purpose**: Docker integration, dashboard enhancement, navigation, and final integration

- [ ] T059 Create multi-stage Dockerfile in `learnflow-app/frontend/Dockerfile` (Stage 1: `node:18-alpine` install deps, Stage 2: build with `next build`, Stage 3: production with standalone output, expose port 3000)
- [ ] T060 Update student dashboard `src/app/dashboard/page.tsx` — add recent activity summary (latest chat, last exercise, last code run), mastery overview widget pulling from progressStore, quick-action cards linking to each feature
- [ ] T061 [P] Create Sidebar component in `src/components/layout/Sidebar.tsx` (nav links: Dashboard, Learn, Code, Exercises, Progress; active state highlighting; teacher link if role=teacher)
- [ ] T062 Update root layout `src/app/layout.tsx` — integrate Sidebar for authenticated pages, responsive layout with sidebar on left and content area
- [ ] T063 Add `next.config.js` configuration — standalone output mode for Docker, image optimization settings, environment variable validation
- [ ] T064 Verify docker-compose integration — build frontend from `learnflow-app/frontend/Dockerfile`, confirm port 3000 accessible, confirm API calls reach backend services on ports 8001-8008, health check passes
- [ ] T065 Create `learnflow-app/infrastructure/postgres/migrations/` directory with initial schema SQL for Better Auth tables (users, sessions, accounts)

---

## Dependencies & Execution Order

### Phase Dependencies

- **Phase 1 (Setup)**: No dependencies — start immediately
- **Phase 2 (Foundational)**: Depends on Phase 1 completion — BLOCKS all user stories
- **Phases 3-9 (User Stories)**: All depend on Phase 2 completion
  - US1 (Auth): No dependencies on other stories
  - US3 (Code Editor): No dependencies on other stories
  - US2 (Chat): No dependencies on other stories
  - US4 (Exercises): Reuses Monaco from US3 (but can use standalone instance)
  - US5 (Progress): No dependencies on other stories
  - US6 (Code Review + Debug): Depends on US3 (extends code editor page)
  - US7 (Teacher): No dependencies on other stories
- **Phase 10 (Polish)**: Depends on all desired user stories being complete

### User Story Dependencies

- **US1 (Auth)**: Independent — can start after Phase 2
- **US3 (Code Editor)**: Independent — can start after Phase 2
- **US2 (Chat)**: Independent — can start after Phase 2
- **US4 (Exercises)**: Independent — can start after Phase 2 (has own Monaco instance)
- **US5 (Progress)**: Independent — can start after Phase 2
- **US6 (Code Review/Debug)**: Depends on US3 (extends code editor page with new panels)
- **US7 (Teacher)**: Independent — can start after Phase 2

### Within Each User Story

- API client + Store can be created in parallel [P]
- Components depend on types (Phase 2) and store
- Page wires everything together — last task in each story

### Parallel Opportunities

Within Phase 2:
```
Parallel: T010 (auth server) + T011 (auth client) + T014 (UI components) + T019 (health route)
Sequential: T010/T011 → T012 (auth route) → T013 (middleware) → T015-T018 (layout)
```

After Phase 2, user stories can run in parallel:
```
Parallel: US1 (auth) + US3 (code editor) + US2 (chat) + US4 (exercises) + US5 (progress) + US7 (teacher)
Sequential: US3 → US6 (code review extends code editor)
```

---

## Implementation Strategy

### MVP First (P1 Stories Only)

1. Complete Phase 1: Setup
2. Complete Phase 2: Foundational (CRITICAL — blocks all stories)
3. Complete Phase 3: US1 — Authentication
4. Complete Phase 4: US3 — Code Editor
5. Complete Phase 5: US2 — AI Chat
6. **STOP and VALIDATE**: Test all P1 stories independently
7. Deploy/demo if ready — students can sign up, chat, and code

### Incremental Delivery

1. Setup + Foundational → Foundation ready
2. Add US1 (Auth) → Test → Deploy (users can sign up)
3. Add US3 (Code Editor) → Test → Deploy (students can code)
4. Add US2 (Chat) → Test → Deploy (students can learn via AI)
5. Add US4 (Exercises) → Test → Deploy (students can practice)
6. Add US5 (Progress) → Test → Deploy (students see mastery)
7. Add US6 (Review/Debug) → Test → Deploy (enhanced code editor)
8. Add US7 (Teacher) → Test → Deploy (teachers can monitor)
9. Phase 10 (Polish + Docker) → Final integration

### Parallel Team Strategy

With multiple developers after Phase 2:
- Developer A: US1 (Auth) → US6 (Review/Debug after US3 done)
- Developer B: US3 (Code Editor) → US4 (Exercises)
- Developer C: US2 (Chat) → US5 (Progress) → US7 (Teacher)

---

## Summary

| Metric | Count |
|--------|-------|
| **Total tasks** | 65 |
| **Phase 1 (Setup)** | 7 |
| **Phase 2 (Foundational)** | 12 |
| **US1 (Auth)** | 6 |
| **US3 (Code Editor)** | 5 |
| **US2 (Chat)** | 6 |
| **US4 (Exercises)** | 6 |
| **US5 (Progress)** | 6 |
| **US6 (Review/Debug)** | 5 |
| **US7 (Teacher)** | 5 |
| **Phase 10 (Polish)** | 7 |
| **Parallel opportunities** | 22 tasks marked [P] |
| **MVP scope** | Phases 1-5 (US1 + US3 + US2 = 36 tasks) |

## Notes

- [P] tasks = different files, no dependencies
- [Story] label maps task to specific user story for traceability
- Each user story is independently completable and testable
- Commit after each task or logical group
- Stop at any checkpoint to validate story independently
- Monaco editor appears in US3, US4 (exercises), and US6 (review) — each instance is independent
