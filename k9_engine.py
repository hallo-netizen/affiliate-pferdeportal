#!/usr/bin/env python3
import argparse, hashlib, json, os, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
LEDGER = ROOT / "state" / "ledger.json"
CURRENT_JOB = ROOT / "runtime" / "CURRENT_JOB.json"
WAREHOUSE = ROOT / "warehouse"

STATIONS = ("research", "write", "check", "repair")

class K9Error(RuntimeError):
    pass

def stable(obj):
    return hashlib.sha256(json.dumps(obj, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode("utf-8")).hexdigest()

def load_json(path):
    return json.loads(Path(path).read_text(encoding="utf-8"))

def write_json(path, data):
    p = Path(path); p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(json.dumps(data, ensure_ascii=False, indent=2, sort_keys=True)+"\n", encoding="utf-8")

def ledger():
    d = load_json(LEDGER)
    if d.get("contract") != "K9_LEDGER_V1" or not isinstance(d.get("items"), list):
        raise K9Error("LEDGER_INVALID")
    return d

def current_job():
    if not CURRENT_JOB.exists():
        return None
    d = load_json(CURRENT_JOB)
    if d.get("contract") != "K9_JOB_V1" or d.get("status") != "OPEN":
        raise K9Error("CURRENT_JOB_INVALID")
    return d

def eligible(item, station):
    s = item["stages"]
    if station == "research": return s["research"] == "PENDING"
    if station == "write": return s["research"] == "DONE" and s["write"] == "PENDING"
    if station == "check": return s["write"] == "DONE" and s["check"] == "PENDING"
    if station == "repair": return s["check"] == "FAIL" and s["repair"] == "PENDING"
    raise K9Error("STATION_INVALID")

def status_report(d=None):
    d = d or ledger()
    result = {"contract":"K9_STATUS_V1","total":len(d["items"]),"stations":{}}
    for st in STATIONS:
        vals=[x["stages"][st] for x in d["items"]]
        result["stations"][st] = {k:vals.count(k) for k in sorted(set(vals) | {"PENDING","DONE"})}
    j=current_job()
    result["active_job"] = None if j is None else {k:j[k] for k in ("job_id","station","item_count","item_ids")}
    return result

def import_intake(path):
    if current_job() is not None: raise K9Error("ACTIVE_JOB_EXISTS")
    src=load_json(path)
    rows=src.get("items")
    if not isinstance(rows,list) or not rows: raise K9Error("INTAKE_EMPTY_OR_INVALID")
    d=ledger(); known={x["item_id"] for x in d["items"]}; add=[]
    for row in rows:
        iid=str(row.get("item_id","")).strip(); title=str(row.get("title","")).strip()
        if not iid or not title or iid in known: raise K9Error("INTAKE_ITEM_INVALID_OR_DUPLICATE")
        known.add(iid)
        add.append({"item_id":iid,"title":title,"metadata":row.get("metadata",{}),"revision":0,
                    "stages":{"research":"PENDING","write":"PENDING","check":"PENDING","repair":"NOT_REQUIRED"}})
    d["items"].extend(add); d["generation"] += 1; write_json(LEDGER,d)
    return {"status":"INTAKE_ACCEPTED","added":len(add),"total":len(d["items"])}

def prepare(station, batch_size, source_run_id="manual"):
    if station not in STATIONS: raise K9Error("STATION_INVALID")
    if batch_size < 1 or batch_size > 1000: raise K9Error("BATCH_SIZE_INVALID")
    existing=current_job()
    if existing is not None:
        if existing["station"] != station: raise K9Error("ACTIVE_JOB_EXISTS_FOR_OTHER_STATION")
        return {"status":"EXISTING_JOB_REUSED","job":existing}
    d=ledger(); items=[x for x in d["items"] if eligible(x,station)][:batch_size]
    if not items:
        return {"status":"NO_ELIGIBLE_WORK","station":station,"report":status_report(d)}
    core={"contract":"K9_JOB_V1","status":"OPEN","station":station,"item_count":len(items),
          "item_ids":[x["item_id"] for x in items],"items":[{"item_id":x["item_id"],"title":x["title"],"metadata":x["metadata"],"revision":x["revision"]} for x in items],
          "source_run_id":str(source_run_id),"ledger_generation":d["generation"]}
    core["job_id"]="K9-"+station.upper()+"-"+stable(core)[:16]
    core["job_sha256"]=stable(core)
    write_json(CURRENT_JOB,core)
    return {"status":"NEW_JOB_PREPARED","job":core}

def validate_submission(job, sub):
    if sub.get("contract") != "K9_SUBMISSION_V1": raise K9Error("SUBMISSION_CONTRACT_INVALID")
    if sub.get("job_id") != job["job_id"] or sub.get("station") != job["station"]: raise K9Error("SUBMISSION_JOB_MISMATCH")
    rows=sub.get("results")
    if not isinstance(rows,list) or len(rows) != job["item_count"]: raise K9Error("SUBMISSION_PARTIAL_OR_COUNT_MISMATCH")
    ids=[r.get("item_id") for r in rows]
    if len(ids)!=len(set(ids)) or set(ids)!=set(job["item_ids"]): raise K9Error("SUBMISSION_ITEM_SET_MISMATCH")
    byid={r["item_id"]:r for r in rows}
    st=job["station"]
    for iid in job["item_ids"]:
        r=byid[iid]
        if st=="research":
            if not isinstance(r.get("facts"),list) or not r["facts"] or not isinstance(r.get("sources"),list) or not r["sources"]: raise K9Error("RESEARCH_RESULT_INCOMPLETE")
        elif st=="write":
            if not isinstance(r.get("article_text"),str) or not r["article_text"].strip(): raise K9Error("WRITE_RESULT_INCOMPLETE")
        elif st=="check":
            if not isinstance(r.get("lt68_pass"),bool) or not isinstance(r.get("ppm679_pass"),bool): raise K9Error("CHECK_RESULT_INCOMPLETE")
        elif st=="repair":
            if not isinstance(r.get("article_text"),str) or not r["article_text"].strip(): raise K9Error("REPAIR_RESULT_INCOMPLETE")
    return byid

def accept(path):
    sub=load_json(path)
    archived=WAREHOUSE / "jobs" / f"{sub.get('job_id','UNKNOWN')}.json"
    if archived.exists():
        return {"status":"ALREADY_ACCEPTED","job_id":sub.get("job_id")}
    job=current_job()
    if job is None: raise K9Error("NO_ACTIVE_JOB")
    byid=validate_submission(job,sub)
    d=ledger()
    if d["generation"] != job["ledger_generation"]:
        raise K9Error("LEDGER_CHANGED_DURING_OPEN_JOB")
    items={x["item_id"]:x for x in d["items"]}
    st=job["station"]
    for iid in job["item_ids"]:
        x=items[iid]; r=byid[iid]
        if not eligible(x,st): raise K9Error("LEDGER_DRIFT_OR_DUPLICATE_PROCESSING")
        if st=="research": x["stages"]["research"]="DONE"
        elif st=="write": x["stages"]["write"]="DONE"
        elif st=="check":
            if r["lt68_pass"] and r["ppm679_pass"]:
                x["stages"]["check"]="DONE"; x["stages"]["repair"]="NOT_REQUIRED"
            else:
                x["stages"]["check"]="FAIL"; x["stages"]["repair"]="PENDING"
        elif st=="repair":
            x["revision"] += 1; x["stages"]["repair"]="DONE"; x["stages"]["check"]="PENDING"
    d["generation"] += 1
    write_json(WAREHOUSE/st/f"{job['job_id']}.json",sub)
    write_json(WAREHOUSE/"jobs"/f"{job['job_id']}.json",job)
    write_json(LEDGER,d)
    CURRENT_JOB.unlink()
    return {"status":"ACCEPTED","job_id":job["job_id"],"station":st,"item_count":job["item_count"],"report":status_report(d)}

def main():
    ap=argparse.ArgumentParser(); sp=ap.add_subparsers(dest="cmd",required=True)
    a=sp.add_parser("import-intake"); a.add_argument("path")
    a=sp.add_parser("prepare"); a.add_argument("station",choices=STATIONS); a.add_argument("batch_size",type=int); a.add_argument("--source-run-id",default="manual")
    a=sp.add_parser("accept"); a.add_argument("path")
    sp.add_parser("status")
    ns=ap.parse_args()
    try:
        if ns.cmd=="import-intake": out=import_intake(ns.path)
        elif ns.cmd=="prepare": out=prepare(ns.station,ns.batch_size,ns.source_run_id)
        elif ns.cmd=="accept": out=accept(ns.path)
        else: out=status_report()
        print(json.dumps(out,ensure_ascii=False,indent=2,sort_keys=True))
    except K9Error as e:
        print(json.dumps({"status":"BLOCKED","reason":str(e)},indent=2),file=sys.stderr); raise SystemExit(2)
if __name__=="__main__": main()
