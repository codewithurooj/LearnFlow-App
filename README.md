# Hackathon III: Reusable Intelligence and Cloud-Native Mastery

An AI-powered platform built entirely using **Skills with MCP Code Execution** -- teaching AI coding agents (Claude Code & Goose) how to build sophisticated cloud-native applications autonomously.

## Repositories

| Repository | Description |
|------------|-------------|
| [`skills-library/`](./skills-library/) | 11 reusable Skills with MCP Code Execution for cloud-native deployment |
| [`learnflow-app/`](./learnflow-app/) | Complete AI-powered Python tutoring platform built via Skills |

## Core Concept

```
Traditional: You write code -> Code runs -> Application works
Agentic:     You write Skills -> AI learns -> AI writes code -> Application works
```

Skills are the product. Each skill contains:
- **SKILL.md** (~100 tokens) -- instructions the agent loads
- **scripts/** (0 tokens) -- code that executes outside context
- **REFERENCE.md** (0 tokens) -- deep docs loaded on-demand

This achieves **80-98% token reduction** vs direct MCP integration.

## Technology Stack

| Layer | Technology |
|-------|------------|
| AI Agents | Claude Code, Goose |
| Frontend | Next.js 14 + Monaco Editor + Better Auth |
| Backend | FastAPI + OpenAI SDK (6 AI agents + code runner) |
| Service Mesh | Dapr (state, pub/sub, service invocation) |
| Messaging | Apache Kafka on Kubernetes |
| Database | PostgreSQL (Neon-compatible) |
| API Gateway | Kong with JWT authentication |
| Orchestration | Kubernetes (Minikube for dev) |
| CI/CD | GitHub Actions + Argo CD (GitOps) |
| Documentation | Docusaurus |

## Skills Library (11 Skills)

### Core Infrastructure (P0)
- **agents-md-gen** -- Generate AGENTS.md files
- **kafka-k8s-setup** -- Deploy Kafka on Kubernetes
- **postgres-k8s-setup** -- Deploy PostgreSQL on Kubernetes
- **dapr-k8s-setup** -- Deploy Dapr service mesh
- **kong-k8s-setup** -- Deploy Kong API Gateway
- **infrastructure-verify** -- Verify all infrastructure health

### Application (P1)
- **fastapi-dapr-agent** -- Scaffold FastAPI + Dapr microservices
- **mcp-code-execution** -- MCP with code execution pattern
- **nextjs-k8s-deploy** -- Deploy Next.js apps to K8s
- **docusaurus-deploy** -- Deploy documentation sites

## LearnFlow Application

An AI-powered Python tutoring platform with:

- **6 AI Agents**: Triage, Concepts, Code Review, Debug, Exercise, Progress
- **Code Editor**: Monaco editor with sandboxed Python execution
- **Progress Tracking**: Mastery calculation with struggle detection
- **Teacher Dashboard**: Class monitoring with struggle alerts
- **8 Python Modules**: Basics through Libraries

### Architecture

```
┌──────────────────────────────────────────────────────┐
│                 KUBERNETES CLUSTER                     │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐           │
│  │ Next.js  │  │ Triage   │  │ Concepts │  ...more  │
│  │ Frontend │  │ +Dapr    │  │ +Dapr    │           │
│  └────┬─────┘  └────┬─────┘  └────┬─────┘           │
│       └──────────────┴─────────────┘                  │
│                      │                                │
│       ┌──────────────┴──────────────┐                │
│       │         KAFKA               │                │
│       │  learning.* | code.* | ...  │                │
│       └──────────────┬──────────────┘                │
│              ┌───────┴───────┐                       │
│         ┌────┴────┐    ┌────┴────┐                   │
│         │PostgreSQL│    │  MCP   │                   │
│         │ (Neon)  │    │ Server │                   │
│         └─────────┘    └────────┘                   │
└──────────────────────────────────────────────────────┘
```

## Quick Start

### Prerequisites
- Docker, Minikube, Helm, Claude Code, Goose

### Setup
```bash
# Start Kubernetes cluster
minikube start --cpus=4 --memory=8192 --driver=docker

# Deploy infrastructure using skills
# Skills auto-deploy Kafka, PostgreSQL, Dapr, Kong

# Run frontend locally
cd learnflow-app/frontend && npm install && npm run dev

# Run backend locally
cd learnflow-app/backend && docker-compose up
```

## Spec-Driven Development

All development follows SDD with complete artifacts:

```
specs/
├── 001-skills-library/        # spec.md, plan.md, tasks.md
├── 002-k8s-infrastructure/
├── 003-learnflow-backend/
├── 004-learnflow-frontend/
├── 005-ai-agents/
└── 006-cloud-deployment-cicd/
```

- **25 Prompt History Records** in `history/prompts/`
- **Architecture Decision Records** in `history/adr/`
- **Project Constitution** in `.specify/memory/constitution.md`

## Evaluation Criteria

| Criterion | Weight |
|-----------|--------|
| Skills Autonomy | 15% |
| Token Efficiency | 10% |
| Cross-Agent Compatibility | 5% |
| Architecture | 20% |
| MCP Integration | 10% |
| Documentation | 10% |
| Spec-Kit Plus Usage | 15% |
| LearnFlow Completion | 15% |

## Standards

Built following [Agentic AI Foundation (AAIF)](https://aaif.io/) standards.
