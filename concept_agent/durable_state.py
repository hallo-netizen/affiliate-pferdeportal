#!/usr/bin/env python3
from __future__ import annotations

import base64
import hashlib
import json
import os
import re
import sys
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path

CONTRACT = "CONCEPT_AGENT_DURABLE_RUNTIME_STATE_V1"
REPOSITORY = "hallo-netizen/affiliate-pferdeportal"
BRANCH = "runtime/concept-agent-current"
STATE_PATH = "concept_agent/runtime/CURRENT_PRODUCTION_STATE.json"
API_ROOT = "https://api.github.com"
MAX_STATE_BYTES = 950_000
BOOTSTRAP_STATE_SHA256 = "fb5d51ea35e71dcc69e565f1173ca0210b2cd081b8c943246adced9619997416"
RECEIPT_CONTRACT = "CONCEPT_AGENT_DURABLE_STATE_RECEIPT_V1"
TRUSTED_RECEIPT_WRITERS = {
    "chatgpt-codex-connector[bot]",
    "github-actions[bot]",
}
HEX64_RE = re.compile(r"^[0-9a-f]{64}$")


class Blocked(RuntimeError):
    pass


def canon(value) -> bytes:
    return json.dumps(
        value,
        ensure_ascii=False,
        sort_keys=True,
        separators=(",", ":"),
    ).encode("utf-8")


def stable(value) -> str:
    return hashlib.sha256(canon(value)).hexdigest()


def seal(value: dict) -> dict:
    out = json.loads(json.dumps(value))
    out.pop("state_sha256", None)
    out["state_sha256"] = stable(out)
    return out


def _verify_bound(value: dict, hash_field: str, contract: str) -> None:
    if not isinstance(value, dict) or value.get("contract") != contract:
        raise Blocked(hash_field.upper() + "_CONTRACT_INVALID")
    core = dict(value)
    declared = core.pop(hash_field, None)
    if not isinstance(declared, str) or not HEX64_RE.fullmatch(declared):
        raise Blocked(hash_field.upper() + "_HASH_INVALID")
    if stable(core) != declared:
        raise Blocked(hash_field.upper() + "_HASH_MISMATCH")


def verify(state: dict) -> dict:
    if not isinstance(state, dict) or state.get("contract") != CONTRACT:
        raise Blocked("DURABLE_STATE_CONTRACT_INVALID")
    core = dict(state)
    declared = core.pop("state_sha256", None)
    if not isinstance(declared, str) or not HEX64_RE.fullmatch(declared):
        raise Blocked("DURABLE_STATE_HASH_INVALID")
    if stable(core) != declared:
        raise Blocked("DURABLE_STATE_HASH_MISMATCH")
    if state.get("repository") != REPOSITORY:
        raise Blocked("DURABLE_STATE_REPOSITORY_INVALID")
    if state.get("state_branch") != BRANCH or state.get("state_path") != STATE_PATH:
        raise Blocked("DURABLE_STATE_LOCATION_INVALID")
    if not HEX64_RE.fullmatch(str(state.get("batch_sha256") or "")):
        raise Blocked("DURABLE_STATE_BATCH_INVALID")
    count = state.get("item_count")
    if not isinstance(count, int) or isinstance(count, bool) or count < 1:
        raise Blocked("DURABLE_STATE_COUNT_INVALID")
    if state.get("publish_allowed") is not False:
        raise Blocked("DURABLE_STATE_PUBLISH_INVALID")
    if state.get("chat_may_choose_action") is not False:
        raise Blocked("DURABLE_STATE_CHAT_ACTION_INVALID")
    if state.get("chat_may_write_state") is not False:
        raise Blocked("DURABLE_STATE_CHAT_WRITE_INVALID")

    ready = state.get("machine_ready")
    if not isinstance(ready, dict) or not isinstance(ready.get("run_id"), int):
        raise Blocked("DURABLE_STATE_MACHINE_READY_INVALID")
    if ready["run_id"] < 1 or ready.get("second_text_start_allowed") is not False:
        raise Blocked("DURABLE_STATE_MACHINE_READY_INVALID")

    binding = state.get("production_binding")
    checkpoint = state.get("checkpoint")
    if binding is None or checkpoint is None:
        if binding is not None or checkpoint is not None:
            raise Blocked("DURABLE_STATE_PARTIAL_PRODUCTION_BINDING")
        if state.get("status") != "WAITING_FOR_RESEARCH_BOUND":
            raise Blocked("DURABLE_STATE_PREPRODUCTION_STATUS_INVALID")
        if state.get("phase") != "RESEARCH_BOUND_REQUIRED":
            raise Blocked("DURABLE_STATE_PREPRODUCTION_PHASE_INVALID")
        if state.get("next_action") != "RUN_EXISTING_RESEARCH_FOR_CURRENT_BATCH":
            raise Blocked("DURABLE_STATE_PREPRODUCTION_ACTION_INVALID")
        return state

    _verify_bound(
        binding,
        "binding_sha256",
        "CONCEPT_AGENT_CURRENT_PRODUCTION_BINDING_V1",
    )
    _verify_bound(
        checkpoint,
        "checkpoint_sha256",
        "CONCEPT_AGENT_CURRENT_PROGRESS_V1",
    )
    if binding.get("batch_sha256") != state["batch_sha256"]:
        raise Blocked("DURABLE_STATE_BINDING_BATCH_MISMATCH")
    if checkpoint.get("batch_sha256") != state["batch_sha256"]:
        raise Blocked("DURABLE_STATE_CHECKPOINT_BATCH_MISMATCH")
    if binding.get("item_count") != count or checkpoint.get("item_count") != count:
        raise Blocked("DURABLE_STATE_PRODUCTION_COUNT_MISMATCH")
    if checkpoint.get("production_binding_sha256") != binding.get("binding_sha256"):
        raise Blocked("DURABLE_STATE_CHECKPOINT_BINDING_MISMATCH")
    if binding.get("publish_allowed") is not False or checkpoint.get("publish_allowed") is not False:
        raise Blocked("DURABLE_STATE_NESTED_PUBLISH_INVALID")
    if state.get("phase") != checkpoint.get("phase"):
        raise Blocked("DURABLE_STATE_PHASE_MISMATCH")
    if state.get("next_action") != checkpoint.get("allowed_action"):
        raise Blocked("DURABLE_STATE_ACTION_MISMATCH")
    expected_status = (
        "STOPPED"
        if checkpoint.get("phase") == "ENDSTEMPEL_PASS_STOP"
        else "PRODUCTION_ACTIVE"
    )
    if state.get("status") != expected_status:
        raise Blocked("DURABLE_STATE_PRODUCTION_STATUS_INVALID")
    return state


class GitHubBackend:
    def __init__(self, token: str | None = None):
        self.token = token or os.environ.get("GITHUB_TOKEN") or os.environ.get("GH_TOKEN")
        if not self.token:
            raise Blocked("DURABLE_STATE_GITHUB_TOKEN_MISSING")

    def _request(self, method: str, path: str, payload=None):
        data = None
        if payload is not None:
            data = json.dumps(payload, ensure_ascii=False).encode("utf-8")
        req = urllib.request.Request(
            API_ROOT + path,
            data=data,
            method=method,
            headers={
                "Accept": "application/vnd.github+json",
                "Authorization": "Bearer " + self.token,
                "User-Agent": "pferdeatelier-durable-state",
                "X-GitHub-Api-Version": "2022-11-28",
                "Content-Type": "application/json",
            },
        )
        try:
            with urllib.request.urlopen(req, timeout=30) as fh:
                raw = fh.read()
        except urllib.error.HTTPError as exc:
            detail = exc.read().decode("utf-8", "replace")
            raise Blocked(
                f"DURABLE_STATE_GITHUB_HTTP_{exc.code}:{detail[:500]}"
            ) from exc
        except Exception as exc:
            raise Blocked("DURABLE_STATE_GITHUB_IO:" + str(exc)) from exc
        if not raw:
            return {}
        try:
            return json.loads(raw.decode("utf-8"))
        except Exception as exc:
            raise Blocked("DURABLE_STATE_GITHUB_JSON_INVALID") from exc

    @staticmethod
    def _contents_path() -> str:
        return (
            "/repos/" + REPOSITORY + "/contents/"
            + urllib.parse.quote(STATE_PATH, safe="/")
            + "?ref=" + urllib.parse.quote(BRANCH, safe="")
        )

    def _receipt_exists(self, state: dict) -> bool:
        if state["state_sha256"] == BOOTSTRAP_STATE_SHA256:
            return True
        issue = (state.get("machine_ready") or {}).get("issue_number")
        if not isinstance(issue, int) or issue < 1:
            raise Blocked("DURABLE_STATE_RECEIPT_ISSUE_INVALID")
        exact = (
            RECEIPT_CONTRACT
            + "\nSTATE_SHA256: " + state["state_sha256"]
            + "\nBATCH_SHA256: " + state["batch_sha256"]
            + "\nPUBLISH: NO"
        )
        page = 1
        while True:
            rows = self._request(
                "GET",
                "/repos/" + REPOSITORY + "/issues/" + str(issue)
                + "/comments?per_page=100&page=" + str(page),
            )
            if not isinstance(rows, list):
                raise Blocked("DURABLE_STATE_RECEIPT_LIST_INVALID")
            for row in rows:
                if str(row.get("body") or "") != exact:
                    continue
                login = str(((row.get("user") or {}).get("login")) or "")
                if login not in TRUSTED_RECEIPT_WRITERS:
                    raise Blocked("DURABLE_STATE_RECEIPT_WRITER_INVALID:" + login)
                return True
            if len(rows) < 100:
                return False
            page += 1

    def _post_receipt(self, state: dict) -> None:
        issue = (state.get("machine_ready") or {}).get("issue_number")
        if not isinstance(issue, int) or issue < 1:
            raise Blocked("DURABLE_STATE_RECEIPT_ISSUE_INVALID")
        body = (
            RECEIPT_CONTRACT
            + "\nSTATE_SHA256: " + state["state_sha256"]
            + "\nBATCH_SHA256: " + state["batch_sha256"]
            + "\nPUBLISH: NO"
        )
        row = self._request(
            "POST",
            "/repos/" + REPOSITORY + "/issues/" + str(issue) + "/comments",
            {"body": body},
        )
        if not isinstance(row, dict):
            raise Blocked("DURABLE_STATE_RECEIPT_RESPONSE_INVALID")
        login = str(((row.get("user") or {}).get("login")) or "")
        if login not in TRUSTED_RECEIPT_WRITERS:
            raise Blocked("DURABLE_STATE_WRITER_IDENTITY_INVALID:" + login)

    def load(self) -> dict:
        row = self._request("GET", self._contents_path())
        if not isinstance(row, dict):
            raise Blocked("DURABLE_STATE_CONTENTS_INVALID")
        blob_sha = str(row.get("sha") or "")
        content = row.get("content")
        if row.get("encoding") != "base64" or not isinstance(content, str):
            raise Blocked("DURABLE_STATE_CONTENTS_ENCODING_INVALID")
        try:
            raw = base64.b64decode(content, validate=False)
            state = json.loads(raw.decode("utf-8"))
        except Exception as exc:
            raise Blocked("DURABLE_STATE_FILE_INVALID") from exc
        verify(state)
        if not self._receipt_exists(state):
            raise Blocked("DURABLE_STATE_MACHINE_RECEIPT_MISSING")
        return {"state": state, "raw": raw, "blob_sha": blob_sha}

    def write(self, state: dict, expected_state_sha256: str) -> dict:
        verify(state)
        raw = (json.dumps(state, ensure_ascii=False, indent=2) + "\n").encode("utf-8")
        if len(raw) > MAX_STATE_BYTES:
            raise Blocked("DURABLE_STATE_TOO_LARGE")

        current = self.load()
        if current["state"]["state_sha256"] != expected_state_sha256:
            raise Blocked("DURABLE_STATE_MOVED")

        result = self._request(
            "PUT",
            "/repos/" + REPOSITORY + "/contents/"
            + urllib.parse.quote(STATE_PATH, safe="/"),
            {
                "message": "Persist Concept Agent durable state " + state["state_sha256"][:12],
                "content": base64.b64encode(raw).decode("ascii"),
                "sha": current["blob_sha"],
                "branch": BRANCH,
            },
        )
        if not isinstance(result, dict):
            raise Blocked("DURABLE_STATE_WRITE_RESPONSE_INVALID")

        # A freely written state is not accepted. The writer must prove that
        # this exact state hash came from an allowed machine identity.
        self._post_receipt(state)

        reread = self.load()
        if reread["raw"] != raw:
            raise Blocked("DURABLE_STATE_READBACK_BYTES_MISMATCH")
        return reread


def _backend(value=None):
    return value if value is not None else GitHubBackend()


def load_current(backend=None) -> dict:
    return _backend(backend).load()["state"]


def assert_current(binding: dict, checkpoint: dict, backend=None) -> dict:
    state = load_current(backend)
    if state.get("production_binding") != binding:
        raise Blocked("DURABLE_STATE_BINDING_NOT_CURRENT")
    if state.get("checkpoint") != checkpoint:
        raise Blocked("DURABLE_STATE_CHECKPOINT_NOT_CURRENT")
    return state


def activate_production(binding: dict, checkpoint: dict, backend=None) -> dict:
    _verify_bound(binding, "binding_sha256", "CONCEPT_AGENT_CURRENT_PRODUCTION_BINDING_V1")
    _verify_bound(checkpoint, "checkpoint_sha256", "CONCEPT_AGENT_CURRENT_PROGRESS_V1")
    be = _backend(backend)
    current = be.load()["state"]
    if current.get("status") != "WAITING_FOR_RESEARCH_BOUND":
        raise Blocked("DURABLE_STATE_ALREADY_ACTIVATED")
    if current.get("phase") != "RESEARCH_BOUND_REQUIRED":
        raise Blocked("DURABLE_STATE_ACTIVATION_PHASE_INVALID")
    if current.get("production_binding") is not None or current.get("checkpoint") is not None:
        raise Blocked("DURABLE_STATE_ACTIVATION_NOT_EMPTY")
    if binding.get("batch_sha256") != current.get("batch_sha256"):
        raise Blocked("DURABLE_STATE_ACTIVATION_BATCH_MISMATCH")
    if binding.get("item_count") != current.get("item_count"):
        raise Blocked("DURABLE_STATE_ACTIVATION_COUNT_MISMATCH")
    if checkpoint.get("production_binding_sha256") != binding.get("binding_sha256"):
        raise Blocked("DURABLE_STATE_ACTIVATION_BINDING_MISMATCH")

    new = dict(current)
    new.pop("state_sha256", None)
    new["status"] = "PRODUCTION_ACTIVE"
    new["phase"] = checkpoint["phase"]
    new["next_action"] = checkpoint["allowed_action"]
    new["production_binding"] = binding
    new["checkpoint"] = checkpoint
    new["last_transition"] = {
        "type": "PRODUCTION_ACTIVATED",
        "binding_sha256": binding["binding_sha256"],
        "checkpoint_sha256": checkpoint["checkpoint_sha256"],
    }
    new = seal(new)
    return be.write(new, current["state_sha256"])["state"]


def persist_checkpoint_transition(
    binding: dict,
    previous: dict,
    new_checkpoint: dict,
    backend=None,
) -> dict:
    _verify_bound(binding, "binding_sha256", "CONCEPT_AGENT_CURRENT_PRODUCTION_BINDING_V1")
    _verify_bound(previous, "checkpoint_sha256", "CONCEPT_AGENT_CURRENT_PROGRESS_V1")
    _verify_bound(new_checkpoint, "checkpoint_sha256", "CONCEPT_AGENT_CURRENT_PROGRESS_V1")
    if new_checkpoint.get("previous_checkpoint_sha256") != previous.get("checkpoint_sha256"):
        raise Blocked("DURABLE_STATE_TRANSITION_CHAIN_INVALID")

    be = _backend(backend)
    current = be.load()["state"]
    if current.get("production_binding") != binding:
        raise Blocked("DURABLE_STATE_TRANSITION_BINDING_STALE")
    if current.get("checkpoint") != previous:
        raise Blocked("DURABLE_STATE_TRANSITION_CHECKPOINT_STALE")

    new = dict(current)
    new.pop("state_sha256", None)
    new["checkpoint"] = new_checkpoint
    new["phase"] = new_checkpoint["phase"]
    new["next_action"] = new_checkpoint["allowed_action"]
    new["status"] = (
        "STOPPED"
        if new_checkpoint["phase"] == "ENDSTEMPEL_PASS_STOP"
        else "PRODUCTION_ACTIVE"
    )
    new["last_transition"] = {
        "type": "CHECKPOINT_COMMITTED",
        "previous_checkpoint_sha256": previous["checkpoint_sha256"],
        "checkpoint_sha256": new_checkpoint["checkpoint_sha256"],
    }
    new = seal(new)
    return be.write(new, current["state_sha256"])["state"]


def materialize_current(binding_path: Path, checkpoint_path: Path, backend=None) -> dict:
    state = load_current(backend)
    binding = state.get("production_binding")
    checkpoint = state.get("checkpoint")
    if not isinstance(binding, dict) or not isinstance(checkpoint, dict):
        raise Blocked("DURABLE_STATE_PRODUCTION_NOT_ACTIVE:" + str(state.get("phase")))
    binding_path.parent.mkdir(parents=True, exist_ok=True)
    checkpoint_path.parent.mkdir(parents=True, exist_ok=True)
    binding_path.write_text(json.dumps(binding, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    checkpoint_path.write_text(json.dumps(checkpoint, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    return {
        "status": state["status"],
        "phase": state["phase"],
        "batch_sha256": state["batch_sha256"],
        "state_sha256": state["state_sha256"],
        "checkpoint_sha256": checkpoint["checkpoint_sha256"],
        "allowed_action": checkpoint["allowed_action"],
        "publish_allowed": False,
    }


def main(argv: list[str]) -> int:
    try:
        if len(argv) == 2 and argv[1] == "status":
            state = load_current()
            print(json.dumps({
                "status": state["status"],
                "phase": state["phase"],
                "batch_sha256": state["batch_sha256"],
                "state_sha256": state["state_sha256"],
                "next_action": state["next_action"],
                "publish_allowed": False,
            }, ensure_ascii=False, sort_keys=True))
            return 0
        if len(argv) == 4 and argv[1] == "materialize":
            result = materialize_current(Path(argv[2]), Path(argv[3]))
            print(json.dumps(result, ensure_ascii=False, sort_keys=True))
            return 0
        raise Blocked("USE: durable_state.py status | materialize OUT_BINDING OUT_CHECKPOINT")
    except Exception as exc:
        print("CONCEPT_AGENT_DURABLE_STATE_BLOCKED:" + str(exc), file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
