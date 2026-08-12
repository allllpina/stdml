import json

from aiokafka import AIOKafkaProducer
from src.schemas.events import ModelCommandEvent, PredictionRequestEvent

from .base import BrokerCommunicator


class KafkaCommunicator(BrokerCommunicator):
    def __init__(
        self,
        bootstrap_servers: str,
        commands_topic: str = "model_commands",
        prediction_topic: str = "predictions"
    ):
        """
        Initializes the Kafka producer configuration.
        We inject the topic names so they can be easily overridden in tests.
        """
        self._commands_topic = commands_topic
        self._prediction_topic = prediction_topic

        self._producer = AIOKafkaProducer(
            bootstrap_servers=bootstrap_servers,
            value_serializer=lambda v: json.dumps(v).encode("utf-8")
        )

    async def start(self) -> None:
        """
        Starts the Kafka producer.
        MUST be called during the FastAPI lifespan startup event.
        """
        await self._producer.start()

    async def close(self) -> None:
        """
        Stops the Kafka producer and flushes pending messages.
        MUST be called during the FastAPI lifespan shutdown event.
        """
        await self._producer.stop()

    async def set_model(self, model_name: str) -> None:
        """Publishes a command to switch the active model."""
        event = ModelCommandEvent(action="set_model", model_name=model_name)
        await self._producer.send_and_wait(self._commands_topic, event.model_dump())

    async def request_prediction(self, respondent_id: int) -> None:
        """Publishes a request to perform inference on a respondent."""
        event = PredictionRequestEvent(respondent_id=respondent_id)
        await self._producer.send_and_wait(self._prediction_topic, event.model_dump())
