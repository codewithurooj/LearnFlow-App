# Quickstart: LearnFlow Frontend

## Prerequisites

- Node.js 18+
- Docker Desktop (for docker-compose integration)
- Backend services running (via `docker compose up postgres zookeeper kafka triage concepts code-runner debug exercise progress code-review`)

## Setup

```bash
cd learnflow-app/frontend

# Install dependencies
npm install

# Create environment file
cp .env.example .env.local
# Edit .env.local with your values

# Run development server
npm run dev
# Open http://localhost:3000
```

## Environment Variables

```env
# Required
NEXT_PUBLIC_API_URL=http://localhost:8001
BETTER_AUTH_SECRET=dev-secret-change-in-production-min32chars
BETTER_AUTH_URL=http://localhost:3000

# Database (for Better Auth session storage)
DATABASE_URL=postgresql://learnflow:learnflow_dev@localhost:5432/learnflow
```

## Docker

```bash
# Build and run with all services
cd learnflow-app
docker compose up -d

# Or build frontend only
cd learnflow-app/frontend
docker build -t learnflow-frontend .
docker run -p 3000:3000 -e NEXT_PUBLIC_API_URL=http://localhost:8001 learnflow-frontend
```

## Key Pages

| Route | Page | Auth Required |
|-------|------|---------------|
| `/` | Landing / redirect to dashboard | No |
| `/auth/login` | Login | No |
| `/auth/signup` | Signup | No |
| `/dashboard` | Student dashboard | Yes (student) |
| `/learn` | AI chat with tutors | Yes (student) |
| `/code` | Code editor + runner | Yes (student) |
| `/exercises` | Coding exercises | Yes (student) |
| `/progress` | Mastery tracking | Yes (student) |
| `/teacher` | Teacher dashboard | Yes (teacher) |

## Tech Stack Quick Reference

- **Framework**: Next.js 14 (App Router)
- **Language**: TypeScript (strict mode)
- **Styling**: Tailwind CSS
- **State**: Zustand
- **Auth**: Better Auth
- **Editor**: Monaco Editor (@monaco-editor/react)
- **Markdown**: react-markdown + rehype-highlight
