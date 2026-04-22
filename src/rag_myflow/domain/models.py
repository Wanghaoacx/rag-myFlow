from pydantic import BaseModel


class Workspace(BaseModel):
    slug: str
    name: str


class KnowledgeBase(BaseModel):
    slug: str
    title: str


class DocumentRecord(BaseModel):
    document_id: str
    file_name: str
    mime_type: str


class ConversationRecord(BaseModel):
    conversation_id: str
    title: str
