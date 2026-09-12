from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Mapping

from isolated_system3.engine import ArticleProfile, System3Engine, System3Fail, _sha256
from isolated_system3.independent_checks import build_quality_evidence, build_rule_evidence


class LiveBoundaryFail(System3Fail):
    pass


def load_wordpress_input(path: str | Path) -> Mapping[str, Any]:
    p = Path(path)
    if p.suffix.lower() != ".json":
        raise LiveBoundaryFail("WORDPRESS_INPUT_FORMAT_FAIL")
    raw = json.loads(p.read_text(encoding="utf-8"))
    if not isinstance(raw, Mapping):
        raise LiveBoundaryFail("WORDPRESS_INPUT_SCHEMA_FAIL")
    return raw


def build_engine(profile_registry: Mapping[str, str]) -> System3Engine:
    if not profile_registry:
        raise LiveBoundaryFail("PROFILE_REGISTRY_EMPTY")
    profiles = {
        article_type: ArticleProfile(article_type=article_type, profile_ref=profile_ref)
        for article_type, profile_ref in profile_registry.items()
    }
    return System3Engine(profiles)


def run_live_boundary(
    input_path: str | Path,
    evidence_path: str | Path,
    output_path: str | Path,
    profile_registry: Mapping[str, str],
) -> Mapping[str, Any]:
    raw = load_wordpress_input(input_path)
    evidence_raw = json.loads(Path(evidence_path).read_text(encoding="utf-8"))
    if not isinstance(evidence_raw, Mapping):
        raise LiveBoundaryFail("LIVE_EVIDENCE_SCHEMA_FAIL")

    draft = evidence_raw.get("DRAFT", {}).get("article") if isinstance(evidence_raw.get("DRAFT"), Mapping) else None
    if not isinstance(draft, str) or not draft.strip():
        raise LiveBoundaryFail("LIVE_DRAFT_MISSING")

    # Never trust supplied RULE_CHECK / QUALITY_CHECK verdicts. Recompute them here.
    checked_evidence = dict(evidence_raw)
    checked_evidence["RULE_CHECK"] = build_rule_evidence(raw, draft)
    checked_evidence["QUALITY_CHECK"] = build_quality_evidence(draft)

    engine = build_engine(profile_registry)
    capsule = engine.ingress(raw)
    result = engine.run(capsule, checked_evidence)

    envelope = {
        "contract": "SYSTEM3_WORDPRESS_DRAFT_ENVELOPE_V1",
        "result": result,
        "publish_allowed": False,
        "wordpress_write_allowed": False,
    }
    envelope["envelope_hash"] = _sha256(envelope)

    out = Path(output_path)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(envelope, ensure_ascii=False, sort_keys=True, indent=2), encoding="utf-8")
    return envelope
