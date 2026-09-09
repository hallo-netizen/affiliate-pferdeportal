from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from p7_release_boundary import Blocked, canon, verify_external_signature, verify_for_import

JOB_CONTRACT="ALT_CENTRAL_MACHINE_JOB_V1"
JOB_KEYS={"contract","job_id","items","publish_allowed"}
ITEM_KEYS={"item_id","input"}

def verify_job_manifest(job_path: Path,signature_path: Path,public_key_path: Path) -> dict:
    if not job_path.is_file():
        raise Blocked("JOB_MANIFEST_MISSING")
    raw=job_path.read_bytes()
    try:
        job=json.loads(raw.decode("utf-8"))
    except Exception as exc:
        raise Blocked("JOB_MANIFEST_JSON_INVALID") from exc
    if not isinstance(job,dict) or set(job)!=JOB_KEYS:
        raise Blocked("JOB_MANIFEST_SCHEMA_INVALID")
    if job.get("contract")!=JOB_CONTRACT:
        raise Blocked("JOB_MANIFEST_CONTRACT_INVALID")
    if job.get("publish_allowed") is not False:
        raise Blocked("JOB_MANIFEST_PUBLISH_NOT_ALLOWED")
    if not isinstance(job.get("job_id"),str) or not job["job_id"]:
        raise Blocked("JOB_ID_INVALID")
    items=job.get("items")
    if not isinstance(items,list) or not items:
        raise Blocked("JOB_ITEMS_INVALID")
    seen=set()
    for item in items:
        if not isinstance(item,dict) or set(item)!=ITEM_KEYS:
            raise Blocked("JOB_ITEM_SCHEMA_INVALID")
        item_id=item.get("item_id")
        if not isinstance(item_id,str) or not item_id:
            raise Blocked("JOB_ITEM_ID_INVALID")
        if item_id in seen:
            raise Blocked("JOB_ITEM_DUPLICATE")
        seen.add(item_id)
        if not isinstance(item.get("input"),dict):
            raise Blocked("JOB_ITEM_INPUT_INVALID")
    if raw!=canon(job):
        raise Blocked("JOB_MANIFEST_NOT_CANONICAL")
    verify_external_signature(job_path,signature_path,public_key_path)
    return job

def next_incomplete_item(
    job_path: Path,
    job_signature_path: Path,
    public_key_path: Path,
    releases_dir: Path,
) -> dict | None:
    job=verify_job_manifest(job_path,job_signature_path,public_key_path)
    for item in job["items"]:
        item_id=item["item_id"]
        release_path=releases_dir/f"{item_id}.json"
        signature_path=releases_dir/f"{item_id}.sig"

        release_exists=release_path.exists()
        signature_exists=signature_path.exists()

        if release_exists != signature_exists:
            raise Blocked("PARTIAL_FINAL_RELEASE_PRESENT:"+item_id)

        if not release_exists:
            return {
                "job_id":job["job_id"],
                "item_id":item_id,
                "input":item["input"],
                "resume_mode":"RESTART_ITEM_FROM_BEGINNING",
            }

        verified=verify_for_import(release_path,signature_path,public_key_path)
        if verified["job_id"]!=job["job_id"]:
            raise Blocked("COMPLETED_RELEASE_JOB_MISMATCH:"+item_id)
        if verified["item_id"]!=item_id:
            raise Blocked("COMPLETED_RELEASE_ITEM_MISMATCH:"+item_id)

    return None
