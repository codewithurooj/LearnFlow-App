# LearnFlow - AI-Powered Python Tutoring Platform

LearnFlow is a cloud-native AI tutoring platform that helps students learn Python through conversational AI agents, an embedded code editor, quizzes, and progress tracking. Built entirely using Skills with MCP Code Execution via Claude Code and Goose.

## Architecture

```
┌──────────────────────────────────────────────────────────────┐
│                     KUBERNETES CLUSTER                        │
│                                                              │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐    │
│  │ Next.js  │  │ Triage   │  │ Concepts │  │  Debug   │    │
│  │ Frontend │  │ Service  │  │ Service  │  │ Service  │    │
│  │ +Monaco  │  │ +Dapr    │  │ +Dapr    │  │ +Dapr    │    │
│  └────┬─────┘  └────┬─────┘  └────┬─────┘  └────┬─────┘    │
│       │              │             │             │           │
│  Kong API Gateway ◄──┴─────────────┴─────────────┘           │
│       │                                                      │
│  ┌────┴──────────────────────────────────────────┐           │
│  │                  KAFKA                         │           │
│  │  learning.* | code.* | struggle.* | progress.*│           │
│  └────┬──────────────────────────────────────────┘           │
│       │                                                      │
│  ┌────┴─────┐  ┌───────────┐  ┌────────────┐               │
│  │PostgreSQL│  │ MCP Server│  │ Prometheus │               │
│  │ (Neon)   │  │ (Context) │  │ Monitoring │               │
│  └──────────┘  └───────────┘  └────────────┘               │
└──────────────────────────────────────────────────────────────┘
```

## Services

### Frontend
- **Next.js 14** with App Router and TypeScript strict mode
- **Monaco Editor** for in-browser Python coding
- **Better Auth** for authentication (login/signup)
- **Zustand** for state management
- **Tailwind CSS** for styling
- **Playwright** for E2E testing

### Backend Microservices (FastAPI + Dapr)

| Service | Port | Purpose |
|---------|------|---------|
| **Triage** | 8001 | Routes student queries to specialist agents |
| **Concepts** | 8002 | Explains Python concepts with adaptive difficulty |
| **Code Review** | 8003 | Analyzes code for correctness, PEP 8, efficiency |
| **Debug** | 8004 | Parses errors, identifies root causes, detects struggles |
| **Exercise** | 8005 | Generates and auto-grades coding challenges |
| **Progress** | 8006 | Tracks mastery scores, streaks, and summaries |
| **Code Runner** | 8007 | Sandboxed Python execution (5s timeout, 50MB memory) |

### Infrastructure
- **Apache Kafka** (Strimzi) -- Event streaming for async communication
- **PostgreSQL** (Bitnami / Neon) -- Persistent data storage
- **Dapr** -- Service mesh for pub/sub, state management, service invocation
- **Kong** -- API Gateway with JWT authentication
- **Prometheus** -- Metrics and monitoring

## Kafka Topics

| Topic | Publisher | Subscriber |
|-------|----------|------------|
| `learning.questions` | Frontend | Triage Service |
| `learning.responses` | Agent Services | Frontend |
| `code.submissions` | Frontend | Code Runner |
| `code.results` | Code Runner | Frontend |
| `struggle.detected` | Debug Service | Teacher Dashboard |
| `progress.updated` | Progress Service | Frontend |

## Project Structure

```
learnflow-app/
├── frontend/               # Next.js 14 application
│   ├── src/
│   │   ├── app/            # Pages (auth, dashboard, code, learn, quizzes, progress, teacher)
│   │   ├── components/     # 30+ React components
│   │   ├── lib/            # API clients, stores, utilities
│   │   └── types/          # TypeScript type definitions
│   └── e2e/                # Playwright tests
├── backend/
│   ├── services/           # 7 microservices
│   │   ├── triage/
│   │   ├── concepts/
│   │   ├── code-review/
│   │   ├── debug/
│   │   ├── exercise/
│   │   ├── progress/
│   │   └── code-runner/
│   └── shared/             # Shared config, models, agents, Dapr clients
├── infrastructure/         # Kubernetes manifests
│   ├── kafka/              # Strimzi Kafka deployment
│   ├── postgres/           # PostgreSQL Helm values
│   ├── dapr/               # Dapr components
│   ├── kong/               # Kong API Gateway config
│   └── monitoring/         # Prometheus setup
├── k8s/                    # Kustomize overlays (staging/production)
├── argocd/                 # Argo CD GitOps applications
├── docs-site/              # Docusaurus documentation
├── docker-compose.yml      # Local development
└── .github/workflows/      # CI/CD pipelines
```

## Running Locally

### Prerequisites
- Node.js 18+, Python 3.11+, Docker

### Frontend
```bash
cd frontend
npm install
npm run dev
# Open http://localhost:3000
```

### Backend (Docker Compose)
```bash
# Start all services with Kafka, PostgreSQL, and Dapr
docker-compose up

# Or run a single service
cd backend/services/triage
pip install -r requirements.txt
uvicorn main:app --port 8001
```

### Environment Variables
Copy `.env.example` to `.env` and configure:
```env
OPENAI_API_KEY=your-key-here
DATABASE_URL=postgresql://user:pass@localhost:5432/learnflow
ENVIRONMENT=development
```

## Deploying to Kubernetes

```bash
# Start Minikube
minikube start --cpus=4 --memory=8192 --driver=docker

# Deploy infrastructure using skills
# Each skill auto-deploys its component

# Or use Helm directly
helm install kafka bitnami/kafka -n kafka -f infrastructure/kafka/values.yaml
helm install postgres bitnami/postgresql -n postgres -f infrastructure/postgres/values.yaml
```

## CI/CD

- **GitHub Actions**: Lint (ruff, eslint, yamllint) -> Test (pytest, vitest) -> Build (Docker) -> Update manifests
- **Argo CD**: GitOps continuous delivery to staging and production
- **Promotion**: `promote-production.yaml` workflow for production releases
- **Rollback**: `rollback.yaml` workflow for emergency rollbacks

## Business Rules

### Mastery Calculation
```
Topic Mastery = Exercises (40%) + Quizzes (30%) + Code Quality (20%) + Streak (10%)
```

### Mastery Levels
- 0-40%: Beginner (Red)
- 41-70%: Learning (Yellow)
- 71-90%: Proficient (Green)
- 91-100%: Mastered (Blue)

### Struggle Detection
Triggers when: same error 3+ times, stuck >10 min, quiz <50%, 5+ failed executions, or student says "I'm stuck".
