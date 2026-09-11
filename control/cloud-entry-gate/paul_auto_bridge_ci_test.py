#!/usr/bin/env python3
from __future__ import annotations

import contextlib
import importlib.util
import io
import json
from pathlib import Path
import subprocess
import sys
import tempfile

MODPATH = Path(__file__).with_name("cloud_entry.py")
spec = importlib.util.spec_from_file_location("cloud_entry", MODPATH)
m = importlib.util.module_from_spec(spec)
spec.loader.exec_module(m)


def run(cmd, cwd=None):
    return subprocess.run(
        cmd,
        cwd=str(cwd) if cwd else None,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=False,
    )


def expect_block(fn, token):
    try:
        fn()
    except m.Blocked as exc:
        if token not in str(exc):
            raise AssertionError(f"expected {token}, got {exc}") from exc
        return
    raise AssertionError(f"expected block {token}")


def helper_bridge_tests():
    old_repo, old_gate = m.REPO, m.PAUL_GATE
    try:
        with tempfile.TemporaryDirectory() as td:
            repo = Path(td) / "repo"
            repo.mkdir()
            run(["git", "init", "-q"], cwd=repo)
            run(["git", "config", "user.email", "ci@example.invalid"], cwd=repo)
            run(["git", "config", "user.name", "CI"], cwd=repo)
            (repo / "x").write_text("x", encoding="utf-8")
            run(["git", "add", "."], cwd=repo)
            run(["git", "commit", "-q", "-m", "base"], cwd=repo)

            gate = repo / "control/paul-scope-gate/paul_scope_gate.py"
            gate.parent.mkdir(parents=True, exist_ok=True)
            gate.write_text(
                """#!/usr/bin/env python3
import pathlib,sys
log=pathlib.Path('gate.log')
cmd=sys.argv[1]
log.write_text((log.read_text() if log.exists() else '')+cmd+'\\n')
if pathlib.Path('FORCE_FAIL').exists():
    print('TEST_GATE_BLOCK')
    raise SystemExit(2)
print('TEST_GATE_PASS:'+cmd)
""",
                encoding="utf-8",
            )

            m.REPO, m.PAUL_GATE = repo, gate

            assert m.run_paul_scope_gate("start") is None
            assert not (repo / "gate.log").exists()

            run(["git", "checkout", "-q", "-b", "paul/test"], cwd=repo)
            assert "TEST_GATE_PASS:start" in m.run_paul_scope_gate("start")
            assert "TEST_GATE_PASS:verify" in m.run_paul_scope_gate("verify")

            (repo / "FORCE_FAIL").write_text("1", encoding="utf-8")
            expect_block(lambda: m.run_paul_scope_gate("start"), "PAUL_SCOPE_GATE_BLOCKED:TEST_GATE_BLOCK")
            (repo / "FORCE_FAIL").unlink()

            gate.unlink()
            expect_block(lambda: m.run_paul_scope_gate("start"), "PAUL_SCOPE_GATE_MISSING")
    finally:
        m.REPO, m.PAUL_GATE = old_repo, old_gate


def main_wiring_tests():
    old = {
        "materialize": m.materialize,
        "verify": m.verify,
        "complete": m.complete,
        "run_paul_scope_gate": m.run_paul_scope_gate,
        "argv": list(sys.argv),
    }
    events = []
    try:
        m.materialize = lambda: {"ok": True, "status": "MATERIALIZE_TEST"}
        m.verify = lambda: {"ok": True, "status": "VERIFY_TEST"}

        def fake_complete(path):
            events.append("complete")
            return {"ok": True, "status": "COMPLETE_TEST"}

        def fake_gate(command):
            events.append("gate:" + command)
            return "AUTO_" + command

        m.complete = fake_complete
        m.run_paul_scope_gate = fake_gate

        for argv, expected_events, expected_status in [
            (["cloud_entry.py", "start"], ["gate:start"], "MATERIALIZE_TEST"),
            (["cloud_entry.py", "verify"], ["gate:verify"], "VERIFY_TEST"),
        ]:
            events.clear()
            sys.argv = argv
            buf = io.StringIO()
            with contextlib.redirect_stdout(buf):
                rc = m.main()
            assert rc == 0
            out = json.loads(buf.getvalue())
            assert out["status"] == expected_status
            assert out["paul_scope_gate"].startswith("AUTO_")
            assert events == expected_events

        events.clear()
        sys.argv = ["cloud_entry.py", "complete", "receipt.json"]
        buf = io.StringIO()
        with contextlib.redirect_stdout(buf):
            rc = m.main()
        assert rc == 0
        out = json.loads(buf.getvalue())
        assert out["status"] == "COMPLETE_TEST"
        assert out["paul_scope_gate"] == "AUTO_verify"
        assert events == ["gate:verify", "complete"]

        def failing_gate(command):
            raise m.Blocked("PAUL_SCOPE_GATE_BLOCKED:TEST")

        m.run_paul_scope_gate = failing_gate
        events.clear()
        sys.argv = ["cloud_entry.py", "start"]
        buf = io.StringIO()
        with contextlib.redirect_stdout(buf):
            rc = m.main()
        assert rc == 2
        out = json.loads(buf.getvalue())
        assert out["status"] == "CODEX_CLOUD_ENTRANCE_BLOCKED"
        assert "PAUL_SCOPE_GATE_BLOCKED:TEST" in out["reason"]
    finally:
        m.materialize = old["materialize"]
        m.verify = old["verify"]
        m.complete = old["complete"]
        m.run_paul_scope_gate = old["run_paul_scope_gate"]
        sys.argv = old["argv"]


def main():
    helper_bridge_tests()
    main_wiring_tests()
    print(json.dumps({
        "ok": True,
        "status": "PAUL_AUTO_BRIDGE_CI_PASS",
        "normal_branch_no_gate": "PASS",
        "paul_start_auto": "PASS",
        "paul_verify_auto": "PASS",
        "paul_complete_preverify_auto": "PASS",
        "gate_failure_blocks": "PASS",
        "missing_gate_blocks": "PASS",
        "main_wiring_start_verify_complete": "PASS"
    }, indent=2))


if __name__ == "__main__":
    main()
