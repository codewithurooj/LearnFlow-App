---
sidebar_position: 2
---

# Services

## AI Agent Services

| Agent | Port | Purpose |
|-------|------|---------|
| **Triage** | 8001 | Routes questions to the right specialist using keyword + AI hybrid classification |
| **Concepts** | 8002 | Explains Python concepts with examples, adapts to mastery level |
| **Code Runner** | 8003 | Executes Python in a sandboxed subprocess (5s timeout, 50MB memory) |
| **Debug** | 8004 | Parses errors, identifies root causes, provides hints before solutions |
| **Exercise** | 8005 | Generates coding challenges and auto-grades submissions |
| **Progress** | 8006 | Tracks per-topic mastery scores and calculates overall progress |
| **Code Review** | 8007 | Analyzes code for correctness, style, efficiency, and readability |

## Mastery Calculation

```
Topic Mastery = Exercises (40%) + Quizzes (30%) + Code Quality (20%) + Streak (10%)
```

| Score | Level | Color |
|-------|-------|-------|
| 0-40% | Beginner | Red |
| 41-70% | Learning | Yellow |
| 71-90% | Proficient | Green |
| 91-100% | Mastered | Blue |

## Struggle Detection

Triggers when a student shows signs of being stuck:

- Same error type 3+ times
- Stuck on an exercise > 10 minutes
- Quiz score < 50%
- 5+ consecutive failed code executions
