"""
LearnFlow Environment Configuration

Centralized configuration management for all microservices.
Uses pydantic-settings for environment variable loading and validation.
"""

from functools import lru_cache
from typing import Optional

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )

    # Service identification
    service_name: str = "learnflow-service"
    service_version: str = "1.0.0"
    environment: str = "development"

    # Server configuration
    host: str = "0.0.0.0"
    port: int = 8000
    debug: bool = False

    # OpenAI configuration
    openai_api_key: str = ""
    openai_model: str = "gpt-4-turbo-preview"
    openai_timeout: int = 30

    # Database configuration
    database_url: str = "postgresql://learnflow:learnflow@localhost:5432/learnflow"
    neon_database_url: str = ""
    use_neon: bool = False

    # Dapr configuration
    dapr_http_port: int = 3500
    dapr_grpc_port: int = 50001
    dapr_pubsub_name: str = "pubsub-kafka"
    dapr_statestore_name: str = "statestore-postgres"

    # Kafka topics
    topic_learning_questions: str = "learning.questions"
    topic_learning_responses: str = "learning.responses"
    topic_code_submissions: str = "code.submissions"
    topic_code_results: str = "code.results"
    topic_struggle_detected: str = "struggle.detected"
    topic_progress_updated: str = "progress.updated"

    # Code execution limits
    code_execution_timeout: int = 5
    code_memory_limit_mb: int = 50

    # Struggle detection thresholds
    struggle_error_threshold: int = 3
    struggle_stuck_minutes: int = 10
    struggle_low_score_threshold: float = 0.5
    struggle_failure_threshold: int = 5

    # Mastery calculation weights
    mastery_weight_exercises: float = 0.4
    mastery_weight_quizzes: float = 0.3
    mastery_weight_code_quality: float = 0.2
    mastery_weight_streak: float = 0.1

    # Logging
    log_level: str = "INFO"
    log_format: str = "json"

    @property
    def dapr_http_url(self) -> str:
        """Get Dapr HTTP endpoint URL."""
        return f"http://localhost:{self.dapr_http_port}"

    @property
    def is_production(self) -> bool:
        """Check if running in production environment."""
        return self.environment.lower() == "production"

    @property
    def active_database_url(self) -> str:
        """Get the active database URL (Neon in production, local otherwise)."""
        if self.use_neon and self.neon_database_url:
            return self.neon_database_url
        return self.database_url


@lru_cache()
def get_settings() -> Settings:
    """
    Get cached settings instance.

    Returns:
        Settings: Application settings loaded from environment.
    """
    return Settings()


# Export commonly used settings
settings = get_settings()
