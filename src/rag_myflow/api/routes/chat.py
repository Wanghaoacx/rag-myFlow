from fastapi import APIRouter

from rag_myflow.rag.models import RagAnswerRequest
from rag_myflow.rag.service import RagService


def create_chat_router(service: RagService) -> APIRouter:
    router = APIRouter()

    @router.post("/api/chat/answer")
    def answer_question(request: RagAnswerRequest) -> dict:
        result = service.answer(request)
        return result.model_dump()

    return router
