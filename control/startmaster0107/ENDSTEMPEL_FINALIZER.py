#!/usr/bin/env python3
from __future__ import annotations

import base64
import hashlib
import json
import os
import re
import shlex
import subprocess
import sys
from pathlib import Path
from typing import Any, Callable, Mapping

PACKAGE_CONTRACT = "PSERC_APPROVED_PRODUCTION_PACKAGE_V1"
ENDSTAMP_CONTRACT = "PFERDE_ATELIER_ENDSTEMPEL_RELEASE_V1"
MANIFEST_CONTRACT = "PFERDE_ATELIER_ENDSTEMPEL_ARTICLE_MANIFEST_V1"
SIGN_REQUEST_CONTRACT = "PFERDE_ATELIER_ENDSTEMPEL_SIGN_REQUEST_V1"
RECEIPT_CONTRACT = "PFERDE_ATELIER_OUTPUT_RELEASE_RECEIPT_V2"
RECEIPT_STATUS = "OUTPUT_RELEASE_PASS_FINAL_REVIEW_AND_REARM_CONFIRMED"
FINAL_FILENAME = "GEN1_7_ARTIKEL_PSERC_APPROVED_PRODUCTION_PACKAGE_107008_FINAL.json"
ARTICLE_NAME_RE = re.compile(r"^ARTICLE_[0-9a-f]{64}\.md$")
HSM_COMMAND_ENV = "ENDSTEMPEL_HSM_CMD"
TIMEOUT_SECONDS = 20


class Blocked(RuntimeError):
    pass


def canonical(obj: Any) -> bytes:
    return json.dumps(obj, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode("utf-8")


def stable_hash(obj: Any) -> str:
    return hashlib.sha256(canonical(obj)).hexdigest()


def file_sha256(path: Path) -> str:
    h = hashlib.sha256()
    with Path(path).open("rb") as fh:
        for chunk in iter(lambda: fh.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def load_json(path: Path) -> dict[str, Any]:
    try:
        value = json.loads(Path(path).read_text(encoding="utf-8"))
    except Exception as exc:
        raise Blocked("JSON_INVALID:" + str(path)) from exc
    if not isinstance(value, dict):
        raise Blocked("JSON_OBJECT_REQUIRED:" + str(path))
    return value


def safe(repo: Path, ref: str) -> Path:
    rel = Path(str(ref or ""))
    if not ref or rel.is_absolute() or ".." in rel.parts:
        raise Blocked("INVALID_RELATIVE_REF")
    resolved = (repo / rel).resolve()
    root = repo.resolve()
    if resolved != root and root not in resolved.parents:
        raise Blocked("REF_ESCAPE")
    return resolved


def validate_receipt(repo: Path, receipt_ref: str) -> tuple[dict[str, Any], Path, str]:
    path = safe(repo, receipt_ref)
    if not path.is_file():
        raise Blocked("107008_RECEIPT_MISSING")
    receipt = load_json(path)
    if receipt.get("contract") != RECEIPT_CONTRACT:
        raise Blocked("107008_RECEIPT_CONTRACT_INVALID")
    if receipt.get("status") != RECEIPT_STATUS:
        raise Blocked("107008_RECEIPT_STATUS_INVALID")
    if int(receipt.get("final_review_sequence") or -1) != 107008:
        raise Blocked("107008_SEQUENCE_INVALID")
    if receipt.get("publish_allowed") is not False:
        raise Blocked("PUBLISH_MUST_BE_FALSE")
    batch = str(receipt.get("batch_sha256") or "")
    if not re.fullmatch(r"[0-9a-f]{64}", batch):
        raise Blocked("BATCH_INVALID")
    expected_parent = (repo / ".pferde-release" / batch).resolve()
    if path.parent.resolve() != expected_parent:
        raise Blocked("107008_RECEIPT_NOT_IN_BOUND_BATCH_RELEASE")
    outputs = receipt.get("outputs")
    if not isinstance(outputs, list) or not outputs:
        raise Blocked("107008_OUTPUTS_MISSING")
    return receipt, path, batch


def article_snapshot(repo: Path, receipt: Mapping[str, Any], batch: str) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    seen_names: set[str] = set()
    release_dir = (repo / ".pferde-release" / batch).resolve()
    for raw in receipt.get("outputs") or []:
        if not isinstance(raw, Mapping):
            raise Blocked("107008_OUTPUT_ROW_INVALID")
        ref = str(raw.get("released_ref") or "")
        digest = str(raw.get("sha256") or "")
        if not ref:
            raise Blocked("107008_OUTPUT_REF_MISSING")
        path = safe(repo, ref)
        if not ARTICLE_NAME_RE.fullmatch(path.name):
            continue
        if path.parent.resolve() != release_dir:
            raise Blocked("ARTICLE_OUTSIDE_BOUND_RELEASE")
        if path.name in seen_names:
            raise Blocked("DUPLICATE_ARTICLE_NAME")
        seen_names.add(path.name)
        if not path.is_file():
            raise Blocked("ARTICLE_MISSING:" + path.name)
        actual = file_sha256(path)
        if digest != actual:
            raise Blocked("ARTICLE_RECEIPT_HASH_MISMATCH:" + path.name)
        rows.append({
            "name": path.name,
            "released_ref": str(path.relative_to(repo)),
            "byte_length": path.stat().st_size,
            "sha256": actual,
        })
    if not rows:
        raise Blocked("NO_RELEASED_ARTICLES_FOUND")
    disk_names = {p.name for p in release_dir.glob("ARTICLE_*.md") if p.is_file()}
    if disk_names != seen_names:
        missing = sorted(seen_names - disk_names)
        additional = sorted(disk_names - seen_names)
        raise Blocked("ARTICLE_SET_MISMATCH:missing=" + ",".join(missing) + ":additional=" + ",".join(additional))
    return sorted(rows, key=lambda x: x["name"])


def build_manifest(repo: Path, receipt_ref: str) -> tuple[dict[str, Any], list[dict[str, Any]]]:
    receipt, receipt_path, batch = validate_receipt(repo, receipt_ref)
    before = article_snapshot(repo, receipt, batch)
    manifest = {
        "contract": MANIFEST_CONTRACT,
        "batch_sha256": batch,
        "source_107008_receipt_ref": str(receipt_path.relative_to(repo)),
        "source_107008_receipt_sha256": file_sha256(receipt_path),
        "article_count": len(before),
        "articles": before,
        "publish_allowed": False,
        "content_mutation_performed": False,
    }
    return manifest, before


def decode_public_key(public_key_b64: str) -> bytes:
    try:
        raw = base64.b64decode(public_key_b64, validate=True)
    except Exception as exc:
        raise Blocked("PUBLIC_KEY_B64_INVALID") from exc
    if len(raw) != 32:
        raise Blocked("PUBLIC_KEY_LENGTH_INVALID")
    return raw


def verify_signature(manifest_sha256: str, signature_b64: str, public_key_b64: str) -> None:
    if not re.fullmatch(r"[0-9a-f]{64}", manifest_sha256):
        raise Blocked("MANIFEST_HASH_INVALID")
    try:
        sig = base64.b64decode(signature_b64, validate=True)
    except Exception as exc:
        raise Blocked("SIGNATURE_B64_INVALID") from exc
    if len(sig) != 64:
        raise Blocked("SIGNATURE_LENGTH_INVALID")
    pub = decode_public_key(public_key_b64)
    try:
        from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PublicKey
        Ed25519PublicKey.from_public_bytes(pub).verify(sig, manifest_sha256.encode("ascii"))
    except Exception as exc:
        raise Blocked("ENDSTEMPEL_SIGNATURE_INVALID") from exc


def call_hsm(manifest_sha256: str, batch: str, receipt_sha256: str, article_count: int, command: str | None = None) -> dict[str, str]:
    cmd = str(command if command is not None else os.environ.get(HSM_COMMAND_ENV, "")).strip()
    if not cmd:
        raise Blocked("ENDSTEMPEL_NON_EXPORTABLE_SIGNER_NOT_BOUND")
    request = {
        "contract": SIGN_REQUEST_CONTRACT,
        "manifest_sha256": manifest_sha256,
        "batch_sha256": batch,
        "source_107008_receipt_sha256": receipt_sha256,
        "article_count": article_count,
        "algorithm": "ED25519",
    }
    try:
        cp = subprocess.run(
            shlex.split(cmd),
            input=json.dumps(request, ensure_ascii=False, separators=(",", ":")) + "\n",
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            timeout=TIMEOUT_SECONDS,
            check=False,
        )
    except subprocess.TimeoutExpired as exc:
        raise Blocked("ENDSTEMPEL_SIGNER_TIMEOUT") from exc
    except OSError as exc:
        raise Blocked("ENDSTEMPEL_SIGNER_UNREACHABLE") from exc
    if cp.returncode != 0:
        raise Blocked("ENDSTEMPEL_SIGNER_FAILED")
    raw = cp.stdout.strip()
    try:
        result = json.loads(raw)
    except json.JSONDecodeError as exc:
        raise Blocked("ENDSTEMPEL_SIGNER_RESPONSE_INVALID") from exc
    if not isinstance(result, dict):
        raise Blocked("ENDSTEMPEL_SIGNER_RESPONSE_INVALID")
    required = {"signing_key_id", "signing_public_key_sha256", "public_key_b64", "signature_b64"}
    if set(result) != required:
        raise Blocked("ENDSTEMPEL_SIGNER_RESPONSE_FIELDS_INVALID")
    public_raw = decode_public_key(str(result["public_key_b64"]))
    public_sha = hashlib.sha256(public_raw).hexdigest()
    if public_sha != result.get("signing_public_key_sha256"):
        raise Blocked("ENDSTEMPEL_PUBLIC_KEY_IDENTITY_MISMATCH")
    verify_signature(manifest_sha256, str(result["signature_b64"]), str(result["public_key_b64"]))
    return {k: str(result[k]) for k in required}


def build_final_envelope(manifest: Mapping[str, Any], signature: Mapping[str, str]) -> dict[str, Any]:
    mhash = stable_hash(manifest)
    envelope = {
        "contract": PACKAGE_CONTRACT,
        "endstamp_contract": ENDSTAMP_CONTRACT,
        "status": "ENDSTEMPEL_PASS",
        "batch_sha256": manifest["batch_sha256"],
        "article_manifest": dict(manifest),
        "article_manifest_sha256": mhash,
        "signature_algorithm": "ED25519",
        "signing_key_id": signature["signing_key_id"],
        "signing_public_key_sha256": signature["signing_public_key_sha256"],
        "signature_b64": signature["signature_b64"],
        "publish_allowed": False,
        "content_mutation_performed": False,
    }
    envelope["package_payload_sha256"] = stable_hash(envelope)
    return envelope


def finalize(repo: Path, receipt_ref: str, signer: Callable[[str, str, str, int], Mapping[str, str]] | None = None) -> dict[str, Any]:
    repo = Path(repo).resolve()
    manifest, before = build_manifest(repo, receipt_ref)
    mhash = stable_hash(manifest)
    signer_fn = signer or (lambda h, b, r, n: call_hsm(h, b, r, n))
    signed = dict(signer_fn(mhash, str(manifest["batch_sha256"]), str(manifest["source_107008_receipt_sha256"]), int(manifest["article_count"])))
    required = {"signing_key_id", "signing_public_key_sha256", "public_key_b64", "signature_b64"}
    if set(signed) != required:
        raise Blocked("ENDSTEMPEL_SIGNER_RESPONSE_FIELDS_INVALID")
    public_raw = decode_public_key(str(signed["public_key_b64"]))
    if hashlib.sha256(public_raw).hexdigest() != signed["signing_public_key_sha256"]:
        raise Blocked("ENDSTEMPEL_PUBLIC_KEY_IDENTITY_MISMATCH")
    verify_signature(mhash, str(signed["signature_b64"]), str(signed["public_key_b64"]))
    receipt = load_json(safe(repo, receipt_ref))
    after = article_snapshot(repo, receipt, str(manifest["batch_sha256"]))
    if before != after:
        raise Blocked("ARTICLE_BYTES_CHANGED_DURING_ENDSTAMP")
    final = build_final_envelope(manifest, signed)
    outdir = repo / ".pferde-release" / str(manifest["batch_sha256"])
    out = outdir / FINAL_FILENAME
    out.write_text(json.dumps(final, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    if article_snapshot(repo, receipt, str(manifest["batch_sha256"])) != before:
        out.unlink(missing_ok=True)
        raise Blocked("ARTICLE_BYTES_CHANGED_AFTER_ENDSTAMP")
    return {
        "ok": True,
        "status": "ENDSTEMPEL_FINAL_PASS",
        "final_ref": str(out.relative_to(repo)),
        "final_sha256": file_sha256(out),
        "batch_sha256": manifest["batch_sha256"],
        "article_count": manifest["article_count"],
        "content_mutation_performed": False,
        "publish_allowed": False,
    }


def main(argv: list[str]) -> int:
    try:
        if len(argv) != 2 or argv[0] != "finalize":
            raise Blocked("USE: ENDSTEMPEL_FINALIZER.py finalize RECEIPT_REF")
        repo = Path(__file__).resolve().parents[2]
        out = finalize(repo, argv[1])
        print(json.dumps(out, ensure_ascii=False, indent=2))
        return 0
    except Exception as exc:
        print(json.dumps({"ok": False, "status": "HARD_BLOCK", "reason": str(exc), "publish_allowed": False}, ensure_ascii=False, indent=2))
        return 2


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
