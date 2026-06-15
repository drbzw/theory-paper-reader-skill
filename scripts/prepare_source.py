#!/usr/bin/env python3
"""Prepare a PDF or Markdown theory paper for auditable model analysis.

The script is intentionally deterministic. It never performs OCR and never
uses a language model. It creates:

- source.json: structured metadata and text units
- source_numbered.txt: line-addressable text for evidence locators

Supported inputs: .pdf, .md, .markdown
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path
from typing import Any

SUPPORTED_MARKDOWN = {".md", ".markdown"}


def fail(message: str, code: int = 2) -> None:
    print(message, file=sys.stderr)
    raise SystemExit(code)


def normalize_lines(text: str) -> list[str]:
    return [line.rstrip() for line in text.replace("\r\n", "\n").replace("\r", "\n").split("\n")]


def prepare_markdown(source: Path) -> tuple[dict[str, Any], str]:
    try:
        text = source.read_text(encoding="utf-8")
    except UnicodeDecodeError:
        fail("MARKDOWN READ FAILED: the file is not valid UTF-8.")

    lines = normalize_lines(text)
    nonempty = sum(bool(line.strip()) for line in lines)
    if nonempty < 20:
        fail("MARKDOWN CONTENT TOO SHORT: fewer than 20 non-empty lines were found.")

    headings: list[dict[str, Any]] = []
    page_markers: list[dict[str, Any]] = []
    image_links: list[dict[str, Any]] = []
    numbered: list[str] = []

    heading_re = re.compile(r"^(#{1,6})\s+(.+?)\s*$")
    page_re = re.compile(r"(?:^|\b)(?:page|p\.?)[ _:-]?(\d{1,4})(?:\b|$)", re.IGNORECASE)
    image_re = re.compile(r"!\[[^\]]*\]\(([^)]+)\)")

    for idx, line in enumerate(lines, start=1):
        locator = f"MD-L{idx:05d}"
        numbered.append(f"[{locator}] {line}")

        heading_match = heading_re.match(line)
        if heading_match:
            headings.append(
                {
                    "level": len(heading_match.group(1)),
                    "title": heading_match.group(2).strip(),
                    "line": idx,
                    "locator": locator,
                }
            )

        page_match = page_re.search(line)
        if page_match and ("page" in line.lower() or line.strip().lower().startswith("p")):
            page_markers.append(
                {"page": int(page_match.group(1)), "line": idx, "locator": locator, "raw": line.strip()}
            )

        for raw_target in image_re.findall(line):
            target = raw_target.strip().split()[0].strip("<>")
            if re.match(r"^[a-z]+://", target, flags=re.IGNORECASE):
                exists: bool | None = None
                resolved = target
            else:
                asset_path = (source.parent / target).resolve()
                exists = asset_path.exists()
                resolved = str(asset_path)
            image_links.append(
                {
                    "target": target,
                    "resolved": resolved,
                    "exists": exists,
                    "line": idx,
                    "locator": locator,
                }
            )

    warnings: list[str] = []
    missing = [item for item in image_links if item["exists"] is False]
    if missing:
        warnings.append(f"{len(missing)} linked local image asset(s) were not found.")
    if not headings:
        warnings.append("No Markdown headings were detected; use line locators as the primary evidence anchors.")
    if not page_markers:
        warnings.append("No explicit page markers were detected; cite section headings plus MD line ranges.")

    payload: dict[str, Any] = {
        "source_type": "markdown",
        "source_path": str(source.resolve()),
        "locator_scheme": "MD-L00001",
        "line_count": len(lines),
        "nonempty_line_count": nonempty,
        "headings": headings,
        "page_markers": page_markers,
        "image_links": image_links,
        "warnings": warnings,
        "units": [
            {
                "unit_id": "markdown-document",
                "locator_start": "MD-L00001",
                "locator_end": f"MD-L{len(lines):05d}",
                "text": text,
            }
        ],
    }
    return payload, "\n".join(numbered) + "\n"


def prepare_pdf(source: Path) -> tuple[dict[str, Any], str]:
    try:
        import fitz  # PyMuPDF
    except ImportError:
        fail("PDF DEPENDENCY MISSING: install requirements.txt before processing PDFs.")

    try:
        document = fitz.open(source)
    except Exception as exc:  # pragma: no cover - library-specific exceptions
        fail(f"PDF OPEN FAILED: {exc}")

    if document.page_count == 0:
        fail("PDF TEXT EXTRACTION FAILED: the PDF contains no pages.")

    units: list[dict[str, Any]] = []
    numbered: list[str] = []
    low_text_pages: list[int] = []
    total_chars = 0

    for page_index in range(document.page_count):
        page_number = page_index + 1
        page = document.load_page(page_index)
        text = page.get_text("text") or ""
        lines = normalize_lines(text)
        visible_chars = sum(len(line.strip()) for line in lines)
        total_chars += visible_chars
        if visible_chars < 80:
            low_text_pages.append(page_number)

        numbered.append(f"=== PAGE {page_number} ===")
        for line_index, line in enumerate(lines, start=1):
            locator = f"P{page_number:03d}-L{line_index:03d}"
            numbered.append(f"[{locator}] {line}")
        numbered.append("")

        units.append(
            {
                "unit_id": f"page-{page_number}",
                "page": page_number,
                "locator_start": f"P{page_number:03d}-L001",
                "locator_end": f"P{page_number:03d}-L{max(len(lines), 1):03d}",
                "visible_character_count": visible_chars,
                "text": text,
            }
        )

    document.close()

    average_chars = total_chars / max(len(units), 1)
    if total_chars < 1000 or average_chars < 100:
        fail(
            "PDF TEXT EXTRACTION FAILED: extracted text is too sparse. "
            "Provide a text-based PDF or a MinerU/other Markdown conversion."
        )

    warnings: list[str] = []
    if low_text_pages:
        warnings.append(
            "Low-text pages detected: " + ", ".join(str(page) for page in low_text_pages[:30])
        )

    payload: dict[str, Any] = {
        "source_type": "pdf",
        "source_path": str(source.resolve()),
        "locator_scheme": "P001-L001",
        "page_count": len(units),
        "total_visible_characters": total_chars,
        "average_visible_characters_per_page": round(average_chars, 2),
        "low_text_pages": low_text_pages,
        "warnings": warnings,
        "units": units,
    }
    return payload, "\n".join(numbered)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("source", type=Path, help="Path to a PDF or Markdown paper")
    parser.add_argument("--output-dir", type=Path, required=True, help="Directory for prepared source files")
    args = parser.parse_args()

    source = args.source.expanduser().resolve()
    if not source.exists() or not source.is_file():
        fail(f"SOURCE NOT FOUND: {source}")

    suffix = source.suffix.lower()
    if suffix == ".pdf":
        payload, numbered_text = prepare_pdf(source)
    elif suffix in SUPPORTED_MARKDOWN:
        payload, numbered_text = prepare_markdown(source)
    else:
        fail("UNSUPPORTED SOURCE TYPE: use .pdf, .md, or .markdown")

    output_dir = args.output_dir.expanduser().resolve()
    output_dir.mkdir(parents=True, exist_ok=True)

    json_path = output_dir / "source.json"
    numbered_path = output_dir / "source_numbered.txt"
    json_path.write_text(json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8")
    numbered_path.write_text(numbered_text, encoding="utf-8")

    print(f"Prepared {payload['source_type']} source")
    print(f"Structured source: {json_path}")
    print(f"Numbered source:   {numbered_path}")
    for warning in payload.get("warnings", []):
        print(f"WARNING: {warning}")


if __name__ == "__main__":
    main()
