---
sidebar_position: 1
---

# Local Development

## Prerequisites

- Docker Desktop
- Node.js 18+
- An OpenAI API key

## Setup

```bash
# Clone the repo
git clone <repo-url>
cd learnflow-app

# Create env file
cp backend/.env.example backend/.env
# Edit backend/.env and set OPENAI_API_KEY

# Start all services
docker compose up -d
```

## Services

| Service | URL |
|---------|-----|
| Frontend | http://localhost:3000 |
| Triage API | http://localhost:8001/docs |
| Concepts API | http://localhost:8002/docs |
| Code Runner API | http://localhost:8003/docs |
| Debug API | http://localhost:8004/docs |
| Exercise API | http://localhost:8005/docs |
| Progress API | http://localhost:8006/docs |
| Code Review API | http://localhost:8007/docs |

## Useful Commands

```bash
# View logs for a service
docker compose logs -f triage

# Restart a single service
docker compose restart concepts

# Stop everything
docker compose down

# Stop and reset database
docker compose down -v
```
