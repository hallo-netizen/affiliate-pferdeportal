from __future__ import annotations

import hashlib
import html
import json
import re
from difflib import SequenceMatcher
from typing import Any, Mapping, Sequence
from urllib.parse import urlparse

RESEARCH_CONTRACT = "SYSTEM4_RESEARCH_EVIDENCE_V1"
FACTS_CONTRACT = "SYSTEM4_FACTS_EVIDENCE_V1"
SHA_RE = re.compile(r"^[0-9a-f]{64}$")
URL_RE = re.compile(r"^https?://", re.I)

MIN_SOURCES = 1
MIN_SOURCE_EVIDENCE_CHARS = 40
MIN_CLAIMS = 2
MIN_CLAIM_TEXT_CHARS = 20
BATCH_SHINGLE_SIZE = 8
MAX_PAIRWISE_SHINGLE_JACCARD = 0.20
MAX_REPAIR_LENGTH_CHANGE = 0.30
MIN_REPAIR_SIMILARITY = 0.72


class ContentGuardError(RuntimeError):
    pass


def text_sha256(value: str) -> str:
    return hashlib.sha256(value.encode("utf-8")).hexdigest()


def _require(condition: bool, code: str) -> None:
    if not condition:
        raise ContentGuardError(code)


def _require_text(value: Any, code: str, minimum: int = 1) -> str:
    _require(isinstance(value, str) and len(value.strip()) >= minimum, code)
    return value.strip()


def _json_text(value: str, code: str) -> dict[str, Any]:
    try:
        obj = json.loads(value)
    except Exception as exc:
        raise ContentGuardError(code) from exc
    _require(isinstance(obj, dict), code)
    return obj


def _normalized_evidence(value: str) -> str:
    return re.sub(r"\s+", " ", value).strip()


def _source_metadata(source: Mapping[str, Any], index: int, prefix: str) -> dict[str, Any]:
    sid = _require_text(source.get("source_id"), f"{prefix}_SOURCE_ID_INVALID:{index}")
    title = _require_text(source.get("source_title"), f"{prefix}_SOURCE_TITLE_INVALID:{index}")
    url = _require_text(source.get("source_url"), f"{prefix}_SOURCE_URL_INVALID:{index}")
    retrieved_at = _require_text(source.get("retrieved_at"), f"{prefix}_SOURCE_RETRIEVED_AT_INVALID:{index}")
    snapshot = _require_text(source.get("snapshot_sha256"), f"{prefix}_SOURCE_HASH_INVALID:{index}")
    _require(URL_RE.match(url) is not None, f"{prefix}_SOURCE_URL_INVALID:{index}")
    parsed = urlparse(url)
    _require(bool(parsed.netloc and "." in parsed.netloc), f"{prefix}_SOURCE_URL_INVALID:{index}")
    _require(SHA_RE.fullmatch(snapshot) is not None, f"{prefix}_SOURCE_HASH_INVALID:{index}")
    _require(title.casefold() != sid.casefold(), f"{prefix}_SOURCE_TITLE_SYNTHETIC:{index}")
    out = {
        "source_id": sid,
        "source_title": title,
        "source_url": url.strip(),
        "retrieved_at": retrieved_at,
        "snapshot_sha256": snapshot,
    }
    if isinstance(source.get("source_kind"), str) and source["source_kind"].strip():
        out["source_kind"] = source["source_kind"].strip()
    return out


def _research_source(source: Mapping[str, Any], index: int, prefix: str = "RESEARCH") -> dict[str, Any]:
    out = _source_metadata(source, index, prefix)
    evidence = _require_text(
        source.get("evidence"),
        f"{prefix}_SOURCE_EVIDENCE_INVALID:{index}",
        MIN_SOURCE_EVIDENCE_CHARS,
    )
    _require(
        text_sha256(evidence) == out["snapshot_sha256"],
        f"{prefix}_SOURCE_HASH_MISMATCH:{index}",
    )
    out["evidence"] = evidence
    return out


def validate_research_document(value: str | Mapping[str, Any]) -> dict[str, Any]:
    obj = _json_text(value, "RESEARCH_JSON_INVALID") if isinstance(value, str) else dict(value)
    _require(obj.get("contract") == RESEARCH_CONTRACT, "RESEARCH_CONTRACT_INVALID")
    sources = obj.get("sources")
    _require(isinstance(sources, list) and len(sources) >= MIN_SOURCES, "RESEARCH_SOURCE_COUNT_TOO_LOW")

    normalized: list[dict[str, Any]] = []
    ids: set[str] = set()
    hashes: set[str] = set()
    for index, raw in enumerate(sources):
        _require(isinstance(raw, dict), f"RESEARCH_SOURCE_OBJECT_REQUIRED:{index}")
        source = _research_source(raw, index)
        _require(source["source_id"] not in ids, f"RESEARCH_SOURCE_ID_DUPLICATE:{index}")
        _require(source["snapshot_sha256"] not in hashes, f"RESEARCH_SOURCE_EVIDENCE_DUPLICATE:{index}")
        ids.add(source["source_id"])
        hashes.add(source["snapshot_sha256"])
        normalized.append(source)
    return {"contract": RESEARCH_CONTRACT, "sources": normalized}


def _claim_core(
    claim: Mapping[str, Any],
    index: int,
    sources: Mapping[str, Mapping[str, Any]],
) -> dict[str, Any]:
    fact_id = _require_text(claim.get("fact_id"), f"FACT_ID_INVALID:{index}")
    source_id = _require_text(claim.get("source_id"), f"FACT_SOURCE_ID_INVALID:{index}")
    statement = _require_text(claim.get("statement"), f"FACT_STATEMENT_INVALID:{index}", MIN_CLAIM_TEXT_CHARS)
    evidence_text = _require_text(
        claim.get("evidence_text"),
        f"FACT_EVIDENCE_TEXT_INVALID:{index}",
        MIN_CLAIM_TEXT_CHARS,
    )
    evidence_hash = _require_text(claim.get("evidence_text_sha256"), f"FACT_EVIDENCE_HASH_INVALID:{index}")
    _require(source_id in sources, f"FACT_SOURCE_NOT_IN_RESEARCH:{index}")
    _require(SHA_RE.fullmatch(evidence_hash) is not None, f"FACT_EVIDENCE_HASH_INVALID:{index}")
    _require(text_sha256(evidence_text) == evidence_hash, f"FACT_EVIDENCE_HASH_MISMATCH:{index}")
    source_evidence = sources[source_id].get("evidence")
    _require(isinstance(source_evidence, str) and source_evidence.strip(), f"FACT_SOURCE_EVIDENCE_MISSING:{index}")
    _require(
        _normalized_evidence(evidence_text) in _normalized_evidence(source_evidence),
        f"FACT_EVIDENCE_NOT_IN_SOURCE:{index}",
    )
    return {
        "fact_id": fact_id,
        "source_id": source_id,
        "statement": statement,
        "evidence_text": evidence_text,
        "evidence_text_sha256": evidence_hash,
    }


def validate_facts_document(
    value: str | Mapping[str, Any],
    research: str | Mapping[str, Any],
) -> dict[str, Any]:
    research_obj = validate_research_document(research)
    sources = {row["source_id"]: row for row in research_obj["sources"]}
    obj = _json_text(value, "FACTS_JSON_INVALID") if isinstance(value, str) else dict(value)
    _require(obj.get("contract") == FACTS_CONTRACT, "FACTS_CONTRACT_INVALID")
    claims = obj.get("claims")
    _require(isinstance(claims, list) and len(claims) >= MIN_CLAIMS, "FACTS_CLAIM_COUNT_TOO_LOW")

    normalized: list[dict[str, Any]] = []
    ids: set[str] = set()
    statements: set[str] = set()
    for index, raw in enumerate(claims):
        _require(isinstance(raw, dict), f"FACT_OBJECT_REQUIRED:{index}")
        claim = _claim_core(raw, index, sources)
        _require(claim["fact_id"] not in ids, f"FACT_ID_DUPLICATE:{index}")
        folded = re.sub(r"\s+", " ", claim["statement"].casefold()).strip()
        _require(folded not in statements, f"FACT_STATEMENT_DUPLICATE:{index}")
        ids.add(claim["fact_id"])
        statements.add(folded)
        normalized.append(claim)
    return {"contract": FACTS_CONTRACT, "claims": normalized}


def _pack_sources(fact_pack: Mapping[str, Any]) -> dict[str, dict[str, Any]]:
    raw_sources = fact_pack.get("sources")
    _require(
        isinstance(raw_sources, list) and len(raw_sources) >= MIN_SOURCES,
        "FACT_PACK_SOURCES_MISSING",
    )
    out: dict[str, dict[str, Any]] = {}
    for index, raw in enumerate(raw_sources):
        _require(isinstance(raw, dict), f"FACT_PACK_SOURCE_OBJECT_REQUIRED:{index}")
        meta = _research_source(raw, index, "FACT_PACK")
        _require(meta["source_id"] not in out, f"FACT_PACK_SOURCE_ID_DUPLICATE:{index}")
        out[meta["source_id"]] = meta
    return out


def _pack_claims(
    fact_pack: Mapping[str, Any],
    sources: Mapping[str, Mapping[str, Any]],
) -> dict[str, dict[str, Any]]:
    raw_claims = fact_pack.get("claims")
    _require(
        isinstance(raw_claims, list) and len(raw_claims) >= MIN_CLAIMS,
        "FACT_PACK_CLAIMS_TOO_LOW",
    )
    out: dict[str, dict[str, Any]] = {}
    for index, raw in enumerate(raw_claims):
        _require(isinstance(raw, dict), f"FACT_PACK_CLAIM_OBJECT_REQUIRED:{index}")
        core = _claim_core(raw, index, sources)
        _require(core["fact_id"] not in out, f"FACT_PACK_FACT_ID_DUPLICATE:{index}")
        source_url = raw.get("source_url")
        if source_url is not None:
            _require(
                isinstance(source_url, str) and source_url.strip() == sources[core["source_id"]]["source_url"],
                f"FACT_PACK_CLAIM_SOURCE_URL_MISMATCH:{index}",
            )
        out[core["fact_id"]] = core
    return out


def validate_fact_pack(
    fact_pack: Mapping[str, Any],
    research: str | Mapping[str, Any] | None = None,
    facts: str | Mapping[str, Any] | None = None,
) -> None:
    _require(isinstance(fact_pack, Mapping), "FACT_PACK_OBJECT_REQUIRED")
    _require(fact_pack.get("contract") == "canonical_fact_pack_v1", "FACT_PACK_CONTRACT_INVALID")
    status = fact_pack.get("status") or fact_pack.get("production_readiness_status")
    _require(status == "SOURCE_VERIFIED_PRODUCTION_READY", "FACT_PACK_NOT_PRODUCTION_READY")

    pack_sources = _pack_sources(fact_pack)
    pack_claims = _pack_claims(fact_pack, pack_sources)

    if research is not None:
        research_obj = validate_research_document(research)
        expected_sources = {
            row["source_id"]: {
                key: row[key]
                for key in ("source_id", "source_title", "source_url", "retrieved_at", "snapshot_sha256", "evidence")
            }
            for row in research_obj["sources"]
        }
        actual_sources = {
            source_id: {
                key: meta[key]
                for key in ("source_id", "source_title", "source_url", "retrieved_at", "snapshot_sha256", "evidence")
            }
            for source_id, meta in pack_sources.items()
        }
        _require(actual_sources == expected_sources, "FACT_PACK_RESEARCH_BINDING_MISMATCH")

    if facts is not None:
        _require(research is not None, "FACT_PACK_FACTS_RESEARCH_REQUIRED")
        facts_obj = validate_facts_document(facts, research)
        expected_claims = {row["fact_id"]: row for row in facts_obj["claims"]}
        _require(pack_claims == expected_claims, "FACT_PACK_FACTS_BINDING_MISMATCH")


def _visible_text(article: str) -> str:
    value = re.sub(r"(?is)<!--.*?-->", " ", article)
    value = re.sub(r"(?is)<(script|style)\b[^>]*>.*?</\1>", " ", value)
    value = re.sub(r"(?s)<[^>]+>", " ", value)
    value = html.unescape(value)
    return re.sub(r"\s+", " ", value).strip()


def _word_tokens(article: str) -> list[str]:
    return [
        token.casefold()
        for token in re.findall(r"\b[\wÄÖÜäöüß-]+\b", _visible_text(article), flags=re.UNICODE)
    ]


def _shingles(article: str, size: int = BATCH_SHINGLE_SIZE) -> set[tuple[str, ...]]:
    words = _word_tokens(article)
    if len(words) < size:
        return set()
    return {tuple(words[i:i + size]) for i in range(len(words) - size + 1)}


def pairwise_shingle_jaccard(first: str, second: str) -> float:
    a = _shingles(first)
    b = _shingles(second)
    if not a and not b:
        return 1.0 if _visible_text(first).casefold() == _visible_text(second).casefold() else 0.0
    if not a or not b:
        return 0.0
    return len(a & b) / len(a | b)


def validate_batch_distinctness(bodies: Sequence[str]) -> dict[str, Any]:
    _require(isinstance(bodies, Sequence) and len(bodies) >= 2, "BATCH_DISTINCTNESS_INPUT_INVALID")
    maximum = 0.0
    worst_pair: tuple[int, int] | None = None
    for left in range(len(bodies)):
        _require(isinstance(bodies[left], str) and bodies[left].strip(), f"BATCH_BODY_INVALID:{left}")
        for right in range(left + 1, len(bodies)):
            score = pairwise_shingle_jaccard(bodies[left], bodies[right])
            if score > maximum:
                maximum = score
                worst_pair = (left, right)
    _require(
        maximum < MAX_PAIRWISE_SHINGLE_JACCARD,
        "BATCH_TEMPLATE_REUSE_BLOCKED:"
        + (f"{worst_pair[0]}:{worst_pair[1]}:{maximum:.4f}" if worst_pair else f"{maximum:.4f}"),
    )
    return {
        "status": "PASS",
        "max_pairwise_shingle_jaccard": round(maximum, 6),
        "threshold": MAX_PAIRWISE_SHINGLE_JACCARD,
    }


def validate_repair_continuity(old_body: str, new_body: str) -> dict[str, Any]:
    _require(isinstance(old_body, str) and old_body.strip(), "REPAIR_OLD_BODY_INVALID")
    _require(isinstance(new_body, str) and new_body.strip(), "REPAIR_NEW_BODY_INVALID")
    old = _visible_text(old_body)
    new = _visible_text(new_body)
    _require(old != new, "REPAIR_DRAFT_UNCHANGED")
    length_change = abs(len(new) - len(old)) / max(1, len(old))
    similarity = SequenceMatcher(None, old, new, autojunk=False).ratio()
    _require(length_change <= MAX_REPAIR_LENGTH_CHANGE, f"REPAIR_SCOPE_TOO_LARGE:LENGTH:{length_change:.4f}")
    _require(similarity >= MIN_REPAIR_SIMILARITY, f"REPAIR_SCOPE_TOO_LARGE:SIMILARITY:{similarity:.4f}")
    return {
        "status": "PASS",
        "length_change": round(length_change, 6),
        "similarity": round(similarity, 6),
    }


def validate_article_fact_ids(article: str, fact_pack: Mapping[str, Any]) -> dict[str, Any]:
    claims = fact_pack.get("claims")
    _require(isinstance(claims, list) and claims, "ARTICLE_FACT_PACK_CLAIMS_MISSING")
    known = {
        str(row.get("fact_id"))
        for row in claims
        if isinstance(row, dict) and isinstance(row.get("fact_id"), str) and row.get("fact_id")
    }
    _require(known, "ARTICLE_FACT_IDS_MISSING")
    referenced = set(re.findall(r'data-fact-id=["\']([^"\']+)["\']', article, flags=re.I))
    for group in re.findall(r'data-fact-ids=["\']([^"\']+)["\']', article, flags=re.I):
        referenced.update(token for token in re.split(r"\s+", group.strip()) if token)
    unknown = sorted(referenced - known)
    _require(not unknown, "ARTICLE_UNKNOWN_FACT_ID:" + (unknown[0] if unknown else ""))
    _require(referenced, "ARTICLE_FACT_TRACE_MISSING")
    return {"status": "PASS", "referenced_fact_count": len(referenced)}


def validate_single_article(article: str, fact_pack: Mapping[str, Any]) -> dict[str, Any]:
    validate_fact_pack(fact_pack)
    trace = validate_article_fact_ids(article, fact_pack)
    return {"status": "PASS", "trace": trace}
