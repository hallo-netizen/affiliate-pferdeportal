#!/usr/bin/env python3
from __future__ import annotations

import argparse
import hashlib
import json
import tempfile
from pathlib import Path
from typing import Any

import binding_transport_gate
import entry_hardlock
import full_e2e_simulation
import resumable_runner
import runner

CONTRACT = "CONCEPT_AGENT_FIXED_BLOCK_ROUTE_V1"
RESTART = "RESTART_BATCH_FROM_INTAKE"
CONTINUE = "CONTINUE_CURRENT_BATCH"
HALT = "TERMINAL_SECURITY_BLOCK"


def stable(value: Any) -> str:
    return hashlib.sha256(json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode("utf-8")).hexdigest()


def route_from_decision(decision: dict[str, Any]) -> dict[str, Any]:
    if not isinstance(decision, dict):
        raise RuntimeError("DECISION_OBJECT_REQUIRED")
    status = decision.get("status")
    reason = str(decision.get("reason") or "")
    if status == "READY":
        action = CONTINUE
        next_stage = str(decision.get("next_stage") or "ARTICLE_PRODUCTION")
        terminal = False
    elif status == "BLOCKED" and reason == "EXACT_CROSS_CHAT_TRANSPORT_MISSING":
        action = RESTART
        next_stage = "INTAKE"
        terminal = False
    elif status == "BLOCKED":
        action = HALT
        next_stage = "NONE"
        terminal = True
    else:
        raise RuntimeError("DECISION_STATUS_INVALID")
    out = {
        "contract": CONTRACT,
        "status": "PASS",
        "source_status": status,
        "source_reason": reason or None,
        "required_action": action,
        "next_stage": next_stage,
        "terminal": terminal,
        "chat_may_choose_action": False,
        "reconstruction_allowed": False,
        "publish_allowed": False,
    }
    out["route_sha256"] = stable(out)
    return out


def route_from_exception(exc: Exception) -> dict[str, Any]:
    return route_from_decision({"status": "BLOCKED", "reason": str(exc)})


def _fixture(root: Path, count: int) -> tuple[Path, Path, Path]:
    base_pointer, binding_raw = binding_transport_gate.fixture(count)
    binding = json.loads(binding_raw.decode("utf-8"))
    transport = root / base_pointer["cross_chat_transport_filename"]
    transport.write_bytes(binding_raw)

    pointer = {
        **base_pointer,
        "intake_sha256": hashlib.sha256(("intake-"+str(count)).encode()).hexdigest(),
        "research_binding_sha256": hashlib.sha256(("research-"+str(count)).encode()).hexdigest(),
        "authoring_bindings_file_sha256": hashlib.sha256(("authoring-"+str(count)).encode()).hexdigest(),
        "article_bodies_present": False,
        "next_article_index": 0,
    }
    current = {
        "concept_agent_current_batch": {
            "workflow": entry_hardlock.WORKFLOW,
            "batch_sha256": binding["batch_sha256"],
            "item_count": count,
            "intake_status": "PASS",
            "research_binding_status": "PASS",
            "authoring_binding_status": "PASS",
            "article_bodies_completed": 0,
            "next_article_index": 0,
            "cross_chat_transport_filename": transport.name,
            "cross_chat_transport_sha256": pointer["cross_chat_transport_sha256"],
            "publish_allowed": False,
        }
    }
    pp = root / "pointer.json"
    cp = root / "current.json"
    pp.write_text(json.dumps(pointer, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    cp.write_text(json.dumps(current, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return pp, cp, transport


def _run_article_pipeline(root: Path, count: int) -> dict[str, Any]:
    binding = runner.simulation_binding(count)
    raw = runner.canon(binding)
    raw_sha = hashlib.sha256(raw).hexdigest()
    result = resumable_runner.execute_resumable(
        binding,
        raw_sha,
        root / "article-pipeline",
        "simulation",
        force_repair_index=1 if count > 1 else None,
    )
    state = result["state"]
    if state.get("status") != "PASS" or state.get("phase") != "COMPLETE":
        raise RuntimeError("ARTICLE_PIPELINE_NOT_COMPLETE")
    if len(state.get("completed_articles") or []) != count:
        raise RuntimeError("ARTICLE_PIPELINE_COUNT_MISMATCH")
    return {
        "status": "PASS",
        "count": count,
        "revisions": [x["revision_count"] for x in state["completed_articles"]],
    }


def positive_existing_transport(repo: Path, out: Path, count: int) -> dict[str, Any]:
    with tempfile.TemporaryDirectory(prefix=f"ca-fixed-positive-{count}-") as td:
        root = Path(td)
        pp, cp, tp = _fixture(root, count)
        decision = entry_hardlock.probe(pp, cp, tp)
        route = route_from_decision(decision)
        if route["required_action"] != CONTINUE or route["next_stage"] != "ARTICLE_PRODUCTION":
            raise RuntimeError("POSITIVE_ROUTE_NOT_CONTINUE")
        articles = _run_article_pipeline(root, count)
        final = full_e2e_simulation.run_positive(repo, out, count)
        return {"count": count, "route": route, "articles": articles, "final": final}


def positive_missing_transport_restart(repo: Path, out: Path, count: int) -> dict[str, Any]:
    with tempfile.TemporaryDirectory(prefix=f"ca-fixed-restart-{count}-") as td:
        root = Path(td)
        pp, cp, _ = _fixture(root, count)
        decision = entry_hardlock.probe(pp, cp, None)
        route = route_from_decision(decision)
        if route["required_action"] != RESTART or route["next_stage"] != "INTAKE":
            raise RuntimeError("MISSING_TRANSPORT_NOT_FIXED_RESTART")
        # Same production modules, but a fresh batch is created from stage 0.
        articles = _run_article_pipeline(root / "fresh-batch", count)
        final = full_e2e_simulation.run_positive(repo, out, count)
        return {"count": count, "route": route, "fresh_batch_articles": articles, "final": final}


def negative_tamper(count: int) -> dict[str, Any]:
    with tempfile.TemporaryDirectory(prefix=f"ca-fixed-negative-{count}-") as td:
        root = Path(td)
        pp, cp, tp = _fixture(root, count)
        tp.write_bytes(tp.read_bytes() + b"X")
        try:
            entry_hardlock.probe(pp, cp, tp)
        except Exception as exc:
            route = route_from_exception(exc)
        else:
            raise RuntimeError("TAMPER_NOT_BLOCKED")
        if route["required_action"] != HALT or not route["terminal"]:
            raise RuntimeError("TAMPER_NOT_TERMINAL")
        return {"count": count, "case": "transport-tamper", "route": route}


def run(repo: Path, out: Path) -> dict[str, Any]:
    out.mkdir(parents=True, exist_ok=True)
    proof = {
        "contract": "CONCEPT_AGENT_FIXED_BLOCK_ROUTE_ACCEPTANCE_V1",
        "status": "PASS",
        "scope": "SAME_MODULES_AS_PRODUCTION_CONTROL",
        "positive_existing_transport": [
            positive_existing_transport(repo, out / "existing-1", 1),
            positive_existing_transport(repo, out / "existing-3", 3),
        ],
        "positive_missing_transport_restart": [
            positive_missing_transport_restart(repo, out / "restart-1", 1),
            positive_missing_transport_restart(repo, out / "restart-3", 3),
        ],
        "negative": [negative_tamper(1), negative_tamper(3)],
        "rules": {
            "missing_transport": RESTART,
            "tamper_or_mismatch": HALT,
            "chat_may_choose_action": False,
            "reconstruction_allowed": False,
            "exactly_one_final_file": True,
        },
        "publish_allowed": False,
    }
    proof["proof_sha256"] = stable(proof)
    (out / "CONCEPT_AGENT_FIXED_BLOCK_ROUTE_ACCEPTANCE_V1.json").write_text(
        json.dumps(proof, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    return proof


def main() -> int:
    ap = argparse.ArgumentParser()
    sub = ap.add_subparsers(dest="cmd", required=True)
    a = sub.add_parser("acceptance")
    a.add_argument("--repo", required=True)
    a.add_argument("--out", required=True)
    r = sub.add_parser("route")
    r.add_argument("--decision", required=True)
    r.add_argument("--out", required=True)
    args = ap.parse_args()
    try:
        if args.cmd == "route":
            decision = json.loads(Path(args.decision).read_text(encoding="utf-8"))
            result = route_from_decision(decision)
            out = Path(args.out)
            out.parent.mkdir(parents=True, exist_ok=True)
            out.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
            print(json.dumps(result, sort_keys=True))
            return 0
        proof = run(Path(args.repo).resolve(), Path(args.out).resolve())
        print(json.dumps({
            "ok": True,
            "status": proof["status"],
            "positive_counts": [1, 3],
            "restart_counts": [1, 3],
            "negative_counts": [1, 3],
            "proof_sha256": proof["proof_sha256"],
        }, sort_keys=True))
        return 0
    except Exception as exc:
        print("CONCEPT_AGENT_FIXED_BLOCK_ROUTE_ACCEPTANCE_BLOCKED:" + str(exc), file=__import__("sys").stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
