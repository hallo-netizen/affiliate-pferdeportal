#!/usr/bin/env python3
from __future__ import annotations

import hashlib
import importlib.util
import json
import tempfile
from pathlib import Path

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[1]


def load(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def load_module(path: Path, name: str):
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError("MODULE_LOAD_FAILED")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def check(condition: bool, message: str):
    if not condition:
        raise AssertionError(message)


def main() -> int:
    policy_path = HERE / "OUTPUT_VISIBILITY_POLICY.json"
    policy = load(policy_path)
    check(policy["chat_output_authority"] == "NONE", "CHAT_OUTPUT_AUTHORITY")
    check(policy["domain_logic_authority"] == "NONE", "DOMAIN_AUTHORITY")
    check(policy["content_semantics_authority"] == "NONE", "CONTENT_AUTHORITY")
    check(policy["quality_authority"] == "NONE", "QUALITY_AUTHORITY")
    check(policy["design_authority"] == "NONE", "DESIGN_AUTHORITY")
    check(policy["seo_authority"] == "NONE", "SEO_AUTHORITY")
    check(policy["publish_allowed"] is False, "PUBLISH")
    check(policy["unbound_output_policy"] == "QUARANTINE_INVALID_NEVER_SURFACE_AS_PROJECT_RESULT", "UNBOUND_POLICY")

    pointer = load(REPO / "control/CURRENT_STARTMASTER.json")
    state_path = REPO / pointer["state_ref"]
    root_path = REPO / pointer["root_ref"]
    state = load(state_path)
    root = load(root_path)
    gate = state["execution_gate"]
    bundle_path = REPO / gate["bundle_ref"]
    bundle = load(bundle_path)

    check(pointer["free_chat_execution_authority"] is False, "FREE_CHAT_EXECUTION_AUTHORITY")
    check(pointer["chat_output_authority"] == "NONE", "POINTER_CHAT_OUTPUT_AUTHORITY")
    check(pointer["visible_output_authority"] == "RELEASE_RECEIPT_ONLY", "VISIBLE_OUTPUT_AUTHORITY")
    check(pointer["visible_output_policy_sha256"] == sha256(policy_path), "POLICY_HASH")
    check(pointer["worker_freshness_guard_sha256"] == sha256(HERE / "worker_freshness_guard.py"), "FRESHNESS_HASH")
    check(pointer["output_release_gate_sha256"] == sha256(HERE / "output_release_gate.py"), "RELEASE_GATE_HASH")
    check(root["current_state_sha256"] == sha256(state_path), "ROOT_STATE_HASH")
    check(gate["bundle_sha256"] == sha256(bundle_path), "STATE_BUNDLE_HASH")
    check(state["execution_gate_rearm_target"]["bundle_sha256"] == sha256(bundle_path), "REARM_BUNDLE_HASH")
    check(gate["domain_logic_authority"] == "NONE", "STATE_DOMAIN_AUTHORITY")
    check(gate["content_quality_design_authority"] == "NONE", "STATE_CONTENT_QUALITY_AUTHORITY")
    check(state["publish_allowed"] is False, "STATE_PUBLISH")

    bindings = {row["ref"]: row["sha256"] for row in bundle["authorized_inputs"]}
    required = {
        pointer["visible_output_policy_ref"]: pointer["visible_output_policy_sha256"],
        pointer["worker_freshness_guard_ref"]: pointer["worker_freshness_guard_sha256"],
        pointer["output_release_gate_ref"]: pointer["output_release_gate_sha256"],
        "control/startmaster0107/START_OPTIMIZATION_POLICY_20260831.json": sha256(REPO / "control/startmaster0107/START_OPTIMIZATION_POLICY_20260831.json"),
    }
    for ref, digest in required.items():
        check(bindings.get(ref) == digest, "BUNDLE_BINDING:" + ref)

    instruction = bundle["instruction"]
    freshness = instruction.find("worker_freshness_guard.py")
    project_entry = instruction.find("project_single_door_entry_v2.py status")
    release_gate = instruction.find("output_release_gate.py release")
    complete = instruction.find("cloud_entry.py complete")
    check(freshness >= 0 and project_entry >= 0 and freshness < project_entry, "FRESHNESS_NOT_FIRST")
    check(release_gate >= 0 and complete >= 0 and release_gate < complete, "RELEASE_NOT_BEFORE_COMPLETE")
    check(".pferde-quarantine/" in instruction, "QUARANTINE_NOT_BOUND")
    check("RELEASE_RECEIPT" in instruction, "RELEASE_RECEIPT_NOT_BOUND")
    check("Keine eigene Workflowentscheidung" in instruction, "NO_NAVIGATION_RULE_MISSING")

    gate_module = load_module(HERE / "output_release_gate.py", "output_release_gate_test")
    with tempfile.TemporaryDirectory() as td:
        base = Path(td)
        q = base / ".pferde-quarantine"
        q.mkdir()
        f = q / "x.bin"
        f.write_bytes(b"ok")
        digest = hashlib.sha256(b"ok").hexdigest()
        old_repo = gate_module.REPO
        gate_module.REPO = base
        try:
            verified = gate_module.verify_outputs(
                {"worker_quarantine_root": ".pferde-quarantine"},
                [{"ref": ".pferde-quarantine/x.bin", "sha256": digest}],
            )
            check(len(verified) == 1, "POSITIVE_OUTPUT_VERIFY")
            try:
                gate_module.verify_outputs(
                    {"worker_quarantine_root": ".pferde-quarantine"},
                    [{"ref": "outside/x.bin", "sha256": digest}],
                )
                raise AssertionError("OUTSIDE_NOT_BLOCKED")
            except gate_module.Blocked as exc:
                check(str(exc).startswith("OUTPUT_OUTSIDE_QUARANTINE"), "OUTSIDE_REASON")
            try:
                gate_module.verify_outputs(
                    {"worker_quarantine_root": ".pferde-quarantine"},
                    [{"ref": ".pferde-quarantine/x.bin", "sha256": "0" * 64}],
                )
                raise AssertionError("HASH_MISMATCH_NOT_BLOCKED")
            except gate_module.Blocked as exc:
                check(str(exc).startswith("OUTPUT_HASH_MISMATCH"), "HASH_REASON")
        finally:
            gate_module.REPO = old_repo

    for source_path in (HERE / "output_release_gate.py", HERE / "worker_freshness_guard.py"):
        source = source_path.read_text(encoding="utf-8")
        for token in ("body_html", "body_text", "post_content", "keyword density", "rewrite("):
            check(token not in source, "CONTENT_MUTATION_TOKEN:" + source_path.name + ":" + token)

    print("OUTPUT_QUARANTINE_TEST_PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
