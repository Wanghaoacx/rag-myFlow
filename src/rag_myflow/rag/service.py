import re

from rag_myflow.domain.models import DocumentChunk
from rag_myflow.domain.store import InMemoryDocumentStore
from rag_myflow.rag.models import Citation, RagAnswerRequest, RagAnswerResult


TOKEN_PATTERN = re.compile(r"[a-z0-9_]+|[\u4e00-\u9fff]", re.IGNORECASE)


class RagService:
    def __init__(self, store: InMemoryDocumentStore | None = None) -> None:
        self.store = store or InMemoryDocumentStore()

    def answer(self, request: RagAnswerRequest) -> RagAnswerResult:
        citation = self._build_citation(request)
        if citation is None:
            return RagAnswerResult(
                answer="当前知识库还没有匹配的文本内容。",
                citations=[],
            )

        return RagAnswerResult(
            answer=f"基于知识库 {', '.join(request.knowledge_base_ids)} 的结果：{citation.snippet}",
            citations=[citation],
        )

    def _build_citation(self, request: RagAnswerRequest) -> Citation | None:
        matched_chunk = self._select_chunk(request.question, self.store.list_chunks(request.knowledge_base_ids))
        if matched_chunk is None:
            return None

        return Citation(
            document_id=matched_chunk.document_id,
            chunk_id=matched_chunk.chunk_id,
            snippet=self._build_snippet(matched_chunk.text),
        )

    def _select_chunk(self, question: str, chunks: list[DocumentChunk]) -> DocumentChunk | None:
        if not chunks:
            return None

        question_tokens = self._tokenize(question)
        scored_chunks = [
            (self._score_chunk(question_tokens, chunk.text), index, chunk)
            for index, chunk in enumerate(chunks)
        ]
        best_score, _, best_chunk = max(scored_chunks, key=lambda item: (item[0], item[1]))
        if best_score <= 0:
            return None
        return best_chunk

    def _score_chunk(self, question_tokens: list[str], chunk_text: str) -> int:
        normalized_text = chunk_text.lower()
        return sum(1 for token in question_tokens if token in normalized_text)

    def _tokenize(self, text: str) -> list[str]:
        return TOKEN_PATTERN.findall(text.lower())

    def _build_snippet(self, text: str) -> str:
        snippet = " ".join(text.split())
        if len(snippet) <= 160:
            return snippet
        return f"{snippet[:160].rstrip()}..."
