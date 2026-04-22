import pytest

from rag_myflow.agent.models import WorkflowRunRequest, WorkflowStep
from rag_myflow.agent.service import UnsupportedWorkflowFeatureError, WorkflowService


def test_workflow_service_runs_rag_query_step() -> None:
    service = WorkflowService()
    request = WorkflowRunRequest(
        workflow_id="wf-001",
        steps=[
            WorkflowStep(
                kind="rag_query",
                payload={"question": "测试问题", "knowledge_base_ids": ["kb-local"]},
            )
        ],
    )

    result = service.run(request)

    assert result.status == "completed"
    assert result.outputs[0]["answer"].startswith("基于知识库")


def test_workflow_service_rejects_deleted_ocr_step() -> None:
    service = WorkflowService()
    request = WorkflowRunRequest(
        workflow_id="wf-002",
        steps=[WorkflowStep(kind="ocr_extract", payload={"file_name": "scan.pdf"})],
    )

    with pytest.raises(UnsupportedWorkflowFeatureError) as exc:
        service.run(request)

    assert exc.value.code == "removed_feature"
