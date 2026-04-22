from itertools import count
import re
from uuid import uuid4

from rag_myflow.domain.models import DocumentChunk, DocumentRecord
from rag_myflow.domain.store import InMemoryDocumentStore
from rag_myflow.ingest.models import IngestRequest
from rag_myflow.ingest.validators import validate_document


PREVIEW_LENGTH = 120
PDF_TEXT_PATTERN = re.compile(r"\((?P<text>(?:\\.|[^\\()])*)\)\s*Tj")
PDF_TEXT_ARRAY_PATTERN = re.compile(r"\[(?P<items>.*?)\]\s*TJ", re.DOTALL)
PDF_LITERAL_PATTERN = re.compile(r"\((?P<text>(?:\\.|[^\\()])*)\)")


class IngestService:
    def __init__(
        self,
        store: InMemoryDocumentStore | None = None,
        default_knowledge_base_id: str = "kb-local",
    ) -> None:
        self.store = store or InMemoryDocumentStore()
        self.default_knowledge_base_id = default_knowledge_base_id

    def ingest(self, request: IngestRequest) -> DocumentRecord:
        validation = validate_document(request)
        document_id = str(uuid4())
        extracted_text = self._extract_text(request, validation.normalized_mime_type)
        chunks = self._build_chunks(document_id, extracted_text)
        document = DocumentRecord(
            document_id=document_id,
            knowledge_base_id=self.default_knowledge_base_id,
            file_name=request.file_name,
            mime_type=validation.normalized_mime_type,
            chunk_count=len(chunks),
            preview_text=self._build_preview(extracted_text),
        )
        self.store.save_document(document, chunks)
        return document

    def _extract_text(self, request: IngestRequest, mime_type: str) -> str:
        if not request.source_bytes:
            return ""

        if mime_type == "application/pdf":
            return self._extract_pdf_text(request.source_bytes)

        return request.source_bytes.decode("utf-8-sig", errors="ignore").strip()

    def _build_chunks(self, document_id: str, text: str) -> list[DocumentChunk]:
        if not text:
            return []

        return [
            DocumentChunk(
                chunk_id=f"{document_id}-chunk-{index:03d}",
                document_id=document_id,
                knowledge_base_id=self.default_knowledge_base_id,
                text=chunk_text,
            )
            for index, chunk_text in self._iter_chunks(text)
        ]

    def _iter_chunks(self, text: str) -> list[tuple[int, str]]:
        lines = [line.strip() for line in text.splitlines() if line.strip()]
        normalized = "\n".join(lines) if lines else text.strip()
        if not normalized:
            return []

        return list(zip(count(1), [normalized], strict=False))

    def _build_preview(self, text: str) -> str | None:
        if not text:
            return None

        if len(text) <= PREVIEW_LENGTH:
            return text
        return f"{text[:PREVIEW_LENGTH].rstrip()}..."

    def _extract_pdf_text(self, source_bytes: bytes) -> str:
        pdf_text = source_bytes.decode("latin-1", errors="ignore")
        extracted_segments = [
            self._decode_pdf_literal(match.group("text"))
            for match in PDF_TEXT_PATTERN.finditer(pdf_text)
        ]

        for array_match in PDF_TEXT_ARRAY_PATTERN.finditer(pdf_text):
            extracted_segments.extend(
                self._decode_pdf_literal(item_match.group("text"))
                for item_match in PDF_LITERAL_PATTERN.finditer(array_match.group("items"))
            )

        cleaned_segments = [segment.strip() for segment in extracted_segments if segment.strip()]
        return "\n".join(cleaned_segments)

    def _decode_pdf_literal(self, value: str) -> str:
        replacements = {
            r"\(": "(",
            r"\)": ")",
            r"\\": "\\",
            r"\n": "\n",
            r"\r": "\r",
            r"\t": "\t",
        }
        decoded = value
        for original, replacement in replacements.items():
            decoded = decoded.replace(original, replacement)
        return decoded
