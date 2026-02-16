---
description: Execute full spec-driven workflow from specification to implementation with automatic skill/subagent routing
---

## User Input

```text
$ARGUMENTS
```

You **MUST** consider the user input before proceeding (if not empty).

## Overview

This command orchestrates the **complete spec-driven development workflow**, automatically invoking the appropriate commands, skills, and subagents at each stage.

## Workflow Stages

```
┌─────────────┐    ┌─────────────┐    ┌─────────────┐    ┌─────────────┐
│  /sp.specify │ → │  /sp.plan   │ → │  /sp.tasks  │ → │/sp.auto-impl│
│             │    │             │    │             │    │             │
│ Creates:    │    │ Creates:    │    │ Creates:    │    │ Uses:       │
│ - spec.md   │    │ - plan.md   │    │ - tasks.md  │    │ - Skills    │
│             │    │ - research.md│   │             │    │ - Subagents │
│             │    │ - contracts/│    │             │    │             │
└─────────────┘    └─────────────┘    └─────────────┘    └─────────────┘
       │                  │                  │                  │
       ▼                  ▼                  ▼                  ▼
   [CHECKPOINT]      [CHECKPOINT]      [CHECKPOINT]      [CHECKPOINT]
   User Review       User Review       User Review       Verify Tests
```

## Execution Modes

### Mode 1: Full Auto (Default)
```bash
/sp.workflow <feature-description>
```
Runs all stages automatically, pausing only for required user input.

### Mode 2: Step-by-Step
```bash
/sp.workflow <feature-description> --step
```
Pauses after each stage for user approval before continuing.

### Mode 3: Resume from Stage
```bash
/sp.workflow --resume plan
```
Resumes from a specific stage (spec, plan, tasks, implement).

---

## Outline

### Stage 0: Initialize Feature

1. Parse user input for feature description
2. Create feature directory structure:
   ```
   specs/<feature-name>/
   ├── spec.md          # Created in Stage 1
   ├── plan.md          # Created in Stage 2
   ├── tasks.md         # Created in Stage 3
   ├── research.md      # Created in Stage 2
   ├── data-model.md    # Created in Stage 2
   ├── contracts/       # Created in Stage 2
   └── checklists/      # Optional
   ```
3. Report: "Feature directory initialized at specs/<feature-name>/"

### Stage 1: Specification (`/sp.specify`)

**Invoke:** `/sp.specify <feature-description>`

**Expected Output:**
- `spec.md` with functional requirements, user stories, acceptance criteria

**Checkpoint:**
- Display spec.md summary
- Ask: "Proceed to planning? (yes/no/edit)"
- If "edit" → Allow user to provide feedback, re-run specify

**ADR Check:**
- If significant architectural decisions detected → Suggest `/sp.adr`

### Stage 2: Planning (`/sp.plan`)

**Invoke:** `/sp.plan`

**Expected Output:**
- `plan.md` - Technical architecture
- `research.md` - Technology decisions
- `data-model.md` - Entity definitions
- `contracts/` - API specifications

**Skill/Subagent Triggers:**
- API design detected → Load `stateless-api-designer` agent
- Database schema needed → Load `db-migrator` agent context

**Checkpoint:**
- Display plan summary (tech stack, architecture)
- Ask: "Proceed to task generation? (yes/no/edit)"

**ADR Check:**
- Multiple architectural decisions → Suggest `/sp.adr` for each

### Stage 3: Task Generation (`/sp.tasks`)

**Invoke:** `/sp.tasks`

**Expected Output:**
- `tasks.md` with phased, dependency-ordered tasks

**Skill Detection:**
For each generated task, annotate with detected skill:
```markdown
- [ ] T-001: Create FastAPI routes for chat [SKILL: fastapi-sqlmodel]
- [ ] T-002: Build Next.js dashboard [SKILL: nextjs-betterauth]
- [ ] T-003: Set up Kafka consumers [SKILL: microservice-scaffolder]
```

**Checkpoint:**
- Display task summary (count by phase, skill distribution)
- Ask: "Proceed to implementation? (yes/no/edit)"

### Stage 4: Implementation (`/sp.auto-implement`)

**Invoke:** `/sp.auto-implement`

**Execution:**
1. Load skill registry from `.claude/skill-registry.md`
2. For each task:
   - Detect skill from annotation or pattern matching
   - Load skill instructions
   - Execute task following skill guidelines
   - Mark task complete in tasks.md
3. Report progress after each phase

**Skill Loading Order:**
1. Check task annotation: `[SKILL: name]` or `[AGENT: name]`
2. If no annotation, pattern match against skill registry
3. If no match, use default implementation approach

**Progress Reporting:**
```
Phase 1: Setup ████████████ 100%
  ✅ T-001: Project initialization
  ✅ T-002: Dependencies installed

Phase 2: Backend ████████░░ 80%
  ✅ T-003: FastAPI routes [fastapi-sqlmodel]
  ✅ T-004: Database models [db-migrator]
  🔄 T-005: Kafka consumers [microservice-scaffolder]
```

### Stage 5: Verification

After implementation:

1. **Run Tests:**
   ```bash
   pytest backend/tests/ -v
   npm test --prefix frontend
   ```

2. **Analyze Artifacts:**
   - Invoke `/sp.analyze` to check consistency

3. **Final Report:**
   ```markdown
   ## Workflow Complete

   ### Feature: <feature-name>

   | Stage | Status | Artifacts |
   |-------|--------|-----------|
   | Specify | ✅ | spec.md |
   | Plan | ✅ | plan.md, research.md, contracts/ |
   | Tasks | ✅ | tasks.md (15 tasks) |
   | Implement | ✅ | 42 files generated |
   | Verify | ✅ | All tests passing |

   ### Skills Used
   - fastapi-sqlmodel: 5 tasks
   - nextjs-betterauth: 4 tasks
   - microservice-scaffolder: 3 tasks
   - helm-chart-builder: 2 tasks
   - db-migrator: 1 task

   ### Next Steps
   - Deploy: `helm install <feature> ./charts/<feature>`
   - Monitor: Check Kubernetes pods
   - Document: Update README with new feature
   ```

---

## Error Handling

### Stage Failure
If any stage fails:
1. Stop workflow
2. Report error with context
3. Suggest fix or manual intervention
4. Provide resume command: `/sp.workflow --resume <stage>`

### Skill Not Found
If skill file missing:
1. Warn: "Skill <name> not found"
2. Fallback to default implementation
3. Continue workflow

### User Abort
If user says "no" at checkpoint:
1. Stop workflow
2. Save progress
3. Provide resume command

---

## Command Chaining

This workflow internally chains these commands:

```
/sp.specify → /sp.plan → /sp.tasks → /sp.auto-implement → /sp.analyze
     │             │           │              │                │
     │             │           │              │                └── Verify
     │             │           │              └── Uses skill registry
     │             │           └── Annotates tasks with skills
     │             └── Triggers stateless-api-designer, db-migrator
     └── Creates spec.md
```

---

## Examples

### Example 1: Full Feature
```bash
User: /sp.workflow Create an AI tutoring chat feature with code execution

Claude:
Stage 0: Initializing feature directory...
✅ Created: specs/ai-tutoring-chat/

Stage 1: Running /sp.specify...
✅ Created: spec.md
Summary: 8 user stories, 15 acceptance criteria

Proceed to planning? (yes/no/edit)
> yes

Stage 2: Running /sp.plan...
✅ Created: plan.md, research.md, data-model.md, contracts/
Tech Stack: FastAPI, Next.js, Kafka, PostgreSQL
📋 ADR suggestion: "AI Agent Architecture" - Document? Run /sp.adr

Proceed to tasks? (yes/no/edit)
> yes

Stage 3: Running /sp.tasks...
✅ Created: tasks.md
Tasks: 15 total
  - Backend (fastapi-sqlmodel): 5
  - Frontend (nextjs-betterauth): 4
  - Infrastructure (dapr-generator): 3
  - Agents (agent-orchestrator): 2
  - Testing (testing-agent): 1

Proceed to implementation? (yes/no/edit)
> yes

Stage 4: Running /sp.auto-implement...
[Progress updates...]

Stage 5: Verification...
✅ All tests passing
✅ Artifact consistency verified

## Workflow Complete!
```

### Example 2: Resume from Plan
```bash
User: /sp.workflow --resume plan

Claude:
Resuming workflow from Stage 2 (Plan)...
Found existing spec.md
Running /sp.plan...
[Continues from plan stage]
```

---

## PHR Creation

As each stage completes, create a PHR:

- Stage 1 (Specify): Stage = `spec`
- Stage 2 (Plan): Stage = `plan`
- Stage 3 (Tasks): Stage = `tasks`
- Stage 4 (Implement): Stage = `green`

Final PHR summarizes entire workflow.
