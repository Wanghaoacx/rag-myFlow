from fastapi.testclient import TestClient

from rag_myflow.api.app import create_app


def test_smoke_flow_health_then_chat() -> None:
    client = TestClient(create_app())

    health_response = client.get("/api/health")
    assert health_response.status_code == 200

    chat_response = client.post(
        "/api/chat/answer",
        json={"question": "系统删除了哪些能力？", "knowledge_base_ids": ["kb-local"]},
    )
    assert chat_response.status_code == 200
    assert chat_response.json()["citations"][0]["chunk_id"] == "chunk-001"
