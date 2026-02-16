---
slug: /
sidebar_position: 1
---

# LearnFlow

**AI-Powered Python Tutoring Platform**

LearnFlow is a platform where students learn Python through AI-powered tutoring, a built-in code editor, coding quizzes, and mastery tracking. Teachers can monitor class progress and receive struggle alerts.

## Key Features

- **AI Chat Tutors** - 6 specialized agents (Triage, Concepts, Debug, Code Review, Exercise, Progress)
- **Monaco Code Editor** - Write and run Python in the browser with a 5s sandboxed executor
- **Mastery Tracking** - Per-topic scores across exercises, quizzes, code quality, and streaks
- **Struggle Detection** - Automatic alerts when students are stuck
- **Teacher Dashboard** - Class-wide progress monitoring

## Built With Skills

This project was built using the **Skills + MCP Code Execution** paradigm:

```
Traditional: You write code → Code runs → Application works
Agentic:     You write Skills → AI learns → AI writes code → Application works
```

Each Skill is ~100 tokens (vs 50,000+ for direct MCP integration), making AI-driven development dramatically more efficient.

## Tech Stack

| Layer | Technology |
|-------|------------|
| Frontend | Next.js 14 + Monaco Editor |
| Backend | FastAPI + OpenAI SDK (6 microservices) |
| Service Mesh | Dapr (state, pub/sub, invocation) |
| Messaging | Apache Kafka |
| Database | PostgreSQL |
| Gateway | Kong |
| Orchestration | Kubernetes |
| CI/CD | GitHub Actions + ArgoCD |

## Quick Start

```bash
# Clone and start
git clone <repo-url>
cd learnflow-app

# Copy env and add your OpenAI key
cp backend/.env.example backend/.env

# Start everything
docker compose up -d

# Open http://localhost:3000
```
