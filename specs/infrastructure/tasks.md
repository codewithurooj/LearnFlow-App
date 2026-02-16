# Tasks: K8s Infrastructure

**Input**: Design documents from `specs/infrastructure/`
**Prerequisites**: plan.md (required), spec.md (required for user stories)

**Tests**: Not explicitly requested in spec. Verification tasks included as infrastructure health checks.

**Organization**: Tasks grouped by infrastructure component (user story) for independent deployment.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1 = Kafka, US2 = PostgreSQL)
- All paths relative to `infrastructure/`

---

## Phase 1: Setup (Directory Structure & Contract Files)

**Purpose**: Create directory structure and configuration files

- [ ] T001 Create infrastructure directory structure: `kafka/`, `postgresql/`, `dapr/`, `kong/`, `verify/`
- [ ] T002 [P] Create `kafka/values.yaml` — Bitnami Kafka Helm values with KRaft mode, resource limits (1GB RAM, 0.5 CPU)
- [ ] T003 [P] Create `kafka/topics.yaml` — topic definitions with partition counts (3 for high-throughput, 1 for low)
- [ ] T004 [P] Create `postgresql/values.yaml` — Bitnami PostgreSQL Helm values with persistent volume, resource limits (512MB, 0.25 CPU)
- [ ] T005 [P] Create `dapr/values.yaml` — Dapr Helm values for `dapr-system` namespace
- [ ] T006 [P] Create `kong/values.yaml` — Kong OSS Helm values for DB-less mode
- [ ] T007 [P] Create `kong/declarative/kong.yaml` — declarative routes for all 7 backend services

---

## Phase 2: Foundational (Skills & Contract Files)

**Purpose**: Create/verify deployment skills and database contracts

**CRITICAL**: Skills must exist before component deployment

- [ ] T008 Verify `kafka-k8s-setup` skill exists in skills-library (or create it)
- [ ] T009 Verify `postgres-k8s-setup` skill exists in skills-library (or create it)
- [ ] T010 [P] Create `dapr/components/pubsub-kafka.yaml` — Dapr pub/sub component bound to Kafka broker
- [ ] T011 [P] Create `dapr/components/statestore-postgres.yaml` — Dapr state store component bound to PostgreSQL
- [ ] T012 [P] Create `postgresql/migrations/001_users.sql` — CREATE TABLE IF NOT EXISTS users (id UUID, email, name, role, password_hash, created_at, updated_at)
- [ ] T013 [P] Create `postgresql/migrations/002_progress.sql` — CREATE TABLE IF NOT EXISTS progress (id UUID, user_id, topic, mastery_score, level, component scores, updated_at)
- [ ] T014 [P] Create `postgresql/migrations/003_code_submissions.sql` — CREATE TABLE IF NOT EXISTS code_submissions (id UUID, user_id, code, stdout, stderr, execution_time, timed_out, created_at)
- [ ] T015 [P] Create `postgresql/migrations/004_chat_history.sql` — CREATE TABLE IF NOT EXISTS chat_history (id UUID, user_id, session_id, role, content, agent_type, created_at)

**Checkpoint**: All configuration and skills ready — deployment can begin

---

## Phase 3: User Story 1 — Kafka Deployment (Priority: P0)

**Goal**: Deploy Kafka with all 6 LearnFlow topics

**Independent Test**: `kubectl get pods -n kafka` shows Ready; topics listable

- [ ] T016 [US1] Create Kafka deployment script — creates `kafka` namespace, runs `helm upgrade --install --atomic bitnami/kafka` with values.yaml
- [ ] T017 [US1] Create Kafka topic creation script — uses kafka-topics.sh to create all 6 topics from topics.yaml
- [ ] T018 [US1] Create Kafka verification script — checks broker pods Ready, all 6 topics exist, broker accessible
- [ ] T019 [US1] Deploy Kafka on Minikube — run deployment and topic creation scripts
- [ ] T020 [US1] Verify Kafka deployment — run verification, confirm all checks pass
- [ ] T021 [US1] Test idempotency — run deployment again, verify no errors or data loss
- [ ] T022 [US1] Document Kafka resource usage — record actual RAM/CPU vs. budget

---

## Phase 4: User Story 2 — PostgreSQL Deployment (Priority: P0)

**Goal**: Deploy PostgreSQL with schema migrations and connection secret

**Independent Test**: Tables exist, secret accessible, connection works

- [ ] T023 [US2] Create PostgreSQL deployment script — creates namespace, runs `helm upgrade --install --atomic bitnami/postgresql`
- [ ] T024 [US2] Create connection secret script — extracts password from Helm release, creates `postgres-credentials` K8s secret
- [ ] T025 [US2] Create migration runner script — connects to PostgreSQL, executes all migration SQL files in order
- [ ] T026 [US2] Create PostgreSQL verification script — checks pod Ready, all 4 tables exist, indexes created, secret accessible
- [ ] T027 [US2] Deploy PostgreSQL on Minikube — run deployment script
- [ ] T028 [US2] Run migrations on Minikube — execute migration runner
- [ ] T029 [US2] Create connection secret — run secret creation script
- [ ] T030 [US2] Verify PostgreSQL deployment — run verification, confirm all checks pass
- [ ] T031 [US2] Test idempotency — run deployment + migrations again
- [ ] T032 [US2] Test migration safety — verify IF NOT EXISTS guards work with existing tables
- [ ] T033 [P] [US2] Create seed data script (optional) — insert test user for development
- [ ] T034 [US2] Document PostgreSQL resource usage
- [ ] T035 [US2] Verify connection from a test pod — deploy alpine pod, connect to PostgreSQL using secret

---

## Phase 5: User Story 3 — Dapr Configuration (Priority: P0)

**Goal**: Install Dapr and configure pub/sub + state store components

**Independent Test**: Test service can publish/subscribe via Dapr and store state

- [ ] T036 [US3] Create Dapr installation script — `helm upgrade --install dapr dapr/dapr --namespace dapr-system --create-namespace`
- [ ] T037 [US3] Create Dapr component deployment script — apply pubsub-kafka.yaml and statestore-postgres.yaml to learnflow namespace
- [ ] T038 [US3] Create Dapr verification script — checks dapr-system pods, components registered, sidecar injector running
- [ ] T039 [US3] Install Dapr on Minikube — run installation script
- [ ] T040 [US3] Deploy Dapr components — run component deployment script
- [ ] T041 [US3] Verify Dapr deployment — run verification
- [ ] T042 [US3] Test Dapr pub/sub — deploy test service with Dapr annotations, publish and subscribe to a test topic
- [ ] T043 [US3] Test Dapr state store — store and retrieve a test key-value pair
- [ ] T044 [US3] Test idempotency — reinstall Dapr, verify no disruption

---

## Phase 6: User Story 4 — Kong API Gateway (Priority: P1)

**Goal**: Deploy Kong with routes and JWT authentication

**Independent Test**: Routes exist, JWT-protected endpoints reject unauthenticated requests

- [ ] T045 [US4] Create Kong deployment script — `helm upgrade --install kong kong/kong --namespace kong --create-namespace` with DB-less values
- [ ] T046 [US4] Create Kong declarative config script — applies kong.yaml with routes for all 7 services
- [ ] T047 [US4] Create JWT configuration script — configures JWT plugin with key and secret
- [ ] T048 [US4] Create Kong verification script — checks pod Ready, routes registered, JWT plugin active
- [ ] T049 [US4] Deploy Kong on Minikube — run deployment script
- [ ] T050 [US4] Apply routes and JWT config — run config scripts
- [ ] T051 [US4] Verify Kong deployment — run verification
- [ ] T052 [US4] Test JWT rejection — send request without token, verify 401
- [ ] T053 [US4] Test JWT acceptance — send request with valid token, verify proxy to backend

---

## Phase 7: User Story 5 — Full Infrastructure Verification (Priority: P1)

**Goal**: Comprehensive verification of all infrastructure components

**Independent Test**: Single script checks all components and produces a report

- [ ] T054 [US5] Create `verify/infrastructure-verify.py` — comprehensive check of Kafka, PostgreSQL, Dapr, Kong
- [ ] T055 [US5] Add resource usage reporting — actual vs. budgeted RAM/CPU per component
- [ ] T056 [US5] Add connectivity tests — verify Kafka → Dapr pub/sub path, PostgreSQL → Dapr state store path
- [ ] T057 [US5] Add topic validation — verify all 6 Kafka topics have correct partition counts
- [ ] T058 [US5] Add table validation — verify all 4 PostgreSQL tables have correct schemas
- [ ] T059 [US5] Run full verification on Minikube — execute and capture report
- [ ] T060 [US5] Document verification results — save pass/fail report
- [ ] T061 [US5] Create runbook for common failures — document resolution steps for each component

---

## Phase 8: Polish & Documentation

**Purpose**: Cross-cutting improvements and documentation

- [ ] T062 [P] Create `README.md` for infrastructure directory — deployment order, prerequisites, quick start
- [ ] T063 [P] Document resource budget vs. actual usage
- [ ] T064 Verify all scripts are idempotent — run full deployment twice from scratch
- [ ] T065 [P] Add cleanup scripts for tearing down each component
- [ ] T066 Verify skill-based deployment — deploy all components using only skill invocations
- [ ] T067 [P] Create troubleshooting guide for common deployment issues
- [ ] T068 Final full-stack verification — fresh Minikube, deploy everything, run comprehensive verification

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies
- **Foundational (Phase 2)**: Depends on Phase 1
- **Kafka (Phase 3)**: Depends on Phase 2 — can run in parallel with Phase 4 and Phase 6
- **PostgreSQL (Phase 4)**: Depends on Phase 2 — can run in parallel with Phase 3 and Phase 6
- **Dapr (Phase 5)**: Depends on Phase 3 (Kafka) AND Phase 4 (PostgreSQL)
- **Kong (Phase 6)**: Depends on Phase 2 — can run in parallel with Phase 3 and Phase 4
- **Verification (Phase 7)**: Depends on Phases 3, 4, 5, 6 all complete
- **Polish (Phase 8)**: Depends on Phase 7

### MVP Scope

Phases 1-4 (Setup + Foundational + Kafka + PostgreSQL) = 35 tasks

---

## Notes

- [P] tasks = different files, no dependencies
- US1 (Kafka), US2 (PostgreSQL), US4 (Kong) can deploy in parallel
- US3 (Dapr) must wait for Kafka + PostgreSQL
- All Helm operations use `upgrade --install --atomic` for idempotency
