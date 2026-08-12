from unittest.mock import MagicMock, patch

import pytest
from src.communicators.mlflow_communicator import DagsHubCommunicator


@pytest.fixture
def dummy_tracking_uri() -> str:
    return "https://dagshub.com/fake-user/fake-repo.mlflow"

@pytest.mark.asyncio
async def test_get_models_success(dummy_tracking_uri: str) -> None:
    with patch(
        "src.communicators.mlflow_communicator.MlflowClient"
    ) as mock_client_class:

        mock_client_instance = MagicMock()

        mock_model_1 = MagicMock()
        mock_model_1.name = "xgboost_v1"

        mock_model_2 = MagicMock()
        mock_model_2.name = "neural_net_v2"

        mock_client_instance.search_registered_models.return_value = [
            mock_model_1, mock_model_2
        ]

        mock_client_class.return_value = mock_client_instance

        communicator = DagsHubCommunicator(tracking_uri=dummy_tracking_uri)

        models = await communicator.get_models()

        assert models == ["xgboost_v1", "neural_net_v2"]
        mock_client_instance.search_registered_models.assert_called_once()


@pytest.mark.asyncio
async def test_get_models_empty(dummy_tracking_uri: str) -> None:
    with patch(
        "src.communicators.mlflow_communicator.MlflowClient"
    ) as mock_client_class:

        mock_client_instance = MagicMock()

        mock_client_instance.search_registered_models.return_value = []
        mock_client_class.return_value = mock_client_instance

        communicator = DagsHubCommunicator(tracking_uri=dummy_tracking_uri)

        models = await communicator.get_models()

        assert models == []
