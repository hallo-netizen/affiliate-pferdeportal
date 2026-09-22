#!/usr/bin/env python3
from __future__ import annotations

import hashlib
import importlib.util
import json
import tempfile
from pathlib import Path

HERE = Path(__file__).resolve().parent
RUNTIME_FILES = [
    HERE / "runner.py",
    HERE / "resumable_runner.py",
    HERE / "full_workflow_gate.py",
    HERE / "entry_hardlock.py",
    HERE / "binding_transport_gate.py",
]
FORBIDDEN = [
    "REAL7_CHATGPT_RUN_001",
    "PSERC_REALTEST_7_READY",
    "GEN1_7_ARTIKEL",
    "Hindernisstangen",
    "Reitplatzbeleuchtung",
    "Mistcontainer",
    "Pferdehaftpflicht",
    "Huffett",
    "Fliegenmasken",
    "Pellets für Pferde",
]

def sha(raw: bytes) -> str:
    return hashlib.sha256(raw).hexdigest()

def stable(value) -> str:
    return sha(json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode("utf-8"))

def load_entry_hardlock():
    p = HERE / "entry_hardlock.py"
    spec = importlib.util.spec_from_file_location("entry_hardlock_genericity", p)
    mod = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(mod)
    return mod

def make_case(count: int, completed: int):
    m = load_entry_hardlock()
    batch = sha(f"generic-batch-{count}".encode())
    core = {
        "contract": "CONCEPT_AGENT_WORK_BINDING_TEST_V1",
        "batch_sha256": batch,
        "item_count": count,
        "items": [
            {
                "item_index": i,
                "plan_slot": sha(f"slot-{count}-{i}".encode()),
                "opaque_bound_work_sha256": sha(f"bound-{count}-{i}".encode()),
            }
            for i in range(count)
        ],
        "publish_allowed": False,
    }
    binding_sha = stable(core)
    transport = {**core, "binding_sha256": binding_sha}
    raw = (json.dumps(transport, ensure_ascii=False, sort_keys=True, separators=(",", ":")) + "\n").encode("utf-8")
    pointer = {
        "contract": m.POINTER_CONTRACT,
        "workflow": m.WORKFLOW,
        "batch_sha256": batch,
        "item_count": count,
        "intake_sha256": sha(b"intake"),
        "research_binding_sha256": sha(b"research"),
        "authoring_bindings_file_sha256": sha(b"authoring"),
        "cross_chat_transport_filename": "CONCEPT_AGENT_CURRENT_WORK_BINDING.json",
        "cross_chat_transport_sha256": sha(raw),
        "cross_chat_transport_binding_sha256": binding_sha,
        "cross_chat_transport_required": True,
        "publish_allowed": False,
    }
    current = {
        "concept_agent_current_batch": {
            "workflow": m.WORKFLOW,
            "batch_sha256": batch,
            "item_count": count,
            "cross_chat_transport_filename": pointer["cross_chat_transport_filename"],
            "cross_chat_transport_sha256": pointer["cross_chat_transport_sha256"],
            "intake_status": "PASS",
            "research_binding_status": "PASS",
            "authoring_binding_status": "PASS",
            "article_bodies_completed": completed,
            "next_article_index": completed,
            "publish_allowed": False,
        }
    }
    with tempfile.TemporaryDirectory() as td:
        td = Path(td)
        pp = td / "pointer.json"
        sp = td / "current.json"
        tp = td / "transport.json"
        pp.write_text(json.dumps(pointer), encoding="utf-8")
        sp.write_text(json.dumps(current), encoding="utf-8")
        tp.write_bytes(raw)
        decision = m.probe(pp, sp, tp)
    if decision.get("status") != "READY":
        raise SystemExit(f"GENERIC_CASE_NOT_READY:{count}:{completed}")
    if decision.get("item_count") != count:
        raise SystemExit(f"GENERIC_COUNT_CHANGED:{count}")
    if decision.get("next_article_index") != completed:
        raise SystemExit(f"GENERIC_PROGRESS_CHANGED:{count}:{completed}")
    return {
        "item_count": count,
        "completed": completed,
        "next_article_index": decision["next_article_index"],
        "status": "PASS",
    }

def main() -> int:
    forbidden_hits = []
    for path in RUNTIME_FILES:
        text = path.read_text(encoding="utf-8")
        for token in FORBIDDEN:
            if token in text:
                forbidden_hits.append({"file": path.name, "token": token})
    if forbidden_hits:
        print(json.dumps({"status":"BLOCKED","forbidden_hits":forbidden_hits}, indent=2))
        return 2

    cases = []
    for count in (1, 2, 17):
        points = sorted({0, max(0, count // 2), max(0, count - 1)})
        for completed in points:
            cases.append(make_case(count, completed))

    proof = {
        "contract": "CONCEPT_AGENT_RUNTIME_GENERICITY_PROOF_V1",
        "status": "PASS",
        "runtime_files": [p.name for p in RUNTIME_FILES],
        "forbidden_legacy_runtime_references": 0,
        "tested_item_counts": [1, 2, 17],
        "tested_cases": cases,
        "rule": "RUNTIME_COUNT_AND_PROGRESS_FROM_BINDING_ONLY",
        "publish_allowed": False,
    }
    proof["proof_sha256"] = stable(proof)
    out = Path("/tmp/concept-agent-genericity")
    out.mkdir(parents=True, exist_ok=True)
    (out / "CONCEPT_AGENT_RUNTIME_GENERICITY_PROOF_V1.json").write_text(
        json.dumps(proof, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    print(json.dumps(proof, ensure_ascii=False, indent=2))
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
