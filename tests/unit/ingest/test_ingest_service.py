from rag_myflow.ingest.models import IngestRequest
from rag_myflow.ingest.service import IngestService


def test_ingest_service_extracts_text_content_into_preview_and_chunk() -> None:
    service = IngestService()

    result = service.ingest(
        IngestRequest(
            file_name="notes.txt",
            mime_type="text/plain",
            has_text_layer=True,
            source_bytes="rag-myFlow 删除了用户、登录和 OCR 模块。".encode("utf-8"),
        )
    )

    assert result.chunk_count == 1
    assert "用户、登录和 OCR 模块" in (result.preview_text or "")
