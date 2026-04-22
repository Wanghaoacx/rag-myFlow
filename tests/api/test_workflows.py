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


def test_workflow_endpoint_uses_uploaded_text_chunk() -> None:
    client = TestClient(create_app())

    upload_response = client.post(
        "/api/documents/upload",
        data={"has_text_layer": "true"},
        files={"file": ("notes.txt", "rag-myFlow 删除了用户、登录和 OCR 模块。".encode("utf-8"), "text/plain")},
    )

    assert upload_response.status_code == 200

    response = client.post(
        "/api/workflows/run",
        json={
            "workflow_id": "wf-001",
            "steps": [
                {
                    "kind": "rag_query",
                    "payload": {
                        "question": "rag-myFlow 删除了什么模块？",
                        "knowledge_base_ids": ["kb-local"],
                    },
                }
            ],
        },
    )

    assert response.status_code == 200
    assert "用户、登录和 OCR 模块" in response.json()["outputs"][0]["citations"][0]["snippet"]
