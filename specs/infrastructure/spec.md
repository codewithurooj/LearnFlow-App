# Feature Specification: K8s Infrastructure

**Feature Branch**: `002-k8s-infrastructure`
**Created**: 2026-01-24
**Status**: Draft
**Input**: User description: "Create specification for infrastructure deployment on Kubernetes. Local development uses Minikube (4 CPU, 8GB RAM). All deployments via Helm charts (no raw kubectl). Skills will automate these deployments."

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Deploy Kafka with Single Skill Invocation (Priority: P0)

A developer invokes the kafka-k8s-setup skill to deploy Apache Kafka on Minikube. The skill creates the kafka namespace, deploys Kafka using Bitnami Helm chart with KRaft mode (no Zookeeper), and creates all 6 LearnFlow topics. The deployment is verified automatically.

**Why this priority**: Kafka is the messaging backbone for all inter-service communication in LearnFlow.

**Independent Test**: Can be fully tested by running the skill on a fresh Minikube cluster and verifying Kafka pods are running and all 6 topics exist.

**Acceptance Scenarios**:

1. **Given** a running Minikube cluster, **When** the kafka-k8s-setup skill is invoked, **Then** Kafka is deployed in the `kafka` namespace with KRaft mode enabled.
2. **Given** Kafka is deployed, **When** topic creation runs, **Then** all 6 topics are created: `learning.questions`, `learning.responses`, `code.submissions`, `code.results`, `struggle.detected`, `progress.updated`.
3. **Given** the deployment completes, **When** verification runs, **Then** all Kafka pods show Ready status and topics are listable via kafka-topics.sh.
4. **Given** the skill is run again, **When** Kafka already exists, **Then** the deployment is updated idempotently without data loss.

---

### User Story 2 - Deploy PostgreSQL with Schema Migrations (Priority: P0)

A developer invokes the postgres-k8s-setup skill to deploy PostgreSQL on Minikube. The skill deploys PostgreSQL using Bitnami Helm chart, runs schema migrations to create all required tables, and stores the connection string as a Kubernetes secret.

**Why this priority**: PostgreSQL stores all user data, progress, code submissions, and chat history.

**Independent Test**: Can be tested by deploying PostgreSQL and verifying all 4 tables exist with correct schemas and the connection secret is created.

**Acceptance Scenarios**:

1. **Given** a running Minikube cluster, **When** the postgres-k8s-setup skill is invoked, **Then** PostgreSQL is deployed in the `learnflow` namespace.
2. **Given** PostgreSQL is running, **When** migrations execute, **Then** tables `users`, `progress`, `code_submissions`, and `chat_history` are created with indexes.
3. **Given** the connection string, **When** stored as a K8s secret, **Then** it is accessible as `postgres-credentials` in the `learnflow` namespace.
4. **Given** the skill is run again, **When** tables already exist, **Then** migrations are idempotent (no duplicates or data loss).

---

### User Story 3 - Configure Dapr for All Microservices (Priority: P0)

A developer invokes the dapr-k8s-setup skill to install Dapr on the cluster and configure components for pub/sub (Kafka), state store (PostgreSQL), and service invocation. All LearnFlow microservices can then use Dapr sidecars.

**Why this priority**: Dapr provides the service mesh that enables pub/sub, state management, and service invocation across all microservices.

**Independent Test**: Can be tested by deploying Dapr, creating components, and verifying a test service can publish/subscribe to Kafka via Dapr and store/retrieve state.

**Acceptance Scenarios**:

1. **Given** Kafka and PostgreSQL are deployed, **When** the dapr-k8s-setup skill is invoked, **Then** Dapr is installed in the `dapr-system` namespace.
2. **Given** Dapr is installed, **When** components are configured, **Then** a pub/sub component (Kafka) and state store component (PostgreSQL) are created.
3. **Given** a test service with Dapr annotations, **When** deployed, **Then** the Dapr sidecar injects and the service can use pub/sub and state APIs.

---

### User Story 4 - Setup Kong API Gateway with JWT Auth (Priority: P1)

A developer invokes the kong-k8s-setup skill to deploy Kong API Gateway in DB-less mode. Kong is configured with routes to all backend services and JWT authentication for protected endpoints.

**Why this priority**: Kong provides the single entry point for all API traffic and handles authentication, but the backend services can be developed and tested without it initially.

**Independent Test**: Can be tested by deploying Kong and verifying routes exist and JWT-protected endpoints reject unauthenticated requests.

**Acceptance Scenarios**:

1. **Given** a running Minikube cluster, **When** the kong-k8s-setup skill is invoked, **Then** Kong is deployed in DB-less mode in the `kong` namespace.
2. **Given** Kong is deployed, **When** routes are configured, **Then** routes exist for all backend services (triage, concepts, code-runner, debug, exercise, progress, code-review).
3. **Given** JWT authentication is configured, **When** a request without a valid JWT hits a protected route, **Then** Kong returns 401 Unauthorized.
4. **Given** a valid JWT token, **When** included in the Authorization header, **Then** the request is proxied to the correct backend service.

---

### User Story 5 - Full Infrastructure Verification (Priority: P1)

A developer runs a comprehensive verification that checks all infrastructure components (Kafka, PostgreSQL, Dapr, Kong) are deployed, healthy, and properly connected. The verification produces a clear report.

**Why this priority**: End-to-end verification ensures all components work together before deploying application services.

**Independent Test**: Can be tested by running the verification after all components are deployed and confirming a full pass report.

**Acceptance Scenarios**:

1. **Given** all infrastructure is deployed, **When** the infrastructure-verify script runs, **Then** each component is checked for pod health, connectivity, and configuration.
2. **Given** verification completes, **When** all checks pass, **Then** a summary report shows `✓` for each component with resource usage.
3. **Given** a component is unhealthy, **When** verification runs, **Then** the report shows `✗` for that component with diagnostic details.

---

### Edge Cases

- What happens when Minikube runs out of memory during deployment? The skill detects OOM conditions and reports resource requirements vs. available resources.
- What happens when Helm chart download fails? The script retries once after 10 seconds, then fails with a clear network error message.
- What happens when Kafka topic creation partially fails? The script reports which topics were created and which failed, with a partial success exit code (2).
- What happens when PostgreSQL migrations conflict with existing data? Migrations use `IF NOT EXISTS` for all CREATE statements to ensure idempotency.
- What happens when Dapr sidecar injection fails? The verification script checks for sidecar presence and reports the Dapr injector status.
- What happens when Kong routes overlap? The declarative config validates route uniqueness before applying.

## Requirements *(mandatory)*

### Functional Requirements

**Kafka (FR-001 to FR-005)**:
- **FR-001**: System MUST deploy Kafka using Bitnami Helm chart with KRaft mode (no Zookeeper dependency).
- **FR-002**: System MUST create the `kafka` namespace if it does not exist.
- **FR-003**: System MUST create all 6 topics: `learning.questions`, `learning.responses`, `code.submissions`, `code.results`, `struggle.detected`, `progress.updated`.
- **FR-004**: System MUST configure topics with appropriate partition counts (3 for high-throughput topics, 1 for low-throughput).
- **FR-005**: System MUST set retention period to 7 days for all topics.

**PostgreSQL (FR-006 to FR-010)**:
- **FR-006**: System MUST deploy PostgreSQL using Bitnami Helm chart with persistent volume.
- **FR-007**: System MUST create 4 tables: `users` (id, email, name, role, created_at), `progress` (id, user_id, topic, mastery_score, level, updated_at), `code_submissions` (id, user_id, code, result, created_at), `chat_history` (id, user_id, session_id, messages, created_at).
- **FR-008**: System MUST store the connection string as Kubernetes secret `postgres-credentials`.
- **FR-009**: System MUST create indexes on foreign key columns and frequently queried fields.
- **FR-010**: System MUST apply migrations idempotently using `IF NOT EXISTS` guards.

**Dapr (FR-011 to FR-015)**:
- **FR-011**: System MUST install Dapr using the official Helm chart in the `dapr-system` namespace.
- **FR-012**: System MUST create a pub/sub component bound to Kafka.
- **FR-013**: System MUST create a state store component bound to PostgreSQL.
- **FR-014**: System MUST enable service invocation for inter-service HTTP calls.
- **FR-015**: System MUST configure sidecar injection annotations for the `learnflow` namespace.

**Kong (FR-016 to FR-021)**:
- **FR-016**: System MUST deploy Kong in DB-less mode using the Kong Helm chart.
- **FR-017**: System MUST configure declarative routes for all 7 backend services.
- **FR-018**: System MUST enable JWT authentication plugin.
- **FR-019**: System MUST configure CORS for frontend origin.
- **FR-020**: System MUST set rate limiting to prevent abuse.
- **FR-021**: System MUST provide a health check endpoint at Kong's admin API.

### Key Entities

- **Namespace**: A Kubernetes namespace isolating infrastructure components (`kafka`, `learnflow`, `dapr-system`, `kong`).
- **Helm Release**: A deployed Helm chart instance with version, values, and status.
- **Kafka Topic**: A message channel with name, partition count, replication factor, and retention period.
- **Database Table**: A PostgreSQL table with schema, indexes, and migration version.
- **Dapr Component**: A Dapr building block configuration (pub/sub or state store) binding to infrastructure.
- **Kong Route**: An API gateway routing rule mapping a path pattern to a backend service with optional authentication.

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: All infrastructure deploys from skill invocations with zero manual kubectl commands.
- **SC-002**: Kafka deployment (including topics) completes in under 3 minutes on Minikube.
- **SC-003**: PostgreSQL deployment (including migrations) completes in under 2 minutes.
- **SC-004**: Dapr installation and component creation completes in under 2 minutes.
- **SC-005**: Kong deployment with route configuration completes in under 2 minutes.
- **SC-006**: Total infrastructure resource usage stays under 2.5GB RAM and 1.25 CPU.
- **SC-007**: Full infrastructure verification passes on a fresh Minikube cluster.
- **SC-008**: All deployments are idempotent — running skills twice produces no errors or data loss.

## Assumptions

- Minikube is running with 4 CPU and 8GB RAM (at least 2.5GB available for infrastructure).
- Helm 3.x is installed and initialized.
- kubectl is configured for the Minikube cluster.
- Network access is available for initial Helm chart downloads.
- Minikube's default storage provisioner is available for persistent volumes.
- Skills from the skills-library (001) are available for deployment automation.
