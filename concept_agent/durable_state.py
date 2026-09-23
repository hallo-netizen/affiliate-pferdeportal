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
SHA_RE = re.compile(r"^[0-9a-f]{40,64}$")
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


def _verify_hash_bound_object(value: dict, field: str, contract: str) -> None:
    if not isinstance(value, dict) or value.get("contract") != contract:
        raise Blocked(field.upper() + "_CONTRACT_INVALID")
    core = dict(value)
    declared = core.pop(field, None)
    if not isinstance(declared, str) or not HEX64_RE.fullmatch(declared):
        raise Blocked(field.upper() + "_HASH_INVALID")
    if stable(core) != declared:
        raise Blocked(field.upper() + "_HASH_MISMATCH")


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
    if not isinstance(ready, dict):
        raise Blocked("DURABLE_STATE_MACHINE_READY_MISSING")
    if not isinstance(ready.get("run_id"), int) or ready["run_id"] < 1:
        raise Blocked("DURABLE_STATE_MACHINE_READY_RUN_INVALID")
    if ready.get("second_text_start_allowed") is not False:
        raise Blocked("DURABLE_STATE_SECOND_TEXT_START_INVALID")

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

    _verify_hash_bound_object(
        binding,
        "binding_sha256",
        "CONCEPT_AGENT_CURRENT_PRODUCTION_BINDING_V1",
    )
    _verify_hash_bound_object(
        checkpoint,
        "checkpoint_sha256",
        "CONCEPT_AGENT_CURRENT_PROGRESS_V1",
    )
    if binding.get("batch_sha256") != state.get("batch_sha256"):
        raise Blocked("DURABLE_STATE_BINDING_BATCH_MISMATCH")
    if checkpoint.get("batch_sha256") != state.get("batch_sha256"):
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

    def _json(self, method: str, path: str, payload: dict | None = None) -> dict:
        url = API_ROOT + path
        data = None
        if payload is not None:
            data = json.dumps(payload, ensure_ascii=False).encode("utf-8")
        req = urllib.request.Request(
            url,
            data=data,
            method=method,
            headers={
                "Accept": "application/vnd.github+json",
                "Authorization": "Bearer " + self.token,
                "User-Agent": "pferdeatelier-concept-agent-durable-state",
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
            value = json.loads(raw.decode("utf-8"))
        except Exception as exc:
            raise Blocked("DURABLE_STATE_GITHUB_JSON_INVALID") from exc
        if not isinstance(value, dict):
            raise Blocked("DURABLE_STATE_GITHUB_RESPONSE_INVALID")
        return value

    @staticmethod
    def _ref_path() -> str:
        return "/repos/" + REPOSITORY + "/git/ref/heads/" + urllib.parse.quote(
            BRANCH, safe=""
        )

    @staticmethod
    def _contents_path() -> str:
        return (
            "/repos/"
            + REPOSITORY
            + "/contents/"
            + urllib.parse.quote(STATE_PATH, safe="/")
            + "?ref="
            + urllib.parse.quote(BRANCH, safe="")
        )

    def load(self) -> dict:
        ref = self._json("GET", self._ref_path())
        head_sha = str(((ref.get("object") or {}).get("sha")) or "")
        if not SHA_RE.fullmatch(head_sha):
            raise Blocked("DURABLE_STATE_BRANCH_HEAD_INVALID")

        row = self._json("GET", self._contents_path())
        blob_sha = str(row.get("sha") or "")
        if not SHA_RE.fullmatch(blob_sha):
            raise Blocked("DURABLE_STATE_BLOB_SHA_INVALID")
        content = row.get("content")
        encoding = row.get("encoding")
        if encoding == "base64" and isinstance(content, str):
            raw = base64.b64decode(content, validate=False)
        else:
            blob = self._json(
                "GET",
                "/repos/" + REPOSITORY + "/git/blobs/" + blob_sha,
            )
            if blob.get("encoding") != "base64" or not isinstance(blob.get("content"), str):
                raise Blocked("DURABLE_STATE_BLOB_CONTENT_INVALID")
            raw = base64.b64decode(blob["content"], validate=False)
        try:
            state = json.loads(raw.decode("utf-8"))
        except Exception as exc:
            raise Blocked("DURABLE_STATE_FILE_JSON_INVALID") from exc
        verify(state)
        return {
            "state": state,
            "raw": raw,
            "head_sha": head_sha,
            "blob_sha": blob_sha,
        }

    def write(self, state: dict, expected_head_sha: str) -> dict:
        verify(state)
        current_ref = self._json("GET", self._ref_path())
        current_head = str(((current_ref.get("object") or {}).get("sha")) or "")
        if current_head != expected_head_sha:
            raise Blocked("DURABLE_STATE_BRANCH_MOVED")

        commit = self._json(
            "GET",
            "/repos/" + REPOSITORY + "/git/commits/" + current_head,
        )
        tree_sha = str(((commit.get("tree") or {}).get("sha")) or "")
        if not SHA_RE.fullmatch(tree_sha):
            raise Blocked("DURABLE_STATE_BASE_TREE_INVALID")

        raw = (
            json.dumps(state, ensure_ascii=False, indent=2) + "\n"
        ).encode("utf-8")
        blob = self._json(
            "POST",
            "/repos/" + REPOSITORY + "/git/blobs",
            {
                "content": base64.b64encode(raw).decode("ascii"),
                "encoding": "base64",
            },
        )
        blob_sha = str(blob.get("sha") or "")
        if not SHA_RE.fullmatch(blob_sha):
            raise Blocked("DURABLE_STATE_NEW_BLOB_INVALID")

        tree = self._json(
            "POST",
            "/repos/" + REPOSITORY + "/git/trees",
            {
                "base_tree": tree_sha,
                "tree": [
                    {
                        "path": STATE_PATH,
                        "mode": "100644",
                        "type": "blob",
                        "sha": blob_sha,
                    }
                ],
            },
        )
        new_tree = str(tree.get("sha") or "")
        if not SHA_RE.fullmatch(new_tree):
            raise Blocked("DURABLE_STATE_NEW_TREE_INVALID")

        new_commit = self._json(
            "POST",
            "/repos/" + REPOSITORY + "/git/commits",
            {
                "message": "Persist Concept Agent durable state "
                + state["state_sha256"][:12],
                "tree": new_tree,
                "parents": [current_head],
            },
        )
        new_commit_sha = str(new_commit.get("sha") or "")
        if not SHA_RE.fullmatch(new_commit_sha):
            raise Blocked("DURABLE_STATE_NEW_COMMIT_INVALID")

        self._json(
            "PATCH",
            self._ref_path(),
            {"sha": new_commit_sha, "force": False},
        )
        reread = self.load()
        if reread["head_sha"] != new_commit_sha:
            raise Blocked("DURABLE_STATE_READBACK_HEAD_MISMATCH")
        if reread["raw"] != raw:
            raise Blocked("DURABLE_STATE_READBACK_BYTES_MISMATCH")
        if reread["state"].get("state_sha256") != state.get("state_sha256"):
            raise Blocked("DURABLE_STATE_READBACK_HASH_MISMATCH")
        return reread


def _backend(value=None):
    return value if value is not None else GitHubBackend()


def load_current(backend=None) -> dict:
    return _backend(backend).load()["state"]


def assert_current(binding: dict, checkpoint: dict, backend=None) -> dict:
    detail = _backend(backend).load()
    state = detail["state"]
    if state.get("production_binding") != binding:
        raise Blocked("DURABLE_STATE_BINDING_NOT_CURRENT")
    if state.get("checkpoint") != checkpoint:
        raise Blocked("DURABLE_STATE_CHECKPOINT_NOT_CURRENT")
    return state


def activate_production(binding: dict, checkpoint: dict, backend=None) -> dict:
    _verify_hash_bound_object(
        binding,
        "binding_sha256",
        "CONCEPT_AGENT_CURRENT_PRODUCTION_BINDING_V1",
    )
    _verify_hash_bound_object(
        checkpoint,
        "checkpoint_sha256",
        "CONCEPT_AGENT_CURRENT_PROGRESS_V1",
    )
    be = _backend(backend)
    detail = be.load()
    current = detail["state"]
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
    return be.write(new, detail["head_sha"])["state"]


def persist_checkpoint_transition(
    binding: dict,
    previous: dict,
    new_checkpoint: dict,
    backend=None,
) -> dict:
    _verify_hash_bound_object(
        binding,
        "binding_sha256",
        "CONCEPT_AGENT_CURRENT_PRODUCTION_BINDING_V1",
    )
    _verify_hash_bound_object(
        previous,
        "checkpoint_sha256",
        "CONCEPT_AGENT_CURRENT_PROGRESS_V1",
    )
    _verify_hash_bound_object(
        new_checkpoint,
        "checkpoint_sha256",
        "CONCEPT_AGENT_CURRENT_PROGRESS_V1",
    )
    if new_checkpoint.get("previous_checkpoint_sha256") != previous.get(
        "checkpoint_sha256"
    ):
        raise Blocked("DURABLE_STATE_TRANSITION_CHAIN_INVALID")

    be = _backend(backend)
    detail = be.load()
    current = detail["state"]
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
    return be.write(new, detail["head_sha"])["state"]


def materialize_current(binding_path: Path, checkpoint_path: Path, backend=None) -> dict:
    state = load_current(backend)
    binding = state.get("production_binding")
    checkpoint = state.get("checkpoint")
    if not isinstance(binding, dict) or not isinstance(checkpoint, dict):
        raise Blocked(
            "DURABLE_STATE_PRODUCTION_NOT_ACTIVE:" + str(state.get("phase"))
        )
    binding_path.parent.mkdir(parents=True, exist_ok=True)
    checkpoint_path.parent.mkdir(parents=True, exist_ok=True)
    binding_path.write_text(
        json.dumps(binding, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    checkpoint_path.write_text(
        json.dumps(checkpoint, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
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
            print(
                json.dumps(
                    {
                        "status": state["status"],
                        "phase": state["phase"],
                        "batch_sha256": state["batch_sha256"],
                        "state_sha256": state["state_sha256"],
                        "next_action": state["next_action"],
                        "publish_allowed": False,
                    },
                    ensure_ascii=False,
                    sort_keys=True,
                )
            )
            return 0
        if len(argv) == 4 and argv[1] == "materialize":
            result = materialize_current(Path(argv[2]), Path(argv[3]))
            print(json.dumps(result, ensure_ascii=False, sort_keys=True))
            return 0
        raise Blocked(
            "USE: durable_state.py status | materialize OUT_BINDING OUT_CHECKPOINT"
        )
    except Exception as exc:
        print("CONCEPT_AGENT_DURABLE_STATE_BLOCKED:" + str(exc), file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
