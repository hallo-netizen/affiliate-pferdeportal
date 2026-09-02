#!/usr/bin/env python3
from __future__ import annotations

import base64
import hashlib
import importlib.util
import json
import os
import shlex
import subprocess
import sys
from pathlib import Path
from typing import Any, Callable

from cryptography.exceptions import InvalidSignature
from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PublicKey

REPO = Path(__file__).resolve().parents[2]
BATCH_SHA256 = "7f2e3290b6ac78ac7df1644395e57ac72f02dc1373e390eb2e532e57a8ce916a"
FINAL_FILENAME = "GEN1_7_ARTIKEL_PSERC_APPROVED_PRODUCTION_PACKAGE_107008_FINAL.json"
PROD_KEY_ID = "workflow-ed25519-8f521756284cb375"
PROD_KEY_SHA256 = "8f521756284cb375c907f508dac333f51b71b515419ee271ca68fa149db66f87"
PROD_PUBLIC_B64 = "6FCxYycU2bJysJFvtH5xZ0ia+k59ZLyK6Av8d9/ujm0="
DUAL_REL = "control/startmaster0107/STARTMASTER0107_DUAL_ROOTFIX_REPAIR.py"
RELEASE_GATE_REL = "control/startmaster0107/production-package-release/production_package_release_gate.py"
MANIFEST_REL = f"control/startmaster0107/recovery_sources/{BATCH_SHA256}/MANIFEST.json"
RED_PHONE_ENV = "PSERC_RED_PHONE_CMD"
TIMEOUT_SECONDS = 20


class RedPhoneBlocked(RuntimeError):
    pass


def _load_module(path: Path, name: str):
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise RedPhoneBlocked("RED_PHONE_MODULE_LOAD_FAILED:" + path.name)
    mod = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = mod
    spec.loader.exec_module(mod)
    return mod


def _load_json(path: Path) -> dict:
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except Exception as exc:
        raise RedPhoneBlocked("RED_PHONE_JSON_INVALID:" + str(path)) from exc
    if not isinstance(data, dict):
        raise RedPhoneBlocked("RED_PHONE_JSON_OBJECT_REQUIRED:" + str(path))
    return data


def _sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _safe(repo: Path, ref: str) -> Path:
    p = Path(str(ref or ""))
    if not str(ref or "") or p.is_absolute() or ".." in p.parts:
        raise RedPhoneBlocked("RED_PHONE_REF_INVALID")
    out = (repo / p).resolve()
    root = repo.resolve()
    if out != root and root not in out.parents:
        raise RedPhoneBlocked("RED_PHONE_REF_ESCAPE")
    return out


def validate_107008_receipt(repo: Path, receipt_ref: str) -> dict:
    receipt = _load_json(_safe(repo, receipt_ref))
    if receipt.get("contract") != "PFERDE_ATELIER_OUTPUT_RELEASE_RECEIPT_V2":
        raise RedPhoneBlocked("RED_PHONE_107008_RECEIPT_CONTRACT_INVALID")
    if receipt.get("status") != "OUTPUT_RELEASE_PASS_FINAL_REVIEW_AND_REARM_CONFIRMED":
        raise RedPhoneBlocked("RED_PHONE_107008_PASS_REQUIRED")
    if receipt.get("batch_sha256") != BATCH_SHA256:
        raise RedPhoneBlocked("RED_PHONE_BATCH_MISMATCH")
    if receipt.get("publish_allowed") is not False:
        raise RedPhoneBlocked("RED_PHONE_PUBLISH_MUST_REMAIN_FALSE")
    outputs = receipt.get("outputs")
    if not isinstance(outputs, list) or len(outputs) != 7:
        raise RedPhoneBlocked("RED_PHONE_107008_OUTPUT_COUNT_INVALID")
    return receipt


def article_snapshot(repo: Path) -> dict[str, str]:
    manifest = _load_json(repo / MANIFEST_REL)
    if manifest.get("contract") != "PFERDE_ATELIER_EXISTING_ARTICLE_RECOVERY_SOURCE_V1":
        raise RedPhoneBlocked("RED_PHONE_ARTICLE_MANIFEST_CONTRACT_INVALID")
    if manifest.get("batch_sha256") != BATCH_SHA256 or manifest.get("item_count") != 7:
        raise RedPhoneBlocked("RED_PHONE_ARTICLE_MANIFEST_BATCH_INVALID")
    if manifest.get("content_mutation_performed") is not False or manifest.get("publish_allowed") is not False:
        raise RedPhoneBlocked("RED_PHONE_ARTICLE_MANIFEST_POLICY_INVALID")
    items = manifest.get("items")
    if not isinstance(items, list) or len(items) != 7:
        raise RedPhoneBlocked("RED_PHONE_ARTICLE_MANIFEST_ITEMS_INVALID")
    snapshot: dict[str, str] = {}
    for row in items:
        if not isinstance(row, dict):
            raise RedPhoneBlocked("RED_PHONE_ARTICLE_MANIFEST_ROW_INVALID")
        ref = str(row.get("ref") or "")
        expected = str(row.get("sha256") or "")
        path = _safe(repo, ref)
        if not path.is_file() or _sha256(path) != expected:
            raise RedPhoneBlocked("RED_PHONE_ARTICLE_HASH_MISMATCH:" + ref)
        snapshot[ref] = expected
    return snapshot


def verify_signature(payload_sha256: str, signature_b64: str) -> None:
    if len(payload_sha256) != 64 or any(c not in "0123456789abcdef" for c in payload_sha256):
        raise RedPhoneBlocked("RED_PHONE_PAYLOAD_HASH_INVALID")
    try:
        signature = base64.b64decode(signature_b64, validate=True)
        public_key = base64.b64decode(PROD_PUBLIC_B64, validate=True)
    except Exception as exc:
        raise RedPhoneBlocked("RED_PHONE_SIGNATURE_ENCODING_INVALID") from exc
    if len(signature) != 64 or len(public_key) != 32:
        raise RedPhoneBlocked("RED_PHONE_SIGNATURE_LENGTH_INVALID")
    if hashlib.sha256(public_key).hexdigest() != PROD_KEY_SHA256:
        raise RedPhoneBlocked("RED_PHONE_TRUST_ANCHOR_INVALID")
    try:
        Ed25519PublicKey.from_public_bytes(public_key).verify(
            signature, payload_sha256.encode("ascii")
        )
    except InvalidSignature as exc:
        raise RedPhoneBlocked("RED_PHONE_SIGNATURE_INVALID") from exc


def call_red_phone(
    payload_sha256: str,
    *,
    runner: Callable[..., Any] = subprocess.run,
    command: str | None = None,
) -> str:
    cmd = (command if command is not None else os.environ.get(RED_PHONE_ENV, "")).strip()
    if not cmd:
        raise RedPhoneBlocked("RED_PHONE_DIRECT_LINE_NOT_CONNECTED")
    request = {
        "contract": "PSERC_SIGN_REQUEST_V1",
        "signature_algorithm": "ED25519",
        "signing_key_id": PROD_KEY_ID,
        "signing_public_key_sha256": PROD_KEY_SHA256,
        "payload_sha256": payload_sha256,
    }
    try:
        proc = runner(
            shlex.split(cmd),
            input=json.dumps(request, ensure_ascii=False, separators=(",", ":")) + "\n",
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            timeout=TIMEOUT_SECONDS,
        )
    except subprocess.TimeoutExpired as exc:
        raise RedPhoneBlocked("RED_PHONE_TIMEOUT") from exc
    except OSError as exc:
        raise RedPhoneBlocked("RED_PHONE_UNREACHABLE") from exc
    if proc.returncode:
        detail = (proc.stderr or proc.stdout or "").strip()[:240]
        raise RedPhoneBlocked("RED_PHONE_SIGNER_FAILED:" + detail)
    raw = (proc.stdout or "").strip()
    if not raw:
        raise RedPhoneBlocked("RED_PHONE_EMPTY_RESPONSE")
    try:
        response = json.loads(raw)
    except json.JSONDecodeError:
        signature_b64 = raw
    else:
        if not isinstance(response, dict):
            raise RedPhoneBlocked("RED_PHONE_RESPONSE_INVALID")
        if response.get("signing_key_id", PROD_KEY_ID) != PROD_KEY_ID:
            raise RedPhoneBlocked("RED_PHONE_KEY_ID_MISMATCH")
        if response.get("signing_public_key_sha256", PROD_KEY_SHA256) != PROD_KEY_SHA256:
            raise RedPhoneBlocked("RED_PHONE_KEY_SHA_MISMATCH")
        signature_b64 = str(response.get("signature_b64") or "")
    verify_signature(payload_sha256, signature_b64)
    return signature_b64


def finalize(repo: Path, receipt_ref: str) -> dict:
    repo = Path(repo).resolve()
    validate_107008_receipt(repo, receipt_ref)
    articles_before = article_snapshot(repo)
    dual = _load_module(repo / DUAL_REL, "red_phone_dual")
    context = dual.context_from_release(repo, receipt_ref)
    meta = context.get("workflow_release_metadata") or {}
    if meta.get("sequence") != 107008:
        raise RedPhoneBlocked("RED_PHONE_CONTEXT_NOT_107008")
    if meta.get("exact_five_batch_sha256") != BATCH_SHA256:
        raise RedPhoneBlocked("RED_PHONE_CONTEXT_BATCH_MISMATCH")
    if int(meta.get("exact_five_item_count") or -1) != 7:
        raise RedPhoneBlocked("RED_PHONE_CONTEXT_ITEM_COUNT_INVALID")

    package = dual.build_package(
        context,
        lambda payload_hash: call_red_phone(payload_hash),
        PROD_KEY_ID,
        PROD_KEY_SHA256,
        PROD_PUBLIC_B64,
        True,
    )

    outdir = repo / ".pferde-release" / BATCH_SHA256
    outdir.mkdir(parents=True, exist_ok=True)
    output = outdir / FINAL_FILENAME
    dual.dump(output, package)
    dual.verify_package(repo, output)

    gate = _load_module(repo / RELEASE_GATE_REL, "red_phone_release_gate")
    gate.validate_package(output, repo, True)

    articles_after = article_snapshot(repo)
    if articles_before != articles_after:
        raise RedPhoneBlocked("RED_PHONE_ARTICLE_MUTATION_DETECTED")
    if package.get("contract") != "PSERC_APPROVED_PRODUCTION_PACKAGE_V1":
        raise RedPhoneBlocked("RED_PHONE_FINAL_PACKAGE_CONTRACT_INVALID")

    return {
        "ok": True,
        "status": "RED_PHONE_FINAL_PACKAGE_PASS",
        "batch_sha256": BATCH_SHA256,
        "package_ref": str(output.relative_to(repo)),
        "package_sha256": _sha256(output),
        "package_id": package["package_id"],
        "article_count": 7,
        "articles_byte_identical": True,
        "publish_allowed": False,
    }


def main(argv: list[str]) -> int:
    try:
        if len(argv) != 2 or argv[0] != "finalize":
            raise RedPhoneBlocked("USE: PSERC_RED_PHONE.py finalize RECEIPT_REF")
        result = finalize(REPO, argv[1])
        print(json.dumps(result, ensure_ascii=False, indent=2))
        return 0
    except Exception as exc:
        print(
            json.dumps(
                {
                    "ok": False,
                    "status": "RED_PHONE_BLOCKED",
                    "reason": str(exc),
                    "publish_allowed": False,
                },
                ensure_ascii=False,
                indent=2,
            )
        )
        return 2


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
