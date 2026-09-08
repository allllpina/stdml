from unittest.mock import MagicMock

import pytest
from src.domain.entities import (
    InferenceCommand,
    ModelSwapCommand,
    PredictionError,
    PredictionResult,
    RespondentFeatures,
)
from src.domain.use_cases import InferenceService
from src.ports.feature_provider import FeatureProvider
from src.ports.model_provider import ModelProvider
from src.ports.result_storage import ResultStorage


@pytest.fixture
def mock_feature_provider() -> MagicMock:
    return MagicMock(spec=FeatureProvider)


@pytest.fixture
def mock_model_provider() -> MagicMock:
    return MagicMock(spec=ModelProvider)


@pytest.fixture
def mock_result_storage() -> MagicMock:
    return MagicMock(spec=ResultStorage)


@pytest.fixture
def inference_service(
    mock_feature_provider: MagicMock,
    mock_model_provider: MagicMock,
    mock_result_storage: MagicMock,
) -> InferenceService:
    return InferenceService(
        feature_provider=mock_feature_provider,
        model_provider=mock_model_provider,
        result_storage=mock_result_storage,
    )


def test_process_inference_success(
    inference_service: InferenceService,
    mock_feature_provider: MagicMock,
    mock_model_provider: MagicMock,
    mock_result_storage: MagicMock,
) -> None:
    # Arrange
    command = InferenceCommand(respondent_id=1)

    # Використовуємо словник з реальними ключами з Feast
    raw_feast_data = {
        "DatabaseServers": 400.0,
        "Survey Year": 2025,
        "PrimaryDatabase": "Microsoft SQL Server",
        "OtherDatabases": "MySQL/MariaDB, PostgreSQL, Microsoft Access, Azure SQL DB (any flavor), Informix",
        "CareerPlansThisYear": "Stay with the same employer, same role",
        "EmploymentSector": "Non-profit",
        "ManageStaff": False,
        "SalaryUSD": 127000.0,
        "EmploymentStatus": "Full time employee",
        "OtherPeopleOnYourTeam": 5,
        "JobTitle": "DBA (Production Focus - build & troubleshoot servers, HA/DR)",
        "YearsWithThisTypeOfJob": 21,
        "HowManyCompanies": "1 (this is the only company where I've had this kind of position)",
        "Gender": "Male",
        "YearsWithThisDatabase": 24,
        "Country": "United States",
        "PopulationOfLargestCityWithin20Miles": "100K-299K (city)",
    }

    # Pydantic сам змапить ці ключі на правильні поля (database_servers тощо)
    mock_features = RespondentFeatures.model_validate(raw_feast_data)

    mock_feature_provider.get_features.return_value = mock_features
    mock_model_provider.predict.return_value = {"prediction": 125000.0}

    # Act
    result = inference_service.process(command)

    # Assert
    assert isinstance(result, PredictionResult)
    assert result.respondent_id == 1
    assert result.prediction == {"prediction": 125000.0}

    # Перевіряємо виклики
    mock_feature_provider.get_features.assert_called_once_with(1)
    mock_model_provider.predict.assert_called_once_with(mock_features)
    mock_result_storage.save.assert_called_once_with(result)


def test_process_inference_missing_features(
    inference_service: InferenceService,
    mock_feature_provider: MagicMock,
    mock_result_storage: MagicMock,
) -> None:
    # Arrange
    command = InferenceCommand(respondent_id=999)
    mock_feature_provider.get_features.return_value = None

    # Act
    result = inference_service.process(command)

    # Assert
    assert isinstance(result, PredictionError)
    assert result.respondent_id == 999
    assert "not found in Feature Store" in result.error_message

    mock_result_storage.save.assert_called_once_with(result)


def test_swap_model_success(
    inference_service: InferenceService,
    mock_model_provider: MagicMock,
    mock_result_storage: MagicMock,
) -> None:
    # Arrange
    command = ModelSwapCommand(model_name="New_Champion_Model")

    # Act
    inference_service.swap_model(command)

    # Assert
    mock_model_provider.load_model.assert_called_once_with("New_Champion_Model")
    mock_result_storage.save_current_model.assert_called_once()

    saved_msg = mock_result_storage.save_current_model.call_args[0][0]
    assert saved_msg.current_model == "New_Champion_Model"
