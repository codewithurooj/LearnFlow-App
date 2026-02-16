# Feature Specification: Skills Library

**Feature Branch**: `001-skills-library`
**Created**: 2026-01-24
**Status**: Draft
**Input**: User description: "Create specification for the skills-library repository. Skills teach AI agents (Claude Code & Goose) to build applications autonomously. Each skill follows SKILL.md (~100 tokens) + REFERENCE.md + scripts/. Must work on both Claude Code AND Goose without modification."

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Skill Discovery and Loading (Priority: P0)

An AI agent receives a user prompt (e.g., "deploy Kafka on Kubernetes") and discovers the appropriate skill from the `.claude/skills/` directory. The agent loads only the SKILL.md file (~100 tokens) into context and follows its instructions.

**Why this priority**: Skill discovery is the foundational mechanism. Without it, no skill can be executed autonomously.

**Independent Test**: Can be fully tested by issuing a prompt that matches a skill trigger and verifying the agent loads only the SKILL.md file and follows its workflow.

**Acceptance Scenarios**:

1. **Given** a user prompt containing "deploy Kafka", **When** the agent scans `.claude/skills/`, **Then** the `kafka-k8s-setup` skill is selected and SKILL.md is loaded.
2. **Given** an ambiguous prompt, **When** multiple skills could match, **Then** the agent selects the most relevant skill based on keyword matching.
3. **Given** a prompt with no matching skill, **When** the agent scans skills, **Then** it falls back to general-purpose behavior and informs the user.

---

### User Story 2 - Autonomous Script Execution (Priority: P0)

An AI agent loads a skill's SKILL.md, which instructs it to execute scripts in the `scripts/` directory. The agent runs the scripts autonomously, captures minimal output (< 50 tokens), and reports success or failure without loading script contents into context.

**Why this priority**: Script execution is the core mechanism for token-efficient skill operation. Scripts do the heavy lifting outside the context window.

**Independent Test**: Can be tested by triggering a skill and verifying scripts execute, return minimal output, and the agent reports the result correctly.

**Acceptance Scenarios**:

1. **Given** a skill with `scripts/deploy.sh`, **When** the agent executes it, **Then** the script runs outside the context window and returns output < 50 tokens.
2. **Given** a script that succeeds, **When** output is captured, **Then** the agent receives a message starting with `✓` and a brief success description.
3. **Given** a script that fails, **When** output is captured, **Then** the agent receives a message starting with `✗` with the error summary and exit code 1.

---

### User Story 3 - Cross-Agent Compatibility (Priority: P0)

The same skill works identically when executed by Claude Code and by Goose. No agent-specific syntax, features, or tooling is used in SKILL.md or scripts.

**Why this priority**: Cross-agent compatibility proves skills are truly portable and reusable, which is a core evaluation criterion.

**Independent Test**: Can be tested by executing the same skill on both Claude Code and Goose and verifying identical behavior and output.

**Acceptance Scenarios**:

1. **Given** a skill in `.claude/skills/<name>/`, **When** loaded by Claude Code, **Then** it executes successfully.
2. **Given** the same skill, **When** loaded by Goose, **Then** it executes with identical behavior and output.
3. **Given** scripts use POSIX-compliant bash, **When** run on any Unix-like system, **Then** they complete without agent-specific dependencies.

---

### User Story 4 - agents-md-gen Skill (Priority: P0)

An AI agent generates an AGENTS.md file for a repository by scanning the codebase structure, identifying key components, and producing a comprehensive guide for AI agents working with that codebase.

**Why this priority**: AGENTS.md generation is a foundational skill that helps other agents understand any repository.

**Independent Test**: Can be tested by running the skill against a known repository and verifying the generated AGENTS.md contains accurate structure, entry points, and conventions.

**Acceptance Scenarios**:

1. **Given** a repository path, **When** the agents-md-gen skill executes, **Then** an AGENTS.md file is generated at the repository root.
2. **Given** the generated file, **When** reviewed, **Then** it contains: project overview, directory structure, key entry points, development conventions, and common commands.

---

### User Story 5 - kafka-k8s-setup Skill (Priority: P0)

An AI agent deploys Apache Kafka on Kubernetes using a single skill invocation. The skill uses Bitnami Helm charts with KRaft mode (no Zookeeper), creates the kafka namespace, deploys the broker, and creates all required topics.

**Why this priority**: Kafka is the messaging backbone for LearnFlow's event-driven architecture.

**Independent Test**: Can be tested by running the skill on Minikube and verifying Kafka pods are running and all 6 topics exist.

**Acceptance Scenarios**:

1. **Given** a running Minikube cluster, **When** the kafka-k8s-setup skill executes, **Then** Kafka is deployed in the `kafka` namespace using Bitnami Helm chart with KRaft mode.
2. **Given** Kafka is deployed, **When** topics are created, **Then** all 6 topics exist: `learning.questions`, `learning.responses`, `code.submissions`, `code.results`, `struggle.detected`, `progress.updated`.
3. **Given** the skill is run again (idempotent), **When** Kafka already exists, **Then** the deployment is updated without errors or data loss.

---

### User Story 6 - postgres-k8s-setup Skill (Priority: P0)

An AI agent deploys PostgreSQL on Kubernetes and runs schema migrations. The skill creates the database, applies migrations for all required tables, and stores the connection string as a Kubernetes secret.

**Why this priority**: PostgreSQL stores all LearnFlow user data, progress, and submissions.

**Independent Test**: Can be tested by deploying and verifying tables exist with correct schemas and the connection secret is accessible.

**Acceptance Scenarios**:

1. **Given** a running Minikube cluster, **When** the postgres-k8s-setup skill executes, **Then** PostgreSQL is deployed using Bitnami Helm chart.
2. **Given** PostgreSQL is running, **When** migrations run, **Then** tables `users`, `progress`, `code_submissions`, and `chat_history` are created with correct schemas.
3. **Given** the connection string, **When** stored as a K8s secret, **Then** it is accessible by other services in the cluster.

---

### User Story 7 - fastapi-dapr-agent Skill (Priority: P0)

An AI agent scaffolds a complete FastAPI microservice with Dapr sidecar configuration. The generated service includes health endpoints, Dapr pub/sub integration, OpenAI SDK setup, Pydantic models, and a Dockerfile.

**Why this priority**: Every LearnFlow backend service follows this pattern, making it the most reused skill.

**Independent Test**: Can be tested by generating a service and verifying it starts, responds to health checks, and has correct Dapr annotations.

**Acceptance Scenarios**:

1. **Given** a service name and port, **When** the fastapi-dapr-agent skill executes, **Then** a complete FastAPI project is scaffolded with the correct structure.
2. **Given** the generated service, **When** started with `uvicorn`, **Then** it responds to `/health` with a 200 status.
3. **Given** the generated Dockerfile, **When** built and run, **Then** the container starts and is ready for Dapr sidecar injection.

---

### User Story 8 - mcp-code-execution Skill (Priority: P0)

An AI agent demonstrates the MCP Code Execution pattern by wrapping an MCP server interaction in a script that executes outside the context window, processes results, and returns minimal output.

**Why this priority**: This skill demonstrates the core paradigm of the hackathon — Skills with MCP Code Execution.

**Independent Test**: Can be tested by running the skill and verifying the MCP interaction completes with output < 50 tokens.

**Acceptance Scenarios**:

1. **Given** an MCP server endpoint, **When** the mcp-code-execution skill runs, **Then** the script interacts with the server outside the context window.
2. **Given** the MCP response, **When** processed by the script, **Then** only filtered/summarized results (< 50 tokens) are returned to the agent.

---

### User Story 9 - nextjs-k8s-deploy Skill (Priority: P1)

An AI agent deploys a Next.js application to Kubernetes using a Helm chart. The skill builds the Docker image, pushes to the cluster registry, and creates the deployment with proper resource limits.

**Why this priority**: Frontend deployment is needed for the complete LearnFlow platform but depends on backend being ready.

**Independent Test**: Can be tested by deploying a Next.js app and verifying the pod runs and the service is accessible.

**Acceptance Scenarios**:

1. **Given** a Next.js project with a Dockerfile, **When** the nextjs-k8s-deploy skill executes, **Then** the image is built and a Kubernetes deployment is created.
2. **Given** the deployment, **When** the pod is running, **Then** the Next.js app is accessible via the configured service port.

---

### User Story 10 - docusaurus-deploy Skill (Priority: P1)

An AI agent deploys a Docusaurus documentation site to Kubernetes. The skill builds the static site, containerizes it with nginx, and deploys it.

**Why this priority**: Documentation is important for the hackathon evaluation but depends on the application being built first.

**Independent Test**: Can be tested by deploying a Docusaurus site and verifying it is accessible via the service URL.

**Acceptance Scenarios**:

1. **Given** a Docusaurus project, **When** the docusaurus-deploy skill executes, **Then** the site is built, containerized, and deployed to Kubernetes.
2. **Given** the deployment, **When** accessed via browser, **Then** the documentation site renders correctly.

---

### Edge Cases

- What happens when a script times out? The skill reports a `✗ Timeout after Xs` message and exits with code 1.
- What happens when Helm chart download fails (network issue)? The script retries once, then reports the failure with a clear error message.
- What happens when two skills modify the same Kubernetes namespace? Skills use `upgrade --install --atomic` to ensure atomic operations; conflicts are reported as warnings.
- What happens when Minikube runs out of resources? The verification script detects resource exhaustion and reports `⚠ Insufficient resources` with current usage.
- What happens when a skill's REFERENCE.md is missing? The skill operates with SKILL.md only; REFERENCE.md is optional supplementary documentation.
- What happens when script permissions are wrong? Scripts include a check for executability and report the issue clearly.
- What happens when the same skill runs concurrently? Helm's atomic flag prevents concurrent modification; the second invocation waits or fails gracefully.

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: Each skill MUST follow the directory structure: `.claude/skills/<skill-name>/SKILL.md` + optional `REFERENCE.md` + `scripts/`.
- **FR-002**: SKILL.md files MUST NOT exceed ~100 tokens.
- **FR-003**: All scripts MUST return output of < 50 tokens to the agent context.
- **FR-004**: Scripts MUST use exit codes: 0 = success, 1 = failure, 2 = partial success.
- **FR-005**: Output MUST use the format: `✓` (success), `✗` (error), `⚠` (warning).
- **FR-006**: All scripts MUST be POSIX-compliant bash (no bash-specific extensions that break portability).
- **FR-007**: Skills MUST work on both Claude Code and Goose without modification.
- **FR-008**: Kubernetes deployments MUST use `helm upgrade --install --atomic` for idempotency.
- **FR-009**: Every skill MUST include a verification step (verify script or verification commands in SKILL.md).
- **FR-010**: Skills MUST NOT hardcode secrets, cluster names, or environment-specific values.
- **FR-011**: The kafka-k8s-setup skill MUST create all 6 LearnFlow Kafka topics.
- **FR-012**: The postgres-k8s-setup skill MUST run schema migrations for all 4 tables.
- **FR-013**: The fastapi-dapr-agent skill MUST generate a complete, runnable FastAPI service with Dapr annotations.
- **FR-014**: The mcp-code-execution skill MUST demonstrate the code execution pattern with <50 token output.
- **FR-015**: The nextjs-k8s-deploy skill MUST support multi-stage Docker builds.
- **FR-016**: The docusaurus-deploy skill MUST produce a static site served by nginx.

### Key Entities

- **Skill**: A reusable unit of AI agent knowledge consisting of SKILL.md, optional REFERENCE.md, and scripts. Has a name, trigger keywords, and target agent compatibility.
- **SKILL.md**: The lightweight instruction file (~100 tokens) loaded into agent context when triggered. Contains trigger conditions, workflow steps, and script references.
- **REFERENCE.md**: Optional detailed documentation loaded on-demand. Contains deep technical details, troubleshooting, and examples.
- **Script**: An executable file (bash/python) that runs outside the context window. Has inputs (arguments/env vars), outputs (stdout < 50 tokens), and an exit code.
- **Template**: A file template used by generative skills (e.g., fastapi-dapr-agent) to scaffold new projects.

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: All 5 P0 skills execute successfully from a single user prompt with zero manual intervention.
- **SC-002**: SKILL.md files are each under 100 tokens as measured by token counter.
- **SC-003**: Script output is under 50 tokens for all success and failure cases.
- **SC-004**: All skills pass verification on both Claude Code and Goose.
- **SC-005**: Kafka deployment completes in under 3 minutes on Minikube (4 CPU, 8GB RAM).
- **SC-006**: PostgreSQL deployment with migrations completes in under 2 minutes.
- **SC-007**: FastAPI service scaffold is fully runnable (starts, health check passes) without manual edits.

## Assumptions

- Minikube is running with 4 CPU and 8GB RAM allocated.
- Helm 3.x is installed and available in PATH.
- kubectl is configured to communicate with the Minikube cluster.
- Python 3.11+ is available for Python-based scripts.
- Docker is available for image building (Minikube's built-in registry or eval $(minikube docker-env)).
- Skills are stored in the `.claude/skills/` directory which both Claude Code and Goose can read natively.
- Network access is available for Helm chart downloads during initial deployment.
