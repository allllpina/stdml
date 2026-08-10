import asyncio
import json
import uuid
from collections.abc import AsyncGenerator

import pytest
from aiokafka import AIOKafkaConsumer
from src.communicators.kafka_communicator import KafkaCommunicator

KAFKA_TEST_URL = "localhost:9094"


@pytest.fixture
def commands_topic() -> str:
    """Generates a unique command topic name per test function."""
    return f"test_commands_{uuid.uuid4().hex[:8]}"


@pytest.fixture
def prediction_topic() -> str:
    """Generates a unique prediction topic name per test function."""
    return f"test_predictions_{uuid.uuid4().hex[:8]}"


@pytest.fixture
async def communicator(
    commands_topic: str,
    prediction_topic: str
) -> AsyncGenerator[KafkaCommunicator, None]:
    """Initializes the communicator with test-isolated topics."""
    comm = KafkaCommunicator(
        bootstrap_servers=KAFKA_TEST_URL,
        commands_topic=commands_topic,
        prediction_topic=prediction_topic,
    )
    await comm.start()
    yield comm
    await comm.close()


async def test_set_model_publishes_message(
    communicator: KafkaCommunicator,
    commands_topic: str
) -> None:
    consumer = AIOKafkaConsumer(
        commands_topic,
        bootstrap_servers=KAFKA_TEST_URL,
        auto_offset_reset="earliest",
        group_id=f"test_group_{uuid.uuid4()}",
    )
    await consumer.start()
    try:
        await communicator.set_model("xgboost_v2")

        msg = await asyncio.wait_for(consumer.getone(), timeout=5.0)
        assert msg.topic == commands_topic

        payload = json.loads(msg.value.decode("utf-8"))
        assert payload == {"action": "set_model", "model_name": "xgboost_v2"}
    finally:
        await consumer.stop()


async def test_request_prediction_publishes_message(
    communicator: KafkaCommunicator,
    prediction_topic: str
) -> None:
    consumer = AIOKafkaConsumer(
        prediction_topic,
        bootstrap_servers=KAFKA_TEST_URL,
        auto_offset_reset="earliest",
        group_id=f"test_group_{uuid.uuid4()}",
    )
    await consumer.start()
    try:
        test_id = 1042
        await communicator.request_prediction(respondent_id=test_id)

        msg = await asyncio.wait_for(consumer.getone(), timeout=5.0)
        assert msg.topic == prediction_topic

        payload = json.loads(msg.value.decode("utf-8"))
        assert payload == {"respondent_id": test_id}
    finally:
        await consumer.stop()
