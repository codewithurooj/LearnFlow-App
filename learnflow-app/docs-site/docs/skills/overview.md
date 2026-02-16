---
sidebar_position: 1
---

# Skills Library

The Skills Library is a collection of 11 reusable Skills that work on both Claude Code and Goose.

## What is a Skill?

A Skill is a lightweight instruction package (~100 tokens) that teaches an AI agent how to perform a specific task. Instead of loading entire MCP server contexts (50,000+ tokens), Skills use scripts for execution and return minimal output.

```
.claude/skills/<skill-name>/
├── SKILL.md           # ~100 tokens (loaded when triggered)
├── REFERENCE.md       # 0 tokens (loaded on-demand)
└── scripts/
    ├── deploy.sh      # 0 tokens (executed, not loaded)
    └── verify.sh      # 0 tokens (executed, returns minimal output)
```

## Available Skills

### Infrastructure (P0)

| Skill | Purpose |
|-------|---------|
| `kafka-k8s-setup` | Deploy Kafka broker to Kubernetes |
| `postgres-k8s-setup` | Deploy PostgreSQL to Kubernetes |
| `dapr-k8s-setup` | Install and configure Dapr service mesh |
| `kong-k8s-setup` | Deploy Kong API Gateway |
| `infrastructure-verify` | Health check all infrastructure components |

### Application (P1)

| Skill | Purpose |
|-------|---------|
| `fastapi-dapr-agent` | Scaffold FastAPI + Dapr microservices |
| `mcp-code-execution` | Generate MCP servers with code execution |
| `nextjs-k8s-deploy` | Build and deploy Next.js to Kubernetes |
| `docusaurus-deploy` | Build and deploy Docusaurus documentation |

### Meta

| Skill | Purpose |
|-------|---------|
| `agents-md-gen` | Generate AGENTS.md files for repositories |
| `_shared/utils.sh` | Shared utility functions across skills |
