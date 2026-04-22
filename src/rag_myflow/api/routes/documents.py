from fastapi import APIRouter, HTTPException

from rag_myflow.ingest.models import IngestRequest
from rag_myflow.ingest.service import IngestService
from rag_myflow.ingest.validators import UnsupportedDocumentError


def create_documents_router(service: IngestService) -> APIRouter:
    router = APIRouter()

    @router.post("/api/documents")
    def create_document(request: IngestRequest) -> dict[str, str]:
        try:
            document = service.ingest(request)
        except UnsupportedDocumentError as exc:
            raise HTTPException(status_code=415, detail={"code": exc.code, "message": exc.message}) from exc

        return {
            "document_id": document.document_id,
            "file_name": document.file_name,
            "mime_type": document.mime_type,
        }

    return router
