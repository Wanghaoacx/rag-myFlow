from pydantic import BaseModel


class IngestRequest(BaseModel):
    file_name: str
    mime_type: str
    has_text_layer: bool
    source_bytes: bytes | None = None


class IngestValidationResult(BaseModel):
    normalized_mime_type: str
