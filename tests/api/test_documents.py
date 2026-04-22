from fastapi.testclient import TestClient

from rag_myflow.api.app import create_app
from rag_myflow.domain.models import DocumentRecord


def test_document_endpoint_rejects_png_upload() -> None:
    client = TestClient(create_app())

    response = client.post(
        "/api/documents",
        json={"file_name": "scan.png", "mime_type": "image/png", "has_text_layer": False},
    )

    assert response.status_code == 415
    assert response.json()["code"] == "ocr_removed"


def test_document_endpoint_uses_injected_ingest_service() -> None:
    class StubIngestService:
        def ingest(self, request):  # noqa: ANN001
            return DocumentRecord(
                document_id="doc-123",
                file_name=request.file_name,
                mime_type="application/pdf",
            )

    client = TestClient(create_app(ingest_service=StubIngestService()))

    response = client.post(
        "/api/documents",
        json={"file_name": "guide.pdf", "mime_type": "application/pdf", "has_text_layer": True},
    )

    assert response.status_code == 200
    assert response.json() == {
        "document_id": "doc-123",
        "file_name": "guide.pdf",
        "mime_type": "application/pdf",
    }


def test_document_upload_endpoint_accepts_pdf_file() -> None:
    client = TestClient(create_app())

    response = client.post(
        "/api/documents/upload",
        data={"has_text_layer": "true"},
        files={"file": ("guide.pdf", b"%PDF-1.4", "application/pdf")},
    )

    assert response.status_code == 200
    assert response.json()["file_name"] == "guide.pdf"
    assert response.json()["mime_type"] == "application/pdf"


def test_document_upload_endpoint_rejects_ocr_only_png() -> None:
    client = TestClient(create_app())

    response = client.post(
        "/api/documents/upload",
        data={"has_text_layer": "false"},
        files={"file": ("scan.png", b"fake-png", "image/png")},
    )

    assert response.status_code == 415
    assert response.json()["code"] == "ocr_removed"


def test_http_exception_detail_uses_unified_shape() -> None:
    from fastapi import HTTPException
    from starlette.exceptions import HTTPException as StarletteHTTPException

    app = create_app()

    @app.get("/api/boom-fastapi")
    def boom_fastapi() -> None:
        raise HTTPException(status_code=400, detail="boom")

    @app.get("/api/boom-starlette")
    def boom_starlette() -> None:
        raise StarletteHTTPException(status_code=400, detail="boom")

    client = TestClient(app)

    fastapi_response = client.get("/api/boom-fastapi")
    starlette_response = client.get("/api/boom-starlette")

    assert fastapi_response.status_code == 400
    assert fastapi_response.json() == {"detail": {"message": "boom"}}
    assert starlette_response.status_code == 400
    assert starlette_response.json() == {"detail": {"message": "boom"}}
