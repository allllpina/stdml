from abc import ABC, abstractmethod

from src.domain.entities import RespondentFeatures


class FeatureProvider(ABC):
    """A port for retrieving respondent attributes from the Feature Store."""

    @abstractmethod
    def get_features(self, respondent_id: int) -> RespondentFeatures | None:
        """Get the features by ID, or return `None` if none are found."""
        pass
