"""
Shared Agent Utilities

Base agent configuration, registry, and prompt loading for OpenAI Agents SDK.
"""

from .base import AgentConfig, create_agent, load_prompt
from .registry import AgentRegistry, get_registry

__all__ = [
    "AgentConfig",
    "create_agent",
    "load_prompt",
    "AgentRegistry",
    "get_registry",
]
