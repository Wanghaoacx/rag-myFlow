from fastapi.testclient import TestClient

from rag_myflow.api.app import create_app


def test_chat_endpoint_returns_answer_and_citations() -> None:
    client = TestClient(create_app())

    response = client.post(
        "/api/chat/answer",
        json={"question": "rag-myFlow 删除了什么能力？", "knowledge_base_ids": ["kb-local"]},
    )

    assert response.status_code == 200
    assert response.json()["citations"][0]["document_id"] == "doc-001"
