---
id: 002
title: Create K8s Infrastructure Plan
stage: plan
date: 2026-01-25
surface: project
model: claude-opus-4-5-20251101
feature: 002-k8s-infrastructure
branch: 002-platinum-tier
user: system
command: /sp.plan
labels: [infrastructure, kubernetes, kafka, postgresql, dapr, kong]
links:
  spec: specs/002-k8s-infrastructure/spec.md
  ticket:
  adr:
  pr:
files:
  - path: specs/002-k8s-infrastructure/plan.md
    action: created
  - path: specs/002-k8s-infrastructure/research.md
    action: created
  - path: specs/002-k8s-infrastructure/data-model.md
    action: created
  - path: specs/002-k8s-infrastructure/quickstart.md
    action: created
  - path: specs/002-k8s-infrastructure/contracts/kafka-topics.yaml
    action: created
  - path: specs/002-k8s-infrastructure/contracts/database-schema.sql
    action: created
  - path: specs/002-k8s-infrastructure/contracts/dapr-components.yaml
    action: created
  - path: specs/002-k8s-infrastructure/contracts/kong-routes.yaml
    action: created
tests:
  - none (planning phase)
---

## Prompt

```text
/sp.plan spec 002 k8s-infrastructure that is in current directory
```

## Response snapshot

Created implementation plan for Kubernetes infrastructure deployment (002-k8s-infrastructure) following the SDD workflow:

**Phase 0 - Research** (`research.md`):
- Kafka: Bitnami Helm with KRaft mode (no Zookeeper)
- PostgreSQL: Bitnami Helm with Minikube storage provisioner
- Dapr: Official Helm chart with pub/sub and state store components
- Kong: OSS Helm in DB-less mode with declarative JWT config
- Resource allocation: ~2.5GB RAM and ~1.25 CPU for infrastructure

**Phase 1 - Design & Contracts**:
- `data-model.md`: 4 tables (users, progress, code_submissions, chat_history) + 6 Kafka topic schemas
- `contracts/kafka-topics.yaml`: 6 topics with partitions and retention
- `contracts/database-schema.sql`: Full PostgreSQL DDL with indexes
- `contracts/dapr-components.yaml`: Pub/sub (Kafka) and state store (PostgreSQL)
- `contracts/kong-routes.yaml`: API routes with JWT authentication

**Constitution Check**: PASS on all 8 principles

**New Skills Required**:
1. dapr-k8s-setup
2. kong-k8s-setup
3. infrastructure-verify

## Outcome

- ✅ Impact: Complete infrastructure plan ready for task generation
- 🧪 Tests: N/A (planning phase)
- 📁 Files: 8 files created (plan.md, research.md, data-model.md, quickstart.md, 4 contracts)
- 🔁 Next prompts: `/sp.tasks` to generate implementation tasks
- 🧠 Reflection: Plan follows constitution principles, resource allocation fits 4CPU/8GB constraint

## Evaluation notes (flywheel)

- Failure modes observed: Agent context update script missing template (non-blocking)
- Graders run and results (PASS/FAIL): Constitution Check PASS
- Prompt variant (if applicable): N/A
- Next experiment (smallest change to try): Run /sp.tasks to validate plan completeness
