#!/usr/bin/env python3
"""ONE-TIME competence acceptance for the EXISTING external SEO owner.
Reads the same untouched MINI 100 keywords and the owner's normal reply.
No new agent, no WordPress import hook, no runtime second SEO review.
Usage:
  python3 test_single_existing_seo_worker_acceptance.py MINI_100_...json EXTERNAL_OWNER_REPLY.json
  python3 test_single_existing_seo_worker_acceptance.py --selftest MINI_100_...json
No PASS can be claimed for the real worker from --selftest (which uses mock replies).
"""
import json
import sys
from pathlib import Path

# Fixed independent editorial counterexamples from the ACTUAL 100-keyword
# file. A change in wording of the file fails rather than silently rematching.
DUPLICATE_INTENT_GROUPS = (
    ("günstige regendecken für pferde", "pferde regendecken günstig"),
    ("regendecke pferd 0g", "regendecke pferd ungefüttert"),
    ("pferde regendecken im test", "regendecken im test", "regendecken für pferde im test"),
)
AMBIGUOUS_SOURCE_QUERIES = ("pferd", "pferd decken")
DISTINCT_INTENT_PAIRS = (
    ("schleich pferdeanhänger", "pferdeanhänger 2 pferde"),
    ("pferdeanhänger mieten", "pferdeanhänger gebraucht kaufen"),
    ("pferdeanhänger 4 pferde", "pferdeanhänger 2 pferde"),
)

def load_original(path):
    original = json.loads(Path(path).read_text(encoding="utf-8"))
    rows = original.get("items", [])
    eligible = [r for r in rows if r.get("decision") == "JA"]
    assert len(rows) == 100 and len(eligible) == 87, "Original-100-Keyword-File changed"
    all_raw = {r["raw_query"] for r in eligible}
    for group in DUPLICATE_INTENT_GROUPS + (AMBIGUOUS_SOURCE_QUERIES,) + DISTINCT_INTENT_PAIRS:
        assert set(group) <= all_raw, "Editorial acceptance fixture and original source differ: " + str(group)
    return eligible

def assess(original, document):
    errors = []
    if document.get("contract") != "PSTE_MINI_SEO_DECISIONS_V1" or document.get("owner") != "EXTERNAL_SINGLE_SEO_EDITOR":
        return ["WRONG_EXTERNAL_OWNER_CONTRACT"]
    outputs = document.get("items")
    if not isinstance(outputs, list):
        return ["EXTERNAL_OWNER_RESULTS_MISSING"]
    expected = {r["raw_query"] for r in original}
    by_raw = {}
    for i, row in enumerate(outputs):
        if not isinstance(row, dict):
            errors.append(f"ITEM_{i}_MALFORMED")
            continue
        raw = row.get("raw_query")
        if not isinstance(raw, str) or raw not in expected:
            errors.append(f"ITEM_{i}_NOT_AN_ORIGINAL_JA_KEYWORD")
            continue
        if raw in by_raw:
            errors.append(f"ITEM_{i}_DUPLICATE_ORIGINAL_KEYWORD")
            continue
        if row.get("box") not in ("FREI", "BELEGT", "KLAERUNG"):
            errors.append(f"ITEM_{i}_UNKNOWN_SEO_DECISION")
            continue
        by_raw[raw] = row
    missing = sorted(expected - set(by_raw))
    if missing:
        errors.append(f"INCOMPLETE_EXTERNAL_WORKER_OUTPUT_{len(missing)}")
    for group in DUPLICATE_INTENT_GROUPS:
        granted = [s for s in group if by_raw.get(s, {}).get("box") == "FREI"]
        if len(granted) > 1:
            errors.append("DUPLICATE_SEARCH_INTENT_WAS_TREATED_AS_MULTIPLE_ARTICLES: " + " / ".join(granted))
    for raw in AMBIGUOUS_SOURCE_QUERIES:
        if by_raw.get(raw, {}).get("box") == "FREI":
            errors.append("UNRESOLVED_BROAD_OR_AMBIGUOUS_ORIGINAL_QUERY_MARKED_FREE: " + raw)
    # Different buyer purposes are different intent slots. This does NOT
    # automatically grant FREI, since the live portal may have the article.
    for a, b in DISTINCT_INTENT_PAIRS:
        x, y = by_raw.get(a, {}), by_raw.get(b, {})
        if x.get("box") == y.get("box") == "FREI" and x.get("intent_slot") == y.get("intent_slot"):
            errors.append(f"DISTINCT_INTENTS_MERGED_IN_ONE_SLOT: {a} / {b}")
    return errors

def synthetic(original):
    # These are TEST ANSWERS, NOT verdicts about the actual WordPress portal.
    output = []
    for i, row in enumerate(original):
        raw = row["raw_query"]
        output.append({
            "pool_key": f"test-{i + 1}",
            "raw_query": raw,
            "box": "KLAERUNG",
            "intent_slot": "",
            "intent_summary": "Current live content not available",
        })
    return {"contract": "PSTE_MINI_SEO_DECISIONS_V1",
        "owner": "EXTERNAL_SINGLE_SEO_EDITOR", "items": output}

def selftest(path):
    original = load_original(path)
    doc = synthetic(original)
    assert not assess(original, doc), "Conservative mock should be accepted"
    # A known wrong quality decision must FAIL, despite perfect JSON shape.
    for group in DUPLICATE_INTENT_GROUPS:
        bad = json.loads(json.dumps(doc))
        for row in bad["items"]:
            if row["raw_query"] in group:
                row["box"] = "FREI"
                row["intent_slot"] = "different-" + row["raw_query"]
        assert any(e.startswith("DUPLICATE_SEARCH_INTENT_WAS_TREATED")
                   for e in assess(original, bad)), "Known semantic duplicate was not caught"
    for raw in AMBIGUOUS_SOURCE_QUERIES:
        bad = json.loads(json.dumps(doc))
        next(row for row in bad["items"] if row["raw_query"] == raw)["box"] = "FREI"
        assert any(e.startswith("UNRESOLVED_BROAD_OR_AMBIGUOUS")
                   for e in assess(original, bad)), "Ambiguous input was incorrectly accepted"
    bad = json.loads(json.dumps(doc))
    bad["items"].pop()
    assert any(e.startswith("INCOMPLETE_EXTERNAL_WORKER_OUTPUT") for e in assess(original, bad))
    print("PASS one-time competence acceptance: 87 original eligible topics, overlap + ambiguous + incomplete negative cases")
    print("NOT A REAL WORKER PASS: no external SEO owner verdicts or WordPress live inventory supplied")


# ONE-TIME read-only acceptance of the REAL TEST-WordPress export, NOT a
# runtime worker and NOT a second semantic decision after the external owner.
import hashlib
import re

_SHA256 = re.compile(r"^[a-f0-9]{64}$")
_REQUIRED = (
    "WORDPRESS", "PSTE_PLAN", "PSERC_ACTIVE_PLAN",
    "PPM679_EXISTING_EDITORIAL_RUNTIME", "MINI_RESERVED",
)
_REFERENCE_FIELDS = (
    "id", "post_id", "pool_key", "seo_topic_id",
    "canonical_article_id", "record_index", "intent_slot", "plan_slot",
)

def check_full_export(payload):
    errors = []
    if not isinstance(payload, dict) or payload.get("contract") != "PSTE_MINI_RESULTS_FOR_EDITORIAL_V1":
        return ["WP_EXPORT_CONTRACT_MISSING_OR_INCORRECT"]
    park = payload.get("parkhaus_snapshot")
    if not isinstance(park, dict) or payload.get("parkhaus_complete") is not True or park.get("complete") is not True:
        return ["WP_PARKHAUS_NOT_COMPLETE"]
    if park.get("contract") != "PSTE_MINI_PARKHAUS_SNAPSHOT_V1" or not _SHA256.fullmatch(str(park.get("sha256", ""))):
        errors.append("WP_PARKHAUS_BINDING_MISSING")
    sources = park.get("sources")
    items = park.get("items")
    subjects = payload.get("seo_subjects")
    if not isinstance(sources, dict) or not isinstance(items, list):
        return errors + ["WP_PARKHAUS_SOURCES_OR_ITEMS_MISSING"]
    for source in _REQUIRED:
        data = sources.get(source)
        if not isinstance(data, dict):
            errors.append("MISSING_SOURCE_" + source)
            continue
        if source in ("WORDPRESS", "PSTE_PLAN", "PSERC_ACTIVE_PLAN", "MINI_RESERVED") and data.get("complete") is not True:
            errors.append("INCOMPLETE_SOURCE_" + source)
        if source == "PPM679_EXISTING_EDITORIAL_RUNTIME":
            # The actual saved plan must not silently be treated as absent
            # OR as an empty newly initialized test plan.
            if data.get("complete") is not True or data.get("status") != "PRESENT":
                errors.append("SAVED_EDITORIAL_PLAN_NOT_VERIFIED_PRESENT")
            if not isinstance(data.get("item_count"),int) or data["item_count"] <= 0:
                errors.append("SAVED_EDITORIAL_PLAN_EMPTY_NOT_THE_EXISTING_PLAN")
        if source == "WORDPRESS" and (not isinstance(data.get("item_count"),int) or data["item_count"] <= 0):
            errors.append("WP_EMPTY_ARTICLE_INVENTORY_CANNOT_PROVE_COVERAGE")
        quantity = data.get("item_count")
        actual = sum(1 for item in items if isinstance(item, dict) and item.get("source") == source)
        if not isinstance(quantity, int) or quantity != actual:
            errors.append("SOURCE_COUNT_MISMATCH_" + source)
    if not isinstance(sources.get("EDITORIAL_PLAN"), dict):
        errors.append("PSTE_EDITORIAL_PLAN_SOURCE_NOT_DECLARED")
    active = sources.get("PSERC_ACTIVE_PLAN", {})
    if isinstance(active, dict) and not _SHA256.fullmatch(str(active.get("snapshot_sha256", ""))):
        errors.append("PSERC_ACTIVE_PLAN_SNAPSHOT_MISSING")
    if not isinstance(subjects, list) or not subjects:
        return errors + ["NO_ACTUAL_JA_SOURCE_QUERIES"]
    completed = payload.get("items")
    if not isinstance(completed, list):
        return errors + ["ORIGINAL_STORED_MINI_RESULTS_MISSING"]
    raw_completed = {}
    for idx, row in enumerate(completed):
        if not isinstance(row, dict):
            errors.append(f"STORED_MINI_ROW_{idx}_MALFORMED")
            continue
        raw = row.get("raw_query")
        if not isinstance(raw, str) or not raw:
            errors.append(f"STORED_MINI_ROW_{idx}_NO_RAW_QUERY")
            continue
        if raw in raw_completed:
            errors.append("AMBIGUOUS_REPEAT_OF_SAVED_RAW_QUERY_" + raw)
        raw_completed[raw] = row
    seen = set()
    for idx, item in enumerate(subjects):
        if not isinstance(item, dict):
            errors.append(f"SEO_SUBJECT_{idx}_MALFORMED")
            continue
        key, raw, identity = item.get("pool_key"), item.get("raw_query"), item.get("source_sha256")
        if not isinstance(key, str) or not key or key in seen:
            errors.append(f"SEO_SUBJECT_{idx}_INVALID_OR_REPEATED_POOL_KEY")
        if isinstance(key, str):
            seen.add(key)
        if not isinstance(raw, str) or not raw or not isinstance(identity, str) or (
            identity != hashlib.sha256((str(key) + "|" + str(raw)).encode("utf-8")).hexdigest()
        ):
            errors.append(f"SEO_SUBJECT_{idx}_ORIGINAL_SOURCE_CHANGED")
            continue
        saved = raw_completed.get(raw)
        if not isinstance(saved, dict) or saved.get("decision") != "JA":
            errors.append(f"SEO_SUBJECT_{idx}_NOT_SAVED_JA")
            continue
        titles = saved.get("titles")
        if not isinstance(titles, list) or not titles or not isinstance(titles[0], dict) or not titles[0].get("title"):
            errors.append(f"SEO_SUBJECT_{idx}_HAS_NO_ORIGINAL_APPROVED_TITLE")
    if payload.get("count") != len(completed):
        errors.append("SAVED_MINI_TOTAL_NOT_AS_DECLARED")
    expected_ja = sum(1 for row in completed if isinstance(row, dict) and row.get("decision") == "JA")
    if len(subjects) != expected_ja:
        errors.append("NOT_ALL_SAVED_JA_HAVE_SOURCE_IDENTITIES")
    return errors

def check_real_owner_reply(export, reply, original_100=None):
    errors = check_full_export(export)
    if errors:
        return errors
    if not isinstance(reply, dict) or reply.get("contract") != "PSTE_MINI_SEO_DECISIONS_V1" or reply.get("owner") != "EXTERNAL_SINGLE_SEO_EDITOR":
        return ["EXTERNAL_SEO_OWNER_CONTRACT_INVALID"]
    park = export["parkhaus_snapshot"]
    if reply.get("snapshot_sha256") != park["sha256"]:
        errors.append("EXTERNAL_SEO_OWNER_INVENTORY_CHANGED")
    expected = {row["pool_key"]: row for row in export["seo_subjects"]}
    titles = {r["raw_query"]: r["titles"][0]["title"]
              for r in export["items"] if isinstance(r, dict) and r.get("decision") == "JA" and r.get("titles")}
    authoritative_refs = set()
    occupied = set()
    for item in park["items"]:
        if not isinstance(item, dict):
            continue
        src = item.get("source")
        if not isinstance(src, str):
            continue
        for field in _REFERENCE_FIELDS:
            value = item.get(field)
            if not isinstance(value, (str, int)) or isinstance(value, bool):
                continue
            name = str(value).strip()
            if name and not (field in ("post_id", "id") and (not name.isdigit() or int(name) <= 0)):
                authoritative_refs.add(src + ":" + name)
        if src != "MINI_RESERVED":
            for field in ("intent_slot", "plan_slot"):
                slot = item.get(field)
                if isinstance(slot, str) and _SHA256.fullmatch(slot):
                    occupied.add(slot)
    verdicts = reply.get("items")
    if not isinstance(verdicts, list):
        return errors + ["EXTERNAL_SEO_OWNER_ITEMS_MISSING"]
    seen, free_slots = set(), {}
    quality_by_raw = {}
    for i, row in enumerate(verdicts):
        if not isinstance(row, dict):
            errors.append(f"OWNER_RESULT_{i}_MALFORMED")
            continue
        key = row.get("pool_key")
        if not isinstance(key, str) or key not in expected or key in seen:
            errors.append(f"OWNER_RESULT_{i}_UNKNOWN_OR_DUPLICATE_SOURCE")
            continue
        seen.add(key)
        subj = expected[key]
        raw = subj["raw_query"]
        if row.get("raw_query") != raw or row.get("source_sha256") != subj["source_sha256"]:
            errors.append("OWNER_SOURCE_BINDING_CHANGED_" + key)
            continue
        box = row.get("box")
        if box not in ("FREI", "BELEGT", "KLAERUNG"):
            errors.append("OWNER_INVALID_BOX_" + key)
            continue
        quality_by_raw[raw] = row
        if box == "FREI":
            slot = row.get("intent_slot")
            if row.get("approved_title") != titles.get(raw) or not isinstance(row.get("intent_summary"), str) or not row["intent_summary"].strip():
                errors.append("OWNER_FREE_TITLE_OR_INTENT_MISSING_" + key)
            if not isinstance(slot, str) or not _SHA256.fullmatch(slot):
                errors.append("OWNER_FREE_SLOT_INVALID_" + key)
            elif slot in occupied or (slot in free_slots and free_slots[slot] != key):
                errors.append("OWNER_FREE_SLOT_ALREADY_OCCUPIED_" + key)
            else:
                free_slots[slot] = key
        elif box == "BELEGT":
            ref = row.get("matched_ref")
            if not isinstance(ref, str) or ref not in authoritative_refs:
                errors.append("OWNER_BELEGT_HAS_NO_EXISTING_SOURCE_" + key)
        elif not isinstance(row.get("reason"), str) or not row["reason"].strip():
            errors.append("OWNER_KLAERUNG_WITHOUT_SPECIFIC_REASON_" + key)
    if seen != set(expected):
        errors.append("OWNER_RESULT_INCOMPLETE_" + str(len(set(expected) - seen)))
    if not any(row.get("box") in ("FREI", "BELEGT") for row in verdicts if isinstance(row, dict)):
        errors.append("EXTERNAL_OWNER_ONLY_UNDECIDED_NO_COMPETENCE_SHOWN")
    # The existing one-time semantic competence check is reused once, rather
    # than being cloned into another production worker.
    if original_100 is not None:
        expected_raw = {r["raw_query"] for r in original_100}
        actual_raw = {v["raw_query"] for v in export["seo_subjects"]}
        if not expected_raw <= actual_raw:
            errors.append("ORIGINAL_87_JA_NOT_PRESENT_IN_REAL_WORDPRESS_EXPORT")
        else:
            subset = dict(reply, items=[quality_by_raw[raw] for raw in expected_raw if raw in quality_by_raw])
            errors.extend(assess(original_100, subset))
    return errors

def run_io_selftest(original_100_path):
    original = load_original(original_100_path)
    complete = []
    subjects = []
    for i, row in enumerate(original):
        raw = row["raw_query"]
        complete.append(dict(raw_query=raw, decision="JA", titles=row["titles"]))
        key = "real-demo-" + str(i)
        subjects.append(dict(pool_key=key, raw_query=raw,
                             source_sha256=hashlib.sha256((key+"|"+raw).encode()).hexdigest()))
    sources = {source:dict(complete=True, item_count=0) for source in _REQUIRED}
    sources["WORDPRESS"]["item_count"] = 1
    sources["PPM679_EXISTING_EDITORIAL_RUNTIME"].update(status="PRESENT", item_count=1)
    sources["PSERC_ACTIVE_PLAN"]["snapshot_sha256"] = "a"*64
    sources["EDITORIAL_PLAN"] = dict(status="NOT_AVAILABLE", item_count=0)
    export = dict(contract="PSTE_MINI_RESULTS_FOR_EDITORIAL_V1", count=len(complete),
        items=complete, seo_subjects=subjects, parkhaus_complete=True,
        parkhaus_snapshot=dict(contract="PSTE_MINI_PARKHAUS_SNAPSHOT_V1",
            complete=True, sha256="b"*64, sources=sources,
            items=[dict(source="WORDPRESS",id=5,title="Synthetic real-page reference"),
                   dict(source="PPM679_EXISTING_EDITORIAL_RUNTIME",
                        canonical_article_id="existing-canonical",title="Synthetic saved plan")]))
    assert check_full_export(export) == [], check_full_export(export)
    verdicts = []
    for source in subjects:
        verdicts.append(dict(**source, box="KLAERUNG", reason="Original source answer remains unverified",
                             intent_slot="", matched_ref="", approved_title="",
                             intent_summary="Unverified"))
    reply = dict(contract="PSTE_MINI_SEO_DECISIONS_V1",owner="EXTERNAL_SINGLE_SEO_EDITOR",
                 snapshot_sha256="b"*64, items=verdicts)
    # The selftest needs exactly one VALID mock decisive case for the
    # competence check; it is not a real portal decision.
    chosen = next(v for v in verdicts if v["raw_query"] == "horseware regendecken")
    chosen["box"] = "FREI"
    chosen["approved_title"] = next(r["titles"][0]["title"] for r in complete if r["raw_query"] == chosen["raw_query"])
    chosen["intent_slot"] = "c"*64
    chosen["intent_summary"] = "Specific synthetic Horseware owner intent"
    assert check_real_owner_reply(export,reply,original) == [], check_real_owner_reply(export,reply,original)
    failures = []
    stale = dict(reply,snapshot_sha256="0"*64)
    failures.append(any("INVENTORY_CHANGED" in e for e in check_real_owner_reply(export,stale,original)))
    missing = dict(export,parkhaus_snapshot=dict(export["parkhaus_snapshot"],
        sources={**sources, "PPM679_EXISTING_EDITORIAL_RUNTIME":dict(complete=True,status="NOT_PRESENT",item_count=1)}))
    failures.append(any("SAVED_EDITORIAL_PLAN_NOT_VERIFIED_PRESENT" in e for e in check_full_export(missing)))
    empty_saved = json.loads(json.dumps(export))
    empty_saved["parkhaus_snapshot"]["sources"]["PPM679_EXISTING_EDITORIAL_RUNTIME"]["item_count"] = 0
    empty_saved["parkhaus_snapshot"]["items"] = [
        row for row in empty_saved["parkhaus_snapshot"]["items"]
        if row.get("source") != "PPM679_EXISTING_EDITORIAL_RUNTIME"
    ]
    failures.append(any("SAVED_EDITORIAL_PLAN_EMPTY_NOT_THE_EXISTING_PLAN" in e
                        for e in check_full_export(empty_saved)))
    malformed = dict(reply,items=verdicts[:-1])
    failures.append(any("INCOMPLETE" in e for e in check_real_owner_reply(export,malformed,original)))
    forged = json.loads(json.dumps(reply))
    forged["items"][0]["box"] = "BELEGT"
    forged["items"][0]["matched_ref"] = "WORDPRESS:99999"
    failures.append(any("NO_EXISTING_SOURCE" in e for e in check_real_owner_reply(export,forged,original)))
    colliding = json.loads(json.dumps(reply))
    colliding["items"].append(dict(colliding["items"][0]))
    failures.append(any("DUPLICATE_SOURCE" in e for e in check_real_owner_reply(export,colliding,original)))
    occupied = json.loads(json.dumps(export))
    occupied["parkhaus_snapshot"]["items"][0]["plan_slot"] = "c"*64
    failures.append(any("ALREADY_OCCUPIED" in e for e in check_real_owner_reply(occupied,reply,original)))
    broken_source = json.loads(json.dumps(reply))
    broken_source["items"][0]["source_sha256"] = "0"*64
    failures.append(any("SOURCE_BINDING_CHANGED" in e for e in check_real_owner_reply(export,broken_source,original)))
    assert all(failures), ["negative case not rejected", failures]
    print("PASS REAL-EXPORT PREFLIGHT SELFTEST: complete existing sources + source keys + 8 targeted negative cases")
    print("MOCK DATA ONLY: no WordPress access, no external SEO verdict, no K0 claim")

if __name__ == "__main__":
    if len(sys.argv) == 3 and sys.argv[1] == "--selftest":
        selftest(sys.argv[2])
    elif len(sys.argv) == 3 and sys.argv[1] == "--io-selftest":
        run_io_selftest(sys.argv[2])
    elif len(sys.argv) == 3 and sys.argv[1] == "--preflight":
        issues = check_full_export(json.loads(Path(sys.argv[2]).read_text(encoding="utf-8")))
        for issue in issues: print("FAIL",issue)
        print("REAL_WORDPRESS_EXPORT", "TECHNICALLY_COMPLETE" if not issues else "NOT_READY")
        raise SystemExit(bool(issues))
    elif len(sys.argv) in (4,5) and sys.argv[1] == "--verify":
        real_export=json.loads(Path(sys.argv[2]).read_text(encoding="utf-8"))
        real_reply=json.loads(Path(sys.argv[3]).read_text(encoding="utf-8"))
        fixed=load_original(sys.argv[4]) if len(sys.argv)==5 else None
        issues=check_real_owner_reply(real_export,real_reply,fixed)
        for issue in issues: print("FAIL",issue)
        print("ONE_TIME_SEO_OWNER_ACCEPTANCE", "TECHNICAL_AND_FIXED_CASES_PASS" if not issues else "NOT_APPROVED")
        print("REAL_STAGING_END_TO_END", "NOT_TESTED_BY_THIS_SCRIPT")
        raise SystemExit(bool(issues))
    elif len(sys.argv) == 3 and not sys.argv[1].startswith("--"):
        original = load_original(sys.argv[1])
        result = assess(original, json.loads(Path(sys.argv[2]).read_text(encoding="utf-8")))
        for issue in result: print("FAIL",issue)
        print("REAL_EXTERNAL_WORKER_QUALITY", "FIXED_TEST_CASES_PASS" if not result else "NOT_APPROVED")
        raise SystemExit(bool(result))
    else:
        raise SystemExit(__doc__)
