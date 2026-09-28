#!/usr/bin/env python3
from __future__ import annotations
import hashlib,json,re,sys
from pathlib import Path

CONTRACT="K8_CLOSEOUT_PLAN_V1"
SHA_RE=re.compile(r"^[0-9a-f]{64}$")
class Blocked(RuntimeError): pass

def stable(v):
    return hashlib.sha256(json.dumps(v,ensure_ascii=False,sort_keys=True,separators=(",",":")).encode()).hexdigest()

def build(batch_sha:str,item_count:int,generation:int=1):
    if not SHA_RE.fullmatch(batch_sha): raise Blocked("BATCH_INVALID")
    if isinstance(item_count,bool) or item_count<1 or isinstance(generation,bool) or generation<1: raise Blocked("COUNT_OR_GENERATION_INVALID")
    gp=f"{generation:06d}"
    out={
      "contract":CONTRACT,"status":"PREALLOCATED","batch_sha256":batch_sha,"item_count":item_count,
      "runtime_generation":generation,
      "steps":["PSERC","ENDSTEMPEL_WITH_FINAL_WORDPRESS_JSON"],
      "endstempel_source_dir":f"control/startmaster0107/recovery_sources/{batch_sha}/generation-{gp}",
      "release_tag":f"konzept8-verbot-endstempel-{batch_sha}-g{gp}",
      "final_filename":"GEN1_7_ARTIKEL_PSERC_APPROVED_PRODUCTION_PACKAGE_107008_FINAL.json",
      "wordpress_exporter_ref":"concept_agent/konzept8_verbot/engine/k8_wordpress_export.py",
      "wordpress_contract":"SYSTEM4_WORDPRESS_HANDOFF_V1",
      "wordpress_filename":f"K8_WORDPRESS_DIRECT_IMPORT_{batch_sha}.json",
      "wordpress_mime_type":"application/json",
      "wordpress_json_required_before_stop":True,
      "route_search_after_articles":False,
      "final_hash_required":True,"publish_allowed":False
    }
    out["plan_sha256"]=stable(out); return out

def main(argv):
    try:
        if len(argv)!=5: raise Blocked("USE: k8_closeout_plan.py BATCH ITEM_COUNT GENERATION OUT")
        out=build(argv[1],int(argv[2]),int(argv[3]))
        Path(argv[4]).write_text(json.dumps(out,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
        print(json.dumps({"status":"PASS","release_tag":out["release_tag"],"generation":out["runtime_generation"]},sort_keys=True)); return 0
    except Exception as e:
        print("K8_CLOSEOUT_PLAN_BLOCKED:"+str(e),file=sys.stderr); return 2
if __name__=="__main__": raise SystemExit(main(sys.argv))
