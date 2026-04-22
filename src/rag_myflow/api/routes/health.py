from fastapi import APIRouter

from rag_myflow.config import AppConfig


def create_health_router(config: AppConfig) -> APIRouter:
    router = APIRouter()

    @router.get("/api/health")
    def healthcheck() -> dict[str, str]:
        return {"status": "ok", "workspace": config.workspace_slug}

    return router
