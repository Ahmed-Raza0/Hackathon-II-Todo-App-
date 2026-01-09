import pytest
from app.main import app
from fastapi.testclient import TestClient


@pytest.fixture
def test_client():
    """Create a test client for the app."""
    with TestClient(app) as client:
        yield client