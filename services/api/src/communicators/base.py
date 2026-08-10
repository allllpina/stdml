from abc import ABC, abstractmethod
from typing import Any


class CacheCommunicator(ABC):
    """Abstract contract for interacting with the caching layer (e.g., Redis)."""

    @abstractmethod
    async def get_model(self) -> str | None:
        """Retrieves the currently active model name."""
        pass

    @abstractmethod
    async def get_results(self, respondent_id: int) -> dict[str, Any] | None:
        """Retrieves the inference results for a specific respondent."""
        pass


class BrokerCommunicator(ABC):
    """Abstract contract for interacting with the message broker (e.g., Kafka)."""

    @abstractmethod
    async def set_model(self, model_name: str) -> None:
        """Publishes a command to switch the active model."""
        pass

    @abstractmethod
    async def request_prediction(self, respondent_id: int) -> None:
        """Publishes a request to perform inference on a respondent."""
        pass


class MLFlowCommunicator(ABC):
    """Abstract contract for interacting with the model registry (e.g., DagsHub)."""

    @abstractmethod
    async def get_models(self) -> list[str]:
        """Fetches a list of all available models from the registry."""
        pass
