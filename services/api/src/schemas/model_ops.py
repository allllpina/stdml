from pydantic import BaseModel, Field

# ---------------------------------------------------------
# Request Schemas
# ---------------------------------------------------------

class SetModelRequest(BaseModel):
    """
    Request schema for setting a new champion model.
    TODO: Add specific versioning fields or model tags if required later.
    """
    model_name: str = Field(
        ..., description="The exact name of the model to load into the worker"
    )


class PredictionOrderRequest(BaseModel):
    """
    Request schema for triggering a prediction.
    """
    respondent_id: int = Field(..., description="Unique identifier of the respondent")


# ---------------------------------------------------------
# Response Schemas
# ---------------------------------------------------------

class GenericStatusResponse(BaseModel):
    """
    Generic response for state-changing operations (e.g., setting a model).
    """
    status: str = Field(default="accepted")
    message: str


class ModelListResponse(BaseModel):
    """
    Response schema for listing available champion models.
    TODO: Expand to list of objects if metadata (date, accuracy) is needed.
    """
    models: list[str] = Field(
        default_factory=list, description="List of available champion model names"
    )


class CurrentModelResponse(BaseModel):
    """
    Response schema for fetching the currently loaded model.
    """
    current_model: str | None = Field(
        default=None, description="Name of the currently active model"
    )


class PredictionOrderResponse(BaseModel):
    """
    Response schema for a triggered prediction order.
    """
    respondent_id: int
    status: str = Field(default="processing")
    message: str


class ModelTestResultResponse(BaseModel):
    """
    Response schema for model evaluation results.
    TODO: Add detailed metrics (MAE, RMSE, etc.) when evaluation logic is ready.
    """
    respondent_id: int
    predicted_salary: float | None = Field(
        default=None, description="The salary predicted by the model"
    )
    actual_salary: float | None = Field(
        default=None, description="The ground truth salary"
    )
    error_margin: float | None = Field(
        default=None, description="Difference between actual and predicted"
    )
