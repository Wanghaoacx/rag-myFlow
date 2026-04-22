from pydantic import BaseModel


class Citation(BaseModel):
    document_id: str
    chunk_id: str
    snippet: str


class RagAnswerRequest(BaseModel):
    question: str
    knowledge_base_ids: list[str]


class RagAnswerResult(BaseModel):
    answer: str
    citations: list[Citation]
