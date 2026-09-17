from __future__ import annotations

import hashlib
import json
import re
from pathlib import Path
from typing import Any, Mapping, Sequence

CONTRACT = "SYSTEM4_GLOBAL_WORKSHOP_V1"
REQUEST_FILENAME = "GLOBAL_WORKSHOP_REQUEST.json"
HARD_STOP_MARKERS = (
    "HASH_MISMATCH",
    "SHA_MISMATCH",
    "INTEGRITY",
    "TAMPER",
    "AUTHORITY",
    "SIGNATURE",
    "MISSING",
    "NOT_BOUND",
    "UNBOUND",
    "BINDING_INVALID",
    "PATH_INVALID",
    "SCHEMA_INVALID",
    "CONTRACT_INVALID",
    "PUBLISH",
)
REPAIRABLE_MARKERS = (
    "REPAIR",
    "LANGUAGETOOL",
    "PPM679",
    "CONTENT",
    "DESIGN",
    "LINK",
    "TITLE",
    "CATEGORY",
    "FACT",
    "RESEARCH",
    "REPEATED_SENTENCE",
    "TEMPLATE_REUSE",
    "DUPLICATE_SENTENCE",
)


class WorkshopError(RuntimeError):
    pass


def _canon(value: Any) -> bytes:
    return (json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":")) + "\n").encode("utf-8")


def _sha(value: Any) -> str:
    return hashlib.sha256(_canon(value)).hexdigest()


def _error_code(exc: BaseException) -> str:
    text = str(exc or "").strip()
    return text or exc.__class__.__name__.upper()


def _structured_findings(exc: BaseException, explicit: Sequence[Mapping[str, Any]] | None = None) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    source = explicit
    if source is None:
        candidate = getattr(exc, "findings", None)
        if isinstance(candidate, list):
            source = candidate
    if source is not None:
        for raw in source:
            if isinstance(raw, Mapping):
                row = dict(raw)
                row.setdefault("error_code", _error_code(exc))
                rows.append(row)
    if not rows:
        rows.append({"error_code": _error_code(exc), "reason": _error_code(exc)})
    return rows


def _is_repairable(code: str, findings: Sequence[Mapping[str, Any]]) -> bool:
    text = code.upper() + "|" + "|".join(
        str(row.get("error_code") or "").upper() + "|" + str(row.get("reason") or "").upper()
        for row in findings
    )
    if any(marker in text for marker in HARD_STOP_MARKERS):
        return False
    if any(marker in text for marker in REPAIRABLE_MARKERS):
        return True
    return False


def _repair_targets(findings: Sequence[Mapping[str, Any]]) -> dict[str, list[dict[str, Any]]]:
    targets: dict[str, list[dict[str, Any]]] = {}
    for raw in findings:
        row = dict(raw)
        indexes = row.get("article_indexes")
        if isinstance(indexes, list) and all(isinstance(v, int) and v >= 0 for v in indexes):
            selected = indexes[3:] if len(indexes) >= 4 else indexes
            for index in selected:
                targets.setdefault(str(index), []).append(row)
            continue
        index = row.get("article_index")
        if isinstance(index, int) and index >= 0:
            targets.setdefault(str(index), []).append(row)
    return targets


def build_request(
    stage: str,
    exc: BaseException,
    *,
    findings: Sequence[Mapping[str, Any]] | None = None,
    context: Mapping[str, Any] | None = None,
) -> dict[str, Any]:
    stage_name = str(stage or "UNKNOWN").strip().upper() or "UNKNOWN"
    rows = _structured_findings(exc, findings)
    code = _error_code(exc)
    repairable = _is_repairable(code, rows)
    request = {
        "contract": CONTRACT,
        "status": "REPAIR_REQUIRED" if repairable else "BLOCKED_NON_REPAIRABLE",
        "terminal_at_origin": False,
        "workshop_required": True,
        "repairable": repairable,
        "origin_stage": stage_name,
        "error_code": code,
        "findings": rows,
        "finding_count": len(rows),
        "repair_targets": _repair_targets(rows),
        "context": dict(context or {}),
        "publish_allowed": False,
    }
    request["request_sha256"] = _sha(request)
    return request


def write_request(output_dir: Path, request: Mapping[str, Any]) -> Path:
    out = Path(output_dir)
    out.mkdir(parents=True, exist_ok=True)
    path = out / REQUEST_FILENAME
    path.write_bytes(_canon(dict(request)))
    return path


def route_article_states(request: Mapping[str, Any], state_paths: Sequence[Path]) -> list[int]:
    if request.get("repairable") is not True:
        return []
    targets = request.get("repair_targets")
    if not isinstance(targets, Mapping):
        return []
    changed: list[int] = []
    for raw_index, raw_findings in targets.items():
        try:
            index = int(raw_index)
        except (TypeError, ValueError):
            raise WorkshopError("WORKSHOP_TARGET_INDEX_INVALID")
        if index < 0 or index >= len(state_paths):
            raise WorkshopError("WORKSHOP_TARGET_INDEX_OUT_OF_RANGE:" + str(index))
        if not isinstance(raw_findings, list) or not raw_findings:
            raise WorkshopError("WORKSHOP_TARGET_FINDINGS_INVALID:" + str(index))
        path = Path(state_paths[index])
        try:
            state = json.loads(path.read_text(encoding="utf-8"))
        except Exception as exc:
            raise WorkshopError("WORKSHOP_STATE_READ_FAILED:" + str(index)) from exc
        if not isinstance(state, dict):
            raise WorkshopError("WORKSHOP_STATE_OBJECT_REQUIRED:" + str(index))
        if state.get("phase") not in {"OUTPUT_GATE_REQUIRED", "CHECK_REQUIRED", "REPAIR_REQUIRED"}:
            raise WorkshopError("WORKSHOP_STATE_PHASE_INVALID:" + str(index))
        draft_sha = str(state.get("draft_sha256") or "")
        if not re.fullmatch(r"[0-9a-f]{64}", draft_sha):
            raise WorkshopError("WORKSHOP_DRAFT_SHA_INVALID:" + str(index))
        findings_for_article = [dict(row) for row in raw_findings if isinstance(row, Mapping)]
        if not findings_for_article:
            raise WorkshopError("WORKSHOP_TARGET_FINDINGS_EMPTY:" + str(index))
        state["checks"] = {
            "status": "FAIL",
            "mode": "GLOBAL_WORKSHOP",
            "checker": str(request.get("origin_stage") or "UNKNOWN"),
            "findings": findings_for_article,
            "checked_draft_sha256": draft_sha,
        }
        state["last_error"] = str(findings_for_article[0].get("error_code") or request.get("error_code") or "WORKSHOP_REPAIR_REQUIRED")
        state["phase"] = "REPAIR_REQUIRED"
        state["release_prepared"] = None
        state["released"] = False
        path.write_text(json.dumps(state, ensure_ascii=False, indent=2, sort_keys=True), encoding="utf-8")
        changed.append(index)
    return changed


def capture(
    stage: str,
    exc: BaseException,
    *,
    output_dir: Path | None = None,
    findings: Sequence[Mapping[str, Any]] | None = None,
    context: Mapping[str, Any] | None = None,
    state_paths: Sequence[Path] | None = None,
) -> tuple[dict[str, Any], Path | None, list[int]]:
    request = build_request(stage, exc, findings=findings, context=context)
    changed: list[int] = []
    if state_paths is not None and request.get("repairable") is True:
        changed = route_article_states(request, state_paths)
    path = write_request(output_dir, request) if output_dir is not None else None
    return request, path, changed
