from __future__ import annotations

import json
import os
import subprocess
import sys
from pathlib import Path

import workspace_recovery_capsule as recovery

HERE = Path(__file__).resolve().parent
TESTWORKER = HERE / "deterministic_test_worker.py"
CONTROLLER = HERE / "controller.py"


class RestartProbeError(RuntimeError):
    pass


def _run(argv: list[str | Path]) -> None:
    env = os.environ.copy()
    env["PYTHONDONTWRITEBYTECODE"] = "1"
    cp = subprocess.run(
        [str(x) for x in argv],
        cwd=HERE.parent,
        env=env,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=False,
    )
    if cp.returncode != 0:
        raise RestartProbeError(
            "RESTART_PROBE_COMMAND_FAILED:"
            + " ".join(str(x) for x in argv)
            + ":STDOUT:"
            + cp.stdout
            + ":STDERR:"
            + cp.stderr
        )


def main(argv: list[str]) -> int:
    try:
        if len(argv) != 4:
            raise RestartProbeError(
                "USE: restart_repair_probe.py CAPSULE RESTORED_WORKSPACE GENERATED_DIR"
            )
        capsule = Path(argv[1])
        workspace = Path(argv[2])
        generated = Path(argv[3])
        restored = recovery.restore_capsule(capsule, workspace)
        state_path = workspace / "state.json"
        state_before = json.loads(state_path.read_text(encoding="utf-8"))
        if state_before.get("phase") != "REPAIR_REQUIRED":
            raise RestartProbeError("RESTART_PROBE_NOT_REPAIR_REQUIRED")
        article_before = dict(state_before.get("article") or {})
        findings_before = list(((state_before.get("checks") or {}).get("findings") or []))
        draft_before = str(state_before.get("draft_markdown") or "")
        draft_sha_before = str(state_before.get("draft_sha256") or "")
        revision_before = int(state_before.get("revision") or 0)

        generated.mkdir(parents=True, exist_ok=True)
        repaired = generated / "restart-repair.html"
        _run([sys.executable, TESTWORKER, "repair", workspace, repaired])
        _run([sys.executable, CONTROLLER, "repair", workspace, repaired])

        state_after = json.loads(state_path.read_text(encoding="utf-8"))
        if state_after.get("phase") != "CHECK_REQUIRED":
            raise RestartProbeError("RESTART_PROBE_REPAIR_DID_NOT_REENTER_CHECK")
        if int(state_after.get("revision") or 0) != revision_before + 1:
            raise RestartProbeError("RESTART_PROBE_REVISION_NOT_ADVANCED")
        if state_after.get("article") != article_before:
            raise RestartProbeError("RESTART_PROBE_ARTICLE_IDENTITY_CHANGED")
        if str(state_after.get("draft_sha256") or "") == draft_sha_before:
            raise RestartProbeError("RESTART_PROBE_DRAFT_NOT_CHANGED_BY_REPAIR")
        if str(state_after.get("draft_markdown") or "") == draft_before:
            raise RestartProbeError("RESTART_PROBE_DRAFT_BYTES_NOT_CHANGED_BY_REPAIR")

        print(json.dumps({
            "contract": "SYSTEM4_REPAIR_RESTART_PROBE_V1",
            "status": "PASS",
            "restored_tree_sha256": restored["tree_sha256"],
            "article": article_before,
            "findings_before_restart": findings_before,
            "revision_before": revision_before,
            "revision_after": state_after.get("revision"),
            "draft_sha256_before": draft_sha_before,
            "draft_sha256_after": state_after.get("draft_sha256"),
            "phase_after": state_after.get("phase"),
            "same_article": True,
            "new_process_restore_and_repair": True,
            "publish_allowed": False,
        }, ensure_ascii=False, sort_keys=True))
        return 0
    except Exception as exc:
        print(json.dumps({
            "ok": False,
            "status": "SYSTEM4_REPAIR_RESTART_PROBE_BLOCKED",
            "reason": str(exc),
            "publish_allowed": False,
        }, ensure_ascii=False, sort_keys=True))
        return 2


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
