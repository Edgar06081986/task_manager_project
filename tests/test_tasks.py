from uuid import UUID

import pytest
from fastapi.testclient import TestClient

from app.main import app
from app.schemas.task import TaskStatus


client = TestClient(app)


def test_create_task_default_status_created():
    payload = {"title": "Test", "description": "Desc"}
    resp = client.post("/tasks", json=payload)
    assert resp.status_code == 201
    data = resp.json()
    assert UUID(data["id"])  # valid UUID
    assert data["title"] == payload["title"]
    assert data["description"] == payload["description"]
    assert data["status"] == TaskStatus.created.value


def test_get_task_and_404():
    # create
    payload = {"title": "To get"}
    created = client.post("/tasks", json=payload).json()

    # get existing
    resp_ok = client.get(f"/tasks/{created['id']}")
    assert resp_ok.status_code == 200
    assert resp_ok.json()["id"] == created["id"]

    # get missing
    resp_404 = client.get("/tasks/00000000-0000-0000-0000-000000000000")
    assert resp_404.status_code == 404


def test_list_tasks_pagination():
    # Ensure clean state is not guaranteed; create a few then list slice
    ids = []
    for i in range(5):
        resp = client.post("/tasks", json={"title": f"T{i}"})
        ids.append(resp.json()["id"])  # noqa: F841
    resp = client.get("/tasks", params={"offset": 1, "limit": 2})
    assert resp.status_code == 200
    items = resp.json()
    assert len(items) <= 2


def test_update_task_and_404():
    created = client.post("/tasks", json={"title": "Old", "description": "Old"}).json()
    # partial update
    resp = client.put(
        f"/tasks/{created['id']}",
        json={"title": "New", "status": TaskStatus.in_progress.value},
    )
    assert resp.status_code == 200
    data = resp.json()
    assert data["title"] == "New"
    assert data["description"] == "Old"
    assert data["status"] == TaskStatus.in_progress.value

    # missing
    resp_404 = client.put(
        "/tasks/00000000-0000-0000-0000-000000000000",
        json={"title": "x"},
    )
    assert resp_404.status_code == 404


def test_delete_task_and_404():
    created = client.post("/tasks", json={"title": "To delete"}).json()
    resp_no_content = client.delete(f"/tasks/{created['id']}")
    assert resp_no_content.status_code == 204

    # already removed
    resp_404 = client.delete(f"/tasks/{created['id']}")
    assert resp_404.status_code == 404