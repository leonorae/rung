import io
import time

from fastapi.testclient import TestClient

test_data = "tests/test_data.csv"

def test_root(client: TestClient):
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Rung API -- causal lab"}

def test_create_analysis(client: TestClient):
    """this only tests the creation, not the completion"""
    csv_content = b"treatment,outcome,age\n1,10.5,25\n0,8.2,30\n1,12.1,28\n"
    files = {"file": ("test.csv", io.BytesIO(csv_content), "text/csv")}

    response = client.post("/api/analyses/", files=files,)
    assert response.status_code == 200
    data = response.json()
    assert "uuid" in data
    assert data["filename"] == "test.csv"
    assert data["status"] == "pending"

def test_get_analysis(client: TestClient):
    csv_content = b"treatment,outcome\n1,10\n0,8\n"
    files = {"file": ("test.csv", io.BytesIO(csv_content), "text/csv")}
    create_response = client.post("/api/analyses/", files=files)
    analysis_uuid = create_response.json()["uuid"]

    response = client.get(f"/api/analyses/{analysis_uuid}")
    assert response.status_code == 200
    data = response.json()
    assert data["uuid"] == analysis_uuid
    assert data["filename"] == "test.csv"


def test_get_nonexistent_analysis(client: TestClient):
    """Test 404 for nonexistent analysis"""
    response = client.get("/api/analyses/nonexistent-id")
    assert response.status_code == 404


def test_list_analyses(client: TestClient):
    """test two analyses"""
    csv_content = b"treatment,outcome\n1,10\n0,8\n"
    files = {"file": ("test.csv", io.BytesIO(csv_content), "text/csv")}
    client.post("/api/analyses/", files=files)
    client.post("/api/analyses/", files=files)

    response = client.get("/api/analyses/")
    assert response.status_code == 200
    data = response.json()
    assert len(data) >= 2
    assert all("uuid" in item for item in data)

def test_analysis_processing(client: TestClient):
    """stub, implement when real processing"""
    pass