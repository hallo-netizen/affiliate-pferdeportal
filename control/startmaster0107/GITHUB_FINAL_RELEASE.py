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
from typing import Any

REPO = Path(__file__).resolve().parents[2]
SOURCE_CONTRACT = "PFERDE_ATELIER_EXISTING_ARTICLE_RECOVERY_SOURCE_V1"
MANIFEST_CONTRACT = "PFERDE_ATELIER_ENDSTEMPEL_ARTICLE_MANIFEST_V1"
PACKAGE_CONTRACT = "PSERC_APPROVED_PRODUCTION_PACKAGE_V1"
ENDSTAMP_CONTRACT = "PFERDE_ATELIER_ENDSTEMPEL_RELEASE_V1"
SIGN_REQUEST_CONTRACT = "PFERDE_ATELIER_GITHUB_FINAL_SIGN_REQUEST_V1"
FINAL_FILENAME = "GEN1_7_ARTIKEL_PSERC_APPROVED_PRODUCTION_PACKAGE_107008_FINAL.json"
ARTICLE_RE = re.compile(r"^ARTICLE_[0-9a-f]{64}\.md$")
SHA_RE = re.compile(r"^[0-9a-f]{64}$")

class Blocked(RuntimeError):
    pass

def canonical(obj: Any) -> bytes:
    return json.dumps(obj, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode("utf-8")

def stable_hash(obj: Any) -> str:
    return hashlib.sha256(canonical(obj)).hexdigest()

def file_sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as fh:
        for chunk in iter(lambda: fh.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()

def load_json(path: Path) -> dict[str, Any]:
    try:
        obj = json.loads(path.read_text(encoding="utf-8"))
    except Exception as exc:
        raise Blocked("JSON_INVALID") from exc
    if not isinstance(obj, dict):
        raise Blocked("JSON_OBJECT_REQUIRED")
    return obj

def safe(ref: str) -> Path:
    p = Path(str(ref or ""))
    if not ref or p.is_absolute() or ".." in p.parts:
        raise Blocked("REF_INVALID")
    out = (REPO / p).resolve()
    if out != REPO.resolve() and REPO.resolve() not in out.parents:
        raise Blocked("REF_ESCAPE")
    return out

def load_source(ref: str) -> tuple[dict[str, Any], Path, str]:
    path = safe(ref)
    if not path.is_file():
        raise Blocked("SOURCE_MANIFEST_MISSING")
    src = load_json(path)
    if src.get("contract") != SOURCE_CONTRACT:
        raise Blocked("SOURCE_CONTRACT_INVALID")
    batch = str(src.get("batch_sha256") or "")
    if not SHA_RE.fullmatch(batch):
        raise Blocked("BATCH_INVALID")
    expected = (REPO / "control/startmaster0107/recovery_sources" / batch / "MANIFEST.json").resolve()
    if path.resolve() != expected:
        raise Blocked("SOURCE_LOCATION_INVALID")
    if src.get("item_count") != 7 or src.get("publish_allowed") is not False or src.get("content_mutation_performed") is not False:
        raise Blocked("SOURCE_BINDING_INVALID")
    return src, path, batch

def load_import_envelope(src: dict[str, Any], source_path: Path, batch: str) -> tuple[dict[str, Any], str]:
    ref = str(src.get("import_envelope_ref") or "")
    declared = str(src.get("import_envelope_sha256") or "")
    path = safe(ref)
    if path.name != IMPORT_ENVELOPE_NAME or path.parent.resolve() != source_path.parent.resolve():
        raise Blocked("IMPORT_ENVELOPE_LOCATION_INVALID")
    if not path.is_file() or not SHA_RE.fullmatch(declared) or file_sha256(path) != declared:
        raise Blocked("IMPORT_ENVELOPE_FILE_HASH_INVALID")
    envelope = load_json(path)
    if stable_hash(envelope) != declared:
        raise Blocked("IMPORT_ENVELOPE_CANONICAL_HASH_INVALID")
    if set(envelope) != IMPORT_ENVELOPE_KEYS or envelope.get("contract") != PACKAGE_CONTRACT:
        raise Blocked("IMPORT_ENVELOPE_SCHEMA_INVALID")
    for field, obj in (
        ("fact_pack_bundle_sha256", envelope.get("fact_pack_bundle")),
        ("production_plan_sha256", envelope.get("production_plan")),
        ("workflow_release_sha256", envelope.get("workflow_release")),
    ):
        if not isinstance(obj, dict) or envelope.get(field) != stable_hash(obj):
            raise Blocked("IMPORT_ENVELOPE_COMPONENT_HASH_INVALID:" + field)
    expected_id = stable_hash({
        "contract": PACKAGE_CONTRACT,
        "fact_pack_bundle_sha256": envelope["fact_pack_bundle_sha256"],
        "production_plan_sha256": envelope["production_plan_sha256"],
        "workflow_release_sha256": envelope["workflow_release_sha256"],
    })
    if envelope.get("package_id") != expected_id:
        raise Blocked("IMPORT_ENVELOPE_PACKAGE_ID_INVALID")
    copy = dict(envelope)
    payload_hash = copy.pop("package_payload_sha256", None)
    if payload_hash != stable_hash(copy):
        raise Blocked("IMPORT_ENVELOPE_PACKAGE_PAYLOAD_HASH_INVALID")
    release = envelope["workflow_release"]
    if release.get("contract") != "WORKFLOW_SUPERVISOR_RELEASE_V2_SIGNED" or release.get("status") != "PASS":
        raise Blocked("IMPORT_ENVELOPE_RELEASE_INVALID")
    if release.get("wordpress_write_performed") is not False:
        raise Blocked("IMPORT_ENVELOPE_PREMATURE_WORDPRESS_WRITE")
    if release.get("exact_five_batch_sha256") != batch:
        raise Blocked("IMPORT_ENVELOPE_BATCH_INVALID")
    return envelope, declared

def validate_import_envelope_articles(envelope: dict[str, Any], articles: list[dict[str, Any]]) -> None:
    release = envelope["workflow_release"]
    release_by_slot = {
        str(row.get("plan_slot") or ""): str(row.get("canonical_article_id") or "")
        for row in (release.get("items") or []) if isinstance(row, dict)
    }
    plan_by_id = {
        str(row.get("canonical_article_id") or ""): row
        for row in (envelope["production_plan"].get("items") or []) if isinstance(row, dict)
    }
    if len(release_by_slot) != len(articles):
        raise Blocked("IMPORT_ENVELOPE_ARTICLE_COUNT_INVALID")
    for article in articles:
        cid = release_by_slot.get(article["plan_slot"])
        item = plan_by_id.get(cid) if cid else None
        body = (item or {}).get("canonical_article", {}).get("body_html")
        if not isinstance(body, str):
            raise Blocked("IMPORT_ENVELOPE_ARTICLE_BODY_MISSING:" + article["plan_slot"])
        raw = body.encode("utf-8")
        if hashlib.sha256(raw).hexdigest() != article["sha256"] or len(raw) != article["byte_length"]:
            raise Blocked("IMPORT_ENVELOPE_ARTICLE_BYTES_MISMATCH:" + article["plan_slot"])

def snapshot(src: dict[str, Any], source_path: Path, batch: str) -> list[dict[str, Any]]:
    rows = src.get("items")
    if not isinstance(rows, list) or len(rows) != 7:
        raise Blocked("SOURCE_ITEMS_INVALID")
    parent = source_path.parent.resolve()
    expected_names: set[str] = set()
    out: list[dict[str, Any]] = []
    for row in rows:
        if not isinstance(row, dict):
            raise Blocked("SOURCE_ITEM_INVALID")
        ref = str(row.get("ref") or "")
        digest = str(row.get("sha256") or "")
        slot = str(row.get("plan_slot") or "")
        p = safe(ref)
        name = p.name
        if not ARTICLE_RE.fullmatch(name) or p.parent.resolve() != parent:
            raise Blocked("ARTICLE_REF_INVALID")
        if not SHA_RE.fullmatch(digest) or not SHA_RE.fullmatch(slot):
            raise Blocked("ARTICLE_BINDING_INVALID")
        if name != f"ARTICLE_{slot}.md" or name in expected_names:
            raise Blocked("ARTICLE_NAME_OR_DUPLICATE_INVALID")
        if not p.is_file():
            raise Blocked("ARTICLE_MISSING:" + name)
        raw = p.read_bytes()
        if hashlib.sha256(raw).hexdigest() != digest:
            raise Blocked("ARTICLE_HASH_MISMATCH:" + name)
        try:
            text = raw.decode("utf-8")
        except UnicodeDecodeError as exc:
            raise Blocked("ARTICLE_UTF8_INVALID:" + name) from exc
        expected_names.add(name)
        out.append({"name": name, "plan_slot": slot, "sha256": digest, "byte_length": len(raw), "content_utf8": text})
    disk_names = {p.name for p in parent.glob("ARTICLE_*.md") if p.is_file()}
    if disk_names != expected_names:
        raise Blocked("ARTICLE_SET_MISMATCH")
    return sorted(out, key=lambda x: x["name"])

def call_signer(manifest_sha256: str, batch: str, source_sha256: str, count: int) -> dict[str, str]:
    cmd = os.environ.get("ENDSTEMPEL_HSM_CMD", "").strip()
    if not cmd:
        raise Blocked("SIGNER_NOT_BOUND")
    req = {"contract": SIGN_REQUEST_CONTRACT, "manifest_sha256": manifest_sha256, "batch_sha256": batch, "source_manifest_sha256": source_sha256, "article_count": count, "algorithm": "ED25519"}
    cp = subprocess.run(shlex.split(cmd), input=json.dumps(req, separators=(",", ":")) + "\n", text=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, timeout=20, check=False)
    if cp.returncode != 0:
        raise Blocked("SIGNER_FAILED")
    try:
        result = json.loads(cp.stdout)
    except Exception as exc:
        raise Blocked("SIGNER_RESPONSE_INVALID") from exc
    required = {"signing_key_id", "signing_public_key_sha256", "public_key_b64", "signature_b64"}
    if not isinstance(result, dict) or set(result) != required:
        raise Blocked("SIGNER_RESPONSE_FIELDS_INVALID")
    return {k: str(result[k]) for k in required}

def trusted_identity() -> dict[str, str]:
    out = {"signing_key_id": os.environ.get("ENDSTEMPEL_TRUSTED_KEY_ID", ""), "signing_public_key_sha256": os.environ.get("ENDSTEMPEL_TRUSTED_PUBLIC_KEY_SHA256", ""), "public_key_b64": os.environ.get("ENDSTEMPEL_TRUSTED_PUBLIC_KEY_B64", "")}
    if not out["signing_key_id"] or not SHA_RE.fullmatch(out["signing_public_key_sha256"]):
        raise Blocked("TRUSTED_IDENTITY_MISSING")
    raw = base64.b64decode(out["public_key_b64"], validate=True)
    if len(raw) != 32 or hashlib.sha256(raw).hexdigest() != out["signing_public_key_sha256"]:
        raise Blocked("TRUSTED_IDENTITY_INVALID")
    return out

def verify_sig(mhash: str, sig_b64: str, pub_b64: str) -> None:
    from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PublicKey
    sig = base64.b64decode(sig_b64, validate=True)
    pub = base64.b64decode(pub_b64, validate=True)
    if len(sig) != 64 or len(pub) != 32:
        raise Blocked("SIGNATURE_ENCODING_INVALID")
    try:
        Ed25519PublicKey.from_public_bytes(pub).verify(sig, mhash.encode("ascii"))
    except Exception as exc:
        raise Blocked("SIGNATURE_INVALID") from exc

def finalize(source_ref: str) -> dict[str, Any]:
    src, source_path, batch = load_source(source_ref)
    before = snapshot(src, source_path, batch)
    import_envelope, import_envelope_sha256 = load_import_envelope(src, source_path, batch)
    validate_import_envelope_articles(import_envelope, before)
    manifest = {"contract": MANIFEST_CONTRACT, "batch_sha256": batch, "source_manifest_ref": str(source_path.relative_to(REPO)), "source_manifest_sha256": file_sha256(source_path), "article_count": 7, "articles": before, "import_envelope_sha256": import_envelope_sha256, "publish_allowed": False, "content_mutation_performed": False}
    mhash = stable_hash(manifest)
    trust = trusted_identity()
    signed = call_signer(mhash, batch, manifest["source_manifest_sha256"], 7)
    for field in ("signing_key_id", "signing_public_key_sha256", "public_key_b64"):
        if signed[field] != trust[field]:
            raise Blocked("SIGNER_IDENTITY_MISMATCH:" + field)
    verify_sig(mhash, signed["signature_b64"], signed["public_key_b64"])
    if before != snapshot(src, source_path, batch):
        raise Blocked("ARTICLE_BYTES_CHANGED_DURING_FINALIZE")
    pkg = {"contract": PACKAGE_CONTRACT, "endstamp_contract": ENDSTAMP_CONTRACT, "status": "ENDSTEMPEL_PASS", "batch_sha256": batch, "article_manifest": manifest, "article_manifest_sha256": mhash, "import_envelope": import_envelope, "import_envelope_sha256": import_envelope_sha256, "signature_algorithm": "ED25519", "signing_key_id": signed["signing_key_id"], "signing_public_key_sha256": signed["signing_public_key_sha256"], "public_key_b64": signed["public_key_b64"], "signature_b64": signed["signature_b64"], "publish_allowed": False, "content_mutation_performed": False}
    pkg["package_payload_sha256"] = stable_hash(pkg)
    outdir = REPO / ".pferde-final"
    outdir.mkdir(exist_ok=True)
    out = outdir / FINAL_FILENAME
    if out.exists():
        raise Blocked("REPLAY_BLOCKED")
    tmp = out.with_suffix(out.suffix + ".tmp")
    try:
        tmp.write_text(json.dumps(pkg, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        if before != snapshot(src, source_path, batch):
            raise Blocked("ARTICLE_BYTES_CHANGED_BEFORE_COMMIT")
        os.replace(tmp, out)
    except Exception:
        tmp.unlink(missing_ok=True)
        out.unlink(missing_ok=True)
        raise
    return {"ok": True, "status": "GITHUB_FINAL_RELEASE_PASS", "final_ref": str(out.relative_to(REPO)), "final_sha256": file_sha256(out), "batch_sha256": batch, "article_count": 7, "publish_allowed": False, "content_mutation_performed": False}

def main() -> int:
    try:
        if len(sys.argv) != 3 or sys.argv[1] != "finalize":
            raise Blocked("USE: GITHUB_FINAL_RELEASE.py finalize SOURCE_MANIFEST_REF")
        print(json.dumps(finalize(sys.argv[2]), ensure_ascii=False, indent=2))
        return 0
    except Exception as exc:
        print(json.dumps({"ok": False, "status": "HARD_BLOCK", "reason": str(exc), "publish_allowed": False}, ensure_ascii=False, indent=2))
        return 2

if __name__ == "__main__":
    raise SystemExit(main())
