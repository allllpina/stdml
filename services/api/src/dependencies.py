from functools import lru_cache

from fastapi import Depends, Request
from src.communicators.base import (
    BrokerCommunicator,
    CacheCommunicator,
    MLFlowCommunicator,
)
from src.core.config import Settings, settings
from src.services.model_service import ModelService


@lru_cache
def get_settings() -> Settings:
    """
    Dependency for injecting application settings.
    Uses lru_cache to ensure settings are instantiated only once.
    """
    return settings


def get_broker(request: Request) -> BrokerCommunicator:
    """Extracts the initialized Kafka broker from the FastAPI app state."""
    return request.app.state.broker


def get_cache(request: Request) -> CacheCommunicator:
    """Extracts the initialized Redis cache from the FastAPI app state."""
    return request.app.state.cache


def get_mlflow(request: Request) -> MLFlowCommunicator:
    """Extracts the initialized DagsHub MLflow client from the FastAPI app state."""
    return request.app.state.mlflow


def get_model_service(
    broker: BrokerCommunicator = Depends(get_broker),
    cache: CacheCommunicator = Depends(get_cache),
    mlflow: MLFlowCommunicator = Depends(get_mlflow),
) -> ModelService:
    """
    Constructs and injects the ModelService.
    FastAPI will automatically resolve the broker, cache, and mlflow dependencies first.
    """
    return ModelService(broker=broker, cache=cache, mlflow=mlflow)
