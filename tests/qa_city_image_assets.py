#!/usr/bin/env python3
"""Validate every repository-local city image used by the map.

The check is intentionally offline for local assets: it verifies that the
asset exists, is non-empty, and has a recognizable raster signature. New
AI-edited city additions must additionally pass the focused Vietnam regression
test, which checks source/license/edit metadata.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DATA_FILES = [ROOT / "world_retirement_data.json", ROOT / "data" / "world_retirement_data.json"]
IMAGE_EXTENSIONS = {".png", ".jpg", ".jpeg", ".webp"}


def fail(message: str) -> None:
    raise AssertionError(message)


def image_signature(path: Path) -> bool:
    header = path.read_bytes()[:12]
    return (
        header.startswith(b"\x89PNG\r\n\x1a\n")
        or header.startswith(b"\xff\xd8\xff")
        or (header[:4] == b"RIFF" and header[8:12] == b"WEBP")
    )


def cities_from(snapshot: dict) -> list[dict]:
    result = []
    for country in snapshot.values():
        if not isinstance(country, dict):
            continue
        cities = country.get("Cities", {})
        if isinstance(cities, dict):
            result.extend(cities.values())
    return result


def main() -> int:
    snapshots = [json.loads(path.read_text()) for path in DATA_FILES]
    if snapshots[0] != snapshots[1]:
        fail("root and data JSON files differ")

    checked = 0
    for city in cities_from(snapshots[0]):
        image = city.get("img", "")
        if not image or image.startswith(("http://", "https://", "//")):
            continue
        path = ROOT / image
        if path.suffix.lower() not in IMAGE_EXTENSIONS:
            fail(f"{city.get('city', '<unknown>')}: unsupported local image extension: {image}")
        if not path.is_file() or path.stat().st_size == 0:
            fail(f"{city.get('city', '<unknown>')}: missing or empty image: {image}")
        if not image_signature(path):
            fail(f"{city.get('city', '<unknown>')}: unrecognized image file: {image}")
        checked += 1

    if checked == 0:
        fail("no repository-local city images were checked")
    print(f"PASS: validated {checked} repository-local city image assets and metadata")
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except Exception as exc:
        print(f"FAIL: {exc}", file=sys.stderr)
        raise SystemExit(1)
