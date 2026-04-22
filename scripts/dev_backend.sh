#!/usr/bin/env bash
set -euo pipefail

uv run uvicorn rag_myflow.api.app:create_app --factory --reload --host 127.0.0.1 --port 8000
