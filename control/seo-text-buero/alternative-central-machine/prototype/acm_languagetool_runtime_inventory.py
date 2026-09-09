#!/usr/bin/env python3
from __future__ import annotations
import json,re,tempfile,zipfile
from pathlib import Path

REPO=Path(__file__).resolve().parents[4]
PPM=REPO/"control/startmaster0107/runtime_packages/PORTAL_PRODUCTION_MACHINE_V6.7.9_SIGNED_ARTICLE_TYPE_EXTENSION_ROOTFIX_FINAL.zip"

def main():
    with tempfile.TemporaryDirectory() as td:
        out=Path(td)/"ppm";out.mkdir()
        with zipfile.ZipFile(PPM) as z:z.extractall(out)
        root=out/"portal-production-machine"
        files=[p for p in root.rglob("*") if p.is_file()]
        paths=[str(p.relative_to(root)) for p in files]
        evidence=[str(p.relative_to(root)) for p in files if re.search(r"(languagetool|language-tool|bestand.?43)",str(p.relative_to(root)),re.I)]
        runtime=[str(p.relative_to(root)) for p in files if (
            p.suffix.lower()==".jar"
            or (p.suffix.lower() in {".sh",".py"} and re.search(r"(languagetool|language-tool)",p.name,re.I))
        )]
        refs=[]
        for p in root.rglob("*"):
            if not p.is_file() or p.suffix.lower() not in {".php",".py",".sh",".json",".md",".txt"}:continue
            try:txt=p.read_text(encoding="utf-8")
            except Exception:continue
            if re.search(r"LanguageTool 6\.8|Bestand 43|raw_report_json|outer_dependency_sha256|inner_dependency_sha256",txt,re.I):
                rows=[]
                for n,line in enumerate(txt.splitlines(),1):
                    if re.search(r"LanguageTool 6\.8|Bestand 43|raw_report_json|outer_dependency_sha256|inner_dependency_sha256|subprocess|java|jar",line,re.I):
                        rows.append({"line":n,"text":line.strip()[:700]})
                refs.append({"file":str(p.relative_to(root)),"hits":rows[:80]})
        print(json.dumps({
          "status":"ACM_LANGUAGETOOL_RUNTIME_INVENTORY_PASS",
          "runtime_candidate_paths":runtime,
          "runtime_candidate_count":len(runtime),
          "evidence_candidate_paths":evidence,
          "contract_and_code_refs":refs[:80],
          "repository_contains_bound_languagetool_runtime":len(runtime)>0,
          "note":"JSON/TXT LanguageTool reports are evidence only and are not counted as an executable runtime.",
          "publish_allowed":False
        },ensure_ascii=False,indent=2))
    return 0

if __name__=="__main__":
    raise SystemExit(main())

# workflow-trigger: lt-runtime-inventory-v1
