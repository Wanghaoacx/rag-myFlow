from fastapi.testclient import TestClient

from rag_myflow.api.app import create_app
from rag_myflow.domain.models import DocumentRecord


def build_text_pdf_bytes(text: str) -> bytes:
    return f"""%PDF-1.4
1 0 obj
<< /Type /Catalog /Pages 2 0 R >>
endobj
2 0 obj
<< /Type /Pages /Count 1 /Kids [3 0 R] >>
endobj
3 0 obj
<< /Type /Page /Parent 2 0 R /MediaBox [0 0 300 144] /Contents 4 0 R /Resources << /Font << /F1 5 0 R >> >> >>
endobj
4 0 obj
<< /Length 55 >>
stream
BT
/F1 18 Tf
72 72 Td
({text}) Tj
ET
endstream
endobj
5 0 obj
<< /Type /Font /Subtype /Type1 /BaseFont /Helvetica >>
endobj
trailer
<< /Root 1 0 R >>
%%EOF
""".encode("utf-8")


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
                chunk_count=0,
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
        "chunk_count": 0,
        "preview_text": None,
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
    assert response.json()["chunk_count"] == 0


def test_document_upload_endpoint_extracts_plain_text_preview() -> None:
    client = TestClient(create_app())

    response = client.post(
        "/api/documents/upload",
        data={"has_text_layer": "true"},
        files={"file": ("notes.txt", "rag-myFlow 删除了用户、登录和 OCR 模块。".encode("utf-8"), "text/plain")},
    )

    assert response.status_code == 200
    assert response.json()["mime_type"] == "text/plain"
    assert response.json()["chunk_count"] == 1
    assert "用户、登录和 OCR 模块" in response.json()["preview_text"]


def test_document_upload_endpoint_extracts_text_layer_pdf_preview() -> None:
    client = TestClient(create_app())

    response = client.post(
        "/api/documents/upload",
        data={"has_text_layer": "true"},
        files={"file": ("guide.pdf", build_text_pdf_bytes("PDF text layer works"), "application/pdf")},
    )

    assert response.status_code == 200
    assert response.json()["mime_type"] == "application/pdf"
    assert response.json()["chunk_count"] == 1
    assert "PDF text layer works" in response.json()["preview_text"]


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
