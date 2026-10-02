from __future__ import annotations
import hashlib, json, re, subprocess, sys, tempfile, zipfile
from pathlib import Path

PPM_SHA256="acbda93bd1c4292de7aaf88db2195631103991ff508b36c88cb694714818abd1"
PSERC_SHA256="77a14aca97f46d60bc9001d66327abb68dd9cac9ad111f8ecefa1a8afd345314"
PSERC_INNER="PSERC-FIX/portal-seo-editorial-plan-compiler_0.28.18_ENDSTEMPEL_IMPORT_ENVELOPE_BINDING.zip"

class Blocked(RuntimeError): pass

def _sha(path:Path)->str:
    return hashlib.sha256(path.read_bytes()).hexdigest()

def _load(path:Path)->dict:
    x=json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(x,dict): raise Blocked("JSON_OBJECT_REQUIRED")
    return x

def _slot_from_article_id(article_id:str)->str:
    return hashlib.sha256(("pserc-plan-slot-v2|"+article_id).encode("utf-8")).hexdigest()

def resolve(intake_path:Path, ppm_zip:Path, pserc_zip:Path)->dict:
    if _sha(ppm_zip)!=PPM_SHA256: raise Blocked("PPM679_PACKAGE_HASH_MISMATCH")
    if _sha(pserc_zip)!=PSERC_SHA256: raise Blocked("PSERC_PACKAGE_HASH_MISMATCH")
    intake=_load(intake_path)
    items=intake.get("items")
    if not isinstance(items,list) or not items: raise Blocked("INTAKE_ITEMS_INVALID")
    slots=[str(x.get("plan_slot") or "") for x in items if isinstance(x,dict)]
    if len(slots)!=len(items) or any(not re.fullmatch(r"[0-9a-f]{64}",s) for s in slots):
        raise Blocked("INTAKE_PLAN_SLOT_INVALID")
    if len(set(slots))!=len(slots): raise Blocked("INTAKE_PLAN_SLOT_DUPLICATE")
    with tempfile.TemporaryDirectory() as td:
        root=Path(td); ppm_dir=root/"ppm"; po=root/"po"; ps=root/"ps"
        ppm_dir.mkdir(); po.mkdir(); ps.mkdir()
        with zipfile.ZipFile(ppm_zip) as z: z.extractall(ppm_dir)
        with zipfile.ZipFile(pserc_zip) as z: z.extractall(po)
        inner=po/PSERC_INNER
        if not inner.is_file(): raise Blocked("PSERC_INNER_ZIP_MISSING")
        with zipfile.ZipFile(inner) as z: z.extractall(ps)
        ppm_root=ppm_dir/"portal-production-machine"
        pserc_root=ps/"portal-seo-editorial-plan-compiler"
        php=r'''<?php
$ppm=$argv[1]; $pserc=$argv[2]; $slots=json_decode((string)file_get_contents($argv[3]),true);
require $ppm.'/tests/normal-draft-production/fixture-builder.php';
require $pserc.'/includes/class-pserc-plan-slot-identity.php';
$out=[];
foreach((array)$slots as $externalSlot){
  $matches=[];
  foreach((array)(PPM679_Editorial_Plan_Registry::plan()['slots']??[]) as $candidate){
    if(is_array($candidate)&&hash_equals(PSERC_Plan_Slot_Identity::token($candidate),(string)$externalSlot)){$matches[]=$candidate;}
  }
  if(count($matches)!==1){fwrite(STDERR,"PLAN_SLOT_REGISTRY_MATCH_NOT_UNIQUE:".$externalSlot.":".count($matches)."\n");exit(2);}
  $slot=$matches[0];
  $out[]=['plan_slot'=>(string)$externalSlot,'article_id'=>(string)($slot['canonical_article_id']??''),'category_slug'=>(string)($slot['category_slug']??'')];
}
echo json_encode($out,JSON_UNESCAPED_UNICODE|JSON_UNESCAPED_SLASHES);
?>'''
        script=root/"resolve.php"; script.write_text(php,encoding="utf-8")
        sp=root/"slots.json"; sp.write_text(json.dumps(slots),encoding="utf-8")
        proc=subprocess.run(["php",str(script),str(ppm_root),str(pserc_root),str(sp)],text=True,stdout=subprocess.PIPE,stderr=subprocess.PIPE,timeout=120)
    if proc.returncode!=0: raise Blocked("CANONICAL_SLOT_RESOLUTION_FAILED:"+(proc.stderr or proc.stdout).strip()[:500])
    try: rows=json.loads(proc.stdout)
    except json.JSONDecodeError as e: raise Blocked("CANONICAL_SLOT_RESOLUTION_OUTPUT_INVALID") from e
    if not isinstance(rows,list) or len(rows)!=len(items): raise Blocked("CANONICAL_SLOT_RESOLUTION_COUNT_INVALID")
    by={}
    for row in rows:
        aid=str(row.get("article_id") or "")
        slot=str(row.get("plan_slot") or "")
        if not re.fullmatch(r"article:[0-9a-f]{24}",aid): raise Blocked("CANONICAL_ARTICLE_ID_INVALID:"+slot)
        if _slot_from_article_id(aid)!=slot: raise Blocked("CANONICAL_ARTICLE_ID_SLOT_MISMATCH:"+slot)
        if slot in by: raise Blocked("CANONICAL_SLOT_RESOLUTION_DUPLICATE:"+slot)
        by[slot]=aid
    if set(by)!=set(slots): raise Blocked("CANONICAL_SLOT_RESOLUTION_SET_MISMATCH")
    return {"contract":"K10_CANONICAL_ARTICLE_BINDINGS_V1","status":"PASS","bindings":by}

def main():
    if len(sys.argv)!=5: raise SystemExit("usage: canonical_binding.py INTAKE PPM_ZIP PSERC_ZIP OUT")
    try:
        out=resolve(Path(sys.argv[1]),Path(sys.argv[2]),Path(sys.argv[3]))
    except Blocked as exc:
        print(json.dumps({"status":"BLOCKED","reason":str(exc)},ensure_ascii=False))
        raise SystemExit(2)
    Path(sys.argv[4]).write_text(json.dumps(out,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
    print(json.dumps(out,ensure_ascii=False))

if __name__=="__main__": main()
