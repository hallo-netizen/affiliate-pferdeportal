#!/usr/bin/env python3
from __future__ import annotations

import json
import re
import subprocess
import tempfile
import zipfile
from pathlib import Path

REPO=Path(__file__).resolve().parents[4]
PPM=REPO/"control/startmaster0107/runtime_packages/PORTAL_PRODUCTION_MACHINE_V6.7.9_SIGNED_ARTICLE_TYPE_EXTENSION_ROOTFIX_FINAL.zip"

PHP=r'''<?php
require __DIR__.'/tests/normal-draft-production/fixture-builder.php';
nd_reset();
$p=nd_build_plan(1,'p41-slot');
$item=$p['items'][0];
$pack=PPM679_Storage::load_fact_pack($item['source_snapshot_id']);
$g=PPM679_Content_Generator::generate($item,$pack);
$ev=PPM679_Content_Validator::check($g,$item,'p41-prep','p41-state');
$prepared=PPM679_Normal_Draft_Adapter::prepare(
  $g,$item,
  array(
    'technical_status'=>$ev['technical_status'],
    'content_quality_status'=>$ev['content_quality_status'],
    'content_hash'=>$ev['content_hash']
  ),
  nd_runtime($p,'p41-runtime'),
  'p41-run',
  PPM679_Diagnostic::stable_hash($p),
  'p41-state'
);
echo json_encode(array(
  'status'=>'P41_PREPARED_IDENTITY',
  'plan_item'=>$item,
  'plan'=>$p,
  'prepared'=>$prepared
),JSON_UNESCAPED_UNICODE|JSON_UNESCAPED_SLASHES)."\n";
'''

def run_json(cmd,cwd):
    p=subprocess.run(cmd,cwd=cwd,text=True,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,timeout=120)
    if p.returncode!=0:
        raise RuntimeError("PHP_FAILED:"+p.stdout[-3000:])
    dec=json.JSONDecoder()
    for line in reversed([x for x in p.stdout.splitlines() if x.strip()]):
        try:
            obj,_=dec.raw_decode(line.lstrip())
        except Exception:
            continue
        if isinstance(obj,dict) and obj.get("status")=="P41_PREPARED_IDENTITY":
            return obj
    raise RuntimeError("P41_RESULT_MISSING")

def method_block(text:str,name:str)->str:
    m=re.search(r"(?:public|private|protected)?\s*(?:static\s+)?function\s+"+re.escape(name)+r"\s*\(",text)
    if not m:return ""
    brace=text.find("{",m.end());depth=0
    for i in range(brace,len(text)):
        if text[i]=="{":depth+=1
        elif text[i]=="}":
            depth-=1
            if depth==0:return text[m.start():i+1]
    return text[m.start():]

def main():
    with tempfile.TemporaryDirectory() as td:
        root=Path(td); out=root/"ppm"; out.mkdir()
        with zipfile.ZipFile(PPM) as z:z.extractall(out)
        ppm=out/"portal-production-machine"

        script=ppm/"p41.php"; script.write_text(PHP,encoding="utf-8")
        result=run_json(["php",str(script)],ppm)
        item=result["plan_item"]; prepared=result["prepared"]; plan=result["plan"]

        adapter=(ppm/"includes/normal-draft-adapter.php").read_text(encoding="utf-8")
        prepare_src=method_block(adapter,"prepare")
        pipeline=(ppm/"includes/normal-draft-pipeline.php").read_text(encoding="utf-8")

        slot_tokens=[]
        for rel,text in [
            ("includes/normal-draft-adapter.php",prepare_src),
            ("includes/normal-draft-pipeline.php",pipeline),
        ]:
            for n,line in enumerate(text.splitlines(),1):
                low=line.lower()
                if "plan_slot" in low or "plan_item_key" in low or "canonical_article_id" in low:
                    slot_tokens.append({"file":rel,"line":n,"text":line.strip()[:700]})

        print(json.dumps({
          "status":"P41_PLAN_SLOT_IDENTITY_INVENTORY_PASS",
          "plan_item_identity":{
            "canonical_article_id":item.get("canonical_article_id"),
            "plan_slot":item.get("plan_slot"),
            "plan_item_key":item.get("plan_item_key"),
            "source_snapshot_id":item.get("source_snapshot_id"),
          },
          "prepared_identity":{
            "plan_item_key":prepared.get("plan_item_key"),
            "prepared_keys":sorted(prepared.keys()) if isinstance(prepared,dict) else [],
            "expected":prepared.get("expected"),
          },
          "plan_contract":plan.get("contract"),
          "plan_item_count":len(plan.get("items",[])) if isinstance(plan.get("items"),list) else None,
          "identity_source_hits":slot_tokens,
        },ensure_ascii=False,indent=2))
    return 0

if __name__=="__main__":
    raise SystemExit(main())
