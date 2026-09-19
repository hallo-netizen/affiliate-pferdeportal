"""Erzeugt genau eine finale Concept-Agent-Rückgabedatei."""
import hashlib
import json
from dataclasses import asdict
from contracts import ArticleJob, Draft


def build_final_file(job: ArticleJob, draft: Draft, trace: list[str], writer: str) -> dict:
    body_bytes=draft.body.encode("utf-8")
    return {
        "contract": "CONCEPT_AGENT_FINAL_ARTICLE_V1",
        "job_id": job.job_id,
        "title": job.title,
        "keyword": job.keyword,
        "article_type": job.article_type,
        "category": job.category,
        "internal_links": list(job.internal_links),
        "writer": writer,
        "article_body": draft.body,
        "article_sha256": hashlib.sha256(body_bytes).hexdigest(),
        "trace": list(trace),
        "status": "FINAL_FILE_READY"
    }


def canonical_json(payload: dict) -> str:
    return json.dumps(payload, ensure_ascii=False, sort_keys=True, separators=(",", ":"))
