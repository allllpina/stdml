from abc import ABC, abstractmethod

from src.domain.entities import PredictionError, PredictionResult


class ResultStorage(ABC):
    """A port for storing inference results."""

    @abstractmethod
    def save(self, result: PredictionResult | PredictionError) -> None:
        """Saves the inference result to storage."""
        pass
