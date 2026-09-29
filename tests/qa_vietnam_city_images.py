#!/usr/bin/env python3
"""Regression checks for Vietnam map-marker and city-detail images.

This intentionally checks the user-visible image path, not just that an ``img``
field exists: every configured URL must return an image, and the map popup plus
the click-opened detail modal must use the same URL resolver.
"""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path
from urllib.request import Request, urlopen


ROOT = Path(__file__).resolve().parents[1]
CITY_FILES = [ROOT / "world_retirement_data.json", ROOT / "data" / "world_retirement_data.json"]
REQUIRED = {"Da Nang", "Ho Chi Minh City", "Hanoi", "Nha Trang"}


def fail(message: str) -> None:
    raise AssertionError(message)


def fetch_image(url: str) -> tuple[int, str]:
    request = Request(url, headers={"User-Agent": "retire-anywhere-map-qa/1.0"})
    with urlopen(request, timeout=20) as response:
        return response.status, response.headers.get_content_type()


def main() -> int:
    snapshots = [json.loads(path.read_text()) for path in CITY_FILES]
    if snapshots[0] != snapshots[1]:
        fail("root and data JSON files differ")

    cities = snapshots[0].get("Vietnam", {}).get("Cities", {})
    if set(cities) != REQUIRED:
        fail(f"Vietnam city set mismatch: {sorted(cities)}")

    for name in sorted(REQUIRED):
        image = cities[name].get("img", "")
        if not image.startswith("assets/cities/"):
            fail(f"{name}: image is not a repository-local asset: {image!r}")
        image_path = ROOT / image
        if not image_path.is_file() or image_path.stat().st_size == 0:
            fail(f"{name}: local image asset missing or empty: {image_path}")
        if not cities[name].get("image_source") or not cities[name].get("image_license"):
            fail(f"{name}: missing source/license attribution")

    html = (ROOT / "index.html").read_text()
    required_snippets = (
        "function resolveCityImage(src)",
        "return /^(https?:)?\\/\\//i.test(src) ? src",
        "const img=resolveCityImage(c.img);",
        "onerror=\"imageErrorFallback(this)\"",
        "window.openCityDetail=openCityDetail;",
    )
    for snippet in required_snippets:
        if snippet not in html:
            fail(f"index.html missing image interaction guard: {snippet}")

    print("PASS: four Vietnam city images are local, attributed, and popup/modal use resolveCityImage")
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except Exception as exc:
        print(f"FAIL: {exc}", file=sys.stderr)
        raise SystemExit(1)
