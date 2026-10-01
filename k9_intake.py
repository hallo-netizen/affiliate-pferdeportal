#!/usr/bin/env python3
import argparse, hashlib, json, re, sys
from pathlib import Path

SOURCE_CONTRACT="PSERC_METADATA_ONLY_READ_ONLY_PREVIEW_V5_DUAL_STRAND"
BATCH_CONTRACT="PSERC_TEXTMACHINE_METADATA_BATCH_V2"
FIELDS=("title","target_keyword","category","article_type","plan_slot")

class IntakeError(RuntimeError):
    pass

def stable(obj):
    raw=json.dumps(obj,ensure_ascii=False,sort_keys=True,separators=(",",":"))
    return hashlib.sha256(raw.encode("utf-8")).hexdigest()

def file_sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()

def batch_from_source(source):
    if not isinstance(source,dict):
        raise IntakeError("WORDPRESS_INPUT_CONTRACT_INVALID")
    if source.get("contract")==BATCH_CONTRACT:
        return source,"WORDPRESS_COMPACT_EXACT_FIVE_FIELDS"
    if source.get("contract")!=SOURCE_CONTRACT:
        raise IntakeError("WORDPRESS_INPUT_CONTRACT_INVALID")
    if source.get("mode")!="READ_ONLY_METADATA_ONLY_EXACT_FIVE_FIELDS":
        raise IntakeError("WORDPRESS_INPUT_MODE_INVALID")
    batch=source.get("next_textmachine_metadata_batch")
    if not isinstance(batch,dict) or batch.get("contract")!=BATCH_CONTRACT:
        raise IntakeError("WORDPRESS_BATCH_CONTRACT_INVALID")
    return batch,"WORDPRESS_LEGACY_SNAPSHOT_EXACT_FIVE_FIELDS"

def verify_batch_hash(batch):
    declared=str(batch.get("batch_sha256") or "")
    if not re.fullmatch(r"[0-9a-f]{64}",declared):
        raise IntakeError("WORDPRESS_BATCH_SHA_INVALID")
    core=dict(batch); core.pop("batch_sha256",None)
    if stable(core)!=declared:
        raise IntakeError("WORDPRESS_BATCH_SHA_MISMATCH")
    return declared

def convert(path):
    try:
        source=json.loads(Path(path).read_text(encoding="utf-8"))
    except Exception as exc:
        raise IntakeError("WORDPRESS_INPUT_JSON_INVALID") from exc
    batch,source_kind=batch_from_source(source)
    if batch.get("status")!="READY_FOR_TEXTMACHINE_METADATA_INTAKE":
        raise IntakeError("WORDPRESS_BATCH_NOT_READY")
    if batch.get("publish_allowed") is not False or batch.get("content_or_format_payload_present") is not False:
        raise IntakeError("WORDPRESS_BATCH_BOUNDARY_INVALID")
    source_batch_sha=verify_batch_hash(batch)
    rows=batch.get("items")
    if not isinstance(rows,list) or not rows:
        raise IntakeError("WORDPRESS_BATCH_EMPTY")
    if batch.get("item_count")!=len(rows):
        raise IntakeError("WORDPRESS_BATCH_COUNT_MISMATCH")
    out=[]; seen_slots=set()
    for row in rows:
        if not isinstance(row,dict) or set(row.keys())!=set(FIELDS):
            raise IntakeError("WORDPRESS_ITEM_NOT_EXACT_FIVE_FIELDS")
        clean={key:str(row.get(key) or "").strip() for key in FIELDS}
        if not all(clean.values()):
            raise IntakeError("WORDPRESS_ITEM_EMPTY_FIELD")
        if clean["plan_slot"] in seen_slots:
            raise IntakeError("WORDPRESS_PLAN_SLOT_DUPLICATE")
        seen_slots.add(clean["plan_slot"])
        item_id="k9-"+hashlib.sha256(clean["plan_slot"].encode("utf-8")).hexdigest()[:24]
        out.append({"item_id":item_id,"title":clean["title"],"metadata":clean})
    core={
        "contract":"K9_INTAKE_V1",
        "source_kind":source_kind,
        "source_file_sha256":file_sha(path),
        "source_batch_sha256":source_batch_sha,
        "item_count":len(out),
        "items":out,
        "publish_allowed":False
    }
    core["batch_id"]="K9-INTAKE-"+stable(core)[:20]
    core["batch_sha256"]=stable(core)
    return core

def main():
    ap=argparse.ArgumentParser(); ap.add_argument("input"); ap.add_argument("--output",required=True); args=ap.parse_args()
    try: result=convert(Path(args.input))
    except IntakeError as exc:
        print(json.dumps({"contract":"K9_INTAKE_V1","status":"BLOCKED","reason":str(exc)},indent=2),file=sys.stderr)
        raise SystemExit(2)
    Path(args.output).write_text(json.dumps(result,ensure_ascii=False,indent=2,sort_keys=True)+"\n",encoding="utf-8")
    print(json.dumps({"status":"K9_INTAKE_READY","batch_id":result["batch_id"],"item_count":result["item_count"]},ensure_ascii=False,indent=2))

if __name__=="__main__":
    main()
