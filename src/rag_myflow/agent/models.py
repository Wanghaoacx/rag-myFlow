from pydantic import BaseModel


class WorkflowStep(BaseModel):
    kind: str
    payload: dict


class WorkflowRunRequest(BaseModel):
    workflow_id: str
    steps: list[WorkflowStep]


class WorkflowRunResult(BaseModel):
    status: str
    outputs: list[dict]
