#!/usr/bin/env python3
from __future__ import annotations

import hashlib
import importlib.util
import json
import tempfile
from pathlib import Path

HERE = Path(__file__).resolve().parent


def load_module(path: Path, name: str):
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError("MODULE_LOAD_FAILED")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def check(condition: bool, message: str):
    if not condition:
        raise AssertionError(message)


def main() -> int:
    policy = json.loads((HERE / "OUTPUT_VISIBILITY_POLICY.json").read_text(encoding="utf-8"))
    check(policy["chat_output_authority"] == "NONE", "CHAT_OUTPUT_AUTHORITY")
    check(policy["domain_logic_authority"] == "NONE", "DOMAIN_AUTHORITY")
    check(policy["quality_authority"] == "NONE", "QUALITY_AUTHORITY")
    check(policy["publish_allowed"] is False, "PUBLISH")
    check(policy["unbound_output_policy"] == "QUARANTINE_INVALID_NEVER_SURFACE_AS_PROJECT_RESULT", "UNBOUND_POLICY")

    gate = load_module(HERE / "output_release_gate.py", "output_release_gate_test")
    with tempfile.TemporaryDirectory() as td:
        base = Path(td)
        q = base / ".pferde-quarantine"
        q.mkdir()
        f = q / "x.bin"
        f.write_bytes(b"ok")
        digest = hashlib.sha256(b"ok").hexdigest()

        old_repo = gate.REPO
        gate.REPO = base
        try:
            verified = gate.verify_outputs(
                {"worker_quarantine_root": ".pferde-quarantine"},
                [{"ref": ".pferde-quarantine/x.bin", "sha256": digest}],
            )
            check(len(verified) == 1, "POSITIVE_OUTPUT_VERIFY")
            try:
                gate.verify_outputs(
                    {"worker_quarantine_root": ".pferde-quarantine"},
                    [{"ref": "outside/x.bin", "sha256": digest}],
                )
                raise AssertionError("OUTSIDE_NOT_BLOCKED")
            except gate.Blocked as exc:
                check(str(exc).startswith("OUTPUT_OUTSIDE_QUARANTINE"), "OUTSIDE_REASON")
            try:
                gate.verify_outputs(
                    {"worker_quarantine_root": ".pferde-quarantine"},
                    [{"ref": ".pferde-quarantine/x.bin", "sha256": "0" * 64}],
                )
                raise AssertionError("HASH_MISMATCH_NOT_BLOCKED")
            except gate.Blocked as exc:
                check(str(exc).startswith("OUTPUT_HASH_MISMATCH"), "HASH_REASON")
        finally:
            gate.REPO = old_repo

    source = (HERE / "output_release_gate.py").read_text(encoding="utf-8")
    forbidden = ["body_html", "body_text", "post_content", "keyword density", "rewrite("]
    for token in forbidden:
        check(token not in source, "CONTENT_MUTATION_TOKEN:" + token)
    print("OUTPUT_QUARANTINE_TEST_PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
