#!/usr/bin/env python3
"""Fail-closed WordPress prewrite content-contract gate.

Read-only: this gate never changes article content, workflow state, WordPress,
or any upstream text-production component.

Usage:
    python3 wordpress_prewrite_gate.py APPROVED_ENVELOPE.json WORDPRESS_CANDIDATE.json

The first file is the already approved/hash-bound production envelope.
The second file is the exact JSON artifact whose article bodies are about
to be written to WordPress.
"""
from __future__ import annotations

import hashlib
import json
import re
import sys
from html.parser import HTMLParser
from pathlib import Path
from typing import Any

ALLOWED_RELEASE_CONTRACT = "WORKFLOW_SUPERVISOR_RELEASE_V2_SIGNED"
ALLOWED_RELEASE_STATUS = "PASS"
ALLOWED_AUTHORING_ROLE = "APPROVED_RESEARCH_TEXT_PROCESS_ONLY"
ALLOWED_AUTHORING_PROCESS = "STARTMASTER_0039_APPROVED_RESEARCH_TEXT_PROCESS_ONLY"
REQUIRED_SEQUENCE_MARKERS = {
    "AUTHORIZED_0039_RESEARCH_TEXT_PROCESS",
    "ARTICLE_ORIGIN_AND_IMMUTABILITY_GATE_PASS",
}
HASH_RE = re.compile(r"^[0-9a-f]{64}$")


def stable_hash(obj: Any) -> str:
    raw = json.dumps(obj, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode("utf-8")
    return hashlib.sha256(raw).hexdigest()


def sha_text(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def norm_text(value: Any) -> str:
    return " ".join(str(value or "").split())


class ArticleHtmlAudit(HTMLParser):
    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.links: list[dict[str, str]] = []
        self._link: dict[str, Any] | None = None
        self.table_count = 0
        self.system_table_count = 0
        self.table_row_count = 0
        self._table_depth = 0
        self._row_has_cell = False
        self._table_visible_chars = 0

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        amap = {k: (v or "") for k, v in attrs}
        if tag.lower() == "a":
            self._link = {"href": amap.get("href", ""), "role": amap.get("data-link-role", ""), "parts": []}
        elif tag.lower() == "table":
            self.table_count += 1
            self._table_depth += 1
            classes = set(amap.get("class", "").split())
            if "system-129-table" in classes:
                self.system_table_count += 1
        elif tag.lower() == "tr" and self._table_depth:
            self._row_has_cell = False
        elif tag.lower() in {"td", "th"} and self._table_depth:
            self._row_has_cell = True

    def handle_endtag(self, tag: str) -> None:
        if tag.lower() == "a" and self._link is not None:
            self.links.append({
                "href": str(self._link["href"]),
                "role": str(self._link["role"]),
                "anchor": norm_text("".join(self._link["parts"])),
            })
            self._link = None
        elif tag.lower() == "tr" and self._table_depth and self._row_has_cell:
            self.table_row_count += 1
            self._row_has_cell = False
        elif tag.lower() == "table" and self._table_depth:
            self._table_depth -= 1

    def handle_data(self, data: str) -> None:
        if self._link is not None:
            self._link["parts"].append(data)
        if self._table_depth:
            self._table_visible_chars += len(norm_text(data))


def parse_html(body_html: str) -> ArticleHtmlAudit:
    parser = ArticleHtmlAudit()
    parser.feed(body_html)
    parser.close()
    return parser


def extract_candidate_articles(obj: Any) -> dict[str, dict[str, dict[str, Any]]]:
    """Return candidate article records indexed by slot and canonical article id."""
    by_slot: dict[str, dict[str, Any]] = {}
    by_id: dict[str, dict[str, Any]] = {}

    def add(article: dict[str, Any], item: dict[str, Any] | None = None) -> None:
        item = item or {}
        runtime = (item.get("runtime_order") or {}) if isinstance(item.get("runtime_order"), dict) else {}
        slot = str(article.get("plan_slot") or item.get("plan_slot") or runtime.get("plan_slot") or "")
        cid = str(article.get("canonical_article_id") or item.get("canonical_article_id") or "")
        rec = dict(article)
        if slot:
            rec.setdefault("plan_slot", slot)
            by_slot.setdefault(slot, rec)
        if cid:
            rec.setdefault("canonical_article_id", cid)
            by_id.setdefault(cid, rec)

    plan = obj.get("production_plan") if isinstance(obj, dict) else None
    if isinstance(plan, dict):
        items = plan.get("items")
        if isinstance(items, list):
            for item in items:
                if not isinstance(item, dict):
                    continue
                article = item.get("canonical_article")
                if isinstance(article, dict):
                    add(article, item)

    def walk(node: Any) -> None:
        if isinstance(node, dict):
            if isinstance(node.get("body_html"), str):
                add(node)
            for value in node.values():
                walk(value)
        elif isinstance(node, list):
            for value in node:
                walk(value)

    if not by_slot and not by_id:
        walk(obj)
    return {"by_slot": by_slot, "by_id": by_id}


def validate(evidence: dict[str, Any], candidate: dict[str, Any]) -> dict[str, Any]:
    errors: list[dict[str, Any]] = []
    plan = evidence.get("production_plan") or {}
    release = evidence.get("workflow_release") or {}

    if release.get("contract") != ALLOWED_RELEASE_CONTRACT:
        errors.append({"code": "APPROVED_TEXT_PROCESS_RELEASE_CONTRACT_INVALID"})
    if release.get("status") != ALLOWED_RELEASE_STATUS:
        errors.append({"code": "APPROVED_TEXT_PROCESS_RELEASE_NOT_PASS"})
    if release.get("authoring_role") != ALLOWED_AUTHORING_ROLE:
        errors.append({
            "code": "APPROVED_TEXT_PROCESS_ORIGIN_NOT_PROVEN",
            "expected": ALLOWED_AUTHORING_ROLE,
            "actual": release.get("authoring_role"),
        })
    if release.get("content_generation_performed_by_supervisor") is not False:
        errors.append({"code": "SUPERVISOR_CONTENT_GENERATION_MUST_BE_FALSE"})
    if release.get("wordpress_write_performed") is not False:
        errors.append({"code": "UPSTREAM_WORDPRESS_WRITE_MUST_BE_FALSE"})

    sequence = set(release.get("sequence") or [])
    missing_sequence = sorted(REQUIRED_SEQUENCE_MARKERS.difference(sequence))
    if missing_sequence:
        errors.append({"code": "APPROVED_TEXT_PROCESS_SEQUENCE_MARKER_MISSING", "missing": missing_sequence})

    release_items = release.get("items") if isinstance(release.get("items"), list) else []
    release_by_slot: dict[str, dict[str, Any]] = {}
    release_by_id: dict[str, dict[str, Any]] = {}
    for row in release_items:
        if not isinstance(row, dict):
            continue
        slot = str(row.get("plan_slot") or "")
        cid = str(row.get("canonical_article_id") or "")
        if slot:
            release_by_slot[slot] = row
        if cid:
            release_by_id[cid] = row

    plan_items = plan.get("items") if isinstance(plan.get("items"), list) else []
    plan_by_slot: dict[str, dict[str, Any]] = {}
    plan_by_id: dict[str, dict[str, Any]] = {}
    for item in plan_items:
        if not isinstance(item, dict):
            continue
        article = item.get("canonical_article") or {}
        runtime = (item.get("runtime_order") or {}) if isinstance(item.get("runtime_order"), dict) else {}
        slot = str(article.get("plan_slot") or item.get("plan_slot") or runtime.get("plan_slot") or "")
        cid = str(article.get("canonical_article_id") or item.get("canonical_article_id") or "")
        if slot:
            plan_by_slot[slot] = item
        if cid:
            plan_by_id[cid] = item

    candidate_index = extract_candidate_articles(candidate)
    candidate_by_slot = candidate_index["by_slot"]
    candidate_by_id = candidate_index["by_id"]

    if not release_by_slot or not plan_items:
        errors.append({"code": "APPROVED_TEXT_PROCESS_BINDINGS_MISSING"})

    bindings: list[tuple[str, dict[str, Any], dict[str, Any], dict[str, Any]]] = []
    for slot, rel_item in release_by_slot.items():
        cid = str(rel_item.get("canonical_article_id") or "")
        item = plan_by_slot.get(slot) or (plan_by_id.get(cid) if cid else None)
        cand = candidate_by_slot.get(slot) or (candidate_by_id.get(cid) if cid else None)
        if item is None:
            errors.append({"code": "RELEASE_PLAN_BINDING_MISSING", "plan_slot": slot, "canonical_article_id": cid})
            continue
        if cand is None:
            errors.append({"code": "WORDPRESS_CANDIDATE_BINDING_MISSING", "plan_slot": slot, "canonical_article_id": cid})
            continue
        bindings.append((slot, rel_item, item, cand))

    # The immutable plan slot is authoritative when present. Canonical article ids
    # are used only for historical package forms that do not carry plan slots.
    if candidate_by_slot:
        if set(candidate_by_slot) != set(release_by_slot):
            errors.append({
                "code": "WORDPRESS_CANDIDATE_SLOT_SET_MISMATCH",
                "expected_slots": sorted(release_by_slot),
                "actual_slots": sorted(candidate_by_slot),
            })
    else:
        expected_ids = {str(x.get("canonical_article_id") or "") for x in release_items if isinstance(x, dict)}
        expected_ids.discard("")
        actual_ids = set(candidate_by_id)
        if expected_ids and actual_ids != expected_ids:
            errors.append({
                "code": "WORDPRESS_CANDIDATE_ARTICLE_SET_MISMATCH",
                "expected_canonical_article_ids": sorted(expected_ids),
                "actual_canonical_article_ids": sorted(actual_ids),
            })

    plan_table_contract = str((plan.get("contract_hashes") or {}).get("table_contract") or "")

    for slot, rel_item, item, candidate_article in sorted(bindings, key=lambda row: row[0]):
        evidence_article = item.get("canonical_article") or {}
        qbind = item.get("quality_binding") or {}

        if rel_item.get("article_origin_gate_status") != "PASS":
            errors.append({"code": "ARTICLE_ORIGIN_GATE_NOT_PASS", "plan_slot": slot})
        if rel_item.get("authoring_process") != ALLOWED_AUTHORING_PROCESS:
            errors.append({
                "code": "ARTICLE_AUTHORING_PROCESS_NOT_APPROVED_ONLY",
                "plan_slot": slot,
                "expected": ALLOWED_AUTHORING_PROCESS,
                "actual": rel_item.get("authoring_process"),
            })
        if rel_item.get("external_rewrite_detected") is not False:
            errors.append({"code": "EXTERNAL_REWRITE_DETECTED", "plan_slot": slot})
        if rel_item.get("content_hash_locked") is not True:
            errors.append({"code": "CONTENT_HASH_NOT_LOCKED", "plan_slot": slot})

        body_html = candidate_article.get("body_html")
        if not isinstance(body_html, str) or not body_html.strip():
            errors.append({"code": "WORDPRESS_CANDIDATE_BODY_HTML_MISSING", "plan_slot": slot})
            continue

        candidate_hash = sha_text(body_html)
        signed_hash = str(rel_item.get("body_html_sha256") or "")
        evidence_body = evidence_article.get("body_html")
        evidence_hash = sha_text(evidence_body) if isinstance(evidence_body, str) else ""

        if not HASH_RE.fullmatch(signed_hash):
            errors.append({"code": "SIGNED_BODY_HTML_HASH_MISSING_OR_INVALID", "plan_slot": slot})
        else:
            if evidence_hash != signed_hash:
                errors.append({
                    "code": "APPROVED_ENVELOPE_BODY_HASH_MISMATCH",
                    "plan_slot": slot,
                    "expected": signed_hash,
                    "actual": evidence_hash,
                })
            if candidate_hash != signed_hash:
                errors.append({
                    "code": "WORDPRESS_CANDIDATE_NOT_BYTE_BOUND_TO_APPROVED_TEXT",
                    "plan_slot": slot,
                    "expected": signed_hash,
                    "actual": candidate_hash,
                })

        audit = parse_html(body_html)

        item_table_contract = str((item.get("contract_hashes") or {}).get("table_contract") or "")
        table_contract = item_table_contract or plan_table_contract
        table_required = bool(HASH_RE.fullmatch(table_contract))
        if table_required:
            if audit.table_count < 1:
                errors.append({"code": "REQUIRED_TABLE_MISSING", "plan_slot": slot})
            elif audit.system_table_count < 1:
                errors.append({"code": "REQUIRED_SYSTEM_129_TABLE_CLASS_MISSING", "plan_slot": slot})
            elif audit.table_row_count < 2 or audit._table_visible_chars < 20:
                errors.append({"code": "REQUIRED_TABLE_EMPTY_OR_STRUCTURALLY_INVALID", "plan_slot": slot})

        registry = qbind.get("portal_link_registry") or {}
        registry_hash = str(qbind.get("portal_link_registry_hash") or "")
        if registry:
            actual_registry_hash = stable_hash(registry)
            if registry_hash != actual_registry_hash:
                errors.append({
                    "code": "PORTAL_LINK_REGISTRY_HASH_MISMATCH",
                    "plan_slot": slot,
                    "expected": registry_hash,
                    "actual": actual_registry_hash,
                })

        allowed: set[tuple[str, str, str]] = set()
        for row in registry.get("entries") or []:
            if not isinstance(row, dict) or row.get("active") is not True:
                continue
            if str(row.get("target_status") or "") != "publish":
                continue
            allowed.add((str(row.get("role") or ""), str(row.get("href") or ""), norm_text(row.get("anchor"))))

        required: set[tuple[str, str, str]] = set()
        for row in qbind.get("link_bindings") or []:
            if not isinstance(row, dict):
                continue
            required.add((str(row.get("role") or ""), str(row.get("href") or ""), norm_text(row.get("anchor"))))

        visible = {(row["role"], row["href"], row["anchor"]) for row in audit.links}

        for link in sorted(visible):
            if link not in allowed:
                errors.append({
                    "code": "UNBOUND_OR_DISALLOWED_VISIBLE_LINK",
                    "plan_slot": slot,
                    "role": link[0],
                    "href": link[1],
                    "anchor": link[2],
                })
        for link in sorted(required):
            if link not in visible:
                errors.append({
                    "code": "REQUIRED_BOUND_LINK_MISSING",
                    "plan_slot": slot,
                    "role": link[0],
                    "href": link[1],
                    "anchor": link[2],
                })

    return {
        "ok": not errors,
        "status": "PASS" if not errors else "BLOCKED",
        "guard": "PFERDE_ATELIER_WORDPRESS_PREWRITE_CONTENT_CONTRACT_GATE_V1",
        "read_only": True,
        "wordpress_write_allowed": not errors,
        "errors": errors,
    }


def main(evidence_path: str, candidate_path: str) -> int:
    evidence = json.loads(Path(evidence_path).read_text(encoding="utf-8"))
    candidate = json.loads(Path(candidate_path).read_text(encoding="utf-8"))
    result = validate(evidence, candidate)
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0 if result["ok"] else 2


if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("usage: wordpress_prewrite_gate.py APPROVED_ENVELOPE.json WORDPRESS_CANDIDATE.json", file=sys.stderr)
        sys.exit(64)
    sys.exit(main(sys.argv[1], sys.argv[2]))
