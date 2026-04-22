import mimetypes

from fastapi import APIRouter, File, Form, HTTPException, UploadFile

from rag_myflow.ingest.models import IngestRequest
from rag_myflow.ingest.service import IngestService
from rag_myflow.ingest.validators import UnsupportedDocumentError


def create_documents_router(service: IngestService) -> APIRouter:
    router = APIRouter()

    def build_ingest_request(
        file_name: str,
        mime_type: str | None,
        has_text_layer: bool,
    ) -> IngestRequest:
        normalized_mime_type = mime_type or mimetypes.guess_type(file_name)[0] or "application/octet-stream"
        return IngestRequest(
            file_name=file_name,
            mime_type=normalized_mime_type,
            has_text_layer=has_text_layer,
        )

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

    @router.post("/api/documents/upload")
    async def upload_document(
        file: UploadFile = File(...),
        has_text_layer: bool = Form(...),
    ) -> dict[str, str]:
        request = build_ingest_request(file.filename or "uploaded-file", file.content_type, has_text_layer)
        try:
            document = service.ingest(request)
        except UnsupportedDocumentError as exc:
            raise HTTPException(status_code=415, detail={"code": exc.code, "message": exc.message}) from exc
        finally:
            await file.close()

        return {
            "document_id": document.document_id,
            "file_name": document.file_name,
            "mime_type": document.mime_type,
        }

    return router
