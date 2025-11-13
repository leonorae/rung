import io
import time
from fastapi.testclient import TestClient


def test_root(client: TestClient):
    """Test root endpoint"""
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Rung API -- causal lab"}

