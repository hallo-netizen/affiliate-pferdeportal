from __future__ import annotations

import hashlib
import json
import subprocess
from pathlib import Path
from typing import Any

class Blocked(RuntimeError):
    pass

CONTRACT="ALT_CENTRAL_MACHINE_RELEASE_V1"
REQUIRED={"contract","job_id","item_id","content_sha256","payload","publish_allowed"}

def canon(obj: Any) -> bytes:
    return json.dumps(obj,sort_keys=True,separators=(",",":"),ensure_ascii=False).encode("utf-8")

def sha_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()

def build_release(job_id: str,item_id: str,payload: dict) -> dict:
    if not isinstance(job_id,str) or not job_id:
        raise ValueError("job_id required")
    if not isinstance(item_id,str) or not item_id:
        raise ValueError("item_id required")
    if not isinstance(payload,dict):
        raise ValueError("payload object required")
    content=canon(payload)
    return {
        "contract":CONTRACT,
        "job_id":job_id,
        "item_id":item_id,
        "content_sha256":sha_bytes(content),
        "payload":payload,
        "publish_allowed":False,
    }

def write_release(path: Path,release: dict) -> None:
    path.write_bytes(canon(release))

def verify_external_signature(data_path: Path,signature_path: Path,public_key_path: Path) -> None:
    if not data_path.is_file():
        raise Blocked("SIGNED_DATA_MISSING")
    if not signature_path.is_file():
        raise Blocked("SIGNATURE_MISSING")
    if not public_key_path.is_file():
        raise Blocked("PUBLIC_KEY_MISSING")
    proc=subprocess.run(
        [
            "openssl","pkeyutl","-verify","-pubin",
            "-inkey",str(public_key_path),
            "-rawin","-in",str(data_path),
            "-sigfile",str(signature_path),
        ],
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True,
    )
    if proc.returncode!=0:
        raise Blocked("EXTERNAL_SIGNATURE_INVALID")


def verify_for_import(release_path: Path,signature_path: Path,public_key_path: Path) -> dict:
    if not release_path.is_file():
        raise Blocked("RELEASE_MISSING")

    raw=release_path.read_bytes()
    try:
        release=json.loads(raw.decode("utf-8"))
    except Exception as exc:
        raise Blocked("RELEASE_JSON_INVALID") from exc

    if not isinstance(release,dict) or set(release)!=REQUIRED:
        raise Blocked("RELEASE_SCHEMA_INVALID")
    if release.get("contract")!=CONTRACT:
        raise Blocked("RELEASE_CONTRACT_INVALID")
    if release.get("publish_allowed") is not False:
        raise Blocked("PUBLISH_NOT_ALLOWED")
    if not isinstance(release.get("job_id"),str) or not release["job_id"]:
        raise Blocked("JOB_ID_INVALID")
    if not isinstance(release.get("item_id"),str) or not release["item_id"]:
        raise Blocked("ITEM_ID_INVALID")
    if not isinstance(release.get("payload"),dict):
        raise Blocked("PAYLOAD_INVALID")
    if release.get("content_sha256")!=sha_bytes(canon(release["payload"])):
        raise Blocked("CONTENT_HASH_MISMATCH")

    # Canonical bytes are mandatory: a semantically equivalent rewrite is still a different release.
    if raw!=canon(release):
        raise Blocked("RELEASE_NOT_CANONICAL")

    verify_external_signature(release_path,signature_path,public_key_path)

    return {
        "status":"IMPORT_VERIFIED_NO_PUBLISH",
        "job_id":release["job_id"],
        "item_id":release["item_id"],
        "content_sha256":release["content_sha256"],
        "publish_allowed":False,
    }
