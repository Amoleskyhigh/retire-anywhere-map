#!/usr/bin/env python3
"""Regression checks for the nine confirmed city/image corrections."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DATA_FILES = [ROOT / "world_retirement_data.json", ROOT / "data" / "world_retirement_data.json"]

EXPECTED = {
    "Da Nang": ("assets/cities/da_nang_ai_edited_v2.png", "My Khe Beach", "CC BY 2.0"),
    "Ho Chi Minh City": ("assets/cities/ho_chi_minh_ai_edited_v2.png", "Saigon Central Post Office", "CC BY-SA 4.0"),
    "Valencia": ("assets/cities/valencia_ai_edited_v2.png", "City of Arts and Sciences", "CC BY-SA 3.0"),
    "Lagos": ("assets/cities/lagos_ai_edited_v2.png", "Ponta da Piedade", "CC BY-SA 2.0"),
    "George Town": ("assets/cities/george_town_ai_edited_v2.png", "Heritage Streets", "CC BY-SA 2.0"),
    "Grecia": ("assets/cities/grecia_ai_edited_v2.png", "Metal Church", "Public domain"),
    "Boquete": ("assets/cities/boquete_ai_edited_v2.png", "Volcan Baru", "CC0"),
    "Melaka": ("assets/cities/melaka_ai_edited_v2.png", "Melaka River Walk", "CC BY-SA 3.0"),
    "Puerto Viejo": ("assets/cities/puerto_viejo_ai_edited_v2.png", "Jaguar Rescue Center", "CC BY-SA 4.0"),
}


def all_cities(snapshot: dict) -> dict[str, dict]:
    return {
        city: record
        for country in snapshot.values()
        if isinstance(country, dict)
        for city, record in country.get("Cities", {}).items()
    }


def main() -> int:
    snapshots = [json.loads(path.read_text()) for path in DATA_FILES]
    assert snapshots[0] == snapshots[1], "root and data JSON files differ"
    cities = all_cities(snapshots[0])
    hashes: dict[str, list[str]] = {}

    for city, (expected_path, expected_landmark, expected_license) in EXPECTED.items():
        assert city in cities, f"missing city: {city}"
        record = cities[city]
        assert record.get("landmark") == expected_landmark, f"{city}: landmark changed unexpectedly"
        assert record.get("img") == expected_path, f"{city}: image path is not the corrected local asset"
        assert record.get("image_source", "").startswith("https://commons.wikimedia.org/wiki/File:"), f"{city}: missing Wikimedia source"
        assert record.get("image_license") == expected_license, f"{city}: missing/incorrect license metadata"
        assert record.get("image_edit_note"), f"{city}: missing AI edit note"
        asset = ROOT / expected_path
        assert asset.is_file() and asset.stat().st_size > 0, f"{city}: missing or empty asset"
        assert asset.read_bytes()[:8] == b"\x89PNG\r\n\x1a\n", f"{city}: asset is not PNG"
        digest = hashlib.sha256(asset.read_bytes()).hexdigest()
        hashes.setdefault(digest, []).append(city)

    duplicates = [cities for cities in hashes.values() if len(cities) > 1]
    assert not duplicates, f"corrected cities share identical image bytes: {duplicates}"
    print(f"PASS: corrected image mapping, licensing metadata, and usable local assets for {len(EXPECTED)} cities")
    return 0


if __name__ == "__main__":
    main()
