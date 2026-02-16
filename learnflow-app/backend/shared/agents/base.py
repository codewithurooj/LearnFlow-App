"""
Base Agent Configuration

Provides AgentConfig model, prompt loader, and agent factory using OpenAI Agents SDK.
"""

import os
from pathlib import Path
from typing import Any, Optional

import structlog
from openai import AsyncOpenAI
from pydantic import BaseModel, Field

from ..config import settings

logger = structlog.get_logger(__name__)

# Resolve prompts directory relative to this file
PROMPTS_DIR = Path(__file__).parent / "prompts"


class AgentConfig(BaseModel):
    """Configuration for an AI agent."""

    name: str
    system_prompt_path: str
    model: str = "gpt-4-turbo-preview"
    tools: list[str] = Field(default_factory=list)
    handoff_targets: list[str] = Field(default_factory=list)
    max_tokens: int = 1024
    temperature: float = 0.7


def load_prompt(prompt_name: str) -> str:
    """
    Load a system prompt from the prompts directory.

    Args:
        prompt_name: Name of the prompt file (without .md extension)

    Returns:
        The prompt text content
    """
    prompt_path = PROMPTS_DIR / f"{prompt_name}.md"

    if not prompt_path.exists():
        logger.warning("Prompt file not found", path=str(prompt_path))
        return f"You are a helpful {prompt_name} assistant."

    return prompt_path.read_text(encoding="utf-8").strip()


def create_agent(config: AgentConfig) -> dict[str, Any]:
    """
    Create an agent configuration dict for use with OpenAI Agents SDK.

    Args:
        config: The agent configuration

    Returns:
        Dict with agent parameters ready for SDK Agent() constructor
    """
    system_prompt = load_prompt(config.system_prompt_path)

    return {
        "name": config.name,
        "instructions": system_prompt,
        "model": config.model or settings.openai_model,
        "model_settings": {
            "temperature": config.temperature,
            "max_tokens": config.max_tokens,
        },
    }


# Pre-defined agent configurations
AGENT_CONFIGS = {
    "triage": AgentConfig(
        name="Triage Agent",
        system_prompt_path="triage",
        model=settings.openai_model,
        handoff_targets=["concepts", "debug", "code_review", "exercise", "progress"],
        max_tokens=256,
        temperature=0.3,
    ),
    "concepts": AgentConfig(
        name="Concepts Agent",
        system_prompt_path="concepts",
        model=settings.openai_model,
        max_tokens=2048,
        temperature=0.7,
    ),
    "debug": AgentConfig(
        name="Debug Agent",
        system_prompt_path="debug",
        model=settings.openai_model,
        max_tokens=1536,
        temperature=0.5,
    ),
    "code_review": AgentConfig(
        name="Code Review Agent",
        system_prompt_path="code_review",
        model=settings.openai_model,
        max_tokens=2048,
        temperature=0.6,
    ),
    "exercise": AgentConfig(
        name="Exercise Agent",
        system_prompt_path="exercise",
        model=settings.openai_model,
        max_tokens=2048,
        temperature=0.7,
    ),
    "progress": AgentConfig(
        name="Progress Agent",
        system_prompt_path="progress",
        model=settings.openai_model,
        max_tokens=1024,
        temperature=0.5,
    ),
}


def get_agent_config(agent_name: str) -> AgentConfig:
    """Get a pre-defined agent configuration by name."""
    if agent_name not in AGENT_CONFIGS:
        raise ValueError(f"Unknown agent: {agent_name}. Available: {list(AGENT_CONFIGS.keys())}")
    return AGENT_CONFIGS[agent_name]
