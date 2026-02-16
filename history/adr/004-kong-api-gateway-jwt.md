# ADR-004: Kong API Gateway with JWT Authentication

- **Status:** Accepted
- **Date:** 2026-01-22
- **Feature:** Infrastructure / Security
- **Context:** LearnFlow exposes multiple backend microservices that need unified routing, rate limiting, and authentication. We needed an API gateway that runs on Kubernetes and handles JWT-based auth for student and teacher roles.

## Decision

Use **Kong API Gateway** deployed on Kubernetes with:

- **JWT Plugin**: Validates JWT tokens on all protected routes
- **Rate Limiting**: Prevents abuse of code execution and AI endpoints
- **Route Management**: Unified /api/v1/* routing to backend services
- **CORS**: Configured for frontend origin

Kong deployed via Helm chart with declarative configuration in `infrastructure/kong/`.

## Consequences

### Positive

- Single entry point for all API traffic with consistent auth enforcement
- JWT validation offloaded from individual services (services trust pre-validated requests)
- Rate limiting protects expensive AI and code execution endpoints
- Declarative configuration fits GitOps workflow with Argo CD
- Widely adopted, well-documented, strong Kubernetes support

### Negative

- Additional infrastructure component to operate and monitor
- Kong configuration has a learning curve (plugins, routes, services)
- Single point of failure if Kong goes down (mitigated by replicas)
- JWT key management requires separate secret rotation process

## Alternatives Considered

**Alternative A: Nginx Ingress Controller + Custom Auth Middleware**
- Use Kubernetes Nginx Ingress with a custom auth service
- Why rejected: More custom code to maintain, less feature-rich for API management

**Alternative B: Traefik**
- Lightweight reverse proxy with Kubernetes-native support
- Why rejected: Less mature JWT/API management plugins compared to Kong

**Alternative C: No Gateway (Direct Service Exposure)**
- Each service handles its own auth and rate limiting
- Why rejected: Duplicated security logic, inconsistent enforcement, harder to audit

## References

- Feature Spec: `specs/002-k8s-infrastructure/spec.md`
- Implementation Plan: `specs/002-k8s-infrastructure/plan.md`
- Related ADRs: ADR-003 (Dapr Service Mesh)
- Skill: `skills-library/.claude/skills/kong-k8s-setup/`
