#!/usr/bin/env python3
from __future__ import annotations

import argparse
import base64
import hashlib
import json
import os
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path
from typing import Any

import runner

STATE_VERSION = "1.0.0"
STATE_CONTRACT = "CONCEPT_AGENT_DURABLE_RUN_STATE_V1"
ENTRY_PROOF_CONTRACT = "CONCEPT_AGENT_REENTRY_PROOF_V1"
STATE_PATH_DEFAULT = "concept_agent/runtime/CURRENT_STATE.json"
ALLOWED_PHASES = {"READY", "DRAFTED", "REPAIR_REQUIRED", "COMPLETE"}


def _stable_without_hash(value: dict[str, Any], field: str) -> str:
    copy = dict(value)
    copy.pop(field, None)
    return runner.stable(copy)


def _seal_state(state: dict[str, Any]) -> dict[str, Any]:
    state = dict(state)
    state["state_sha256"] = _stable_without_hash(state, "state_sha256")
    return state


def _seal_proof(proof: dict[str, Any]) -> dict[str, Any]:
    proof = dict(proof)
    proof["proof_sha256"] = _stable_without_hash(proof, "proof_sha256")
    return proof


def _article_valid(article: dict[str, Any], item: dict[str, Any]) -> None:
    idx = item["item_index"]
    if article.get("item_index") != idx:
        raise runner.Blocked(f"STATE_ARTICLE_INDEX_MISMATCH:{idx}")
    if article.get("plan_slot") != item["plan_slot"]:
        raise runner.Blocked(f"STATE_ARTICLE_SLOT_MISMATCH:{idx}")
    if article.get("bound_work_sha256") != item["opaque_bound_work_sha256"]:
        raise runner.Blocked(f"STATE_ARTICLE_BOUND_WORK_MISMATCH:{idx}")
    body = article.get("body_html")
    body_sha = article.get("body_sha256")
    if not isinstance(body, str) or not body.strip():
        raise runner.Blocked(f"STATE_ARTICLE_BODY_EMPTY:{idx}")
    if body_sha != runner.sha_bytes(body.encode("utf-8")):
        raise runner.Blocked(f"STATE_ARTICLE_BODY_HASH_MISMATCH:{idx}")
    checks = article.get("checks")
    if not isinstance(checks, dict) or checks.get("status") != "PASS":
        raise runner.Blocked(f"STATE_ARTICLE_CHECK_NOT_PASS:{idx}")
    if checks.get("content_sha256") != body_sha:
        raise runner.Blocked(f"STATE_ARTICLE_CHECK_HASH_MISMATCH:{idx}")
    revision = article.get("revision_count")
    if not isinstance(revision, int) or revision < 1 or revision > 6:
        raise runner.Blocked(f"STATE_ARTICLE_REVISION_INVALID:{idx}")


def initial_state(run: dict[str, Any], binding_file_sha256: str) -> dict[str, Any]:
    return _seal_state({
        "contract": STATE_CONTRACT,
        "state_version": STATE_VERSION,
        "status": "IN_PROGRESS",
        "phase": "READY",
        "batch_sha256": run["batch_sha256"],
        "binding_file_sha256": binding_file_sha256,
        "item_count": run["item_count"],
        "next_item_index": 0,
        "completed_articles": [],
        "current": None,
        "event_log": [],
        "publish_allowed": False,
    })


def validate_state(state: dict[str, Any], run: dict[str, Any], binding_file_sha256: str) -> dict[str, Any]:
    if not isinstance(state, dict):
        raise runner.Blocked("STATE_OBJECT_REQUIRED")
    if state.get("contract") != STATE_CONTRACT:
        raise runner.Blocked("STATE_CONTRACT_INVALID")
    if state.get("state_version") != STATE_VERSION:
        raise runner.Blocked("STATE_VERSION_INVALID")
    if state.get("publish_allowed") is not False:
        raise runner.Blocked("STATE_PUBLISH_MUST_BE_FALSE")
    declared = state.get("state_sha256")
    if not isinstance(declared, str) or declared != _stable_without_hash(state, "state_sha256"):
        raise runner.Blocked("STATE_HASH_MISMATCH")
    if state.get("batch_sha256") != run["batch_sha256"]:
        raise runner.Blocked("STATE_BATCH_MISMATCH")
    if state.get("binding_file_sha256") != binding_file_sha256:
        raise runner.Blocked("STATE_BINDING_MISMATCH")
    if state.get("item_count") != run["item_count"]:
        raise runner.Blocked("STATE_ITEM_COUNT_MISMATCH")
    phase = state.get("phase")
    if phase not in ALLOWED_PHASES:
        raise runner.Blocked("STATE_PHASE_INVALID")
    completed = state.get("completed_articles")
    if not isinstance(completed, list):
        raise runner.Blocked("STATE_COMPLETED_LIST_REQUIRED")
    if len(completed) > run["item_count"]:
        raise runner.Blocked("STATE_COMPLETED_TOO_MANY")
    for idx, article in enumerate(completed):
        if not isinstance(article, dict):
            raise runner.Blocked(f"STATE_ARTICLE_OBJECT_REQUIRED:{idx}")
        _article_valid(article, run["items"][idx])
    next_idx = state.get("next_item_index")
    if not isinstance(next_idx, int):
        raise runner.Blocked("STATE_NEXT_INDEX_INVALID")
    if next_idx != len(completed):
        raise runner.Blocked("STATE_SEQUENCE_GAP")
    current = state.get("current")
    if phase == "COMPLETE":
        if next_idx != run["item_count"] or current is not None:
            raise runner.Blocked("STATE_COMPLETE_SHAPE_INVALID")
        if state.get("status") != "PASS":
            raise runner.Blocked("STATE_COMPLETE_STATUS_INVALID")
    else:
        if next_idx >= run["item_count"]:
            raise runner.Blocked("STATE_INCOMPLETE_INDEX_INVALID")
        if state.get("status") != "IN_PROGRESS":
            raise runner.Blocked("STATE_IN_PROGRESS_STATUS_INVALID")
        item = run["items"][next_idx]
        if phase == "READY":
            if current is not None:
                raise runner.Blocked("STATE_READY_CURRENT_MUST_BE_EMPTY")
        else:
            if not isinstance(current, dict):
                raise runner.Blocked("STATE_CURRENT_REQUIRED")
            if current.get("item_index") != next_idx or current.get("plan_slot") != item["plan_slot"]:
                raise runner.Blocked("STATE_CURRENT_IDENTITY_MISMATCH")
            if current.get("bound_work_sha256") != item["opaque_bound_work_sha256"]:
                raise runner.Blocked("STATE_CURRENT_BOUND_WORK_MISMATCH")
            body = current.get("body_html")
            if not isinstance(body, str) or not body.strip():
                raise runner.Blocked("STATE_CURRENT_BODY_EMPTY")
            if current.get("body_sha256") != runner.sha_bytes(body.encode("utf-8")):
                raise runner.Blocked("STATE_CURRENT_BODY_HASH_MISMATCH")
            revision = current.get("revision")
            if not isinstance(revision, int) or revision < 1 or revision > 6:
                raise runner.Blocked("STATE_CURRENT_REVISION_INVALID")
            findings = current.get("findings")
            if phase == "REPAIR_REQUIRED":
                if not isinstance(findings, list) or not findings:
                    raise runner.Blocked("STATE_REPAIR_FINDINGS_REQUIRED")
            elif findings not in ([], None):
                raise runner.Blocked("STATE_DRAFTED_FINDINGS_FORBIDDEN")
    return state


def entry_proof(state: dict[str, Any], run: dict[str, Any], resumed: bool) -> dict[str, Any]:
    completed = state["completed_articles"]
    proof = {
        "contract": ENTRY_PROOF_CONTRACT,
        "status": "PASS",
        "entry_mode": "RESUME" if resumed else "NEW",
        "batch_sha256": run["batch_sha256"],
        "state_sha256": state["state_sha256"],
        "validated_completed_count": len(completed),
        "validated_completed_indices": list(range(len(completed))),
        "current_phase": state["phase"],
        "next_item_index": state["next_item_index"],
        "fast_forward_only": True,
        "workflow_control_authority": "RUNNER_ONLY",
        "chat_execution_authority": "NONE",
        "publish_allowed": False,
    }
    return _seal_proof(proof)


def _github_request(method: str, url: str, token: str, payload: dict[str, Any] | None = None) -> Any:
    data = None if payload is None else json.dumps(payload, ensure_ascii=False).encode("utf-8")
    headers = {
        "Authorization": "Bearer " + token,
        "Accept": "application/vnd.github+json",
        "X-GitHub-Api-Version": "2022-11-28",
    }
    if data is not None:
        headers["Content-Type"] = "application/json"
    req = urllib.request.Request(url, data=data, headers=headers, method=method)
    try:
        with urllib.request.urlopen(req, timeout=30) as response:
            raw = response.read()
            return json.loads(raw) if raw else {}
    except urllib.error.HTTPError as exc:
        if exc.code == 404 and method == "GET":
            return None
        detail = exc.read().decode("utf-8", "replace")[-300:]
        raise runner.Blocked(f"STATE_GITHUB_HTTP_ERROR:{exc.code}:{detail}") from exc
    except Exception as exc:
        raise runner.Blocked("STATE_GITHUB_CALL_FAILED") from exc


def persist_github_state(state: dict[str, Any]) -> None:
    if os.getenv("CONCEPT_AGENT_PERSIST_GITHUB_STATE", "").strip() != "1":
        return
    token = os.getenv("GITHUB_TOKEN", "").strip()
    repo = os.getenv("GITHUB_REPOSITORY", "").strip()
    branch = os.getenv("CONCEPT_AGENT_STATE_BRANCH", "concept-agent/production-control").strip()
    path = os.getenv("CONCEPT_AGENT_STATE_PATH", STATE_PATH_DEFAULT).strip()
    if not token or not repo or not branch or not path:
        raise runner.Blocked("STATE_GITHUB_CONFIG_MISSING")
    quoted = "/".join(urllib.parse.quote(x, safe="") for x in path.split("/"))
    url = f"https://api.github.com/repos/{repo}/contents/{quoted}"
    existing = _github_request("GET", url + "?ref=" + urllib.parse.quote(branch, safe=""), token)
    payload: dict[str, Any] = {
        "message": f"Concept Agent runtime state: {state['phase']} item {state['next_item_index']}",
        "content": base64.b64encode((json.dumps(state, ensure_ascii=False, indent=2) + "\n").encode("utf-8")).decode("ascii"),
        "branch": branch,
    }
    if isinstance(existing, dict) and isinstance(existing.get("sha"), str):
        payload["sha"] = existing["sha"]
    _github_request("PUT", url, token, payload)


def checkpoint(state: dict[str, Any], outdir: Path) -> dict[str, Any]:
    state = _seal_state(state)
    runner.write_json(outdir / "CURRENT_STATE.json", state)
    persist_github_state(state)
    return state


def _handoff_from_state(state: dict[str, Any], outdir: Path, mode: str) -> dict[str, Any]:
    handoff = {
        "contract": runner.HANDOFF_CONTRACT,
        "runner_version": runner.RUNNER_VERSION + "+durable-state",
        "mode": mode,
        "status": "PASS",
        "batch_sha256": state["batch_sha256"],
        "item_count": state["item_count"],
        "publish_allowed": False,
        "articles": state["completed_articles"],
        "event_log": state["event_log"],
        "durable_state_sha256": state["state_sha256"],
    }
    handoff["handoff_sha256"] = runner.stable(handoff)
    runner.write_json(outdir / "CONCEPT_AGENT_CHAT_HANDOFF_V1.json", handoff)
    return handoff


def execute_resumable(
    binding: dict[str, Any],
    binding_file_sha256: str,
    outdir: Path,
    mode: str,
    resume_state: dict[str, Any] | None = None,
    force_repair_index: int | None = None,
    stop_phase: str | None = None,
    stop_item_index: int | None = None,
) -> dict[str, Any]:
    run = runner.normalize_binding(binding)
    outdir.mkdir(parents=True, exist_ok=True)
    if mode == "production":
        raise runner.Blocked("DIRECT_MODEL_API_ROUTE_REMOVED_USE_EXISTING_107007")

    resumed = resume_state is not None
    state = validate_state(resume_state, run, binding_file_sha256) if resumed else initial_state(run, binding_file_sha256)
    proof = entry_proof(state, run, resumed)
    runner.write_json(outdir / "CONCEPT_AGENT_ENTRY_PROOF.json", proof)

    def maybe_stop() -> bool:
        return stop_phase == state["phase"] and (stop_item_index is None or stop_item_index == state["next_item_index"])

    if state["phase"] == "COMPLETE":
        return {"state": state, "handoff": _handoff_from_state(state, outdir, mode), "entry_proof": proof}

    while state["phase"] != "COMPLETE":
        idx = state["next_item_index"]
        item = run["items"][idx]

        if state["phase"] == "READY":
            state["event_log"].append({"event": "ITEM_START", "item_index": idx, "plan_slot": item["plan_slot"]})
            if mode == "simulation":
                writer = runner._sim_writer(item, 1, [])
            else:
                writer = runner._model_call(item, 1, None, [])
            body = writer.get("body_html")
            if writer.get("item_index") != idx or writer.get("plan_slot") != item["plan_slot"]:
                raise runner.Blocked(f"WRITER_IDENTITY_MISMATCH:{idx}")
            if writer.get("used_bound_work_sha256") != item["opaque_bound_work_sha256"]:
                raise runner.Blocked(f"WRITER_BOUND_WORK_MISMATCH:{idx}")
            if not isinstance(body, str) or not body.strip():
                raise runner.Blocked(f"WRITER_BODY_EMPTY:{idx}")
            body_sha = runner.sha_bytes(body.encode("utf-8"))
            state["current"] = {
                "item_index": idx,
                "plan_slot": item["plan_slot"],
                "bound_work_sha256": item["opaque_bound_work_sha256"],
                "revision": 1,
                "body_html": body,
                "body_sha256": body_sha,
                "findings": [],
                "previous_body_html": None,
                "prior_findings": [],
            }
            state["phase"] = "DRAFTED"
            state["event_log"].append({"event": "DRAFT", "item_index": idx, "revision": 1, "body_sha256": body_sha})
            state = checkpoint(state, outdir)
            if maybe_stop():
                return {"state": state, "handoff": None, "entry_proof": proof}
            continue

        if state["phase"] == "REPAIR_REQUIRED":
            cur = state["current"]
            revision = int(cur["revision"]) + 1
            if revision > 6:
                raise runner.Blocked(f"REPAIR_LIMIT_EXCEEDED:{idx}")
            findings = cur["findings"]
            if mode == "simulation":
                writer = runner._sim_writer(item, revision, findings)
            else:
                writer = runner._model_call(item, revision, cur["body_html"], findings)
            body = writer.get("body_html")
            if writer.get("item_index") != idx or writer.get("plan_slot") != item["plan_slot"]:
                raise runner.Blocked(f"WRITER_IDENTITY_MISMATCH:{idx}")
            if writer.get("used_bound_work_sha256") != item["opaque_bound_work_sha256"]:
                raise runner.Blocked(f"WRITER_BOUND_WORK_MISMATCH:{idx}")
            if not isinstance(body, str) or not body.strip():
                raise runner.Blocked(f"WRITER_BODY_EMPTY:{idx}")
            body_sha = runner.sha_bytes(body.encode("utf-8"))
            state["current"] = {
                "item_index": idx,
                "plan_slot": item["plan_slot"],
                "bound_work_sha256": item["opaque_bound_work_sha256"],
                "revision": revision,
                "body_html": body,
                "body_sha256": body_sha,
                "findings": [],
                "previous_body_html": cur["body_html"],
                "prior_findings": findings,
            }
            state["phase"] = "DRAFTED"
            state["event_log"].append({"event": "DRAFT", "item_index": idx, "revision": revision, "body_sha256": body_sha})
            state = checkpoint(state, outdir)
            if maybe_stop():
                return {"state": state, "handoff": None, "entry_proof": proof}
            continue

        if state["phase"] != "DRAFTED":
            raise runner.Blocked("STATE_PHASE_UNREACHABLE")
        cur = state["current"]
        body = cur["body_html"]
        revision = int(cur["revision"])
        if mode == "simulation":
            result = runner._sim_check(item, body, revision, force_repair_index == idx)
        else:
            checker_cmd = os.getenv("CONCEPT_AGENT_CHECKER_CMD", "").strip()
            result = runner._external_check(
                checker_cmd,
                item,
                body,
                revision,
                batch_sha256=run["batch_sha256"],
                previous_body_html=cur.get("previous_body_html"),
                prior_findings=cur.get("prior_findings") if isinstance(cur.get("prior_findings"), list) else [],
            )
        state["event_log"].append({
            "event": "CHECK",
            "item_index": idx,
            "revision": revision,
            "status": result["status"],
            "content_sha256": result["content_sha256"],
        })
        if result["status"] == "REPAIR_REQUIRED":
            findings = result.get("findings") if isinstance(result.get("findings"), list) else []
            if not findings:
                raise runner.Blocked(f"REPAIR_FINDINGS_MISSING:{idx}")
            cur["findings"] = findings
            state["phase"] = "REPAIR_REQUIRED"
            state = checkpoint(state, outdir)
            if maybe_stop():
                return {"state": state, "handoff": None, "entry_proof": proof}
            continue
        if result["status"] != "PASS":
            raise runner.Blocked(f"CHECK_NOT_PASS:{idx}")
        if result["content_sha256"] != cur["body_sha256"]:
            raise runner.Blocked(f"PASS_HASH_MISMATCH:{idx}")
        article = {
            "item_index": idx,
            "plan_slot": item["plan_slot"],
            "title": item["title"],
            "target_keyword": item["target_keyword"],
            "category": item["category"],
            "article_type": item["article_type"],
            "revision_count": revision,
            "body_html": body,
            "body_sha256": cur["body_sha256"],
            "checks": result,
            "bound_work_sha256": item["opaque_bound_work_sha256"],
        }
        state["completed_articles"].append(article)
        state["event_log"].append({"event": "ITEM_PASS", "item_index": idx, "revision": revision, "body_sha256": cur["body_sha256"]})
        state["next_item_index"] = idx + 1
        state["current"] = None
        if state["next_item_index"] == run["item_count"]:
            state["phase"] = "COMPLETE"
            state["status"] = "PASS"
        else:
            state["phase"] = "READY"
        state = checkpoint(state, outdir)
        if maybe_stop():
            return {"state": state, "handoff": None, "entry_proof": proof}

    return {"state": state, "handoff": _handoff_from_state(state, outdir, mode), "entry_proof": proof}


def simulation_middle_positive(outdir: Path) -> dict[str, Any]:
    binding = runner.simulation_binding(3)
    raw_sha = hashlib.sha256(runner.canon(binding)).hexdigest()

    first = execute_resumable(binding, raw_sha, outdir / "after-one", "simulation", stop_phase="READY", stop_item_index=1)
    state1 = first["state"]
    resumed1 = execute_resumable(binding, raw_sha, outdir / "resume-after-one", "simulation", resume_state=state1)
    if resumed1["entry_proof"]["entry_mode"] != "RESUME" or resumed1["entry_proof"]["validated_completed_count"] != 1:
        raise runner.Blocked("MID_ENTRY_AFTER_ONE_NOT_PROVEN")

    repair_stop = execute_resumable(
        binding, raw_sha, outdir / "repair-stop", "simulation",
        force_repair_index=1, stop_phase="REPAIR_REQUIRED", stop_item_index=1
    )
    state2 = repair_stop["state"]
    resumed2 = execute_resumable(
        binding, raw_sha, outdir / "resume-repair", "simulation",
        resume_state=state2, force_repair_index=1
    )
    revisions = [x["revision_count"] for x in resumed2["state"]["completed_articles"]]
    if revisions != [1, 2, 1]:
        raise runner.Blocked("MID_ENTRY_REPAIR_SEQUENCE_NOT_PROVEN")
    return {
        "contract": "CONCEPT_AGENT_MID_ENTRY_POSITIVE_PROOF_V1",
        "status": "PASS",
        "after_article_entry": resumed1["entry_proof"],
        "mid_repair_entry": resumed2["entry_proof"],
        "revisions": revisions,
        "publish_allowed": False,
    }


def simulation_middle_negative(outdir: Path) -> dict[str, Any]:
    binding = runner.simulation_binding(3)
    raw_sha = hashlib.sha256(runner.canon(binding)).hexdigest()
    base = execute_resumable(binding, raw_sha, outdir / "base", "simulation", stop_phase="READY", stop_item_index=1)["state"]
    cases = []

    def expect(name: str, mutate) -> None:
        bad = json.loads(json.dumps(base))
        mutate(bad)
        bad = _seal_state(bad)
        try:
            execute_resumable(binding, raw_sha, outdir / name, "simulation", resume_state=bad)
        except runner.Blocked as exc:
            cases.append({"case": name, "blocked": True, "reason": str(exc)})
        else:
            raise runner.Blocked("MID_ENTRY_NEGATIVE_NOT_BLOCKED:" + name)

    expect("skip-forward", lambda s: s.__setitem__("next_item_index", 2))
    expect("rewind", lambda s: s.__setitem__("next_item_index", 0))

    def body_tamper(s):
        s["completed_articles"][0]["body_html"] += " manipuliert"
    expect("completed-body-tamper", body_tamper)

    def wrong_phase(s):
        s["phase"] = "REPAIR_REQUIRED"
        s["current"] = {
            "item_index": 1,
            "plan_slot": binding["items"][1]["plan_slot"],
            "bound_work_sha256": runner.stable(binding["items"][1]),
            "revision": 1,
            "body_html": "<p>fake</p>",
            "body_sha256": runner.sha_bytes(b"<p>fake</p>"),
            "findings": [],
        }
    expect("fake-repair-entry", wrong_phase)

    proof = {
        "contract": "CONCEPT_AGENT_MID_ENTRY_NEGATIVE_PROOF_V1",
        "status": "PASS",
        "cases": cases,
        "publish_allowed": False,
    }
    proof["proof_sha256"] = runner.stable(proof)
    runner.write_json(outdir / "CONCEPT_AGENT_MID_ENTRY_NEGATIVE_PROOF.json", proof)
    return proof


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser()
    sub = parser.add_subparsers(dest="command", required=True)

    for name in ("simulate-mid-positive", "simulate-mid-negative"):
        p = sub.add_parser(name)
        p.add_argument("--out", required=True)

    runp = sub.add_parser("run")
    runp.add_argument("--binding", required=True)
    runp.add_argument("--binding-sha256", required=True)
    runp.add_argument("--state")
    runp.add_argument("--out", required=True)
    args = parser.parse_args(argv)
    try:
        if args.command == "simulate-mid-positive":
            proof = simulation_middle_positive(Path(args.out))
            runner.write_json(Path(args.out) / "CONCEPT_AGENT_MID_ENTRY_POSITIVE_PROOF.json", proof)
            print(json.dumps({"ok": True, "status": "CONCEPT_AGENT_MID_ENTRY_POSITIVE_PASS"}, sort_keys=True))
            return 0
        if args.command == "simulate-mid-negative":
            simulation_middle_negative(Path(args.out))
            print(json.dumps({"ok": True, "status": "CONCEPT_AGENT_MID_ENTRY_NEGATIVE_PASS"}, sort_keys=True))
            return 0

        path = Path(args.binding)
        raw = path.read_bytes()
        if runner.sha_bytes(raw) != args.binding_sha256:
            raise runner.Blocked("BINDING_SHA_MISMATCH")
        binding = runner.read_json(path)
        runner.normalize_binding(binding, args.binding_sha256, runner.sha_bytes(raw))
        state = runner.read_json(Path(args.state)) if args.state and Path(args.state).is_file() else None
        result = execute_resumable(binding, args.binding_sha256, Path(args.out), "production", resume_state=state)
        if result["handoff"] is None:
            raise runner.Blocked("PRODUCTION_DID_NOT_COMPLETE")
        print(json.dumps({
            "ok": True,
            "status": "CONCEPT_AGENT_PRODUCTION_PASS",
            "handoff_sha256": result["handoff"]["handoff_sha256"],
            "durable_state_sha256": result["state"]["state_sha256"],
        }, sort_keys=True))
        return 0
    except runner.Blocked as exc:
        out = Path(getattr(args, "out", "."))
        blocked = {
            "contract": runner.BLOCK_CONTRACT,
            "status": "BLOCKED",
            "reason": str(exc),
            "publish_allowed": False,
        }
        blocked["blocked_sha256"] = runner.stable(blocked)
        runner.write_json(out / "CONCEPT_AGENT_BLOCKED.json", blocked)
        print("CONCEPT_AGENT_RESUMABLE_BLOCKED:" + str(exc), file=os.sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
