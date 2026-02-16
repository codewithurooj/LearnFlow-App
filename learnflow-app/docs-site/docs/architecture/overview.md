---
sidebar_position: 1
---

# Architecture Overview

LearnFlow uses a microservices architecture running on Kubernetes with Dapr as the service mesh.

```
┌─────────────────────────────────────────────────────┐
│                 Kubernetes Cluster                   │
│                                                     │
│  Kong API Gateway                                   │
│       │                                             │
│  ┌────┴────────────────────────────────────────┐    │
│  │  Dapr Sidecar Mesh                          │    │
│  │  ├── Triage    (8001) - Question routing     │    │
│  │  ├── Concepts  (8002) - Python explanations  │    │
│  │  ├── Code Runner (8003) - Sandboxed exec     │    │
│  │  ├── Debug     (8004) - Error analysis       │    │
│  │  ├── Exercise  (8005) - Challenge generator  │    │
│  │  ├── Progress  (8006) - Mastery tracking     │    │
│  │  └── Code Review (8007) - Code analysis      │    │
│  └─────────────────────────────────────────────┘    │
│       │                    │                         │
│   Kafka (pub/sub)    PostgreSQL (state)              │
└─────────────────────────────────────────────────────┘
```

## Design Principles

1. **Stateless services** - All state managed via Dapr (PostgreSQL statestore)
2. **Event-driven** - Services communicate via Kafka topics through Dapr pub/sub
3. **AI-native** - Each service wraps an OpenAI SDK agent with specialized prompts
4. **Sandbox isolation** - Code execution has strict resource limits (5s, 50MB, no network)
5. **Mastery-adaptive** - Content difficulty adapts to each student's mastery level
