#!/usr/bin/env python3
from __future__ import annotations

import argparse
import importlib.util
import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
REPO_ROOT = HERE.parents[3]

class H8RuntimeBlocked(RuntimeError):
    pass

def _module(path: Path, name: str):
    if not path.is_file():
        raise H8RuntimeBlocked("MODULE_MISSING:" + path.name)
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise H8RuntimeBlocked("MODULE_LOAD_FAILED:" + path.name)
    mod = importlib.util.module_from_spec(spec)
    sys.modules[name] = mod
    try:
        spec.loader.exec_module(mod)
    except Exception:
        sys.modules.pop(name, None)
        raise
    return mod

def validate(repo: Path, contract_path: Path, state_path: Path):
    repo = Path(repo).resolve()
    legacy = _module(repo / "control/startmaster0107/runtime_inbox/runtime_batch_slot_guard.py", "h8_legacy_runtime_guard")
    out = legacy.validate(repo, Path(contract_path).resolve(), Path(state_path).resolve())
    if out.get("status") != "RUNTIME_INPUTS_BOUND":
        return out
    provenance = _module(repo / "control/single-door-boundary/preproduction_provenance_guard.py", "h8_runtime_provenance")
    proof = provenance.validate_attached_package(repo)
    if proof.get("status") != "H8_PREPRODUCTION_PROVENANCE_PASS":
        raise H8RuntimeBlocked("H8_ATTACHED_PROVENANCE_NOT_PASS")
    result = dict(out)
    result["h8_provenance_status"] = proof["status"]
    result["h8_bootstrap_authority_sha256"] = proof["bootstrap_authority_sha256"]
    result["authoritative_execution_origin"] = "SINGLE_DOOR_BOOTSTRAP_ONLY"
    result["content_semantics_inspected"] = False
    result["quality_authority"] = "NONE"
    return result

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("state")
    ap.add_argument("--contract", required=True)
    ap.add_argument("--repo", default=".")
    args = ap.parse_args()
    try:
        out = validate(Path(args.repo), Path(args.contract), Path(args.state))
        print(json.dumps(out, ensure_ascii=False, indent=2))
        return 0
    except Exception as exc:
        print(json.dumps({
            "ok": False,
            "status": "H8_RUNTIME_BATCH_SLOT_BLOCKED",
            "error": str(exc),
            "publish_allowed": False,
        }, ensure_ascii=False, indent=2))
        return 2

if __name__ == "__main__":
    raise SystemExit(main())
