from typing import cast

from src.communicators.base import (
    BrokerCommunicator,
    CacheCommunicator,
    MLFlowCommunicator,
)
from src.schemas.model_ops import PredictionResult


class ModelService:
    def __init__(
        self,
        broker: BrokerCommunicator,
        cache: CacheCommunicator,
        mlflow: MLFlowCommunicator,
    ):
        self._broker = broker
        self._cache = cache
        self._mlflow = mlflow

    async def get_models(self) -> list[str]:
        """Fetches the list of available models from the MLflow registry."""
        return cast(list[str], await self._mlflow.get_models())

    async def get_model(self) -> str | None:
        """Fetches the currently active model from the Redis cache."""
        return cast(str | None, await self._cache.get_model())

    async def set_model(self, model_name: str) -> None:
        """
        Publishes a command to the message broker to switch the active model.
        The worker service will pick this up and update Redis once it loads the model.
        """
        await self._broker.set_model(model_name)

    async def predict(self, respondent_id: int) -> None:
        """Publishes an inference request to the message broker."""
        await self._broker.request_prediction(respondent_id)

    async def get_result(self, respondent_id: int) -> PredictionResult:
        """
        Attempts to fetch the final prediction result from the cache.
        Returns a mock schema if the result is not yet available.
        """
        result = await self._cache.get_prediction_result(respondent_id)

        if result is not None:
            return PredictionResult(**result)

        return PredictionResult(
            respondent_id=respondent_id,
            status="processing_or_not_found",
            prediction=None,
            confidence=0.0
        )
