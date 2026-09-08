import asyncio
import json
import logging

from aiokafka import AIOKafkaConsumer
from src.domain.entities import InferenceCommand, ModelSwapCommand
from src.domain.use_cases import InferenceService

logger = logging.getLogger(__name__)


class KafkaInboundListener:
    """Adapter that listens to Kafka topics for inference commands and control events."""

    def __init__(
        self,
        bootstrap_servers: str,
        inference_topic: str,
        control_topic: str,
        group_id: str,
        inference_service: InferenceService,
    ):
        self._inference_topic = inference_topic
        self._control_topic = control_topic
        self._inference_service = inference_service

        self._consumer = AIOKafkaConsumer(
            self._inference_topic,
            self._control_topic,
            bootstrap_servers=bootstrap_servers,
            group_id=group_id,
            enable_auto_commit=True,
            value_deserializer=lambda m: json.loads(m.decode("utf-8")),
        )

    async def start(self) -> None:
        """Starts the infinite Kafka listening loop."""
        await self._consumer.start()
        logger.info(f"Kafka Listener started. Subscribed to: [{self._inference_topic}, {self._control_topic}]")

        try:
            async for msg in self._consumer:
                try:
                    raw_data = msg.value
                    topic = msg.topic
                    logger.info(f"Received message from topic '{topic}': {raw_data}")

                    # Route the message based on the topic it originated from
                    if topic == self._inference_topic:
                        inf_command = InferenceCommand.model_validate(raw_data)
                        await asyncio.to_thread(self._inference_service.process, inf_command)

                    elif topic == self._control_topic:
                        swap_command = ModelSwapCommand.model_validate(raw_data)
                        await asyncio.to_thread(self._inference_service.swap_model, swap_command)

                    else:
                        logger.warning(f"Received message from unknown topic: {topic}")

                except Exception as e:
                    logger.error(f"Error processing Kafka message: {e}", exc_info=True)
        finally:
            await self._consumer.stop()
            logger.info("Kafka Listener stopped.")
