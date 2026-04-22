import mimetypes

from fastapi import APIRouter, File, Form, HTTPException, UploadFile

from rag_myflow.ingest.models import IngestRequest
from rag_myflow.ingest.service import IngestService
from rag_myflow.ingest.validators import UnsupportedDocumentError


def _build_document_response(document) -> dict[str, str | int | None]:  # noqa: ANN001
    return {
        "document_id": document.document_id,
        "file_name": document.file_name,
        "mime_type": document.mime_type,
        "chunk_count": document.chunk_count,
        "preview_text": document.preview_text,
    }


def create_documents_router(service: IngestService) -> APIRouter:
    router = APIRouter()

    def build_ingest_request(
        file_name: str,
        mime_type: str | None,
        has_text_layer: bool,
        source_bytes: bytes | None = None,
    ) -> IngestRequest:
        normalized_mime_type = mime_type or mimetypes.guess_type(file_name)[0] or "application/octet-stream"
        return IngestRequest(
            file_name=file_name,
            mime_type=normalized_mime_type,
            has_text_layer=has_text_layer,
            source_bytes=source_bytes,
        )

    @router.post("/api/documents")
    def create_document(request: IngestRequest) -> dict[str, str | int | None]:
        try:
            document = service.ingest(request)
        except UnsupportedDocumentError as exc:
            raise HTTPException(status_code=415, detail={"code": exc.code, "message": exc.message}) from exc

        return _build_document_response(document)

    @router.post("/api/documents/upload")
    async def upload_document(
        file: UploadFile = File(...),
        has_text_layer: bool = Form(...),
    ) -> dict[str, str | int | None]:
        try:
            source_bytes = await file.read()
            request = build_ingest_request(
                file.filename or "uploaded-file",
                file.content_type,
                has_text_layer,
                source_bytes=source_bytes,
            )
            document = service.ingest(request)
        except UnsupportedDocumentError as exc:
            raise HTTPException(status_code=415, detail={"code": exc.code, "message": exc.message}) from exc
        finally:
            await file.close()

        return _build_document_response(document)

    return router
