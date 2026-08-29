#!/usr/bin/env python3
"""Build machine-readable and visual journal indexes from synchronized YAML."""

from __future__ import annotations

import html
import json
import re
from collections import Counter
from pathlib import Path
from typing import Any

import yaml


SITE_ROOT = Path(__file__).resolve().parents[1]
JOURNAL_ROOT = SITE_ROOT / "docs" / "journal"
OUTPUT_JSON = SITE_ROOT / "docs" / "assets" / "data" / "journal_index.json"
OUTPUT_PAGE = JOURNAL_ROOT / "index.md"
STATUS_ORDER = ["VERIFIED", "PARTIAL", "TO_VERIFY", "PLANNED"]
STATUS_LABELS = {
    "VERIFIED": "Đã xác minh",
    "PARTIAL": "Một phần",
    "TO_VERIFY": "Cần xác minh",
    "PLANNED": "Kế hoạch",
}


def parse_document(path: Path) -> tuple[dict[str, Any], str]:
    text = path.read_text(encoding="utf-8")
    if not text.startswith("---\n"):
        raise ValueError(f"Missing YAML front matter: {path}")
    parts = text.split("---\n", 2)
    if len(parts) != 3:
        raise ValueError(f"Invalid front matter: {path}")
    metadata = yaml.safe_load(parts[1])
    if not isinstance(metadata, dict):
        raise ValueError(f"Front matter is not a mapping: {path}")
    return metadata, parts[2]


def clean_markdown(text: str) -> str:
    text = re.sub(r"<[^>]+>", " ", text)
    text = re.sub(r"!\[([^\]]*)\]\([^)]+\)", r"\1", text)
    text = re.sub(r"\[([^\]]+)\]\([^)]+\)", r"\1", text)
    text = re.sub(r"[*_#>\x60]", "", text)
    return " ".join(text.split())


def objective_summary(body: str) -> str:
    match = re.search(
        r"^## 1\. Mục tiêu\s*$\n+(.*?)(?=^## 2\.)",
        body,
        flags=re.MULTILINE | re.DOTALL,
    )
    if not match:
        return ""
    paragraphs = [
        clean_markdown(part)
        for part in re.split(r"\n\s*\n", match.group(1))
        if clean_markdown(part)
    ]
    return paragraphs[0] if paragraphs else ""


def build() -> int:
    paths = sorted(JOURNAL_ROOT.glob("J*.md"))
    journals: list[dict[str, Any]] = []
    for path in paths:
        metadata, body = parse_document(path)
        record = {
            "journal_id": str(metadata["journal_id"]),
            "experiment_id": str(metadata["experiment_id"]),
            "title": str(metadata["title"]),
            "date": str(metadata["date"]),
            "status": str(metadata["status"]).upper(),
            "evidence_level": str(metadata["evidence_level"]),
            "last_updated": str(metadata["last_updated"]),
            "summary": objective_summary(body),
            "url": f"{path.stem}/",
        }
        journals.append(record)

    journals.sort(key=lambda row: row["journal_id"])
    counts = Counter(row["status"] for row in journals)
    payload = {
        "generated_from": "docs/journal YAML front matter",
        "count": len(journals),
        "status_counts": {
            status: counts.get(status, 0) for status in STATUS_ORDER
        },
        "journals": journals,
    }
    OUTPUT_JSON.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT_JSON.write_text(
        json.dumps(payload, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )

    cards = []
    for row in journals:
        status = row["status"]
        status_label = STATUS_LABELS.get(status, status)
        cards.append(
            f'<article class="journal-card" data-journal-card '
            f'data-status="{html.escape(status)}">'
            '<div class="journal-card__top">'
            f'<span class="journal-card__id">{html.escape(row["journal_id"])}</span>'
            f'<span class="status-badge status-{status.lower()}">'
            f'{html.escape(status_label)} · {html.escape(status)}</span>'
            "</div>"
            f'<h2><a href="{html.escape(row["url"])}">'
            f'{html.escape(row["title"])}</a></h2>'
            f'<p>{html.escape(row["summary"])}</p>'
            '<div class="journal-card__meta">'
            f'<span>{html.escape(row["date"])}</span>'
            f'<span>{html.escape(row["experiment_id"])}</span>'
            f'<span>Evidence: {html.escape(row["evidence_level"])}</span>'
            "</div>"
            f'<a class="card-link" href="{html.escape(row["url"])}" '
            f'aria-label="Đọc {html.escape(row["journal_id"])}">Đọc bài →</a>'
            "</article>"
        )

    page = """---
title: Nhật ký nghiên cứu
---

<section class="page-intro">
  <p class="eyebrow">J01 — J16</p>
  <h1>Nhật ký nghiên cứu</h1>
  <p>Mỗi bài ghi lại câu hỏi, phương pháp, quan sát, vấn đề, điều chỉnh và bằng chứng. Trạng thái được đọc trực tiếp từ YAML front matter của Markdown nguồn.</p>
</section>

<div class="journal-toolbar" role="group" aria-label="Lọc bài theo trạng thái">
  <button class="filter-button is-active" type="button" data-journal-filter="ALL" aria-pressed="true">Tất cả</button>
  <button class="filter-button" type="button" data-journal-filter="VERIFIED" aria-pressed="false">Verified</button>
  <button class="filter-button" type="button" data-journal-filter="PARTIAL" aria-pressed="false">Partial</button>
  <button class="filter-button" type="button" data-journal-filter="PLANNED" aria-pressed="false">Planned</button>
</div>

<p class="filter-result" data-filter-result aria-live="polite"></p>

<div class="journal-grid">
""" + "\n".join(cards) + """
</div>
"""
    OUTPUT_PAGE.write_text(page, encoding="utf-8")
    print(f"INDEX PASS: {len(journals)} journals, counts={dict(counts)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(build())
