#!/usr/bin/env python3
from __future__ import annotations
import argparse, hashlib, json, subprocess, tempfile, zipfile
from pathlib import Path

PPM_REL="control/startmaster0107/runtime_packages/PORTAL_PRODUCTION_MACHINE_V6.7.9_SIGNED_ARTICLE_TYPE_EXTENSION_ROOTFIX_FINAL.zip"
PSERC_REL="control/startmaster0107/runtime_packages/PSERC-FIX.zip"
PPM_SHA="acbda93bd1c4292de7aaf88db2195631103991ff508b36c88cb694714818abd1"
PSERC_SHA="77a14aca97f46d60bc9001d66327abb68dd9cac9ad111f8ecefa1a8afd345314"
INNER="PSERC-FIX/portal-seo-editorial-plan-compiler_0.28.18_ENDSTEMPEL_IMPORT_ENVELOPE_BINDING.zip"

def sha(p: Path) -> str:
    return hashlib.sha256(p.read_bytes()).hexdigest()

def main() -> int:
    ap=argparse.ArgumentParser()
    ap.add_argument("--repo",required=True)
    ap.add_argument("--slots",required=True)
    ap.add_argument("--out",required=True)
    a=ap.parse_args()
    repo=Path(a.repo)
    ppm=repo/PPM_REL; pserc=repo/PSERC_REL
    if sha(ppm)!=PPM_SHA: raise SystemExit("PPM679_PACKAGE_HASH_MISMATCH")
    if sha(pserc)!=PSERC_SHA: raise SystemExit("PSERC_PACKAGE_HASH_MISMATCH")
    slots=json.loads(Path(a.slots).read_text(encoding="utf-8"))
    if not isinstance(slots,list) or not slots: raise SystemExit("SLOTS_INVALID")
    if len(set(slots))!=len(slots): raise SystemExit("SLOTS_DUPLICATE")
    with tempfile.TemporaryDirectory() as td:
        t=Path(td); ppmd=t/"ppm"; outer=t/"outer"; inner=t/"inner"
        ppmd.mkdir(); outer.mkdir(); inner.mkdir()
        with zipfile.ZipFile(ppm) as z:z.extractall(ppmd)
        with zipfile.ZipFile(pserc) as z:z.extractall(outer)
        iz=outer/INNER
        if not iz.is_file(): raise SystemExit("PSERC_INNER_ZIP_MISSING")
        with zipfile.ZipFile(iz) as z:z.extractall(inner)
        pp=ppmd/"portal-production-machine"; ps=inner/"portal-seo-editorial-plan-compiler"
        php=t/"dump.php"
        php.write_text(r'''<?php
$ppm=$argv[1]; $pserc=$argv[2]; $want=json_decode((string)file_get_contents($argv[3]),true);
require $ppm.'/tests/normal-draft-production/fixture-builder.php';
require $pserc.'/includes/class-pserc-stable-json.php';
require $pserc.'/includes/class-pserc-plan-slot-identity.php';
$map=[];
foreach((array)(PPM679_Editorial_Plan_Registry::plan()['slots']??[]) as $candidate){
 if(!is_array($candidate))continue;
 $token=PSERC_Plan_Slot_Identity::token($candidate);
 if(in_array($token,$want,true)){$map[$token]=$candidate;}
}
$out=[];
foreach($want as $token){
 if(!isset($map[$token])){fwrite(STDERR,"PLAN_SLOT_NOT_FOUND:".$token."\n");exit(2);}
 $row=$map[$token]; $row['plan_slot']=$token; $out[]=$row;
}
echo json_encode($out,JSON_UNESCAPED_SLASHES|JSON_UNESCAPED_UNICODE);
?>''',encoding="utf-8")
        cp=subprocess.run(["php",str(php),str(pp),str(ps),str(a.slots)],text=True,stdout=subprocess.PIPE,stderr=subprocess.PIPE,timeout=120)
        if cp.returncode: raise SystemExit("SLOT_METADATA_EXPORT_FAILED:"+cp.stderr[-500:])
        rows=json.loads(cp.stdout)
    out={"contract":"CONCEPT_AGENT_SLOT_METADATA_EXPORT_V1","status":"PASS","item_count":len(rows),"items":rows,"publish_allowed":False}
    Path(a.out).parent.mkdir(parents=True,exist_ok=True)
    Path(a.out).write_text(json.dumps(out,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
    print(json.dumps({"ok":True,"item_count":len(rows)},sort_keys=True))
    return 0
if __name__=="__main__": raise SystemExit(main())
