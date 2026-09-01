#!/usr/bin/env python3
from __future__ import annotations
import base64, hashlib, importlib.util, json, sys
from pathlib import Path
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PrivateKey

REPO=Path(__file__).resolve().parents[2]
FROZEN_TEST_CONTRACT_SHA256="822401d582a751a99e519341e9c1560d198f37778ed67ba42dd5b9a111b4b59f"

def mod(p,n):
    s=importlib.util.spec_from_file_location(n,p)
    if s is None or s.loader is None: raise RuntimeError("MODULE_LOAD_FAILED")
    m=importlib.util.module_from_spec(s); sys.modules[n]=m; s.loader.exec_module(m); return m
def stable(o): return hashlib.sha256(json.dumps(o,ensure_ascii=False,sort_keys=True,separators=(",",":")).encode()).hexdigest()
def sign(payload):
    priv=Ed25519PrivateKey.generate()
    pub=priv.public_key().public_bytes(encoding=serialization.Encoding.Raw,format=serialization.PublicFormat.Raw)
    pub_sha=hashlib.sha256(pub).hexdigest(); key="test-"+pub_sha[:16]
    p=dict(payload); p.update(contract="WORKFLOW_SUPERVISOR_RELEASE_V2_SIGNED",status="PASS",signature_algorithm="ED25519",signing_key_id=key,signing_public_key_sha256=pub_sha)
    payload_sha=stable(p); p["release_payload_sha256"]=payload_sha; p["signature_b64"]=base64.b64encode(priv.sign(payload_sha.encode("ascii"))).decode("ascii")
    p["release_sha256"]=stable(p)
    return p,{key:{"sha256":pub_sha,"public_key_b64":base64.b64encode(pub).decode("ascii")}}
def blocked(fn):
    try: fn()
    except Exception: return True
    return False

def main():
    bridge=mod(REPO/"control/single-door-boundary/codex_current_room_bridge.py","rootfix_bridge_test")
    runtime=mod(REPO/"control/output-quarantine/runtime_entry_gate.py","rootfix_runtime_test")
    s={"ticket_id":"a"*64,"state_sha256":"b"*64,"bundle_sha256":"c"*64,"batch_sha256":"d"*64,"current_room_token":"R_D_1_01"}
    it={"canonical_article_id":"article:test","plan_slot":"e"*64}
    outputs=[{"ref":".pferde-quarantine/a/x.json","sha256":"f"*64}]
    item={
        "terminal_completion_contract":"PFERDE_ATELIER_FACHWORKFLOW_TERMINAL_COMPLETION_V1",
        "terminal_phase":"107007_ITEM","terminal_gate_id":"EXISTING_UNCHANGED_FACHWORKFLOW_TERMINAL_PASS",
        "ticket_id":s["ticket_id"],"state_sha256":s["state_sha256"],"bundle_sha256":s["bundle_sha256"],"batch_sha256":s["batch_sha256"],
        "room_token":s["current_room_token"],"canonical_article_id":it["canonical_article_id"],"plan_slot":it["plan_slot"],
        "outputs_manifest_sha256":bridge.outputs_manifest_sha256(outputs),"content_or_quality_rules_changed":False,"publish_allowed":False,
    }
    assert blocked(lambda: bridge.validate_item_terminal_completion(dict(item),s,it,outputs))
    signed,keys=sign(item)
    assert bridge.validate_item_terminal_completion(signed,s,it,outputs,trusted_keys=keys)["status"]=="SIGNED_TERMINAL_FACHWORKFLOW_COMPLETION_PASS"
    wrong,wrongkeys=sign({**item,"canonical_article_id":"article:other"})
    assert blocked(lambda: bridge.validate_item_terminal_completion(wrong,s,it,outputs,trusted_keys=wrongkeys))

    binding={"prepared_ref":".pferde-release-staging/x","prepared_sha256":"1"*64,"batch_sha256":"2"*64}
    ticket={"ticket_id":"3"*64,"state_sha256":"4"*64,"bundle_sha256":"5"*64}
    final={
        "terminal_completion_contract":"PFERDE_ATELIER_FACHWORKFLOW_TERMINAL_COMPLETION_V1",
        "terminal_phase":"107008_FINAL_REVIEW","terminal_gate_id":"EXISTING_UNCHANGED_FINAL_FACHREVIEW_TERMINAL_PASS",
        "ticket_id":ticket["ticket_id"],"state_sha256":ticket["state_sha256"],"bundle_sha256":ticket["bundle_sha256"],
        "prepared_release_ref":binding["prepared_ref"],"prepared_release_sha256":binding["prepared_sha256"],"prepared_batch_sha256":binding["batch_sha256"],
        "reviewed_prepared_release_only":True,"content_or_quality_rules_changed":False,"publish_allowed":False,
    }
    assert blocked(lambda: runtime.validate_final_terminal_completion(dict(final),binding,ticket))
    sf,kf=sign(final)
    assert runtime.validate_final_terminal_completion(sf,binding,ticket,trusted_keys=kf)["status"]=="SIGNED_TERMINAL_FINAL_REVIEW_COMPLETION_PASS"
    stale,ks=sign({**final,"ticket_id":"6"*64})
    assert blocked(lambda: runtime.validate_final_terminal_completion(stale,binding,ticket,trusted_keys=ks))
    print(json.dumps({"ok":True,"status":"STARTMASTER0107_FROZEN_TERMINAL_PROOF_TESTS_PASS","frozen_test_contract_sha256":FROZEN_TEST_CONTRACT_SHA256,"domain_or_quality_rules_changed":False,"publish_allowed":False},indent=2))
    return 0
if __name__=="__main__": raise SystemExit(main())
