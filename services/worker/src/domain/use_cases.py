import logging

from src.domain.entities import (
    CurrentModelMessage,
    InferenceCommand,
    ModelSwapCommand,
    PredictionError,
    PredictionResult,
)
from src.ports.feature_provider import FeatureProvider
from src.ports.model_provider import ModelProvider
from src.ports.result_storage import ResultStorage

logger = logging.getLogger(__name__)


class InferenceService:
    """Business-orchestration of inference process."""

    def __init__(
        self,
        feature_provider: FeatureProvider,
        model_provider: ModelProvider,
        result_storage: ResultStorage,
    ):
        self._feature_provider = feature_provider
        self._model_provider = model_provider
        self._result_storage = result_storage

    def process(self, command: InferenceCommand) -> PredictionResult | PredictionError:
        logger.info(f"Starting request processing {command.request_id} for respondent_id={command.respondent_id}")

        result: PredictionResult | PredictionError

        try:
            features = self._feature_provider.get_features(command.respondent_id)
            if features is None:
                raise ValueError(f"Features for respondent_id={command.respondent_id} not found in Feature Store.")

            prediction_dict = self._model_provider.predict(features)
            result = PredictionResult(
                request_id=command.request_id,
                respondent_id=command.respondent_id,
                prediction=prediction_dict,
            )
        except Exception as e:
            result = PredictionError(
                request_id=command.request_id, respondent_id=command.respondent_id, error_message=f"Error: {e}"
            )

        self._result_storage.save(result)
        logger.info(f"Request {command.request_id} has been processed and saved successfully.")

        return result

    def swap_model(self, command: ModelSwapCommand) -> None:
        """Handles the hot-swap of the ML model in memory."""
        logger.info(f"Initiating model hot-swap to '{command.model_name}' (champion)")

        try:
            self._model_provider.load_model(command.model_name)
            msg = CurrentModelMessage(current_model=command.model_name)
            self._result_storage.save_current_model(msg)
            logger.info(f"Model successfully swapped to '{command.model_name}' and state updated.")
        except Exception as e:
            logger.error(f"Error {e} has occurred during weights swapping.", exc_info=True)
