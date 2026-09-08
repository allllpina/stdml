from abc import ABC, abstractmethod

from src.domain.entities import FeatureValue, RespondentFeatures


class ModelProvider(ABC):
    """A port for working with ML models (loading and inference)."""

    @abstractmethod
    def load_model(self, model_name: str) -> None:
        """Loads a model into the worker's memory (for example, by the “champion” tag)."""
        pass

    @abstractmethod
    def predict(self, features: RespondentFeatures) -> dict[str, FeatureValue]:
        """It generates a forecast based on the features it has received."""
        pass
