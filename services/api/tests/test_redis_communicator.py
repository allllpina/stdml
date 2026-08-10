import json
from collections.abc import AsyncGenerator

import pytest
import redis.asyncio as redis
from src.communicators.redis_communicator import RedisCommunicator

# Both local port-forwarding and GitHub Actions Service Containers will use this
REDIS_TEST_URL = "redis://localhost:6379/0"

@pytest.fixture
async def real_redis_client() -> AsyncGenerator[redis.Redis, None]:
    """A direct raw Redis client used strictly for setting up test data
    and cleaning the database after tests run.
    """
    async with redis.Redis.from_url(REDIS_TEST_URL, decode_responses=True) as client:
        yield client
        await client.delete("current_model", "result:999", "result:777")


@pytest.fixture
async def communicator() -> AsyncGenerator[RedisCommunicator, None]:
    """The actual class instance we are testing."""
    comm = RedisCommunicator(REDIS_TEST_URL)
    yield comm
    await comm.close()


@pytest.mark.asyncio
async def test_get_model_success(
    communicator: RedisCommunicator,
    real_redis_client: redis.Redis,
) -> None:
    await real_redis_client.set("current_model", "xgboost_v1")

    model = await communicator.get_model()

    assert model == "xgboost_v1"


@pytest.mark.asyncio
async def test_get_results_success(
    communicator: RedisCommunicator,
    real_redis_client: redis.Redis,
) -> None:
    test_id = 999
    payload = {"prediction": 42.5, "anomaly": False}
    await real_redis_client.set(f"result:{test_id}", json.dumps(payload))

    result = await communicator.get_results(respondent_id=test_id)

    assert result == payload


@pytest.mark.asyncio
async def test_get_results_not_found(
    communicator: RedisCommunicator,
) -> None:
    result = await communicator.get_results(respondent_id=888)

    assert result is None


@pytest.mark.asyncio
async def test_get_results_invalid_json_graceful_fail(
    communicator: RedisCommunicator,
    real_redis_client: redis.Redis,
) -> None:
    test_id = 777
    await real_redis_client.set(f"result:{test_id}", "this is strictly not json")

    result = await communicator.get_results(respondent_id=test_id)

    assert result is None
