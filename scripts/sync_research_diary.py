#!/usr/bin/env python3
"""Synchronize the scientific Markdown diary into the MkDocs presentation layer."""

from __future__ import annotations

import argparse
import hashlib
import html
import json
import os
import re
import shutil
import subprocess
import sys
from pathlib import Path
from typing import Any

import yaml


SITE_ROOT = Path(__file__).resolve().parents[1]
DOCS_ROOT = SITE_ROOT / "docs"
DEFAULT_SOURCE = SITE_ROOT.parent / "fish" / "research_diary"
SOURCE_REPOSITORY = "https://github.com/khkt-tn/fish"
SOURCE_BRANCH = "main"
MAX_IMAGE_BYTES = 2 * 1024 * 1024

ROOT_MAPPING = {
    "ABOUT_PROJECT.md": "project.md",
    "RESEARCH_TIMELINE.md": "timeline.md",
    "MEDIA_INDEX.md": "media.md",
    "EVIDENCE_INDEX.md": "evidence.md",
    "CONTRIBUTION_LOG.md": "contributions.md",
}

PAGE_TITLES = {
    "ABOUT_PROJECT.md": "Dự án",
    "RESEARCH_TIMELINE.md": "Timeline nghiên cứu",
    "MEDIA_INDEX.md": "Media",
    "EVIDENCE_INDEX.md": "Minh chứng",
    "CONTRIBUTION_LOG.md": "Đóng góp",
}

STATUS_LABELS = {
    "VERIFIED": "Đã xác minh",
    "PARTIAL": "Một phần",
    "TO_VERIFY": "Cần xác minh",
    "PLANNED": "Kế hoạch",
}

LINK_PATTERN = re.compile(r"(!?)\[([^\]]*)\]\(([^)]+)\)")
IMAGE_SUFFIXES = {".png", ".jpg", ".jpeg", ".gif", ".webp", ".svg"}


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def git_value(project_root: Path, *args: str) -> str:
    result = subprocess.run(
        ["git", "-C", str(project_root), *args],
        check=True,
        capture_output=True,
        text=True,
    )
    return result.stdout.strip()


def parse_front_matter(text: str, path: Path) -> tuple[dict[str, Any], str, str]:
    if not text.startswith("---\n"):
        raise ValueError(f"Missing YAML front matter: {path}")
    parts = text.split("---\n", 2)
    if len(parts) != 3:
        raise ValueError(f"Invalid YAML front matter boundary: {path}")
    raw_front = parts[1]
    metadata = yaml.safe_load(raw_front)
    if not isinstance(metadata, dict):
        raise ValueError(f"Front matter is not a mapping: {path}")
    return metadata, raw_front, parts[2]


def source_target_map(source_root: Path) -> dict[Path, Path]:
    mapping: dict[Path, Path] = {}
    for source_name, destination_name in ROOT_MAPPING.items():
        mapping[(source_root / source_name).resolve()] = (
            DOCS_ROOT / destination_name
        ).resolve()
    for source_path in sorted((source_root / "entries").glob("J*.md")):
        mapping[source_path.resolve()] = (
            DOCS_ROOT / "journal" / source_path.name
        ).resolve()
    mapping[(source_root / "README.md").resolve()] = (
        DOCS_ROOT / "journal" / "index.md"
    ).resolve()
    return mapping


def relative_markdown_path(from_path: Path, to_path: Path) -> str:
    return Path(os.path.relpath(to_path, from_path.parent)).as_posix()


def repository_url(project_root: Path, resolved: Path) -> str:
    relative = resolved.relative_to(project_root.resolve()).as_posix()
    kind = "blob" if resolved.is_file() else "tree"
    return f"{SOURCE_REPOSITORY}/{kind}/{SOURCE_BRANCH}/{relative}"


def copy_image(
    source_image: Path,
    project_root: Path,
    destination_markdown: Path,
    copied_images: list[dict[str, Any]],
) -> str:
    size = source_image.stat().st_size
    if size > MAX_IMAGE_BYTES:
        raise ValueError(
            f"Referenced image exceeds {MAX_IMAGE_BYTES} bytes: "
            f"{source_image} ({size} bytes)"
        )
    relative_source = source_image.relative_to(project_root).as_posix()
    destination = DOCS_ROOT / "assets" / "images" / "research" / relative_source
    destination.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(source_image, destination)
    copied_images.append(
        {
            "source": relative_source,
            "destination": destination.relative_to(SITE_ROOT).as_posix(),
            "bytes": size,
            "sha256": sha256_file(source_image),
        }
    )
    return relative_markdown_path(destination_markdown, destination)


def transform_links(
    content: str,
    source_path: Path,
    destination_path: Path,
    source_root: Path,
    project_root: Path,
    mapped_paths: dict[Path, Path],
    copied_images: list[dict[str, Any]],
    warnings: list[str],
) -> str:
    def replace(match: re.Match[str]) -> str:
        marker, label, raw_target = match.groups()
        target = raw_target.strip().strip("<>")
        if target.startswith(("http://", "https://", "mailto:", "#")):
            return match.group(0)

        path_part, anchor = (target.split("#", 1) + [""])[:2]
        if not path_part:
            return match.group(0)
        resolved = (source_path.parent / path_part).resolve()

        if marker == "!":
            if not resolved.exists():
                warnings.append(
                    f"Missing referenced image in {source_path.name}: {path_part}"
                )
                return match.group(0)
            if resolved.suffix.lower() not in IMAGE_SUFFIXES:
                warnings.append(
                    f"Unsupported referenced image type in "
                    f"{source_path.name}: {path_part}"
                )
                return match.group(0)
            destination_target = copy_image(
                resolved, project_root, destination_path, copied_images
            )
            return f"![{label}]({destination_target})"

        mapped = mapped_paths.get(resolved)
        if mapped is not None:
            destination_target = relative_markdown_path(destination_path, mapped)
            if anchor:
                destination_target += f"#{anchor}"
            return f"[{label}]({destination_target})"

        try:
            resolved.relative_to(project_root)
        except ValueError:
            warnings.append(
                f"Link escapes scientific repository in "
                f"{source_path.name}: {path_part}"
            )
            return match.group(0)

        if not resolved.exists():
            warnings.append(f"Missing local link in {source_path.name}: {path_part}")
            return match.group(0)

        remote = repository_url(project_root, resolved)
        if anchor:
            remote += f"#{anchor}"
        return f"[{label}]({remote})"

    return LINK_PATTERN.sub(replace, content)


def replace_media_placeholders(content: str) -> str:
    content = re.sub(
        r"\x60TODO_YOUTUBE_(?:VIDEO_ID|URL)\x60",
        '<span class="media-waiting">Đang chờ cập nhật</span>',
        content,
    )
    content = content.replace(
        "TODO_UPLOAD",
        '<span class="status-badge status-todo">Chờ video</span>',
    )
    return content


def link_verified_commits(content: str) -> str:
    return re.sub(
        r"\x60([0-9a-f]{40})\x60",
        lambda match: (
            f"[\x60{match.group(1)}\x60]"
            f"({SOURCE_REPOSITORY}/commit/{match.group(1)})"
        ),
        content,
    )


def evidence_navigation(content: str) -> str:
    block = """
<nav class="evidence-map" aria-label="Nhóm minh chứng">
  <a href="#git-evidence"><span>01</span><strong>Git</strong></a>
  <a href="#dataset-evidence"><span>02</span><strong>Dataset</strong></a>
  <a href="#model-evidence"><span>03</span><strong>Model</strong></a>
  <a href="#tracking-evidence"><span>04</span><strong>Tracking</strong></a>
  <a href="#model-evidence"><span>05</span><strong>Behavior</strong></a>
  <a href="#environment-evidence"><span>06</span><strong>Environment</strong></a>
  <a href="#environment-evidence"><span>07</span><strong>Notebook</strong></a>
</nav>
"""
    lines = content.splitlines()
    for index, line in enumerate(lines):
        if line.startswith("# "):
            lines[index + 1 : index + 1] = ["", block.strip(), ""]
            break
    return "\n".join(lines)


def metadata_panel(metadata: dict[str, Any]) -> str:
    status = str(metadata.get("status", "TO_VERIFY")).upper()
    label = STATUS_LABELS.get(status, status)
    rows = [
        ("Mã nhật ký", metadata.get("journal_id", "")),
        ("Experiment", metadata.get("experiment_id", "")),
        ("Ngày", metadata.get("date", "")),
        ("Trạng thái", label),
        ("Evidence", metadata.get("evidence_level", "")),
        ("Cập nhật", metadata.get("last_updated", "")),
    ]
    items = []
    for key, value in rows:
        value_text = html.escape(str(value))
        if key == "Trạng thái":
            value_text = (
                f'<span class="status-badge status-{status.lower()}">'
                f"{html.escape(label)} · {html.escape(status)}</span>"
            )
        items.append(
            '<div class="journal-meta__item">'
            f'<span class="journal-meta__label">{html.escape(key)}</span>'
            f'<span class="journal-meta__value">{value_text}</span>'
            "</div>"
        )
    return (
        '<section class="journal-meta" aria-label="Thông tin bài nhật ký">'
        + "".join(items)
        + "</section>"
    )


def inject_journal_panel(body: str, metadata: dict[str, Any]) -> str:
    lines = body.lstrip("\n").splitlines()
    insert_at = 0
    for index, line in enumerate(lines):
        if line.startswith("# "):
            insert_at = index + 1
            break
    panel_lines = ["", metadata_panel(metadata), ""]
    lines[insert_at:insert_at] = panel_lines
    return "\n".join(lines).rstrip() + "\n"


def page_wrapper(source_name: str, body: str) -> str:
    slug = Path(source_name).stem.lower().replace("_", "-")
    return (
        f'<div class="source-page source-{slug}" markdown>\n\n'
        + body.strip()
        + "\n\n</div>\n"
    )


def sync(source_root: Path) -> int:
    source_root = source_root.resolve()
    project_root = source_root.parent.resolve()
    if not (source_root / "entries").is_dir():
        raise FileNotFoundError(f"Diary entries directory not found: {source_root}")

    source_files = [
        *(source_root / name for name in ROOT_MAPPING),
        *sorted((source_root / "entries").glob("J*.md")),
    ]
    for path in source_files:
        if not path.is_file():
            raise FileNotFoundError(path)

    before_hashes = {
        path.relative_to(project_root).as_posix(): sha256_file(path)
        for path in source_files
    }
    mapped_paths = source_target_map(source_root)
    copied_images: list[dict[str, Any]] = []
    warnings: list[str] = []
    destinations: list[dict[str, str]] = []

    journal_root = DOCS_ROOT / "journal"
    journal_root.mkdir(parents=True, exist_ok=True)
    for old_path in journal_root.glob("J*.md"):
        old_path.unlink()

    research_images = DOCS_ROOT / "assets" / "images" / "research"
    if research_images.exists():
        shutil.rmtree(research_images)

    for source_path in source_files:
        if source_path.parent == source_root / "entries":
            destination = journal_root / source_path.name
            text = source_path.read_text(encoding="utf-8")
            metadata, raw_front, body = parse_front_matter(text, source_path)
            body = transform_links(
                body,
                source_path,
                destination,
                source_root,
                project_root,
                mapped_paths,
                copied_images,
                warnings,
            )
            body = replace_media_placeholders(body)
            body = link_verified_commits(body)
            body = inject_journal_panel(body, metadata)
            output = (
                "---\n"
                + raw_front
                + "---\n"
                + "<!-- Generated from scientific source; "
                + "do not edit this copy directly. -->\n\n"
                + body
            )
        else:
            destination = DOCS_ROOT / ROOT_MAPPING[source_path.name]
            body = source_path.read_text(encoding="utf-8")
            body = transform_links(
                body,
                source_path,
                destination,
                source_root,
                project_root,
                mapped_paths,
                copied_images,
                warnings,
            )
            body = replace_media_placeholders(body)
            body = link_verified_commits(body)
            if source_path.name == "EVIDENCE_INDEX.md":
                body = evidence_navigation(body)
            body = page_wrapper(source_path.name, body)
            output = (
                "---\n"
                + f'title: "{PAGE_TITLES[source_path.name]}"\n'
                + "---\n\n"
                + "<!-- Generated from scientific source; "
                + "do not edit this copy directly. -->\n\n"
                + body
            )

        destination.parent.mkdir(parents=True, exist_ok=True)
        destination.write_text(output, encoding="utf-8")
        destinations.append(
            {
                "source": source_path.relative_to(project_root).as_posix(),
                "destination": destination.relative_to(SITE_ROOT).as_posix(),
                "source_sha256": sha256_file(source_path),
                "destination_sha256": sha256_file(destination),
            }
        )
        print(
            f"SYNCED {source_path.relative_to(project_root)} "
            f"-> {destination.relative_to(SITE_ROOT)}"
        )

    after_hashes = {
        path.relative_to(project_root).as_posix(): sha256_file(path)
        for path in source_files
    }
    if before_hashes != after_hashes:
        raise RuntimeError("Scientific source Markdown changed during synchronization")

    report = {
        "source_root": source_root.relative_to(project_root).as_posix(),
        "source_check_path": Path(
            os.path.relpath(project_root, SITE_ROOT)
        ).as_posix(),
        "source_repository": SOURCE_REPOSITORY,
        "source_branch": SOURCE_BRANCH,
        "source_git_commit": git_value(project_root, "rev-parse", "HEAD"),
        "source_files": destinations,
        "copied_images": copied_images,
        "warnings": warnings,
    }
    report_path = DOCS_ROOT / "assets" / "data" / "sync_report.json"
    report_path.parent.mkdir(parents=True, exist_ok=True)
    report_path.write_text(
        json.dumps(report, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )

    for warning in warnings:
        print(f"WARNING {warning}", file=sys.stderr)
    print(
        f"SYNC PASS: {len(destinations)} Markdown files, "
        f"{len(copied_images)} referenced images, {len(warnings)} warnings"
    )
    return 0


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--source",
        type=Path,
        default=DEFAULT_SOURCE,
        help="Path to the scientific research_diary directory.",
    )
    args = parser.parse_args()
    return sync(args.source)


if __name__ == "__main__":
    raise SystemExit(main())
