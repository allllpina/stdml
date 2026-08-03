import pytest
from fastapi.testclient import TestClient
from src.main import app


@pytest.fixture
def client() -> TestClient:
    """
    Provides a TestClient instance for the FastAPI application.
    This allows making HTTP requests to the API without starting a real server.
    """
    return TestClient(app)
