#!/usr/bin/env python3
import argparse, hashlib, json, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
LEDGER = ROOT / "state" / "ledger.json"
CURRENT_JOB = ROOT / "runtime" / "CURRENT_JOB.json"
WAREHOUSE = ROOT / "warehouse"
STATIONS = ("research", "write", "check", "repair")

class K9Error(RuntimeError):
    pass

def stable(obj):
    raw = json.dumps(obj, ensure_ascii=False, sort_keys=True, separators=(",", ":"))
    return hashlib.sha256(raw.encode("utf-8")).hexdigest()

def load_json(path):
    return json.loads(Path(path).read_text(encoding="utf-8"))

def write_json(path, data):
    p = Path(path)
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(json.dumps(data, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")

def ledger():
    data = load_json(LEDGER)
    if data.get("contract") != "K9_LEDGER_V1" or not isinstance(data.get("items"), list):
        raise K9Error("LEDGER_INVALID")
    return data

def current_job():
    if not CURRENT_JOB.exists():
        return None
    data = load_json(CURRENT_JOB)
    declared = data.get("job_sha256")
    core = dict(data)
    core.pop("job_sha256", None)
    if data.get("contract") != "K9_JOB_V1" or data.get("status") != "OPEN":
        raise K9Error("CURRENT_JOB_INVALID")
    if declared != stable(core):
        raise K9Error("CURRENT_JOB_HASH_INVALID")
    return data

def write_chat_entry(job):
    entry = {
        "contract": "K9_CHAT_ENTRY_V1",
        "concept": "K9",
        "status": "OPEN_JOB_READY_FOR_CHAT",
        "repository": "hallo-netizen/affiliate-pferdeportal",
        "branch": "konzept9/greenfield-20260929",
        "job_path": "runtime/CURRENT_JOB.json",
        "job_id": job["job_id"],
        "job_sha256": job["job_sha256"],
        "station": job["station"],
        "item_count": job["item_count"],
        "allowed_action": "EXECUTE_EXACT_STATION_ONLY",
        "forbidden": [
            "SEARCH_OTHER_CONCEPTS",
            "ROUTE_TO_NEXT_STATION",
            "RECONSTRUCT_JOB",
            "USE_LEGACY_RUNTIME"
        ],
        "completion_rule": "RETURN_ONE_COMPLETE_K9_SUBMISSION_FOR_THIS_EXACT_JOB"
    }
    write_json(CHAT_ENTRY, entry)
    return entry

def eligible(item, station):
    s = item["stages"]
    if station == "research":
        return s["research"] == "PENDING"
    if station == "write":
        return s["research"] == "DONE" and s["write"] == "PENDING"
    if station == "check":
        return s["write"] == "DONE" and s["check"] == "PENDING"
    if station == "repair":
        return s["check"] == "FAIL" and s["repair"] == "PENDING"
    raise K9Error("STATION_INVALID")

def status_report(data=None):
    data = data or ledger()
    result = {"contract": "K9_STATUS_V1", "total": len(data["items"]), "stations": {}}
    for station in STATIONS:
        values = [x["stages"][station] for x in data["items"]]
        result["stations"][station] = {
            key: values.count(key) for key in sorted(set(values) | {"PENDING", "DONE"})
        }
    job = current_job()
    result["active_job"] = None if job is None else {
        key: job[key] for key in ("job_id", "station", "item_count", "item_ids")
    }
    return result

def import_intake(path):
    if current_job() is not None:
        raise K9Error("ACTIVE_JOB_EXISTS")
    source = load_json(path)
    rows = source.get("items")
    if not isinstance(rows, list) or not rows:
        raise K9Error("INTAKE_EMPTY_OR_INVALID")
    data = ledger()
    known = {x["item_id"] for x in data["items"]}
    additions = []
    for row in rows:
        item_id = str(row.get("item_id", "")).strip()
        title = str(row.get("title", "")).strip()
        metadata = row.get("metadata", {})
        if not item_id or not title or item_id in known or not isinstance(metadata, dict):
            raise K9Error("INTAKE_ITEM_INVALID_OR_DUPLICATE")
        known.add(item_id)
        additions.append({
            "item_id": item_id,
            "title": title,
            "metadata": metadata,
            "revision": 0,
            "products": {},
            "stages": {
                "research": "PENDING",
                "write": "PENDING",
                "check": "PENDING",
                "repair": "NOT_REQUIRED"
            }
        })
    data["items"].extend(additions)
    data["generation"] += 1
    write_json(LEDGER, data)
    return {"status": "INTAKE_ACCEPTED", "added": len(additions), "total": len(data["items"])}

def _product_result(item, stage):
    ref = item.get("products", {}).get(stage)
    if not isinstance(ref, dict):
        raise K9Error("INPUT_PRODUCT_REFERENCE_MISSING:" + stage)
    rel = ref.get("path")
    if not isinstance(rel, str) or not rel.startswith("warehouse/") or ".." in Path(rel).parts:
        raise K9Error("INPUT_PRODUCT_PATH_INVALID:" + stage)
    path = ROOT / rel
    if not path.is_file():
        raise K9Error("INPUT_PRODUCT_MISSING:" + stage)
    package = load_json(path)
    if ref.get("sha256") != stable(package):
        raise K9Error("INPUT_PRODUCT_HASH_MISMATCH:" + stage)
    if package.get("contract") != "K9_SUBMISSION_V1" or package.get("station") != stage:
        raise K9Error("INPUT_PRODUCT_CONTRACT_MISMATCH:" + stage)
    matches = [r for r in package.get("results", []) if r.get("item_id") == item["item_id"]]
    if len(matches) != 1:
        raise K9Error("INPUT_PRODUCT_ITEM_MISSING:" + stage)
    return matches[0], ref

def _inputs_for(item, station):
    if station == "research":
        return {}, {}
    research, research_ref = _product_result(item, "research")
    if station == "write":
        return {"research": research}, {"research": research_ref}

    article_stage = "repair" if item.get("revision", 0) > 0 and item.get("products", {}).get("repair") else "write"
    article, article_ref = _product_result(item, article_stage)
    payload = {"research": research, "article": article}
    refs = {"research": research_ref, "article": article_ref}

    if station == "repair":
        check, check_ref = _product_result(item, "check")
        payload["failed_check"] = check
        refs["failed_check"] = check_ref
    return payload, refs

def prepare(station, batch_size, source_run_id="manual"):
    if station not in STATIONS:
        raise K9Error("STATION_INVALID")
    if batch_size < 1 or batch_size > 1000:
        raise K9Error("BATCH_SIZE_INVALID")

    existing = current_job()
    if existing is not None:
        if existing["station"] != station:
            raise K9Error("ACTIVE_JOB_EXISTS_FOR_OTHER_STATION")
        write_chat_entry(existing)
        return {"status": "EXISTING_JOB_REUSED", "job": existing}

    data = ledger()
    items = [x for x in data["items"] if eligible(x, station)][:batch_size]
    if not items:
        return {"status": "NO_ELIGIBLE_WORK", "station": station, "report": status_report(data)}

    job_items = []
    for item in items:
        inputs, refs = _inputs_for(item, station)
        job_items.append({
            "item_id": item["item_id"],
            "title": item["title"],
            "metadata": item["metadata"],
            "revision": item["revision"],
            "input_products": inputs,
            "input_product_refs": refs
        })

    core = {
        "contract": "K9_JOB_V1",
        "status": "OPEN",
        "station": station,
        "item_count": len(items),
        "item_ids": [x["item_id"] for x in items],
        "items": job_items,
        "source_run_id": str(source_run_id),
        "ledger_generation": data["generation"]
    }
    core["job_id"] = "K9-" + station.upper() + "-" + stable(core)[:16]
    core["job_sha256"] = stable(core)
    write_json(CURRENT_JOB, core)
    write_chat_entry(core)
    return {"status": "NEW_JOB_PREPARED", "job": core}

def validate_submission(job, submission):
    if submission.get("contract") != "K9_SUBMISSION_V1":
        raise K9Error("SUBMISSION_CONTRACT_INVALID")
    if submission.get("job_id") != job["job_id"] or submission.get("station") != job["station"]:
        raise K9Error("SUBMISSION_JOB_MISMATCH")
    rows = submission.get("results")
    if not isinstance(rows, list) or len(rows) != job["item_count"]:
        raise K9Error("SUBMISSION_PARTIAL_OR_COUNT_MISMATCH")
    ids = [r.get("item_id") for r in rows]
    if len(ids) != len(set(ids)) or set(ids) != set(job["item_ids"]):
        raise K9Error("SUBMISSION_ITEM_SET_MISMATCH")
    by_id = {r["item_id"]: r for r in rows}
    station = job["station"]
    for item_id in job["item_ids"]:
        row = by_id[item_id]
        if station == "research":
            if not isinstance(row.get("facts"), list) or not row["facts"] or not isinstance(row.get("sources"), list) or not row["sources"]:
                raise K9Error("RESEARCH_RESULT_INCOMPLETE")
        elif station == "write":
            if not isinstance(row.get("article_text"), str) or not row["article_text"].strip():
                raise K9Error("WRITE_RESULT_INCOMPLETE")
        elif station == "check":
            if not isinstance(row.get("lt68_pass"), bool) or not isinstance(row.get("ppm679_pass"), bool):
                raise K9Error("CHECK_RESULT_INCOMPLETE")
        elif station == "repair":
            if not isinstance(row.get("article_text"), str) or not row["article_text"].strip():
                raise K9Error("REPAIR_RESULT_INCOMPLETE")
    return by_id

def accept(path):
    submission = load_json(path)
    archived = WAREHOUSE / "jobs" / f"{submission.get('job_id', 'UNKNOWN')}.json"
    if archived.exists():
        return {"status": "ALREADY_ACCEPTED", "job_id": submission.get("job_id")}

    job = current_job()
    if job is None:
        raise K9Error("NO_ACTIVE_JOB")
    by_id = validate_submission(job, submission)
    data = ledger()
    if data["generation"] != job["ledger_generation"]:
        raise K9Error("LEDGER_CHANGED_DURING_OPEN_JOB")

    items = {x["item_id"]: x for x in data["items"]}
    stage = job["station"]
    product_rel = f"warehouse/{stage}/{job['job_id']}.json"
    product_ref = {"job_id": job["job_id"], "path": product_rel, "sha256": stable(submission)}

    for item_id in job["item_ids"]:
        item = items[item_id]
        result = by_id[item_id]
        if not eligible(item, stage):
            raise K9Error("LEDGER_DRIFT_OR_DUPLICATE_PROCESSING")
        item.setdefault("products", {})[stage] = dict(product_ref)

        if stage == "research":
            item["stages"]["research"] = "DONE"
        elif stage == "write":
            item["stages"]["write"] = "DONE"
        elif stage == "check":
            if result["lt68_pass"] and result["ppm679_pass"]:
                item["stages"]["check"] = "DONE"
                item["stages"]["repair"] = "NOT_REQUIRED"
            else:
                item["stages"]["check"] = "FAIL"
                item["stages"]["repair"] = "PENDING"
        elif stage == "repair":
            item["revision"] += 1
            item["stages"]["repair"] = "DONE"
            item["stages"]["check"] = "PENDING"

    data["generation"] += 1
    write_json(ROOT / product_rel, submission)
    write_json(WAREHOUSE / "jobs" / f"{job['job_id']}.json", job)
    write_json(LEDGER, data)
    CURRENT_JOB.unlink()
    if CHAT_ENTRY.exists():
        CHAT_ENTRY.unlink()
    return {
        "status": "ACCEPTED",
        "job_id": job["job_id"],
        "station": stage,
        "item_count": job["item_count"],
        "report": status_report(data)
    }

def main():
    parser = argparse.ArgumentParser()
    subs = parser.add_subparsers(dest="cmd", required=True)
    p = subs.add_parser("import-intake")
    p.add_argument("path")
    p = subs.add_parser("prepare")
    p.add_argument("station", choices=STATIONS)
    p.add_argument("batch_size", type=int)
    p.add_argument("--source-run-id", default="manual")
    p = subs.add_parser("accept")
    p.add_argument("path")
    subs.add_parser("status")
    args = parser.parse_args()

    try:
        if args.cmd == "import-intake":
            result = import_intake(args.path)
        elif args.cmd == "prepare":
            result = prepare(args.station, args.batch_size, args.source_run_id)
        elif args.cmd == "accept":
            result = accept(args.path)
        else:
            result = status_report()
        print(json.dumps(result, ensure_ascii=False, indent=2, sort_keys=True))
    except K9Error as exc:
        print(json.dumps({"status": "BLOCKED", "reason": str(exc)}, indent=2), file=sys.stderr)
        raise SystemExit(2)

if __name__ == "__main__":
    main()
