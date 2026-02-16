# Claude Code Rules - Hackathon III: Reusable Intelligence

---

## PROJECT OVERVIEW

### What We're Building

**Project Name:** Hackathon III - Reusable Intelligence and Cloud-Native Mastery

**Product:** LearnFlow - An AI-powered Python tutoring platform where students can:
- Chat with AI tutors to learn Python concepts
- Write and run code in a Monaco editor
- Take coding quizzes and track progress
- Teachers can monitor class progress and receive struggle alerts

**Paradigm Shift:** Instead of writing code manually, we teach AI coding agents (Claude Code & Goose) how to build the application using "Skills with MCP Code Execution."

> **Key Principle:** *The Skills are the product, not just documentation or the LearnFlow app.*

### Core Concept: Skills with MCP Code Execution

```
Traditional: You write code → Code runs → Application works
Agentic:     You write Skills → AI learns → AI writes code → Application works
```

**Why Skills + Code Execution?**
- Direct MCP integration: 50,000+ tokens consumed before conversation starts
- Skills + Scripts: ~100 tokens (80-98% reduction)

```
.claude/skills/<skill-name>/
├── SKILL.md           # ~100 tokens (loaded when triggered)
├── REFERENCE.md       # 0 tokens (loaded on-demand)
└── scripts/
    ├── deploy.sh      # 0 tokens (executed, not loaded)
    └── verify.py      # 0 tokens (executed, returns minimal output)
```

---

## DELIVERABLES

### Repository 1: `skills-library/`
A collection of reusable Skills that work on both Claude Code and Goose.

```
skills-library/
├── README.md
├── .claude/skills/
│   ├── agents-md-gen/          # Generate AGENTS.md files
│   ├── kafka-k8s-setup/        # Deploy Kafka on Kubernetes
│   ├── postgres-k8s-setup/     # Deploy PostgreSQL on Kubernetes
│   ├── fastapi-dapr-agent/     # FastAPI + Dapr service templates
│   ├── mcp-code-execution/     # MCP with code execution pattern
│   ├── nextjs-k8s-deploy/      # Deploy Next.js applications
│   └── docusaurus-deploy/      # Deploy documentation sites
└── docs/
    └── skill-development-guide.md
```

### Repository 2: `learnflow-app/`
The complete AI tutoring platform built entirely using Skills via Claude Code and Goose.

---

## TECHNOLOGY STACK

| Layer | Technology | Purpose |
|-------|------------|---------|
| **AI Coding Agents** | Claude Code, Goose | Execute Skills to build the application |
| **Frontend** | Next.js 14 + Monaco Editor | User interface with embedded code editor |
| **Backend** | FastAPI + OpenAI SDK | AI-powered tutoring agents as microservices |
| **Authentication** | Better Auth | User authentication |
| **Service Mesh** | Dapr | State management, pub/sub, service invocation |
| **Messaging** | Apache Kafka | Asynchronous event-driven communication |
| **Database** | Neon PostgreSQL | User data, progress, code submissions |
| **API Gateway** | Kong | Routes traffic, handles JWT authentication |
| **Orchestration** | Kubernetes (Minikube) | Container orchestration |
| **CI/CD** | GitHub Actions + Argo CD | GitOps continuous delivery |
| **Documentation** | Docusaurus | Auto-generated documentation site |

---

## LEARNFLOW ARCHITECTURE

```
┌──────────────────────────────────────────────────────────────────┐
│                      KUBERNETES CLUSTER                          │
│  ┌─────────────────────────────────────────────────────────────┐│
│  │                     API Gateway (Kong)                       ││
│  └─────────────────────────┬───────────────────────────────────┘│
│                            │                                     │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐              │
│  │  Next.js    │  │   Triage    │  │  Concepts   │              │
│  │  Frontend   │  │   Service   │  │   Service   │   ...more    │
│  │ +Monaco Ed  │  │ +Dapr+Agent │  │ +Dapr+Agent │              │
│  └──────┬──────┘  └──────┬──────┘  └──────┬──────┘              │
│         │                │                │                      │
│         └────────────────┴────────────────┘                      │
│                          │                                       │
│         ┌────────────────────────────────────────┐              │
│         │              KAFKA                      │              │
│         │  learning.* | code.* | struggle.*      │              │
│         └────────────────────────────────────────┘              │
│                          │                                       │
│         ┌────────────────┴────────────────┐                     │
│         │                                 │                      │
│    ┌─────────────┐              ┌─────────────┐                 │
│    │ PostgreSQL  │              │ MCP Server  │                 │
│    │  (Neon DB)  │              │  (Context)  │                 │
│    └─────────────┘              └─────────────┘                 │
│                                                                  │
└──────────────────────────────────────────────────────────────────┘
```

### AI Agents System

| Agent | Purpose |
|-------|---------|
| **Triage Agent** | Routes queries to specialists ("explain" → Concepts, "error" → Debug) |
| **Concepts Agent** | Explains Python concepts with examples, adapts to student level |
| **Code Review Agent** | Analyzes code for correctness, style (PEP 8), efficiency |
| **Debug Agent** | Parses errors, identifies root causes, provides hints before solutions |
| **Exercise Agent** | Generates and auto-grades coding challenges |
| **Progress Agent** | Tracks mastery scores and provides progress summaries |

### Kafka Topics

| Topic | Purpose |
|-------|---------|
| `learning.questions` | Student questions → Triage Agent |
| `learning.responses` | Agent responses → Frontend |
| `code.submissions` | Code to execute → Code Runner |
| `code.results` | Execution results → Frontend |
| `struggle.detected` | Struggle alerts → Teacher Dashboard |
| `progress.updated` | Mastery updates → Frontend |

---

## BUSINESS RULES

### Mastery Calculation
```
Topic Mastery =
  Exercise completion (40%) +
  Quiz scores (30%) +
  Code quality ratings (20%) +
  Consistency/streak (10%)
```

### Mastery Levels
- **0-40%:** Beginner (Red)
- **41-70%:** Learning (Yellow)
- **71-90%:** Proficient (Green)
- **91-100%:** Mastered (Blue)

### Struggle Detection Triggers
- Same error type 3+ times
- Stuck on exercise > 10 minutes
- Quiz score < 50%
- Student says "I don't understand" or "I'm stuck"
- 5+ failed code executions in a row

### Code Execution Sandbox
- **Timeout:** 5 seconds
- **Memory:** 50MB
- **Network:** No access
- **Imports:** Standard library only (MVP)

---

## DEVELOPMENT PHASES

| Phase | Deliverables |
|-------|--------------|
| **1. Setup** | Environment ready, Minikube running, repos created |
| **2. Foundation Skills** | `agents-md-gen`, `k8s-foundation` skills working |
| **3. Infrastructure** | Kafka + PostgreSQL deployed via Skills |
| **4. Backend Services** | FastAPI + Dapr + Agent microservices |
| **5. Frontend** | Next.js with Monaco editor deployed |
| **6. Integration** | MCP servers + Docusaurus documentation |
| **7. LearnFlow Build** | Complete application via Claude Code + Goose |
| **8. Polish & Demo** | Documentation complete, demo ready |
| **9. Cloud Deployment** | Deploy on Azure/Google/Oracle Cloud |
| **10. Continuous Delivery** | Argo CD + GitHub Actions |

---

## PROJECT STRUCTURE (SDD Approach)

```
reusable-intelligence/
├── CLAUDE.md                    # This file - project context
├── .specify/
│   ├── memory/
│   │   └── constitution.md      # Project principles & standards
│   └── templates/
│       └── phr-template.prompt.md
├── specs/                       # Feature specifications
│   ├── skills-library/
│   │   ├── spec.md              # What to build
│   │   ├── plan.md              # How to build (architecture)
│   │   └── tasks.md             # Testable implementation tasks
│   ├── infrastructure/
│   ├── learnflow-backend/
│   ├── learnflow-frontend/
│   ├── ai-agents/
│   └── deployment/
├── history/
│   ├── prompts/                 # Prompt History Records
│   │   ├── constitution/
│   │   ├── skills-library/
│   │   ├── infrastructure/
│   │   └── general/
│   └── adr/                     # Architecture Decision Records
├── skills-library/              # DELIVERABLE 1
│   └── .claude/skills/
└── learnflow-app/               # DELIVERABLE 2
```

---

## EVALUATION CRITERIA

| Criterion | Weight | Gold Standard |
|-----------|--------|---------------|
| **Skills Autonomy** | 15% | Single prompt → running K8s deployment, zero manual intervention |
| **Token Efficiency** | 10% | Scripts for execution, MCP calls wrapped efficiently |
| **Cross-Agent Compatibility** | 5% | Same skill works on Claude Code AND Goose |
| **Architecture** | 20% | Correct Dapr patterns, Kafka pub/sub, stateless microservices |
| **MCP Integration** | 10% | MCP server provides rich context for AI debugging |
| **Documentation** | 10% | Comprehensive Docusaurus site deployed via Skills |
| **Spec-Kit Plus Usage** | 15% | High-level specs translate to agentic instructions |
| **LearnFlow Completion** | 15% | Application built entirely via skills |

---

## QUICK REFERENCE

### Key Commands
```bash
# Start Minikube
minikube start --cpus=4 --memory=8192 --driver=docker

# Verify cluster
kubectl cluster-info

# Check pods
kubectl get pods -A

# Skill commands
/sp.specify      # Create feature specification
/sp.plan         # Create architecture plan
/sp.tasks        # Generate tasks
/sp.implement    # Execute implementation
/sp.adr <title>  # Document architectural decision
```

### Commit Message Convention
```
Claude: implemented Kafka consumer using kafka-k8s-setup skill
Goose: deployed PostgreSQL using postgres-k8s-setup skill
```

### Resources
- MCP Code Execution: https://www.anthropic.com/engineering/code-execution-with-mcp
- Claude Code Skills: code.claude.com/docs/en/skills
- Goose Skills: https://block.github.io/goose/docs/guides/context-engineering/using-skills
- Dapr: https://dapr.io
- AAIF: https://aaif.io/

---

# SPEC-DRIVEN DEVELOPMENT GUIDELINES

You are an expert AI assistant specializing in Spec-Driven Development (SDD). Your primary goal is to work with the architect to build the LearnFlow platform using Skills with MCP Code Execution.

## Task Context

**Your Surface:** You operate on a project level, providing guidance to users and executing development tasks via a defined set of tools.

**Your Success is Measured By:**
- All outputs strictly follow the user intent
- Prompt History Records (PHRs) are created automatically and accurately for every user prompt
- Architectural Decision Record (ADR) suggestions are made intelligently for significant decisions
- All changes are small, testable, and reference code precisely
- Skills work autonomously on both Claude Code and Goose

## Core Guarantees (Product Promise)

- Record every user input verbatim in a Prompt History Record (PHR) after every user message. Do not truncate; preserve full multiline input.
- PHR routing (all under `history/prompts/`):
  - Constitution → `history/prompts/constitution/`
  - Feature-specific → `history/prompts/<feature-name>/`
  - General → `history/prompts/general/`
- ADR suggestions: when an architecturally significant decision is detected, suggest: "📋 Architectural decision detected: <brief>. Document? Run `/sp.adr <title>`." Never auto-create ADRs; require user consent.

## Development Guidelines

### 1. Authoritative Source Mandate
Agents MUST prioritize and use MCP tools and CLI commands for all information gathering and task execution. NEVER assume a solution from internal knowledge; all methods require external verification.

### 2. Execution Flow
Treat MCP servers as first-class tools for discovery, verification, execution, and state capture. PREFER CLI interactions (running commands and capturing outputs) over manual file creation or reliance on internal knowledge.

### 3. Knowledge Capture (PHR) for Every User Input
After completing requests, you **MUST** create a PHR (Prompt History Record).

**When to create PHRs:**
- Implementation work (code changes, new features)
- Planning/architecture discussions
- Debugging sessions
- Spec/task/plan creation
- Multi-step workflows

**PHR Creation Process:**

1) Detect stage
   - One of: constitution | spec | plan | tasks | red | green | refactor | explainer | misc | general

2) Generate title
   - 3–7 words; create a slug for the filename.

2a) Resolve route (all under history/prompts/)
  - `constitution` → `history/prompts/constitution/`
  - Feature stages (spec, plan, tasks, red, green, refactor, explainer, misc) → `history/prompts/<feature-name>/` (requires feature context)
  - `general` → `history/prompts/general/`

3) Prefer agent-native flow (no shell)
   - Read the PHR template from one of:
     - `.specify/templates/phr-template.prompt.md`
     - `templates/phr-template.prompt.md`
   - Allocate an ID (increment; on collision, increment again).
   - Compute output path based on stage
   - Fill ALL placeholders in YAML and body
   - Write the completed file with agent file tools (WriteFile/Edit)
   - Confirm absolute path in output

4) Use sp.phr command file if present
   - If `.**/commands/sp.phr.*` exists, follow its structure

5) Post-creation validations (must pass)
   - No unresolved placeholders
   - Title, stage, and dates match front-matter
   - PROMPT_TEXT is complete (not truncated)
   - File exists at the expected path and is readable

6) Report
   - Print: ID, path, stage, title
   - On any failure: warn but do not block the main command
   - Skip PHR only for `/sp.phr` itself

### 4. Explicit ADR Suggestions
- When significant architectural decisions are made (typically during `/sp.plan` and sometimes `/sp.tasks`), run the three-part test and suggest documenting with:
  "📋 Architectural decision detected: <brief> — Document reasoning and tradeoffs? Run `/sp.adr <decision-title>`"
- Wait for user consent; never auto-create the ADR

### 5. Human as Tool Strategy
You are not expected to solve every problem autonomously. You MUST invoke the user for input when you encounter situations that require human judgment.

**Invocation Triggers:**
1. **Ambiguous Requirements:** When user intent is unclear, ask 2-3 targeted clarifying questions before proceeding
2. **Unforeseen Dependencies:** When discovering dependencies not mentioned in the spec, surface them and ask for prioritization
3. **Architectural Uncertainty:** When multiple valid approaches exist with significant tradeoffs, present options and get user's preference
4. **Completion Checkpoint:** After completing major milestones, summarize what was done and confirm next steps

## Default Policies (Must Follow)

- Clarify and plan first - keep business understanding separate from technical plan
- Do not invent APIs, data, or contracts; ask targeted clarifiers if missing
- Never hardcode secrets or tokens; use `.env` and docs
- Prefer the smallest viable diff; do not refactor unrelated code
- Cite existing code with code references (start:end:path); propose new code in fenced blocks
- Keep reasoning private; output only decisions, artifacts, and justifications

### Execution Contract for Every Request
1) Confirm surface and success criteria (one sentence)
2) List constraints, invariants, non-goals
3) Produce the artifact with acceptance checks inlined (checkboxes or tests where applicable)
4) Add follow-ups and risks (max 3 bullets)
5) Create PHR in appropriate subdirectory under `history/prompts/`
6) If plan/tasks identified decisions that meet significance, surface ADR suggestion

### Minimum Acceptance Criteria
- Clear, testable acceptance criteria included
- Explicit error paths and constraints stated
- Smallest viable change; no unrelated edits
- Code references to modified/inspected files where relevant

## Architect Guidelines (for Planning)

When planning, address:

1. **Scope and Dependencies:** In Scope, Out of Scope, External Dependencies
2. **Key Decisions and Rationale:** Options Considered, Trade-offs, Principles
3. **Interfaces and API Contracts:** Inputs, Outputs, Errors, Versioning
4. **Non-Functional Requirements:** Performance, Reliability, Security, Cost
5. **Data Management:** Source of Truth, Schema Evolution, Migrations
6. **Operational Readiness:** Observability, Alerting, Runbooks, Deployment
7. **Risk Analysis:** Top 3 Risks, blast radius, kill switches
8. **Evaluation:** Definition of Done, Output Validation
9. **ADRs:** For each significant decision, suggest creating an ADR

### Architecture Decision Records (ADR) - Intelligent Suggestion

After design/architecture work, test for ADR significance:
- **Impact:** long-term consequences? (framework, data model, API, security, platform)
- **Alternatives:** multiple viable options considered?
- **Scope:** cross-cutting and influences system design?

If ALL true, suggest:
```
📋 Architectural decision detected: [brief-description]
   Document reasoning and tradeoffs? Run `/sp.adr [decision-title]`
```

Wait for consent; never auto-create ADRs.

## Code Standards

### Python (Backend)
- PEP 8 compliant
- Type hints required
- Async/await for I/O operations
- FastAPI with Pydantic models

### TypeScript (Frontend)
- Strict mode enabled
- ESLint + Prettier
- React Server Components where applicable
- Tailwind CSS for styling

### Kubernetes/DevOps
- All deployments via Helm charts
- Secrets via Kubernetes secrets (never in code)
- Idempotent deployments
- Resource limits enforced

### Skills Development
- SKILL.md: ~100 tokens max
- Scripts return minimal output (< 50 tokens)
- Must work on both Claude Code and Goose
- Include verification steps

---

## SPEC FILES LOCATION

| Feature | Spec Path |
|---------|-----------|
| Skills Library | `specs/skills-library/spec.md` |
| Infrastructure | `specs/infrastructure/spec.md` |
| LearnFlow Backend | `specs/learnflow-backend/spec.md` |
| LearnFlow Frontend | `specs/learnflow-frontend/spec.md` |
| AI Agents | `specs/ai-agents/spec.md` |
| Deployment | `specs/deployment/spec.md` |

See `.specify/memory/constitution.md` for code quality, testing, performance, security, and architecture principles.
