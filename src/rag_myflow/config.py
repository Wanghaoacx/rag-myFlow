from enum import Enum

from pydantic import BaseModel


class OcrPolicy(str, Enum):
    REJECT = "reject"


class AppConfig(BaseModel):
    workspace_slug: str = "local"
    workspace_name: str = "My Workspace"
    default_knowledge_base_id: str = "kb-local"
    ocr_policy: OcrPolicy = OcrPolicy.REJECT
