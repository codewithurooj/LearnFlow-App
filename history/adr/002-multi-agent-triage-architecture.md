# ADR-002: Multi-Agent Architecture with Triage Routing

- **Status:** Accepted
- **Date:** 2026-01-18
- **Feature:** AI Agents System
- **Context:** LearnFlow needs to handle diverse student interactions: concept explanations, code reviews, debugging, exercises, and progress tracking. We needed to decide whether to use a single monolithic agent or multiple specialized agents.

## Decision

Adopt a **multi-agent architecture** with a Triage Agent as the entry point that routes queries to 5 specialist agents.

- **Triage Agent**: Classifies intent and routes to specialists
- **Concepts Agent**: Python concept explanations with adaptive difficulty
- **Code Review Agent**: PEP 8 compliance, correctness, efficiency analysis
- **Debug Agent**: Error parsing, root cause identification, struggle detection
- **Exercise Agent**: Challenge generation and auto-grading
- **Progress Agent**: Mastery tracking and summary generation

Communication via Kafka topics with Dapr pub/sub abstraction.

## Consequences

### Positive

- Each agent has focused system prompts, improving response quality
- Independent scaling: debug agent can scale during high-error periods
- Isolated failures: one agent failing doesn't take down others
- Clearer separation of concerns for development and testing
- Struggle detection is co-located with the Debug Agent where errors are analyzed

### Negative

- Additional latency from triage routing (one extra hop)
- Classification errors can send queries to wrong specialist
- More services to deploy and monitor (7 total)
- Shared state requires Dapr coordination

## Alternatives Considered

**Alternative A: Single Monolithic Agent**
- One large system prompt covering all capabilities
- Why rejected: Context window pollution, harder to maintain, cannot scale independently

**Alternative B: Client-Side Routing**
- Frontend determines which agent to call based on UI context
- Why rejected: Coupling business logic to frontend, natural language queries need NLP classification

**Alternative C: LLM Router (no dedicated triage service)**
- Use OpenAI function calling to dynamically route
- Why rejected: Higher latency and cost per query, less predictable routing

## References

- Feature Spec: `specs/005-ai-agents/spec.md`
- Implementation Plan: `specs/005-ai-agents/plan.md`
- Related ADRs: ADR-003 (Dapr Service Mesh)
