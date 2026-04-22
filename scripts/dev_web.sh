#!/usr/bin/env bash
set -euo pipefail

cd web
npm run dev -- --host 127.0.0.1 --port 5173
