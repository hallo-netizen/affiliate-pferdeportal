#!/usr/bin/env python3
from __future__ import annotations
import base64, gzip, hashlib, json, re, sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
ARTICLE_RE = re.compile(r"^ARTICLE_[0-9a-f]{64}\.md$")
SHA_RE = re.compile(r"^[0-9a-f]{64}$")
FINAL_NAME = "GEN1_7_ARTIKEL_PSERC_APPROVED_PRODUCTION_PACKAGE_107008_FINAL.json"

class Blocked(RuntimeError):
    pass

def sha256_bytes(raw: bytes) -> str:
    return hashlib.sha256(raw).hexdigest()

def sha256_file(path: Path) -> str:
    return sha256_bytes(path.read_bytes())

def load_json(path: Path) -> dict:
    try:
        obj = json.loads(path.read_text(encoding="utf-8"))
    except Exception as exc:
        raise Blocked("JSON_INVALID:" + str(path)) from exc
    if not isinstance(obj, dict):
        raise Blocked("JSON_OBJECT_REQUIRED:" + str(path))
    return obj

def safe(ref: str) -> Path:
    p = Path(str(ref or ""))
    if not ref or p.is_absolute() or ".." in p.parts:
        raise Blocked("REF_INVALID")
    q = (REPO / p).resolve()
    root = REPO.resolve()
    if q != root and root not in q.parents:
        raise Blocked("REF_ESCAPE")
    return q

def build(release_receipt_ref: str, final_package_ref: str) -> dict:
    receipt_path = safe(release_receipt_ref)
    package_path = safe(final_package_ref)
    if not receipt_path.is_file():
        raise Blocked("RELEASE_RECEIPT_MISSING")
    if not package_path.is_file():
        raise Blocked("FINAL_PACKAGE_MISSING")
    if package_path.name != FINAL_NAME:
        raise Blocked("FINAL_PACKAGE_NAME_INVALID")

    receipt = load_json(receipt_path)
    if receipt.get("contract") != "PFERDE_ATELIER_OUTPUT_RELEASE_RECEIPT_V2":
        raise Blocked("RELEASE_RECEIPT_CONTRACT_INVALID")
    if receipt.get("status") != "OUTPUT_RELEASE_PASS_FINAL_REVIEW_AND_REARM_CONFIRMED":
        raise Blocked("RELEASE_RECEIPT_STATUS_INVALID")
    if receipt.get("publish_allowed") is not False:
        raise Blocked("AUTO_PUBLISH_FORBIDDEN")
    batch = str(receipt.get("batch_sha256") or "")
    if not SHA_RE.fullmatch(batch):
        raise Blocked("BATCH_INVALID")

    rows = receipt.get("outputs")
    if not isinstance(rows, list):
        raise Blocked("RELEASE_OUTPUTS_INVALID")
    articles = []
    for row in rows:
        if not isinstance(row, dict):
            continue
        ref = str(row.get("released_ref") or "")
        digest = str(row.get("sha256") or "")
        p = safe(ref)
        if ARTICLE_RE.fullmatch(p.name):
            if not p.is_file() or not SHA_RE.fullmatch(digest):
                raise Blocked("ARTICLE_OUTPUT_INVALID:" + p.name)
            raw = p.read_bytes()
            actual = sha256_bytes(raw)
            if actual != digest:
                raise Blocked("ARTICLE_HASH_MISMATCH:" + p.name)
            slot = p.name[len("ARTICLE_"):-3]
            if slot != p.stem[len("ARTICLE_"):]:
                raise Blocked("ARTICLE_SLOT_INVALID:" + p.name)
            articles.append({
                "name": p.name,
                "plan_slot": slot,
                "sha256": actual,
                "byte_length": len(raw),
                "content_utf8": raw.decode("utf-8"),
            })
    if len(articles) != 7 or len({a["name"] for a in articles}) != 7:
        raise Blocked("EXACTLY_SEVEN_ARTICLES_REQUIRED")
    articles.sort(key=lambda x: x["name"])

    source_manifest = {
        "contract": "PFERDE_ATELIER_EXISTING_ARTICLE_RECOVERY_SOURCE_V1",
        "batch_sha256": batch,
        "item_count": 7,
        "publish_allowed": False,
        "content_mutation_performed": False,
        "items": [
            {
                "ref": f"control/startmaster0107/recovery_sources/{batch}/{a['name']}",
                "sha256": a["sha256"],
                "plan_slot": a["plan_slot"],
            }
            for a in articles
        ],
    }

    payload = {
        "contract": "PFERDE_ATELIER_CHAT_DELIVERY_PAYLOAD_V1",
        "status": "DELIVERY_HANDOFF_READY",
        "batch_sha256": batch,
        "release_receipt_ref": release_receipt_ref,
        "release_receipt_sha256": sha256_file(receipt_path),
        "final_package_ref": final_package_ref,
        "final_package_sha256": pkg_sha,
        "source_manifest": source_manifest,
        "articles": articles,
        "publish_allowed": False,
        "content_mutation_performed": False,
    }
    raw = json.dumps(payload, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode("utf-8")
    packed = gzip.compress(raw, compresslevel=9, mtime=0)
    encoded = base64.b64encode(packed).decode("ascii")
    return {
        "ok": True,
        "status": "DELIVERY_HANDOFF_READY",
        "contract": "PFERDE_ATELIER_CHAT_DELIVERY_ENVELOPE_V1",
        "batch_sha256": batch,
        "payload_sha256": sha256_bytes(raw),
        "gzip_sha256": sha256_bytes(packed),
        "encoding": "gzip+base64",
        "payload_b64": encoded,
        "article_count": 7,
        "publish_allowed": False,
        "content_mutation_performed": False,
    }

def selftest() -> dict:
    return {
        "ok": True,
        "status": "CHAT_DELIVERY_PAYLOAD_SELFTEST_PASS",
        "publish_allowed": False,
        "content_mutation_performed": False,
    }

def main() -> int:
    try:
        if len(sys.argv) == 2 and sys.argv[1] == "selftest":
            out = selftest()
        elif len(sys.argv) == 4 and sys.argv[1] == "build":
            out = build(sys.argv[2], sys.argv[3])
        else:
            raise Blocked("USE: chat_delivery_payload.py selftest | build RELEASE_RECEIPT_REF FINAL_PACKAGE_REF")
        print(json.dumps(out, ensure_ascii=False, separators=(",", ":")))
        return 0
    except Exception as exc:
        print(json.dumps({"ok": False, "status": "CHAT_DELIVERY_PAYLOAD_BLOCKED", "reason": str(exc), "publish_allowed": False}, ensure_ascii=False, separators=(",", ":")))
        return 2

if __name__ == "__main__":
    raise SystemExit(main())
