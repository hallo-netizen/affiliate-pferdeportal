#!/usr/bin/env python3
from pathlib import Path
import hashlib,json,os,shutil
REPO=Path(__file__).resolve().parents[2]
OUT=Path("/tmp/concept-agent-shadow-output")
FILES=[
 "isolated_system4/production_checks_engine.py",
 "isolated_system4/LT68Worker.java",
 "control/startmaster0107/runtime_packages/PORTAL_PRODUCTION_MACHINE_V6.7.9_SIGNED_ARTICLE_TYPE_EXTENSION_ROOTFIX_FINAL.zip",
 "control/startmaster0107/runtime_packages/PSERC-FIX.zip",
 "affiliate-portal-router/assets/portal-structure-v279.json",
]
EXPECTED={
 "control/startmaster0107/runtime_packages/PORTAL_PRODUCTION_MACHINE_V6.7.9_SIGNED_ARTICLE_TYPE_EXTENSION_ROOTFIX_FINAL.zip":"acbda93bd1c4292de7aaf88db2195631103991ff508b36c88cb694714818abd1",
 "control/startmaster0107/runtime_packages/PSERC-FIX.zip":"77a14aca97f46d60bc9001d66327abb68dd9cac9ad111f8ecefa1a8afd345314",
 "isolated_system4/LT68Worker.java":"f2487a84b9fc4424e6207a26d8278d31207a7746e7cd504800faa22652876503",
}
def sha(p):
 h=hashlib.sha256()
 with p.open("rb") as q:
  for b in iter(lambda:q.read(1024*1024),b""): h.update(b)
 return h.hexdigest()
def main():
 OUT.mkdir(parents=True,exist_ok=True)
 rows=[]
 for rel in FILES:
  src=REPO/rel
  if not src.is_file(): raise SystemExit("BUNDLE_SOURCE_MISSING:"+rel)
  actual=sha(src)
  if rel in EXPECTED and actual!=EXPECTED[rel]: raise SystemExit("BUNDLE_HASH_MISMATCH:"+rel)
  dst=OUT/rel; dst.parent.mkdir(parents=True,exist_ok=True); shutil.copyfile(src,dst)
  rows.append({"ref":rel,"sha256":actual,"bytes":dst.stat().st_size})
 jar=Path(os.environ.get("SYSTEM4_LANGUAGETOOL_JAR",""))
 if not jar.is_file(): raise SystemExit("LT_JAR_MISSING")
 jarsha=sha(jar)
 if jarsha!="2122882e800d312a0543d895c56c0a84a9bb131c9b9846efd8fc033129353ae8": raise SystemExit("LT_JAR_HASH_MISMATCH")
 dst=OUT/"languagetool-commandline.jar"; shutil.copyfile(jar,dst)
 rows.append({"ref":"languagetool-commandline.jar","sha256":jarsha,"bytes":dst.stat().st_size})
 proof={"contract":"CONCEPT_AGENT_VALIDATOR_BUNDLE_V1","status":"PASS","files":rows,"publish_allowed":False}
 (OUT/"VALIDATOR_BUNDLE_PROOF.json").write_text(json.dumps(proof,indent=2)+"\n",encoding="utf-8")
 print(json.dumps(proof,sort_keys=True))
if __name__=="__main__": main()
