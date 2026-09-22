#!/usr/bin/env python3
from __future__ import annotations
import hashlib, io, json, os, zipfile
from pathlib import Path

OUT=Path(__file__).resolve().parents[1]/"CATEGORY_INTEGRATION_HOBBYRAUM"/"out"
OUT.mkdir(parents=True,exist_ok=True)
outer=Path(os.environ.get("PSERC_ZIP","/tmp/pserc.zip"))
expected="77a14aca97f46d60bc9001d66327abb68dd9cac9ad111f8ecefa1a8afd345314"
sha=hashlib.sha256(outer.read_bytes()).hexdigest()
if sha!=expected: raise SystemExit("PSERC_SHA_MISMATCH:"+sha)
inner_name="PSERC-FIX/portal-seo-editorial-plan-compiler_0.28.18_ENDSTEMPEL_IMPORT_ENVELOPE_BINDING.zip"
with zipfile.ZipFile(outer) as z:
    raw=z.read(inner_name)
with zipfile.ZipFile(io.BytesIO(raw)) as z:
    names=z.namelist()
    terms=[
      "PSERC_PORTAL_STRUCTURE_REGISTRY_V1",
      "PSTE_PORTAL_TAXONOMY_SNAPSHOT_V3",
      "portal_structure_registry",
      "category_slug",
      "get_terms(",
      "get_pages(",
      "WORDPRESS_READ_ONLY",
      "taxonomy",
      "structure",
      "current",
    ]
    hits={t:[] for t in terms}
    headers=[]
    for name in names:
        if name.endswith("/"): continue
        try: txt=z.read(name).decode("utf-8")
        except Exception: continue
        if "Plugin Name:" in txt or "Version:" in txt[:2000]:
            if "portal-seo-editorial-plan-compiler" in name.lower() or "Plugin Name:" in txt:
                headers.append({"member":name,"head":"\n".join(txt.splitlines()[:40])})
        lines=txt.splitlines()
        low=txt.lower()
        for t in terms:
            if t.lower() not in low: continue
            for i,line in enumerate(lines):
                if t.lower() in line.lower():
                    hits[t].append({"member":name,"line":i+1,"context":"\n".join(lines[max(0,i-6):min(len(lines),i+12)])})
                    if len(hits[t])>=40: break
    registry_name="portal-seo-editorial-plan-compiler/contracts/portal-structure-registry-v1.json"
    registry=json.loads(z.read(registry_name).decode("utf-8"))
    registry_summary={
      "contract":registry.get("contract"),
      "version":registry.get("version"),
      "source":registry.get("source"),
      "entry_count":len(registry.get("entries") or []),
      "registry_sha256":registry.get("registry_sha256"),
      "top_keys":list(registry.keys()),
      "first_entries":(registry.get("entries") or [])[:3],
      "last_entries":(registry.get("entries") or [])[-3:],
    }
    integrity=[]
    for name in names:
        if name.endswith("/") or not name.lower().endswith((".json",".php",".txt",".md")): continue
        try: txt=z.read(name).decode("utf-8")
        except Exception: continue
        if "portal-structure-registry-v1.json" in txt or registry.get("registry_sha256","") in txt or (registry.get("source") or {}).get("raw_sha256","") in txt:
            integrity.append({"member":name,"contains_registry_path":"portal-structure-registry-v1.json" in txt,"contains_registry_hash":registry.get("registry_sha256","") in txt,"contains_source_hash":(registry.get("source") or {}).get("raw_sha256","") in txt})
    gate_name="portal-seo-editorial-plan-compiler/includes/class-pserc-portal-structure-gate.php"
    gate_text=z.read(gate_name).decode("utf-8")
    out={"status":"PASS_READ_ONLY","outer_sha256":sha,"inner_sha256":hashlib.sha256(raw).hexdigest(),"inner_files":len(names),"headers":headers,"registry":registry_summary,"registry_integrity_references":integrity,"portal_structure_gate_full":gate_text,"hits":hits}
    (OUT/"pserc-category-audit.json").write_text(json.dumps(out,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
    print(json.dumps(out,ensure_ascii=False,indent=2))
    print("PSERC_CATEGORY_READ_ONLY_AUDIT_PASS")
