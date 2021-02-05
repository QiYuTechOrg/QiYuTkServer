#!/usr/bin/env bash

set -e

exec /usr/local/bin/uvicorn tbk.asgi:app --host 0.0.0.0 --port 8002
