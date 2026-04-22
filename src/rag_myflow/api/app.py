from fastapi import FastAPI
from fastapi.exceptions import HTTPException as FastAPIHTTPException
from fastapi.responses import JSONResponse
from starlette.exceptions import HTTPException as StarletteHTTPException

from rag_myflow.agent.service import WorkflowService
from rag_myflow.api.routes.chat import create_chat_router
from rag_myflow.api.routes.documents import create_documents_router
from rag_myflow.api.routes.health import create_health_router
from rag_myflow.api.routes.workflows import create_workflows_router
from rag_myflow.config import AppConfig
from rag_myflow.ingest.service import IngestService
from rag_myflow.rag.service import RagService


def _build_http_error_payload(exc: StarletteHTTPException) -> dict[str, object]:
    if isinstance(exc.detail, dict):
        return exc.detail
    return {"detail": {"message": str(exc.detail)}}


def create_app(
    config: AppConfig | None = None,
    ingest_service: IngestService | None = None,
    rag_service: RagService | None = None,
    workflow_service: WorkflowService | None = None,
) -> FastAPI:
    app_config = config or AppConfig()
    document_service = ingest_service or IngestService()
    answer_service = rag_service or RagService()
    flow_service = workflow_service or WorkflowService(answer_service)

    app = FastAPI(title="rag-myFlow API")
    app.include_router(create_health_router(app_config))
    app.include_router(create_documents_router(document_service))
    app.include_router(create_chat_router(answer_service))
    app.include_router(create_workflows_router(flow_service))

    @app.exception_handler(StarletteHTTPException)
    async def http_exception_handler(_, exc: StarletteHTTPException) -> JSONResponse:
        return JSONResponse(status_code=exc.status_code, content=_build_http_error_payload(exc))

    @app.exception_handler(FastAPIHTTPException)
    async def fastapi_http_exception_handler(_, exc: FastAPIHTTPException) -> JSONResponse:
        return JSONResponse(status_code=exc.status_code, content=_build_http_error_payload(exc))

    return app
