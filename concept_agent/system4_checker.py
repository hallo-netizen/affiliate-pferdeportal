#!/usr/bin/env python3
from __future__ import annotations

import hashlib
import json
import os
import subprocess
import sys
import tempfile
from pathlib import Path
from typing import Any

REPO = Path(__file__).resolve().parents[1]
S4 = REPO / "isolated_system4"
if str(S4) not in sys.path:
    sys.path.insert(0, str(S4))

import authoring_contract
import controller_engine

SYSTEM4_BOUND_CONTRACT = "CONCEPT_AGENT_SYSTEM4_BOUND_ITEM_V1"


class Blocked(RuntimeError):
    pass


def stable(value: Any) -> str:
    return hashlib.sha256(json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode("utf-8")).hexdigest()


def sha_text(value: str) -> str:
    return hashlib.sha256(value.encode("utf-8")).hexdigest()


def _run(args: list[str], env: dict[str, str]) -> subprocess.CompletedProcess[str]:
    return subprocess.run(args, cwd=REPO, env=env, text=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, timeout=360, check=False)


def _state_base(item: dict[str, Any], bound: dict[str, Any], batch_sha: str) -> dict[str, Any]:
    article = {k: item[k] for k in ("title", "target_keyword", "category", "article_type", "plan_slot")}
    research_text = json.dumps(bound["research_document"], ensure_ascii=False, sort_keys=True, separators=(",", ":"))
    facts_text = json.dumps(bound["facts_document"], ensure_ascii=False, sort_keys=True, separators=(",", ":"))
    state = {
        "contract": controller_engine.CONTRACT,
        "source_snapshot_sha256": bound["source_snapshot_sha256"],
        "batch_sha256": batch_sha,
        "article": article,
        "immutable_core_sha256": "",
        "publish_allowed": False,
        "phase": "DRAFT_REQUIRED",
        "revision": 0,
        "research": {"text": research_text, "sha256": sha_text(research_text)},
        "facts": {"text": facts_text, "sha256": sha_text(facts_text)},
        "production_context": bound["production_context"],
        "authoring_contract": bound["authoring_contract"],
        "draft_markdown": None,
        "draft_sha256": None,
        "checks": {},
        "last_error": None,
        "release_prepared": None,
        "released": False,
    }
    state["immutable_core_sha256"] = controller_engine.sha(controller_engine.immutable_core(state))
    controller_engine.verify_state(state)
    authoring_contract.validate_bound(REPO, state)
    return state


def check(request: dict[str, Any]) -> tuple[dict[str, Any], int]:
    if request.get("contract") != "CONCEPT_AGENT_CHECK_REQUEST_V1" or request.get("publish_allowed") is not False:
        raise Blocked("CHECK_REQUEST_INVALID")
    item = request.get("item")
    if not isinstance(item, dict):
        raise Blocked("CHECK_ITEM_INVALID")
    bound = item.get("system4_bound")
    if not isinstance(bound, dict) or bound.get("contract") != SYSTEM4_BOUND_CONTRACT or bound.get("publish_allowed") is not False:
        raise Blocked("SYSTEM4_BOUND_ITEM_MISSING")
    declared = bound.get("binding_sha256")
    core = dict(bound)
    core.pop("binding_sha256", None)
    if declared != stable(core):
        raise Blocked("SYSTEM4_BOUND_ITEM_HASH_MISMATCH")
    if request.get("plan_slot") != item.get("plan_slot") or request.get("item_index") != item.get("item_index"):
        raise Blocked("CHECK_IDENTITY_MISMATCH")
    body = request.get("body_html")
    if not isinstance(body, str) or not body.strip():
        raise Blocked("CHECK_BODY_EMPTY")
    revision = request.get("revision")
    if not isinstance(revision, int) or isinstance(revision, bool) or revision < 1:
        raise Blocked("CHECK_REVISION_INVALID")
    previous_body = request.get("previous_body_html")
    prior_findings = request.get("prior_findings") if isinstance(request.get("prior_findings"), list) else []
    batch_sha = str(request.get("batch_sha256") or "")
    if len(batch_sha) != 64:
        raise Blocked("CHECK_BATCH_SHA_MISSING")

    env = os.environ.copy()
    env["PYTHONDONTWRITEBYTECODE"] = "1"
    controller = str(S4 / "controller.py")
    with tempfile.TemporaryDirectory(prefix="concept-agent-s4-check-") as td:
        root = Path(td)
        workspace = root / "workspace"
        workspace.mkdir()
        state = _state_base(item, bound, batch_sha)
        state_path = workspace / "state.json"

        if revision == 1:
            state_path.write_text(json.dumps(state, ensure_ascii=False, indent=2, sort_keys=True), encoding="utf-8")
            draft = root / "draft.html"
            draft.write_text(body, encoding="utf-8")
            cp = _run([sys.executable, controller, "draft", str(workspace), str(draft)], env)
            if cp.returncode != 0:
                raise Blocked("SYSTEM4_DRAFT_REJECTED:" + (cp.stdout or cp.stderr)[-700:])
        else:
            if not isinstance(previous_body, str) or not previous_body.strip() or not prior_findings:
                raise Blocked("REPAIR_CONTEXT_MISSING")
            state["phase"] = "REPAIR_REQUIRED"
            state["revision"] = revision - 1
            state["draft_markdown"] = previous_body
            state["draft_sha256"] = sha_text(previous_body)
            state["checks"] = {
                "status": "FAIL",
                "mode": "FULL_PRODUCTION",
                "errors": ["CONCEPT_AGENT_PRIOR_REPAIR_REQUIRED"],
                "findings": prior_findings,
                "checker": "concept_agent_previous_fullcheck",
                "checked_draft_sha256": state["draft_sha256"],
            }
            state["last_error"] = "CONCEPT_AGENT_PRIOR_REPAIR_REQUIRED"
            controller_engine.verify_state(state)
            state_path.write_text(json.dumps(state, ensure_ascii=False, indent=2, sort_keys=True), encoding="utf-8")
            repair = root / "repair.html"
            repair.write_text(body, encoding="utf-8")
            cp = _run([sys.executable, controller, "repair", str(workspace), str(repair)], env)
            if cp.returncode != 0:
                raise Blocked("SYSTEM4_REPAIR_REJECTED:" + (cp.stdout or cp.stderr)[-700:])

        cp = _run([sys.executable, controller, "fullcheck", str(workspace)], env)
        current = json.loads(state_path.read_text(encoding="utf-8"))
        content_sha = sha_text(body)
        if cp.returncode == 0:
            if current.get("phase") != "OUTPUT_GATE_REQUIRED" or current.get("checks", {}).get("status") != "PASS":
                raise Blocked("SYSTEM4_FULLCHECK_PASS_STATE_INVALID")
            evidence = current["checks"].get("production_evidence") or {}
            return {
                "status": "PASS",
                "content_sha256": content_sha,
                "languagetool": ((evidence.get("evidence") or {}).get("languagetool") or {}),
                "ppm": ((evidence.get("evidence") or {}).get("ppm679") or {}),
                "system4_production_evidence": evidence,
                "publish_allowed": False,
            }, 0
        if cp.returncode == 3 and current.get("phase") == "REPAIR_REQUIRED":
            findings = current.get("checks", {}).get("findings")
            if not isinstance(findings, list) or not findings:
                raise Blocked("SYSTEM4_REPAIR_FINDINGS_MISSING")
            return {
                "status": "REPAIR_REQUIRED",
                "content_sha256": content_sha,
                "checker": current.get("checks", {}).get("checker") or "SYSTEM4_FULLCHECK",
                "findings": findings,
                "publish_allowed": False,
            }, 10
        raise Blocked("SYSTEM4_FULLCHECK_BLOCKED:" + (cp.stdout or cp.stderr)[-900:])


def main() -> int:
    try:
        request = json.loads(sys.stdin.read())
        if not isinstance(request, dict):
            raise Blocked("CHECK_REQUEST_OBJECT_REQUIRED")
        result, rc = check(request)
        print(json.dumps(result, ensure_ascii=False, sort_keys=True))
        return rc
    except Exception as exc:
        print("CONCEPT_AGENT_SYSTEM4_CHECKER_BLOCKED:" + str(exc), file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
