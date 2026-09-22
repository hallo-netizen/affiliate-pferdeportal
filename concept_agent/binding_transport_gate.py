#!/usr/bin/env python3
from __future__ import annotations

import argparse
import base64
import hashlib
import json
import re
import sys
from pathlib import Path
from typing import Any

POINTER_CONTRACT = "PFERDE_ATELIER_CONCEPT_AGENT_WORK_BINDING_POINTER_V1"
WORKFLOW = "PFERDE_ATELIER_KONZEPT_5_CONCEPT_AGENT"
RECEIPT_CONTRACT = "CONCEPT_AGENT_DURABLE_BINDING_RECEIPT_V1"
SHA_RE = re.compile(r"^[0-9a-f]{64}$")


class Blocked(RuntimeError):
    pass


def sha(raw: bytes) -> str:
    return hashlib.sha256(raw).hexdigest()


def stable(value: Any) -> str:
    return sha(json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode("utf-8"))


def load(path: Path) -> dict[str, Any]:
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except Exception as exc:
        raise Blocked("JSON_INVALID:" + str(path)) from exc
    if not isinstance(value, dict):
        raise Blocked("JSON_OBJECT_REQUIRED:" + str(path))
    return value


def validate_pointer(pointer: dict[str, Any]) -> None:
    if pointer.get("contract") != POINTER_CONTRACT:
        raise Blocked("POINTER_CONTRACT_INVALID")
    if pointer.get("workflow") != WORKFLOW:
        raise Blocked("WORKFLOW_INVALID")
    if pointer.get("cross_chat_transport_required") is not True:
        raise Blocked("TRANSPORT_NOT_REQUIRED")
    if pointer.get("publish_allowed") is not False:
        raise Blocked("POINTER_PUBLISH_INVALID")
    for key in ("batch_sha256", "cross_chat_transport_sha256", "cross_chat_transport_binding_sha256"):
        if not SHA_RE.fullmatch(str(pointer.get(key) or "")):
            raise Blocked("POINTER_HASH_INVALID:" + key)


def accept(pointer_path: Path, candidate_path: Path, durable_path: Path, receipt_path: Path) -> dict[str, Any]:
    pointer = load(pointer_path)
    validate_pointer(pointer)
    if not candidate_path.is_file():
        raise Blocked("CANDIDATE_MISSING")

    raw = candidate_path.read_bytes()
    actual = sha(raw)
    expected = pointer["cross_chat_transport_sha256"]
    if actual != expected:
        raise Blocked("TRANSPORT_SHA_MISMATCH")

    try:
        value = json.loads(raw.decode("utf-8"))
    except Exception as exc:
        raise Blocked("TRANSPORT_JSON_INVALID") from exc
    if not isinstance(value, dict):
        raise Blocked("TRANSPORT_OBJECT_REQUIRED")
    if value.get("binding_sha256") != pointer["cross_chat_transport_binding_sha256"]:
        raise Blocked("TRANSPORT_BINDING_SHA_MISMATCH")
    if value.get("batch_sha256") != pointer["batch_sha256"]:
        raise Blocked("TRANSPORT_BATCH_MISMATCH")
    if value.get("item_count") != pointer.get("item_count"):
        raise Blocked("TRANSPORT_ITEM_COUNT_MISMATCH")
    if value.get("publish_allowed") is not False:
        raise Blocked("TRANSPORT_PUBLISH_INVALID")

    durable_path.parent.mkdir(parents=True, exist_ok=True)
    durable_path.write_bytes(raw)
    if durable_path.read_bytes() != raw or sha(durable_path.read_bytes()) != expected:
        raise Blocked("DURABLE_BYTE_COPY_MISMATCH")

    receipt = {
        "contract": RECEIPT_CONTRACT,
        "status": "PASS",
        "workflow": WORKFLOW,
        "batch_sha256": pointer["batch_sha256"],
        "item_count": pointer["item_count"],
        "durable_ref": str(durable_path),
        "transport_sha256": actual,
        "transport_binding_sha256": value["binding_sha256"],
        "exact_bytes_preserved": True,
        "reconstruction_performed": False,
        "publish_allowed": False,
    }
    receipt["receipt_sha256"] = stable(receipt)
    receipt_path.parent.mkdir(parents=True, exist_ok=True)
    receipt_path.write_text(json.dumps(receipt, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return receipt


def fixture(count: int = 16) -> tuple[dict[str, Any], bytes]:
    items = []
    for i in range(count):
        items.append({
            "item_index": i,
            "plan_slot": hashlib.sha256(f"persist-slot-{i}".encode()).hexdigest(),
            "title": f"Persistenz-Testartikel {i+1}",
            "target_keyword": f"Persistenz Test {i+1}",
            "category": "test",
            "article_type": "Beratung",
            "research_binding": {"status": "BOUND"},
            "authoring_binding": {"status": "BOUND"},
        })
    core = {
        "contract": "CONCEPT_AGENT_WORK_BINDING_TEST_V1",
        "batch_sha256": hashlib.sha256(b"persist-16-batch").hexdigest(),
        "item_count": count,
        "items": items,
        "publish_allowed": False,
    }
    binding_sha = stable(core)
    value = {**core, "binding_sha256": binding_sha}
    raw = (json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":")) + "\n").encode("utf-8")
    pointer = {
        "contract": POINTER_CONTRACT,
        "workflow": WORKFLOW,
        "batch_sha256": core["batch_sha256"],
        "item_count": count,
        "cross_chat_transport_filename": "CONCEPT_AGENT_CURRENT_WORK_BINDING.json",
        "cross_chat_transport_sha256": sha(raw),
        "cross_chat_transport_binding_sha256": binding_sha,
        "cross_chat_transport_required": True,
        "publish_allowed": False,
    }
    return pointer, raw


def simulate(outdir: Path) -> dict[str, Any]:
    outdir.mkdir(parents=True, exist_ok=True)
    pointer, raw = fixture(16)
    pp = outdir / "pointer.json"
    cp = outdir / "candidate.json"
    dp = outdir / "durable" / "CONCEPT_AGENT_CURRENT_WORK_BINDING.json"
    rp = outdir / "DURABLE_BINDING_RECEIPT.json"
    pp.write_text(json.dumps(pointer, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    cp.write_bytes(raw)
    positive = accept(pp, cp, dp, rp)
    if dp.read_bytes() != raw:
        raise Blocked("POSITIVE_BYTES_CHANGED")

    negative = []
    bad = outdir / "tampered.json"
    bad.write_bytes(raw + b" ")
    try:
        accept(pp, bad, outdir / "bad-durable.json", outdir / "bad-receipt.json")
    except Blocked as exc:
        negative.append({"case": "byte-tamper", "blocked": True, "reason": str(exc)})
    else:
        raise Blocked("TAMPER_NOT_BLOCKED")

    wrong = json.loads(raw.decode("utf-8"))
    wrong["binding_sha256"] = "0" * 64
    wrong_raw = (json.dumps(wrong, ensure_ascii=False, sort_keys=True, separators=(",", ":")) + "\n").encode("utf-8")
    pointer2 = dict(pointer)
    pointer2["cross_chat_transport_sha256"] = sha(wrong_raw)
    pp2 = outdir / "pointer-wrong-internal.json"
    cp2 = outdir / "candidate-wrong-internal.json"
    pp2.write_text(json.dumps(pointer2, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    cp2.write_bytes(wrong_raw)
    try:
        accept(pp2, cp2, outdir / "bad2-durable.json", outdir / "bad2-receipt.json")
    except Blocked as exc:
        negative.append({"case": "internal-binding-tamper", "blocked": True, "reason": str(exc)})
    else:
        raise Blocked("INTERNAL_BINDING_TAMPER_NOT_BLOCKED")

    proof = {
        "contract": "CONCEPT_AGENT_DURABLE_BINDING_SIMULATION_V1",
        "status": "PASS",
        "article_count": 16,
        "positive": positive,
        "negative": negative,
        "rule": "NO_HANDOFF_COMPLETE_WITHOUT_EXACT_DURABLE_BINDING",
        "publish_allowed": False,
    }
    proof["proof_sha256"] = stable(proof)
    (outdir / "CONCEPT_AGENT_DURABLE_BINDING_SIMULATION_V1.json").write_text(
        json.dumps(proof, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    return proof


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser()
    sub = ap.add_subparsers(dest="cmd", required=True)

    p = sub.add_parser("accept")
    p.add_argument("--pointer", required=True)
    p.add_argument("--candidate", required=True)
    p.add_argument("--durable", required=True)
    p.add_argument("--receipt", required=True)

    p = sub.add_parser("simulate")
    p.add_argument("--out", required=True)

    args = ap.parse_args(argv)
    try:
        if args.cmd == "simulate":
            proof = simulate(Path(args.out))
            print(json.dumps({"ok": True, "status": proof["status"], "article_count": 16, "proof_sha256": proof["proof_sha256"]}, sort_keys=True))
            return 0
        receipt = accept(Path(args.pointer), Path(args.candidate), Path(args.durable), Path(args.receipt))
        print(json.dumps({"ok": True, "status": "PASS", "transport_sha256": receipt["transport_sha256"], "receipt_sha256": receipt["receipt_sha256"]}, sort_keys=True))
        return 0
    except (Blocked, OSError, json.JSONDecodeError) as exc:
        print("CONCEPT_AGENT_BINDING_TRANSPORT_BLOCKED:" + str(exc), file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
