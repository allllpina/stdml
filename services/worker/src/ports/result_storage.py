from abc import ABC, abstractmethod

from src.domain.entities import CurrentModelMessage, PredictionError, PredictionResult


class ResultStorage(ABC):
    """A port for storing inference results."""

    @abstractmethod
    def save(self, result: PredictionResult | PredictionError) -> None:
        """Saves the inference result to storage."""
        pass

    @abstractmethod
    def save_current_model(self, message: CurrentModelMessage) -> None:
        """Saves the currently loaded model state to the storage."""
        pass
