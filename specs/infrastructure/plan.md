# Implementation Plan: K8s Infrastructure

**Branch**: `002-k8s-infrastructure` | **Date**: 2026-01-25 | **Spec**: [spec.md](./spec.md)
**Input**: Feature specification from `specs/infrastructure/spec.md`

## Summary

Deploy the complete LearnFlow infrastructure stack on Minikube using Skills. Four components — Apache Kafka, PostgreSQL, Dapr, and Kong API Gateway — are deployed via Helm charts with automated verification. Total resource budget: ~2.5GB RAM and ~1.25 CPU within Minikube's 4 CPU / 8GB allocation.

## Technical Context

**Language/Version**: Bash (POSIX-compliant), Python 3.11+ for verification, SQL for migrations
**Primary Dependencies**: Helm 3.x, kubectl, Minikube, Dapr CLI
**Storage**: PostgreSQL (persistent volume on Minikube)
**Testing**: Infrastructure verification scripts (health checks, connectivity tests)
**Target Platform**: Minikube (4 CPU, 8GB RAM, Docker driver)
**Project Type**: Infrastructure deployment (no application code)
**Performance Goals**: Full stack deployment < 10 minutes
**Constraints**: Total infra < 2.5GB RAM, < 1.25 CPU; all Helm-based; idempotent
**Scale/Scope**: 4 infrastructure components, 4 namespaces, 6 Kafka topics, 4 DB tables

## Constitution Check

| Principle | Status | Notes |
|-----------|--------|-------|
| I. Skills-First | PASS | Each component deployed via a skill |
| II. Token Efficiency | PASS | Skills invoke scripts; minimal context usage |
| III. Cloud-Native | PASS | All Helm-based K8s deployments |
| IV. Microservices | PASS | Infrastructure supports microservice communication (Kafka, Dapr) |
| V. Security | PASS | Secrets in K8s secrets, JWT auth via Kong |
| VI. SDD | PASS | Spec → Plan → Tasks workflow |
| VII. Cross-Agent | PASS | Skills work on Claude Code and Goose |
| VIII. Observability | PASS | Verification scripts for all components |

## Project Structure

### Documentation (this feature)

```text
specs/infrastructure/
├── plan.md              # This file
├── tasks.md             # Implementation tasks
├── checklists/
│   └── requirements.md  # Quality checklist
```

### Infrastructure Configuration

```text
infrastructure/
├── kafka/
│   ├── values.yaml          # Bitnami Kafka Helm values (KRaft mode)
│   └── topics.yaml          # Topic definitions
├── postgresql/
│   ├── values.yaml          # Bitnami PostgreSQL Helm values
│   └── migrations/
│       ├── 001_users.sql
│       ├── 002_progress.sql
│       ├── 003_code_submissions.sql
│       └── 004_chat_history.sql
├── dapr/
│   ├── values.yaml          # Dapr Helm values
│   └── components/
│       ├── pubsub-kafka.yaml
│       └── statestore-postgres.yaml
├── kong/
│   ├── values.yaml          # Kong Helm values (DB-less)
│   └── declarative/
│       ├── kong.yaml         # Routes and services
│       └── jwt-plugin.yaml   # JWT configuration
└── verify/
    └── infrastructure-verify.py  # Full stack verification
```

## Research Findings

### Kafka (Bitnami Helm + KRaft)
- Chart: `oci://registry-1.docker.io/bitnamicharts/kafka`
- KRaft mode: `kraft.enabled=true`, `zookeeper.enabled=false`
- Resource allocation: ~1GB RAM, ~0.5 CPU
- 3 partitions for high-throughput topics (learning.*, code.*), 1 for low-throughput (struggle.*, progress.*)

### PostgreSQL (Bitnami Helm)
- Chart: `oci://registry-1.docker.io/bitnamicharts/postgresql`
- Minikube storage provisioner for persistent volume
- Resource allocation: ~512MB RAM, ~0.25 CPU
- Connection string stored as K8s secret

### Dapr (Official Helm)
- Chart: `dapr/dapr` from `https://dapr.github.io/helm-charts/`
- Namespace: `dapr-system`
- Pub/sub component: `pubsub` (Kafka binding)
- State store component: `statestore` (PostgreSQL binding)
- Resource allocation: ~256MB RAM, ~0.25 CPU

### Kong (OSS Helm, DB-less)
- Chart: `kong/kong` from `https://charts.konghq.com`
- DB-less mode with declarative configuration
- JWT plugin for authentication
- Resource allocation: ~256MB RAM, ~0.25 CPU

### Resource Budget

| Component | RAM | CPU | Namespace |
|-----------|-----|-----|-----------|
| Kafka | 1024MB | 0.5 | kafka |
| PostgreSQL | 512MB | 0.25 | learnflow |
| Dapr | 256MB | 0.25 | dapr-system |
| Kong | 256MB | 0.25 | kong |
| **Total** | **~2GB** | **~1.25** | |

## Data Model

### Database Schema

**users**
| Column | Type | Constraints |
|--------|------|-------------|
| id | UUID | PRIMARY KEY DEFAULT gen_random_uuid() |
| email | VARCHAR(255) | UNIQUE NOT NULL |
| name | VARCHAR(255) | NOT NULL |
| role | VARCHAR(20) | DEFAULT 'student' CHECK (role IN ('student', 'teacher')) |
| password_hash | VARCHAR(255) | NOT NULL |
| created_at | TIMESTAMPTZ | DEFAULT NOW() |
| updated_at | TIMESTAMPTZ | DEFAULT NOW() |

**progress**
| Column | Type | Constraints |
|--------|------|-------------|
| id | UUID | PRIMARY KEY DEFAULT gen_random_uuid() |
| user_id | UUID | REFERENCES users(id) NOT NULL |
| topic | VARCHAR(100) | NOT NULL |
| mastery_score | DECIMAL(5,2) | DEFAULT 0.00 |
| level | VARCHAR(20) | DEFAULT 'beginner' |
| exercises_score | DECIMAL(5,2) | DEFAULT 0.00 |
| quizzes_score | DECIMAL(5,2) | DEFAULT 0.00 |
| quality_score | DECIMAL(5,2) | DEFAULT 0.00 |
| streak_score | DECIMAL(5,2) | DEFAULT 0.00 |
| updated_at | TIMESTAMPTZ | DEFAULT NOW() |

**code_submissions**
| Column | Type | Constraints |
|--------|------|-------------|
| id | UUID | PRIMARY KEY DEFAULT gen_random_uuid() |
| user_id | UUID | REFERENCES users(id) NOT NULL |
| code | TEXT | NOT NULL |
| language | VARCHAR(20) | DEFAULT 'python' |
| stdout | TEXT | |
| stderr | TEXT | |
| execution_time_ms | INTEGER | |
| timed_out | BOOLEAN | DEFAULT FALSE |
| created_at | TIMESTAMPTZ | DEFAULT NOW() |

**chat_history**
| Column | Type | Constraints |
|--------|------|-------------|
| id | UUID | PRIMARY KEY DEFAULT gen_random_uuid() |
| user_id | UUID | REFERENCES users(id) NOT NULL |
| session_id | UUID | NOT NULL |
| role | VARCHAR(20) | NOT NULL CHECK (role IN ('student', 'agent', 'system')) |
| content | TEXT | NOT NULL |
| agent_type | VARCHAR(50) | |
| created_at | TIMESTAMPTZ | DEFAULT NOW() |

### Kafka Topics

| Topic | Partitions | Retention | Purpose |
|-------|-----------|-----------|---------|
| learning.questions | 3 | 7d | Student queries → Triage |
| learning.responses | 3 | 7d | Agent responses → Frontend |
| code.submissions | 3 | 7d | Code to execute → Code Runner |
| code.results | 3 | 7d | Execution results → Frontend |
| struggle.detected | 1 | 7d | Struggle alerts → Teacher Dashboard |
| progress.updated | 1 | 7d | Mastery updates → Frontend |

## Complexity Tracking

No constitution violations — no complexity justification needed.
