from pathlib import Path

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict

# Compute default feast repo path dynamically based on file location
PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent.parent
DEFAULT_FEAST_REPO = str(PROJECT_ROOT / "infra" / "feast")


class Settings(BaseSettings):
    """Application settings loaded from environment variables or .env file."""

    # Feast configuration
    feast_repo_path: str = Field(default=DEFAULT_FEAST_REPO)

    # MLflow configuration
    mlflow_tracking_uri: str = Field(default="http://localhost:5000")
    initial_model_name: str = Field(default="Model_Pyfunc")

    # Redis configuration
    redis_url: str = Field(default="redis://localhost:6379/0")

    # Kafka configuration
    kafka_bootstrap_servers: str = Field(default="localhost:9094")
    prediction_topic: str = Field(default="inference_commands")
    model_control_topic: str = Field(default="model_commands")
    kafka_group_id: str = Field(default="ml_worker_group")

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )


settings = Settings()
