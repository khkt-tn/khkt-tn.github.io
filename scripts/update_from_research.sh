#!/usr/bin/env bash
set -euo pipefail

SITE_ROOT=$(cd "$(dirname "$0")/.." && pwd)
cd "$SITE_ROOT"

python scripts/sync_research_diary.py
python scripts/build_journal_index.py
python scripts/validate_site.py
git status --short --branch
