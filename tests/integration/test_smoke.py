from fastapi.testclient import TestClient

from rag_myflow.api.app import create_app


def test_smoke_health_endpoint_returns_ok() -> None:
    client = TestClient(create_app())

    health_response = client.get("/api/health")
    assert health_response.status_code == 200


def test_smoke_documents_endpoint_rejects_ocr_only_input() -> None:
    client = TestClient(create_app())

    response = client.post(
        "/api/documents",
        json={"file_name": "scan.png", "mime_type": "image/png", "has_text_layer": False},
    )

    assert response.status_code == 415
    assert response.json()["code"] == "ocr_removed"


def test_smoke_chat_endpoint_returns_citation() -> None:
    client = TestClient(create_app())

    chat_response = client.post(
        "/api/chat/answer",
        json={"question": "系统删除了哪些能力？", "knowledge_base_ids": ["kb-local"]},
    )

    assert chat_response.status_code == 200
    assert chat_response.json()["citations"][0]["chunk_id"] == "chunk-001"


def test_smoke_workflow_endpoint_completes_rag_query() -> None:
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
    assert response.json()["outputs"][0]["citations"][0]["document_id"] == "doc-001"
