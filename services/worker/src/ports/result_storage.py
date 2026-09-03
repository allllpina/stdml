from abc import ABC, abstractmethod

from src.domain.entities import PredictionResult


class ResultStorage(ABC):
    """A port for storing inference results."""

    @abstractmethod
    def save(self, result: PredictionResult) -> None:
        """Saves the inference result to storage."""
        pass
