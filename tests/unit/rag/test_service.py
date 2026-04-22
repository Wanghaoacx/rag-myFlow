from rag_myflow.rag.models import RagAnswerRequest
from rag_myflow.ingest.models import IngestRequest
from rag_myflow.ingest.service import IngestService
from rag_myflow.rag.service import RagService


def test_rag_service_returns_answer_with_citations() -> None:
    service = RagService()

    result = service.answer(
        RagAnswerRequest(
            question="rag-myFlow 删除了什么能力？",
            knowledge_base_ids=["kb-local"],
        )
    )

    assert result.answer == "当前知识库还没有匹配的文本内容。"
    assert result.citations == []


def test_rag_service_prefers_uploaded_text_chunk() -> None:
    ingest_service = IngestService()
    ingest_service.ingest(
        IngestRequest(
            file_name="notes.txt",
            mime_type="text/plain",
            has_text_layer=True,
            source_bytes="rag-myFlow 删除了用户、登录和 OCR 模块。".encode("utf-8"),
        )
    )
    service = RagService(store=ingest_service.store)

    result = service.answer(
        RagAnswerRequest(
            question="rag-myFlow 删除了什么模块？",
            knowledge_base_ids=["kb-local"],
        )
    )

    assert "用户、登录和 OCR 模块" in result.citations[0].snippet
