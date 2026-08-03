from fastapi import HTTPException, status


class MLOpsBaseException(Exception):
    """Base class for all internal API exceptions."""
    pass

class ModelNotFoundError(HTTPException):
    def __init__(self, model_name: str):
        super().__init__(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Model '{model_name}' not found or is not a champion."
        )

class KafkaConnectionError(HTTPException):
    def __init__(self) -> None:
        super().__init__(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Failed to connect to Kafka message broker."
        )
