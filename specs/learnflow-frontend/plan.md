# Implementation Plan: LearnFlow Frontend

**Branch**: `learnflow-frontend` | **Date**: 2026-02-14 | **Spec**: [spec.md](./spec.md)
**Input**: Feature specification from `specs/learnflow-frontend/spec.md`

## Summary

Build a Next.js 14 frontend application for the LearnFlow AI tutoring platform. The application provides authenticated access to an AI chat interface, Monaco-based Python code editor with execution, coding exercises with auto-grading, mastery progress tracking, code review, debug help, and a teacher dashboard with struggle alerts. It connects to 8 existing backend microservices via REST APIs and must be containerized for docker-compose deployment.

## Technical Context

**Language/Version**: TypeScript 5.x (strict mode), Node.js 18+
**Primary Dependencies**: Next.js 14 (App Router), @monaco-editor/react, better-auth, zustand, tailwindcss, react-markdown, rehype-highlight
**Storage**: No frontend database; Better Auth uses backend PostgreSQL for sessions; localStorage for code persistence
**Testing**: Vitest (unit), Playwright (E2E)
**Target Platform**: Modern desktop browsers (Chrome, Firefox, Edge, Safari latest 2 versions), minimum 1024px width
**Project Type**: Web application (frontend only — backend already exists)
**Performance Goals**: Interactive within 3 seconds, API responses rendered within 2 seconds
**Constraints**: Must integrate with existing docker-compose.yml on port 3000; backend services on ports 8001-8008
**Scale/Scope**: 8 pages, ~30 components, 5 Zustand stores, 8 API client modules

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

| Principle | Status | Notes |
|-----------|--------|-------|
| I. Skills-First | PASS | Frontend build/deploy can use `nextjs-k8s-deploy` skill |
| II. Token Efficiency | PASS | No MCP servers loaded at startup in frontend |
| III. Cloud-Native | PASS | Dockerfile with multi-stage build, docker-compose compatible |
| IV. Microservices | PASS | Frontend is a separate service; communicates via REST to microservices |
| V. Security | PASS | Better Auth for authentication; no secrets hardcoded; env vars used |
| VI. SDD | PASS | Spec → Plan → Tasks workflow followed |
| VII. Cross-Agent | PASS | Standard Next.js project; no agent-specific code |
| VIII. Observability | PASS | Health check endpoint at `/api/health`; structured error handling |

**Quality Standards Check**:
- TypeScript strict mode: ENABLED
- ESLint + Prettier: REQUIRED (configured in project)
- React Server Components: Used where applicable (layouts, pages without client state)
- Tailwind CSS: Primary styling approach

## Project Structure

### Documentation (this feature)

```text
specs/learnflow-frontend/
├── plan.md              # This file
├── research.md          # Phase 0 output
├── data-model.md        # Phase 1 output
├── quickstart.md        # Phase 1 output
├── contracts/
│   └── api-client.md    # Phase 1 output
├── checklists/
│   └── requirements.md  # Spec quality checklist
└── tasks.md             # Phase 2 output (created by /sp.tasks)
```

### Source Code

```text
learnflow-app/frontend/
├── Dockerfile
├── .dockerignore
├── .env.example
├── .env.local              # Local dev (gitignored)
├── next.config.js
├── tailwind.config.ts
├── tsconfig.json
├── package.json
├── postcss.config.js
│
├── public/
│   └── favicon.ico
│
├── src/
│   ├── app/                       # Next.js App Router pages
│   │   ├── layout.tsx             # Root layout (providers, nav)
│   │   ├── page.tsx               # Landing → redirect to /dashboard
│   │   ├── auth/
│   │   │   ├── login/page.tsx     # Login form
│   │   │   └── signup/page.tsx    # Signup form
│   │   ├── dashboard/page.tsx     # Student dashboard
│   │   ├── learn/page.tsx         # AI chat interface
│   │   ├── code/page.tsx          # Code editor + runner
│   │   ├── exercises/page.tsx     # Exercise generator + grading
│   │   ├── progress/page.tsx      # Mastery tracking
│   │   ├── teacher/page.tsx       # Teacher dashboard
│   │   └── api/
│   │       ├── health/route.ts    # Health check endpoint
│   │       └── auth/[...all]/route.ts  # Better Auth API routes
│   │
│   ├── components/
│   │   ├── layout/
│   │   │   ├── Navbar.tsx         # Navigation bar with auth state
│   │   │   ├── Sidebar.tsx        # Page sidebar navigation
│   │   │   └── AuthGuard.tsx      # Route protection wrapper
│   │   ├── auth/
│   │   │   ├── LoginForm.tsx      # Email/password login
│   │   │   └── SignupForm.tsx     # Registration form
│   │   ├── chat/
│   │   │   ├── ChatInterface.tsx  # Full chat UI
│   │   │   ├── ChatMessage.tsx    # Single message bubble
│   │   │   └── ChatInput.tsx      # Message input with send
│   │   ├── editor/
│   │   │   ├── CodeEditor.tsx     # Monaco wrapper (dynamic import)
│   │   │   ├── OutputPanel.tsx    # Execution results display
│   │   │   ├── ReviewPanel.tsx    # Code review results
│   │   │   └── DebugPanel.tsx     # Debug help results
│   │   ├── exercises/
│   │   │   ├── ExerciseCard.tsx   # Exercise display
│   │   │   ├── TopicSelector.tsx  # Topic + difficulty picker
│   │   │   └── GradingResult.tsx  # Submission results
│   │   ├── progress/
│   │   │   ├── MasteryOverview.tsx    # Overall mastery summary
│   │   │   ├── TopicCard.tsx          # Per-topic mastery card
│   │   │   └── TopicDetail.tsx        # Drill-down breakdown
│   │   ├── teacher/
│   │   │   ├── ClassOverview.tsx      # Aggregated class stats
│   │   │   ├── StudentList.tsx        # Sortable student table
│   │   │   └── StruggleAlert.tsx      # Alert notification card
│   │   └── ui/
│   │       ├── Button.tsx
│   │       ├── Card.tsx
│   │       ├── Input.tsx
│   │       ├── Loading.tsx
│   │       ├── ErrorMessage.tsx
│   │       └── StarRating.tsx
│   │
│   ├── lib/
│   │   ├── auth.ts            # Better Auth client configuration
│   │   ├── auth-server.ts     # Better Auth server configuration
│   │   ├── api.ts             # Base API client (fetch wrapper)
│   │   └── api/
│   │       ├── triage.ts      # Triage service client
│   │       ├── concepts.ts    # Concepts service client
│   │       ├── code-runner.ts # Code Runner client
│   │       ├── debug.ts       # Debug service client
│   │       ├── exercise.ts    # Exercise service client
│   │       ├── progress.ts    # Progress service client
│   │       ├── code-review.ts # Code Review client
│   │       └── mcp-context.ts # MCP Context client (teacher)
│   │
│   ├── stores/
│   │   ├── authStore.ts       # User session state
│   │   ├── chatStore.ts       # Chat messages, loading
│   │   ├── editorStore.ts     # Code, results, review, debug
│   │   ├── exerciseStore.ts   # Current exercise, submission
│   │   └── progressStore.ts   # Mastery data
│   │
│   ├── types/
│   │   └── index.ts           # All TypeScript interfaces
│   │
│   └── middleware.ts          # Auth + role-based route protection
│
├── e2e/
│   ├── auth.spec.ts           # Login/signup E2E tests
│   ├── chat.spec.ts           # Chat interaction tests
│   └── code-editor.spec.ts   # Code execution tests
│
└── vitest.config.ts
```

**Structure Decision**: Web application with frontend-only scope. The `learnflow-app/frontend/` directory is created as a self-contained Next.js project that integrates with the existing `learnflow-app/backend/` services via the docker-compose.yml already defined at the `learnflow-app/` root.

## Implementation Phases

### Phase A: Project Scaffolding & Auth (P1 - User Story 1)

1. Initialize Next.js 14 project with TypeScript strict mode, Tailwind CSS, ESLint
2. Configure Better Auth (server + client) with email/password
3. Create auth pages (login, signup) and API route handler
4. Create middleware for route protection and role checking
5. Create root layout with Navbar and AuthGuard
6. Create Dockerfile (multi-stage) and .env.example
7. Verify: user can sign up, log in, access dashboard, sign out

### Phase B: Code Editor & Execution (P1 - User Story 3)

1. Create Monaco Editor component with dynamic import (SSR disabled)
2. Create output panel for stdout/stderr/timeout display
3. Create Code Runner API client
4. Wire editor → run button → API → output panel
5. Implement localStorage code persistence (FR-013)
6. Verify: write code, run, see output; code survives refresh

### Phase C: AI Chat Interface (P1 - User Story 2)

1. Create Triage API client
2. Create chat components (ChatInterface, ChatMessage, ChatInput)
3. Implement Zustand chatStore with message history
4. Render Markdown responses with syntax-highlighted code blocks (react-markdown + rehype-highlight)
5. Add loading states and error handling with retry
6. Verify: send question, receive formatted response with code examples

### Phase D: Exercises & Grading (P2 - User Story 4)

1. Create Exercise API client
2. Create topic/difficulty selector component
3. Create exercise display with embedded Monaco editor
4. Implement submission and grading result display
5. Verify: generate exercise, submit solution, see score and feedback

### Phase E: Progress Tracking (P2 - User Story 5)

1. Create Progress API client
2. Create mastery overview with color-coded levels
3. Create topic cards and detail drill-down
4. Implement mastery level colors (Red/Yellow/Green/Blue)
5. Verify: view overall mastery, drill into topics, see breakdowns

### Phase F: Code Review & Debug Help (P2 - User Stories 6 & 3.4)

1. Create Code Review and Debug API clients
2. Add "Review Code" button and ReviewPanel to code editor page
3. Add "Get Help" button on errors and DebugPanel
4. Implement star rating display and criterion scores
5. Verify: submit for review, see ratings; click help on error, see hints

### Phase G: Teacher Dashboard (P3 - User Story 7)

1. Create MCP Context API client
2. Create ClassOverview component with aggregated stats
3. Create StudentList with sorting
4. Create StruggleAlert cards with polling (30s interval)
5. Add role guard (teacher-only access)
6. Verify: teacher sees class data, struggle alerts appear

### Phase H: Integration & Docker (All)

1. Create student dashboard page with summary widgets
2. Add navigation between all pages
3. Test docker-compose build and startup with all services
4. Verify all docker-compose health checks pass
5. End-to-end flow: signup → chat → code → exercise → progress

## Complexity Tracking

No constitution violations detected. All design decisions align with the mandated technology stack and architectural principles.

## Risks

1. **Monaco Editor bundle size**: Monaco adds ~2MB to the client bundle. Mitigated by dynamic import and code splitting — only loaded on pages that use it.
2. **Better Auth + PostgreSQL**: Better Auth needs database access for session storage. The frontend's Dockerfile must include the DATABASE_URL env var pointing to the shared PostgreSQL instance.
3. **CORS in docker-compose**: Frontend (port 3000) calling backends (ports 8001-8008) requires CORS. Already configured in all backend services.
