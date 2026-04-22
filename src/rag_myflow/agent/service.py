from dataclasses import dataclass

from rag_myflow.agent.models import WorkflowRunRequest, WorkflowRunResult
from rag_myflow.rag.models import RagAnswerRequest
from rag_myflow.rag.service import RagService


@dataclass
class UnsupportedWorkflowFeatureError(Exception):
    code: str
    message: str


class WorkflowService:
    def __init__(self, rag_service: RagService | None = None) -> None:
        self.rag_service = rag_service or RagService()

    def run(self, request: WorkflowRunRequest) -> WorkflowRunResult:
        outputs: list[dict] = []
        for step in request.steps:
            if step.kind == "rag_query":
                result = self.rag_service.answer(RagAnswerRequest(**step.payload))
                outputs.append(result.model_dump())
                continue

            raise UnsupportedWorkflowFeatureError(
                code="removed_feature",
                message=f"工作流步骤 {step.kind} 已从 rag-myFlow 中移除。",
            )

        return WorkflowRunResult(status="completed", outputs=outputs)
