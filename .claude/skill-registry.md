# Skill & Subagent Registry

This registry maps task patterns to the appropriate skills and subagents for automatic invocation.

## Quick Reference

```
Task mentions "FastAPI" → Use fastapi-sqlmodel skill
Task mentions "Next.js" → Use nextjs-betterauth skill
Task mentions "Helm chart" → Use helm-chart-builder skill
Task mentions "Kafka consumer" → Use microservice-scaffolder agent
Task mentions "Dapr" → Use dapr-generator agent
Task mentions "database migration" → Use db-migrator agent
Task mentions "AI agent" → Use agent-orchestrator agent
Task mentions "MCP server" → Use mcp-server-creator skill
Task mentions "create skill" → Use skill-creator skill
Task mentions "production skill" → Use skill-creator-pro skill
Task mentions "validate skill" → Use skill-validator skill
```

---

## Skills (`.claude/skills/`)

### 1. fastapi-sqlmodel
**Path:** `.claude/skills/fastapi-sqlmodel.md`
**Triggers:** `FastAPI`, `backend`, `routes`, `endpoints`, `API`, `SQLModel`, `CRUD`
**Generates:**
- `backend/app/models/{resource}.py`
- `backend/app/routes/{resource}s.py`
- `backend/app/middleware/auth.py`
- `backend/tests/test_{resource}s.py`

### 2. nextjs-betterauth
**Path:** `.claude/skills/nextjs-betterauth.md`
**Triggers:** `Next.js`, `frontend`, `React`, `components`, `pages`, `dashboard`, `UI`
**Generates:**
- `frontend/app/{page}/page.tsx`
- `frontend/components/{component}.tsx`
- `frontend/lib/api/{resource}.ts`
- `frontend/lib/auth.ts`

### 3. helm-chart-builder
**Path:** `.claude/skills/helm-chart-builder.md`
**Triggers:** `Helm`, `chart`, `Kubernetes`, `K8s`, `deployment`, `values.yaml`
**Generates:**
- `charts/{name}/Chart.yaml`
- `charts/{name}/values.yaml`
- `charts/{name}/templates/*.yaml`

### 4. dockerfile-generator
**Path:** `.claude/skills/dockerfile-generator.md`
**Triggers:** `Dockerfile`, `container`, `image`, `Docker`, `containerize`
**Generates:**
- `{service}/Dockerfile`
- `{service}/.dockerignore`

### 5. monorepo-structure
**Path:** `.claude/skills/monorepo-structure.md`
**Triggers:** `project structure`, `monorepo`, `initialize`, `scaffold`
**Generates:**
- Project directory structure
- Base configuration files

### 6. mcp-server-creator
**Path:** `.claude/skills/mcp-server-creator/SKILL.md`
**Triggers:** `MCP`, `Model Context Protocol`, `tool server`, `context server`
**Generates:**
- MCP server implementation
- Tool definitions
- Transport configuration

### 7. skill-creator
**Path:** `.claude/skills/skill-creator/SKILL.md`
**Triggers:** `create skill`, `new skill`, `build skill`, `skill development`
**Purpose:** Guide for creating effective skills that extend Claude's capabilities with specialized knowledge, workflows, or tool integrations
**Generates:**
- SKILL.md with proper frontmatter
- `scripts/` directory for executable code
- `references/` directory for documentation
- `assets/` directory for templates/resources
- Packaged `.skill` distribution file

### 8. skill-creator-pro
**Path:** `.claude/skills/skill-creator-pro/SKILL.md`
**Triggers:** `production skill`, `pro skill`, `domain skill`, `advanced skill creation`, `improve skill`
**Purpose:** Creates production-grade, reusable skills with automatic domain discovery from codebase, conversation, and authentic sources
**Generates:**
- Production-quality SKILL.md (<500 lines)
- Domain expertise in `references/` (structured per domain needs)
- Type-aware skills (Builder, Guide, Automation, Analyzer, Validator)
- Scripts for deterministic procedures
- Assets for templates/boilerplate

### 9. skill-validator
**Path:** `.claude/skills/skill-validator/SKILL.md`
**Triggers:** `validate skill`, `skill review`, `skill audit`, `skill quality`, `check skill`
**Purpose:** Validates skills against production-level criteria with 9-category scoring
**Generates:**
- Validation report with scores (0-100)
- Category-by-category assessment (Structure, Content, User Interaction, Documentation, Domain Standards, Technical Robustness, Maintainability, Zero-Shot Implementation, Reusability)
- Improvement recommendations
- Quality rating (Production/Good/Adequate/Developing/Incomplete)

---

## Subagents (`.claude/agents/`)

### 1. agent-orchestrator
**Path:** `.claude/agents/agent-orchestrator/agent.md`
**Triggers:** `AI agent`, `orchestrator`, `OpenAI SDK`, `tool calling`, `agent workflow`
**Purpose:** Design multi-agent systems with handoffs and tool calling
**Output:** Agent architecture, tool definitions, workflow diagrams

### 2. microservice-scaffolder
**Path:** `.claude/agents/microservice-scaffolder/agent.md`
**Triggers:** `Kafka consumer`, `microservice`, `event-driven`, `pub/sub service`
**Purpose:** Generate complete Kafka consumer microservices
**Output:** Full service with Dockerfile, Helm chart, tests

### 3. dapr-generator
**Path:** `.claude/agents/dapr-generator/agent.md`
**Triggers:** `Dapr`, `state store`, `pubsub component`, `secrets component`, `binding`
**Purpose:** Generate Dapr component configurations
**Output:** YAML component files for Dapr sidecar

### 4. db-migrator
**Path:** `.claude/agents/db-migrator/agent.md`
**Triggers:** `database`, `migration`, `schema`, `ALTER TABLE`, `new column`, `PostgreSQL`
**Purpose:** Generate safe database migrations
**Output:** Migration scripts, rollback scripts, SQLModel updates

### 5. helm-updater
**Path:** `.claude/agents/helm-updater/agent.md`
**Triggers:** `helm upgrade`, `add env var`, `update values`, `chart update`
**Purpose:** Incrementally update existing Helm charts
**Output:** Updated values.yaml, deployment.yaml changes

### 6. testing-agent
**Path:** `.claude/agents/testing-agent/README.md`
**Triggers:** `E2E test`, `integration test`, `test suite`, `automated testing`
**Purpose:** Design and execute comprehensive test suites
**Output:** Test specifications, test scripts

### 7. stateless-api-designer
**Path:** `.claude/agents/stateless-api-designer/agent.md`
**Triggers:** `API design`, `REST contract`, `OpenAPI`, `API specification`
**Purpose:** Design RESTful API contracts
**Output:** OpenAPI specs, endpoint documentation

### 8. nl-test-generator
**Path:** `.claude/agents/nl-test-generator/agent.md`
**Triggers:** `Given-When-Then`, `BDD`, `test scenarios`, `acceptance criteria`
**Purpose:** Convert natural language to test specifications
**Output:** Test specs in Given-When-Then format

### 9. mcp-builder
**Path:** `.claude/agents/mcp-builder/agent.md`
**Triggers:** `MCP tool`, `tool interface`, `context protocol design`
**Purpose:** Design MCP tool interfaces
**Output:** Tool specifications, parameter schemas

### 10. ui-ux-agent
**Path:** `.claude/agents/ui-ux-agent/agent.md`
**Triggers:** `UI design`, `UX`, `user interface`, `component design`
**Purpose:** UI/UX design guidance
**Output:** Design recommendations, component patterns

---

## LearnFlow Project Mapping

| LearnFlow Component | Primary Skill/Agent | Secondary |
|--------------------|---------------------|-----------|
| Chat API | fastapi-sqlmodel | stateless-api-designer |
| AI Tutoring Agents | agent-orchestrator | mcp-builder |
| Student Dashboard | nextjs-betterauth | ui-ux-agent |
| Monaco Editor Page | nextjs-betterauth | - |
| Teacher Dashboard | nextjs-betterauth | ui-ux-agent |
| Code Execution Service | microservice-scaffolder | mcp-server-creator |
| Progress Tracking | fastapi-sqlmodel | db-migrator |
| Struggle Detection | microservice-scaffolder | dapr-generator |
| Kafka Topics | dapr-generator | - |
| PostgreSQL Schema | db-migrator | - |
| K8s Deployment | helm-chart-builder | helm-updater |
| E2E Testing | testing-agent | nl-test-generator |
| Skills Library (Deliverable 1) | skill-creator-pro | skill-validator |
| New Domain Skills | skill-creator | skill-creator-pro |
| Skill Quality Assurance | skill-validator | - |

---

## Usage in Commands

### In `/sp.auto-implement`:
```python
# Pseudo-code for skill detection
def detect_skill(task_description):
    patterns = {
        'fastapi-sqlmodel': ['FastAPI', 'backend', 'routes', 'API'],
        'nextjs-betterauth': ['Next.js', 'frontend', 'React', 'dashboard'],
        'helm-chart-builder': ['Helm', 'chart', 'K8s', 'deployment'],
        'microservice-scaffolder': ['Kafka', 'consumer', 'microservice'],
        'dapr-generator': ['Dapr', 'component', 'pubsub'],
        'db-migrator': ['migration', 'schema', 'database'],
        'agent-orchestrator': ['AI agent', 'orchestrator', 'workflow'],
        'skill-creator': ['create skill', 'new skill', 'build skill'],
        'skill-creator-pro': ['production skill', 'pro skill', 'domain skill', 'improve skill'],
        'skill-validator': ['validate skill', 'skill review', 'skill audit', 'check skill'],
    }

    for skill, keywords in patterns.items():
        if any(kw.lower() in task_description.lower() for kw in keywords):
            return skill
    return 'default'
```

### Manual Override in tasks.md:
```markdown
- [ ] T-005: Create progress service [SKILL: microservice-scaffolder]
- [ ] T-006: Design agent workflow [AGENT: agent-orchestrator]
```

---

## Adding New Skills

1. Create skill file in `.claude/skills/{name}.md`
2. Add entry to this registry
3. Update pattern matching in `/sp.auto-implement`

## Adding New Subagents

1. Create agent folder in `.claude/agents/{name}/`
2. Add `agent.md` with role and instructions
3. Add entry to this registry
4. Update pattern matching in `/sp.auto-implement`
