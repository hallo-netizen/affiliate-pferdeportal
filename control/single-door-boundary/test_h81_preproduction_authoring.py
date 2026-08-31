#!/usr/bin/env python3
from __future__ import annotations
import importlib.util,json,sys,tempfile
from pathlib import Path
HERE=Path(__file__).resolve().parent;REPO=HERE.parents[1]
def load(p,name):
    s=importlib.util.spec_from_file_location(name,p);assert s and s.loader;m=importlib.util.module_from_spec(s);sys.modules[name]=m;s.loader.exec_module(m);return m
def blocked(fn,token):
    try: fn()
    except Exception as e:
        assert token in str(e),(token,str(e));return
    raise AssertionError("expected block "+token)
entry=load(HERE/"project_single_door_entry_v3.py","h81_test_entry")
author=load(HERE/"single_door_authoring_entry.py","h81_test_author")
prov=load(HERE/"preproduction_provenance_guard_v2.py","h81_test_prov")
real=entry.resolve_entry(repo=REPO)
assert real["status"]=="PREPRODUCTION_AUTHORING_SINGLE_DOOR_REQUIRED" and real["room_token"]=="R_AUTHOR_001"
req=real["worker_request"];assert req["input"]=="R_AUTHOR_001" and len(req["tools"])==1 and req["parallel_tool_calls"] is False
idle=entry.resolve_entry(repo=REPO,runtime_provider=lambda r:{"status":"READY_IDLE"});assert idle["status"]=="PROJECT_ARMED_NO_ACTIVE_BATCH"
prod=entry.resolve_entry(repo=REPO,runtime_provider=lambda r:{"status":"RUNTIME_INPUTS_BOUND","selected_item_count":7},attached_provenance_provider=lambda r:{"status":"H81_PREPRODUCTION_PROVENANCE_PASS","entry_receipt_sha256":"a"*64},route_provider=lambda r,c,m:{"room_token":"R_001","worker_request":{"input":"R_001"}})
assert prod["status"]=="PRODUCTIVE_SINGLE_DOOR_READY" and prod["item_count"]==7
blocked(lambda:entry.resolve_entry(repo=REPO,runtime_provider=lambda r:{"status":"RUNTIME_INPUTS_BOUND","selected_item_count":7},attached_provenance_provider=lambda r:{"status":"NO"},route_provider=lambda r,c,m:{"room_token":"R_001","worker_request":{}}),"ATTACHED_PACKAGE_PROVENANCE_NOT_PASS")
r=author.build_entry_receipt(REPO,created_at_utc="2026-08-31T10:00:00Z");assert author.validate_entry_receipt(REPO,r)==r
bad=dict(r);bad["batch_sha256"]="0"*64;blocked(lambda:author.validate_entry_receipt(REPO,bad),"RECEIPT_HASH_INVALID")
base_release={"contract":"WORKFLOW_SUPERVISOR_RELEASE_V2_SIGNED","status":"PASS","authoring_role":prov.EXPECTED_AUTHORING_ROLE,"sequence":prov.EXPECTED_SEQUENCE,"content_generation_performed_by_supervisor":False,"wordpress_write_performed":False,"created_at_utc":"2026-08-31T10:01:00Z","items":[{"authoring_process":prov.EXPECTED_AUTHORING_PROCESS,"research_evidence_gate_status":"PASS","article_origin_gate_status":"PASS","language_quality_gate_status":"PASS","external_rewrite_detected":False,"trusted_self_approval":False,"content_hash_locked":True}]}
with tempfile.TemporaryDirectory() as td:
    p=Path(td)/"pkg.json";p.write_text(json.dumps({"workflow_release":base_release}),encoding="utf-8")
    proof=prov.validate_signed_existing_process(REPO,p,release_validator=lambda p,r:{"ok":True,"package_id":"x","artifact_sha256":"b"*64},entry_receipt_provider=lambda r:r0)
