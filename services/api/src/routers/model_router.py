from fastapi import APIRouter, Depends, status
from src.dependencies import get_model_service
from src.schemas.model_ops import (
    CurrentModelResponse,
    GenericStatusResponse,
    ModelListResponse,
    PredictionOrderRequest,
    PredictionOrderResponse,
    PredictionResult,
    SetModelRequest,
)
from src.services.model_service import ModelService

router = APIRouter(prefix="/models", tags=["Models"])


@router.get("", response_model=ModelListResponse)
async def list_models(
    service: ModelService = Depends(get_model_service),
) -> ModelListResponse:
    """Fetches the list of available champion models."""
    models = await service.get_models()
    return ModelListResponse(models=models)


@router.get("/current", response_model=CurrentModelResponse)
async def get_current_model(
    service: ModelService = Depends(get_model_service),
) -> CurrentModelResponse:
    """Fetches the currently active model."""
    model = await service.get_model()
    return CurrentModelResponse(current_model=model)


@router.post(
    "/current",
    response_model=GenericStatusResponse,
    status_code=status.HTTP_202_ACCEPTED,
)
async def set_current_model(
    request: SetModelRequest,
    service: ModelService = Depends(get_model_service),
) -> GenericStatusResponse:
    """Publishes a command to switch the active model."""
    await service.set_model(request.model_name)
    return GenericStatusResponse(
        status="accepted",
        message=f"Model switch to '{request.model_name}' initiated.",
    )


@router.post(
    "/predict",
    response_model=PredictionOrderResponse,
    status_code=status.HTTP_202_ACCEPTED,
)
async def request_prediction(
    request: PredictionOrderRequest,
    service: ModelService = Depends(get_model_service),
) -> PredictionOrderResponse:
    """Publishes a request to perform inference on a respondent."""
    await service.predict(request.respondent_id)
    return PredictionOrderResponse(
        respondent_id=request.respondent_id,
        status="processing",
        message="Prediction request queued successfully.",
    )


@router.get("/predict/{respondent_id}", response_model=PredictionResult)
async def get_prediction_result(
    respondent_id: int,
    service: ModelService = Depends(get_model_service),
) -> PredictionResult:
    """Retrieves the prediction result from the cache."""
    return await service.get_result(respondent_id)
