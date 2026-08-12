import asyncio

from mlflow.tracking import MlflowClient

from .base import MLFlowCommunicator


class DagsHubCommunicator(MLFlowCommunicator):
    def __init__(self, tracking_uri: str):
        """
        Initializes the MLflow client pointing to your DagsHub repository.
        Note: The environment variables
        (MLFLOW_TRACKING_USERNAME, MLFLOW_TRACKING_PASSWORD)
        must be loaded in the OS environment
        for the client to authenticate successfully.
        """
        self._client = MlflowClient(tracking_uri=tracking_uri)

    async def get_models(self) -> list[str]:
        """
        Asynchronously fetches a list of all available models from the DagsHub registry.
        """

        return await asyncio.to_thread(self._fetch_models_sync)

    def _fetch_models_sync(self) -> list[str]:
        """
        Synchronous helper method containing your exact scaffold logic.
        """
        registered_models = self._client.search_registered_models()


        return [model.name for model in registered_models]
