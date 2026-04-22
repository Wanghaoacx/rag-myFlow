from rag_myflow.rag.models import RagAnswerRequest
from rag_myflow.rag.service import RagService


def test_rag_service_returns_answer_with_citations() -> None:
    service = RagService()

    result = service.answer(
        RagAnswerRequest(
            question="rag-myFlow 删除了什么能力？",
            knowledge_base_ids=["kb-local"],
        )
    )

    assert result.answer.startswith("基于知识库")
    assert result.citations[0].document_id == "doc-001"
