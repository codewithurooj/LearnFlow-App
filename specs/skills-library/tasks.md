# Tasks: Skills Library

**Input**: Design documents from `specs/skills-library/`
**Prerequisites**: plan.md (required), spec.md (required for user stories)

**Tests**: Not explicitly requested in spec. Test tasks omitted.

**Organization**: Tasks grouped by user story (skill) for independent implementation.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US4, US5)
- All paths relative to `skills-library/`

---

## Phase 1: Setup (Repository Infrastructure)

**Purpose**: Initialize the skills library repository structure

- [ ] T001 Create repository root with README.md describing the skills library purpose and usage
- [ ] T002 Create `.claude/skills/` directory structure for all 7 skills
- [ ] T003 [P] Create `shared/lib.sh` with common bash utilities (check_tool, output formatting ✓/✗/⚠, error handling)
- [ ] T004 [P] Create `docs/skill-development-guide.md` with instructions for creating new skills
- [ ] T005 [P] Create `.gitignore` for the repository
- [ ] T006 [P] Create `AGENTS.md` for the skills-library repository itself

---

## Phase 2: Foundational (Shared Utilities)

**Purpose**: Core infrastructure that all skills depend on

**CRITICAL**: No skill implementation can begin until shared utilities are ready

- [ ] T007 Implement `shared/lib.sh` — functions: `check_tool()` (verify CLI tools exist), `ok()` (✓ output), `err()` (✗ output), `warn()` (⚠ output), `require_env()` (check env vars)
- [ ] T008 Create `shared/verify_base.py` — base verification class with health check patterns, kubectl helpers, and result formatting

**Checkpoint**: Shared utilities ready — skill implementation can begin

---

## Phase 3: User Story 4 — agents-md-gen Skill (Priority: P0)

**Goal**: Generate AGENTS.md files for any repository

**Independent Test**: Run skill against a known repository and verify AGENTS.md is generated correctly

- [ ] T009 [P] [US4] Create `agents-md-gen/SKILL.md` (~100 tokens) with trigger keywords and workflow steps in `.claude/skills/agents-md-gen/SKILL.md`
- [ ] T010 [P] [US4] Create `agents-md-gen/REFERENCE.md` with detailed documentation in `.claude/skills/agents-md-gen/REFERENCE.md`
- [ ] T011 [US4] Create `agents-md-gen/scripts/generate.sh` — scans repo structure, identifies key files, generates AGENTS.md content
- [ ] T012 [US4] Create `agents-md-gen/scripts/verify.py` — validates generated AGENTS.md has required sections (overview, structure, commands)
- [ ] T013 [US4] Test agents-md-gen skill on skills-library repository itself

---

## Phase 4: User Story 5 — kafka-k8s-setup Skill (Priority: P0)

**Goal**: Deploy Kafka on Kubernetes with all LearnFlow topics

**Independent Test**: Deploy on Minikube and verify pods + topics exist

- [ ] T014 [P] [US5] Create `kafka-k8s-setup/SKILL.md` (~100 tokens) in `.claude/skills/kafka-k8s-setup/SKILL.md`
- [ ] T015 [P] [US5] Create `kafka-k8s-setup/REFERENCE.md` with Helm values documentation in `.claude/skills/kafka-k8s-setup/REFERENCE.md`
- [ ] T016 [US5] Create `kafka-k8s-setup/scripts/deploy.sh` — creates namespace, runs `helm upgrade --install --atomic` with Bitnami Kafka (KRaft mode)
- [ ] T017 [US5] Create `kafka-k8s-setup/scripts/create-topics.sh` — creates all 6 LearnFlow Kafka topics with correct partition counts
- [ ] T018 [US5] Create `kafka-k8s-setup/scripts/verify.py` — checks pods running, topics exist, broker accessible
- [ ] T019 [US5] Test kafka-k8s-setup skill on Minikube — verify idempotent deployment

---

## Phase 5: User Story 6 — postgres-k8s-setup Skill (Priority: P0)

**Goal**: Deploy PostgreSQL with schema migrations

**Independent Test**: Deploy on Minikube and verify tables + secret exist

- [ ] T020 [P] [US6] Create `postgres-k8s-setup/SKILL.md` (~100 tokens) in `.claude/skills/postgres-k8s-setup/SKILL.md`
- [ ] T021 [P] [US6] Create `postgres-k8s-setup/REFERENCE.md` in `.claude/skills/postgres-k8s-setup/REFERENCE.md`
- [ ] T022 [US6] Create `postgres-k8s-setup/scripts/deploy.sh` — creates namespace, deploys via Bitnami Helm, stores connection string as K8s secret
- [ ] T023 [US6] Create `postgres-k8s-setup/scripts/migrate.sh` — runs SQL migrations (CREATE TABLE IF NOT EXISTS for users, progress, code_submissions, chat_history)
- [ ] T024 [US6] Create migration SQL files: `migrations/001_users.sql`, `002_progress.sql`, `003_code_submissions.sql`, `004_chat_history.sql`
- [ ] T025 [US6] Create `postgres-k8s-setup/scripts/verify.py` — checks pod running, tables exist, secret accessible
- [ ] T026 [US6] Test postgres-k8s-setup skill on Minikube — verify idempotent deployment and migration

---

## Phase 6: User Story 7 — fastapi-dapr-agent Skill (Priority: P0)

**Goal**: Scaffold a complete FastAPI + Dapr microservice

**Independent Test**: Generate a service, start it, verify health check passes

- [ ] T027 [P] [US7] Create `fastapi-dapr-agent/SKILL.md` (~100 tokens) in `.claude/skills/fastapi-dapr-agent/SKILL.md`
- [ ] T028 [P] [US7] Create `fastapi-dapr-agent/REFERENCE.md` in `.claude/skills/fastapi-dapr-agent/REFERENCE.md`
- [ ] T029 [P] [US7] Create `fastapi-dapr-agent/templates/main.py.tmpl` — FastAPI app with health endpoint, Dapr integration, OpenAI setup
- [ ] T030 [P] [US7] Create `fastapi-dapr-agent/templates/models.py.tmpl` — Base Pydantic models (HealthResponse, ChatRequest, ChatResponse)
- [ ] T031 [P] [US7] Create `fastapi-dapr-agent/templates/Dockerfile.tmpl` — Multi-stage build (builder + runtime)
- [ ] T032 [P] [US7] Create `fastapi-dapr-agent/templates/requirements.txt.tmpl` — FastAPI, uvicorn, openai, dapr-ext-fastapi, pydantic
- [ ] T033 [US7] Create `fastapi-dapr-agent/scripts/scaffold.sh` — reads service name and port from args, copies and substitutes templates
- [ ] T034 [US7] Create `fastapi-dapr-agent/scripts/verify.py` — checks generated files exist, service starts, health check passes
- [ ] T035 [US7] Test fastapi-dapr-agent skill — generate a test service and verify it runs

---

## Phase 7: User Story 8 — mcp-code-execution Skill (Priority: P0)

**Goal**: Demonstrate MCP Code Execution pattern

**Independent Test**: Run skill and verify MCP interaction with < 50 token output

- [ ] T036 [P] [US8] Create `mcp-code-execution/SKILL.md` (~100 tokens) in `.claude/skills/mcp-code-execution/SKILL.md`
- [ ] T037 [P] [US8] Create `mcp-code-execution/REFERENCE.md` in `.claude/skills/mcp-code-execution/REFERENCE.md`
- [ ] T038 [US8] Create `mcp-code-execution/scripts/execute.py` — demonstrates MCP server interaction outside context window, filters results to < 50 tokens
- [ ] T039 [US8] Create `mcp-code-execution/scripts/verify.py` — validates output token count and format
- [ ] T040 [US8] Test mcp-code-execution skill — verify pattern works end-to-end

---

## Phase 8: User Story 9 — nextjs-k8s-deploy Skill (Priority: P1)

**Goal**: Deploy Next.js applications to Kubernetes

**Independent Test**: Deploy a Next.js app and verify pod runs

- [ ] T041 [P] [US9] Create `nextjs-k8s-deploy/SKILL.md` (~100 tokens) in `.claude/skills/nextjs-k8s-deploy/SKILL.md`
- [ ] T042 [P] [US9] Create `nextjs-k8s-deploy/REFERENCE.md` in `.claude/skills/nextjs-k8s-deploy/REFERENCE.md`
- [ ] T043 [US9] Create `nextjs-k8s-deploy/scripts/deploy.sh` — builds Docker image, creates K8s deployment and service via Helm
- [ ] T044 [US9] Create `nextjs-k8s-deploy/scripts/verify.py` — checks pod running, service accessible, health endpoint responding
- [ ] T045 [US9] Test nextjs-k8s-deploy skill on Minikube

---

## Phase 9: User Story 10 — docusaurus-deploy Skill (Priority: P1)

**Goal**: Deploy Docusaurus documentation sites to Kubernetes

**Independent Test**: Deploy a Docusaurus site and verify it's accessible

- [ ] T046 [P] [US10] Create `docusaurus-deploy/SKILL.md` (~100 tokens) in `.claude/skills/docusaurus-deploy/SKILL.md`
- [ ] T047 [P] [US10] Create `docusaurus-deploy/REFERENCE.md` in `.claude/skills/docusaurus-deploy/REFERENCE.md`
- [ ] T048 [US10] Create `docusaurus-deploy/scripts/deploy.sh` — builds static site, containerizes with nginx, deploys to K8s
- [ ] T049 [US10] Create `docusaurus-deploy/scripts/verify.py` — checks pod running, site accessible, index.html served
- [ ] T050 [US10] Test docusaurus-deploy skill on Minikube

---

## Phase 10: Polish & Cross-Cutting Concerns

**Purpose**: Cross-agent testing, documentation, and validation

- [ ] T051 [P] Test all P0 skills on Claude Code — verify each executes from single prompt
- [ ] T052 [P] Test all P0 skills on Goose — verify identical behavior
- [ ] T053 Validate all SKILL.md files are under 100 tokens
- [ ] T054 Validate all script outputs are under 50 tokens
- [ ] T055 [P] Update README.md with complete skill catalog and usage examples
- [ ] T056 [P] Update `docs/skill-development-guide.md` with lessons learned
- [ ] T057 Run full verification suite across all 7 skills — document results

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies — start immediately
- **Foundational (Phase 2)**: Depends on Phase 1 — BLOCKS all skills
- **Skills (Phases 3-9)**: All depend on Phase 2; can proceed in parallel
- **Polish (Phase 10)**: Depends on all skills being complete

### Parallel Opportunities

- Phases 3-9 (all skills) can run in parallel after Phase 2
- Within each skill: SKILL.md and REFERENCE.md can be written in parallel
- Templates in fastapi-dapr-agent (T029-T032) can all run in parallel

### MVP Scope

Phases 1-2 + Phase 3 (agents-md-gen) = 13 tasks for minimal viable skill

---

## Implementation Strategy

### MVP First (agents-md-gen Only)

1. Complete Phase 1: Setup
2. Complete Phase 2: Foundational
3. Complete Phase 3: agents-md-gen
4. **STOP and VALIDATE**: Test on both Claude Code and Goose
5. Continue with remaining P0 skills

### Full P0 Delivery

1. Setup + Foundational → Foundation ready
2. All P0 skills in parallel (Phases 3-7)
3. Polish (Phase 10 for P0)
4. P1 skills (Phases 8-9)
5. Final polish

## Notes

- [P] tasks = different files, no dependencies
- [Story] label maps to spec user stories
- Each skill is independently completable and testable
- Commit after each task or logical group
