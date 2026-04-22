from rag_myflow.domain.models import DocumentChunk, DocumentRecord


class InMemoryDocumentStore:
    def __init__(self) -> None:
        self._documents: dict[str, DocumentRecord] = {}
        self._chunks: list[DocumentChunk] = []

    def save_document(self, document: DocumentRecord, chunks: list[DocumentChunk]) -> None:
        self._documents[document.document_id] = document
        self._chunks = [chunk for chunk in self._chunks if chunk.document_id != document.document_id]
        self._chunks.extend(chunks)

    def list_chunks(self, knowledge_base_ids: list[str]) -> list[DocumentChunk]:
        if not knowledge_base_ids:
            return list(self._chunks)
        return [chunk for chunk in self._chunks if chunk.knowledge_base_id in knowledge_base_ids]
