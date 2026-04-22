import pytest
from pydantic import ValidationError

from rag_myflow.ingest.models import IngestRequest
from rag_myflow.ingest.validators import UnsupportedDocumentError, validate_document


def test_validate_document_accepts_text_pdf() -> None:
    request = IngestRequest(
        file_name="report.pdf",
        mime_type="application/pdf",
        has_text_layer=True,
    )

    result = validate_document(request)

    assert result.normalized_mime_type == "application/pdf"


def test_validate_document_rejects_scanned_pdf_without_text_layer() -> None:
    request = IngestRequest(
        file_name="scan.pdf",
        mime_type="application/pdf",
        has_text_layer=False,
    )

    with pytest.raises(UnsupportedDocumentError) as exc:
        validate_document(request)

    assert exc.value.code == "ocr_removed"


def test_validate_document_rejects_image_only_png() -> None:
    request = IngestRequest(
        file_name="scan.png",
        mime_type="image/png",
        has_text_layer=False,
    )

    with pytest.raises(UnsupportedDocumentError) as exc:
        validate_document(request)

    assert exc.value.code == "ocr_removed"


def test_validate_document_rejects_other_unsupported_type() -> None:
    request = IngestRequest(
        file_name="report.txt",
        mime_type="text/plain",
        has_text_layer=True,
    )

    with pytest.raises(UnsupportedDocumentError) as exc:
        validate_document(request)

    assert exc.value.code == "unsupported_type"


def test_validate_document_requires_text_layer_flag() -> None:
    with pytest.raises(ValidationError):
        IngestRequest(file_name="scan.pdf", mime_type="application/pdf")
