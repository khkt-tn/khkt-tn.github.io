#!/usr/bin/env python3
"""Validate synchronized research content before publishing the MkDocs site."""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import sys
from datetime import date
from pathlib import Path
from typing import Any
from urllib.parse import unquote, urlsplit

import yaml


SITE_ROOT = Path(__file__).resolve().parents[1]
DOCS_ROOT = SITE_ROOT / "docs"
JOURNAL_ROOT = DOCS_ROOT / "journal"
EXPECTED_IDS = [f"J{number:02d}" for number in range(1, 14)]
EXPECTED_MEDIA_IDS = [
    "V01",
    "V02",
    "V03",
    "V04",
    "V05",
    "V06",
    "V07",
    "V08",
    "V10",
]
VALID_STATUSES = {"VERIFIED", "PARTIAL", "TO_VERIFY", "PLANNED"}
CUTOFF_DATE = date(2026, 8, 29)
LINK_PATTERN = re.compile(r"!?\[[^\]]*\]\(([^)]+)\)")
HTML_LINK_PATTERN = re.compile(r"""(?:href|src)=["']([^"']+)["']""")
SECRET_PATTERNS = {
    "private key": re.compile(r"-----BEGIN [A-Z ]*PRIVATE KEY-----"),
    "GitHub token": re.compile(r"\bgh[pousr]_[A-Za-z0-9_]{20,}\b"),
    "generic API secret": re.compile(
        r"(?i)\b(api[_ -]?key|access[_ -]?token|client[_ -]?secret)"
        r"\s*[:=]\s*['\x22][^'\x22]{12,}['\x22]"
    ),
}
TEXT_SUFFIXES = {
    ".md",
    ".yml",
    ".yaml",
    ".py",
    ".js",
    ".css",
    ".json",
    ".txt",
    ".sh",
}


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def parse_front_matter(path: Path) -> tuple[dict[str, Any], str]:
    text = path.read_text(encoding="utf-8")
    if not text.startswith("---\n"):
        raise ValueError("missing YAML front matter")
    parts = text.split("---\n", 2)
    if len(parts) != 3:
        raise ValueError("invalid YAML front matter boundary")
    metadata = yaml.safe_load(parts[1])
    if not isinstance(metadata, dict):
        raise ValueError("front matter is not a mapping")
    return metadata, parts[2]


def local_link_errors(path: Path, text: str) -> list[str]:
    errors: list[str] = []
    in_fence = False
    for line_number, line in enumerate(text.splitlines(), start=1):
        stripped = line.lstrip()
        if stripped.startswith("~~~") or stripped.startswith(chr(96) * 3):
            in_fence = not in_fence
            continue
        if in_fence:
            continue
        matches = [
            *(match.group(1) for match in LINK_PATTERN.finditer(line)),
            *(match.group(1) for match in HTML_LINK_PATTERN.finditer(line)),
        ]
        for raw_match in matches:
            raw_target = raw_match.strip().strip("<>")
            target = raw_target.split()[0]
            parsed = urlsplit(target)
            if parsed.scheme or target.startswith(("#", "mailto:")):
                continue
            local_path = unquote(parsed.path)
            if not local_path:
                continue
            if local_path.startswith("/"):
                resolved = (DOCS_ROOT / local_path.lstrip("/")).resolve()
            else:
                resolved = (path.parent / local_path).resolve()
            try:
                resolved.relative_to(DOCS_ROOT.resolve())
            except ValueError:
                errors.append(
                    f"{path.relative_to(SITE_ROOT)}:{line_number}: "
                    f"local link escapes docs: {target}"
                )
                continue
            route_candidates = [
                resolved,
                resolved.with_suffix(".md"),
                resolved / "index.md",
            ]
            if not any(candidate.exists() for candidate in route_candidates):
                errors.append(
                    f"{path.relative_to(SITE_ROOT)}:{line_number}: "
                    f"missing local target: {target}"
                )
    return errors


def validate(skip_source_check: bool) -> int:
    errors: list[str] = []
    warnings: list[str] = []
    journal_ids: list[str] = []
    status_counts = {status: 0 for status in sorted(VALID_STATUSES)}

    journal_paths = sorted(JOURNAL_ROOT.glob("J*.md"))
    for path in journal_paths:
        try:
            metadata, body = parse_front_matter(path)
        except (ValueError, yaml.YAMLError) as exc:
            errors.append(f"{path.relative_to(SITE_ROOT)}: {exc}")
            continue

        required = {
            "journal_id",
            "experiment_id",
            "title",
            "date",
            "status",
            "authors",
            "tags",
            "evidence_level",
            "last_updated",
        }
        missing = sorted(required - metadata.keys())
        if missing:
            errors.append(
                f"{path.relative_to(SITE_ROOT)}: missing fields {missing}"
            )

        journal_id = str(metadata.get("journal_id", ""))
        journal_ids.append(journal_id)
        expected_filename_id = path.stem.split("_", 1)[0]
        if journal_id != expected_filename_id:
            errors.append(
                f"{path.relative_to(SITE_ROOT)}: journal_id {journal_id!r} "
                f"does not match filename {expected_filename_id!r}"
            )

        status = str(metadata.get("status", "")).upper()
        if status not in VALID_STATUSES:
            errors.append(
                f"{path.relative_to(SITE_ROOT)}: invalid status {status!r}"
            )
        else:
            status_counts[status] += 1

        raw_date = str(metadata.get("date", ""))
        if raw_date != "TO_VERIFY":
            try:
                entry_date = date.fromisoformat(raw_date)
            except ValueError:
                errors.append(
                    f"{path.relative_to(SITE_ROOT)}: invalid date {raw_date!r}"
                )
            else:
                if status in {"VERIFIED", "PARTIAL"} and entry_date > CUTOFF_DATE:
                    errors.append(
                        f"{path.relative_to(SITE_ROOT)}: completed entry date "
                        f"{entry_date} is after cutoff {CUTOFF_DATE}"
                    )

        if "TODO_YOUTUBE_VIDEO_ID" in body or "TODO_YOUTUBE_URL" in body:
            errors.append(
                f"{path.relative_to(SITE_ROOT)}: raw YouTube placeholder leaked"
            )
        if "Đang chờ cập nhật" in body or "TODO_UPLOAD" in body:
            warnings.append(
                f"{path.relative_to(SITE_ROOT)}: media is waiting for update"
            )

    duplicates = sorted(
        journal_id
        for journal_id in set(journal_ids)
        if journal_ids.count(journal_id) > 1
    )
    if duplicates:
        errors.append(f"duplicate journal IDs: {duplicates}")
    if sorted(journal_ids) != EXPECTED_IDS:
        errors.append(
            f"journal set mismatch: expected {EXPECTED_IDS}, got "
            f"{sorted(journal_ids)}"
        )

    for path in sorted(DOCS_ROOT.rglob("*.md")):
        errors.extend(local_link_errors(path, path.read_text(encoding="utf-8")))

    media_path = DOCS_ROOT / "media.md"
    if not media_path.is_file():
        errors.append("missing docs/media.md")
    else:
        media_ids = re.findall(
            r"^\|\s*(V\d{2})\s*\|",
            media_path.read_text(encoding="utf-8"),
            flags=re.MULTILINE,
        )
        if media_ids != EXPECTED_MEDIA_IDS:
            errors.append(
                f"media set mismatch: expected {EXPECTED_MEDIA_IDS}, "
                f"got {media_ids}"
            )

    index_path = DOCS_ROOT / "assets" / "data" / "journal_index.json"
    if not index_path.is_file():
        errors.append("missing docs/assets/data/journal_index.json")
    else:
        try:
            index_payload = json.loads(index_path.read_text(encoding="utf-8"))
            indexed_ids = [
                str(row["journal_id"]) for row in index_payload["journals"]
            ]
            if indexed_ids != EXPECTED_IDS:
                errors.append(
                    f"journal index mismatch: expected {EXPECTED_IDS}, "
                    f"got {indexed_ids}"
                )
            if index_payload.get("status_counts") != {
                status: status_counts.get(status, 0)
                for status in ["VERIFIED", "PARTIAL", "TO_VERIFY", "PLANNED"]
            }:
                errors.append("journal index status counts do not match YAML")
        except (KeyError, TypeError, json.JSONDecodeError) as exc:
            errors.append(f"invalid journal index JSON: {exc}")

    sync_path = DOCS_ROOT / "assets" / "data" / "sync_report.json"
    if not sync_path.is_file():
        errors.append("missing docs/assets/data/sync_report.json")
    else:
        try:
            sync_payload = json.loads(sync_path.read_text(encoding="utf-8"))
            for record in sync_payload["source_files"]:
                destination = SITE_ROOT / record["destination"]
                if not destination.is_file():
                    errors.append(f"missing synchronized file: {destination}")
                elif sha256_file(destination) != record["destination_sha256"]:
                    errors.append(
                        f"synchronized destination changed: {destination}"
                    )

                if not skip_source_check:
                    source_project = (
                        SITE_ROOT / sync_payload["source_check_path"]
                    ).resolve()
                    source = source_project / record["source"]
                    if not source.is_file():
                        errors.append(f"missing scientific source: {source}")
                    elif sha256_file(source) != record["source_sha256"]:
                        errors.append(f"scientific source hash changed: {source}")
        except (KeyError, TypeError, json.JSONDecodeError) as exc:
            errors.append(f"invalid sync report JSON: {exc}")

    required_site_files = [
        SITE_ROOT / "mkdocs.yml",
        SITE_ROOT / ".github" / "workflows" / "pages.yml",
        DOCS_ROOT / "index.md",
        DOCS_ROOT / "assets" / "css" / "extra.css",
        DOCS_ROOT / "assets" / "js" / "extra.js",
    ]
    for path in required_site_files:
        if not path.is_file():
            errors.append(f"missing required site file: {path.relative_to(SITE_ROOT)}")

    ignored_parts = {".git", ".venv", "__pycache__", "site"}
    for path in sorted(SITE_ROOT.rglob("*")):
        if not path.is_file() or ignored_parts.intersection(path.parts):
            continue
        relative = path.relative_to(SITE_ROOT)
        if path.stat().st_size > 5 * 1024 * 1024:
            errors.append(f"unexpected file larger than 5 MiB: {relative}")
        if path.suffix.lower() not in TEXT_SUFFIXES:
            continue
        try:
            text = path.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            continue
        for label, pattern in SECRET_PATTERNS.items():
            if pattern.search(text):
                errors.append(f"possible {label} in {relative}")

    for warning in sorted(set(warnings)):
        print(f"WARNING: {warning}")
    if errors:
        for error in errors:
            print(f"ERROR: {error}", file=sys.stderr)
        print(
            f"VALIDATION FAIL: {len(errors)} error(s), "
            f"{len(set(warnings))} warning(s)",
            file=sys.stderr,
        )
        return 1

    print(
        "VALIDATION PASS: "
        f"{len(journal_paths)} journals; "
        + ", ".join(
            f"{status}={status_counts[status]}"
            for status in ["VERIFIED", "PARTIAL", "TO_VERIFY", "PLANNED"]
        )
        + f"; {len(set(warnings))} media warning(s)"
    )
    return 0


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--skip-source-check",
        action="store_true",
        help="Skip checks against local scientific source (for GitHub Actions).",
    )
    args = parser.parse_args()
    return validate(args.skip_source_check)


if __name__ == "__main__":
    raise SystemExit(main())
