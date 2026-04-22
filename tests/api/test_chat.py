from fastapi.testclient import TestClient

from rag_myflow.api.app import create_app
from rag_myflow.domain.store import InMemoryDocumentStore
from rag_myflow.ingest.service import IngestService


def test_chat_endpoint_returns_answer_and_citations() -> None:
    client = TestClient(create_app())

    response = client.post(
        "/api/chat/answer",
        json={"question": "rag-myFlow 删除了什么能力？", "knowledge_base_ids": ["kb-local"]},
    )

    assert response.status_code == 200
    assert response.json()["citations"] == []


def test_chat_endpoint_shares_store_when_only_ingest_service_is_injected() -> None:
    client = TestClient(create_app(ingest_service=IngestService(store=InMemoryDocumentStore())))

    upload_response = client.post(
        "/api/documents/upload",
        data={"has_text_layer": "true"},
        files={"file": ("notes.txt", "rag-myFlow 删除了用户、登录和 OCR 模块。".encode("utf-8"), "text/plain")},
    )

    assert upload_response.status_code == 200

    response = client.post(
        "/api/chat/answer",
        json={"question": "rag-myFlow 删除了什么模块？", "knowledge_base_ids": ["kb-local"]},
    )

    assert response.status_code == 200
    assert "用户、登录和 OCR 模块" in response.json()["citations"][0]["snippet"]


def test_chat_endpoint_returns_empty_citations_when_question_has_no_match() -> None:
    client = TestClient(create_app())

    upload_response = client.post(
        "/api/documents/upload",
        data={"has_text_layer": "true"},
        files={"file": ("notes.txt", "rag-myFlow 删除了用户、登录和 OCR 模块。".encode("utf-8"), "text/plain")},
    )

    assert upload_response.status_code == 200

    response = client.post(
        "/api/chat/answer",
        json={"question": "今天天气怎么样？", "knowledge_base_ids": ["kb-local"]},
    )

    assert response.status_code == 200
    assert response.json()["citations"] == []


def test_chat_endpoint_returns_uploaded_text_as_citation() -> None:
    client = TestClient(create_app())

    upload_response = client.post(
        "/api/documents/upload",
        data={"has_text_layer": "true"},
        files={"file": ("notes.txt", "rag-myFlow 删除了用户、登录和 OCR 模块。".encode("utf-8"), "text/plain")},
    )

    assert upload_response.status_code == 200

    response = client.post(
        "/api/chat/answer",
        json={"question": "rag-myFlow 删除了什么模块？", "knowledge_base_ids": ["kb-local"]},
    )

    assert response.status_code == 200
    assert "用户、登录和 OCR 模块" in response.json()["citations"][0]["snippet"]
