from datetime import UTC, datetime

from pydantic import BaseModel, Field

# ---------------------------------------------------------
# Request Schemas
# ---------------------------------------------------------


class SetModelRequest(BaseModel):
    """
    Request schema for setting a new champion model.
    TODO: Add specific versioning fields or model tags if required later.
    """

    model_name: str = Field(..., description="The exact name of the model to load into the worker")


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

    models: list[str] = Field(default_factory=list, description="List of available champion model names")


class CurrentModelResponse(BaseModel):
    """
    Response schema for fetching the currently loaded model.
    """

    current_model: str | None = Field(default=None, description="Name of the currently active model")


class PredictionOrderResponse(BaseModel):
    """
    Response schema for a triggered prediction order.
    """

    respondent_id: int
    status: str = Field(default="processing")
    message: str


FeatureValue = int | float | str | bool | None


class PredictionResult(BaseModel):
    """The model's output, to be saved to the database or sent to the client."""

    respondent_id: int
    prediction: dict[str, FeatureValue]
    processed_at: datetime = Field(default_factory=lambda: datetime.now(UTC))


class PredictionError(BaseModel):
    """The error message, to be saved to the redis cache in case of problems"""

    respondent_id: int
    error_message: str
    occured_at: datetime = Field(default_factory=lambda: datetime.now(UTC))
