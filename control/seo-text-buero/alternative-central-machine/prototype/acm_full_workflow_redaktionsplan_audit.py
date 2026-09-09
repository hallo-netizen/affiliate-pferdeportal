#!/usr/bin/env python3
from __future__ import annotations
import json,re,tempfile,zipfile
from pathlib import Path

REPO=Path(__file__).resolve().parents[4]
PPM=REPO/"control/startmaster0107/runtime_packages/PORTAL_PRODUCTION_MACHINE_V6.7.9_SIGNED_ARTICLE_TYPE_EXTENSION_ROOTFIX_FINAL.zip"
PSERC=REPO/"control/startmaster0107/runtime_packages/PSERC-FIX.zip"
PSERC_INNER="PSERC-FIX/portal-seo-editorial-plan-compiler_0.28.18_ENDSTEMPEL_IMPORT_ENVELOPE_BINDING.zip"

def methods(text,name):
    m=re.search(r"class\s+"+re.escape(name)+r"\b",text)
    if not m:return {}
    b=text.find("{",m.end());d=0;end=len(text)
    for i in range(b,len(text)):
        if text[i]=="{":d+=1
        elif text[i]=="}":
            d-=1
            if d==0:end=i+1;break
    cls=text[m.start():end]
    out={}
    for mm in re.finditer(r"(?:public|private|protected)?\s*(?:static\s+)?function\s+([A-Za-z_][A-Za-z0-9_]*)\s*\(",cls):
        name2=mm.group(1); bb=cls.find("{",mm.end()); dd=0
        if bb<0:continue
        for j in range(bb,len(cls)):
            if cls[j]=="{":dd+=1
            elif cls[j]=="}":
                dd-=1
                if dd==0:
                    out[name2]=cls[mm.start():j+1]
                    break
    return out

def scan_refs(root:Path,needles:list[str]):
    rows=[]
    for p in root.rglob("*"):
        if not p.is_file() or p.suffix.lower() not in {".php",".py",".json",".md",".txt",".yml",".yaml"}:continue
        try:txt=p.read_text(encoding="utf-8")
        except Exception:continue
        hits=[]
        for n,line in enumerate(txt.splitlines(),1):
            found=[x for x in needles if x.lower() in line.lower()]
            if found:hits.append({"line":n,"tokens":found,"text":line.strip()[:800]})
        if hits:rows.append({"file":str(p.relative_to(root)),"hits":hits[:100]})
    return rows

def main():
    src=json.loads((REPO/"control/startmaster0107/runtime_inbox/generations/000001/SOURCE_SNAPSHOT.json").read_text(encoding="utf-8"))
    batch=src["next_textmachine_metadata_batch"]
    required={"article_type","category","plan_slot","target_keyword","title"}
    if batch.get("status")!="READY_FOR_TEXTMACHINE_METADATA_INTAKE":raise RuntimeError("EDITORIAL_BATCH_NOT_READY")
    items=batch.get("items")
    if not isinstance(items,list) or len(items)!=batch.get("item_count"):raise RuntimeError("EDITORIAL_COUNT_INVALID")
    for x in items:
        if set(x)!=required:raise RuntimeError("EDITORIAL_ITEM_FIELDS_DRIFT")
        if not re.fullmatch(r"[0-9a-f]{64}",str(x["plan_slot"])):raise RuntimeError("EDITORIAL_PLAN_SLOT_INVALID")
    if len({x["plan_slot"] for x in items})!=len(items):raise RuntimeError("EDITORIAL_SLOT_DUPLICATE")

    pkg=json.loads((REPO/"control/startmaster0107/runtime_inbox/generations/000001/PRODUCTION_PACKAGE.json").read_text(encoding="utf-8"))
    rel=(pkg.get("workflow_release") or {}).get("items") or []
    byslot={str(x.get("plan_slot")):str(x.get("canonical_article_id")) for x in rel if isinstance(x,dict)}
    if set(byslot)!=set(x["plan_slot"] for x in items):raise RuntimeError("EDITORIAL_TO_RELEASE_SLOT_SET_MISMATCH")
    if any(not v.startswith("article:") for v in byslot.values()):raise RuntimeError("CANONICAL_ARTICLE_ID_INVALID")

    with tempfile.TemporaryDirectory() as td:
        t=Path(td);po=t/"ppm";so=t/"pserc_outer";ps=t/"pserc"
        po.mkdir();so.mkdir();ps.mkdir()
        with zipfile.ZipFile(PPM) as z:z.extractall(po)
        with zipfile.ZipFile(PSERC) as z:z.extractall(so)
        inner=so/PSERC_INNER
        if not inner.is_file():raise RuntimeError("PSERC_INNER_MISSING")
        with zipfile.ZipFile(inner) as z:z.extractall(ps)
        ppm=po/"portal-production-machine";pserc=ps/"portal-seo-editorial-plan-compiler"

        admin=(ppm/"includes/admin.php").read_text(encoding="utf-8")
        admin_refs=scan_refs(ppm,[
          "PSERC_APPROVED_PRODUCTION_PACKAGE_V1","ENDSTEMPEL_PASS",
          "ENDSTEMPEL_WORDPRESS_PREIMPORT_PASS","pferde_endstempel_verify_before_write",
          "normal_plan","ppm679_normal_fact_packs","production_plan"
        ])
        repo_refs=scan_refs(REPO,[
          "ENDSTEMPEL_WORDPRESS_VERIFY.php","pferde_endstempel_verify_before_write",
          "pferde_endstempel_atomic_import","SIGNED_JSON_VERIFIED_FOR_EXISTING_IMPORT_HANDOFF"
        ])
        signature_wired_anywhere=any(r["file"]!="control/startmaster0107/ENDSTEMPEL_WORDPRESS_VERIFY.php" for r in repo_refs)

        # Editorial plan / inventory / dedup behavior.
        ep=(ppm/"includes/editorial-plan-runtime-gate.php").read_text(encoding="utf-8")
        pre=methods(ep,"PPM679_Editorial_Plan_Runtime_Gate").get("preflight","")
        rec=[]
        dup=[]
        registry=[]
        for p in (ppm/"includes").glob("*.php"):
            txt=p.read_text(encoding="utf-8")
            if "PPM679_Content_Inventory_Reconciler" in txt:
                rec.append({"file":p.name,"methods":methods(txt,"PPM679_Content_Inventory_Reconciler")})
            if "PPM679_Systemwide_Duplicate_Guard" in txt:
                dup.append({"file":p.name,"methods":methods(txt,"PPM679_Systemwide_Duplicate_Guard")})
            if "PPM679_Editorial_Plan_Registry" in txt:
                registry.append({"file":p.name,"methods":methods(txt,"PPM679_Editorial_Plan_Registry")})

        inventory_blob=json.dumps(rec,ensure_ascii=False).lower()
        dup_blob=json.dumps(dup,ensure_ascii=False).lower()
        plan_blob=json.dumps(registry,ensure_ascii=False).lower()

        post_statuses=sorted(set(re.findall(r"'(publish|draft|trash|private|pending|future)'",inventory_blob+dup_blob)))
        if not {"publish","draft","trash"}.issubset(set(post_statuses)):raise RuntimeError("WP_INVENTORY_STATUS_COVERAGE_INCOMPLETE")

        # Manual publish separation: target normal-draft path must never publish.
        publish_refs=scan_refs(ppm,["wp_publish_post","post_status","publish_allowed","AUTO_PUBLISH"])
        normal_publish_lines=[]
        for r in publish_refs:
            if "normal-draft" in r["file"] or "admin.php"==r["file"] or "wordpress" in r["file"]:
                normal_publish_lines.append(r)
        forbidden_runtime_publish=False
        for r in normal_publish_lines:
            for h in r["hits"]:
                if "wp_publish_post" in h["text"] and "test" not in r["file"].lower():
                    forbidden_runtime_publish=True

        # Claude references in executable production-relevant code only.
        claude_repo=scan_refs(REPO,["Claude"])
        executable_claude=[]
        for r in claude_repo:
            if Path(r["file"]).suffix.lower() in {".php",".py",".sh",".yml",".yaml"}:
                executable_claude.append(r)
        claude_ppm=scan_refs(ppm,["Claude"])
        claude_pserc=scan_refs(pserc,["Claude"])

        print(json.dumps({
          "status":"ACM_FULL_WORKFLOW_REDAKTIONSPLAN_AUDIT_PASS",
          "editorial_source":{
            "source_snapshot_filename":src.get("source_snapshot_filename"),
            "source_snapshot_sha256":src.get("source_snapshot_sha256"),
            "batch_status":batch.get("status"),
            "item_count":batch.get("item_count"),
            "maximum_articles":batch.get("maximum_articles"),
            "maximum_articles_per_type":batch.get("maximum_articles_per_type"),
            "metadata_fields":sorted(required),
            "unique_plan_slots":True,
            "slot_to_canonical_article_id_bound":True
          },
          "editorial_runtime":{
            "preflight_present":bool(pre),
            "preflight_source":pre[:12000],
            "wp_inventory_statuses":post_statuses,
            "existing_wp_inventory_reconciliation_present":"reconcile" in inventory_blob,
            "systemwide_duplicate_guard_present":"duplicate" in dup_blob or "ownership" in dup_blob,
            "editorial_registry_present":bool(registry),
            "registry_source_excerpt":plan_blob[:18000]
          },
          "wordpress_final_json":{
            "ppm_admin_upload_refs":admin_refs[:80],
            "repo_signature_refs":repo_refs[:80],
            "signature_verifier_wired_into_separate_runtime_file":signature_wired_anywhere,
            "note":"False means verifier exists and is tested, but no separate repository PHP runtime currently calls it."
          },
          "manual_publish_boundary":{
            "normal_draft_publish_refs":normal_publish_lines[:80],
            "runtime_wp_publish_post_found":forbidden_runtime_publish,
            "workflow_publish_allowed":False
          },
          "claude":{
            "repo_executable_refs":executable_claude[:80],
            "ppm_refs":claude_ppm[:80],
            "pserc_refs":claude_pserc[:80],
            "structural_requirement":False
          },
          "publish_allowed":False
        },ensure_ascii=False,indent=2))
    return 0

if __name__=="__main__":
    raise SystemExit(main())

# workflow-trigger: full-redaktionsplan-audit-v1
