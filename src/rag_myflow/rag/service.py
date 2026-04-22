from rag_myflow.rag.models import Citation, RagAnswerRequest, RagAnswerResult


class RagService:
    def answer(self, request: RagAnswerRequest) -> RagAnswerResult:
        citation = Citation(
            document_id="doc-001",
            chunk_id="chunk-001",
            snippet="用户、登录与 OCR 已从 rag-myFlow 中移除。",
        )
        return RagAnswerResult(
            answer=f"基于知识库 {', '.join(request.knowledge_base_ids)} 的结果：{citation.snippet}",
            citations=[citation],
        )
