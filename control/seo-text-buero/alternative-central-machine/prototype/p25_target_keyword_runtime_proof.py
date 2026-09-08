#!/usr/bin/env python3
from __future__ import annotations
import json,re,subprocess,tempfile,zipfile
from pathlib import Path

REPO=Path(__file__).resolve().parents[4]
PPM=REPO/"control/startmaster0107/runtime_packages/PORTAL_PRODUCTION_MACHINE_V6.7.9_SIGNED_ARTICLE_TYPE_EXTENSION_ROOTFIX_FINAL.zip"
ERROR="BLOCKED_CONTENT_TARGET_KEYWORD_TITLE"
RULE="TITLE_MUST_CONTAIN_TARGET_KEYWORD"

def extract_method(text,pos):
    # nearest method before match, then balanced block
    starts=list(re.finditer(r"(?:public|private|protected)?\s*(?:static\s+)?function\s+([A-Za-z_][A-Za-z0-9_]*)\s*\(",text[:pos]))
    if not starts:return None
    m=starts[-1]; brace=text.find("{",m.end())
    if brace<0:return None
    depth=0
    for i in range(brace,len(text)):
        if text[i]=="{": depth+=1
        elif text[i]=="}":
            depth-=1
            if depth==0:
                return {"name":m.group(1),"source":text[m.start():i+1]}
    return None

def error_codes(obj):
    out=[]
    if isinstance(obj,dict):
        if isinstance(obj.get("error_code"),str):out.append(obj["error_code"])
        for v in obj.values():out.extend(error_codes(v))
    elif isinstance(obj,list):
        for v in obj:out.extend(error_codes(v))
    return out

PHP=r'''<?php
require __DIR__.'/tests/normal-draft-production/fixture-builder.php';
nd_reset();
$p=nd_build_plan(1,'p25-keyword');
$item=$p['items'][0];
$pack=PPM679_Storage::load_fact_pack($item['source_snapshot_id']);
$g=PPM679_Content_Generator::generate($item,$pack);
$base=PPM679_Content_Validator::check($g,$item,'p25-base','p25-state');
$binding=is_array($item['quality_binding']??null)?$item['quality_binding']:array();
$keyword=(string)($binding['target_keyword']??($item['target_keyword']??''));
$mut=$g;
if($keyword!==''){
  $title=(string)($mut['title']??'');
  $mut['title']=trim(str_ireplace($keyword,'',$title));
  if($mut['title']===$title || $mut['title']==='')$mut['title']='Unverbundener Testtitel ohne Zielbegriff';
}else{
  $mut['title']='Unverbundener Testtitel ohne Zielbegriff';
}
$bad=PPM679_Content_Validator::check($mut,$item,'p25-negative','p25-state');
echo json_encode(array(
  'status'=>'P25_RUNTIME_PROBE',
  'target_keyword'=>$keyword,
  'base_ok'=>!empty($base['ok']),
  'base_codes'=>nd_error_codes($base),
  'original_title'=>$g['title']??null,
  'mutated_title'=>$mut['title']??null,
  'mutated_ok'=>!empty($bad['ok']),
  'mutated_codes'=>nd_error_codes($bad)
),JSON_UNESCAPED_UNICODE|JSON_UNESCAPED_SLASHES)."\n";
'''

def main():
    with tempfile.TemporaryDirectory() as td:
        root=Path(td)
        with zipfile.ZipFile(PPM) as z:z.extractall(root)
        ppm=root/"portal-production-machine"

        static=[]
        for p in ppm.rglob("*"):
            if not p.is_file() or p.suffix.lower() not in {".php",".json",".md",".txt"}:continue
            try:txt=p.read_text(encoding="utf-8")
            except Exception:continue
            if ERROR in txt or RULE in txt:
                positions=[m.start() for m in re.finditer(re.escape(ERROR),txt)]
                methods=[]
                for pos in positions:
                    mb=extract_method(txt,pos)
                    if mb:methods.append({"name":mb["name"],"source":mb["source"]})
                static.append({
                    "file":str(p.relative_to(ppm)),
                    "has_error":ERROR in txt,
                    "has_rule":RULE in txt,
                    "methods":methods,
                })

        probe=ppm/"p25-probe.php";probe.write_text(PHP,encoding="utf-8")
        proc=subprocess.run(["php",str(probe)],cwd=ppm,text=True,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,timeout=120)
        if proc.returncode!=0:raise RuntimeError("P25_PHP_FAILED:"+proc.stdout[-3000:])
        result=None
        for line in reversed([x for x in proc.stdout.splitlines() if x.strip()]):
            try:
                o=json.loads(line)
                if isinstance(o,dict) and o.get("status")=="P25_RUNTIME_PROBE":result=o;break
            except Exception:pass
        if result is None:raise RuntimeError("P25_RESULT_MISSING:"+proc.stdout[-3000:])

        if not static:raise RuntimeError("TARGET_KEYWORD_RULE_SOURCE_NOT_FOUND")
        if result.get("base_ok") is not True:raise RuntimeError("BASELINE_CONTENT_VALIDATOR_NOT_PASS")
        if not result.get("target_keyword"):raise RuntimeError("TARGET_KEYWORD_NOT_BOUND_IN_NORMAL_FIXTURE")
        if result.get("mutated_ok") is not False:raise RuntimeError("TARGET_KEYWORD_TITLE_MUTATION_NOT_BLOCKED")
        if ERROR not in result.get("mutated_codes",[]):raise RuntimeError("EXPECTED_TARGET_KEYWORD_BLOCKER_MISSING")

        print(json.dumps({
            "status":"P25_TARGET_KEYWORD_RUNTIME_PROOF_PASS",
            "static_sources":static,
            "runtime_probe":result,
            "exact_blocker":ERROR,
            "rule":RULE,
            "reachable_via":"PPM679_Content_Validator::check",
        },ensure_ascii=False,indent=2))
    return 0

if __name__=="__main__":
    raise SystemExit(main())
