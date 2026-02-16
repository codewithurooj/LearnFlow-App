"""
Agent Registry

Manages agent registration and handoff lookup for multi-agent orchestration.
"""

from typing import Optional

import structlog

from .base import AgentConfig, AGENT_CONFIGS

logger = structlog.get_logger(__name__)


class AgentRegistry:
    """Registry for managing agent configurations and handoff targets."""

    def __init__(self) -> None:
        self._agents: dict[str, AgentConfig] = {}

    def register(self, name: str, config: AgentConfig) -> None:
        """Register an agent configuration."""
        self._agents[name] = config
        logger.info("Agent registered", name=name)

    def get(self, name: str) -> Optional[AgentConfig]:
        """Get an agent configuration by name."""
        return self._agents.get(name)

    def get_handoff_targets(self, agent_name: str) -> list[str]:
        """Get the list of agents this agent can hand off to."""
        config = self._agents.get(agent_name)
        if not config:
            return []
        return config.handoff_targets

    def list_agents(self) -> list[str]:
        """List all registered agent names."""
        return list(self._agents.keys())

    def get_service_app_id(self, agent_name: str) -> str:
        """Map agent name to Dapr service app ID."""
        service_map = {
            "concepts": "concepts-service",
            "debug": "debug-service",
            "code_review": "code-review-service",
            "exercise": "exercise-service",
            "progress": "progress-service",
            "triage": "triage-service",
        }
        return service_map.get(agent_name, f"{agent_name}-service")

    def get_service_endpoint(self, agent_name: str) -> str:
        """Map agent name to its primary API endpoint."""
        endpoint_map = {
            "concepts": "api/v1/concepts/explain",
            "debug": "api/v1/debug/analyze",
            "code_review": "api/v1/review/analyze",
            "exercise": "api/v1/exercises/generate",
            "progress": "api/v1/progress",
        }
        return endpoint_map.get(agent_name, f"api/v1/{agent_name}")


# Singleton registry
_registry: Optional[AgentRegistry] = None


def get_registry() -> AgentRegistry:
    """Get the global agent registry, initializing with defaults if needed."""
    global _registry
    if _registry is None:
        _registry = AgentRegistry()
        for name, config in AGENT_CONFIGS.items():
            _registry.register(name, config)
    return _registry
