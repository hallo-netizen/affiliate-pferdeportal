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

if __name__ == "__main__":
    if len(sys.argv) == 3 and sys.argv[1] == "--selftest":
        selftest(sys.argv[2])
    elif len(sys.argv) == 3:
        original = load_original(sys.argv[1])
        result = assess(original, json.loads(Path(sys.argv[2]).read_text(encoding="utf-8")))
        for issue in result:
            print("FAIL", issue)
        print("REAL_EXTERNAL_WORKER_QUALITY", "PASS" if not result else "NOT_APPROVED")
        raise SystemExit(1 if result else 0)
    else:
        raise SystemExit(__doc__)
