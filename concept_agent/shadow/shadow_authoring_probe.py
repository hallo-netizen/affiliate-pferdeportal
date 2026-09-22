#!/usr/bin/env python3
from pathlib import Path
import hashlib,json,subprocess,tempfile,zipfile

REPO=Path(__file__).resolve().parents[2]
OUT=Path("/tmp/concept-agent-shadow-output")
PPM=REPO/"control/startmaster0107/runtime_packages/PORTAL_PRODUCTION_MACHINE_V6.7.9_SIGNED_ARTICLE_TYPE_EXTENSION_ROOTFIX_FINAL.zip"
PPM_SHA="acbda93bd1c4292de7aaf88db2195631103991ff508b36c88cb694714818abd1"
IDS=[
"article:277289349b5a5091767a01b1","article:6f12ebc079953babff75fe00","article:40e70bdf41f7ebc44ca0c188",
"article:b173e46a0f955ad7467e80ec","article:f78a6387af81e400c31c447f","article:09c961ebeec074c32324fcc5",
"article:f363ad9f8d1f7e91a81ea740","article:98d25b1963465407779b7354","article:5207874abd18dad1db470264",
"article:b8d4fba69c8aa211c51d9e0e","article:0403a67125f7ec7af49ffaa1","article:6ff9535e7ae20e22298ee842",
"article:6f2ceb50c5159e3e7d5e44ac","article:7b003121b663cd27a5df29d0","article:66a12650abafbb93159be7b1",
"article:2ff55b21f209f7d67e0d6b86"]

def sha(p):
    return hashlib.sha256(p.read_bytes()).hexdigest()

def relevant(d):
    out={}
    for k,v in d.items():
        kl=str(k).lower()
        if any(t in kl for t in ("title","keyword","topic","subject","category","article_type","canonical_article_id","intent")):
            if isinstance(v,(str,int,float,bool)) or v is None:
                out[k]=v
            elif isinstance(v,(list,dict)):
                out[k]=v
    return out

def walk(v,path,matches):
    if isinstance(v,dict):
        cid=v.get("canonical_article_id")
        if cid in IDS:
            matches[cid].append({"path":path,"fields":relevant(v),"all_keys":sorted(v.keys())})
        for k,x in v.items():
            walk(x,path+[str(k)],matches)
    elif isinstance(v,list):
        for i,x in enumerate(v):
            walk(x,path+[str(i)],matches)

def main():
    if sha(PPM)!=PPM_SHA: raise SystemExit("PPM679_PACKAGE_HASH_MISMATCH")
    with tempfile.TemporaryDirectory() as td:
        root=Path(td)
        with zipfile.ZipFile(PPM) as z:z.extractall(root)
        ppm=root/"portal-production-machine"
        php=root/"dump.php"
        php.write_text("""<?php
require $argv[1].'/tests/normal-draft-production/fixture-builder.php';
echo json_encode(PPM679_Editorial_Plan_Registry::plan(),JSON_UNESCAPED_SLASHES|JSON_UNESCAPED_UNICODE);
?>""",encoding="utf-8")
        cp=subprocess.run(["php",str(php),str(ppm)],text=True,stdout=subprocess.PIPE,stderr=subprocess.PIPE,timeout=120)
        if cp.returncode: raise SystemExit("PPM_PLAN_DUMP_FAILED:"+cp.stderr[-500:])
        plan=json.loads(cp.stdout)
        matches={cid:[] for cid in IDS}
        walk(plan,[],matches)
        keyword_nodes=[]
        def kwalk(v,path):
            if isinstance(v,dict):
                for k,x in v.items():
                    if "target_keyword" in str(k).lower():
                        keyword_nodes.append({"path":path+[str(k)],"value":x})
                    kwalk(x,path+[str(k)])
            elif isinstance(v,list):
                for i,x in enumerate(v): kwalk(x,path+[str(i)])
        kwalk(plan,[])
    proof={
      "contract":"CONCEPT_AGENT_PPM16_AUTHORITATIVE_METADATA_DIAGNOSTIC_V1",
      "status":"PASS",
      "ppm_version":"6.7.9",
      "ppm_package_sha256":PPM_SHA,
      "canonical_id_count":len(IDS),
      "canonical_matches":matches,
      "target_keyword_nodes":keyword_nodes,
      "all_16_ids_present":all(matches[c] for c in IDS),
      "all_16_have_target_keyword":all(any("target_keyword" in json.dumps(m,ensure_ascii=False) for m in matches[c]) for c in IDS),
      "publish_allowed":False
    }
    OUT.mkdir(parents=True,exist_ok=True)
    (OUT/"PPM16_AUTHORITATIVE_METADATA_DIAGNOSTIC.json").write_text(json.dumps(proof,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
    print(json.dumps({"status":"PASS","all_16_ids_present":proof["all_16_ids_present"],"target_keyword_node_count":len(keyword_nodes),"all_16_have_target_keyword":proof["all_16_have_target_keyword"]},sort_keys=True))
if __name__=="__main__": main()
