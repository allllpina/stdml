from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    # Metadata
    project_name: str = "API"
    version: str = "0.1.0"

    # Infrastructure (Default values for local dev)
    kafka_bootstrap_servers: str = Field(default="localhost:9094")
    model_control_topic: str = Field(default="model_commands")
    prediction_topic: str = Field(default="predictions")

    # State and Feast
    redis_url: str = Field(default="redis://localhost:6379/0")

    # Secrets (Vault)
    vault_addr: str = Field(default="http://localhost:8200")
    vault_token: str | None = Field(default=None)

    mlflow_tracking_uri: str = Field(default="https://dagshub.com/fake-user/fake-repo.mlflow")

    # Settings can be read from .env
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore"
    )

# Settings singleton
settings = Settings()
