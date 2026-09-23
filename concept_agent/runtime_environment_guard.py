#!/usr/bin/env python3
from __future__ import annotations

import hashlib
import importlib.util
import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
REPO = HERE.parent
VALIDATOR_REL = "control/startmaster0107/codex-production-runtime/codex_environment_preflight.py"
TOOLBOX_REL = "control/startmaster0107/codex-production-runtime/RUNTIME_TOOLBOX_MANIFEST.json"
CONTRACT = "CONCEPT_AGENT_CANONICAL_RUNTIME_BINDING_V1"

class Blocked(RuntimeError):
    pass

def canon(value) -> bytes:
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode("utf-8")

def stable(value) -> str:
    return hashlib.sha256(canon(value)).hexdigest()

def file_sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()

def _validator(repo: Path):
    path = (Path(repo) / VALIDATOR_REL).resolve()
    if not path.is_file():
        raise Blocked("CANONICAL_RUNTIME_VALIDATOR_MISSING")
    spec = importlib.util.spec_from_file_location("concept_agent_runtime_validator", path)
    if spec is None or spec.loader is None:
        raise Blocked("CANONICAL_RUNTIME_VALIDATOR_LOAD_FAILED")
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)
    return module, path

def current_binding(repo: Path = REPO) -> dict:
    repo = Path(repo).resolve()
    try:
        validator, validator_path = _validator(repo)
        manifest, manifest_sha = validator.validate_toolbox_manifest(repo)
        raw_tools = validator.validate_runtime_tools(repo, manifest, manifest_sha)
        tools = validator.require_runtime_tools(raw_tools, manifest, manifest_sha)
    except Blocked:
        raise
    except Exception as exc:
        raise Blocked("CANONICAL_EXECUTION_ENVIRONMENT_NOT_READY:" + str(exc)) from exc

    required_true = {
        "php_executable": True,
        "java_executable": True,
        "ed25519_runtime": True,
        "languagetool_real_execution": True,
        "agent_network_required": False,
        "content_semantics_inspected": False,
        "publish_allowed": False,
    }
    for key, expected in required_true.items():
        if tools.get(key) != expected:
            raise Blocked("CANONICAL_RUNTIME_TOOL_INVALID:" + key)

    result = {
        "contract": CONTRACT,
        "status": "PASS",
        "validator_ref": VALIDATOR_REL,
        "validator_sha256": file_sha(validator_path),
        "toolbox_manifest_ref": TOOLBOX_REL,
        "toolbox_manifest_sha256": manifest_sha,
        "runtime_tools_sha256": stable(tools),
        "languagetool_engine": tools.get("languagetool_engine"),
        "languagetool_jar_sha256": tools.get("languagetool_jar_sha256"),
        "ppm679_package_sha256": tools.get("ppm679_package_sha256"),
        "pserc_fix_package_sha256": tools.get("pserc_fix_package_sha256"),
        "free_tool_selection": False,
        "free_binary_lookup": False,
        "fallback_runtime_allowed": False,
        "publish_allowed": False,
    }
    result["binding_sha256"] = stable(result)
    return result

def verify(value: dict, repo: Path = REPO) -> dict:
    if not isinstance(value, dict) or value.get("contract") != CONTRACT:
        raise Blocked("CANONICAL_RUNTIME_BINDING_CONTRACT_INVALID")
    core = dict(value)
    declared = core.pop("binding_sha256", None)
    if declared != stable(core):
        raise Blocked("CANONICAL_RUNTIME_BINDING_HASH_MISMATCH")
    expected = current_binding(repo)
    if value != expected:
        raise Blocked("CANONICAL_RUNTIME_BINDING_NOT_CURRENT")
    return value

def main(argv: list[str]) -> int:
    try:
        if argv not in (["probe"], ["verify"]):
            raise Blocked("USE: runtime_environment_guard.py probe")
        value = current_binding(REPO)
        print(json.dumps(value, ensure_ascii=False, sort_keys=True))
        return 0
    except Exception as exc:
        print("CONCEPT_AGENT_RUNTIME_BLOCKED:" + str(exc), file=sys.stderr)
        return 2

if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
