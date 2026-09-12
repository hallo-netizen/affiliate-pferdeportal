from __future__ import annotations

import base64
import hashlib
import json
import re
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Mapping

from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PublicKey

FINAL_CONTRACT = "PSERC_APPROVED_PRODUCTION_PACKAGE_V1"
ENDSTAMP_CONTRACT = "PFERDE_ATELIER_ENDSTEMPEL_RELEASE_V1"
MANIFEST_CONTRACT = "PFERDE_ATELIER_ENDSTEMPEL_ARTICLE_MANIFEST_V1"
SIGN_REQUEST_CONTRACT = "SYSTEM4_GITHUB_MANIFEST_SIGN_REQUEST_V1"
SIGN_RESPONSE_CONTRACT = "SYSTEM4_GITHUB_MANIFEST_SIGNATURE_V1"

PINNED_KEY_ID = "github-secret-ed25519-d2ebbf13f6c930e9"
PINNED_PUBLIC_SHA256 = "d2ebbf13f6c930e987d097a494e3d091db5de028775e1ecc27cbf877d1912df4"
PINNED_PUBLIC_B64 = "o909SI05NPsf9GvOM/M3ce33Od09lhYK8NPyf6SecMA="

SHA_RE = re.compile(r"^[0-9a-f]{64}$")
ARTICLE_RE = re.compile(r"^ARTICLE_([0-9a-f]{64})\.md$")


class SignatureBridgeError(RuntimeError):
    pass


@dataclass(frozen=True)
class Trust:
    key_id: str
    public_sha256: str
    public_b64: str


DEFAULT_TRUST = Trust(PINNED_KEY_ID, PINNED_PUBLIC_SHA256, PINNED_PUBLIC_B64)


def canonical(value: Any) -> bytes:
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode("utf-8")


def stable_hash(value: Any) -> str:
    return hashlib.sha256(canonical(value)).hexdigest()


def file_sha256(path: Path) -> str:
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def load_json(path: Path) -> dict[str, Any]:
    try:
        value = json.loads(Path(path).read_text(encoding="utf-8"))
    except Exception as exc:
        raise SignatureBridgeError("JSON_INVALID:" + str(path)) from exc
    if not isinstance(value, dict):
        raise SignatureBridgeError("JSON_OBJECT_REQUIRED:" + str(path))
    return value


def _validate_manifest(manifest: Mapping[str, Any]) -> tuple[str, str]:
    if manifest.get("contract") != MANIFEST_CONTRACT:
        raise SignatureBridgeError("MANIFEST_CONTRACT_INVALID")
    batch = str(manifest.get("batch_sha256") or "")
    if not SHA_RE.fullmatch(batch):
        raise SignatureBridgeError("MANIFEST_BATCH_INVALID")
    if manifest.get("article_count") != 7:
        raise SignatureBridgeError("MANIFEST_ARTICLE_COUNT_INVALID")
    if manifest.get("publish_allowed") is not False or manifest.get("content_mutation_performed") is not False:
        raise SignatureBridgeError("MANIFEST_FLAGS_INVALID")
    import_sha = str(manifest.get("import_envelope_sha256") or "")
    if not SHA_RE.fullmatch(import_sha):
        raise SignatureBridgeError("MANIFEST_IMPORT_ENVELOPE_SHA_INVALID")
    rows = manifest.get("articles")
    if not isinstance(rows, list) or len(rows) != 7:
        raise SignatureBridgeError("MANIFEST_ARTICLES_INVALID")
    seen: set[str] = set()
    for row in rows:
        if not isinstance(row, dict):
            raise SignatureBridgeError("MANIFEST_ARTICLE_INVALID")
        name = str(row.get("name") or "")
        slot = str(row.get("plan_slot") or "")
        match = ARTICLE_RE.fullmatch(name)
        content = row.get("content_utf8")
        digest = str(row.get("sha256") or "")
        if not match or match.group(1) != slot or slot in seen or not SHA_RE.fullmatch(digest):
            raise SignatureBridgeError("MANIFEST_ARTICLE_BINDING_INVALID")
        if not isinstance(content, str):
            raise SignatureBridgeError("MANIFEST_ARTICLE_CONTENT_INVALID")
        raw = content.encode("utf-8")
        if hashlib.sha256(raw).hexdigest() != digest or len(raw) != row.get("byte_length"):
            raise SignatureBridgeError("MANIFEST_ARTICLE_BYTES_INVALID:" + slot)
        seen.add(slot)
    return batch, stable_hash(dict(manifest))


def build_sign_request(manifest_path: Path, proof_path: Path, proof_ref: str) -> dict[str, Any]:
    manifest = load_json(Path(manifest_path))
    batch, manifest_sha = _validate_manifest(manifest)
    proof = load_json(Path(proof_path))
    if proof.get("publish_allowed") is not False:
        raise SignatureBridgeError("PROOF_PUBLISH_ALLOWED_INVALID")
    if proof.get("next_required") not in ("SIGNED_WORKFLOW_RELEASE", "SIGNED_WORKFLOW_RELEASE_REQUIRED"):
        raise SignatureBridgeError("PROOF_NEXT_BOUNDARY_INVALID")
    articles = proof.get("articles")
    if not isinstance(articles, list) or len(articles) != 7:
        raise SignatureBridgeError("PROOF_ARTICLE_COUNT_INVALID")
    proof_slots = [str(x.get("plan_slot") or "") for x in articles if isinstance(x, dict)]
    manifest_slots = [str(x.get("plan_slot") or "") for x in manifest["articles"]]
    if proof_slots != manifest_slots:
        raise SignatureBridgeError("PROOF_MANIFEST_SLOT_MISMATCH")
    proof_digests = [str(x.get("final_draft_sha256") or x.get("draft_sha256") or "") for x in articles if isinstance(x, dict)]
    manifest_digests = [str(x.get("sha256") or "") for x in manifest["articles"]]
    if proof_digests != manifest_digests:
        raise SignatureBridgeError("PROOF_MANIFEST_HASH_MISMATCH")
    return {
        "contract": SIGN_REQUEST_CONTRACT,
        "manifest_sha256": manifest_sha,
        "batch_sha256": batch,
        "article_count": 7,
        "algorithm": "ED25519",
        "proof_ref": proof_ref,
        "proof_sha256": file_sha256(Path(proof_path)),
        "publish_allowed": False,
    }


def _validate_trust(trust: Trust) -> bytes:
    if not trust.key_id or not SHA_RE.fullmatch(trust.public_sha256):
        raise SignatureBridgeError("TRUST_IDENTITY_INVALID")
    try:
        raw = base64.b64decode(trust.public_b64, validate=True)
    except Exception as exc:
        raise SignatureBridgeError("TRUST_PUBLIC_KEY_INVALID") from exc
    if len(raw) != 32 or hashlib.sha256(raw).hexdigest() != trust.public_sha256:
        raise SignatureBridgeError("TRUST_PUBLIC_KEY_INVALID")
    return raw


def apply_signature(unsigned_path: Path, signature_path: Path, out_path: Path, trust: Trust = DEFAULT_TRUST) -> dict[str, Any]:
    unsigned = load_json(Path(unsigned_path))
    allowed = {
        "contract", "endstamp_contract", "batch_sha256", "article_manifest",
        "import_envelope", "import_envelope_sha256", "publish_allowed",
        "content_mutation_performed",
    }
    if set(unsigned) != allowed:
        raise SignatureBridgeError("UNSIGNED_SCHEMA_INVALID")
    if unsigned.get("contract") != FINAL_CONTRACT or unsigned.get("endstamp_contract") != ENDSTAMP_CONTRACT:
        raise SignatureBridgeError("UNSIGNED_CONTRACT_INVALID")
    if unsigned.get("publish_allowed") is not False or unsigned.get("content_mutation_performed") is not False:
        raise SignatureBridgeError("UNSIGNED_FLAGS_INVALID")
    batch, manifest_sha = _validate_manifest(unsigned["article_manifest"])
    if unsigned.get("batch_sha256") != batch:
        raise SignatureBridgeError("UNSIGNED_BATCH_MISMATCH")
    import_sha = str(unsigned.get("import_envelope_sha256") or "")
    if not SHA_RE.fullmatch(import_sha) or stable_hash(unsigned.get("import_envelope")) != import_sha:
        raise SignatureBridgeError("UNSIGNED_IMPORT_ENVELOPE_HASH_INVALID")
    if unsigned["article_manifest"].get("import_envelope_sha256") != import_sha:
        raise SignatureBridgeError("MANIFEST_IMPORT_ENVELOPE_MISMATCH")

    response = load_json(Path(signature_path))
    required = {
        "contract", "manifest_sha256", "batch_sha256", "article_count", "algorithm",
        "signing_key_id", "signing_public_key_sha256", "public_key_b64", "signature_b64",
    }
    if set(response) != required or response.get("contract") != SIGN_RESPONSE_CONTRACT:
        raise SignatureBridgeError("SIGNATURE_RESPONSE_SCHEMA_INVALID")
    if response.get("manifest_sha256") != manifest_sha or response.get("batch_sha256") != batch:
        raise SignatureBridgeError("SIGNATURE_RESPONSE_BINDING_INVALID")
    if response.get("article_count") != 7 or response.get("algorithm") != "ED25519":
        raise SignatureBridgeError("SIGNATURE_RESPONSE_CONTRACT_INVALID")
    if (
        response.get("signing_key_id") != trust.key_id
        or response.get("signing_public_key_sha256") != trust.public_sha256
        or response.get("public_key_b64") != trust.public_b64
    ):
        raise SignatureBridgeError("SIGNER_IDENTITY_MISMATCH")
    pub_raw = _validate_trust(trust)
    try:
        sig = base64.b64decode(str(response.get("signature_b64") or ""), validate=True)
        if len(sig) != 64:
            raise ValueError("length")
        Ed25519PublicKey.from_public_bytes(pub_raw).verify(sig, manifest_sha.encode("ascii"))
    except Exception as exc:
        raise SignatureBridgeError("SIGNATURE_INVALID") from exc

    final = dict(unsigned)
    final["status"] = "ENDSTEMPEL_PASS"
    final["article_manifest_sha256"] = manifest_sha
    final["signature_algorithm"] = "ED25519"
    final["signing_key_id"] = trust.key_id
    final["signing_public_key_sha256"] = trust.public_sha256
    final["public_key_b64"] = trust.public_b64
    final["signature_b64"] = response["signature_b64"]
    final["package_payload_sha256"] = stable_hash(final)
    Path(out_path).write_text(json.dumps(final, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    return {
        "status": "SYSTEM4_SIGNED_WORDPRESS_JSON_READY",
        "final_ref": str(out_path),
        "final_sha256": file_sha256(Path(out_path)),
        "manifest_sha256": manifest_sha,
        "batch_sha256": batch,
        "article_count": 7,
        "publish_allowed": False,
    }


def main(argv: list[str]) -> int:
    try:
        if len(argv) == 6 and argv[1] == "request":
            request = build_sign_request(Path(argv[2]), Path(argv[3]), argv[4])
            Path(argv[5]).write_text(json.dumps(request, ensure_ascii=False, indent=2, sort_keys=True) + "\n", encoding="utf-8")
            print("SYSTEM4_SIGN_REQUEST_READY:" + stable_hash(request))
            return 0
        if len(argv) == 5 and argv[1] == "finalize":
            print(json.dumps(apply_signature(Path(argv[2]), Path(argv[3]), Path(argv[4])), ensure_ascii=False, sort_keys=True))
            return 0
        raise SignatureBridgeError("USAGE: request MANIFEST PROOF PROOF_REF OUT | finalize UNSIGNED SIGNATURE OUT")
    except SignatureBridgeError as exc:
        print("SYSTEM4_SIGNATURE_BRIDGE_FAIL:" + str(exc))
        return 2


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
