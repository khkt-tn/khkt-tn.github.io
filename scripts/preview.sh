#!/usr/bin/env bash
set -euo pipefail

SITE_ROOT=$(cd "$(dirname "$0")/.." && pwd)
cd "$SITE_ROOT"

exec python -m mkdocs serve --dev-addr 127.0.0.1:8000 "$@"
