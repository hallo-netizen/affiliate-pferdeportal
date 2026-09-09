#!/usr/bin/env python3
from __future__ import annotations
import json,re,tempfile,zipfile
from pathlib import Path

REPO=Path(__file__).resolve().parents[4]
PPM=REPO/"control/startmaster0107/runtime_packages/PORTAL_PRODUCTION_MACHINE_V6.7.9_SIGNED_ARTICLE_TYPE_EXTENSION_ROOTFIX_FINAL.zip"

def method_block(text:str,name:str)->str:
    m=re.search(r"function\s+"+re.escape(name)+r"\s*\(",text)
    if not m:return ""
    b=text.find("{",m.end())
    if b<0:return ""
    d=0
    for i in range(b,len(text)):
        if text[i]=="{":d+=1
        elif text[i]=="}":
            d-=1
            if d==0:return text[m.start():i+1]
    return text[m.start():]

def main()->int:
    with tempfile.TemporaryDirectory() as td:
        root=Path(td)
        with zipfile.ZipFile(PPM) as z:z.extractall(root)
        ppm=root/"portal-production-machine"
        fb=ppm/"tests/normal-draft-production/fixture-builder.php"
        if not fb.is_file():raise RuntimeError("FIXTURE_BUILDER_MISSING")
        txt=fb.read_text(encoding="utf-8")
        build=method_block(txt,"nd_build_plan")
        if not build:raise RuntimeError("ND_BUILD_PLAN_MISSING")

        # Produce one authoritative sample item/fact-pack using the existing fixture builder.
        probe=ppm/"acm-schema-probe.php"
        probe.write_text(r'''<?php
require __DIR__.'/tests/normal-draft-production/fixture-builder.php';
nd_reset();
$p=nd_build_plan(4,'acm-schema-probe');
$item=$p['items'][0];
$pack=PPM679_Storage::load_fact_pack($item['source_snapshot_id']);
$beratungItem=null;$beratungPack=null;
foreach($p['items'] as $candidate){
  if((string)($candidate['article_type']??'')==='Beratung'){
    $beratungItem=$candidate;
    $beratungPack=PPM679_Storage::load_fact_pack($candidate['source_snapshot_id']);
    break;
  }
}
if(!is_array($beratungItem)||!is_array($beratungPack)){fwrite(STDERR,"BERATUNG_SAMPLE_MISSING\n");exit(2);}
if(isset($beratungItem['canonical_article']['body_html'])){$beratungItem['canonical_article']['body_html']='[OMITTED_SCHEMA_PROBE]';}
echo json_encode(array(
  'status'=>'ACM_FACTPACK_PLAN_SCHEMA_SAMPLE',
  'plan_header'=>array_diff_key($p,array('items'=>true)),
  'faq_item'=>$item,
  'faq_fact_pack'=>$pack,
  'beratung_item'=>$beratungItem,
  'beratung_fact_pack'=>$beratungPack
),JSON_UNESCAPED_UNICODE|JSON_UNESCAPED_SLASHES|JSON_PRETTY_PRINT)."\n";
''',encoding="utf-8")
        import subprocess
        cp=subprocess.run(["php",str(probe)],cwd=ppm,text=True,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,timeout=120)
        if cp.returncode!=0:raise RuntimeError("SCHEMA_PROBE_FAILED:"+cp.stdout[-2000:])
        sample=json.loads(cp.stdout)
        print(json.dumps({
          "status":"ACM_FACTPACK_PLAN_SCHEMA_PROBE_PASS",
          "nd_build_plan_source":build,
          "sample":sample,
          "publish_allowed":False
        },ensure_ascii=False,indent=2))
    return 0

if __name__=="__main__":
    raise SystemExit(main())
