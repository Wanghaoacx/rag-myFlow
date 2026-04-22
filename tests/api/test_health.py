from fastapi.testclient import TestClient

from rag_myflow.api.app import create_app
from rag_myflow.config import AppConfig


def test_health_endpoint_returns_workspace_context() -> None:
    client = TestClient(create_app())

    response = client.get("/api/health")

    assert response.status_code == 200
    assert response.json() == {"status": "ok", "workspace": "local"}


def test_health_endpoint_uses_injected_workspace_context() -> None:
    client = TestClient(create_app(AppConfig(workspace_slug="lab")))

    response = client.get("/api/health")

    assert response.status_code == 200
    assert response.json() == {"status": "ok", "workspace": "lab"}
