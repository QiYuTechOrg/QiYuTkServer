#!/usr/bin/env bash

set -e

exec /usr/local/bin/gunicorn -b 0.0.0.0:8002 -w 2 -k uvicorn.workers.UvicornWorker tbk.asgi:app
