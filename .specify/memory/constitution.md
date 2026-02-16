<!--
  SYNC IMPACT REPORT
  ==================
  Version Change: 0.0.0 → 1.0.0 (MAJOR - Initial constitution creation)

  Modified Principles: N/A (new document)

  Added Sections:
  - 8 Core Principles (Skills-First, Token Efficiency, Cloud-Native, etc.)
  - Technology Stack section
  - Quality Standards section
  - Governance section

  Removed Sections: N/A

  Templates Requiring Updates:
  - plan-template.md: ✅ Compatible (Constitution Check section exists)
  - spec-template.md: ✅ Compatible (Requirements section aligns)
  - tasks-template.md: ✅ Compatible (Phase structure aligns)

  Follow-up TODOs: None
-->

# Hackathon III: Reusable Intelligence - Constitution

## Mission Statement

Build **LearnFlow**, an AI-powered Python tutoring platform, using the **Skills with MCP Code Execution** paradigm. Instead of writing code manually, we teach AI coding agents (Claude Code & Goose) to build cloud-native applications autonomously.

> **Core Principle:** *The Skills are the product, not just documentation or the LearnFlow application.*

## Core Principles

### I. Skills-First Development

All development MUST be done through Skills that AI agents can execute autonomously.

- Every component MUST have a corresponding Skill before implementation
- Skills MUST work on both Claude Code AND Goose without modification
- Skills are located in `.claude/skills/<skill-name>/SKILL.md`
- Manual coding is permitted ONLY when Skills cannot achieve the task
- The goal is single-prompt-to-deployment: one user request triggers complete autonomous execution

**Rationale:** Skills are reusable knowledge that can build many applications. Manual code only builds one thing.

### II. Token Efficiency (MCP Code Execution Pattern)

All MCP integrations MUST use the Code Execution pattern to minimize token consumption.

- SKILL.md files MUST NOT exceed ~100 tokens
- Scripts execute OUTSIDE the context window (0 tokens consumed)
- Only minimal results (< 50 tokens) enter the agent's context
- Direct MCP server loading at startup is PROHIBITED (causes 50,000+ token bloat)
- Scripts handle data filtering/processing BEFORE returning results

**Structure Required:**
```
.claude/skills/<skill-name>/
├── SKILL.md           # ~100 tokens (loaded when triggered)
├── REFERENCE.md       # 0 tokens (loaded only on-demand)
└── scripts/
    ├── deploy.sh      # 0 tokens (executed, never loaded)
    └── verify.py      # 0 tokens (returns minimal output)
```

**Rationale:** 80-98% token reduction while maintaining full capability enables longer, more productive agent sessions.

### III. Cloud-Native Architecture

All services MUST follow cloud-native principles for Kubernetes deployment.

- All services MUST be containerized with Docker
- Deployments MUST use Helm charts (no raw kubectl apply with inline YAML)
- Services MUST be stateless; use Dapr for state management
- Inter-service communication MUST use Kafka pub/sub via Dapr
- All deployments MUST be idempotent (re-runnable without side effects)
- Resource limits MUST be defined for all containers

**Rationale:** Cloud-native architecture ensures scalability, resilience, and consistent deployment across environments.

### IV. Microservices & Event-Driven Design

The LearnFlow platform MUST be built as event-driven microservices.

- Each AI agent (Triage, Concepts, Debug, etc.) MUST be a separate service
- Services communicate via Kafka topics, NOT direct HTTP calls for async operations
- Dapr sidecar MUST handle pub/sub, state, and service invocation
- Each service MUST have a single responsibility
- Services MUST be independently deployable and scalable

**Kafka Topics:**
| Topic | Purpose |
|-------|---------|
| `learning.questions` | Student queries to Triage |
| `learning.responses` | Agent responses to Frontend |
| `code.submissions` | Code execution requests |
| `code.results` | Execution results |
| `struggle.detected` | Teacher alerts |
| `progress.updated` | Mastery updates |

**Rationale:** Event-driven microservices enable loose coupling, independent scaling, and resilient systems.

### V. Security & Sandbox Constraints

All user code execution MUST be sandboxed with strict limits.

- Code execution timeout: 5 seconds MAX
- Memory limit: 50MB MAX
- Network access: PROHIBITED
- File system access: /tmp only
- Allowed imports: Python standard library only (MVP)
- Secrets MUST NEVER be hardcoded; use Kubernetes secrets or `.env`
- JWT authentication REQUIRED for all API endpoints

**Rationale:** Sandboxing prevents malicious code execution; secrets management prevents credential leaks.

### VI. Spec-Driven Development (SDD)

All features MUST follow the SDD workflow before implementation.

- **Constitution** (`.specify/memory/constitution.md`): Project principles (this file)
- **Specification** (`specs/<feature>/spec.md`): What to build with acceptance criteria
- **Plan** (`specs/<feature>/plan.md`): How to build with architecture decisions
- **Tasks** (`specs/<feature>/tasks.md`): Testable implementation tasks
- PHRs (Prompt History Records) MUST be created for every significant interaction
- ADRs (Architecture Decision Records) MUST be proposed for significant decisions

**Workflow:** Constitution → Spec → Plan → Tasks → Implementation

**Rationale:** SDD ensures clarity, traceability, and AI agents have complete context for autonomous work.

### VII. Cross-Agent Compatibility

All Skills MUST work identically on Claude Code and Goose.

- Use `.claude/skills/` directory (Goose reads this natively)
- No agent-specific syntax or features in SKILL.md
- Scripts MUST use standard bash/Python (no agent-specific tooling)
- Test every Skill on BOTH agents before marking complete
- Commit messages MUST indicate which agent performed the work

**Commit Convention:**
```
Claude: implemented Kafka consumer using kafka-k8s-setup skill
Goose: deployed PostgreSQL using postgres-k8s-setup skill
```

**Rationale:** Cross-agent compatibility proves Skills are truly portable and reusable.

### VIII. Observability & Verification

All deployments MUST include verification and be observable.

- Every Skill MUST include a `verify.py` or equivalent verification script
- Verification scripts MUST return clear pass/fail status with minimal output
- All services MUST emit structured logs (JSON format)
- Health check endpoints REQUIRED for all services (`/health`)
- Script exit codes: 0 = success, 1 = failure, 2 = partial success

**Output Format:**
```
✓ <success message>
✗ <error message>
⚠ <warning message>
```

**Rationale:** Observability enables debugging; verification ensures deployments succeed before proceeding.

## Technology Stack

| Layer | Technology | Mandatory |
|-------|------------|-----------|
| AI Coding Agents | Claude Code, Goose | YES |
| Frontend | Next.js 14 + Monaco Editor | YES |
| Backend | FastAPI + OpenAI SDK | YES |
| Authentication | Better Auth | YES |
| Service Mesh | Dapr | YES |
| Messaging | Apache Kafka | YES |
| Database | Neon PostgreSQL | YES |
| API Gateway | Kong | YES |
| Orchestration | Kubernetes (Minikube local) | YES |
| CI/CD | GitHub Actions + Argo CD | YES |
| Documentation | Docusaurus | YES |

**Deviation Policy:** Technology stack changes require ADR approval and constitution amendment.

## Quality Standards

### Python (Backend)
- PEP 8 compliance REQUIRED
- Type hints REQUIRED for all functions
- Async/await for all I/O operations
- Pydantic models for all API contracts

### TypeScript (Frontend)
- Strict mode ENABLED
- ESLint + Prettier REQUIRED
- React Server Components where applicable
- Tailwind CSS for styling

### Skills Development
- SKILL.md: ~100 tokens MAX
- Scripts return < 50 tokens output
- Verification step REQUIRED
- Works on Claude Code AND Goose

### Kubernetes/DevOps
- Helm charts for all deployments
- Secrets via K8s secrets (never in code)
- Resource limits defined
- Idempotent deployments

## Deliverables

### Repository 1: `skills-library/`
| Skill | Purpose | Priority |
|-------|---------|----------|
| `agents-md-gen` | Generate AGENTS.md files | P0 |
| `kafka-k8s-setup` | Deploy Kafka on Kubernetes | P0 |
| `postgres-k8s-setup` | Deploy PostgreSQL on Kubernetes | P0 |
| `fastapi-dapr-agent` | FastAPI + Dapr service templates | P0 |
| `mcp-code-execution` | MCP with code execution pattern | P0 |
| `nextjs-k8s-deploy` | Deploy Next.js applications | P1 |
| `docusaurus-deploy` | Deploy documentation sites | P1 |

### Repository 2: `learnflow-app/`
Complete AI tutoring platform built entirely using Skills via Claude Code and Goose.

## Governance

### Amendment Process
1. Propose change via `/sp.adr <decision-title>`
2. Document rationale and tradeoffs
3. Get user approval
4. Update constitution with version bump
5. Propagate changes to dependent templates

### Version Policy
- **MAJOR:** Principle removal/redefinition, breaking governance changes
- **MINOR:** New principle added, section expansion
- **PATCH:** Clarifications, typo fixes, non-semantic changes

### Compliance
- All PRs MUST verify constitution compliance
- Skills MUST be tested on both Claude Code and Goose
- Complexity additions MUST be justified in Complexity Tracking section of plan.md
- Constitution supersedes all other guidance documents

### Runtime Guidance
- See `CLAUDE.md` for complete project context and development guidance
- See `specs/<feature>/` for feature-specific specifications
- See `history/adr/` for architectural decision records

**Version**: 1.0.0 | **Ratified**: 2025-01-24 | **Last Amended**: 2025-01-24
