# ADR-001: Skills + MCP Code Execution Over Direct MCP Integration

- **Status:** Accepted
- **Date:** 2026-01-15
- **Feature:** Skills Library
- **Context:** The project requires AI agents (Claude Code, Goose) to deploy infrastructure and build applications autonomously. We needed to decide how agents interact with external tools and services.

## Decision

Adopt the **Skills + MCP Code Execution** pattern instead of connecting MCP servers directly to agents.

- **Entry Point**: SKILL.md (~100 tokens loaded on trigger)
- **Execution**: scripts/*.sh and scripts/*.py (0 tokens, executed not loaded)
- **Reference**: REFERENCE.md (0 tokens, loaded on-demand)
- **Result**: Only minimal output enters agent context (~10 tokens)

## Consequences

### Positive

- 80-98% token reduction compared to direct MCP (from ~50,000 to ~110 tokens)
- Cross-agent compatibility: same skills work on Claude Code, Goose, and Codex
- Scripts can be versioned, tested, and debugged independently
- Agent context window preserved for actual reasoning and conversation
- Skills are reusable across projects, not just this hackathon

### Negative

- Extra layer of indirection: debugging requires checking both SKILL.md and scripts
- Scripts must handle their own error reporting concisely
- Agents cannot dynamically discover MCP tool capabilities (fixed skill interface)

## Alternatives Considered

**Alternative A: Direct MCP Server Integration**
- Connect MCP servers to agents via ~/.claude/mcp.json
- Every tool definition loads at startup (~10,000-50,000 tokens)
- Why rejected: Consumes 25-41% of context window before conversation starts

**Alternative B: Skills without scripts (instructions only)**
- SKILL.md contains full instructions, agent writes code each time
- Why rejected: No token savings on execution, agent may generate incorrect commands

## References

- Feature Spec: `specs/001-skills-library/spec.md`
- Implementation Plan: `specs/001-skills-library/plan.md`
- Related ADRs: ADR-002 (Multi-Agent Architecture)
- Source: [Anthropic Engineering Blog - Code Execution with MCP](https://www.anthropic.com/engineering/code-execution-with-mcp)
