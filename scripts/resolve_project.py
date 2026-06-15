#!/usr/bin/env python3
"""Resolve Theory Paper Reader project configuration and output paths.

The script searches from a starting directory upward for
`.theory-paper-reader.yaml`. If no configuration is found, it falls back to a
safe standalone layout rooted at the starting directory.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path
from typing import Any

import yaml

CONFIG_NAME = ".theory-paper-reader.yaml"

DEFAULT_CONFIG: dict[str, Any] = {
    "version": 1,
    "library_name": "Theory Paper Library",
    "paths": {
        "analysis_root": "theory-paper-analysis",
        "paper_library": "paper_library",
        "model_library": "model_library",
        "update_queue": "update_queue",
        "indexes": "indexes",
        "input_root": "inputs",
    },
    "input_policy": {
        "copy_original_source": False,
        "retain_source_manifest": True,
    },
    "library_policy": {
        "auto_promote_paper_card": False,
        "auto_modify_model_library": False,
        "require_human_approval": True,
    },
}

PATH_KEYS = (
    "analysis_root",
    "paper_library",
    "model_library",
    "update_queue",
    "indexes",
    "input_root",
)


def fail(message: str, code: int = 2) -> None:
    print(message, file=sys.stderr)
    raise SystemExit(code)


def deep_merge(base: dict[str, Any], override: dict[str, Any]) -> dict[str, Any]:
    merged: dict[str, Any] = {}
    for key, value in base.items():
        if isinstance(value, dict):
            merged[key] = deep_merge(value, {})
        else:
            merged[key] = value
    for key, value in override.items():
        if isinstance(value, dict) and isinstance(merged.get(key), dict):
            merged[key] = deep_merge(merged[key], value)
        else:
            merged[key] = value
    return merged


def discover_config(start: Path) -> Path | None:
    current = start.resolve()
    if current.is_file():
        current = current.parent
    for directory in (current, *current.parents):
        candidate = directory / CONFIG_NAME
        if candidate.is_file():
            return candidate
    return None


def load_config(path: Path | None) -> dict[str, Any]:
    if path is None:
        return deep_merge(DEFAULT_CONFIG, {})
    try:
        raw = yaml.safe_load(path.read_text(encoding="utf-8"))
    except (OSError, UnicodeDecodeError, yaml.YAMLError) as exc:
        fail(f"PROJECT CONFIG READ FAILED: {exc}")
    if raw is None:
        raw = {}
    if not isinstance(raw, dict):
        fail("PROJECT CONFIG INVALID: top-level YAML value must be a mapping.")
    config = deep_merge(DEFAULT_CONFIG, raw)
    if config.get("version") != 1:
        fail("PROJECT CONFIG INVALID: only version 1 is supported.")
    if not isinstance(config.get("paths"), dict):
        fail("PROJECT CONFIG INVALID: paths must be a mapping.")
    return config


def validate_relative_path(value: Any, key: str) -> Path:
    if not isinstance(value, str) or not value.strip():
        fail(f"PROJECT CONFIG INVALID: paths.{key} must be a non-empty string.")
    path = Path(value.strip())
    if path.is_absolute() or ".." in path.parts:
        fail(f"PROJECT CONFIG INVALID: paths.{key} must stay inside the project root.")
    return path


def slugify(value: str) -> str:
    value = value.strip().lower()
    value = re.sub(r"[^a-z0-9]+", "-", value)
    value = re.sub(r"-{2,}", "-", value).strip("-")
    return value or "paper"


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--start", type=Path, default=Path.cwd(), help="Directory from which to search upward")
    parser.add_argument("--source", type=Path, required=True, help="Primary PDF or Markdown source")
    parser.add_argument("--slug", help="Optional explicit paper slug")
    parser.add_argument("--create", action="store_true", help="Create configured directories and the paper analysis directory")
    parser.add_argument("--write", type=Path, help="Optional JSON output file")
    args = parser.parse_args()

    start = args.start.expanduser().resolve()
    source = args.source.expanduser().resolve()
    if not source.is_file():
        fail(f"SOURCE NOT FOUND: {source}")

    config_path = discover_config(start)
    project_root = config_path.parent if config_path else start
    config = load_config(config_path)

    resolved_paths: dict[str, Path] = {}
    for key in PATH_KEYS:
        relative = validate_relative_path(config["paths"][key], key)
        resolved_paths[key] = (project_root / relative).resolve()

    paper_slug = slugify(args.slug or source.stem)
    analysis_dir = resolved_paths["analysis_root"] / paper_slug
    source_dir = analysis_dir / "source"

    if args.create:
        for path in resolved_paths.values():
            path.mkdir(parents=True, exist_ok=True)
        source_dir.mkdir(parents=True, exist_ok=True)

    payload = {
        "config_found": config_path is not None,
        "config_path": str(config_path) if config_path else None,
        "project_root": str(project_root),
        "library_name": config["library_name"],
        "paper_slug": paper_slug,
        "source_path": str(source),
        "analysis_dir": str(analysis_dir),
        "source_dir": str(source_dir),
        "paths": {key: str(path) for key, path in resolved_paths.items()},
        "input_policy": config["input_policy"],
        "library_policy": config["library_policy"],
    }

    text = json.dumps(payload, ensure_ascii=False, indent=2)
    if args.write:
        output = args.write.expanduser().resolve()
        output.parent.mkdir(parents=True, exist_ok=True)
        output.write_text(text + "\n", encoding="utf-8")
    print(text)


if __name__ == "__main__":
    main()
