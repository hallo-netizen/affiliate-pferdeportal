#!/usr/bin/env python3
from __future__ import annotations
import json,re,subprocess,tempfile,zipfile
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
          "pserc_supervisor_validate":class_method(pserc,"PSERC_Workflow_Supervisor","validate"),
        }
        if not critical["ppm_load_fact_pack"] or not critical["ppm_generate"]:
            raise RuntimeError("PPM_FACTPACK_CRITICAL_METHOD_MISSING")
        if not critical["pserc_bridge_prepare"]:
            raise RuntimeError("PSERC_BRIDGE_PREPARE_MISSING")
        supervisor_validate=critical["pserc_supervisor_validate"]
        if not supervisor_validate or "PSERC_PPM_Intake_Bridge::prepare" not in supervisor_validate["source"]:
            raise RuntimeError("PSERC_SUPERVISOR_PREPARE_BINDING_MISSING")

        prepare_tests=[]
        supervisor_tests=[]
        tests_root=pserc/"tests"
        if tests_root.is_dir():
            for test in sorted(tests_root.rglob("*.php")):
                txt=test.read_text(encoding="utf-8")
                direct="PSERC_PPM_Intake_Bridge::prepare" in txt
                indirect="PSERC_Workflow_Supervisor::validate(" in txt
                if not direct and not indirect:
                    continue
                proc=subprocess.run(
                    ["php",str(test)],
                    cwd=pserc,
                    text=True,
                    stdout=subprocess.PIPE,
                    stderr=subprocess.STDOUT,
                    timeout=180,
                )
                row={
                    "test":str(test.relative_to(pserc)),
                    "returncode":proc.returncode,
                    "status":"PASS" if proc.returncode==0 else "FAIL",
                    "output_tail":proc.stdout[-2400:],
                }
                (prepare_tests if direct else supervisor_tests).append(row)
        covered=prepare_tests+supervisor_tests
        if not covered:
            raise RuntimeError("PSERC_BRIDGE_PREPARE_EXISTING_TEST_COVERAGE_MISSING")
        failed=[x["test"] for x in covered if x["returncode"]!=0]
        if failed:
            raise RuntimeError("PSERC_BRIDGE_PREPARE_EXISTING_TEST_FAILED:"+",".join(failed))

        print(json.dumps({
          "status":"P26_RESEARCH_FACTPACK_CHAIN_MAP_PASS",
          "critical_methods":critical,
          "pserc_bridge_prepare_direct_tests":prepare_tests,
          "pserc_bridge_prepare_via_supervisor_tests":supervisor_tests,
          "ppm_matches":scan(ppm,"PPM",70),
          "pserc_matches":scan(pserc,"PSERC",90),
          "pste_matches":scan(PSTE,"PSTE",90),
        },ensure_ascii=False,indent=2))
    return 0

if __name__=="__main__":
    raise SystemExit(main())
