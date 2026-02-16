# AGENTS.md - LearnFlow Application

## Overview

This directory contains LearnFlow, an AI-powered Python tutoring platform. It includes both infrastructure components and backend microservices, all deployed via Kubernetes with Skills from the skills-library.

## Directory Structure

```
learnflow-app/
├── backend/
│   ├── shared/              # Shared libraries (models, dapr, config)
│   ├── services/
│   │   ├── triage/          # Question routing (Port 8001)
│   │   ├── concepts/        # Concept explanations (Port 8002)
│   │   ├── code-runner/     # Sandboxed execution (Port 8003)
│   │   ├── debug/           # Error analysis (Port 8004)
│   │   ├── exercise/        # Exercise generation (Port 8005)
│   │   └── progress/        # Mastery tracking (Port 8006)
│   └── deploy/
│       ├── helm/            # Helm charts
│       └── verify/          # Health check scripts
├── infrastructure/
│   ├── kafka/               # Message broker (Kafka)
│   ├── postgres/            # Database (PostgreSQL)
│   ├── dapr/                # Service mesh (Dapr)
│   ├── kong/                # API Gateway (Kong)
│   ├── verify/              # Health check scripts
│   └── rollback/            # Rollback scripts
└── AGENTS.md                # This file
```

---

## Backend Services

### Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    API Gateway (Kong)                        │
└─────────────────────────────────────────────────────────────┘
                              │
        ┌─────────────────────┼─────────────────────┐
        │                     │                     │
   ┌────▼────┐          ┌────▼────┐          ┌────▼────┐
   │ Triage  │          │ Concepts│          │  Code   │
   │ :8001   │─────────▶│  :8002  │          │ Runner  │
   └────┬────┘          └─────────┘          │  :8003  │
        │                                     └────┬────┘
        │    ┌─────────┐      ┌─────────┐         │
        └───▶│  Debug  │      │Exercise │◀────────┘
             │  :8004  │      │  :8005  │
             └────┬────┘      └────┬────┘
                  │                │
                  └───────┬────────┘
                          │
                   ┌──────▼──────┐
                   │  Progress   │
                   │   :8006     │
                   └─────────────┘
```

### Service Details

| Service | Port | Purpose | Key Files |
|---------|------|---------|-----------|
| Triage | 8001 | Routes questions to specialists | classifier.py, agent.py |
| Concepts | 8002 | Explains Python concepts | agent.py, adapters.py |
| Code Runner | 8003 | Sandboxed code execution | sandbox.py, resource_limiter.py |
| Debug | 8004 | Error analysis and hints | error_parser.py, struggle_detector.py |
| Exercise | 8005 | Generates/grades exercises | agent.py, grader.py |
| Progress | 8006 | Tracks mastery scores | calculator.py, events.py |

### Tech Stack

- **Framework**: FastAPI with async/await
- **AI**: OpenAI SDK (gpt-4-turbo-preview)
- **Messaging**: Kafka via Dapr pub/sub
- **State**: PostgreSQL via Dapr state store
- **Validation**: Pydantic v2

### Mastery Formula

```
Topic Mastery = 40% exercises + 30% quizzes + 20% code quality + 10% streak
```

| Level | Score | Color |
|-------|-------|-------|
| Beginner | 0-40% | Red |
| Learning | 41-70% | Yellow |
| Proficient | 71-90% | Green |
| Mastered | 91-100% | Blue |

### Backend Deployment

```bash
# Build images
cd backend
for svc in triage concepts code-runner debug exercise progress; do
  docker build -t learnflow-$svc:latest -f services/$svc/Dockerfile .
done

# Deploy with Helm
helm upgrade --install learnflow-backend deploy/helm/learnflow-backend \
  --namespace learnflow --create-namespace \
  --set openai.apiKey=$OPENAI_API_KEY

# Verify
./deploy/verify/backend-health.sh learnflow
```

---

## Infrastructure Components

### Kafka (Message Broker)
- **Namespace**: `kafka`
- **Topics**: 6 predefined (learning.*, code.*, struggle.*, progress.*)
- **Skill**: `kafka-k8s-setup`
- **Purpose**: Async communication between microservices

### PostgreSQL (Database)
- **Namespace**: `database`
- **Tables**: users, progress, code_submissions, chat_history
- **Skill**: `postgres-k8s-setup`
- **Purpose**: Persistent data storage

### Dapr (Service Mesh)
- **Namespace**: `dapr-system`
- **Components**: pubsub-kafka, statestore-postgres
- **Skill**: `dapr-k8s-setup`
- **Purpose**: Pub/sub, state management, service invocation

### Kong (API Gateway)
- **Namespace**: `kong`
- **Authentication**: JWT
- **Skill**: `kong-k8s-setup`
- **Purpose**: External traffic routing, authentication

## Deployment Order

Dependencies require this order:
1. Kafka (no dependencies)
2. PostgreSQL (no dependencies)
3. Dapr (depends on Kafka + PostgreSQL)
4. Kong (can deploy parallel with #1-2)

## Resource Limits

Total cluster: 4 CPU, 8GB RAM

| Component | CPU (req/lim) | Memory (req/lim) |
|-----------|---------------|------------------|
| Kafka | 500m/1000m | 1Gi/2Gi |
| Zookeeper | 250m/500m | 512Mi/1Gi |
| PostgreSQL | 250m/500m | 512Mi/1Gi |
| Dapr | 250m/500m | 256Mi/512Mi |
| Kong | 250m/500m | 256Mi/512Mi |

## AI Agent Context

When working with infrastructure:
- All deployments are idempotent (use `helm upgrade --install`)
- Verify with `kubectl get pods -n <namespace>` after deployment
- Credentials stored as K8s secrets (never plain text)
- Use verification scripts in `verify/` directory
- Rollback scripts available in `rollback/` directory

## Skills Reference

```bash
# Deploy Kafka
# Skill: kafka-k8s-setup

# Deploy PostgreSQL
# Skill: postgres-k8s-setup

# Configure Dapr
# Skill: dapr-k8s-setup

# Deploy Kong
# Skill: kong-k8s-setup

# Full verification
# Skill: infrastructure-verify
```
