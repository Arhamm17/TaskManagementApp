import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "backend"))

from backend.app import app


def test_health():
    client = app.test_client()

    response = client.get("/api/health")

    assert response.status_code == 200
    assert response.json["status"] == "ok"


def test_get_tasks():
    client = app.test_client()

    response = client.get("/api/tasks")

    assert response.status_code == 200
    assert isinstance(response.json, list)


def test_create_task():
    client = app.test_client()

    response = client.post(
        "/api/tasks",
        json={"title": "Test task"}
    )

    assert response.status_code == 201
    assert response.json["title"] == "Test task"