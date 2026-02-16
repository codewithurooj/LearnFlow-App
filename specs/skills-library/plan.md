# Implementation Plan: Skills Library

**Branch**: `001-skills-library` | **Date**: 2026-01-25 | **Spec**: [spec.md](./spec.md)
**Input**: Feature specification from `specs/skills-library/spec.md`

## Summary

Build a reusable Skills Library containing 7 skills (5 P0, 2 P1) that enable AI agents (Claude Code and Goose) to autonomously execute infrastructure deployments, service scaffolding, and documentation generation. Each skill follows the MCP Code Execution pattern: SKILL.md (~100 tokens) loaded into context, scripts executed outside the context window with minimal output (< 50 tokens).

## Technical Context

**Language/Version**: Bash (POSIX-compliant), Python 3.11+
**Primary Dependencies**: Helm 3.x, kubectl, Docker, Dapr CLI
**Storage**: N/A (skills operate on the cluster, not a database)
**Testing**: Verification scripts (verify.py/verify.sh) per skill
**Target Platform**: Minikube on Linux/macOS/WSL, Claude Code, Goose
**Project Type**: Single project (skill library)
**Performance Goals**: Each skill completes in < 5 minutes on Minikube (4 CPU, 8GB RAM)
**Constraints**: SKILL.md < 100 tokens, script output < 50 tokens, POSIX-compliant bash
**Scale/Scope**: 7 skills, ~35 scripts, 7 REFERENCE.md files

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

| Principle | Status | Notes |
|-----------|--------|-------|
| I. Skills-First | PASS | This IS the skills library — all development creates skills |
| II. Token Efficiency | PASS | SKILL.md ~100 tokens, scripts 0 tokens, output <50 tokens |
| III. Cloud-Native | PASS | All deployments use Helm charts on Kubernetes |
| IV. Microservices | PASS | fastapi-dapr-agent generates microservice scaffolds |
| V. Security | PASS | No hardcoded secrets; values from env vars and K8s secrets |
| VI. SDD | PASS | Spec → Plan → Tasks workflow followed |
| VII. Cross-Agent | PASS | Skills tested on both Claude Code and Goose |
| VIII. Observability | PASS | Every skill includes verify.py with ✓/✗/⚠ output |

## Project Structure

### Documentation (this feature)

```text
specs/skills-library/
├── plan.md              # This file
├── tasks.md             # Phase 2 output (/sp.tasks)
├── checklists/
│   └── requirements.md  # Spec quality checklist
```

### Source Code (repository root)

```text
skills-library/
├── .claude/
│   └── skills/
│       ├── agents-md-gen/
│       │   ├── SKILL.md
│       │   ├── REFERENCE.md
│       │   └── scripts/
│       │       ├── generate.sh
│       │       └── verify.py
│       ├── kafka-k8s-setup/
│       │   ├── SKILL.md
│       │   ├── REFERENCE.md
│       │   └── scripts/
│       │       ├── deploy.sh
│       │       ├── create-topics.sh
│       │       └── verify.py
│       ├── postgres-k8s-setup/
│       │   ├── SKILL.md
│       │   ├── REFERENCE.md
│       │   └── scripts/
│       │       ├── deploy.sh
│       │       ├── migrate.sh
│       │       └── verify.py
│       ├── fastapi-dapr-agent/
│       │   ├── SKILL.md
│       │   ├── REFERENCE.md
│       │   ├── scripts/
│       │   │   ├── scaffold.sh
│       │   │   └── verify.py
│       │   └── templates/
│       │       ├── main.py.tmpl
│       │       ├── models.py.tmpl
│       │       ├── Dockerfile.tmpl
│       │       └── requirements.txt.tmpl
│       ├── mcp-code-execution/
│       │   ├── SKILL.md
│       │   ├── REFERENCE.md
│       │   └── scripts/
│       │       ├── execute.py
│       │       └── verify.py
│       ├── nextjs-k8s-deploy/
│       │   ├── SKILL.md
│       │   ├── REFERENCE.md
│       │   └── scripts/
│       │       ├── deploy.sh
│       │       └── verify.py
│       └── docusaurus-deploy/
│           ├── SKILL.md
│           ├── REFERENCE.md
│           └── scripts/
│               ├── deploy.sh
│               └── verify.py
├── shared/
│   └── lib.sh               # Shared bash utilities (check_tool, output formatting)
├── README.md
└── docs/
    └── skill-development-guide.md
```

**Structure Decision**: Single project with `.claude/skills/<name>/` directory structure. Each skill is self-contained with SKILL.md, REFERENCE.md, and scripts/. Shared utilities in `shared/lib.sh`.

## Research Findings

### Skill Discovery Mechanism
- Claude Code scans `.claude/skills/` for SKILL.md files and matches based on trigger keywords
- Goose reads the same directory natively
- SKILL.md must contain clear trigger conditions and workflow steps

### Helm Best Practices for Skills
- Use `helm upgrade --install --atomic` for idempotent deployments
- `--atomic` flag ensures rollback on failure
- `--wait` ensures pods are ready before reporting success
- Bitnami charts preferred for Kafka and PostgreSQL (well-maintained, configurable)

### Kafka KRaft Mode
- KRaft (Kafka Raft) eliminates Zookeeper dependency
- Bitnami chart supports KRaft via `kraft.enabled=true`
- Reduces resource usage by ~500MB RAM

### Dapr Integration Patterns
- Standard annotations: `dapr.io/enabled: "true"`, `dapr.io/app-id`, `dapr.io/app-port`
- Pub/sub component bound to Kafka: `pubsub.kafka`
- State store component bound to PostgreSQL: `statestore`

### Cross-Platform Script Compatibility
- POSIX-compliant bash (no bashisms like `[[ ]]`, use `[ ]`)
- Check tool availability before use: `command -v helm >/dev/null 2>&1`
- Use standard utilities: sed, awk, grep (no GNU-specific flags)

### Output Format Standard
- Success: `✓ <brief description>` (< 50 tokens)
- Failure: `✗ <error summary>` (< 50 tokens)
- Warning: `⚠ <warning message>` (< 50 tokens)
- Exit codes: 0 = success, 1 = failure, 2 = partial success

## Data Model

### Skill Schema

| Field | Type | Description |
|-------|------|-------------|
| name | string | Skill identifier (directory name) |
| trigger_keywords | string[] | Words that activate the skill |
| description | string | One-line purpose |
| priority | P0/P1 | Implementation priority |
| scripts | Script[] | Executable files in scripts/ |
| templates | File[] | Template files for generative skills |
| dependencies | string[] | Required CLI tools |

### Script Schema

| Field | Type | Description |
|-------|------|-------------|
| name | string | Script filename |
| type | bash/python | Script language |
| inputs | Param[] | Arguments and env vars |
| outputs | string | Stdout format |
| exit_codes | Map | 0=success, 1=failure, 2=partial |

## Complexity Tracking

No constitution violations — no complexity justification needed.
