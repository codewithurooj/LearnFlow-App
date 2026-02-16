# Research: LearnFlow Frontend

**Date**: 2026-02-14
**Feature**: learnflow-frontend
**Spec**: [spec.md](./spec.md)

## R1: Better Auth Integration with Next.js 14

**Decision**: Use Better Auth with its official Next.js adapter (`@better-auth/next`). Authentication state managed via session cookies. Better Auth handles signup/login/logout endpoints automatically.

**Rationale**: Better Auth is specified in the constitution's technology stack as mandatory. It provides built-in Next.js App Router support, session management, and email/password authentication out of the box, minimizing custom auth code.

**Alternatives considered**:
- NextAuth.js: More established but not in the technology stack; would require constitution amendment
- Custom JWT: Higher maintenance, more security risk in MVP

## R2: Monaco Editor in Next.js (SSR Compatibility)

**Decision**: Use `@monaco-editor/react` package with Next.js `dynamic()` import and `ssr: false`. The editor component is a client component (`"use client"` directive) that loads only in the browser.

**Rationale**: Monaco Editor requires browser APIs (DOM, Web Workers) and cannot render server-side. Dynamic import with SSR disabled is the standard pattern for Next.js App Router. The `@monaco-editor/react` wrapper provides a React-friendly API with built-in loading states.

**Alternatives considered**:
- CodeMirror 6: Lighter weight but less feature-rich; Monaco specified in requirements
- Ace Editor: Older, fewer features than Monaco

## R3: State Management with Zustand

**Decision**: Use Zustand for client-side state with these stores:
- `authStore`: Current user session, role
- `chatStore`: Active chat session messages, loading state
- `editorStore`: Current code, language, execution results
- `exerciseStore`: Current exercise, submission state
- `progressStore`: Mastery data, topic details

**Rationale**: Zustand is lightweight (~1KB), has no boilerplate, works with React Server Components (stores are client-only), and persists state easily via middleware (localStorage for code persistence per FR-013).

**Alternatives considered**:
- Redux Toolkit: Heavier, more boilerplate for this app size
- React Context: Sufficient for small state but doesn't handle complex derived state well

## R4: API Communication Pattern

**Decision**: Create a centralized API client (`lib/api.ts`) using `fetch` with the base URL from `NEXT_PUBLIC_API_URL` environment variable. Each backend service gets a typed client module. The frontend communicates via HTTP REST directly to backend services (routed through the triage service for chat, directly to individual services for other endpoints).

**Rationale**: The spec states frontend communicates via HTTP REST, not Kafka. A centralized client ensures consistent error handling, auth header injection, and type safety. The triage service (port 8001) is the primary entry point for chat; other services are called directly for their specific functions.

**Alternatives considered**:
- GraphQL gateway: Over-engineering for MVP; backend is REST
- tRPC: Requires backend changes; backend is Python/FastAPI

## R5: Struggle Alert Delivery to Teacher Dashboard

**Decision**: Use polling (30-second interval) via `setInterval` + `fetch` to the MCP Context server's `/class/overview` endpoint. Display a notification badge count that updates on each poll.

**Rationale**: The spec assumes no WebSocket connections in MVP. Polling is simpler to implement and sufficient for a teacher dashboard that doesn't need sub-second updates. The MCP Context server (port 8008) already provides aggregated class data including struggles.

**Alternatives considered**:
- Server-Sent Events: Better UX but requires backend changes not in scope
- WebSockets: Full-duplex but over-engineering for MVP

## R6: Role-Based Access Control (Student vs Teacher)

**Decision**: Better Auth user records include a `role` field (`student` | `teacher`). Middleware checks the role from the session on protected routes. Teacher dashboard routes (`/teacher/*`) are guarded by role check. Student routes are the default for authenticated users.

**Rationale**: Simple role field is sufficient for MVP with only two roles. Better Auth supports custom fields on user records. Route-level protection is straightforward with Next.js middleware.

**Alternatives considered**:
- Permission-based ACL: Over-engineering for 2 roles
- Separate auth providers: Unnecessary complexity

## R7: Docker Compose Integration

**Decision**: Create a multi-stage Dockerfile using `node:18-alpine`. Stage 1: install dependencies. Stage 2: build Next.js. Stage 3: production image with standalone output. The frontend service in docker-compose.yml already references `./frontend/Dockerfile` on port 3000 with `NEXT_PUBLIC_API_URL=http://localhost:8001`.

**Rationale**: Multi-stage build minimizes image size. Next.js standalone output mode produces a minimal Node.js server. The existing docker-compose.yml already has the frontend service definition; we just need to provide the matching directory and Dockerfile.

**Alternatives considered**:
- Single-stage build: Larger image, includes dev dependencies
- Nginx static: Doesn't support API routes needed for Better Auth
