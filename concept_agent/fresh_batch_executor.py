#!/usr/bin/env python3
from __future__ import annotations

import argparse
import copy
import hashlib
import json
import os
import re
import sys
import urllib.error
import urllib.request
from pathlib import Path
from typing import Any
from urllib.parse import urlparse

REPO = Path(__file__).resolve().parents[1]
S4 = REPO / "isolated_system4"
if str(S4) not in sys.path:
    sys.path.insert(0, str(S4))

import intake_bridge
import authoring_contract
import content_guard
import controller_engine
import machine_point0
import source_acquisition

BINDING_CONTRACT = "CONCEPT_AGENT_PRODUCTIVE_WORK_BINDING_V1"
SYSTEM4_BOUND_CONTRACT = "CONCEPT_AGENT_SYSTEM4_BOUND_ITEM_V1"


class Blocked(RuntimeError):
    pass


def canon(value: Any) -> bytes:
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode("utf-8")


def stable(value: Any) -> str:
    return hashlib.sha256(canon(value)).hexdigest()


def sha_text(value: str) -> str:
    return hashlib.sha256(value.encode("utf-8")).hexdigest()


def load(path: Path) -> dict[str, Any]:
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except Exception as exc:
        raise Blocked("JSON_INVALID:" + str(path)) from exc
    if not isinstance(value, dict):
        raise Blocked("JSON_OBJECT_REQUIRED:" + str(path))
    return value


def write(path: Path, value: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def _response(payload: dict[str, Any], timeout: int = 240) -> dict[str, Any]:
    key = os.getenv("OPENAI_API_KEY", "").strip()
    if not key:
        raise Blocked("OPENAI_API_KEY_MISSING")
    req = urllib.request.Request(
        "https://api.openai.com/v1/responses",
        data=json.dumps(payload, ensure_ascii=False).encode("utf-8"),
        headers={"Authorization": "Bearer " + key, "Content-Type": "application/json"},
        method="POST",
    )
    try:
        with urllib.request.urlopen(req, timeout=timeout) as response:
            value = json.loads(response.read())
    except urllib.error.HTTPError as exc:
        detail = exc.read().decode("utf-8", "replace")[-600:]
        raise Blocked(f"OPENAI_HTTP_ERROR:{exc.code}:{detail}") from exc
    except Exception as exc:
        raise Blocked("OPENAI_CALL_FAILED:" + type(exc).__name__) from exc
    if not isinstance(value, dict):
        raise Blocked("OPENAI_RESPONSE_INVALID")
    return value


def _output_text(response: dict[str, Any]) -> str:
    for row in response.get("output", []):
        if not isinstance(row, dict) or row.get("type") != "message":
            continue
        for part in row.get("content", []):
            if isinstance(part, dict) and part.get("type") in {"output_text", "text"} and isinstance(part.get("text"), str):
                return part["text"]
    raise Blocked("OPENAI_OUTPUT_TEXT_MISSING")


def _candidate_sources(article: dict[str, Any]) -> list[dict[str, str]]:
    model = os.getenv("CONCEPT_AGENT_MODEL", "gpt-5.6-sol")
    prompt = (
        "Recherchiere für einen deutschsprachigen Pferde-Fachartikel belastbare Quellen. "
        "Suche im Web und nenne/citiere mindestens zehn konkrete öffentlich erreichbare Inhaltsseiten. "
        "Bevorzuge offizielle Stellen, Fachorganisationen, Hochschulen, Tierärzte, Versicherungsbedingungen, "
        "Hersteller-Fachdokumentation oder etablierte Fachmedien passend zum Thema. Vermeide Suchergebnisseiten, "
        "Foren, reine Shops ohne Fachinhalt und offensichtlich paywall-geschützte Seiten.\n\n"
        f"Titel: {article['title']}\n"
        f"Suchbegriff: {article['target_keyword']}\n"
        f"Artikeltyp: {article['article_type']}\n"
        "Deine Textantwort ist nur Hilfstext; entscheidend sind die von der Websuche gelieferten Quellen-URLs."
    )
    result = _response({
        "model": model,
        "reasoning": {"effort": "medium"},
        "tools": [{"type": "web_search", "search_context_size": "medium"}],
        "tool_choice": "auto",
        "include": ["web_search_call.action.sources"],
        "input": prompt,
    })
    found: list[dict[str, str]] = []
    seen: set[str] = set()

    def add(url: Any, title: Any = "") -> None:
        u = str(url or "").strip()
        if not u.startswith(("https://", "http://")) or u in seen:
            return
        host = urlparse(u).netloc.casefold()
        if not host or host.endswith("openai.com"):
            return
        seen.add(u)
        found.append({"url": u, "title": str(title or "").strip()})

    for row in result.get("output", []):
        if not isinstance(row, dict):
            continue
        action = row.get("action") if isinstance(row.get("action"), dict) else {}
        sources = action.get("sources") if isinstance(action.get("sources"), list) else []
        for src in sources:
            if isinstance(src, dict):
                add(src.get("url") or src.get("source_url"), src.get("title") or src.get("name"))
        for part in row.get("content", []) if isinstance(row.get("content"), list) else []:
            if not isinstance(part, dict):
                continue
            for ann in part.get("annotations", []) if isinstance(part.get("annotations"), list) else []:
                if isinstance(ann, dict) and ann.get("type") == "url_citation":
                    add(ann.get("url"), ann.get("title"))
    if len(found) < 2:
        raise Blocked("RESEARCH_WEB_SOURCE_CANDIDATES_TOO_LOW")
    return found


def _trim_source(source: dict[str, Any], limit: int = 24000) -> dict[str, Any]:
    row = dict(source)
    evidence = " ".join(str(row.get("evidence") or "").split())
    if len(evidence) > limit:
        evidence = evidence[:limit].rsplit(" ", 1)[0].strip()
    if len(evidence) < content_guard.MIN_SOURCE_EVIDENCE_CHARS:
        raise Blocked("RESEARCH_EVIDENCE_TOO_THIN")
    row["evidence"] = evidence
    row["snapshot_sha256"] = sha_text(evidence)
    return row


def _acquire_sources(article: dict[str, Any], minimum: int = 3) -> list[dict[str, Any]]:
    candidates = _candidate_sources(article)
    accepted: list[dict[str, Any]] = []
    slot = article["plan_slot"]
    for candidate in candidates[:16]:
        sid = "ca-" + hashlib.sha256(candidate["url"].encode("utf-8")).hexdigest()[:24]
        request = {
            "contract": source_acquisition.CONTRACT,
            "item_count": 1,
            "items": [{
                "item_index": 0,
                "plan_slot": slot,
                "sources": [{
                    "source_id": sid,
                    "source_url": candidate["url"],
                    "source_title": candidate["title"],
                    "source_kind": "OPENAI_WEB_SEARCH_BOUND_FETCH",
                }],
            }],
        }
        try:
            result = source_acquisition.acquire_batch(request, timeout=20.0, max_bytes=1_000_000)
            row = _trim_source(result["items"][0]["sources"][0])
            content_guard.validate_research_document({"contract": content_guard.RESEARCH_CONTRACT, "sources": [row]})
        except Exception:
            continue
        accepted.append(row)
        if len(accepted) >= minimum:
            break
    if len(accepted) < minimum:
        raise Blocked(f"RESEARCH_FETCHABLE_SOURCE_COUNT_TOO_LOW:{len(accepted)}:{minimum}")
    return accepted


def _facts_from_model(article: dict[str, Any], research: dict[str, Any]) -> dict[str, Any]:
    model = os.getenv("CONCEPT_AGENT_MODEL", "gpt-5.6-sol")
    source_ids = [s["source_id"] for s in research["sources"]]
    schema = {
        "type": "object",
        "additionalProperties": False,
        "properties": {
            "claims": {
                "type": "array",
                "minItems": 6,
                "maxItems": 12,
                "items": {
                    "type": "object",
                    "additionalProperties": False,
                    "properties": {
                        "source_id": {"type": "string", "enum": source_ids},
                        "statement": {"type": "string"},
                        "evidence_text": {"type": "string"},
                    },
                    "required": ["source_id", "statement", "evidence_text"],
                },
            }
        },
        "required": ["claims"],
    }
    payload = {
        "article": {k: article[k] for k in ("title", "target_keyword", "article_type")},
        "sources": research["sources"],
        "rules": [
            "Use only supplied source evidence.",
            "evidence_text must be copied verbatim as one contiguous passage from the selected source evidence.",
            "statement must be a factual German sentence supported by that passage.",
            "Choose useful, non-duplicate facts for the requested article.",
        ],
    }
    last_error = ""
    for _ in range(2):
        response = _response({
            "model": model,
            "reasoning": {"effort": "medium"},
            "input": [
                {"role": "developer", "content": "Du extrahierst nur belegte Fakten aus bereits gebundener Evidenz. Keine Websuche, keine zusätzlichen Quellen."},
                {"role": "user", "content": json.dumps(payload | ({"previous_validation_error": last_error} if last_error else {}), ensure_ascii=False)},
            ],
            "text": {"format": {"type": "json_schema", "name": "concept_agent_facts", "strict": True, "schema": schema}},
        })
        try:
            parsed = json.loads(_output_text(response))
            claims = []
            for index, row in enumerate(parsed.get("claims") or []):
                evidence = str(row.get("evidence_text") or "").strip()
                claims.append({
                    "fact_id": f"fact-{article['plan_slot'][:12]}-{index + 1}",
                    "source_id": row["source_id"],
                    "statement": str(row["statement"]).strip(),
                    "evidence_text": evidence,
                    "evidence_text_sha256": sha_text(evidence),
                })
            facts = {"contract": content_guard.FACTS_CONTRACT, "claims": claims}
            content_guard.validate_facts_document(facts, research)
            return facts
        except Exception as exc:
            last_error = str(exc)[:500]
    raise Blocked("FACT_EXTRACTION_NOT_VALID:" + last_error)


def _context_text(article: dict[str, Any], facts: dict[str, Any]) -> dict[str, str]:
    model = os.getenv("CONCEPT_AGENT_MODEL", "gpt-5.6-sol")
    claims = [{"fact_id": r["fact_id"], "statement": r["statement"]} for r in facts["claims"]]
    schema = {
        "type": "object",
        "additionalProperties": False,
        "properties": {
            "lead": {"type": "string"},
            "conclusion": {"type": "string"},
            "faq_direct_answer": {"type": "string"},
        },
        "required": ["lead", "conclusion", "faq_direct_answer"],
    }
    response = _response({
        "model": model,
        "reasoning": {"effort": "medium"},
        "input": [
            {"role": "developer", "content": "Formuliere nur kurze fachliche Bindetexte aus den gelieferten Fakten. Erfinde keine Fakten."},
            {"role": "user", "content": json.dumps({
                "title": article["title"], "target_keyword": article["target_keyword"], "article_type": article["article_type"],
                "facts": claims,
                "requirements": {
                    "lead": "1-2 klare Sätze",
                    "conclusion": "2-3 klare Sätze",
                    "faq_direct_answer": "Bei FAQ 45-70 Wörter direkte Antwort; sonst leerer String",
                },
            }, ensure_ascii=False)},
        ],
        "text": {"format": {"type": "json_schema", "name": "concept_agent_context_text", "strict": True, "schema": schema}},
    })
    value = json.loads(_output_text(response))
    return {k: str(value.get(k) or "").strip() for k in ("lead", "conclusion", "faq_direct_answer")}


def _slug(text: str) -> str:
    value = text.casefold().replace("ä", "ae").replace("ö", "oe").replace("ü", "ue").replace("ß", "ss")
    return re.sub(r"[^a-z0-9]+", "-", value).strip("-")[:160] or "artikel"


def _bind_item(article: dict[str, Any], sources: list[dict[str, Any]], batch_sha: str) -> dict[str, Any]:
    research = content_guard.validate_research_document({"contract": content_guard.RESEARCH_CONTRACT, "sources": copy.deepcopy(sources)})
    facts = _facts_from_model(article, research)
    normalized_facts = content_guard.validate_facts_document(facts, research)
    source_snapshot_id = stable({"article": article, "research": research})
    source_by_id = {r["source_id"]: r for r in research["sources"]}
    pack_claims = []
    for row in normalized_facts["claims"]:
        claim = dict(row)
        claim["source_url"] = source_by_id[row["source_id"]]["source_url"]
        claim["claim_status"] = "FULLY_SUPPORTED"
        claim["article_types"] = [article["article_type"]]
        pack_claims.append(claim)
    fact_pack = {
        "contract": "canonical_fact_pack_v1",
        "status": "SOURCE_VERIFIED_PRODUCTION_READY",
        "source_snapshot_id": source_snapshot_id,
        "fact_pack_id": source_snapshot_id,
        "sources": copy.deepcopy(research["sources"]),
        "claims": pack_claims,
    }
    content_guard.validate_fact_pack(fact_pack, research, normalized_facts)

    plan = machine_point0._prewrite_plan(REPO, article)
    quality = copy.deepcopy(plan["quality_binding"])
    text = _context_text(article, normalized_facts)
    if article["article_type"] == "FAQ":
        quality["faq_direct_answer"] = text["faq_direct_answer"]
    plan["quality_binding"] = quality
    plan["quality_binding_hash"] = authoring_contract._stable(quality)
    links = copy.deepcopy(quality.get("link_bindings") or [])
    allowed = [row["fact_id"] for row in pack_claims]
    direct = text["faq_direct_answer"] if article["article_type"] == "FAQ" else ""
    plan["source_snapshot_id"] = source_snapshot_id
    plan["runtime_order"] = {
        "order_id": "concept-agent-" + article["plan_slot"][:16],
        "article_type": article["article_type"],
        "title": article["title"],
        "slug": _slug(article["title"]),
        "subject_scope": article["title"],
        "subject_label": article["target_keyword"],
        "lead": text["lead"],
        "conclusion": text["conclusion"],
        "links": links,
        "allowed_fact_ids": allowed,
        "question": article["title"],
        "answer": direct or text["lead"],
        "faq_question": article["title"],
        "faq_answer": direct or text["lead"],
        "summary": text["lead"],
        "search_intent": plan.get("search_intent") or "informational",
    }
    plan["canonical_article"] = {
        "title": article["title"],
        "article_type": article["article_type"],
        "slug": plan["runtime_order"]["slug"],
    }
    plan["source_hashes"] = [row["snapshot_sha256"] for row in research["sources"]]

    state_seed: dict[str, Any] = {
        "contract": controller_engine.CONTRACT,
        "source_snapshot_sha256": source_snapshot_id,
        "batch_sha256": batch_sha,
        "article": {k: article[k] for k in ("title", "target_keyword", "category", "article_type", "plan_slot")},
        "publish_allowed": False,
    }
    production_context = {
        "fact_pack": fact_pack,
        "production_plan_item": plan,
        "sha256": controller_engine.sha({"fact_pack": fact_pack, "production_plan_item": plan}),
    }
    state_seed["production_context"] = production_context
    state_seed["authoring_contract"] = authoring_contract.build(REPO, state_seed, fact_pack, plan)
    authoring_contract.validate_bound(REPO, state_seed)
    system4 = {
        "contract": SYSTEM4_BOUND_CONTRACT,
        "source_snapshot_sha256": source_snapshot_id,
        "research_document": research,
        "facts_document": normalized_facts,
        "production_context": production_context,
        "authoring_contract": state_seed["authoring_contract"],
        "publish_allowed": False,
    }
    system4["binding_sha256"] = stable(system4)
    return system4


def build(snapshot_path: Path, intake_path: Path, out_path: Path) -> dict[str, Any]:
    snapshot = load(snapshot_path)
    intake = load(intake_path)
    expected = intake_bridge.prepare(snapshot)
    if stable(expected) != stable(intake):
        raise Blocked("INTAKE_NOT_EXACT_REPREPARATION")
    batch = snapshot.get("next_textmachine_metadata_batch")
    if not isinstance(batch, dict) or batch.get("batch_sha256") != intake.get("batch_sha256"):
        raise Blocked("SNAPSHOT_BATCH_MISMATCH")

    acquired: list[list[dict[str, Any]]] = []
    submission_items = []
    for article in intake["items"]:
        sources = _acquire_sources(article)
        acquired.append(sources)
        submission_items.append({
            "item_index": article["item_index"],
            "plan_slot": article["plan_slot"],
            "sources": [{k: s[k] for k in ("source_id", "source_title", "source_url", "evidence", "snapshot_sha256")} for s in sources],
        })
    submission = {
        "contract": intake_bridge.RESEARCH_SUBMISSION_CONTRACT,
        "batch_sha256": intake["batch_sha256"],
        "item_count": intake["item_count"],
        "items": submission_items,
    }
    research_bound = intake_bridge.bind_research(intake, submission)

    items = []
    for article, sources, bound_row in zip(intake["items"], acquired, research_bound["items"]):
        system4 = _bind_item(article, sources, intake["batch_sha256"])
        links = system4["production_context"]["production_plan_item"]["quality_binding"].get("link_bindings") or []
        if len([r for r in links if isinstance(r, dict) and r.get("active") is not False]) != 3:
            raise Blocked("AUTHORING_INTERNAL_LINK_COUNT_NOT_THREE:" + str(article["item_index"]))
        items.append({
            "item_index": article["item_index"],
            "plan_slot": article["plan_slot"],
            "title": article["title"],
            "target_keyword": article["target_keyword"],
            "category": article["category"],
            "article_type": article["article_type"],
            "research_binding": {
                "status": "BOUND",
                "article_identity_sha256": bound_row["article_identity_sha256"],
                "source_pool_sha256": bound_row["source_pool_sha256"],
                "sources": bound_row["sources"],
            },
            "authoring_binding": {
                "status": "BOUND",
                "internal_links": [r["href"] for r in links],
                "system4_authoring_contract_sha256": stable(system4["authoring_contract"]),
            },
            "system4_bound": system4,
        })
    binding = {
        "contract": BINDING_CONTRACT,
        "batch_sha256": intake["batch_sha256"],
        "item_count": intake["item_count"],
        "items": items,
        "research_binding_sha256": research_bound["research_binding_sha256"],
        "publish_allowed": False,
    }
    write(out_path, binding)
    return binding


def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser()
    p.add_argument("--snapshot", required=True)
    p.add_argument("--intake", required=True)
    p.add_argument("--out", required=True)
    args = p.parse_args(argv)
    try:
        result = build(Path(args.snapshot), Path(args.intake), Path(args.out))
        print(json.dumps({
            "ok": True,
            "status": "CONCEPT_AGENT_PRODUCTIVE_WORK_BINDING_READY",
            "batch_sha256": result["batch_sha256"],
            "item_count": result["item_count"],
            "binding_sha256": hashlib.sha256(Path(args.out).read_bytes()).hexdigest(),
            "publish_allowed": False,
        }, sort_keys=True))
        return 0
    except Exception as exc:
        print("CONCEPT_AGENT_FRESH_BATCH_BINDER_BLOCKED:" + str(exc), file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
