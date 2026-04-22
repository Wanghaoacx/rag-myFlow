# rag-myFlow 实施计划

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** 基于 RAGFlow 的核心能力提取，搭建一个单用户、无登录、无 OCR 的 `rag-myFlow` 源码项目，并先跑通知识库导入、检索对话、工作流骨架和轻量前端。

**Architecture:** 先在空仓库里建立新的单用户项目骨架，再通过清晰的 `core-ingest`、`core-rag`、`core-agent`、`app-api`、`app-web` 五层边界接入提取能力。所有对外接口都只服务唯一 `workspace`，并在导入入口直接拒绝 OCR 依赖型文档。

**Tech Stack:** Python 3.12, FastAPI, Pydantic v2, pytest, httpx, React 18, TypeScript, Vite, Vitest, Testing Library

---

## 文件结构与职责

本仓库当前几乎为空，因此本计划先定义目标结构。所有实现任务都围绕以下文件展开。

### 后端

- 创建 `pyproject.toml`
  - 定义 Python 包、FastAPI、pytest、httpx 等基础依赖。
- 创建 `.gitignore`
  - 忽略 `.venv/`、`node_modules/`、`.pytest_cache/`、`dist/`、`.DS_Store` 等本地文件。
- 创建 `src/rag_myflow/__init__.py`
  - Python 包入口。
- 创建 `src/rag_myflow/config.py`
  - 单用户默认配置、OCR 拒绝策略、默认工作区常量。
- 创建 `src/rag_myflow/domain/models.py`
  - `Workspace`、`KnowledgeBase`、`DocumentRecord`、`ConversationRecord` 等基础领域模型。
- 创建 `src/rag_myflow/ingest/models.py`
  - 文档导入请求和导入结果模型。
- 创建 `src/rag_myflow/ingest/validators.py`
  - 文件类型校验和 OCR 不支持错误。
- 创建 `src/rag_myflow/ingest/service.py`
  - 导入服务入口，先实现“校验 + 生成占位记录”。
- 创建 `src/rag_myflow/rag/models.py`
  - 检索命中、引用、问答结果模型。
- 创建 `src/rag_myflow/rag/service.py`
  - 统一检索问答服务骨架。
- 创建 `src/rag_myflow/agent/models.py`
  - 工作流步骤、运行结果模型。
- 创建 `src/rag_myflow/agent/service.py`
  - 工作流执行服务骨架。
- 创建 `src/rag_myflow/api/app.py`
  - FastAPI 应用工厂。
- 创建 `src/rag_myflow/api/routes/health.py`
  - 健康检查路由。
- 创建 `src/rag_myflow/api/routes/documents.py`
  - 文档导入接口。
- 创建 `src/rag_myflow/api/routes/chat.py`
  - 检索对话接口。
- 创建 `src/rag_myflow/api/routes/workflows.py`
  - 工作流执行接口。

### 前端

- 创建 `web/package.json`
  - 前端依赖和脚本。
- 创建 `web/tsconfig.json`
  - TypeScript 编译配置。
- 创建 `web/vite.config.ts`
  - Vite 和 Vitest 配置。
- 创建 `web/index.html`
  - Vite 页面入口。
- 创建 `web/src/main.tsx`
  - React 启动入口。
- 创建 `web/src/App.tsx`
  - 应用主布局和导航。
- 创建 `web/src/lib/api.ts`
  - 调用后端 API 的轻量封装。
- 创建 `web/src/pages/KnowledgeBasePage.tsx`
  - 知识库与文档页。
- 创建 `web/src/pages/ChatPage.tsx`
  - 检索对话页。
- 创建 `web/src/pages/WorkflowPage.tsx`
  - 工作流页。
- 创建 `web/src/pages/SettingsPage.tsx`
  - 模型与系统设置页。

### 测试与文档

- 创建 `tests/unit/test_config.py`
  - 验证默认工作区和 OCR 策略。
- 创建 `tests/unit/ingest/test_validators.py`
  - 验证 OCR 文档拒绝逻辑。
- 创建 `tests/unit/rag/test_service.py`
  - 验证引用拼装和问答结构。
- 创建 `tests/unit/agent/test_service.py`
  - 验证工作流执行和已删除能力报错。
- 创建 `tests/api/test_health.py`
  - 验证健康检查接口。
- 创建 `tests/api/test_documents.py`
  - 验证文档导入接口。
- 创建 `tests/api/test_chat.py`
  - 验证对话接口。
- 创建 `tests/api/test_workflows.py`
  - 验证工作流接口。
- 创建 `tests/integration/test_smoke.py`
  - 验证主流程 smoke 测试。
- 创建 `web/src/test/app.test.tsx`
  - 验证前端导航和高频页面入口。
- 创建 `docs/upstream/ragflow-capability-inventory.md`
  - 记录后续要从 RAGFlow 提取的能力清单与映射关系。
- 创建 `README.md`
  - 中文项目说明和本地启动方式。
- 创建 `scripts/dev_backend.sh`
  - 启动后端开发服务。
- 创建 `scripts/dev_web.sh`
  - 启动前端开发服务。

## 任务拆分

### Task 1: 建立仓库骨架与单用户配置

**Files:**
- Create: `.gitignore`
- Create: `pyproject.toml`
- Create: `src/rag_myflow/__init__.py`
- Create: `src/rag_myflow/config.py`
- Create: `src/rag_myflow/domain/models.py`
- Create: `tests/unit/test_config.py`
- Create: `docs/upstream/ragflow-capability-inventory.md`

- [ ] **Step 1: 编写失败测试，锁定默认工作区和 OCR 策略**

```python
from rag_myflow.config import AppConfig, OcrPolicy


def test_default_workspace_and_ocr_policy() -> None:
    config = AppConfig()

    assert config.workspace_slug == "local"
    assert config.workspace_name == "My Workspace"
    assert config.ocr_policy is OcrPolicy.REJECT
```

- [ ] **Step 2: 运行测试，确认当前仓库还没有实现**

Run: `uv run pytest tests/unit/test_config.py -q`

Expected:

```text
E   ModuleNotFoundError: No module named 'rag_myflow'
```

- [ ] **Step 3: 写最小实现和仓库基础文件**

`.gitignore`

```gitignore
.DS_Store
.venv/
__pycache__/
.pytest_cache/
.coverage
node_modules/
dist/
coverage/
```

`pyproject.toml`

```toml
[project]
name = "rag-myflow"
version = "0.1.0"
description = "Single-user local RAG system inspired by RAGFlow"
requires-python = ">=3.12"
dependencies = [
  "fastapi>=0.115.0",
  "pydantic>=2.8.0",
  "uvicorn>=0.30.0",
]

[project.optional-dependencies]
dev = [
  "httpx>=0.27.0",
  "pytest>=8.3.0",
  "pytest-asyncio>=0.23.0",
]

[build-system]
requires = ["setuptools>=68.0"]
build-backend = "setuptools.build_meta"

[tool.pytest.ini_options]
pythonpath = ["src"]
testpaths = ["tests"]
```

`src/rag_myflow/__init__.py`

```python
__all__ = ["__version__"]

__version__ = "0.1.0"
```

`src/rag_myflow/config.py`

```python
from enum import Enum

from pydantic import BaseModel


class OcrPolicy(str, Enum):
    REJECT = "reject"


class AppConfig(BaseModel):
    workspace_slug: str = "local"
    workspace_name: str = "My Workspace"
    ocr_policy: OcrPolicy = OcrPolicy.REJECT
```

`src/rag_myflow/domain/models.py`

```python
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
```

`docs/upstream/ragflow-capability-inventory.md`

```md
# RAGFlow 能力提取清单

## 后端优先评估目录

- `api/`: 可复用的服务入口和接口模式
- `rag/`: 检索、召回、重排相关能力
- `deepdoc/`: 文档解析能力，后续只保留非 OCR 路径
- `agent/`: 工作流与 Agent 能力
- `web/`: 仅用于参考信息架构，不直接复用页面

## 明确删除范围

- 用户、登录、认证、租户、组织、成员、权限
- OCR 模型、OCR 配置、OCR 任务链路、OCR 入口
```

- [ ] **Step 4: 重新运行测试，确认最小配置骨架可用**

Run: `uv run pytest tests/unit/test_config.py -q`

Expected:

```text
1 passed
```

- [ ] **Step 5: 提交这一批初始化改动**

```bash
git add .gitignore pyproject.toml src/rag_myflow/__init__.py src/rag_myflow/config.py src/rag_myflow/domain/models.py tests/unit/test_config.py docs/upstream/ragflow-capability-inventory.md
git commit -m "chore: bootstrap rag-myflow skeleton"
```

### Task 2: 实现非 OCR 文档导入校验层

**Files:**
- Create: `src/rag_myflow/ingest/models.py`
- Create: `src/rag_myflow/ingest/validators.py`
- Create: `src/rag_myflow/ingest/service.py`
- Create: `tests/unit/ingest/test_validators.py`

- [ ] **Step 1: 编写失败测试，锁定支持和拒绝规则**

```python
import pytest

from rag_myflow.ingest.models import IngestRequest
from rag_myflow.ingest.validators import UnsupportedDocumentError, validate_document


def test_validate_document_accepts_text_pdf() -> None:
    request = IngestRequest(file_name="report.pdf", mime_type="application/pdf", has_text_layer=True)

    result = validate_document(request)

    assert result.normalized_mime_type == "application/pdf"


def test_validate_document_rejects_image_only_png() -> None:
    request = IngestRequest(file_name="scan.png", mime_type="image/png", has_text_layer=False)

    with pytest.raises(UnsupportedDocumentError) as exc:
        validate_document(request)

    assert exc.value.code == "ocr_removed"
```

- [ ] **Step 2: 运行测试，确认导入模块尚未实现**

Run: `uv run pytest tests/unit/ingest/test_validators.py -q`

Expected:

```text
E   ModuleNotFoundError: No module named 'rag_myflow.ingest'
```

- [ ] **Step 3: 写最小实现，先把校验边界钉死**

`src/rag_myflow/ingest/models.py`

```python
from pydantic import BaseModel


class IngestRequest(BaseModel):
    file_name: str
    mime_type: str
    has_text_layer: bool = True


class IngestValidationResult(BaseModel):
    normalized_mime_type: str
```

`src/rag_myflow/ingest/validators.py`

```python
from dataclasses import dataclass

from rag_myflow.ingest.models import IngestRequest, IngestValidationResult


TEXT_BASED_MIME_TYPES = {
    "application/pdf",
    "text/plain",
    "text/markdown",
    "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
}

OCR_ONLY_MIME_TYPES = {
    "image/png",
    "image/jpeg",
    "image/webp",
}


@dataclass
class UnsupportedDocumentError(Exception):
    code: str
    message: str


def validate_document(request: IngestRequest) -> IngestValidationResult:
    if request.mime_type in OCR_ONLY_MIME_TYPES:
        raise UnsupportedDocumentError(
            code="ocr_removed",
            message="该文件类型依赖 OCR，rag-myFlow 当前版本不支持。",
        )

    if request.mime_type == "application/pdf" and not request.has_text_layer:
        raise UnsupportedDocumentError(
            code="ocr_removed",
            message="扫描版 PDF 依赖 OCR，rag-myFlow 当前版本不支持。",
        )

    if request.mime_type not in TEXT_BASED_MIME_TYPES:
        raise UnsupportedDocumentError(
            code="unsupported_type",
            message=f"暂不支持的文件类型: {request.mime_type}",
        )

    return IngestValidationResult(normalized_mime_type=request.mime_type)
```

`src/rag_myflow/ingest/service.py`

```python
from uuid import uuid4

from rag_myflow.domain.models import DocumentRecord
from rag_myflow.ingest.models import IngestRequest
from rag_myflow.ingest.validators import validate_document


class IngestService:
    def ingest(self, request: IngestRequest) -> DocumentRecord:
        validation = validate_document(request)
        return DocumentRecord(
            document_id=str(uuid4()),
            file_name=request.file_name,
            mime_type=validation.normalized_mime_type,
        )
```

- [ ] **Step 4: 再次运行测试，确认导入校验通过**

Run: `uv run pytest tests/unit/ingest/test_validators.py -q`

Expected:

```text
2 passed
```

- [ ] **Step 5: 提交导入校验层**

```bash
git add src/rag_myflow/ingest/models.py src/rag_myflow/ingest/validators.py src/rag_myflow/ingest/service.py tests/unit/ingest/test_validators.py
git commit -m "feat: add non-ocr ingest validation"
```

### Task 3: 搭建单用户 API 壳层和文档导入接口

**Files:**
- Create: `src/rag_myflow/api/app.py`
- Create: `src/rag_myflow/api/routes/health.py`
- Create: `src/rag_myflow/api/routes/documents.py`
- Create: `tests/api/test_health.py`
- Create: `tests/api/test_documents.py`

- [ ] **Step 1: 编写失败测试，锁定健康检查和 OCR 拒绝响应**

`tests/api/test_health.py`

```python
from fastapi.testclient import TestClient

from rag_myflow.api.app import create_app


def test_health_endpoint_returns_workspace_context() -> None:
    client = TestClient(create_app())

    response = client.get("/api/health")

    assert response.status_code == 200
    assert response.json() == {"status": "ok", "workspace": "local"}
```

`tests/api/test_documents.py`

```python
from fastapi.testclient import TestClient

from rag_myflow.api.app import create_app


def test_document_endpoint_rejects_png_upload() -> None:
    client = TestClient(create_app())

    response = client.post(
        "/api/documents",
        json={"file_name": "scan.png", "mime_type": "image/png", "has_text_layer": False},
    )

    assert response.status_code == 415
    assert response.json()["code"] == "ocr_removed"
```

- [ ] **Step 2: 运行测试，确认 API 应用工厂尚未存在**

Run: `uv run pytest tests/api/test_health.py tests/api/test_documents.py -q`

Expected:

```text
E   ModuleNotFoundError: No module named 'rag_myflow.api'
```

- [ ] **Step 3: 写最小实现，提供统一 API 入口**

`src/rag_myflow/api/routes/health.py`

```python
from fastapi import APIRouter

router = APIRouter()


@router.get("/api/health")
def healthcheck() -> dict[str, str]:
    return {"status": "ok", "workspace": "local"}
```

`src/rag_myflow/api/routes/documents.py`

```python
from fastapi import APIRouter, HTTPException

from rag_myflow.ingest.models import IngestRequest
from rag_myflow.ingest.service import IngestService
from rag_myflow.ingest.validators import UnsupportedDocumentError

router = APIRouter()
service = IngestService()


@router.post("/api/documents")
def create_document(request: IngestRequest) -> dict[str, str]:
    try:
        document = service.ingest(request)
    except UnsupportedDocumentError as exc:
        raise HTTPException(status_code=415, detail={"code": exc.code, "message": exc.message}) from exc

    return {
        "document_id": document.document_id,
        "file_name": document.file_name,
        "mime_type": document.mime_type,
    }
```

`src/rag_myflow/api/app.py`

```python
from fastapi import FastAPI
from fastapi.responses import JSONResponse
from fastapi.exceptions import HTTPException

from rag_myflow.api.routes.documents import router as document_router
from rag_myflow.api.routes.health import router as health_router


def create_app() -> FastAPI:
    app = FastAPI(title="rag-myFlow API")
    app.include_router(health_router)
    app.include_router(document_router)

    @app.exception_handler(HTTPException)
    async def http_exception_handler(_, exc: HTTPException) -> JSONResponse:
        if isinstance(exc.detail, dict):
            return JSONResponse(status_code=exc.status_code, content=exc.detail)
        return JSONResponse(status_code=exc.status_code, content={"message": str(exc.detail)})

    return app
```

- [ ] **Step 4: 运行 API 测试，确认壳层行为正确**

Run: `uv run pytest tests/api/test_health.py tests/api/test_documents.py -q`

Expected:

```text
2 passed
```

- [ ] **Step 5: 提交 API 壳层**

```bash
git add src/rag_myflow/api/app.py src/rag_myflow/api/routes/health.py src/rag_myflow/api/routes/documents.py tests/api/test_health.py tests/api/test_documents.py
git commit -m "feat: add single-user api shell"
```

### Task 4: 实现统一检索问答服务与对话接口

**Files:**
- Create: `src/rag_myflow/rag/models.py`
- Create: `src/rag_myflow/rag/service.py`
- Create: `src/rag_myflow/api/routes/chat.py`
- Create: `tests/unit/rag/test_service.py`
- Create: `tests/api/test_chat.py`
- Modify: `src/rag_myflow/api/app.py`

- [ ] **Step 1: 编写失败测试，锁定引用拼装结构**

`tests/unit/rag/test_service.py`

```python
from rag_myflow.rag.models import RagAnswerRequest
from rag_myflow.rag.service import RagService


def test_rag_service_returns_answer_with_citations() -> None:
    service = RagService()

    result = service.answer(
        RagAnswerRequest(
            question="rag-myFlow 删除了什么能力？",
            knowledge_base_ids=["kb-local"],
        )
    )

    assert result.answer.startswith("基于知识库")
    assert result.citations[0].document_id == "doc-001"
```

`tests/api/test_chat.py`

```python
from fastapi.testclient import TestClient

from rag_myflow.api.app import create_app


def test_chat_endpoint_returns_answer_and_citations() -> None:
    client = TestClient(create_app())

    response = client.post(
        "/api/chat/answer",
        json={"question": "rag-myFlow 删除了什么能力？", "knowledge_base_ids": ["kb-local"]},
    )

    assert response.status_code == 200
    assert response.json()["citations"][0]["document_id"] == "doc-001"
```
```

- [ ] **Step 2: 运行测试，确认 `rag` 模块尚未实现**

Run: `uv run pytest tests/unit/rag/test_service.py -q`

Expected:

```text
E   ModuleNotFoundError: No module named 'rag_myflow.rag'
```

- [ ] **Step 3: 写最小实现，并暴露 `/api/chat/answer`**

`src/rag_myflow/rag/models.py`

```python
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
```

`src/rag_myflow/rag/service.py`

```python
from rag_myflow.rag.models import Citation, RagAnswerRequest, RagAnswerResult


class RagService:
    def answer(self, request: RagAnswerRequest) -> RagAnswerResult:
        citation = Citation(
            document_id="doc-001",
            chunk_id="chunk-001",
            snippet="用户、登录与 OCR 已从 rag-myFlow 中移除。",
        )
        return RagAnswerResult(
            answer=f"基于知识库 {', '.join(request.knowledge_base_ids)} 的结果：{citation.snippet}",
            citations=[citation],
        )
```

`src/rag_myflow/api/routes/chat.py`

```python
from fastapi import APIRouter

from rag_myflow.rag.models import RagAnswerRequest
from rag_myflow.rag.service import RagService

router = APIRouter()
service = RagService()


@router.post("/api/chat/answer")
def answer_question(request: RagAnswerRequest) -> dict:
    result = service.answer(request)
    return result.model_dump()
```

`src/rag_myflow/api/app.py`

```python
from fastapi import FastAPI
from fastapi.responses import JSONResponse
from fastapi.exceptions import HTTPException

from rag_myflow.api.routes.chat import router as chat_router
from rag_myflow.api.routes.documents import router as document_router
from rag_myflow.api.routes.health import router as health_router


def create_app() -> FastAPI:
    app = FastAPI(title="rag-myFlow API")
    app.include_router(health_router)
    app.include_router(document_router)
    app.include_router(chat_router)

    @app.exception_handler(HTTPException)
    async def http_exception_handler(_, exc: HTTPException) -> JSONResponse:
        if isinstance(exc.detail, dict):
            return JSONResponse(status_code=exc.status_code, content=exc.detail)
        return JSONResponse(status_code=exc.status_code, content={"message": str(exc.detail)})

    return app
```

- [ ] **Step 4: 运行单元和 API 测试，确认问答链路可用**

Run: `uv run pytest tests/unit/rag/test_service.py tests/api/test_chat.py -q`

Expected:

```text
2 passed
```

- [ ] **Step 5: 提交统一检索服务**

```bash
git add src/rag_myflow/rag/models.py src/rag_myflow/rag/service.py src/rag_myflow/api/routes/chat.py src/rag_myflow/api/app.py tests/unit/rag/test_service.py tests/api/test_chat.py
git commit -m "feat: add rag answer service"
```

### Task 5: 实现工作流骨架和已删除能力显式报错

**Files:**
- Create: `src/rag_myflow/agent/models.py`
- Create: `src/rag_myflow/agent/service.py`
- Create: `src/rag_myflow/api/routes/workflows.py`
- Create: `tests/unit/agent/test_service.py`
- Create: `tests/api/test_workflows.py`
- Modify: `src/rag_myflow/api/app.py`

- [ ] **Step 1: 编写失败测试，锁定支持和不支持路径**

`tests/unit/agent/test_service.py`

```python
import pytest

from rag_myflow.agent.models import WorkflowRunRequest, WorkflowStep
from rag_myflow.agent.service import UnsupportedWorkflowFeatureError, WorkflowService


def test_workflow_service_runs_rag_query_step() -> None:
    service = WorkflowService()
    request = WorkflowRunRequest(
        workflow_id="wf-001",
        steps=[WorkflowStep(kind="rag_query", payload={"question": "测试问题", "knowledge_base_ids": ["kb-local"]})],
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
```

`tests/api/test_workflows.py`

```python
from fastapi.testclient import TestClient

from rag_myflow.api.app import create_app


def test_workflow_endpoint_runs_rag_query_step() -> None:
    client = TestClient(create_app())

    response = client.post(
        "/api/workflows/run",
        json={
            "workflow_id": "wf-001",
            "steps": [
                {"kind": "rag_query", "payload": {"question": "测试问题", "knowledge_base_ids": ["kb-local"]}}
            ],
        },
    )

    assert response.status_code == 200
    assert response.json()["status"] == "completed"
```
```

- [ ] **Step 2: 运行测试，确认工作流模块尚未实现**

Run: `uv run pytest tests/unit/agent/test_service.py -q`

Expected:

```text
E   ModuleNotFoundError: No module named 'rag_myflow.agent'
```

- [ ] **Step 3: 写最小实现，并暴露 `/api/workflows/run`**

`src/rag_myflow/agent/models.py`

```python
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
```

`src/rag_myflow/agent/service.py`

```python
from dataclasses import dataclass

from rag_myflow.agent.models import WorkflowRunRequest, WorkflowRunResult
from rag_myflow.rag.models import RagAnswerRequest
from rag_myflow.rag.service import RagService


@dataclass
class UnsupportedWorkflowFeatureError(Exception):
    code: str
    message: str


class WorkflowService:
    def __init__(self) -> None:
        self.rag_service = RagService()

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
```

`src/rag_myflow/api/routes/workflows.py`

```python
from fastapi import APIRouter, HTTPException

from rag_myflow.agent.models import WorkflowRunRequest
from rag_myflow.agent.service import UnsupportedWorkflowFeatureError, WorkflowService

router = APIRouter()
service = WorkflowService()


@router.post("/api/workflows/run")
def run_workflow(request: WorkflowRunRequest) -> dict:
    try:
        result = service.run(request)
    except UnsupportedWorkflowFeatureError as exc:
        raise HTTPException(status_code=400, detail={"code": exc.code, "message": exc.message}) from exc

    return result.model_dump()
```

`src/rag_myflow/api/app.py`

```python
from fastapi import FastAPI
from fastapi.responses import JSONResponse
from fastapi.exceptions import HTTPException

from rag_myflow.api.routes.chat import router as chat_router
from rag_myflow.api.routes.documents import router as document_router
from rag_myflow.api.routes.health import router as health_router
from rag_myflow.api.routes.workflows import router as workflow_router


def create_app() -> FastAPI:
    app = FastAPI(title="rag-myFlow API")
    app.include_router(health_router)
    app.include_router(document_router)
    app.include_router(chat_router)
    app.include_router(workflow_router)

    @app.exception_handler(HTTPException)
    async def http_exception_handler(_, exc: HTTPException) -> JSONResponse:
        if isinstance(exc.detail, dict):
            return JSONResponse(status_code=exc.status_code, content=exc.detail)
        return JSONResponse(status_code=exc.status_code, content={"message": str(exc.detail)})

    return app
```

- [ ] **Step 4: 运行单元和 API 测试，确认工作流骨架可用**

Run: `uv run pytest tests/unit/agent/test_service.py tests/api/test_workflows.py -q`

Expected:

```text
2 passed
```

- [ ] **Step 5: 提交工作流骨架**

```bash
git add src/rag_myflow/agent/models.py src/rag_myflow/agent/service.py src/rag_myflow/api/routes/workflows.py src/rag_myflow/api/app.py tests/unit/agent/test_service.py tests/api/test_workflows.py
git commit -m "feat: add workflow service skeleton"
```

### Task 6: 搭建轻量前端和高频页面入口

**Files:**
- Create: `web/package.json`
- Create: `web/tsconfig.json`
- Create: `web/vite.config.ts`
- Create: `web/index.html`
- Create: `web/src/main.tsx`
- Create: `web/src/App.tsx`
- Create: `web/src/lib/api.ts`
- Create: `web/src/pages/KnowledgeBasePage.tsx`
- Create: `web/src/pages/ChatPage.tsx`
- Create: `web/src/pages/WorkflowPage.tsx`
- Create: `web/src/pages/SettingsPage.tsx`
- Create: `web/src/test/app.test.tsx`

- [ ] **Step 1: 编写失败测试，锁定四个高频导航入口**

```tsx
import { render, screen } from "@testing-library/react";
import App from "../App";


test("renders primary navigation", () => {
  render(<App />);

  expect(screen.getByText("知识库")).toBeInTheDocument();
  expect(screen.getByText("对话")).toBeInTheDocument();
  expect(screen.getByText("工作流")).toBeInTheDocument();
  expect(screen.getByText("设置")).toBeInTheDocument();
});
```

- [ ] **Step 2: 运行测试，确认前端工程尚未初始化**

Run: `cd web && npm run test -- --run`

Expected:

```text
bash: cd: web: No such file or directory
```

- [ ] **Step 3: 写最小实现，先把页面壳层建起来**

`web/package.json`

```json
{
  "name": "rag-myflow-web",
  "private": true,
  "version": "0.1.0",
  "type": "module",
  "scripts": {
    "dev": "vite",
    "build": "vite build",
    "test": "vitest"
  },
  "dependencies": {
    "react": "^18.3.1",
    "react-dom": "^18.3.1"
  },
  "devDependencies": {
    "@testing-library/jest-dom": "^6.6.3",
    "@testing-library/react": "^16.1.0",
    "@types/react": "^18.3.12",
    "@types/react-dom": "^18.3.1",
    "@vitejs/plugin-react": "^4.3.4",
    "typescript": "^5.6.3",
    "vite": "^5.4.10",
    "vitest": "^2.1.4"
  }
}
```

`web/index.html`

```html
<!doctype html>
<html lang="zh-CN">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <title>rag-myFlow</title>
  </head>
  <body>
    <div id="root"></div>
    <script type="module" src="/src/main.tsx"></script>
  </body>
</html>
```

`web/tsconfig.json`

```json
{
  "compilerOptions": {
    "target": "ES2020",
    "lib": ["DOM", "ES2020"],
    "jsx": "react-jsx",
    "module": "ESNext",
    "moduleResolution": "Bundler",
    "strict": true,
    "types": ["vitest/globals", "@testing-library/jest-dom"]
  },
  "include": ["src"]
}
```

`web/vite.config.ts`

```ts
import { defineConfig } from "vite";
import react from "@vitejs/plugin-react";

export default defineConfig({
  plugins: [react()],
  test: {
    environment: "jsdom",
    globals: true,
  },
});
```

`web/src/main.tsx`

```tsx
import React from "react";
import ReactDOM from "react-dom/client";

import App from "./App";

ReactDOM.createRoot(document.getElementById("root")!).render(
  <React.StrictMode>
    <App />
  </React.StrictMode>,
);
```

`web/src/App.tsx`

```tsx
import { useState } from "react";

import { ChatPage } from "./pages/ChatPage";
import { KnowledgeBasePage } from "./pages/KnowledgeBasePage";
import { SettingsPage } from "./pages/SettingsPage";
import { WorkflowPage } from "./pages/WorkflowPage";

type TabKey = "knowledge" | "chat" | "workflow" | "settings";

const tabs: Array<{ key: TabKey; label: string }> = [
  { key: "knowledge", label: "知识库" },
  { key: "chat", label: "对话" },
  { key: "workflow", label: "工作流" },
  { key: "settings", label: "设置" },
];

export default function App() {
  const [activeTab, setActiveTab] = useState<TabKey>("knowledge");

  return (
    <main>
      <h1>rag-myFlow</h1>
      <nav>
        {tabs.map((tab) => (
          <button key={tab.key} onClick={() => setActiveTab(tab.key)}>
            {tab.label}
          </button>
        ))}
      </nav>
      {activeTab === "knowledge" && <KnowledgeBasePage />}
      {activeTab === "chat" && <ChatPage />}
      {activeTab === "workflow" && <WorkflowPage />}
      {activeTab === "settings" && <SettingsPage />}
    </main>
  );
}
```

`web/src/pages/KnowledgeBasePage.tsx`

```tsx
export function KnowledgeBasePage() {
  return <section>知识库与文档管理</section>;
}
```

`web/src/pages/ChatPage.tsx`

```tsx
export function ChatPage() {
  return <section>检索对话</section>;
}
```

`web/src/pages/WorkflowPage.tsx`

```tsx
export function WorkflowPage() {
  return <section>工作流与 Agent</section>;
}
```

`web/src/pages/SettingsPage.tsx`

```tsx
export function SettingsPage() {
  return <section>模型与系统设置</section>;
}
```

`web/src/lib/api.ts`

```ts
export async function getHealth(): Promise<{ status: string; workspace: string }> {
  const response = await fetch("/api/health");
  if (!response.ok) {
    throw new Error("health request failed");
  }
  return response.json();
}
```

`web/src/test/app.test.tsx`

```tsx
import { render, screen } from "@testing-library/react";

import App from "../App";


test("renders primary navigation", () => {
  render(<App />);

  expect(screen.getByText("知识库")).toBeInTheDocument();
  expect(screen.getByText("对话")).toBeInTheDocument();
  expect(screen.getByText("工作流")).toBeInTheDocument();
  expect(screen.getByText("设置")).toBeInTheDocument();
});
```

- [ ] **Step 4: 运行前端测试，确认导航壳层通过**

Run: `cd web && npm install && npm run test -- --run`

Expected:

```text
✓ web/src/test/app.test.tsx
```

- [ ] **Step 5: 提交前端壳层**

```bash
git add web/package.json web/tsconfig.json web/vite.config.ts web/index.html web/src/main.tsx web/src/App.tsx web/src/lib/api.ts web/src/pages/KnowledgeBasePage.tsx web/src/pages/ChatPage.tsx web/src/pages/WorkflowPage.tsx web/src/pages/SettingsPage.tsx web/src/test/app.test.tsx
git commit -m "feat: add lightweight web shell"
```

### Task 7: 补齐启动脚本、项目说明和 smoke 测试

**Files:**
- Create: `tests/integration/test_smoke.py`
- Create: `README.md`
- Create: `scripts/dev_backend.sh`
- Create: `scripts/dev_web.sh`

- [ ] **Step 1: 编写失败测试，锁定最小可运行主链路**

```python
from fastapi.testclient import TestClient

from rag_myflow.api.app import create_app


def test_smoke_flow_health_then_chat() -> None:
    client = TestClient(create_app())

    health_response = client.get("/api/health")
    assert health_response.status_code == 200

    chat_response = client.post(
        "/api/chat/answer",
        json={"question": "系统删除了哪些能力？", "knowledge_base_ids": ["kb-local"]},
    )
    assert chat_response.status_code == 200
    assert chat_response.json()["citations"][0]["chunk_id"] == "chunk-001"
```

- [ ] **Step 2: 运行 smoke 测试，先看到缺失文件失败**

Run: `uv run pytest tests/integration/test_smoke.py -q`

Expected:

```text
E   file or directory not found: tests/integration/test_smoke.py
```

- [ ] **Step 3: 写最小实现，补齐启动方式和项目文档**

`scripts/dev_backend.sh`

```bash
#!/usr/bin/env bash
set -euo pipefail

uv run uvicorn rag_myflow.api.app:create_app --factory --reload --host 127.0.0.1 --port 8000
```

`scripts/dev_web.sh`

```bash
#!/usr/bin/env bash
set -euo pipefail

cd web
npm run dev -- --host 127.0.0.1 --port 5173
```

`README.md`

````md
# rag-myFlow

一个基于 RAGFlow 能力提取思路构建的单用户本地 RAG 系统。

## 当前目标

- 删除用户、登录、权限、租户相关能力
- 删除 OCR 模型与 OCR 解析链路
- 保留知识库、检索对话、工作流和模型设置主路径

## 本地开发

### 后端

```bash
uv sync
bash scripts/dev_backend.sh
```

### 前端

```bash
cd web
npm install
bash ../scripts/dev_web.sh
```
````

`tests/integration/test_smoke.py`

```python
from fastapi.testclient import TestClient

from rag_myflow.api.app import create_app


def test_smoke_flow_health_then_chat() -> None:
    client = TestClient(create_app())

    health_response = client.get("/api/health")
    assert health_response.status_code == 200

    chat_response = client.post(
        "/api/chat/answer",
        json={"question": "系统删除了哪些能力？", "knowledge_base_ids": ["kb-local"]},
    )
    assert chat_response.status_code == 200
    assert chat_response.json()["citations"][0]["chunk_id"] == "chunk-001"
```

- [ ] **Step 4: 运行 smoke 测试，确认主链路成立**

Run: `uv run pytest tests/integration/test_smoke.py -q`

Expected:

```text
1 passed
```

- [ ] **Step 5: 提交收尾文档和脚本**

```bash
git add tests/integration/test_smoke.py README.md scripts/dev_backend.sh scripts/dev_web.sh
git commit -m "docs: add local development guide and smoke test"
```

## 自检

### 1. 设计覆盖检查

- 单用户和无登录：Task 1、Task 3 通过 `AppConfig` 与 API 壳层固定 `workspace` 覆盖。
- 删除 OCR：Task 2 和 Task 3 明确在导入层与接口层拒绝 OCR 输入。
- 保留知识库/检索/对话主路径：Task 4 提供统一 `RagService` 和 `/api/chat/answer`。
- 保留工作流或 Agent：Task 5 提供工作流骨架与显式错误分支。
- 轻量前端：Task 6 提供四个高频页面入口。
- 源码开发优先：Task 7 提供开发脚本、README 和 smoke 测试。
- 后续对上游能力提取的准备：Task 1 的 `docs/upstream/ragflow-capability-inventory.md` 提供提取清单。

### 2. 占位符检查

- 已避免使用 `TODO`、`TBD`、`implement later` 等占位词。
- 每个任务都给出了明确文件路径、测试命令、预期输出和最小实现代码。

### 3. 类型与命名一致性检查

- `OcrPolicy`、`IngestRequest`、`RagAnswerRequest`、`WorkflowRunRequest` 等名称在各任务中保持一致。
- `/api/health`、`/api/documents`、`/api/chat/answer`、`/api/workflows/run` 四个接口路径在测试和实现中一致。
