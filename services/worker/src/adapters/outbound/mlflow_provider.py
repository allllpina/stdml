import logging
from typing import cast, override

import mlflow
import pandas as pd
from mlflow.pyfunc import PyFuncModel

from src.domain.entities import FeatureValue, RespondentFeatures
from src.ports.model_provider import ModelProvider

logger = logging.getLogger(__name__)


class MLflowModelProvider(ModelProvider):
    """Implementation of ModelProvider for use with MLflow."""

    def __init__(self, tracking_uri: str):
        mlflow.set_tracking_uri(tracking_uri)
        self._model: None | PyFuncModel = None
        self._current_model_name: str | None = None

    @override
    def load_model(self, model_name: str) -> None:
        """
        Loads the model from MLflow using the alias “champion.”
        Blocks execution until the model is fully loaded into memory.
        """
        model_uri = f"models:/{model_name}@champion"
        logger.info(f"Downloading model from MLflow: {model_uri}")

        try:
            self._model = mlflow.pyfunc.load_model(model_uri)
            self._current_model_name = model_name
            logger.info("The model has been successfully loaded into the worker's memory.")
        except Exception as e:
            logger.error(f"Model loading error {model_uri}: {e}")
            raise RuntimeError(f"Unable to load the model {model_name}") from e

    @override
    def predict(self, features: RespondentFeatures) -> dict[str, FeatureValue]:
        """Generating a forecast. The model is expected to be loaded."""
        if self._model is None:
            raise RuntimeError("The model has not been loaded. Call `load_model()` before `predict()`.")

        feature_dict = features.model_dump(by_alias=True, exclude={"respondent_id"})
        df_input = pd.DataFrame([feature_dict])

        try:
            raw_prediction: object = self._model.predict(df_input)

            if not isinstance(raw_prediction, pd.DataFrame):
                raise TypeError(f"Model returned {type(raw_prediction)}, expected pd.DataFrame")

            result_dict = raw_prediction.to_dict(orient="records")[0]

            return cast(dict[str, FeatureValue], result_dict)

        except Exception as e:
            logger.error(f"Error during inference: {e}")
            raise
