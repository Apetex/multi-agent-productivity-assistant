import json
from fastapi.testclient import TestClient
from app.main import app


def test_health():
    client = TestClient(app)
    resp = client.get("/health")
    assert resp.status_code == 200
    assert resp.json().get("status") == "healthy"


def test_chat_note():
    client = TestClient(app)
    resp = client.post("/chat", json={"message": "Save note: test note from unit test"})
    assert resp.status_code == 200
    body = resp.json()
    assert "final_response" in body
