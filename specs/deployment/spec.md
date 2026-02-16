# Feature Specification: Cloud Deployment & CI/CD

**Feature Branch**: `006-cloud-deployment-cicd`
**Created**: 2026-01-25
**Status**: Draft
**Input**: User description: "Create specification for cloud deployment and CI/CD. GitOps with Argo CD. GitHub Actions for CI. Target: Azure/Google/Oracle Cloud."

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Push to Main Triggers Automatic Staging Deployment (Priority: P1)

A developer pushes code to the main branch. GitHub Actions CI automatically runs linting, tests, builds Docker images, pushes them to the container registry, and updates Kubernetes manifests. Argo CD detects the manifest change and auto-syncs the staging environment.

**Why this priority**: Automated staging deployment is the foundation of the CI/CD pipeline. Everything else depends on it.

**Independent Test**: Can be tested by pushing a code change to main and verifying the staging environment is updated within 10 minutes without manual intervention.

**Acceptance Scenarios**:

1. **Given** a push to main branch, **When** GitHub Actions triggers, **Then** the CI pipeline runs lint, test, and build stages sequentially.
2. **Given** CI passes, **When** Docker images are built, **Then** they are tagged with the git SHA and pushed to the container registry.
3. **Given** images are pushed, **When** manifests are updated, **Then** Argo CD detects the change and syncs the staging environment.
4. **Given** sync completes, **When** health checks pass, **Then** the deployment is marked as successful and a notification is sent.
5. **Given** CI fails at any stage, **When** the failure occurs, **Then** the pipeline stops, the developer is notified, and no deployment happens.

---

### User Story 2 - One-Click Promote Staging to Production (Priority: P2)

After staging has been verified, a developer triggers a promotion workflow that deploys the same image versions from staging to production. The promotion uses Kustomize overlays to apply production-specific configuration.

**Why this priority**: Production promotion is critical for delivering value to users but requires staging to work first.

**Independent Test**: Can be tested by triggering the promote workflow after a successful staging deployment and verifying production matches staging versions.

**Acceptance Scenarios**:

1. **Given** staging is verified and stable, **When** a developer triggers the promote workflow (manual dispatch), **Then** production manifests are updated with staging image versions.
2. **Given** production manifests are updated, **When** Argo CD syncs production, **Then** all services are updated with zero downtime using rolling updates.
3. **Given** production deployment completes, **When** health checks pass, **Then** the promotion is marked as successful.

---

### User Story 3 - Rollback Within 5 Minutes (Priority: P2)

If issues are detected in a deployment, a developer triggers a rollback workflow that reverts to the previous known-good version within 5 minutes. Argo CD handles the rollback using its revision history.

**Why this priority**: Rapid rollback is essential for production reliability but is a safety net, not a primary flow.

**Independent Test**: Can be tested by deploying a broken version, triggering rollback, and verifying the previous version is restored within 5 minutes.

**Acceptance Scenarios**:

1. **Given** a problematic deployment, **When** a developer triggers rollback via workflow dispatch, **Then** Argo CD reverts to the previous sync revision.
2. **Given** rollback is triggered, **When** the previous version is restored, **Then** all services are healthy within 5 minutes.
3. **Given** rollback completes, **When** the developer reviews, **Then** an audit trail shows what was reverted and by whom.

---

### User Story 4 - Health Dashboard Shows All Service Status (Priority: P3)

A developer or operator views a Grafana dashboard showing real-time health of all LearnFlow services. The dashboard displays latency, error rates, agent response times, and SLO compliance. Alerts fire when SLO thresholds are violated.

**Why this priority**: Monitoring is important for operational readiness but all services must be deployed first.

**Independent Test**: Can be tested by viewing the Grafana dashboard and verifying all services show metrics, and triggering a synthetic alert by exceeding a threshold.

**Acceptance Scenarios**:

1. **Given** all services are deployed, **When** a developer opens the Grafana dashboard, **Then** metrics for all 8 LearnFlow services are displayed.
2. **Given** metrics are flowing, **When** a service's error rate exceeds 5%, **Then** an alert fires within 2 minutes.
3. **Given** the dashboard, **When** viewing latency metrics, **Then** p50, p95, and p99 latencies are shown per service.
4. **Given** SLO configuration, **When** any SLO is violated (e.g., latency > 3s for >5 min), **Then** an alert is triggered.

---

### Edge Cases

- What happens when the CI pipeline fails during image push? The pipeline retries the push once, then fails with a clear error. No manifests are updated.
- What happens when Argo CD sync fails? Argo CD retries based on its sync policy. After 3 failures, an alert is sent and manual intervention is required.
- What happens during a rollback if the previous version also has issues? The operator can specify a specific revision number to rollback to instead of just "previous".
- What happens when secrets rotation occurs during deployment? External Secrets Operator handles rotation independently of deployment cycles; secrets sync asynchronously.
- What happens when a cloud provider is unreachable? Kustomize overlays are cloud-agnostic; the same manifests work on AKS, GKE, and OKE with only the overlay values changing.
- What happens when Prometheus storage fills up? Retention is configured for 15 days; older data is automatically purged.

## Requirements *(mandatory)*

### Functional Requirements

**CI Pipeline (FR-001 to FR-006)**:
- **FR-001**: System MUST trigger CI pipeline on push to main branch.
- **FR-002**: System MUST run lint, test, and build stages in the CI pipeline.
- **FR-003**: System MUST build Docker images for all services and tag with git SHA.
- **FR-004**: System MUST push images to container registry on successful build.
- **FR-005**: System MUST update Kubernetes manifests with new image tags.
- **FR-006**: System MUST send notifications on pipeline success or failure.

**GitOps / Argo CD (FR-007 to FR-012)**:
- **FR-007**: System MUST use Argo CD for continuous delivery with auto-sync enabled.
- **FR-008**: System MUST configure prune and self-heal for Argo CD applications.
- **FR-009**: System MUST maintain separate Argo CD applications for staging and production.
- **FR-010**: System MUST support manual promotion from staging to production.
- **FR-011**: System MUST support rollback to any previous revision via workflow dispatch.
- **FR-012**: System MUST maintain an audit trail of all deployments and rollbacks.

**Kubernetes Configuration (FR-013 to FR-018)**:
- **FR-013**: System MUST use Kustomize with base + overlays (local, staging, production).
- **FR-014**: System MUST define all services as Kubernetes Deployments with resource limits.
- **FR-015**: System MUST configure Ingress for external access.
- **FR-016**: System MUST enforce zero-downtime deployments using rolling update strategy.
- **FR-017**: System MUST include readiness and liveness probes for all services.
- **FR-018**: System MUST define HorizontalPodAutoscaler for production environment.

**Secrets Management (FR-019 to FR-021)**:
- **FR-019**: System MUST use Kubernetes secrets for local/development environment.
- **FR-020**: System MUST use External Secrets Operator (ESO) for cloud environments.
- **FR-021**: System MUST NEVER store secrets in git (enforced by CI checks).

**Monitoring & Alerting (FR-022 to FR-024)**:
- **FR-022**: System MUST deploy Prometheus for metrics collection from all services.
- **FR-023**: System MUST deploy Grafana with pre-configured dashboards for latency, error rate, and agent response time.
- **FR-024**: System MUST configure alerting rules for SLO violations (latency > 3s, error rate > 5%, agent timeout).

### Key Entities

- **Pipeline Run**: A CI execution with ID, trigger (push/manual), stages, status, duration, and artifacts.
- **Deployment**: A Kubernetes deployment event with service name, image tag, environment, timestamp, and status.
- **Environment**: A deployment target (local, staging, production) with its Kustomize overlay and Argo CD application.
- **Service**: A LearnFlow microservice with name, port, image, resource limits, and health status.
- **Alert**: A monitoring notification with rule name, severity, service, threshold, current value, and timestamp.
- **Secret**: A sensitive configuration value with name, namespace, source (K8s secret or ESO), and rotation policy.

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: Push-to-staging deployment completes in under 10 minutes end-to-end.
- **SC-002**: Zero-downtime deployments verified — no 5xx errors during rolling updates.
- **SC-003**: Rollback completes within 5 minutes of trigger.
- **SC-004**: Production promotion from staging completes in under 5 minutes.
- **SC-005**: Grafana dashboard shows metrics for all 8 services within 2 minutes of deployment.
- **SC-006**: SLO alerts fire within 2 minutes of threshold violation.
- **SC-007**: CI pipeline detects and blocks any commit containing secrets in code.
- **SC-008**: Kustomize overlays work across all 3 cloud providers (AKS, GKE, OKE) without modification.

## Assumptions

- GitHub is the source code repository with GitHub Actions available.
- A container registry is available (GitHub Container Registry or cloud-provider registry).
- Argo CD will be deployed in the cluster (local and cloud).
- Kustomize is used instead of Helm for application deployment (Helm used only for infrastructure).
- External Secrets Operator supports Azure Key Vault, Google Secret Manager, and Oracle Vault.
- Prometheus and Grafana are deployed using community Helm charts.
- Services expose Prometheus-compatible metrics endpoints.
- Cloud Kubernetes services (AKS, GKE, OKE) are provisioned separately (outside scope of this feature).
