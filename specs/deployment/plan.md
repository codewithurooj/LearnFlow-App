# Implementation Plan: Cloud Deployment & CI/CD

**Branch**: `006-cloud-deployment-cicd` | **Date**: 2026-02-01 | **Spec**: [spec.md](./spec.md)
**Input**: Feature specification from `specs/deployment/spec.md`

## Summary

Implement a complete CI/CD pipeline and cloud deployment system for LearnFlow using GitHub Actions for CI, Argo CD for GitOps-based continuous delivery, Kustomize for environment management (local/staging/production), Prometheus + Grafana for monitoring, and External Secrets Operator for cloud secrets management. Target cloud platforms: Azure (AKS), Google (GKE), and Oracle (OKE).

## Technical Context

**Language/Version**: YAML (Kustomize, Argo CD, GitHub Actions), Bash, Python for scripts
**Primary Dependencies**: Argo CD, Kustomize, Prometheus, Grafana, External Secrets Operator
**Storage**: Prometheus TSDB (15-day retention), Grafana dashboards (configmap)
**Testing**: Infrastructure verification scripts, deployment smoke tests
**Target Platform**: Minikube (local), AKS/GKE/OKE (cloud)
**Project Type**: Infrastructure/DevOps
**Performance Goals**: < 10 min push-to-staging, < 5 min promotion, < 5 min rollback
**Constraints**: Zero-downtime, secrets never in git, cloud-agnostic manifests
**Scale/Scope**: 8 services, 3 environments, 5 GitHub Actions workflows, 6+ Grafana dashboards

## Constitution Check

| Principle | Status | Notes |
|-----------|--------|-------|
| I. Skills-First | PASS | 5 new skills: cicd-github-actions, argocd-k8s-setup, kustomize-k8s-setup, monitoring-k8s-setup, external-secrets-setup |
| II. Token Efficiency | PASS | Skills invoke scripts for deployment |
| III. Cloud-Native | PASS | K8s-native with Kustomize, Argo CD, ESO |
| IV. Microservices | PASS | Each service independently deployed |
| V. Security | PASS | ESO for secrets, no secrets in git, CI scan |
| VI. SDD | PASS | Spec → Plan → Tasks workflow |
| VII. Cross-Agent | PASS | Standard YAML/Bash, no agent-specific code |
| VIII. Observability | PASS | Prometheus + Grafana + alerting |

## Project Structure

### Documentation (this feature)

```text
specs/deployment/
├── plan.md              # This file
├── tasks.md             # Implementation tasks
├── checklists/
│   └── requirements.md  # Quality checklist
```

### Source Code

```text
learnflow-app/
├── k8s/
│   ├── base/
│   │   ├── kustomization.yaml
│   │   ├── namespace.yaml
│   │   ├── triage/
│   │   │   ├── deployment.yaml
│   │   │   └── service.yaml
│   │   ├── concepts/
│   │   │   ├── deployment.yaml
│   │   │   └── service.yaml
│   │   ├── code-runner/
│   │   │   ├── deployment.yaml
│   │   │   └── service.yaml
│   │   ├── debug/
│   │   │   ├── deployment.yaml
│   │   │   └── service.yaml
│   │   ├── exercise/
│   │   │   ├── deployment.yaml
│   │   │   └── service.yaml
│   │   ├── progress/
│   │   │   ├── deployment.yaml
│   │   │   └── service.yaml
│   │   ├── code-review/
│   │   │   ├── deployment.yaml
│   │   │   └── service.yaml
│   │   └── frontend/
│   │       ├── deployment.yaml
│   │       └── service.yaml
│   ├── overlays/
│   │   ├── local/
│   │   │   ├── kustomization.yaml
│   │   │   └── patches/
│   │   ├── staging/
│   │   │   ├── kustomization.yaml
│   │   │   ├── ingress.yaml
│   │   │   └── patches/
│   │   └── production/
│   │       ├── kustomization.yaml
│   │       ├── ingress.yaml
│   │       ├── hpa.yaml
│   │       └── patches/
│   └── argocd/
│       ├── project.yaml
│       ├── staging-app.yaml
│       └── production-app.yaml
├── .github/
│   └── workflows/
│       ├── ci.yaml              # Lint, test, build on push
│       ├── deploy-staging.yaml  # Auto-deploy to staging on main
│       ├── promote-production.yaml  # Manual promote
│       ├── rollback.yaml        # Manual rollback
│       └── secret-scan.yaml     # Check for leaked secrets
├── monitoring/
│   ├── prometheus/
│   │   ├── values.yaml
│   │   └── rules/
│   │       └── slo-alerts.yaml
│   └── grafana/
│       ├── values.yaml
│       └── dashboards/
│           ├── overview.json
│           ├── services.json
│           ├── agents.json
│           ├── kafka.json
│           ├── postgres.json
│           └── slo.json
└── secrets/
    ├── local/
    │   └── secrets.yaml         # K8s secrets for local dev
    └── cloud/
        ├── cluster-secret-store.yaml
        ├── external-secrets-openai.yaml
        ├── external-secrets-postgres.yaml
        └── external-secrets-auth.yaml
```

## Research Findings

### Kustomize Patterns
- Base contains common manifests; overlays patch per environment
- `kustomization.yaml` lists resources and patches
- Image tags updated via `kustomize edit set image`
- Strategic merge patches for environment-specific configs

### Argo CD Configuration
- Application CRD defines source repo, path, and target cluster
- Auto-sync: `syncPolicy.automated.prune: true, selfHeal: true`
- Sync waves: `argocd.argoproj.io/sync-wave` annotation for ordering
- Health checks: built-in for Deployments, custom for CRDs

### GitHub Actions CI
- Matrix builds for multiple services
- Docker layer caching with `actions/cache`
- Image tagging: `ghcr.io/<org>/<service>:<git-sha>`
- Secret scanning: `trufflehog` or `gitleaks` action

### External Secrets Operator (Multi-Cloud)
- ClusterSecretStore per cloud provider
- Azure: Key Vault with managed identity
- Google: Secret Manager with workload identity
- Oracle: Vault with instance principal
- ExternalSecret CRD maps provider secrets to K8s secrets

### Prometheus + Grafana Stack
- `kube-prometheus-stack` Helm chart (community)
- ServiceMonitor CRD for per-service scraping
- AlertManager for routing alerts
- Grafana dashboards as ConfigMaps
- Key metrics: request_duration_seconds, request_total, error_total

### Zero-Downtime Rolling Updates
- `strategy.rollingUpdate.maxUnavailable: 0, maxSurge: 1`
- Readiness probes must pass before traffic is sent
- `terminationGracePeriodSeconds: 30` for graceful shutdown
- PodDisruptionBudget for high-availability services

## Data Model

### Pipeline Run
| Field | Type | Description |
|-------|------|-------------|
| id | string | GitHub Actions run ID |
| trigger | enum | push, manual_dispatch, schedule |
| branch | string | Source branch |
| commit_sha | string | Git commit SHA |
| stages | Stage[] | lint, test, build, push, deploy |
| status | enum | pending, running, success, failure |
| duration_s | integer | Total pipeline duration |
| started_at | timestamp | Pipeline start time |

### Deployment
| Field | Type | Description |
|-------|------|-------------|
| id | string | Argo CD sync ID |
| service | string | Service name |
| image_tag | string | Docker image tag (git SHA) |
| environment | enum | local, staging, production |
| status | enum | syncing, healthy, degraded, missing |
| revision | integer | Argo CD revision number |
| deployed_at | timestamp | Deployment time |

### Environment
| Field | Type | Description |
|-------|------|-------------|
| name | enum | local, staging, production |
| cluster | string | Kubernetes cluster name |
| overlay_path | string | Kustomize overlay directory |
| argocd_app | string | Argo CD application name |
| auto_sync | boolean | Whether Argo CD auto-syncs |

## Skills Required

| Skill | Purpose |
|-------|---------|
| cicd-github-actions | Generate GitHub Actions workflow files |
| argocd-k8s-setup | Install and configure Argo CD |
| kustomize-k8s-setup | Create Kustomize base + overlays |
| monitoring-k8s-setup | Deploy Prometheus + Grafana stack |
| external-secrets-setup | Configure ESO for cloud secrets |

## Complexity Tracking

No constitution violations — no complexity justification needed.
