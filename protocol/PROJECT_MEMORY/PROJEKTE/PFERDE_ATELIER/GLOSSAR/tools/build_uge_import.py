#!/usr/bin/env python3
"""Build a UGE JSON import from the authoritative Pferde Atelier glossary facts.

Project adapter only: it never modifies source records and never publishes.
Only research-verified records are emitted. Editorial source/provenance fields stay
in the Wissensdatenbank and are deliberately not copied into WordPress.
"""
from __future__ import annotations

import argparse
import html
import json
from pathlib import Path
from typing import Any

FORMAT = "uge-json-v1"
REQUIRED = (
    "id",
    "begriff",
    "synonyme",
    "oberbereich",
    "kurzdefinition",
    "facherklaerung",
    "abgrenzung",
    "verwandte_begriffe",
    "recherche_status",
)


def _text(value: Any, key: str, source: Path) -> str:
    if not isinstance(value, str) or not value.strip():
        raise ValueError(f"{source.name}: {key} fehlt/leer")
    return value.strip()


def _string_list(value: Any, key: str, source: Path) -> list[str]:
    if not isinstance(value, list) or any(not isinstance(v, str) for v in value):
        raise ValueError(f"{source.name}: {key} muss Liste aus Textwerten sein")
    return [v.strip() for v in value if v.strip()]


def convert_record(record: dict[str, Any], source: Path) -> dict[str, Any] | None:
    missing = [key for key in REQUIRED if key not in record]
    if missing:
        raise ValueError(f"{source.name}: Pflichtfelder fehlen: {', '.join(missing)}")

    status = _text(record["recherche_status"], "recherche_status", source)
    if status != "GEPRUEFT":
        return None

    external_id = _text(record["id"], "id", source)
    if not external_id.startswith("term-") or len(external_id) <= 5:
        raise ValueError(f"{source.name}: id muss stabil mit term- beginnen")

    title = _text(record["begriff"], "begriff", source)
    group = _text(record["oberbereich"], "oberbereich", source)
    definition = _text(record["kurzdefinition"], "kurzdefinition", source)
    explanation = _text(record["facherklaerung"], "facherklaerung", source)
    boundary = _text(record["abgrenzung"], "abgrenzung", source)
    synonyms = _string_list(record["synonyme"], "synonyme", source)
    related = _string_list(record["verwandte_begriffe"], "verwandte_begriffe", source)

    content = (
        f"<p>{html.escape(explanation)}</p>"
        f"<p><strong>Abgrenzung:</strong> {html.escape(boundary)}</p>"
    )

    return {
        "external_id": external_id,
        "title": title,
        "slug": external_id[5:],
        "content": content,
        "groups": [group],
        "fields": {
            "short_definition": definition,
            "synonyms": ", ".join(synonyms),
            "related_terms": ", ".join(related),
        },
    }


def build(source_dir: Path) -> dict[str, Any]:
    if not source_dir.is_dir():
        raise ValueError(f"Quellordner fehlt: {source_dir}")

    items: list[dict[str, Any]] = []
    skipped: list[str] = []
    seen_ids: set[str] = set()
    seen_slugs: set[str] = set()

    for source in sorted(source_dir.glob("term-*.json")):
        try:
            record = json.loads(source.read_text(encoding="utf-8"))
        except json.JSONDecodeError as exc:
            raise ValueError(f"{source.name}: ungültiges JSON: {exc}") from exc
        if not isinstance(record, dict):
            raise ValueError(f"{source.name}: Datensatz muss JSON-Objekt sein")
        item = convert_record(record, source)
        if item is None:
            skipped.append(source.name)
            continue
        if item["external_id"] in seen_ids:
            raise ValueError(f"Doppelte ID: {item['external_id']}")
        if item["slug"] in seen_slugs:
            raise ValueError(f"Doppelter Slug: {item['slug']}")
        seen_ids.add(item["external_id"])
        seen_slugs.add(item["slug"])
        items.append(item)

    if not items:
        raise ValueError("Keine GEPRUEFTEN Glossardatensätze gefunden")

    return {
        "format": FORMAT,
        "source": "PFERDE_ATELIER/WISSENSDATENBANK/AKTENSCHRAENKE/GLOSSAR/DATEN",
        "policy": "GEPRUEFT_ONLY_DRAFT_IMPORT",
        "skipped_unverified": skipped,
        "items": items,
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("source_dir", type=Path)
    parser.add_argument("output", type=Path)
    args = parser.parse_args()

    try:
        payload = build(args.source_dir)
    except ValueError as exc:
        parser.error(str(exc))

    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(
        json.dumps(payload, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    print(f"UGE_CAMPUS_ADAPTER_PASS items={len(payload['items'])} skipped={len(payload['skipped_unverified'])}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
