#!/usr/bin/env python3
import argparse, hashlib, json, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
LEDGER = ROOT / "state" / "ledger.json"
CURRENT_JOB = ROOT / "runtime" / "CURRENT_JOB.json"
CHAT_ENTRY = ROOT / "runtime" / "CHAT_ENTRY.json"
WORKER_CONTRACTS = ROOT / "contracts" / "K9_WORKER_CONTRACTS.json"
WAREHOUSE = ROOT / "warehouse"
STATIONS = ("research", "write", "check", "repair")
LT68_JAR_SHA256 = "2122882e800d312a0543d895c56c0a84a9bb131c9b9846efd8fc033129353ae8"
PPM679_PACKAGE_SHA256 = "acbda93bd1c4292de7aaf88db2195631103991ff508b36c88cb694714818abd1"

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

def worker_contract(station):
    data = load_json(WORKER_CONTRACTS)
    if data.get("contract") != "K9_WORKER_CONTRACTS_V1":
        raise K9Error("WORKER_CONTRACT_FILE_INVALID")
    value = data.get("contracts", {}).get(station)
    if not isinstance(value, dict):
        raise K9Error("WORKER_CONTRACT_MISSING:" + station)
    return value

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
        "submission_path": "submissions/" + job["job_id"] + ".json",
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
        "completion_rule": "RETURN_ONE_COMPLETE_K9_SUBMISSION_FOR_THIS_EXACT_JOB",
        "worker_type": job["worker_contract"]["worker_type"],
        "output_contract": job["worker_contract"]["output_contract"]
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
        "ledger_generation": data["generation"],
        "worker_contract": worker_contract(station)
    }
    core["job_id"] = "K9-" + station.upper() + "-" + stable(core)[:16]
    core["job_sha256"] = stable(core)
    write_json(CURRENT_JOB, core)
    write_chat_entry(core)
    return {"status": "NEW_JOB_PREPARED", "job": core}

def _job_item(job, item_id):
    matches = [x for x in job.get("items", []) if x.get("item_id") == item_id]
    if len(matches) != 1:
        raise K9Error("JOB_ITEM_MISSING_OR_DUPLICATE")
    return matches[0]

def _validate_research_product(row, job_item):
    product = row.get("research_product")
    if not isinstance(product, dict) or product.get("contract") != "K9_RESEARCH_PRODUCT_V1":
        raise K9Error("RESEARCH_PRODUCT_CONTRACT_INVALID")
    sources = product.get("sources")
    pack = product.get("fact_pack")
    if not isinstance(sources, list) or not sources or not isinstance(pack, dict):
        raise K9Error("RESEARCH_PRODUCT_INCOMPLETE")

    source_ids = []
    for source in sources:
        if not isinstance(source, dict):
            raise K9Error("RESEARCH_SOURCE_INVALID")
        sid = str(source.get("source_id") or "").strip()
        url = str(source.get("url") or "").strip()
        title = str(source.get("title") or "").strip()
        if not sid or not url or not title:
            raise K9Error("RESEARCH_SOURCE_REQUIRED_FIELD_MISSING")
        source_ids.append(sid)
    if len(source_ids) != len(set(source_ids)):
        raise K9Error("RESEARCH_SOURCE_ID_DUPLICATE")

    required_pack = {
        "fact_pack_id", "domain", "article_type", "fact_ids", "status", "claims",
        "fact_pack_hash", "source_manifest_hash", "claim_register_hash",
        "required_block_coverage", "table_evidence_coverage",
        "conclusion_evidence_coverage", "article_type_coverage",
        "temporal_validity_status", "contradiction_status",
        "production_readiness_status", "placeholder_content_status"
    }
    if not required_pack.issubset(pack):
        raise K9Error("RESEARCH_FACT_PACK_REQUIRED_FIELD_MISSING")
    if pack.get("status") != "SOURCE_VERIFIED_PRODUCTION_READY" or pack.get("production_readiness_status") != "SOURCE_VERIFIED_PRODUCTION_READY":
        raise K9Error("RESEARCH_FACT_PACK_NOT_PRODUCTION_READY")
    fact_ids = pack.get("fact_ids")
    claims = pack.get("claims")
    if not isinstance(fact_ids, list) or not fact_ids or not isinstance(claims, list) or not claims:
        raise K9Error("RESEARCH_FACT_PACK_FACTS_MISSING")
    if len(fact_ids) != len(set(fact_ids)):
        raise K9Error("RESEARCH_FACT_ID_DUPLICATE")

    claim_ids = []
    for claim in claims:
        if not isinstance(claim, dict):
            raise K9Error("RESEARCH_CLAIM_INVALID")
        for key in ("fact_id", "source_id", "locator", "statement", "claim_status", "subject_scope", "time_scope"):
            if not str(claim.get(key) or "").strip():
                raise K9Error("RESEARCH_CLAIM_REQUIRED_FIELD_MISSING:" + key)
        if claim.get("claim_status") != "FULLY_SUPPORTED":
            raise K9Error("RESEARCH_CLAIM_NOT_FULLY_SUPPORTED")
        if claim["source_id"] not in source_ids:
            raise K9Error("RESEARCH_CLAIM_SOURCE_UNKNOWN")
        claim_ids.append(claim["fact_id"])
    if set(claim_ids) != set(fact_ids) or len(claim_ids) != len(set(claim_ids)):
        raise K9Error("RESEARCH_FACT_CLAIM_SET_MISMATCH")

    expected_type = str(job_item.get("metadata", {}).get("article_type") or "").strip()
    if expected_type and pack.get("article_type") != expected_type:
        raise K9Error("RESEARCH_ARTICLE_TYPE_MISMATCH")
    declared = product.get("product_sha256")
    core = dict(product)
    core.pop("product_sha256", None)
    if declared != stable(core):
        raise K9Error("RESEARCH_PRODUCT_HASH_INVALID")
    return product

def _validate_article_product(row, job_item):
    product = row.get("article_product")
    if not isinstance(product, dict) or product.get("contract") != "K9_ARTICLE_PRODUCT_V1":
        raise K9Error("ARTICLE_PRODUCT_CONTRACT_INVALID")
    title = str(product.get("title") or "").strip()
    html = str(product.get("content_html") or "")
    if not title or not html.strip():
        raise K9Error("ARTICLE_PRODUCT_CONTENT_MISSING")
    content_sha = hashlib.sha256(html.encode("utf-8")).hexdigest()
    if product.get("content_sha256") != content_sha:
        raise K9Error("ARTICLE_PRODUCT_CONTENT_HASH_INVALID")

    research_row = job_item.get("input_products", {}).get("research")
    if not isinstance(research_row, dict):
        raise K9Error("ARTICLE_RESEARCH_INPUT_MISSING")
    research = research_row.get("research_product")
    if not isinstance(research, dict):
        raise K9Error("ARTICLE_RESEARCH_PRODUCT_MISSING")
    if product.get("research_product_sha256") != research.get("product_sha256"):
        raise K9Error("ARTICLE_RESEARCH_BINDING_MISMATCH")

    ppm_item = product.get("ppm_item")
    if not isinstance(ppm_item, dict):
        raise K9Error("ARTICLE_PPM_ITEM_MISSING")
    fact_pack = research.get("fact_pack", {})
    if ppm_item.get("source_snapshot_id") != fact_pack.get("fact_pack_id"):
        raise K9Error("ARTICLE_PPM_SOURCE_BINDING_MISMATCH")
    if ppm_item.get("article_type") != fact_pack.get("article_type"):
        raise K9Error("ARTICLE_PPM_TYPE_BINDING_MISMATCH")
    canonical = ppm_item.get("canonical_article")
    if not isinstance(canonical, dict) or canonical.get("body_html") != html or canonical.get("title") != title:
        raise K9Error("ARTICLE_PPM_CANONICAL_BINDING_MISMATCH")

    declared = product.get("product_sha256")
    core = dict(product)
    core.pop("product_sha256", None)
    if declared != stable(core):
        raise K9Error("ARTICLE_PRODUCT_HASH_INVALID")
    return product

def _validate_check_product(row, job_item):
    lt = row.get("lt68_result")
    ppm = row.get("ppm679_result")
    if not isinstance(lt, dict) or lt.get("contract") != "K9_LT68_RESULT_V1":
        raise K9Error("CHECK_LT68_RESULT_INVALID")
    if not isinstance(ppm, dict) or ppm.get("contract") != "K9_PPM679_RESULT_V1":
        raise K9Error("CHECK_PPM679_RESULT_INVALID")

    article_row = job_item.get("input_products", {}).get("article")
    if not isinstance(article_row, dict):
        raise K9Error("CHECK_ARTICLE_INPUT_MISSING")
    article = article_row.get("article_product")
    if not isinstance(article, dict):
        raise K9Error("CHECK_ARTICLE_PRODUCT_MISSING")
    content_sha = article.get("content_sha256")

    if lt.get("jar_sha256") != LT68_JAR_SHA256 or lt.get("article_sha256") != content_sha:
        raise K9Error("CHECK_LT68_BINDING_INVALID")
    if ppm.get("ppm_package_sha256") != PPM679_PACKAGE_SHA256 or ppm.get("content_sha256") != content_sha:
        raise K9Error("CHECK_PPM679_BINDING_INVALID")
    if lt.get("status") not in ("PASS", "REPAIR_REQUIRED") or ppm.get("status") not in ("PASS", "REPAIR_REQUIRED"):
        raise K9Error("CHECK_RESULT_STATUS_INVALID")
    return lt, ppm

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
        job_item = _job_item(job, item_id)
        if station == "research":
            _validate_research_product(row, job_item)
        elif station == "write":
            _validate_article_product(row, job_item)
        elif station == "check":
            _validate_check_product(row, job_item)
        elif station == "repair":
            _validate_article_product(row, job_item)
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
            lt_status = result["lt68_result"]["status"]
            ppm_status = result["ppm679_result"]["status"]
            if lt_status == "PASS" and ppm_status == "PASS":
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
