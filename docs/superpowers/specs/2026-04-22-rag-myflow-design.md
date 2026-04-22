# rag-myFlow Design

Date: 2026-04-22
Status: Written for user review

## 1. Goal

Build `rag-myFlow` as a single-user local knowledge system inspired by RAGFlow, but not as a direct forked UI-preserving trim. The project should extract and reorganize the core RAG capabilities into a smaller codebase that is easier to run and evolve in source-development mode.

The first version should:

- Keep the main product capabilities: knowledge base management, document import and parsing, chunking and indexing, retrieval and chat, workflow or agent execution, model configuration, and system settings.
- Remove all user, registration, login, authentication, tenant, organization, membership, and permission features.
- Remove all OCR-related models, OCR task chains, OCR configuration, and OCR UI entry points.
- Prefer explicit unsupported behavior over silent degradation when an OCR-dependent input is encountered.
- Use a lightweight new frontend focused on the user's high-frequency paths rather than preserving the upstream UI.

## 2. Product Scope

### In Scope

- Single local workspace only
- Source-code-first development workflow
- New lightweight web UI covering:
  - knowledge base and document management
  - retrieval chat
  - workflow or agent operations
  - model and system settings
- Reuse of mature RAGFlow parsing, retrieval, and orchestration capabilities where they fit the new architecture
- New single-user API layer with simplified contracts

### Out of Scope

- Preserving the current RAGFlow UI
- Full compatibility with upstream API contracts
- Multi-user, multi-tenant, RBAC, or team management
- Login shells or placeholder authentication modules
- OCR support of any kind
- Full preservation of upstream deployment matrix

## 3. Architecture

`rag-myFlow` should be organized as a capability-extraction project with five top-level modules.

### 3.1 `core-ingest`

Responsibilities:

- document import
- format parsing
- chunk generation
- embedding calls
- index construction

Notes:

- Reuse upstream ingestion and parsing logic selectively.
- Keep only non-OCR parsing paths, such as plain text, Office documents, PDF text layer, and web content.
- Reject scanned PDFs, image-only files, and other OCR-dependent inputs at the ingestion boundary.

### 3.2 `core-rag`

Responsibilities:

- retrieval
- reranking
- citation assembly
- context packaging
- answer generation orchestration

Notes:

- This module becomes the shared retrieval service for chat and workflow execution.
- No user, tenant, or permission filtering should remain in retrieval calls.

### 3.3 `core-agent`

Responsibilities:

- workflow definitions
- agent execution
- run-state persistence
- integration with retrieval and model services

Notes:

- Keep the main workflow or agent value path.
- Do not require the full upstream advanced agent feature surface in v1.
- Reuse `core-rag` instead of introducing a separate workflow-only retrieval path.

### 3.4 `app-api`

Responsibilities:

- expose the new single-user API
- translate UI actions into internal service calls
- inject fixed local context when reused upstream code still expects identity-like fields

Notes:

- External API contracts should be rewritten for single-user operation.
- Clients should not send login tokens, user IDs, tenant IDs, or permission context.

### 3.5 `app-web`

Responsibilities:

- provide the new lightweight frontend
- expose only the high-frequency user paths

Notes:

- The frontend is task-oriented, not upstream-compatible.
- It should optimize for short paths and local solo usage.

## 4. Data Model

The data model should be reduced from multi-user resources to single-workspace resources.

### Core entities

- `workspace`: the only local workspace, replacing user and tenant context
- `knowledge_base`: knowledge base definition and retrieval defaults
- `document`: imported source file or remote content record
- `chunk`: parsed and indexed document segments with source traceability
- `conversation`: chat session container
- `message`: message history in a conversation
- `workflow`: workflow or agent definition
- `agent_run`: workflow execution record
- `model_profile`: LLM, embedding, reranker, and related model configuration
- `system_setting`: local runtime and indexing settings

### Data-model rules

- All resources belong to the single default `workspace`.
- No owner, tenant, member, or permission tables should remain as active domain concepts.
- If reused upstream code still references those fields internally, that dependency should be eliminated during implementation rather than exposed as part of the new design.

## 5. Key Data Flows

### 5.1 Document ingestion

`upload or import -> parse -> chunk -> embed -> index -> ready`

Behavior rules:

- OCR-dependent documents fail fast with a clear unsupported error.
- Unsupported inputs must not silently skip parsing or produce incomplete indexing results.

### 5.2 Retrieval chat

`question -> retrieve -> rerank -> assemble context -> call model -> answer with citations`

Behavior rules:

- Retrieval scope is controlled by selected knowledge bases and chat configuration only.
- No tenant or permission filtering remains in this flow.

### 5.3 Workflow or agent execution

`workflow step -> call rag service, tools, or model -> persist run state -> return output`

Behavior rules:

- Workflow retrieval reuses the same `core-rag` interfaces as chat.
- Deleted capabilities must fail explicitly if referenced.

### 5.4 Settings updates

`UI or API update -> validate -> persist config -> hot reload or apply on next run`

Behavior rules:

- Model and system settings are managed through one coherent configuration surface.
- There is no split between user-level and system-level settings.

## 6. API Design Principles

- Build a new single-user API rather than inheriting upstream auth-oriented contracts.
- Keep public APIs simple and local-first.
- Hide any temporary internal compatibility shims inside `app-api`.
- Do not expose user, session, organization, tenant, or permission concepts externally.

## 7. Error Handling

The project should prefer explicit failure over hidden fallback.

### Required behaviors

- OCR-dependent document input returns a clear "unsupported because OCR has been removed" error.
- Residual permission or tenant dependencies discovered during implementation are treated as architecture issues to remove, not permanent runtime branches to preserve.
- Workflow nodes that depend on removed features return clear unsupported errors in both API and UI.

## 8. Testing Strategy

### Unit tests

- single-user context substitution behavior
- non-OCR ingestion validation
- retrieval and citation core logic

### Integration tests

- document import to indexed retrieval chat
- workflow or agent execution using retrieval
- settings update affecting later runs

### Regression tests

- system boot without login, user, or tenant modules
- successful completion of main high-frequency flows
- stable explicit failure for scanned PDFs, images, or OCR-only inputs

## 9. Delivery Boundaries for V1

V1 should include:

- extracted backend core modules
- new single-user API layer
- lightweight frontend
- source-development startup scripts
- minimal project documentation

V1 should not include:

- upstream UI preservation
- auth compatibility shells
- OCR placeholders
- full upstream deployment compatibility

## 10. Confirmed Decisions

These decisions were confirmed during brainstorming:

- Single-user only
- No login
- Architecture-level removal of auth and OCR, not only feature-level hiding
- Source development is the primary operating mode
- Existing upstream UI does not need to be preserved
- A lightweight frontend covering the high-frequency paths is acceptable

## 11. Implementation Direction

The implementation plan should assume a phased extraction approach:

1. identify reusable upstream capability slices
2. define the new single-user API and domain model
3. extract and adapt ingestion, retrieval, and workflow cores
4. build the lightweight frontend on the new API
5. add verification coverage for the supported and unsupported paths

This design is intentionally strict about removing multi-user and OCR concepts at the architectural level so that `rag-myFlow` remains maintainable as a personal source-driven system instead of a partially disabled enterprise product.
