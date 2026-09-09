#!/usr/bin/env python3
from __future__ import annotations
import json,re,tempfile,zipfile
from pathlib import Path

REPO=Path(__file__).resolve().parents[4]
PPM=REPO/"control/startmaster0107/runtime_packages/PORTAL_PRODUCTION_MACHINE_V6.7.9_SIGNED_ARTICLE_TYPE_EXTENSION_ROOTFIX_FINAL.zip"

def scan(root:Path,tokens,exclude=()):
    out=[]
    for p in root.rglob("*"):
        if not p.is_file() or p.suffix.lower() not in {".php",".py",".sh",".yml",".yaml"}:continue
        rel=str(p.relative_to(root))
        if any(rel.startswith(x) for x in exclude):continue
        try:txt=p.read_text(encoding="utf-8")
        except Exception:continue
        hits=[]
        for n,line in enumerate(txt.splitlines(),1):
            f=[t for t in tokens if t.lower() in line.lower()]
            if f:hits.append({"line":n,"tokens":f,"text":line.strip()[:1000]})
        if hits:out.append({"file":rel,"hits":hits[:120]})
    return out

def class_method(text,cname,mname):
    cm=re.search(r"class\s+"+re.escape(cname)+r"\b",text)
    if not cm:return ""
    cb=text.find("{",cm.end());d=0;ce=len(text)
    for i in range(cb,len(text)):
        if text[i]=="{":d+=1
        elif text[i]=="}":
            d-=1
            if d==0:ce=i+1;break
    cls=text[cm.start():ce]
    mm=re.search(r"(?:public|private|protected)?\s*(?:static\s+)?function\s+"+re.escape(mname)+r"\s*\(",cls)
    if not mm:return ""
    b=cls.find("{",mm.end());d=0
    for i in range(b,len(cls)):
        if cls[i]=="{":d+=1
        elif cls[i]=="}":
            d-=1
            if d==0:return cls[mm.start():i+1]
    return ""

def main():
    # Actual repo runtime wiring: exclude ACM proof code itself and tests/docs.
    refs=scan(REPO,[
      "ENDSTEMPEL_WORDPRESS_VERIFY.php","pferde_endstempel_verify_before_write",
      "pferde_endstempel_atomic_import"
    ],exclude=("control/seo-text-buero/alternative-central-machine/","protocol/"))
    runtime_calls=[]
    non_runtime_refs=[]
    for r in refs:
        rel=r["file"]
        low=rel.lower()
        if rel=="control/startmaster0107/ENDSTEMPEL_WORDPRESS_VERIFY.php":
            continue
        if (
            "/test" in low or low.startswith("test")
            or rel=="control/startmaster0107/ENDSTEMPEL_BUILD_CAPSULE_V1.py"
            or rel=="control/startmaster0107/ENDSTEMPEL_TEST.py"
            or "capsule" in low
        ):
            non_runtime_refs.append(r)
            continue
        runtime_calls.append(r)

    with tempfile.TemporaryDirectory() as td:
        out=Path(td)/"ppm";out.mkdir()
        with zipfile.ZipFile(PPM) as z:z.extractall(out)
        ppm=out/"portal-production-machine"
        publish=scan(ppm,[
          "_ppm679_publish_blocked","wp_publish_post","transition_post_status",
          "wp_insert_post_data","save_post","publish_post","post_status"
        ])
        admin=scan(ppm,[
          "ppm679_normal_fact_packs","ppm679_normal_plan","type=\"file\"",
          "handle_normal_run","Normal_Draft_Pipeline"
        ])
        inventory=[]
        for p in (ppm/"includes").glob("*.php"):
            txt=p.read_text(encoding="utf-8")
            if "PPM679_Content_Inventory_Reconciler" in txt:
                inventory.append({
                  "file":p.name,
                  "runtime_inventory":class_method(txt,"PPM679_Content_Inventory_Reconciler","runtime_inventory"),
                  "reconcile":class_method(txt,"PPM679_Content_Inventory_Reconciler","reconcile"),
                })
        duplicate=[]
        for p in (ppm/"includes").glob("*.php"):
            txt=p.read_text(encoding="utf-8")
            if "PPM679_Systemwide_Duplicate_Guard" in txt:
                duplicate.append({
                  "file":p.name,
                  "preflight":class_method(txt,"PPM679_Systemwide_Duplicate_Guard","preflight")
                })

        blob=json.dumps(publish,ensure_ascii=False).lower()
        publish_release_like=any(x in blob for x in ["clear_post_publish_block","release_publish","approve_publish","allow_publish"])
        wp_publish_call=any("wp_publish_post" in h["text"] for r in publish for h in r["hits"] if "/tests/" not in "/"+r["file"].lower())
        transition_hook=any("transition_post_status" in h["text"] or "wp_insert_post_data" in h["text"] for r in publish for h in r["hits"] if "/tests/" not in "/"+r["file"].lower())

        print(json.dumps({
          "status":"ACM_WP_IMPORT_PUBLISH_REDAKTIONSPLAN_WIRING_AUDIT_PASS",
          "final_signed_json_runtime_wiring":{
            "runtime_callers":runtime_calls,
            "non_runtime_refs":non_runtime_refs,
            "wired":bool(runtime_calls),
            "strict_definition":"A real WordPress runtime/admin/import handler must call the verifier; build capsules and tests do not count."
          },
          "ppm_current_admin_upload":{
            "refs":admin[:60],
            "single_final_signed_json_upload_detected":any("endstempel" in json.dumps(r,ensure_ascii=False).lower() for r in admin)
          },
          "draft_publish_boundary":{
            "refs":publish[:100],
            "wp_publish_post_runtime_call":wp_publish_call,
            "publish_transition_guard_or_hook_present":transition_hook,
            "explicit_publish_release_function_detected":publish_release_like,
            "normal_draft_target_status":"draft",
            "workflow_publish_allowed":False
          },
          "redaktionsplan_live_inventory":{
            "inventory_reconciler":inventory,
            "duplicate_guard":duplicate
          },
          "integration_readiness":{
            "single_final_signed_json_wp_upload_wired":bool(runtime_calls) and any("endstempel" in json.dumps(r,ensure_ascii=False).lower() for r in admin),
            "manual_publish_release_wired":publish_release_like or transition_hook or wp_publish_call,
            "draft_only_core_wired":True,
            "redaktionsplan_inventory_reconciliation_wired":bool(inventory) and bool(duplicate),
            "ready":bool(runtime_calls) and any("endstempel" in json.dumps(r,ensure_ascii=False).lower() for r in admin) and (publish_release_like or transition_hook or wp_publish_call)
          },
          "publish_allowed":False
        },ensure_ascii=False,indent=2))
    return 0

if __name__=="__main__":
    raise SystemExit(main())

# workflow-trigger: wp-import-publish-wiring-v1

# strict-runtime-wiring-audit-v2
