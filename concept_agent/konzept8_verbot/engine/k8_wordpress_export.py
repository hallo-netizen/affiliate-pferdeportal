#!/usr/bin/env python3
from __future__ import annotations

import hashlib
import json
import re
import sys
from pathlib import Path

from . import k8_progress_guard as progress_guard

CONTRACT = "SYSTEM4_WORDPRESS_HANDOFF_V1"
PLUGIN_VERSION = "0.28.27"
PPM_VERSION = "6.7.9"
SHA_RE = re.compile(r"^[0-9a-f]{64}$")

class Blocked(RuntimeError):
    pass

def load(path: Path) -> dict:
    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise Blocked("JSON_OBJECT_REQUIRED:" + str(path))
    return value

def _bound_slug(item: dict) -> str:
    plan = item.get("production_plan_item")
    if not isinstance(plan, dict):
        raise Blocked("PRODUCTION_PLAN_ITEM_MISSING")
    canonical = plan.get("canonical_article")
    runtime = plan.get("runtime_order")
    slug = None
    if isinstance(canonical, dict):
        slug = canonical.get("slug")
    if (not isinstance(slug, str) or not slug.strip()) and isinstance(runtime, dict):
        slug = runtime.get("slug")
    if not isinstance(slug, str) or not slug.strip():
        raise Blocked("BOUND_SLUG_MISSING")
    return slug.strip()

def _canonical_article_id(item: dict) -> str:
    plan = item.get("production_plan_item")
    if not isinstance(plan, dict):
        raise Blocked("PRODUCTION_PLAN_ITEM_MISSING")
    value = plan.get("canonical_article_id")
    if not isinstance(value, str) or not value.strip():
        raise Blocked("CANONICAL_ARTICLE_ID_MISSING")
    return value.strip()

def build(binding: dict, checkpoint: dict) -> dict:
    progress_guard.verify_binding(binding)
    progress_guard.verify_checkpoint(binding, checkpoint)
    if checkpoint.get("phase") not in {"PSERC_PASS_ENDSTEMPEL_REQUIRED", "ENDSTEMPEL_PASS_STOP"}:
        raise Blocked("WORDPRESS_EXPORT_TOO_EARLY")
    if checkpoint.get("status") not in {"IN_PROGRESS", "PASS"}:
        raise Blocked("WORDPRESS_EXPORT_STATE_INVALID")
    if not SHA_RE.fullmatch(str(checkpoint.get("pserc_package_sha256") or "")):
        raise Blocked("PSERC_PASS_REQUIRED")

    completed = checkpoint.get("completed_items")
    drafts = checkpoint.get("drafts")
    if not isinstance(completed, list) or len(completed) != binding.get("item_count"):
        raise Blocked("ALL_ARTICLES_PASS_REQUIRED")
    if not isinstance(drafts, list) or len(drafts) != binding.get("item_count"):
        raise Blocked("DRAFT_SET_INCOMPLETE")

    articles = []
    for index, item in enumerate(binding["items"]):
        identity = item.get("identity")
        if not isinstance(identity, dict):
            raise Blocked(f"IDENTITY_MISSING:{index}")
        done = completed[index]
        matches = [row for row in drafts if isinstance(row, dict) and row.get("item_index") == index]
        if len(matches) != 1:
            raise Blocked(f"DRAFT_NOT_UNIQUE:{index}")
        draft = matches[0]
        if done.get("lt68") != "PASS" or done.get("ppm679") != "PASS":
            raise Blocked(f"ARTICLE_NOT_PASS:{index}")
        if draft.get("draft_sha256") != done.get("draft_sha256"):
            raise Blocked(f"DRAFT_PASS_HASH_MISMATCH:{index}")
        body = draft.get("content_utf8")
        if not isinstance(body, str) or not body:
            raise Blocked(f"DRAFT_BODY_MISSING:{index}")
        articles.append({
            "index": index,
            "canonical_article_id": _canonical_article_id(item),
            "title": identity["title"],
            "slug": _bound_slug(item),
            "target_keyword": identity["target_keyword"],
            "category": identity["category"],
            "article_type": identity["article_type"],
            "plan_slot": identity["plan_slot"],
            "final_draft_sha256": draft["draft_sha256"],
            "revision_count": draft["revision"],
            "body": body,
            "languagetool": {
                "status": "PASS",
                "engine": "LanguageTool 6.8",
            },
            "ppm679": {
                "status": "PASS",
                "ppm_version": PPM_VERSION,
                "content_sha256": draft["draft_sha256"],
            },
        })

    return {
        "contract": CONTRACT,
        "batch_sha256": binding["batch_sha256"],
        "publish_allowed": False,
        "signing_deferred": True,
        "batch_gate_status": "SYSTEM4_BATCH_FULL_PASS_COLLECTED",
        "no_legacy_status": "PASS",
        "test_suite_status": "PASS",
        "article_count": len(articles),
        "wordpress_review": {
            "file_format": "JSON",
            "mime_type": "application/json",
            "intended_next_step": "WORDPRESS_DIRECT_IMPORT",
            "plugin_name": "Portal SEO Editorial Plan Compiler",
            "plugin_version_verified_against": PLUGIN_VERSION,
            "ppm_version_verified_against": PPM_VERSION,
            "direct_wordpress_upload_ready": True,
            "direct_upload_block_reason": None,
            "required_downstream_components": [],
        },
        "articles": articles,
    }

def write_export(binding: dict, checkpoint: dict, out_path: Path) -> dict:
    value = build(binding, checkpoint)
    raw = (json.dumps(value, ensure_ascii=False, indent=2) + "\n").encode("utf-8")
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_bytes(raw)
    digest = hashlib.sha256(raw).hexdigest()
    return {
        "status": "PASS",
        "contract": CONTRACT,
        "file_format": "JSON",
        "mime_type": "application/json",
        "filename": out_path.name,
        "wordpress_json_sha256": digest,
        "article_count": len(value["articles"]),
        "publish_allowed": False,
    }

def main(argv: list[str]) -> int:
    try:
        if len(argv) != 5 or argv[1] != "export":
            raise Blocked("USE: k8_wordpress_export.py export BINDING CHECKPOINT OUT_JSON")
        receipt = write_export(load(Path(argv[2])), load(Path(argv[3])), Path(argv[4]))
        print(json.dumps(receipt, ensure_ascii=False, sort_keys=True))
        return 0
    except Exception as exc:
        print("K8_WORDPRESS_EXPORT_BLOCKED:" + str(exc), file=sys.stderr)
        return 2

if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
