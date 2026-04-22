from fastapi import APIRouter, HTTPException

from rag_myflow.agent.models import WorkflowRunRequest
from rag_myflow.agent.service import UnsupportedWorkflowFeatureError, WorkflowService


def create_workflows_router(service: WorkflowService) -> APIRouter:
    router = APIRouter()

    @router.post("/api/workflows/run")
    def run_workflow(request: WorkflowRunRequest) -> dict:
        try:
            result = service.run(request)
        except UnsupportedWorkflowFeatureError as exc:
            raise HTTPException(status_code=400, detail={"code": exc.code, "message": exc.message}) from exc

        return result.model_dump()

    return router
