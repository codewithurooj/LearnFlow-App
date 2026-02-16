# ADR-003: Dapr as Service Mesh Over Direct Kafka/PostgreSQL Clients

- **Status:** Accepted
- **Date:** 2026-01-20
- **Feature:** Infrastructure
- **Context:** Backend microservices need to communicate via Kafka pub/sub and persist state to PostgreSQL. We needed to decide whether each service directly integrates with Kafka and PostgreSQL clients or uses a service mesh abstraction.

## Decision

Use **Dapr (Distributed Application Runtime)** as the service mesh layer providing:

- **Pub/Sub**: Kafka messaging via Dapr pub/sub component (`pubsub-kafka`)
- **State Management**: PostgreSQL state via Dapr state store (`statestore-postgres`)
- **Service Invocation**: Inter-service calls via Dapr service invocation
- **Sidecar Pattern**: Each service gets a Dapr sidecar handling infrastructure concerns

## Consequences

### Positive

- Services are infrastructure-agnostic: switching from Kafka to RabbitMQ requires only a Dapr component change
- Simplified service code: no Kafka/PostgreSQL client library dependencies
- Consistent API across all services (HTTP/gRPC via Dapr sidecar)
- Built-in retry, circuit breaking, and observability
- Aligns with AAIF standards for cloud-native microservices

### Negative

- Additional operational complexity: Dapr control plane + sidecars to manage
- Debugging requires understanding Dapr's abstraction layer
- Slight latency overhead from sidecar proxy
- Team must learn Dapr concepts and configuration

## Alternatives Considered

**Alternative A: Direct Kafka + PostgreSQL Clients**
- Each service uses confluent-kafka-python and asyncpg directly
- Why rejected: Tight infrastructure coupling, duplicated connection logic, harder to swap backends

**Alternative B: Cloud-Managed Event Grid (Azure Event Grid / AWS EventBridge)**
- Use cloud-native eventing without self-managed Kafka
- Why rejected: Vendor lock-in, not portable across clouds, doesn't work with Minikube

**Alternative C: gRPC Direct Communication (no message broker)**
- Services call each other synchronously via gRPC
- Why rejected: Tight coupling, no async processing, no event replay capability

## References

- Feature Spec: `specs/002-k8s-infrastructure/spec.md`
- Implementation Plan: `specs/002-k8s-infrastructure/plan.md`
- Related ADRs: ADR-002 (Multi-Agent Architecture), ADR-004 (Kong API Gateway)
- External: [Dapr Documentation](https://dapr.io)
