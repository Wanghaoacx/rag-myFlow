from fastapi.testclient import TestClient

from rag_myflow.api.app import create_app


def test_workflow_endpoint_runs_rag_query_step() -> None:
    client = TestClient(create_app())

    response = client.post(
        "/api/workflows/run",
        json={
            "workflow_id": "wf-001",
            "steps": [
                {
                    "kind": "rag_query",
                    "payload": {
                        "question": "测试问题",
                        "knowledge_base_ids": ["kb-local"],
                    },
                }
            ],
        },
    )

    assert response.status_code == 200
    assert response.json()["status"] == "completed"
