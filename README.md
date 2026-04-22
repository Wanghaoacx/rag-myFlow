# rag-myFlow

一个基于 RAGFlow 能力提取思路构建的单用户本地 RAG 系统。

## 当前目标

- 删除用户、登录、权限、租户相关能力
- 删除 OCR 模型与 OCR 解析链路
- 保留知识库、检索对话、工作流和模型设置主路径

## 本地开发

### 后端

```bash
uv sync --extra dev
bash scripts/dev_backend.sh
```

### 前端

```bash
cd web
npm install
bash ../scripts/dev_web.sh
```
