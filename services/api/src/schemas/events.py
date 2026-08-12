from typing import Literal

from pydantic import BaseModel


class ModelCommandEvent(BaseModel):
    action: Literal["set_model"]
    model_name: str

class PredictionRequestEvent(BaseModel):
    respondent_id: int
