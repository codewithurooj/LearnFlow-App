# Tasks: Cloud Deployment & CI/CD

**Input**: Design documents from `specs/deployment/`
**Prerequisites**: plan.md (required), spec.md (required for user stories)

**Tests**: Not explicitly requested in spec. Verification tasks included as deployment smoke tests.

**Organization**: Tasks grouped by user story for independent implementation.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1 = Staging Deploy)
- All paths relative to `learnflow-app/`

---

## Phase 1: Setup (Base K8s Manifests & Directory Structure)

**Purpose**: Create Kustomize base manifests for all services

- [ ] T001 Create `k8s/base/kustomization.yaml` — list all resources
- [ ] T002 [P] Create `k8s/base/namespace.yaml` — learnflow namespace definition
- [ ] T003 [P] Create `k8s/base/triage/deployment.yaml` — Deployment with Dapr annotations, port 8001, resource limits
- [ ] T004 [P] Create `k8s/base/triage/service.yaml` — ClusterIP service for triage
- [ ] T005 [P] Create `k8s/base/concepts/deployment.yaml` — port 8002, resource limits
- [ ] T006 [P] Create `k8s/base/concepts/service.yaml` — ClusterIP service
- [ ] T007 [P] Create `k8s/base/code-runner/deployment.yaml` — port 8003, resource limits
- [ ] T008 [P] Create `k8s/base/code-runner/service.yaml` — ClusterIP service
- [ ] T009 [P] Create `k8s/base/debug/deployment.yaml` — port 8004
- [ ] T010 [P] Create `k8s/base/debug/service.yaml`
- [ ] T011 [P] Create `k8s/base/exercise/deployment.yaml` — port 8005
- [ ] T012 [P] Create `k8s/base/exercise/service.yaml`
- [ ] T013 [P] Create `k8s/base/progress/deployment.yaml` — port 8006

---

## Phase 2: Foundational (Overlays, Argo CD Project, Verification)

**Purpose**: Create environment overlays and Argo CD configuration

**CRITICAL**: Must complete before user story deployment workflows

- [ ] T014 [P] Create `k8s/base/progress/service.yaml`
- [ ] T015 [P] Create `k8s/base/code-review/deployment.yaml` — port 8007
- [ ] T016 [P] Create `k8s/base/code-review/service.yaml`
- [ ] T017 [P] Create `k8s/base/frontend/deployment.yaml` — port 3000
- [ ] T018 [P] Create `k8s/base/frontend/service.yaml`
- [ ] T019 Create `k8s/overlays/local/kustomization.yaml` — local overlay with Minikube patches (lower resource limits, NodePort services)
- [ ] T020 [P] Create `k8s/overlays/staging/kustomization.yaml` — staging overlay with medium resource limits
- [ ] T021 [P] Create `k8s/overlays/staging/ingress.yaml` — staging ingress configuration
- [ ] T022 [P] Create `k8s/overlays/production/kustomization.yaml` — production overlay with full resource limits
- [ ] T023 [P] Create `k8s/overlays/production/ingress.yaml` — production ingress
- [ ] T024 [P] Create `k8s/overlays/production/hpa.yaml` — HorizontalPodAutoscaler for production services

**Checkpoint**: Base manifests and overlays ready — CI/CD workflows can reference them

---

## Phase 3: User Story 1 — Staging Deploy (Priority: P1) MVP

**Goal**: Push to main → automatic staging deployment

**Independent Test**: Push commit → staging environment updated within 10 minutes

- [ ] T025 [US1] Create `.github/workflows/ci.yaml` — on push: lint, test, build Docker images for all services, tag with git SHA
- [ ] T026 [US1] Create `.github/workflows/deploy-staging.yaml` — on main push after CI: push images to registry, update staging kustomization with new image tags, commit manifest changes
- [ ] T027 [US1] Create `k8s/argocd/project.yaml` — Argo CD AppProject for LearnFlow with source repo and destination cluster
- [ ] T028 [US1] Create `k8s/argocd/staging-app.yaml` — Argo CD Application for staging: auto-sync, prune, self-heal, source: k8s/overlays/staging

**Checkpoint**: US1 complete — push to main auto-deploys to staging

---

## Phase 4: User Story 2 — Production Promotion (Priority: P2)

**Goal**: One-click promote staging to production

**Independent Test**: Trigger promote workflow → production matches staging versions

- [ ] T029 [US2] Create `.github/workflows/promote-production.yaml` — manual dispatch: read staging image tags, update production kustomization, commit
- [ ] T030 [US2] Create `k8s/argocd/production-app.yaml` — Argo CD Application for production: manual sync (no auto), prune, self-heal
- [ ] T031 [US2] Create `scripts/promote.sh` — helper script to extract staging image tags and apply to production overlay

**Checkpoint**: US2 complete — one-click staging → production promotion

---

## Phase 5: User Story 3 — Rollback (Priority: P2)

**Goal**: Rollback to previous version within 5 minutes

**Independent Test**: Trigger rollback → previous version restored

- [ ] T032 [US3] Create `.github/workflows/rollback.yaml` — manual dispatch with revision input: trigger Argo CD rollback to specified revision
- [ ] T033 [US3] Create `scripts/rollback.sh` — helper script: `argocd app rollback <app> <revision>`, verify health after rollback

**Checkpoint**: US3 complete — rollback within 5 minutes

---

## Phase 6: User Story 4 — Health Dashboard (Priority: P3)

**Goal**: Grafana dashboard showing all service health and SLO compliance

**Independent Test**: View dashboard → metrics for all 8 services displayed

- [ ] T034 [US4] Create `monitoring/prometheus/values.yaml` — kube-prometheus-stack Helm values with ServiceMonitor for LearnFlow services
- [ ] T035 [US4] Create `monitoring/prometheus/rules/slo-alerts.yaml` — alerting rules: latency > 3s, error rate > 5%, agent timeout > 5s
- [ ] T036 [US4] Create `monitoring/grafana/values.yaml` — Grafana Helm values with dashboard provisioning
- [ ] T037 [P] [US4] Create `monitoring/grafana/dashboards/overview.json` — service overview: request rate, error rate, latency p50/p95/p99
- [ ] T038 [P] [US4] Create `monitoring/grafana/dashboards/services.json` — per-service detail dashboard
- [ ] T039 [P] [US4] Create `monitoring/grafana/dashboards/agents.json` — AI agent response times and routing accuracy

**Checkpoint**: US4 complete — monitoring dashboards and alerts configured

---

## Phase 7: Secrets Management

**Purpose**: Configure External Secrets Operator for cloud environments

- [ ] T040 Create `secrets/local/secrets.yaml` — K8s secrets for local dev (OpenAI key, DB credentials, auth secret)
- [ ] T041 [P] Create `secrets/cloud/cluster-secret-store.yaml` — ClusterSecretStore with provider configs for Azure/Google/Oracle
- [ ] T042 [P] Create `secrets/cloud/external-secrets-openai.yaml` — ExternalSecret mapping cloud vault → K8s secret for OpenAI API key
- [ ] T043 [P] Create `secrets/cloud/external-secrets-postgres.yaml` — ExternalSecret for PostgreSQL credentials
- [ ] T044 [P] Create `secrets/cloud/external-secrets-auth.yaml` — ExternalSecret for Better Auth secret
- [ ] T045 Create `.github/workflows/secret-scan.yaml` — CI check: run gitleaks/trufflehog to detect leaked secrets
- [ ] T046 Test secret scan — verify it catches a test secret and blocks the commit

**Checkpoint**: Secrets management configured for local and cloud

---

## Phase 8: Polish & Validation

**Purpose**: Cross-cutting improvements and deployment validation

- [ ] T047 [P] Add sync wave annotations to Argo CD apps — ensure namespace → infra → services deploy order
- [ ] T048 [P] Add graceful shutdown to all deployments — `terminationGracePeriodSeconds: 30`, preStop hooks
- [ ] T049 [P] Add readiness and liveness probes to all base deployments
- [ ] T050 [P] Add PodDisruptionBudget for production services
- [ ] T051 Validate local overlay — deploy to Minikube using `kubectl apply -k k8s/overlays/local`
- [ ] T052 Validate complete pipeline — push → CI → staging deploy → verify → promote → production

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies — start immediately
- **Foundational (Phase 2)**: Depends on Phase 1
- **US1 Staging (Phase 3)**: Depends on Phase 2
- **US2 Production (Phase 4)**: Depends on Phase 3
- **US3 Rollback (Phase 5)**: Depends on Phase 3
- **US4 Monitoring (Phase 6)**: Depends on Phase 2, can run in parallel with Phases 3-5
- **Secrets (Phase 7)**: Depends on Phase 2, can run in parallel with Phases 3-6
- **Polish (Phase 8)**: Depends on all phases

### Parallel Opportunities

- All base manifests (T002-T018) can run in parallel
- All overlays (T019-T024) can run in parallel after base
- US4 monitoring can run in parallel with US1-US3
- Secrets management can run in parallel with US1-US4

### MVP Scope

Phases 1-3 (Setup + Foundational + US1 Staging Deploy) = 28 tasks

---

## Notes

- [P] tasks = different files, no dependencies
- All Kustomize overlays inherit from base — changes to base propagate
- Argo CD apps point to overlay directories in the same repo
- GitHub Actions workflows use reusable actions where possible
- All deployments use rolling update strategy for zero-downtime
