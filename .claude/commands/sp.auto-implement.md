---
description: Automatically implement tasks using the appropriate skills and subagents based on task type detection
---

## User Input

```text
$ARGUMENTS
```

You **MUST** consider the user input before proceeding (if not empty).

## Overview

This command extends `/sp.implement` by **automatically detecting task types** and invoking the appropriate skills/subagents for each task.

## Skill & Subagent Router

### Detection Rules

When processing each task from `tasks.md`, detect the task type and invoke the corresponding skill/subagent:

| Task Pattern | Detected Type | Skill/Subagent to Use |
|--------------|---------------|----------------------|
| "FastAPI", "backend", "routes", "endpoints", "API" | Backend API | `.claude/skills/fastapi-sqlmodel.md` |
| "Next.js", "frontend", "React", "components", "pages" | Frontend | `.claude/skills/nextjs-betterauth.md` |
| "Helm", "chart", "Kubernetes", "K8s", "deployment" | K8s Deployment | `.claude/skills/helm-chart-builder.md` |
| "database", "migration", "schema", "SQLModel", "table" | Database | `.claude/agents/db-migrator/agent.md` |
| "Kafka", "consumer", "event", "pub/sub", "microservice" | Microservice | `.claude/agents/microservice-scaffolder/agent.md` |
| "Dapr", "state store", "pubsub component" | Dapr Config | `.claude/agents/dapr-generator/agent.md` |
| "MCP", "tool", "server" | MCP Server | `.claude/skills/mcp-server-creator/SKILL.md` |
| "agent", "orchestrator", "AI workflow", "OpenAI SDK" | AI Agent | `.claude/agents/agent-orchestrator/agent.md` |
| "test", "E2E", "integration test", "pytest" | Testing | `.claude/agents/testing-agent/README.md` |
| "API design", "contract", "OpenAPI" | API Design | `.claude/agents/stateless-api-designer/agent.md` |
| "Dockerfile", "container", "image" | Containerization | `.claude/skills/dockerfile-generator.md` |
| "values.yaml", "helm upgrade", "annotations" | Helm Update | `.claude/agents/helm-updater/agent.md` |

### Execution Flow

```
1. Parse tasks.md → Extract all tasks with [PENDING] status
2. For each task:
   a. Detect task type using pattern matching
   b. Load corresponding skill/subagent instructions
   c. Execute task following skill guidelines
   d. Mark task as [DONE] in tasks.md
   e. Create PHR for the task
3. If task type is unknown → use default implementation approach
4. Report progress after each phase
```

## Outline

### Step 1: Load Context

1. Run `.specify/scripts/powershell/check-prerequisites.ps1 -Json -RequireTasks -IncludeTasks`
2. Parse FEATURE_DIR and load:
   - `tasks.md` - Task list
   - `plan.md` - Architecture and tech stack
   - `spec.md` - Requirements

### Step 2: Analyze Tasks

For each task in tasks.md:

```markdown
## Task Analysis

| Task ID | Description | Detected Type | Skill/Subagent |
|---------|-------------|---------------|----------------|
| T-001   | Create FastAPI routes for chat | Backend API | fastapi-sqlmodel |
| T-002   | Build Next.js dashboard | Frontend | nextjs-betterauth |
| T-003   | Deploy to Kubernetes | K8s Deployment | helm-chart-builder |
```

### Step 3: Execute with Skills

For each task, follow this pattern:

```markdown
### Executing Task: {task_id}

**Type Detected:** {type}
**Skill Loaded:** {skill_path}

**Skill Instructions:**
{Read and follow the skill's guidelines}

**Implementation:**
{Generate code following skill templates}

**Verification:**
{Run any verification steps from skill}

**Status:** ✅ Complete
```

### Step 4: Skill Invocation Examples

#### Backend Task (FastAPI)
```
1. Read `.claude/skills/fastapi-sqlmodel.md`
2. Extract resource name from task (e.g., "chat", "quiz", "progress")
3. Generate:
   - models/{resource}.py
   - routes/{resource}s.py
   - tests/test_{resource}s.py
4. Follow JWT auth patterns from skill
```

#### Frontend Task (Next.js)
```
1. Read `.claude/skills/nextjs-betterauth.md`
2. Extract component/page from task
3. Generate:
   - app/{page}/page.tsx
   - components/{component}.tsx
   - lib/api/{resource}.ts
4. Include Better Auth integration
```

#### Infrastructure Task (Helm)
```
1. Read `.claude/skills/helm-chart-builder.md`
2. Extract service name from task
3. Generate:
   - charts/{service}/Chart.yaml
   - charts/{service}/values.yaml
   - charts/{service}/templates/*.yaml
```

#### Microservice Task (Kafka Consumer)
```
1. Read `.claude/agents/microservice-scaffolder/agent.md`
2. Extract service purpose from task
3. Generate:
   - services/{name}/app/main.py
   - services/{name}/app/consumer.py
   - services/{name}/Dockerfile
   - services/{name}/requirements.txt
```

### Step 5: Progress Tracking

After each task completion:

1. Update tasks.md: Change `[ ]` to `[X]`
2. Log to console:
   ```
   ✅ T-001: Create FastAPI routes for chat
      Skill: fastapi-sqlmodel
      Files: backend/app/routes/chat.py, backend/app/models/chat.py
   ```
3. If task fails, stop and report error

### Step 6: Completion Report

```markdown
## Implementation Complete

### Summary
- Total Tasks: 12
- Completed: 12
- Failed: 0

### Skills Used
| Skill | Tasks | Files Generated |
|-------|-------|-----------------|
| fastapi-sqlmodel | 4 | 12 files |
| nextjs-betterauth | 3 | 9 files |
| helm-chart-builder | 2 | 6 files |
| microservice-scaffolder | 2 | 8 files |
| dapr-generator | 1 | 3 files |

### Next Steps
- Run `/sp.analyze` to verify consistency
- Run tests: `pytest backend/tests/`
- Deploy: `helm install ...`
```

## Error Handling

If skill file not found:
```
⚠️ Skill not found: {skill_path}
Falling back to default implementation approach.
```

If task type cannot be detected:
```
⚠️ Unknown task type for: {task_description}
Using general implementation approach.
Please specify skill manually if needed.
```

## Manual Skill Override

User can specify skill in task description:

```markdown
- [ ] T-005: Create progress service [SKILL: microservice-scaffolder]
```

This overrides auto-detection.

---

## PHR Creation

As the main request completes, you MUST create and complete a PHR (Prompt History Record).

1) Stage: `green` (implementation)
2) Title: Generate 3-7 word title
3) Route: `history/prompts/<feature-name>/`
4) Create PHR with full PROMPT_TEXT and RESPONSE_TEXT
