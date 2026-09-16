from __future__ import annotations

import copy
import hashlib
import hmac
import json
import re
import secrets
from typing import Any, Callable, Mapping, Sequence

CONTRACT = "SYSTEM4A_CAPSULE_V3"
SHA_RE = re.compile(r"^[0-9a-f]{64}$")
ARTICLE_KEYS = {"title", "target_keyword", "category", "article_type", "plan_slot"}
PHASES = {
    "RESEARCH_REQUIRED",
    "FACTS_REQUIRED",
    "CONTEXT_REQUIRED",
    "DRAFT_REQUIRED",
    "FULLCHECK_REQUIRED",
    "REPAIR_REQUIRED",
    "ARTICLE_PASS",
}


class CapsuleError(RuntimeError):
    pass


def _canonical(value: Any) -> bytes:
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode("utf-8")


def _sha_text(value: str) -> str:
    return hashlib.sha256(value.encode("utf-8")).hexdigest()


def _require(condition: bool, code: str) -> None:
    if not condition:
        raise CapsuleError(code)


class CapsuleController:
    """One-door supervisor.

    The controller owns route/state only. All Pferde-Atelier fach/design/quality
    decisions are delegated to one injected read-only checker backend.
    """

    REQUIRED_CHECK_METHODS = {
        "research",
        "facts",
        "context",
        "draft",
        "repair",
        "fullcheck",
        "batch",
    }

    def __init__(self, authority_key: bytes, checks: Any):
        _require(isinstance(authority_key, (bytes, bytearray)) and len(authority_key) >= 32, "AUTHORITY_KEY_INVALID")
        for name in self.REQUIRED_CHECK_METHODS:
            _require(callable(getattr(checks, name, None)), "CHECK_BACKEND_INVALID:" + name)
        self._key = bytes(authority_key)
        self._checks = checks
        self._states: dict[str, dict[str, Any]] = {}

    def _seal_payload(self, state: Mapping[str, Any]) -> str:
        payload = {k: v for k, v in state.items() if k != "controller_seal"}
        return hmac.new(self._key, _canonical(payload), hashlib.sha256).hexdigest()

    def _reseal(self, state: dict[str, Any]) -> None:
        state["controller_seal"] = self._seal_payload(state)

    def _verify(self, state: Mapping[str, Any]) -> None:
        seal = state.get("controller_seal")
        _require(isinstance(seal, str) and SHA_RE.fullmatch(seal) is not None, "STATE_SEAL_MISSING")
        _require(hmac.compare_digest(seal, self._seal_payload(state)), "STATE_INTEGRITY_FAIL")
        _require(state.get("contract") == CONTRACT, "STATE_CONTRACT_INVALID")
        _require(state.get("publish_allowed") is False, "PUBLISH_FORBIDDEN")
        _require(state.get("phase") in PHASES, "STATE_PHASE_INVALID")

    def _state(self, capsule_id: str) -> dict[str, Any]:
        _require(isinstance(capsule_id, str) and capsule_id in self._states, "CAPSULE_NOT_FOUND")
        state = self._states[capsule_id]
        self._verify(state)
        return state

    @staticmethod
    def _validate_article(article: Mapping[str, Any]) -> dict[str, str]:
        _require(isinstance(article, Mapping) and set(article) == ARTICLE_KEYS, "ARTICLE_SCHEMA_INVALID")
        out = {k: str(article[k]).strip() for k in ARTICLE_KEYS}
        _require(all(out.values()), "ARTICLE_VALUE_INVALID")
        _require(SHA_RE.fullmatch(out["plan_slot"]) is not None, "PLAN_SLOT_INVALID")
        return out

    @staticmethod
    def _pass(result: Mapping[str, Any], sha_field: str, expected_sha: str, stage: str) -> None:
        _require(isinstance(result, Mapping) and result.get("status") == "PASS", stage + "_NOT_PASS")
        _require(result.get(sha_field) == expected_sha, stage + "_CHECK_HASH_MISMATCH")

    def create(self, article: Mapping[str, Any], source_snapshot_sha256: str, batch_sha256: str) -> str:
        normalized = self._validate_article(article)
        _require(SHA_RE.fullmatch(str(source_snapshot_sha256)) is not None, "SOURCE_SNAPSHOT_SHA_INVALID")
        _require(SHA_RE.fullmatch(str(batch_sha256)) is not None, "BATCH_SHA_INVALID")
        capsule_id = secrets.token_hex(16)
        state = {
            "contract": CONTRACT,
            "capsule_id": capsule_id,
            "article": normalized,
            "source_snapshot_sha256": source_snapshot_sha256,
            "batch_sha256": batch_sha256,
            "phase": "RESEARCH_REQUIRED",
            "publish_allowed": False,
            "revision": 0,
            "research": None,
            "facts": None,
            "production_context": None,
            "draft": None,
            "checks": None,
            "findings": [],
        }
        self._reseal(state)
        self._states[capsule_id] = state
        return capsule_id

    def status(self, capsule_id: str) -> dict[str, Any]:
        state = self._state(capsule_id)
        return {
            "capsule_id": capsule_id,
            "phase": state["phase"],
            "article": copy.deepcopy(state["article"]),
            "revision": state["revision"],
            "findings": copy.deepcopy(state["findings"]),
            "publish_allowed": False,
        }

    def submit_research(self, capsule_id: str, research_text: str) -> None:
        state = self._state(capsule_id)
        _require(state["phase"] == "RESEARCH_REQUIRED", "PHASE_TRANSITION_FORBIDDEN")
        _require(isinstance(research_text, str) and research_text.strip(), "RESEARCH_EMPTY")
        expected = _sha_text(research_text)
        result = self._checks.research(research_text)
        self._pass(result, "sha256", expected, "RESEARCH")
        state["research"] = {"text": research_text, "sha256": expected}
        state["phase"] = "FACTS_REQUIRED"
        state["findings"] = []
        self._reseal(state)

    def submit_facts(self, capsule_id: str, facts_text: str) -> None:
        state = self._state(capsule_id)
        _require(state["phase"] == "FACTS_REQUIRED", "PHASE_TRANSITION_FORBIDDEN")
        _require(isinstance(facts_text, str) and facts_text.strip(), "FACTS_EMPTY")
        expected = _sha_text(facts_text)
        result = self._checks.facts(facts_text, state["research"]["text"])
        self._pass(result, "sha256", expected, "FACTS")
        state["facts"] = {"text": facts_text, "sha256": expected}
        state["phase"] = "CONTEXT_REQUIRED"
        state["findings"] = []
        self._reseal(state)

    def submit_context(self, capsule_id: str, context_text: str) -> None:
        state = self._state(capsule_id)
        _require(state["phase"] == "CONTEXT_REQUIRED", "PHASE_TRANSITION_FORBIDDEN")
        _require(isinstance(context_text, str) and context_text.strip(), "CONTEXT_EMPTY")
        expected = _sha_text(context_text)
        result = self._checks.context(
            context_text,
            article=state["article"],
            source_snapshot_sha256=state["source_snapshot_sha256"],
            research_text=state["research"]["text"],
            facts_text=state["facts"]["text"],
        )
        self._pass(result, "sha256", expected, "CONTEXT")
        fact_pack = result.get("fact_pack")
        plan = result.get("production_plan_item")
        _require(isinstance(fact_pack, dict) and isinstance(plan, dict), "CONTEXT_RESULT_INVALID")
        state["production_context"] = {
            "fact_pack": copy.deepcopy(fact_pack),
            "production_plan_item": copy.deepcopy(plan),
            "input_sha256": expected,
        }
        state["phase"] = "DRAFT_REQUIRED"
        state["findings"] = []
        self._reseal(state)

    def submit_draft(self, capsule_id: str, draft: str) -> None:
        state = self._state(capsule_id)
        _require(state["phase"] in {"DRAFT_REQUIRED", "REPAIR_REQUIRED"}, "PHASE_TRANSITION_FORBIDDEN")
        _require(isinstance(draft, str) and draft.strip(), "DRAFT_EMPTY")
        context = state.get("production_context")
        _require(isinstance(context, dict), "PRODUCTION_CONTEXT_MISSING")
        expected = _sha_text(draft)
        if state["phase"] == "REPAIR_REQUIRED":
            old = state.get("draft")
            _require(isinstance(old, dict) and isinstance(old.get("text"), str), "REPAIR_OLD_DRAFT_MISSING")
            result = self._checks.repair(
                old["text"], draft,
                article_type=state["article"]["article_type"],
                fact_pack=context["fact_pack"],
            )
            self._pass(result, "sha256", expected, "REPAIR")
        else:
            result = self._checks.draft(
                draft,
                article_type=state["article"]["article_type"],
                fact_pack=context["fact_pack"],
            )
            self._pass(result, "sha256", expected, "DRAFT")
        state["draft"] = {"text": draft, "sha256": expected}
        state["revision"] += 1
        state["checks"] = None
        state["phase"] = "FULLCHECK_REQUIRED"
        state["findings"] = []
        self._reseal(state)

    def fullcheck(self, capsule_id: str) -> None:
        state = self._state(capsule_id)
        _require(state["phase"] == "FULLCHECK_REQUIRED", "PHASE_TRANSITION_FORBIDDEN")
        draft = state.get("draft")
        context = state.get("production_context")
        _require(isinstance(draft, dict) and isinstance(context, dict), "FULLCHECK_INPUT_MISSING")
        text = draft.get("text")
        draft_sha = draft.get("sha256")
        _require(isinstance(text, str) and _sha_text(text) == draft_sha, "DRAFT_INTEGRITY_FAIL")
        result = self._checks.fullcheck(
            text,
            article=state["article"],
            source_snapshot_sha256=state["source_snapshot_sha256"],
            fact_pack=context["fact_pack"],
            production_plan_item=context["production_plan_item"],
        )
        _require(isinstance(result, Mapping), "FULLCHECK_RESULT_INVALID")
        _require(result.get("checked_sha256") == draft_sha, "FULLCHECK_HASH_MISMATCH")
        if result.get("status") == "PASS":
            state["checks"] = {"status": "PASS", "evidence": copy.deepcopy(result.get("evidence"))}
            state["phase"] = "ARTICLE_PASS"
            state["findings"] = []
        elif result.get("status") == "FAIL":
            findings = result.get("findings")
            _require(isinstance(findings, list) and findings, "FAIL_FINDINGS_REQUIRED")
            state["checks"] = {
                "status": "FAIL",
                "checker": result.get("checker"),
                "findings": copy.deepcopy(findings),
            }
            state["phase"] = "REPAIR_REQUIRED"
            state["findings"] = copy.deepcopy(findings)
        else:
            raise CapsuleError("FULLCHECK_STATUS_INVALID")
        self._reseal(state)

    def export_article(self, capsule_id: str) -> dict[str, Any]:
        state = self._state(capsule_id)
        _require(state["phase"] == "ARTICLE_PASS", "OUTPUT_GATE_CLOSED")
        _require(isinstance(state.get("checks"), dict) and state["checks"].get("status") == "PASS", "OUTPUT_CHECK_MISSING")
        draft = state["draft"]
        return {
            "article": copy.deepcopy(state["article"]),
            "body": draft["text"],
            "body_sha256": draft["sha256"],
            "revision": state["revision"],
            "production_context": copy.deepcopy(state["production_context"]),
            "production_evidence": copy.deepcopy(state["checks"].get("evidence")),
            "publish_allowed": False,
        }

    def batch_check(self, capsule_ids: Sequence[str]) -> dict[str, Any]:
        _require(isinstance(capsule_ids, Sequence) and len(capsule_ids) >= 1, "BATCH_INPUT_INVALID")
        bodies = []
        for capsule_id in capsule_ids:
            state = self._state(capsule_id)
            _require(state["phase"] == "ARTICLE_PASS", "BATCH_ARTICLE_NOT_PASS")
            bodies.append(state["draft"]["text"])
        result = self._checks.batch(bodies)
        _require(isinstance(result, Mapping) and result.get("status") == "PASS", "BATCH_NOT_PASS")
        return copy.deepcopy(dict(result))

    def checkpoint(self, capsule_id: str) -> bytes:
        state = self._state(capsule_id)
        return _canonical(state)

    def restore(self, checkpoint: bytes) -> str:
        _require(isinstance(checkpoint, (bytes, bytearray)), "CHECKPOINT_INVALID")
        try:
            state = json.loads(bytes(checkpoint).decode("utf-8"))
        except Exception as exc:
            raise CapsuleError("CHECKPOINT_JSON_INVALID") from exc
        _require(isinstance(state, dict), "CHECKPOINT_OBJECT_REQUIRED")
        self._verify(state)
        capsule_id = state.get("capsule_id")
        _require(isinstance(capsule_id, str) and capsule_id, "CAPSULE_ID_INVALID")
        _require(capsule_id not in self._states, "CAPSULE_ALREADY_LOADED")
        self._states[capsule_id] = state
        return capsule_id

    def next_work_request(self, capsule_id: str) -> dict[str, Any] | None:
        state = self._state(capsule_id)
        phase = state["phase"]
        article = copy.deepcopy(state["article"])
        if phase == "RESEARCH_REQUIRED":
            return {"task": "research", "article": article}
        if phase == "FACTS_REQUIRED":
            return {"task": "facts", "article": article, "research": state["research"]["text"]}
        if phase == "CONTEXT_REQUIRED":
            return {
                "task": "context",
                "article": article,
                "source_snapshot_sha256": state["source_snapshot_sha256"],
                "research": state["research"]["text"],
                "facts": state["facts"]["text"],
            }
        if phase == "DRAFT_REQUIRED":
            return {
                "task": "draft",
                "article": article,
                "research": state["research"]["text"],
                "facts": state["facts"]["text"],
                "production_context": copy.deepcopy(state["production_context"]),
            }
        if phase == "REPAIR_REQUIRED":
            return {
                "task": "repair",
                "article": article,
                "research": state["research"]["text"],
                "facts": state["facts"]["text"],
                "production_context": copy.deepcopy(state["production_context"]),
                "draft": state["draft"]["text"],
                "findings": copy.deepcopy(state["findings"]),
            }
        if phase in {"FULLCHECK_REQUIRED", "ARTICLE_PASS"}:
            return None
        raise CapsuleError("PHASE_HAS_NO_WORK_REQUEST")

    def apply_worker_result(self, capsule_id: str, result: Mapping[str, Any]) -> None:
        state = self._state(capsule_id)
        _require(isinstance(result, Mapping) and set(result) == {"content"}, "WORKER_RESULT_SCHEMA_INVALID")
        content = result.get("content")
        _require(isinstance(content, str) and content.strip(), "WORKER_CONTENT_EMPTY")
        phase = state["phase"]
        if phase == "RESEARCH_REQUIRED":
            self.submit_research(capsule_id, content)
        elif phase == "FACTS_REQUIRED":
            self.submit_facts(capsule_id, content)
        elif phase == "CONTEXT_REQUIRED":
            self.submit_context(capsule_id, content)
        elif phase in {"DRAFT_REQUIRED", "REPAIR_REQUIRED"}:
            self.submit_draft(capsule_id, content)
        else:
            raise CapsuleError("WORKER_RESULT_NOT_ALLOWED_IN_PHASE")

    def run_automatic(self, capsule_id: str, worker: Callable[[Mapping[str, Any]], Mapping[str, Any]], max_rounds: int = 20) -> dict[str, Any]:
        _require(callable(worker), "WORKER_INVALID")
        _require(isinstance(max_rounds, int) and 1 <= max_rounds <= 100, "MAX_ROUNDS_INVALID")
        rounds = 0
        while rounds < max_rounds:
            state = self._state(capsule_id)
            if state["phase"] == "ARTICLE_PASS":
                return self.export_article(capsule_id)
            if state["phase"] == "FULLCHECK_REQUIRED":
                self.fullcheck(capsule_id)
                continue
            request = self.next_work_request(capsule_id)
            _require(request is not None, "WORK_REQUEST_MISSING")
            result = worker(copy.deepcopy(request))
            self.apply_worker_result(capsule_id, result)
            rounds += 1
        raise CapsuleError("AUTOMATION_ROUND_LIMIT")
