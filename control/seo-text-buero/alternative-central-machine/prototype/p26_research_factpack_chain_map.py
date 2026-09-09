#!/usr/bin/env python3
from __future__ import annotations
import hashlib,json,re,subprocess,tempfile,zipfile
from pathlib import Path

REPO=Path(__file__).resolve().parents[4]
PPM=REPO/"control/startmaster0107/runtime_packages/PORTAL_PRODUCTION_MACHINE_V6.7.9_SIGNED_ARTICLE_TYPE_EXTENSION_ROOTFIX_FINAL.zip"
PSERC=REPO/"control/startmaster0107/runtime_packages/PSERC-FIX.zip"
PSERC_INNER="PSERC-FIX/portal-seo-editorial-plan-compiler_0.28.18_ENDSTEMPEL_IMPORT_ENVELOPE_BINDING.zip"
PSTE=REPO/"PSTE_0.56.25"

TERMS=(
 "fact_pack","fact-pack","source_snapshot_id","research","source_snapshot",
 "PSERC_PPM_Intake_Bridge","PSTE","production_plan","quality_binding"
)

def method_names(text):
    return sorted(set(re.findall(r"function\s+([A-Za-z_][A-Za-z0-9_]*)\s*\(",text)))

def lines(text):
    out=[]
    for n,line in enumerate(text.splitlines(),1):
        low=line.lower()
        hits=[t for t in TERMS if t.lower() in low]
        if hits:
            out.append({"line":n,"terms":hits,"text":line.strip()[:650]})
    return out

def scan(root,label,limit=120):
    rows=[]
    for p in root.rglob("*"):
        if not p.is_file() or p.suffix.lower() not in {".php",".py",".json",".md",".txt"}:
            continue
        try:txt=p.read_text(encoding="utf-8")
        except Exception:continue
        hs=lines(txt)
        if hs:
            rows.append({
              "owner":label,
              "file":str(p.relative_to(root)),
              "methods":method_names(txt)[:80],
              "hits":hs[:80],
            })
    rows.sort(key=lambda x:(0 if "fact" in x["file"].lower() else 1,x["file"]))
    return rows[:limit]

def class_method(root,cname,mname):
    for p in root.rglob("*.php"):
        txt=p.read_text(encoding="utf-8")
        cm=re.search(r"class\s+"+re.escape(cname)+r"\b",txt)
        if not cm:continue
        mm=re.search(r"(?:public|private|protected)?\s*(?:static\s+)?function\s+"+re.escape(mname)+r"\s*\(",txt)
        if not mm:continue
        brace=txt.find("{",mm.end());depth=0
        if brace<0:continue
        for i in range(brace,len(txt)):
            if txt[i]=="{":depth+=1
            elif txt[i]=="}":
                depth-=1
                if depth==0:
                    return {"file":str(p.relative_to(root)),"source":txt[mm.start():i+1]}
    return None

def main():
    with tempfile.TemporaryDirectory() as td:
        t=Path(td)
        ppm_out=t/"ppm"; po=t/"pserc_outer"; ps=t/"pserc"
        ppm_out.mkdir();po.mkdir();ps.mkdir()
        with zipfile.ZipFile(PPM) as z:z.extractall(ppm_out)
        with zipfile.ZipFile(PSERC) as z:z.extractall(po)
        inner=po/PSERC_INNER
        if not inner.is_file():raise RuntimeError("PSERC_INNER_MISSING")
        with zipfile.ZipFile(inner) as z:z.extractall(ps)
        ppm=ppm_out/"portal-production-machine"
        pserc=ps/"portal-seo-editorial-plan-compiler"

        critical={
          "ppm_load_fact_pack":class_method(ppm,"PPM679_Storage","load_fact_pack"),
          "ppm_generate":class_method(ppm,"PPM679_Content_Generator","generate"),
          "pserc_bridge_prepare":class_method(pserc,"PSERC_PPM_Intake_Bridge","prepare"),
          "pserc_bridge_execute":class_method(pserc,"PSERC_PPM_Intake_Bridge","execute"),
          "pserc_bridge_verify_package_item":class_method(pserc,"PSERC_PPM_Intake_Bridge","verifyPackageItem"),
          "pserc_supervisor_validate":class_method(pserc,"PSERC_Workflow_Supervisor","validate"),
        }
        if not critical["ppm_load_fact_pack"] or not critical["ppm_generate"]:
            raise RuntimeError("PPM_FACTPACK_CRITICAL_METHOD_MISSING")
        if not critical["pserc_bridge_prepare"]:
            raise RuntimeError("PSERC_BRIDGE_PREPARE_MISSING")
        supervisor_validate=critical["pserc_supervisor_validate"]
        if not supervisor_validate or "PSERC_PPM_Intake_Bridge::prepare" not in supervisor_validate["source"]:
            raise RuntimeError("PSERC_SUPERVISOR_PREPARE_BINDING_MISSING")

        # P26 only: prove the existing PSERC prepare seam with frozen real package/plan data.
        approved=pserc/"approved-production-packages/gen1-7-final-existing-import-envelope.json"
        canonical_plan=ppm/"contracts/canonical-complete-editorial-plan-v1.json"
        if not approved.is_file() or not canonical_plan.is_file():
            raise RuntimeError("P26_FIXED_INPUT_SOURCE_MISSING")

        def tree_fingerprint(root):
            h=hashlib.sha256()
            for fp in sorted(x for x in root.rglob("*") if x.is_file()):
                h.update(str(fp.relative_to(root)).encode("utf-8")+b"\0")
                h.update(hashlib.sha256(fp.read_bytes()).digest())
            return h.hexdigest()

        before={"ppm":tree_fingerprint(ppm),"pserc":tree_fingerprint(pserc)}
        proof_php=t/"p26-pserc-prepare-proof.php"
        proof_php.write_text(r'''<?php
define('ABSPATH', __DIR__.'/');
require_once $argv[1].'/includes/class-pserc-stable-json.php';
require_once $argv[1].'/includes/class-pserc-metadata-boundary.php';
require_once $argv[1].'/includes/class-pserc-plan-slot-identity.php';
require_once $argv[1].'/includes/class-pserc-ppm-intake-bridge.php';

$env=json_decode(file_get_contents($argv[1].'/approved-production-packages/gen1-7-final-existing-import-envelope.json'),true);
$productionPackage=is_array($env['production_plan']??null)?$env['production_plan']:null;
$plan=json_decode(file_get_contents($argv[2].'/contracts/canonical-complete-editorial-plan-v1.json'),true);
if(!is_array($productionPackage)||!is_array($plan)){fwrite(STDERR,"P26_INPUT_JSON_INVALID\n");exit(2);}

$slots=[];
foreach((array)($plan['slots']??[]) as $slot){
    if(!is_array($slot))continue;
    $cid=(string)($slot['canonical_article_id']??'');
    if($cid!=='')$slots[$cid]=$slot;
}
$items=[];
foreach((array)($productionPackage['items']??[]) as $pitem){
    if(!is_array($pitem)){fwrite(STDERR,"P26_PACKAGE_ITEM_INVALID\n");exit(2);}
    $cid=(string)($pitem['canonical_article_id']??'');
    $slot=$slots[$cid]??null;
    if(!is_array($slot)){fwrite(STDERR,"P26_CANONICAL_SLOT_MISSING:".$cid."\n");exit(2);}
    $items[]=[
        'title'=>(string)($pitem['topic']??''),
        'target_keyword'=>(string)($pitem['target_keyword']??''),
        'category'=>(string)($slot['category_slug']??''),
        'article_type'=>(string)($pitem['article_type']??''),
        'plan_slot'=>PSERC_Plan_Slot_Identity::token($slot),
    ];
}
$batch=[
    'contract'=>'PSERC_TEXTMACHINE_METADATA_BATCH_V2',
    'status'=>'READY_FOR_METADATA_HANDOFF',
    'item_count'=>count($items),
    'maximum_articles'=>0,
    'maximum_articles_per_type'=>0,
    'publish_allowed'=>false,
    'content_or_format_payload_present'=>false,
    'items'=>$items,
];
$batch['batch_sha256']=PSERC_Stable_Json::hash($batch);
$snapshot=['ok'=>true,'status'=>'P26_FIXED_PPM_SNAPSHOT','version'=>'6.7.9','plan'=>$plan,'write_attempted'=>false];

$rehash=function(array $b): array {
    unset($b['batch_sha256']);
    $b['batch_sha256']=PSERC_Stable_Json::hash($b);
    return $b;
};
$blocked=function($r): bool {
    return is_array($r)&&empty($r['ok'])&&str_starts_with((string)($r['status']??''),'PSERC_BRIDGE_');
};

$positive=PSERC_PPM_Intake_Bridge::prepare($batch,$productionPackage,$snapshot);

$wrongSlot=$batch;
$wrongSlot['items'][0]['plan_slot']=str_repeat('0',64);
$wrongSlot=$rehash($wrongSlot);
$negSlot=PSERC_PPM_Intake_Bridge::prepare($wrongSlot,$productionPackage,$snapshot);

$wrongTitle=$batch;
$wrongTitle['items'][0]['title'].=' P26-WRONG';
$wrongTitle=$rehash($wrongTitle);
$negTitle=PSERC_PPM_Intake_Bridge::prepare($wrongTitle,$productionPackage,$snapshot);

$wrongKeyword=$batch;
$wrongKeyword['items'][0]['target_keyword'].=' p26-wrong';
$wrongKeyword=$rehash($wrongKeyword);
$negKeyword=PSERC_PPM_Intake_Bridge::prepare($wrongKeyword,$productionPackage,$snapshot);

$wrongIdentity=$productionPackage;
$wrongIdentity['items'][0]['canonical_article_id']='article:p26-invalid-identity';
$negIdentity=PSERC_PPM_Intake_Bridge::prepare($batch,$wrongIdentity,$snapshot);

$pass=
    !empty($positive['ok']) &&
    ($positive['status']??'')==='PSERC_PPM_INTAKE_BRIDGE_PREPARED' &&
    (($positive['report']['write_attempted_by_bridge']??null)===false) &&
    (($positive['report']['publish_allowed']??null)===false) &&
    $blocked($negSlot) &&
    $blocked($negTitle) &&
    $blocked($negKeyword) &&
    $blocked($negIdentity);

echo json_encode([
    'status'=>$pass?'P26_PSERC_PREPARE_PROOF_PASS':'P26_PSERC_PREPARE_PROOF_BLOCKED',
    'positive_status'=>$positive['status']??null,
    'positive_item_count'=>count($items),
    'prepare_no_write'=>($positive['report']['write_attempted_by_bridge']??null)===false,
    'publish_allowed'=>$positive['report']['publish_allowed']??null,
    'negative_plan_slot'=>$negSlot['status']??null,
    'negative_identity'=>$negIdentity['status']??null,
    'negative_title'=>$negTitle['status']??null,
    'negative_keyword'=>$negKeyword['status']??null,
],JSON_UNESCAPED_UNICODE|JSON_UNESCAPED_SLASHES)."\n";
exit($pass?0:2);
''',encoding="utf-8")

        proc=subprocess.run(
            ["php",str(proof_php),str(pserc),str(ppm)],
            cwd=t,
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            timeout=180,
        )
        if proc.returncode!=0:
            raise RuntimeError("P26_PSERC_PREPARE_PROOF_FAILED\n"+proc.stdout[-5000:])
        try:
            proof=json.loads(proc.stdout.strip().splitlines()[-1])
        except Exception as e:
            raise RuntimeError("P26_PSERC_PREPARE_PROOF_JSON_INVALID") from e
        after={"ppm":tree_fingerprint(ppm),"pserc":tree_fingerprint(pserc)}
        if before!=after:
            raise RuntimeError("P26_PSERC_PREPARE_WRITE_DETECTED")
        if proof.get("status")!="P26_PSERC_PREPARE_PROOF_PASS":
            raise RuntimeError("P26_PSERC_PREPARE_PROOF_NOT_PASS")
        if proof.get("prepare_no_write") is not True or proof.get("publish_allowed") is not False:
            raise RuntimeError("P26_PSERC_PREPARE_SAFETY_INVARIANT_FAILED")

        print(json.dumps({
          "status":"P26_RESEARCH_FACTPACK_CHAIN_MAP_PASS",
          "critical_methods":critical,
          "pserc_prepare_proof":proof,
          "filesystem_unchanged":True,
          "ppm_matches":scan(ppm,"PPM",70),
          "pserc_matches":scan(pserc,"PSERC",90),
          "pste_matches":scan(PSTE,"PSTE",90),
        },ensure_ascii=False,indent=2))
    return 0

if __name__=="__main__":
    raise SystemExit(main())
