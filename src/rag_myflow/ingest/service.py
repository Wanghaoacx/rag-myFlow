from uuid import uuid4

from rag_myflow.domain.models import DocumentRecord
from rag_myflow.ingest.models import IngestRequest
from rag_myflow.ingest.validators import validate_document


class IngestService:
    def ingest(self, request: IngestRequest) -> DocumentRecord:
        validation = validate_document(request)
        return DocumentRecord(
            document_id=str(uuid4()),
            file_name=request.file_name,
            mime_type=validation.normalized_mime_type,
        )

