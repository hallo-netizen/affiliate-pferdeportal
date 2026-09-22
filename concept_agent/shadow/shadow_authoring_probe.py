#!/usr/bin/env python3
from __future__ import annotations
import hashlib,json,subprocess,tempfile,zipfile
from pathlib import Path

REPO=Path(__file__).resolve().parents[2]
PPM=REPO/"control/startmaster0107/runtime_packages/PORTAL_PRODUCTION_MACHINE_V6.7.9_SIGNED_ARTICLE_TYPE_EXTENSION_ROOTFIX_FINAL.zip"
PSERC=REPO/"control/startmaster0107/runtime_packages/PSERC-FIX.zip"
PPM_SHA="acbda93bd1c4292de7aaf88db2195631103991ff508b36c88cb694714818abd1"
PSERC_SHA="77a14aca97f46d60bc9001d66327abb68dd9cac9ad111f8ecefa1a8afd345314"
INNER="PSERC-FIX/portal-seo-editorial-plan-compiler_0.28.18_ENDSTEMPEL_IMPORT_ENVELOPE_BINDING.zip"
OUT=Path("/tmp/concept-agent-shadow-output")
SLOTS=[
"0b401802eeed8574d9c80f7eb5e1abb03c0ac5dbf82fa8b8a95deb7abf3bec15",
"23330868f4b0c79781d83d539e3f5854b31d0667fa48ba45c084911b243568fe",
"916a0af7de7981275f29d95e854778ed6ffa5147f1cdff4aae4592f37ba27892",
"160c801f6e1b6c99065f287083a6b5fbc93a545764e04e7c833531904d77bb5d",
"4a5cb3c5e9265835dafb8213c00ce6575407e9b79024b613778517ce6d545c55",
"307f0a6f59c3d8c1cef8fd88c59754aada60fef9aee6de617a7f0e7b1419da0b",
"5999b9b00de2a1756101c5ebfb2b547c6ff2b9360bd9bae0988696a795ff6288",
"19020cbf4c886a65fe3bc488b17872ed387d26bdc19ed1fdc4dd2078caa9f684",
"27b5c81a0da11c5628d223bebc55603923f05304f57c66ff191620efd15707bd",
"a554b0f86f23cda760d2a03f839934cbc4dda269d961ff891e763a684283352b",
"fa1a9a959616dfebead59102343f751a7147e9b149afaff63a01d42d7b1fa442",
"fb9b282e561584c5203bd7058dcff93976f87421092f2d95f3df42ab579659c5",
"e8c73ae9008889fb168c5527d2fe6d55c7779627eed61952538afd131ad1e57f",
"6ee476b7ef6c754e75fc284dac8f5e5bbb2f60f6001029c0838af15638b56713",
"53c8c859fbbc1b9a2a17ffe53efaf31d74520ac7a89aebc1e84ec9a6ea95ea6f",
"f1c165d83a4d24d1c3ab7fe632f9e97c1f0898a8b67a2e5253a842ba46cd456b",
]
def h(p): return hashlib.sha256(p.read_bytes()).hexdigest()
def main():
    if h(PPM)!=PPM_SHA: raise SystemExit("PPM679_PACKAGE_HASH_MISMATCH")
    if h(PSERC)!=PSERC_SHA: raise SystemExit("PSERC_FIX_PACKAGE_HASH_MISMATCH")
    with tempfile.TemporaryDirectory() as td:
        t=Path(td); ppm=t/"ppm"; outer=t/"outer"; inner=t/"inner"; ppm.mkdir(); outer.mkdir(); inner.mkdir()
        with zipfile.ZipFile(PPM) as z:z.extractall(ppm)
        with zipfile.ZipFile(PSERC) as z:z.extractall(outer)
        iz=outer/INNER
        if not iz.is_file(): raise SystemExit("PSERC_INNER_ZIP_MISSING")
        with zipfile.ZipFile(iz) as z:z.extractall(inner)
        pp=ppm/"portal-production-machine"; ps=inner/"portal-seo-editorial-plan-compiler"
        php=t/"resolve.php"
        php.write_text(r'''<?php
$ppm=$argv[1]; $pserc=$argv[2]; $want=array_flip(json_decode((string)file_get_contents($argv[3]),true));
require $ppm.'/tests/normal-draft-production/fixture-builder.php';
require $pserc.'/includes/class-pserc-stable-json.php';
require $pserc.'/includes/class-pserc-plan-slot-identity.php';
$out=[];
foreach((array)(PPM679_Editorial_Plan_Registry::plan()['slots']??[]) as $candidate){
 if(!is_array($candidate))continue;
 $token=PSERC_Plan_Slot_Identity::token($candidate);
 if(isset($want[$token])){
  $out[]=['plan_slot'=>$token,'canonical_article_id'=>(string)($candidate['canonical_article_id']??''),'category_slug'=>(string)($candidate['category_slug']??'')];
 }
}
echo json_encode($out,JSON_UNESCAPED_SLASHES|JSON_UNESCAPED_UNICODE);
?>''',encoding="utf-8")
        wp=t/"wanted.json"; wp.write_text(json.dumps(SLOTS),encoding="utf-8")
        cp=subprocess.run(["php",str(php),str(pp),str(ps),str(wp)],text=True,stdout=subprocess.PIPE,stderr=subprocess.PIPE,timeout=120)
        if cp.returncode: raise SystemExit("SLOT_RESOLVER_FAILED:"+cp.stderr[:300])
        rows=json.loads(cp.stdout)
    by={r["plan_slot"]:r for r in rows}
    if len(rows)!=16 or set(by)!=set(SLOTS): raise SystemExit("PLAN_SLOT_REGISTRY_MATCH_NOT_EXACT_16")
    if any(not r["canonical_article_id"].startswith("article:") for r in rows): raise SystemExit("CANONICAL_ID_INVALID")
    ordered=[by[s] for s in SLOTS]
    OUT.mkdir(parents=True,exist_ok=True)
    proof={"contract":"CONCEPT_AGENT_PLAN_SLOT_BINDING_PROOF_V1","status":"PASS","item_count":16,"ppm_version":"6.7.9","ppm_package_sha256":PPM_SHA,"pserc_fix_sha256":PSERC_SHA,"items":ordered,"publish_allowed":False}
    (OUT/"PLAN_SLOT_BINDINGS.json").write_text(json.dumps(proof,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
    print(json.dumps(proof,ensure_ascii=False,indent=2))
if __name__=="__main__": main()
