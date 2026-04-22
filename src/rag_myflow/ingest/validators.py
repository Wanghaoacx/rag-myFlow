from dataclasses import dataclass

from rag_myflow.ingest.models import IngestRequest, IngestValidationResult


OCR_ONLY_MIME_TYPES = {
    "image/png",
    "image/jpeg",
    "image/webp",
}

SUPPORTED_TEXT_MIME_TYPES = {
    "application/json",
    "text/csv",
    "text/markdown",
    "text/plain",
}


@dataclass
class UnsupportedDocumentError(Exception):
    code: str
    message: str


def validate_document(request: IngestRequest) -> IngestValidationResult:
    if request.mime_type == "application/pdf" and not request.has_text_layer:
        raise UnsupportedDocumentError(
            code="ocr_removed",
            message="扫描版 PDF 依赖 OCR，rag-myFlow 当前版本不支持。",
        )

    if request.mime_type in OCR_ONLY_MIME_TYPES:
        raise UnsupportedDocumentError(
            code="ocr_removed",
            message="该文件类型依赖 OCR，rag-myFlow 当前版本不支持。",
        )

    if request.mime_type not in {"application/pdf", *SUPPORTED_TEXT_MIME_TYPES}:
        raise UnsupportedDocumentError(
            code="unsupported_type",
            message=f"暂不支持的文件类型: {request.mime_type}",
        )

    return IngestValidationResult(normalized_mime_type=request.mime_type)
