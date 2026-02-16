---
sidebar_position: 3
---

# Event System

LearnFlow uses Kafka topics via Dapr pub/sub for asynchronous communication.

## Topics

| Topic | Publisher | Consumer | Purpose |
|-------|----------|----------|---------|
| `learning.questions` | Frontend | Triage | Student questions for routing |
| `learning.responses` | All agents | Frontend | Agent responses to display |
| `code.submissions` | Frontend | Code Runner, Code Review | Code to execute and review |
| `code.results` | Code Runner | Frontend | Execution output |
| `struggle.detected` | Debug, Code Runner, Progress | Teacher Dashboard | Struggle alerts |
| `progress.updated` | Progress | Frontend | Mastery score changes |

## Event Flow

```
Student asks question
    → learning.questions (Kafka)
    → Triage classifies & routes
    → Specialist agent processes
    → learning.responses (Kafka)
    → Frontend displays response

Student submits code
    → code.submissions (Kafka)
    → Code Runner executes (parallel)
    → Code Review analyzes (parallel)
    → code.results (Kafka) → Frontend
    → progress.updated (Kafka) → Frontend
    → struggle.detected (Kafka) → Teacher (if applicable)
```
