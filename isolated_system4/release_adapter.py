from __future__ import annotations

import base64
import hashlib
import json
import re
from pathlib import Path
from typing import Any, Mapping

PACKAGE_CONTRACT = "PSERC_APPROVED_PRODUCTION_PACKAGE_V1"
ENDSTAMP_CONTRACT = "PFERDE_ATELIER_ENDSTEMPEL_RELEASE_V1"
MANIFEST_CONTRACT = "PFERDE_ATELIER_ENDSTEMPEL_ARTICLE_MANIFEST_V1"
SIGN_REQUEST_CONTRACT = "PFERDE_ATELIER_ENDSTEMPEL_SIGN_REQUEST_V1"


class ReleaseError(RuntimeError):
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


def _decode_public_key(value: str) -> bytes:
    try:
        raw = base64.b64decode(value, validate=True)
    except Exception as exc:
        raise ReleaseError("PUBLIC_KEY_B64_INVALID") from exc
    if len(raw) != 32:
        raise ReleaseError("PUBLIC_KEY_LENGTH_INVALID")
    return raw


def verify_signature(manifest_sha256: str, signature: Mapping[str, str]) -> None:
    required = {"signing_key_id", "signing_public_key_sha256", "public_key_b64", "signature_b64"}
    if set(signature) != required:
        raise ReleaseError("SIGNATURE_FIELDS_INVALID")
    pub = _decode_public_key(str(signature["public_key_b64"]))
    if hashlib.sha256(pub).hexdigest() != signature["signing_public_key_sha256"]:
        raise ReleaseError("PUBLIC_KEY_SHA_MISMATCH")
    try:
        sig = base64.b64decode(str(signature["signature_b64"]), validate=True)
    except Exception as exc:
        raise ReleaseError("SIGNATURE_B64_INVALID") from exc
    if len(sig) != 64:
        raise ReleaseError("SIGNATURE_LENGTH_INVALID")
    try:
        from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PublicKey
        Ed25519PublicKey.from_public_bytes(pub).verify(sig, manifest_sha256.encode("ascii"))
    except Exception as exc:
        raise ReleaseError("SIGNATURE_INVALID") from exc


def build_unsigned(state: Mapping[str, Any], out_dir: Path) -> dict[str, Any]:
    checks = state.get("checks")
    if not isinstance(checks, dict) or checks.get("status") != "PASS" or checks.get("mode") != "FULL_PRODUCTION":
        raise ReleaseError("FULL_PRODUCTION_CHECK_PASS_REQUIRED")
    if checks.get("checked_draft_sha256") != state.get("draft_sha256"):
        raise ReleaseError("CHECKED_DRAFT_HASH_MISMATCH")
    if state.get("publish_allowed") is not False:
        raise ReleaseError("PUBLISH_MUST_REMAIN_FALSE")
    article = state.get("article")
    if not isinstance(article, dict):
        raise ReleaseError("ARTICLE_BINDING_MISSING")
    slot = str(article.get("plan_slot") or "")
    batch = str(state.get("batch_sha256") or "")
    if not re.fullmatch(r"[0-9a-f]{64}", slot):
        raise ReleaseError("PLAN_SLOT_INVALID")
    if not re.fullmatch(r"[0-9a-f]{64}", batch):
        raise ReleaseError("BATCH_SHA_INVALID")
    draft = str(state.get("draft_markdown") or "")
    if hashlib.sha256(draft.encode("utf-8")).hexdigest() != state.get("draft_sha256"):
        raise ReleaseError("DRAFT_HASH_INVALID")

    out_dir = Path(out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    name = "ARTICLE_" + slot + ".md"
    article_path = out_dir / name
    article_path.write_bytes(draft.encode("utf-8"))
    article_sha = file_sha256(article_path)
    if article_sha != state.get("draft_sha256"):
        raise ReleaseError("ARTICLE_OUTPUT_BYTES_CHANGED")

    manifest = {
        "contract": MANIFEST_CONTRACT,
        "batch_sha256": batch,
        "source_system4_state_sha256": stable_hash(state),
        "article_count": 1,
        "articles": [{
            "name": name,
            "released_ref": name,
            "byte_length": article_path.stat().st_size,
            "sha256": article_sha,
        }],
        "publish_allowed": False,
        "content_mutation_performed": False,
    }
    manifest_sha = stable_hash(manifest)
    sign_request = {
        "contract": SIGN_REQUEST_CONTRACT,
        "manifest_sha256": manifest_sha,
        "batch_sha256": batch,
        "source_system4_state_sha256": manifest["source_system4_state_sha256"],
        "article_count": 1,
        "algorithm": "ED25519",
        "publish_allowed": False,
    }
    manifest_path = out_dir / "article_manifest.json"
    request_path = out_dir / "endstamp_sign_request.json"
    manifest_path.write_text(json.dumps(manifest, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    request_path.write_text(json.dumps(sign_request, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    return {
        "status": "SYSTEM4_ENDSTEMPEL_SIGNATURE_REQUIRED",
        "article_path": str(article_path),
        "article_sha256": article_sha,
        "manifest_path": str(manifest_path),
        "manifest_sha256": manifest_sha,
        "sign_request_path": str(request_path),
        "sign_request": sign_request,
        "publish_allowed": False,
    }


def finalize_signed(unsigned: Mapping[str, Any], signature: Mapping[str, str], final_path: Path) -> dict[str, Any]:
    manifest_path = Path(str(unsigned.get("manifest_path") or ""))
    if not manifest_path.is_file():
        raise ReleaseError("MANIFEST_FILE_MISSING")
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    if not isinstance(manifest, dict) or manifest.get("contract") != MANIFEST_CONTRACT:
        raise ReleaseError("MANIFEST_CONTRACT_INVALID")
    mhash = stable_hash(manifest)
    if mhash != unsigned.get("manifest_sha256"):
        raise ReleaseError("MANIFEST_HASH_DRIFT")
    verify_signature(mhash, signature)
    article_rows = manifest.get("articles")
    if not isinstance(article_rows, list) or len(article_rows) != 1:
        raise ReleaseError("ARTICLE_MANIFEST_INVALID")
    article_path = manifest_path.parent / str(article_rows[0].get("name") or "")
    if not article_path.is_file() or file_sha256(article_path) != article_rows[0].get("sha256"):
        raise ReleaseError("ARTICLE_BYTES_DRIFTED_BEFORE_FINAL_JSON")

    envelope = {
        "contract": PACKAGE_CONTRACT,
        "endstamp_contract": ENDSTAMP_CONTRACT,
        "status": "ENDSTEMPEL_PASS",
        "batch_sha256": manifest["batch_sha256"],
        "article_manifest": manifest,
        "article_manifest_sha256": mhash,
        "signature_algorithm": "ED25519",
        "signing_key_id": signature["signing_key_id"],
        "signing_public_key_sha256": signature["signing_public_key_sha256"],
        "signature_b64": signature["signature_b64"],
        "publish_allowed": False,
        "content_mutation_performed": False,
    }
    envelope["package_payload_sha256"] = stable_hash(envelope)
    final_path = Path(final_path)
    final_path.write_text(json.dumps(envelope, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    if file_sha256(article_path) != article_rows[0]["sha256"]:
        final_path.unlink(missing_ok=True)
        raise ReleaseError("ARTICLE_BYTES_CHANGED_AFTER_FINAL_JSON")
    return {
        "status": "SYSTEM4_WORDPRESS_SIGNED_JSON_READY",
        "final_path": str(final_path),
        "final_sha256": file_sha256(final_path),
        "article_sha256": article_rows[0]["sha256"],
        "publish_allowed": False,
        "content_mutation_performed": False,
    }
