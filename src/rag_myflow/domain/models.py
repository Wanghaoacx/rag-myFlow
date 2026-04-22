from pydantic import BaseModel


class Workspace(BaseModel):
    slug: str
    name: str


class KnowledgeBase(BaseModel):
    slug: str
    title: str


class DocumentRecord(BaseModel):
    document_id: str
    knowledge_base_id: str = "kb-local"
    file_name: str
    mime_type: str
    chunk_count: int = 0
    preview_text: str | None = None


class DocumentChunk(BaseModel):
    chunk_id: str
    document_id: str
    knowledge_base_id: str
    text: str


class ConversationRecord(BaseModel):
    conversation_id: str
    title: str
