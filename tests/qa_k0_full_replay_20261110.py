"""Read-only QA replay of an already completed K0 draft using the cleaned K0 rule bundle.

No production workflow, credentials, WordPress writes or newly researched article content.
"""
from __future__ import annotations

import argparse
import copy
import hashlib
import json
import tempfile
from pathlib import Path

from engine.k0_portal_resolver import load as load_json, resolve, validate_intake
from engine.k0_writer_station import prepare, seal, verify as verify_writer, Blocked as WriterBlocked
from engine.k0_production_gate import verify as verify_production
from engine.k0_full_rules import verify_pre_lt68, verify_final
from engine.lt68_external import run as run_lt
from engine.k0_wordpress_export import build as build_wordpress, verify_export
from engine.core import stable
from engine.k0_seo_owner_binding import bind_context

ROOT = Path(__file__).resolve().parents[1]
RUN_PREFIX = "k0-20261110-42619ca7-"
BATCH_DIR = ROOT / "real_runs/k0/batch-20261110-42619ca7"


def load(path):
    return json.loads(Path(path).read_text(encoding="utf-8"))


def check(value, label):
    if not value:
        raise AssertionError(label)
    print("PASS", label)
    return True


def main(jar):
    checks = []
    original_batch = load(BATCH_DIR / "BATCH_INTAKE.json")
    rows = validate_intake(original_batch)
    assert len(rows) == 3
    check(len(rows) == 3, "PSERC_ORIGINAL_THREE_ITEM_BATCH")
    registry = load(ROOT / "K0_PORTAL_REGISTRY.json")
    # Synthetic upstream snapshot: isolated QA only, never claim live PSERC provenance.
    source_manifest = load(ROOT / "tests/fixtures/k0_seo_owner_manifest_SYNTHETIC_QA_20261110.json")

    jobs = []
    intakes = []
    portals = []
    for i in range(1, 4):
        rd = ROOT / ("real_runs/k0/" + RUN_PREFIX + f"{i:02d}-r2")
        intake = load(rd / "WORDPRESS_INTAKE.json")
        identity = validate_intake(intake)[0]
        check(identity == rows[i-1], f"HANDOFF_IDENTITY_UNCHANGED_{i}")
        portal = resolve(intake, registry)
        check(portal["status"] == "PASS" and portal["items"][0]["portal_id"] == "pferdeatelier",
              f"AUTO_PORTAL_ASSIGNMENT_{i}")
        ctx = load(rd / "AUTHORING_CONTEXT.json")
        ctx = bind_context(source_manifest, intake, ctx)
        check(ctx["content_profile"]["seo_owner_manifest_sha256"]==source_manifest["manifest_sha256"], f"ORIGINAL_SEO_OWNER_SOURCE_BOUND_{i}")
        ctx["run_instance_id"] = "run:" + hashlib.sha256(("qa-replay|" + str(rd)).encode()).hexdigest()[:24]
        job = prepare(intake, portal, ctx)
        check(job["writer_rule_binding"]["article_hard_rule_count"] == 81, f"K0_81_RULE_BUNDLE_BEFORE_WRITER_{i}")
        check(job["identity"]["title"] == identity["title"], f"EXTERNAL_TITLE_PRESERVED_{i}")
        check(bool(job["content_profile"].get("search_intent")), f"CONTENT_INTENT_PRESENT_{i}")
        jobs.append(job)
        intakes.append(intake)
        portals.append(portal)

    rd = ROOT / ("real_runs/k0/" + RUN_PREFIX + "01-r2")
    previous_sealed = load(rd / "SEALED_WRITER_PRODUCT.json")
    previous_wordpress = load(rd / "WORDPRESS_SINGLE.json")
    job = jobs[0]
    draft = {
        "contract": "K0_WRITER_DRAFT_V1",
        "job_id": job["job_id"],
        "title": job["identity"]["title"],
        "content_html": previous_sealed["html"],
        "table_decision": copy.deepcopy(job["rule_context"]["table_decision"]),
        "lt_authoritative_terms": copy.deepcopy(previous_sealed["lt_authoritative_terms"]),
        "revision_count": previous_sealed["revision_count"],
        "publish_allowed": False,
    }
    product = seal(job, draft)
    check(verify_writer(job, product)["status"] == "PASS", "NEW_81_RULE_WRITER_SEAL")

    category = previous_wordpress["articles"][0]["production_context"]["production_plan_item"]["quality_binding"]["wordpress_category"]
    check(category["slug"] == job["identity"]["category"] and category["id"] > 0,
          "PREVIOUS_VERIFIED_WORDPRESS_CATEGORY_SNAPSHOT")
    category_payload = [{"id": category["id"], "slug": category["slug"]}]
    production = verify_production(product, portals[0], category_payload)
    check(production["status"] == "PASS", "FULL_K0_PRODUCTION_QUALITY_GATE")
    check(production["all_rules_pre_lt68_status"] == "PASS", "ALL_80_CONTENT_RULES_BEFORE_LT68")
    pre = verify_pre_lt68(product, category_payload)
    check(pre["status"] == "READY_FOR_LT68" and pre["required_receipt_count"] == 80,
          "PRE_LANGUAGE_TOOL_80_RULES")

    with tempfile.TemporaryDirectory(prefix="k0-qa-replay-") as d:
        article_path = Path(d) / "SEALED_WRITER_PRODUCT_QA.json"
        article_path.write_text(json.dumps(product, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        lt = run_lt(Path(jar), article_path)
    check(lt["status"] == "PASS" and lt["finding_count"] == 0, "REAL_LANGUAGE_TOOL_6_8_FRESH_PASS")
    check(lt["html_sha256"] == hashlib.sha256(product["html"].encode()).hexdigest(),
          "LT_HTML_HASH_EQUALS_CURRENT_WRITER_BODY")

    full = verify_final(product, category_payload, lt)
    check(full["status"] == "PASS" and full["article_hard_rule_count"] == 81,
          "K0_FINAL_81_RULES_AFTER_LT68")

    article_id = previous_wordpress["articles"][0]["article_id"]
    plan_slot = job["identity"]["plan_slot"]
    check(hashlib.sha256(("pserc-plan-slot-v2|" + article_id).encode()).hexdigest() == plan_slot,
          "ORIGINAL_CANONICAL_ID_PLAN_SLOT_BOUND")
    bindings = {
        "contract": "K10_CANONICAL_ARTICLE_BINDINGS_V1", "status": "PASS",
        "bindings": {plan_slot: article_id},
    }
    wp = build_wordpress(intakes[0], product, portals[0], production, lt,
                         full, bindings, category_payload)
    verified = verify_export(wp, intakes[0])
    check(verified["status"] == "PASS", "FINAL_SYSTEM4_WORDPRESS_EXPORT_VERIFIED")
    check(wp["articles"][0]["body"] == previous_wordpress["articles"][0]["body"],
          "ORIGINAL_ARTICLE_BODY_UNCHANGED")
    check(wp["articles"][0]["title"] == rows[0]["title"], "WORDPRESS_TITLE_EXTERNAL_PRESERVED")
    check(wp["publish_allowed"] is False, "PUBLISH_UNCONDITIONALLY_FORBIDDEN")

    tampered = dict(draft)
    tampered["title"] = "Noch ein anderer Titel"
    try:
        seal(job, tampered)
    except WriterBlocked:
        check(True, "NEGATIVE_WRITER_CANNOT_CHANGE_APPROVED_TITLE")
    else:
        raise AssertionError("APPROVED_TITLE_MUTATION_WAS_NOT_BLOCKED")

    tampered_prod = copy.deepcopy(product)
    tampered_prod["content_profile"]["search_intent"] = "ILLEGITIMATE_UNBOUND_OVERRIDE"
    try:
        verify_writer(job, tampered_prod)
    except WriterBlocked:
        check(True, "NEGATIVE_WRITER_CANNOT_OVERRIDE_BOUND_INTENT")
    else:
        raise AssertionError("WRITER_INTENT_MUTATION_WAS_NOT_BLOCKED")

    tampered_wp = copy.deepcopy(wp)
    tampered_wp["articles"][0]["title"] = "Nicht freigegeben"
    try:
        verify_export(tampered_wp, intakes[0])
    except Exception:
        check(True, "NEGATIVE_WORDPRESS_TITLE_TAMPERING_BLOCKED")
    else:
        raise AssertionError("WORDPRESS_TITLE_MUTATION_WAS_NOT_BLOCKED")

    report = {
        "contract": "K0_QA_FULL_PIPELINE_REPLAY_20261110",
        "status": "PASS",
        "method": "READ_ONLY_REPLAY_USING_PREVIOUS_VERIFIED_ARTICLE_AND_CATEGORY_SNAPSHOT",
        "dataforseo_live": False,
        "wordpress_live_write": False,
        "fresh_new_research": False,
        "keyword_intent_source_e2e_binding": "NOT_PROVEN_FROM_FIVE_FIELD_HANDOFF",
        "new_rule_count": 81,
        "pre_lt_rule_count": 80,
        "real_lt": True,
        "article_id": article_id,
        "article_body_sha256": hashlib.sha256(product["html"].encode()).hexdigest(),
        "wordPress_export": "SYSTEM4_WORDPRESS_HANDOFF_V1_VALID_AND_UNCHANGED",
        "cases": [
            "THREE_REAL_PSERc_INTAKES_TO_NEW_81_RULE_K0_WRITER_JOBS",
            "ONE_PREVIOUS_ARTICLE_SEALED_WITH_NEW_RULES",
            "ALL_TEXT_FACT_STRUCTURE_GATES_PASS",
            "REAL_LANGUAGE_TOOL_6_8_PASS",
            "FINAL_81_RULE_VERIFY_PASS",
            "WORDPRESS_SINGLE_EXPORT_VERIFY_PASS",
            "NEGATIVE_MUTATION_GATES_PASS",
        ],
        "publish_allowed": False,
    }
    print("QA_REPORT=" + json.dumps(report, ensure_ascii=False, sort_keys=True))
    return report


if __name__ == "__main__":
    ap=argparse.ArgumentParser()
    ap.add_argument("--jar",required=True)
    args=ap.parse_args()
    main(args.jar)
