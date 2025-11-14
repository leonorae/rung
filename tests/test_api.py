import io
import time

from fastapi.testclient import TestClient

test_data = "tests/test_data.csv"

def test_root(client: TestClient):
    """Test root endpoint"""
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Rung API -- causal lab"}

def test_create_analysis(client: TestClient):
    """Test create analysis endpoint"""
    csv_content = b"treatment,outcome,age\n1,10.5,25\n0,8.2,30\n1,12.1,28\n"
    files = {"file": ("test.csv", io.BytesIO(csv_content), "text/csv")}

    response = client.post("/api/analyses/", files=files,)
    assert response.status_code == 200
    data = response.json()
    assert "uuid" in data
    assert data["filename"] == "test.csv"
    assert data["status"] == "pending"

