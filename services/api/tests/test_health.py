from fastapi.testclient import TestClient
from src.core.config import settings


def test_health_check_status_code(client: TestClient) -> None:
    """
    Ensures the /health endpoint returns a 200 OK status.
    """
    response = client.get("/health")
    assert response.status_code == 200


def test_health_check_response_structure(client: TestClient) -> None:
    """
    Validates the JSON payload returned by the /health endpoint.
    """
    response = client.get("/health")
    data = response.json()

    assert data["status"] == "ok"
    assert data["service"] == settings.project_name
    assert data["version"] == settings.version
    assert "kafka_broker" in data
