#!/usr/bin/env python3
from __future__ import annotations

import copy
import hashlib
import importlib.util
from pathlib import Path

HERE = Path(__file__).resolve().parent
GATE = HERE / "wordpress_prewrite_gate.py"
spec = importlib.util.spec_from_file_location("wordpress_prewrite_gate", GATE)
mod = importlib.util.module_from_spec(spec)
assert spec.loader is not None
spec.loader.exec_module(mod)

SLOT = "a" * 64
CID = "article:test-approved-only"
TABLE_CONTRACT = "b" * 64


def body(table=True, extra_external=False, drop_further=False, wrong_table_class=False):
    table_html = ""
    if table:
        cls = "comparison-table" if wrong_table_class else "system-129-table comparison-table"
        table_html = (
            '<section data-block="table"><h2>Vergleich</h2>'
            f'<table class="{cls}"><thead><tr><th>Kriterium</th><th>Prüfung</th></tr></thead>'
            '<tbody><tr><td>A</td><td>B</td></tr><tr><td>C</td><td>D</td></tr></tbody></table></section>'
        )
    links = [
        '<a data-link-role="parent_category" href="/stall/">Stall und Haltung</a>',
        '<a data-link-role="semantic_related" href="/stall/boxen/">Boxen</a>',
    ]
    if not drop_further:
        links.append('<a data-link-role="further_information" href="/stall/boxen/matten/">Boxenmatten</a>')
    if extra_external:
        links.append('<a href="https://example.org/source">Externe Quelle</a>')
    return '<article data-article-type="Beratung">' + table_html + '<p>' + ' '.join(links) + '</p></article>'


def fixture(html=None):
    html = html or body()
    registry = {
        "contract": "portal_link_registry_snapshot_v2",
        "entries": [
            {"role":"parent_category","href":"/stall/","anchor":"Stall und Haltung","active":True,"target_status":"publish"},
            {"role":"semantic_related","href":"/stall/boxen/","anchor":"Boxen","active":True,"target_status":"publish"},
            {"role":"further_information","href":"/stall/boxen/matten/","anchor":"Boxenmatten","active":True,"target_status":"publish"},
        ],
    }
    qbind = {
        "link_bindings": [
            {"role":"parent_category","href":"/stall/","anchor":"Stall und Haltung"},
            {"role":"semantic_related","href":"/stall/boxen/","anchor":"Boxen"},
            {"role":"further_information","href":"/stall/boxen/matten/","anchor":"Boxenmatten"},
        ],
        "portal_link_registry": registry,
        "portal_link_registry_hash": mod.stable_hash(registry),
        "table_value_statement": "Die Tabelle ist für diesen Artikelvertrag erforderlich.",
    }
    h = hashlib.sha256(html.encode("utf-8")).hexdigest()
    return {
        "production_plan": {
            "contract": "production_plan_v4",
            "contract_hashes": {"table_contract": TABLE_CONTRACT},
            "items": [{
                "plan_slot": SLOT,
                "canonical_article_id": CID,
                "article_type": "Beratung",
                "contract_hashes": {"table_contract": TABLE_CONTRACT},
                "canonical_article": {"plan_slot": SLOT, "canonical_article_id": CID, "body_html": html},
                "quality_binding": qbind,
            }],
        },
        "workflow_release": {
            "contract": mod.ALLOWED_RELEASE_CONTRACT,
            "status": "PASS",
            "authoring_role": mod.ALLOWED_AUTHORING_ROLE,
            "sequence": sorted(mod.REQUIRED_SEQUENCE_MARKERS),
            "content_generation_performed_by_supervisor": False,
            "wordpress_write_performed": False,
            "items": [{
                "plan_slot": SLOT,
                "canonical_article_id": CID,
                "body_html_sha256": h,
                "article_origin_gate_status": "PASS",
                "authoring_process": mod.ALLOWED_AUTHORING_PROCESS,
                "external_rewrite_detected": False,
                "content_hash_locked": True,
            }],
        },
    }


def codes(result):
    return {x["code"] for x in result["errors"]}


def assert_pass(name, evidence, candidate):
    r = mod.validate(evidence, candidate)
    assert r["status"] == "PASS", (name, r)
    assert r["read_only"] is True
    assert r["wordpress_write_allowed"] is True
    print("PASS", name)


def assert_block(name, evidence, candidate, code):
    r = mod.validate(evidence, candidate)
    assert r["status"] == "BLOCKED", (name, r)
    assert r["wordpress_write_allowed"] is False
    assert code in codes(r), (name, code, r)
    print("PASS", name, "->", code)


base = fixture()
assert_pass("approved_process_table_and_bound_links", base, copy.deepcopy(base))

old_origin = copy.deepcopy(base)
old_origin["workflow_release"]["authoring_role"] = "CHAT_OR_APPROVED_RESEARCH_TEXT_PROCESS"
old_origin["workflow_release"]["items"][0]["authoring_process"] = "STARTMASTER_0039_CHAT_OR_APPROVED_RESEARCH_TEXT_PROCESS"
assert_block("old_chat_or_origin_is_rejected", old_origin, copy.deepcopy(old_origin), "APPROVED_TEXT_PROCESS_ORIGIN_NOT_PROVEN")

no_table = fixture(body(table=False))
assert_block("required_table_missing", no_table, copy.deepcopy(no_table), "REQUIRED_TABLE_MISSING")

wrong_table = fixture(body(wrong_table_class=True))
assert_block("required_system_table_class_missing", wrong_table, copy.deepcopy(wrong_table), "REQUIRED_SYSTEM_129_TABLE_CLASS_MISSING")

extra_link = fixture(body(extra_external=True))
assert_block("unbound_external_link", extra_link, copy.deepcopy(extra_link), "UNBOUND_OR_DISALLOWED_VISIBLE_LINK")

missing_link = fixture(body(drop_further=True))
assert_block("required_bound_link_missing", missing_link, copy.deepcopy(missing_link), "REQUIRED_BOUND_LINK_MISSING")

late_mutation = copy.deepcopy(base)
late_mutation["production_plan"]["items"][0]["canonical_article"]["body_html"] = body(extra_external=True)
assert_block("late_body_rewrite_after_approval", base, late_mutation, "WORDPRESS_CANDIDATE_NOT_BYTE_BOUND_TO_APPROVED_TEXT")

bad_registry = copy.deepcopy(base)
bad_registry["production_plan"]["items"][0]["quality_binding"]["portal_link_registry"]["entries"][0]["href"] = "/manipulated/"
assert_block("link_registry_hash_tamper", bad_registry, copy.deepcopy(bad_registry), "PORTAL_LINK_REGISTRY_HASH_MISMATCH")

print("ALL_WORDPRESS_PREWRITE_GATE_TESTS_PASS")
