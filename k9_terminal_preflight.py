#!/usr/bin/env python3
import argparse, hashlib, json
from pathlib import Path

import k9_pserc
import k9_wordpress_export

CONTRACT="K9_TERMINAL_READINESS_PREFLIGHT_V1"
class Blocked(RuntimeError): pass

def stable(obj):
    return hashlib.sha256(json.dumps(obj,ensure_ascii=False,sort_keys=True,separators=(",",":")).encode()).hexdigest()

def load(path):
    value=json.loads(Path(path).read_text(encoding="utf-8"))
    if not isinstance(value,dict): raise Blocked("JSON_OBJECT_REQUIRED:"+str(path))
    return value

def run(root,ppm,pserc,pserc_output):
    root=Path(root)
    status=load(root/"state/STATUS.json")
    if status.get("active_job") is not None or status.get("remaining")!=0 or status.get("repair_required")!=0:
        raise Blocked("TERMINAL_STATUS_NOT_READY")
    if status.get("total",0)<1 or status.get("fully_done")!=status.get("total"):
        raise Blocked("TERMINAL_ARTICLES_NOT_ALL_CHECK_DONE")
    ledger=load(root/"state/ledger.json")
    ledger_raw=(root/"state/ledger.json").read_bytes()
    _,intake,items=k9_pserc.active_intake_items(root,ledger)
    if len(items)!=status.get("total") and len(items)!=intake.get("item_count"):
        # Active intake is allowed to be the current suffix of a historical ledger.
        if len(items)!=intake.get("item_count"):
            raise Blocked("TERMINAL_ACTIVE_INTAKE_COUNT_INVALID")
    slots=set()
    for item in items:
        meta=item.get("metadata") if isinstance(item,dict) else None
        slot=str(meta.get("plan_slot") or "") if isinstance(meta,dict) else ""
        if not slot or slot in slots:
            raise Blocked("TERMINAL_LEDGER_SLOT_INVALID")
        slots.add(slot)
        if not k9_wordpress_export.ledger_article_done(item):
            raise Blocked("TERMINAL_WORDPRESS_LEDGER_STATE_INVALID:"+slot)
        if not isinstance(meta,dict) or any(not str(meta.get(k) or "").strip() for k in ("title","target_keyword","category","article_type","plan_slot")):
            raise Blocked("TERMINAL_WORDPRESS_METADATA_INCOMPLETE:"+slot)

    pserc_result=k9_pserc.run(root,ppm,pserc)
    if pserc_result.get("status")!="PASS" or pserc_result.get("bridge_status")!="PSERC_FINAL_INTEGRITY_ONLY_PASS":
        raise Blocked("TERMINAL_PSERC_NOT_PASS")
    if int(pserc_result.get("article_count") or 0)!=len(items):
        raise Blocked("TERMINAL_PSERC_ARTICLE_COUNT_MISMATCH")
    Path(pserc_output).write_text(json.dumps(pserc_result,ensure_ascii=False,indent=2,sort_keys=True)+"\n",encoding="utf-8")
    result={
        "contract":CONTRACT,
        "status":"PASS",
        "article_count":len(items),
        "ledger_sha256":hashlib.sha256(ledger_raw).hexdigest(),
        "active_intake_batch_sha256":str(intake.get("batch_sha256") or ""),
        "pserc_result_sha256":stable(pserc_result),
        "pserc_output":str(pserc_output),
        "wordpress_ledger_readiness":"PASS",
        "quality_gates_reused":["LT_6_8","PPM_6_7_9","K9_WRITING_RULES"],
        "publish_allowed":False,
    }
    return result

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("root")
    ap.add_argument("ppm")
    ap.add_argument("pserc")
    ap.add_argument("--pserc-output",required=True)
    ap.add_argument("--output",required=True)
    a=ap.parse_args()
    try:
        out=run(a.root,a.ppm,a.pserc,a.pserc_output)
    except Exception as exc:
        print(json.dumps({"contract":CONTRACT,"status":"BLOCKED","reason":str(exc),"publish_allowed":False},ensure_ascii=False,indent=2))
        raise SystemExit(2)
    Path(a.output).write_text(json.dumps(out,ensure_ascii=False,indent=2,sort_keys=True)+"\n",encoding="utf-8")
    print(json.dumps({"status":"K9_TERMINAL_READINESS_PASS","article_count":out["article_count"]},indent=2))
if __name__=="__main__": main()
