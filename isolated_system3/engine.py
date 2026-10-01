from __future__ import annotations

import copy
import hashlib
import json
from dataclasses import dataclass
from typing import Any, Dict, Mapping, Tuple


FIXED_STATES: Tuple[str, ...] = (
    "INGRESS",
    "CAPSULE",
    "RESEARCH",
    "FACT_CHECK",
    "DRAFT",
    "LANGUAGE",
    "RULE_CHECK",
    "QUALITY_CHECK",
    "OUTPUT_GATE",
    "DONE",
)

FORBIDDEN_EXTERNAL_KEYS = {
    "next_state",
    "route",
    "rules",
    "ruleset_ref",
    "toolchain_ref",
    "prompt",
    "system_prompt",
    "publish_allowed",
    "article_type",
    "workflow",
}

REQUIRED_INPUT_KEYS = {
    "article_id",
    "article_type",
    "source_payload",
    "ruleset_ref",
    "toolchain_ref",
}


class System3Fail(RuntimeError):
    pass


def _canonical_json(value: Any) -> str:
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False)


def _sha256(value: Any) -> str:
    return hashlib.sha256(_canonical_json(value).encode("utf-8")).hexdigest()


def _scan_forbidden_external_keys(value: Any, path: str = "source_payload") -> None:
    if isinstance(value, Mapping):
        for key, child in value.items():
            if key in FORBIDDEN_EXTERNAL_KEYS:
                raise System3Fail(f"EXTERNAL_CONTROL_FIELD_BLOCKED:{path}.{key}")
            _scan_forbidden_external_keys(child, f"{path}.{key}")
    elif isinstance(value, list):
        for index, child in enumerate(value):
            _scan_forbidden_external_keys(child, f"{path}[{index}]")


@dataclass(frozen=True)
class ArticleProfile:
    article_type: str
    profile_ref: str


@dataclass(frozen=True)
class Capsule:
    payload: Dict[str, Any]
    capsule_hash: str

    @classmethod
    def create(cls, payload: Dict[str, Any]) -> "Capsule":
        frozen_copy = copy.deepcopy(payload)
        return cls(payload=frozen_copy, capsule_hash=_sha256(frozen_copy))

    def verify(self) -> None:
        if _sha256(self.payload) != self.capsule_hash:
            raise System3Fail("CAPSULE_INTEGRITY_FAIL")


class System3Engine:
    """Single-process prototype. Routing is hard-coded; model/chat has no routing authority."""

    def __init__(self, profiles: Mapping[str, ArticleProfile]):
        self._profiles = dict(profiles)

    @property
    def states(self) -> Tuple[str, ...]:
        return FIXED_STATES

    def ingress(self, raw: Mapping[str, Any]) -> Capsule:
        if set(raw.keys()) != REQUIRED_INPUT_KEYS:
            missing = sorted(REQUIRED_INPUT_KEYS - set(raw.keys()))
            extra = sorted(set(raw.keys()) - REQUIRED_INPUT_KEYS)
            raise System3Fail(f"INGRESS_SCHEMA_FAIL:missing={missing}:extra={extra}")

        article_type = raw["article_type"]
        if article_type not in self._profiles:
            raise System3Fail("UNKNOWN_ARTICLE_TYPE")

        if not isinstance(raw["source_payload"], Mapping):
            raise System3Fail("SOURCE_PAYLOAD_SCHEMA_FAIL")
        _scan_forbidden_external_keys(raw["source_payload"])

        if not isinstance(raw["ruleset_ref"], str) or not raw["ruleset_ref"].strip():
            raise System3Fail("RULESET_REF_MISSING")
        if not isinstance(raw["toolchain_ref"], str) or not raw["toolchain_ref"].strip():
            raise System3Fail("TOOLCHAIN_REF_MISSING")

        profile = self._profiles[article_type]
        capsule_payload = {
            "article_id": raw["article_id"],
            "article_type": article_type,
            "profile_ref": profile.profile_ref,
            "ruleset_ref": raw["ruleset_ref"],
            "toolchain_ref": raw["toolchain_ref"],
            "source_payload": copy.deepcopy(raw["source_payload"]),
            "publish_allowed": False,
            "process_version": "SYSTEM3_ONE_PROCESS_V1",
        }
        return Capsule.create(capsule_payload)

    def run(self, capsule: Capsule, stage_evidence: Mapping[str, Any]) -> Dict[str, Any]:
        capsule.verify()

        required_evidence = {
            "RESEARCH",
            "FACT_CHECK",
            "DRAFT",
            "LANGUAGE",
            "RULE_CHECK",
            "QUALITY_CHECK",
        }
        missing = sorted(required_evidence - set(stage_evidence.keys()))
        if missing:
            raise System3Fail(f"EVIDENCE_MISSING:{','.join(missing)}")

        trace = ["INGRESS", "CAPSULE"]
        for state in FIXED_STATES[2:-2]:
            evidence = stage_evidence[state]
            if not isinstance(evidence, Mapping):
                raise System3Fail(f"{state}_EVIDENCE_SCHEMA_FAIL")
            if evidence.get("status") != "PASS":
                raise System3Fail(f"{state}_FAIL")
            if "next_state" in evidence or "route" in evidence:
                raise System3Fail(f"{state}_ROUTING_AUTHORITY_BLOCKED")
            trace.append(state)

        draft = stage_evidence["DRAFT"].get("article")
        if not isinstance(draft, str) or not draft.strip():
            raise System3Fail("DRAFT_ARTICLE_MISSING")

        rule_check = stage_evidence["RULE_CHECK"]
        if rule_check.get("all_rules_exact") is not True:
            raise System3Fail("RULE_CONFORMITY_FAIL")

        quality = stage_evidence["QUALITY_CHECK"]
        if quality.get("quality_floor_pass") is not True:
            raise System3Fail("QUALITY_FLOOR_FAIL")

        trace.append("OUTPUT_GATE")
        capsule.verify()

        result = {
            "contract": "SYSTEM3_OUTPUT_V1",
            "article_id": capsule.payload["article_id"],
            "article_type": capsule.payload["article_type"],
            "profile_ref": capsule.payload["profile_ref"],
            "ruleset_ref": capsule.payload["ruleset_ref"],
            "toolchain_ref": capsule.payload["toolchain_ref"],
            "capsule_hash": capsule.capsule_hash,
            "article": draft,
            "rule_conformity": True,
            "quality_floor_pass": True,
            "publish_allowed": False,
            "trace": trace + ["DONE"],
        }
        result["output_hash"] = _sha256(result)
        return result
