# rag-myFlow

一个基于 RAGFlow 能力提取思路构建的单用户本地 RAG 系统。

## 当前目标

- 删除用户、登录、权限、租户相关能力
- 删除 OCR 模型与 OCR 解析链路
- 保留知识库、检索对话、工作流和模型设置主路径

## 当前最小导入链路

- 已支持真实文本提取并进入检索的文件类型：`text/plain`、`text/markdown`、`text/csv`、`application/json`
- 图片、扫描件和无文本层 PDF 会被显式拒绝
- `application/pdf` 目前保留导入入口，但这一版还没有接入真正的 PDF 文本提取

## 本地开发

### 后端

```bash
uv sync --extra dev
bash scripts/dev_backend.sh
```

### 前端

```bash
cd web
npm ci
bash ../scripts/dev_web.sh
```
