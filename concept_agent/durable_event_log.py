#!/usr/bin/env python3
from __future__ import annotations

import argparse
import base64
import gzip
import hashlib
import json
import re
import sys
import tempfile
import urllib.parse
import urllib.request
from pathlib import Path
from typing import Any

HERE = Path(__file__).resolve().parent
REPO = HERE.parent
SYSTEM4 = REPO / "isolated_system4"
if str(SYSTEM4) not in sys.path:
    sys.path.insert(0, str(SYSTEM4))

import intake_bridge
import production_bridge
import progress_guard
import universal_reentry_guard

EVENT_CONTRACT = "CONCEPT_AGENT_DURABLE_EVENT_V1"
TRUSTED_EVENT_AUTHOR = "chatgpt-codex-connector[bot]"
TRUSTED_START_AUTHOR = "github-actions[bot]"
SNAPSHOT_REF = "concept_agent/current/PSERC_METADATA_SNAPSHOT.json"
MAX_COMMENT_BYTES = 60000
SHA_RE = re.compile(r"^[0-9a-f]{64}$")


class Blocked(RuntimeError):
    pass


def canon(value: Any) -> bytes:
    return json.dumps(
        value,
        ensure_ascii=False,
        sort_keys=True,
        separators=(",", ":"),
    ).encode("utf-8")


def stable(value: Any) -> str:
    return hashlib.sha256(canon(value)).hexdigest()


def sha(raw: bytes) -> str:
    return hashlib.sha256(raw).hexdigest()


def load_json(path: Path) -> dict[str, Any]:
    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise Blocked("JSON_OBJECT_REQUIRED:" + str(path))
    return value


def _current_batch() -> dict[str, Any]:
    snapshot = load_json(REPO / SNAPSHOT_REF)
    intake = intake_bridge.prepare(snapshot)
    batch = str(intake.get("batch_sha256") or "")
    count = intake.get("item_count")
    if not SHA_RE.fullmatch(batch):
        raise Blocked("DURABLE_EVENT_CURRENT_BATCH_INVALID")
    if not isinstance(count, int) or isinstance(count, bool) or count < 1:
        raise Blocked("DURABLE_EVENT_CURRENT_COUNT_INVALID")
    if intake.get("publish_allowed") is not False:
        raise Blocked("DURABLE_EVENT_CURRENT_PUBLISH_INVALID")
    return {
        "batch_sha256": batch,
        "item_count": count,
        "metadata_snapshot_ref": SNAPSHOT_REF,
        "publish_allowed": False,
    }


def _api_json(url: str):
    req = urllib.request.Request(
        url,
        headers={
            "Accept": "application/vnd.github+json",
            "User-Agent": "pferdeatelier-concept-agent-durable-event",
            "X-GitHub-Api-Version": "2022-11-28",
        },
    )
    try:
        with urllib.request.urlopen(req, timeout=30) as fh:
            return json.load(fh)
    except Exception as exc:
        raise Blocked("DURABLE_EVENT_GITHUB_READ_FAILED:" + str(exc)) from exc


def _discover_issue(batch_sha256: str) -> int:
    title = "TEXT_START_BATCH_CLAIM:" + batch_sha256
    query = 'repo:hallo-netizen/affiliate-pferdeportal in:title "' + title + '"'
    url = (
        "https://api.github.com/search/issues?q="
        + urllib.parse.quote(query, safe="")
        + "&per_page=100"
    )
    value = _api_json(url)
    items = value.get("items") if isinstance(value, dict) else None
    if not isinstance(items, list):
        raise Blocked("DURABLE_EVENT_CLAIM_SEARCH_INVALID")
    exact = [
        row for row in items
        if isinstance(row, dict)
        and row.get("title") == title
        and "pull_request" not in row
    ]
    if len(exact) != 1:
        raise Blocked("DURABLE_EVENT_CLAIM_NOT_EXACT:" + str(len(exact)))
    number = exact[0].get("number")
    if not isinstance(number, int) or isinstance(number, bool) or number < 1:
        raise Blocked("DURABLE_EVENT_CLAIM_NUMBER_INVALID")
    return number


def _api_comments(issue_number: int) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    page = 1
    while True:
        url = (
            "https://api.github.com/repos/hallo-netizen/affiliate-pferdeportal/issues/"
            + str(issue_number)
            + "/comments?per_page=100&page="
            + str(page)
        )
        value = _api_json(url)
        if not isinstance(value, list):
            raise Blocked("DURABLE_EVENT_COMMENT_LIST_INVALID")
        rows.extend(x for x in value if isinstance(x, dict))
        if len(value) < 100:
            return rows
        page += 1


def _comments(path: Path | None, issue_number: int) -> list[dict[str, Any]]:
    if path is None:
        return _api_comments(issue_number)
    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, list):
        raise Blocked("DURABLE_EVENT_TEST_COMMENT_LIST_INVALID")
    return [x for x in value if isinstance(x, dict)]


def _login(row: dict[str, Any]) -> str:
    user = row.get("user")
    return str(user.get("login") if isinstance(user, dict) else "")


def _anchor(rows: list[dict[str, Any]], cfg: dict[str, Any]) -> str:
    matches = []
    for row in rows:
        if _login(row) != TRUSTED_START_AUTHOR:
            continue
        body = str(row.get("body") or "")
        lines = body.strip().splitlines()
        if not lines or lines[0] != "TEXT_START_MACHINE_READY":
            continue
        fields = {}
        for line in lines[1:]:
            if ": " in line:
                key, value = line.split(": ", 1)
                fields[key] = value
        if (
            str(fields.get("TARGET_ACTION_RUN_ID") or "").isdigit()
            and str(fields.get("SOURCE_RUN_ID") or "").isdigit()
            and fields.get("BATCH_SHA256") == cfg["batch_sha256"]
            and fields.get("PUBLISH") == "NO"
        ):
            matches.append((row, body.strip()))
    if len(matches) != 1:
        raise Blocked("DURABLE_EVENT_MACHINE_READY_ANCHOR_NOT_EXACT:" + str(len(matches)))
    row, body = matches[0]
    return stable(
        {
            "comment_id": row.get("id"),
            "author": TRUSTED_START_AUTHOR,
            "body": body,
        }
    )


def _decode_payload(event: dict[str, Any]) -> bytes:
    kind = event.get("payload_kind")
    if kind not in {"UTF8_GZIP_BASE64", "JSON_GZIP_BASE64"}:
        raise Blocked("DURABLE_EVENT_PAYLOAD_KIND_INVALID")
    encoded = event.get("payload_b64")
    if not isinstance(encoded, str) or not encoded:
        raise Blocked("DURABLE_EVENT_PAYLOAD_MISSING")
    try:
        raw = gzip.decompress(base64.b64decode(encoded.encode("ascii"), validate=True))
    except Exception as exc:
        raise Blocked("DURABLE_EVENT_PAYLOAD_DECODE_INVALID") from exc
    if len(raw) != event.get("payload_size_bytes") or sha(raw) != event.get("payload_sha256"):
        raise Blocked("DURABLE_EVENT_PAYLOAD_INTEGRITY_FAIL")
    if kind == "UTF8_GZIP_BASE64":
        try:
            raw.decode("utf-8")
        except UnicodeDecodeError as exc:
            raise Blocked("DURABLE_EVENT_PAYLOAD_UTF8_INVALID") from exc
    else:
        try:
            value = json.loads(raw.decode("utf-8"))
        except Exception as exc:
            raise Blocked("DURABLE_EVENT_PAYLOAD_JSON_INVALID") from exc
        if not isinstance(value, dict):
            raise Blocked("DURABLE_EVENT_PAYLOAD_JSON_OBJECT_REQUIRED")
    return raw


def payload_json(event: dict[str, Any]) -> dict[str, Any]:
    if event.get("payload_kind") != "JSON_GZIP_BASE64":
        raise Blocked("DURABLE_EVENT_JSON_PAYLOAD_REQUIRED")
    value = json.loads(_decode_payload(event).decode("utf-8"))
    if not isinstance(value, dict):
        raise Blocked("DURABLE_EVENT_JSON_PAYLOAD_OBJECT_REQUIRED")
    return value


def payload_text(event: dict[str, Any]) -> str:
    if event.get("payload_kind") != "UTF8_GZIP_BASE64":
        raise Blocked("DURABLE_EVENT_TEXT_PAYLOAD_REQUIRED")
    return _decode_payload(event).decode("utf-8")


def _parse_event_comment(row: dict[str, Any], batch_sha256: str) -> dict[str, Any] | None:
    body = str(row.get("body") or "")
    if not body.startswith(EVENT_CONTRACT + "\n"):
        return None
    if _login(row) != TRUSTED_EVENT_AUTHOR:
        return None
    line = body.splitlines()[1] if len(body.splitlines()) >= 2 else ""
    try:
        event = json.loads(line)
    except Exception as exc:
        raise Blocked("DURABLE_EVENT_JSON_INVALID:" + str(row.get("id"))) from exc
    if not isinstance(event, dict) or event.get("contract") != EVENT_CONTRACT:
        raise Blocked("DURABLE_EVENT_CONTRACT_INVALID")
    if event.get("batch_sha256") != batch_sha256:
        raise Blocked("DURABLE_EVENT_BATCH_MISMATCH")
    if event.get("publish_allowed") is not False:
        raise Blocked("DURABLE_EVENT_PUBLISH_TRUE")
    sequence = event.get("sequence")
    if not isinstance(sequence, int) or isinstance(sequence, bool) or sequence < 1:
        raise Blocked("DURABLE_EVENT_SEQUENCE_INVALID")
    previous = event.get("previous_event_sha256")
    if not isinstance(previous, str) or not SHA_RE.fullmatch(previous):
        raise Blocked("DURABLE_EVENT_PREVIOUS_HASH_INVALID")
    action = event.get("executed_action")
    if not isinstance(action, dict) or not isinstance(action.get("action"), str):
        raise Blocked("DURABLE_EVENT_ACTION_INVALID")
    _decode_payload(event)
    core = dict(event)
    declared = core.pop("event_sha256", None)
    if not isinstance(declared, str) or not SHA_RE.fullmatch(declared):
        raise Blocked("DURABLE_EVENT_HASH_INVALID")
    if stable(core) != declared:
        raise Blocked("DURABLE_EVENT_HASH_MISMATCH")
    event["_comment_id"] = row.get("id")
    return event


def event_chain(rows: list[dict[str, Any]], cfg: dict[str, Any]) -> tuple[str, list[dict[str, Any]]]:
    anchor = _anchor(rows, cfg)
    by_seq: dict[int, dict[str, Any]] = {}
    for row in rows:
        event = _parse_event_comment(row, cfg["batch_sha256"])
        if event is None:
            continue
        seq = event["sequence"]
        if seq in by_seq:
            if by_seq[seq]["event_sha256"] != event["event_sha256"]:
                raise Blocked("DURABLE_EVENT_SEQUENCE_AMBIGUOUS:" + str(seq))
            continue
        by_seq[seq] = event

    if not by_seq:
        return anchor, []

    highest = max(by_seq)
    if set(by_seq) != set(range(1, highest + 1)):
        raise Blocked("DURABLE_EVENT_SEQUENCE_GAP")
    ordered = [by_seq[i] for i in range(1, highest + 1)]
    previous = anchor
    for event in ordered:
        if event["previous_event_sha256"] != previous:
            raise Blocked("DURABLE_EVENT_CHAIN_BROKEN:" + str(event["sequence"]))
        previous = event["event_sha256"]
    return anchor, ordered


def _research_sources(event: dict[str, Any], index: int) -> list[dict[str, Any]]:
    payload = payload_json(event)
    sources = payload.get("sources")
    if not isinstance(sources, list) or not sources:
        raise Blocked("DURABLE_EVENT_RESEARCH_SOURCES_EMPTY:" + str(index))
    checked = []
    seen = set()
    for pos, source in enumerate(sources):
        if not isinstance(source, dict):
            raise Blocked("DURABLE_EVENT_RESEARCH_SOURCE_INVALID")
        required = ("source_id", "source_title", "source_url", "evidence", "snapshot_sha256")
        if any(not isinstance(source.get(k), str) or not source[k].strip() for k in required):
            raise Blocked("DURABLE_EVENT_RESEARCH_SOURCE_FIELD_INVALID")
        if source["source_id"] in seen:
            raise Blocked("DURABLE_EVENT_RESEARCH_SOURCE_DUPLICATE")
        seen.add(source["source_id"])
        if intake_bridge._forbidden_research_url(source["source_url"]):
            raise Blocked("DURABLE_EVENT_RESEARCH_OWN_DOMAIN_FORBIDDEN")
        if hashlib.sha256(source["evidence"].encode("utf-8")).hexdigest() != source["snapshot_sha256"]:
            raise Blocked("DURABLE_EVENT_RESEARCH_SOURCE_HASH_MISMATCH")
        checked.append({k: source[k] for k in required})
    return checked


def _snapshot_and_intake(cfg: dict[str, Any]) -> tuple[dict[str, Any], dict[str, Any]]:
    snapshot = load_json(REPO / cfg["metadata_snapshot_ref"])
    intake = intake_bridge.prepare(snapshot)
    if intake.get("batch_sha256") != cfg["batch_sha256"] or intake.get("item_count") != cfg["item_count"]:
        raise Blocked("DURABLE_EVENT_INTAKE_CURRENT_MISMATCH")
    return snapshot, intake


def _research_action(intake: dict[str, Any], index: int) -> dict[str, Any]:
    row = intake["items"][index]
    return {
        "action": "RESEARCH_ITEM",
        "item_index": index,
        "plan_slot": row["plan_slot"],
        "identity_sha256": row["identity_sha256"],
        "canonical_bound_worker_only": True,
        "free_chat_execution": False,
        "fallback_route": "STOP",
    }


def _build_production(cfg: dict[str, Any], research_events: list[dict[str, Any]]):
    snapshot, intake = _snapshot_and_intake(cfg)
    rows = []
    for index, event in enumerate(research_events):
        expected = _research_action(intake, index)
        if event.get("executed_action") != expected:
            raise Blocked("DURABLE_EVENT_RESEARCH_ACTION_MISMATCH:" + str(index))
        rows.append(
            {
                "item_index": index,
                "plan_slot": intake["items"][index]["plan_slot"],
                "sources": _research_sources(event, index),
            }
        )
    submission = {
        "contract": intake_bridge.RESEARCH_SUBMISSION_CONTRACT,
        "batch_sha256": intake["batch_sha256"],
        "item_count": intake["item_count"],
        "items": rows,
    }
    bound = intake_bridge.bind_research(intake, submission)
    binding = production_bridge.build(snapshot, intake, bound)
    checkpoint = production_bridge.initial_checkpoint(binding)
    return intake, bound, binding, checkpoint


def _materialize_draft(state: dict[str, Any], root: Path, index: int) -> Path:
    rows = state.get("drafts")
    if not isinstance(rows, list):
        raise Blocked("DURABLE_EVENT_DRAFTS_MISSING")
    found = [x for x in rows if isinstance(x, dict) and x.get("item_index") == index]
    if len(found) != 1:
        raise Blocked("DURABLE_EVENT_CURRENT_DRAFT_MISSING")
    row = found[0]
    path = root / row["filename"]
    path.write_text(row["content_utf8"], encoding="utf-8")
    if progress_guard.file_sha(path) != row["draft_sha256"]:
        raise Blocked("DURABLE_EVENT_CURRENT_DRAFT_HASH_MISMATCH")
    return path


def replay_production(
    binding: dict[str, Any],
    checkpoint: dict[str, Any],
    events: list[dict[str, Any]],
) -> dict[str, Any]:
    state = checkpoint
    with tempfile.TemporaryDirectory(prefix="concept-agent-event-replay-") as td:
        root = Path(td)
        for event in events:
            expected = progress_guard.expected_action(binding, state)
            if event.get("executed_action") != expected:
                raise Blocked("DURABLE_EVENT_PRODUCTION_ACTION_MISMATCH:" + str(event["sequence"]))
            decision = universal_reentry_guard.build(binding, state)
            action = expected["action"]
            index = expected.get("item_index")
            if action == "WRITE_DRAFT":
                text = payload_text(event)
                path = root / f"{index:02d}_{binding['items'][index]['identity']['plan_slot']}.md"
                path.write_text(text, encoding="utf-8")
                state = progress_guard.record_draft(binding, state, decision, index, path)
            elif action == "RUN_CHECKER":
                result = payload_json(event)
                path = _materialize_draft(state, root, index)
                state = progress_guard.record_check(
                    binding,
                    state,
                    decision,
                    index,
                    expected["checker"],
                    result,
                    path,
                )
            elif action == "REPAIR_DRAFT":
                text = payload_text(event)
                path = _materialize_draft(state, root, index)
                path.write_text(text, encoding="utf-8")
                state = progress_guard.replace_draft(binding, state, decision, index, path)
            elif action == "RUN_PSERC":
                state = progress_guard.record_batch_stage(
                    binding, state, decision, "PSERC", payload_json(event)
                )
            elif action == "RUN_ENDSTEMPEL":
                state = progress_guard.record_batch_stage(
                    binding, state, decision, "ENDSTEMPEL", payload_json(event)
                )
            else:
                raise Blocked("DURABLE_EVENT_UNEXPECTED_TERMINAL_ACTION:" + action)
    return state


def derive(rows: list[dict[str, Any]], cfg: dict[str, Any] | None = None) -> dict[str, Any]:
    cfg = dict(cfg or _current_batch())
    anchor, events = event_chain(rows, cfg)
    _, intake = _snapshot_and_intake(cfg)

    research_events = []
    pos = 0
    while pos < len(events) and events[pos]["executed_action"].get("action") == "RESEARCH_ITEM":
        research_events.append(events[pos])
        pos += 1

    if len(research_events) > cfg["item_count"]:
        raise Blocked("DURABLE_EVENT_TOO_MANY_RESEARCH_EVENTS")

    for index, event in enumerate(research_events):
        if event["executed_action"] != _research_action(intake, index):
            raise Blocked("DURABLE_EVENT_RESEARCH_ORDER_INVALID:" + str(index))
        _research_sources(event, index)

    if len(research_events) < cfg["item_count"]:
        if pos != len(events):
            raise Blocked("DURABLE_EVENT_PRODUCTION_BEFORE_RESEARCH_BOUND")
        action = _research_action(intake, len(research_events))
        return {
            "status": "IN_PROGRESS",
            "batch_sha256": cfg["batch_sha256"],
            "sequence": len(events),
            "last_event_sha256": events[-1]["event_sha256"] if events else anchor,
            "stage": "RESEARCH",
            "allowed_action": action,
            "production_binding": None,
            "checkpoint": None,
            "publish_allowed": False,
        }

    _, bound, binding, checkpoint = _build_production(cfg, research_events)
    state = replay_production(binding, checkpoint, events[pos:])
    action = progress_guard.expected_action(binding, state)
    return {
        "status": "STOPPED" if action["action"] == "STOP" else "IN_PROGRESS",
        "batch_sha256": cfg["batch_sha256"],
        "sequence": len(events),
        "last_event_sha256": events[-1]["event_sha256"] if events else anchor,
        "stage": universal_reentry_guard.build(binding, state)["outer_stage"],
        "allowed_action": action,
        "research_binding_sha256": bound["research_binding_sha256"],
        "production_binding": binding,
        "checkpoint": state,
        "publish_allowed": False,
    }


def _encode_payload(kind: str, raw: bytes) -> dict[str, Any]:
    compressed = gzip.compress(raw, compresslevel=9, mtime=0)
    return {
        "payload_kind": kind,
        "payload_b64": base64.b64encode(compressed).decode("ascii"),
        "payload_sha256": sha(raw),
        "payload_size_bytes": len(raw),
    }


def make_event(current: dict[str, Any], action: dict[str, Any], kind: str, raw: bytes) -> dict[str, Any]:
    if action != current["allowed_action"]:
        raise Blocked("DURABLE_EVENT_SEAL_ACTION_NOT_CURRENT")
    event = {
        "contract": EVENT_CONTRACT,
        "batch_sha256": current["batch_sha256"],
        "sequence": current["sequence"] + 1,
        "previous_event_sha256": current["last_event_sha256"],
        "executed_action": action,
        **_encode_payload(kind, raw),
        "publish_allowed": False,
    }
    event["event_sha256"] = stable(event)
    body = EVENT_CONTRACT + "\n" + json.dumps(
        event, ensure_ascii=False, sort_keys=True, separators=(",", ":")
    )
    if len(body.encode("utf-8")) > MAX_COMMENT_BYTES:
        raise Blocked("DURABLE_EVENT_COMMENT_TOO_LARGE")
    return event


def _current(comments_path: Path | None) -> tuple[list[dict[str, Any]], dict[str, Any]]:
    cfg = _current_batch()
    if comments_path is None:
        issue_number = _discover_issue(cfg["batch_sha256"])
        rows = _comments(None, issue_number)
    else:
        rows = _comments(comments_path, 0)
    return rows, derive(rows, cfg)


def _write_current(out: Path, current: dict[str, Any]) -> None:
    out.mkdir(parents=True, exist_ok=True)
    visible = {
        k: v
        for k, v in current.items()
        if k not in {"production_binding", "checkpoint"}
    }
    (out / "CURRENT_DURABLE_ACTION.json").write_text(
        json.dumps(visible, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    if isinstance(current.get("production_binding"), dict):
        (out / "CURRENT_PRODUCTION_BINDING.json").write_text(
            json.dumps(current["production_binding"], ensure_ascii=False, indent=2) + "\n",
            encoding="utf-8",
        )
    if isinstance(current.get("checkpoint"), dict):
        (out / "CURRENT_PROGRESS_CHECKPOINT.json").write_text(
            json.dumps(current["checkpoint"], ensure_ascii=False, indent=2) + "\n",
            encoding="utf-8",
        )
        action = current["allowed_action"]
        if action.get("action") in {"RUN_CHECKER", "REPAIR_DRAFT"}:
            index = action["item_index"]
            with tempfile.TemporaryDirectory() as td:
                path = _materialize_draft(current["checkpoint"], Path(td), index)
                (out / path.name).write_bytes(path.read_bytes())


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--comments-json")
    sub = ap.add_subparsers(dest="cmd", required=True)

    p = sub.add_parser("current")
    p.add_argument("--out", required=True)

    p = sub.add_parser("seal-research")
    p.add_argument("--sources-json", required=True)

    p = sub.add_parser("seal-draft")
    p.add_argument("--draft", required=True)

    p = sub.add_parser("seal-check")
    p.add_argument("--result-json", required=True)

    p = sub.add_parser("seal-repair")
    p.add_argument("--draft", required=True)

    p = sub.add_parser("seal-batch-stage")
    p.add_argument("--result-json", required=True)

    args = ap.parse_args(argv)
    comments_path = Path(args.comments_json) if args.comments_json else None

    try:
        _, current = _current(comments_path)
        if args.cmd == "current":
            _write_current(Path(args.out), current)
            print(json.dumps({
                "status": current["status"],
                "sequence": current["sequence"],
                "stage": current["stage"],
                "allowed_action": current["allowed_action"],
                "publish_allowed": False,
            }, ensure_ascii=False, sort_keys=True))
            return 0

        action = current["allowed_action"]
        name = action.get("action")

        if args.cmd == "seal-research":
            if name != "RESEARCH_ITEM":
                raise Blocked("DURABLE_EVENT_RESEARCH_NOT_ALLOWED")
            payload = load_json(Path(args.sources_json))
            event = make_event(current, action, "JSON_GZIP_BASE64", canon(payload))
        elif args.cmd == "seal-draft":
            if name != "WRITE_DRAFT":
                raise Blocked("DURABLE_EVENT_DRAFT_NOT_ALLOWED")
            event = make_event(current, action, "UTF8_GZIP_BASE64", Path(args.draft).read_bytes())
        elif args.cmd == "seal-check":
            if name != "RUN_CHECKER":
                raise Blocked("DURABLE_EVENT_CHECK_NOT_ALLOWED")
            event = make_event(current, action, "JSON_GZIP_BASE64", canon(load_json(Path(args.result_json))))
        elif args.cmd == "seal-repair":
            if name != "REPAIR_DRAFT":
                raise Blocked("DURABLE_EVENT_REPAIR_NOT_ALLOWED")
            event = make_event(current, action, "UTF8_GZIP_BASE64", Path(args.draft).read_bytes())
        elif args.cmd == "seal-batch-stage":
            if name not in {"RUN_PSERC", "RUN_ENDSTEMPEL"}:
                raise Blocked("DURABLE_EVENT_BATCH_STAGE_NOT_ALLOWED")
            event = make_event(current, action, "JSON_GZIP_BASE64", canon(load_json(Path(args.result_json))))
        else:
            raise Blocked("DURABLE_EVENT_COMMAND_INVALID")

        print(EVENT_CONTRACT)
        print(json.dumps(event, ensure_ascii=False, sort_keys=True, separators=(",", ":")))
        return 0
    except Exception as exc:
        print("CONCEPT_AGENT_DURABLE_EVENT_BLOCKED:" + str(exc), file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
