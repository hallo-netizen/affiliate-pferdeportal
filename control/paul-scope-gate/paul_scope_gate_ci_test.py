#!/usr/bin/env python3
from __future__ import annotations

import importlib.util
import json
import os
from pathlib import Path
import shutil
import subprocess
import tempfile

MODPATH = Path(__file__).with_name("paul_scope_gate.py")
spec = importlib.util.spec_from_file_location("paul_scope_gate", MODPATH)
m = importlib.util.module_from_spec(spec)
spec.loader.exec_module(m)


def run(*args: str, cwd: Path | None = None) -> str:
    p = subprocess.run(
        list(args),
        cwd=str(cwd) if cwd else None,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=False,
    )
    if p.returncode != 0:
        raise RuntimeError(f"CMD_FAIL:{' '.join(args)}\nSTDOUT={p.stdout}\nSTDERR={p.stderr}")
    return p.stdout.strip()


def write(repo: Path, rel: str, text: str) -> None:
    p = repo / rel
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(text, encoding="utf-8")


def commit_all(repo: Path, msg: str) -> str:
    run("git", "add", "-A", cwd=repo)
    run("git", "commit", "-q", "-m", msg, cwd=repo)
    return run("git", "rev-parse", "HEAD", cwd=repo)


def expect_block(fn, token: str) -> None:
    try:
        fn()
    except m.Blocked as exc:
        if token not in str(exc):
            raise AssertionError(f"expected {token}, got {exc}") from exc
        return
    raise AssertionError(f"expected block {token}")


def assignment(base_sha: str, assignment_id: str = "TEXT-PAUL-001") -> str:
    return f"""# TEXT HOBBYRAUM
STATUS: AKTIV / PAUL

<!-- PAUL_ASSIGNMENT_V1
STATUS: ACTIVE
WORKER: PAUL
ASSIGNMENT_ID: {assignment_id}
PAUL_BRANCH: paul/test-current-campus
TECHNICAL_BASE_SHA: {base_sha}
WRITE_SCOPE: src/allowed.txt
TASK_SOURCE: protocol/PROJECT_MEMORY/PROJEKTE/PFERDE_ATELIER/TEXT/TASK.md
TARGET_SOURCE: protocol/PROJECT_MEMORY/PROJEKTE/PFERDE_ATELIER/TEXT/TARGET.md
RULES_SOURCE: protocol/PROJECT_MEMORY/PROJEKTE/PFERDE_ATELIER/TEXT/RULES.md
-->
"""


def seed_base(seed: Path) -> str:
    write(seed, "src/allowed.txt", "BASE\n")
    write(seed, "src/other.txt", "BASE\n")
    write(seed, "protocol/PROJECT_MEMORY/START_HERE.md", "CAMPUS BASE\n")
    office = "protocol/PROJECT_MEMORY/PROJEKTE/PFERDE_ATELIER/TEXT"
    write(seed, f"{office}/START_HERE.md", "TEXT START BASE\n")
    write(seed, f"{office}/CURRENT_STATE.md", "CURRENT OLD ON PAUL BRANCH\n")
    write(seed, f"{office}/HOBBYRAUM.md", "HOBBYROOM OLD ON PAUL BRANCH\n")
    write(seed, f"{office}/TASK.md", "TASK OLD ON PAUL BRANCH\n")
    write(seed, f"{office}/TARGET.md", "TARGET OLD ON PAUL BRANCH\n")
    write(seed, f"{office}/RULES.md", "RULES OLD ON PAUL BRANCH\n")
    write(seed, "protocol/PROJECT_MEMORY/FEHLERREGISTER.md", "ERROR INDEX BASE\n")
    write(seed, "protocol/PROJECT_MEMORY/ZIELVERTRAEGE/REGISTER.md", "TARGET INDEX BASE\n")
    write(seed, "protocol/PROJECT_MEMORY/AENDERUNGSREGISTER.md", "WHY BASE\n")
    write(seed, "protocol/PROJECT_MEMORY/HANDLUNGSVERZEICHNIS.md", "ACTIONS BASE\n")
    return commit_all(seed, "base")


def update_campus(admin: Path, rel: str, text: str, msg: str) -> str:
    run("git", "checkout", "-q", m.OFFICIAL_CAMPUS_REF, cwd=admin)
    run("git", "pull", "-q", "--ff-only", "origin", m.OFFICIAL_CAMPUS_REF, cwd=admin)
    write(admin, rel, text)
    sha = commit_all(admin, msg)
    run("git", "push", "-q", "origin", m.OFFICIAL_CAMPUS_REF, cwd=admin)
    return sha


def main() -> None:
    old_cwd = Path.cwd()
    with tempfile.TemporaryDirectory() as td:
        root = Path(td)
        origin = root / "origin.git"
        run("git", "init", "--bare", "-q", str(origin))

        seed = root / "seed"
        run("git", "clone", "-q", str(origin), str(seed))
        run("git", "config", "user.email", "ci@example.invalid", cwd=seed)
        run("git", "config", "user.name", "CI", cwd=seed)
        base_sha = seed_base(seed)
        run("git", "branch", "-M", "main", cwd=seed)
        run("git", "push", "-q", "-u", "origin", "main", cwd=seed)

        # Build authoritative Campus AFTER the Paul technical base.
        run("git", "checkout", "-q", "-b", m.OFFICIAL_CAMPUS_REF, cwd=seed)
        office = "protocol/PROJECT_MEMORY/PROJEKTE/PFERDE_ATELIER/TEXT"
        write(seed, f"{office}/CURRENT_STATE.md", "CURRENT CAMPUS V1\n")
        write(seed, f"{office}/HOBBYRAUM.md", assignment(base_sha))
        write(seed, f"{office}/TASK.md", "TASK CAMPUS V1\n")
        write(seed, f"{office}/TARGET.md", "TARGET CAMPUS V1\n")
        write(seed, f"{office}/RULES.md", "RULES CAMPUS V1\n")
        campus_v1 = commit_all(seed, "campus v1")
        run("git", "push", "-q", "-u", "origin", m.OFFICIAL_CAMPUS_REF, cwd=seed)

        paul = root / "paul"
        run("git", "clone", "-q", str(origin), str(paul))
        run("git", "config", "user.email", "ci@example.invalid", cwd=paul)
        run("git", "config", "user.name", "CI", cwd=paul)
        run("git", "checkout", "-q", "-b", "paul/test-current-campus", base_sha, cwd=paul)

        admin = root / "admin"
        run("git", "clone", "-q", str(origin), str(admin))
        run("git", "config", "user.email", "ci@example.invalid", cwd=admin)
        run("git", "config", "user.name", "CI", cwd=admin)
        run("git", "checkout", "-q", m.OFFICIAL_CAMPUS_REF, cwd=admin)

        os.chdir(paul)
        try:
            # NEGATIVE baseline: Paul branch really contains stale Campus copies.
            local_current = (paul / office / "CURRENT_STATE.md").read_text(encoding="utf-8")
            assert local_current == "CURRENT OLD ON PAUL BRANCH\n"

            # POSITIVE 1: start fetches latest official Campus, not local stale copy.
            m.start()
            capsule = json.loads((paul / ".paul-capsule/ASSIGNMENT.json").read_text(encoding="utf-8"))
            assert capsule["campus_head"] == campus_v1
            cap_current = (
                paul / ".paul-capsule/sources" / office / "CURRENT_STATE.md"
            ).read_text(encoding="utf-8")
            assert cap_current == "CURRENT CAMPUS V1\n"
            assert cap_current != local_current

            # POSITIVE 2: allowed technical work with unchanged relevant Campus verifies.
            write(paul, "src/allowed.txt", "PAUL ALLOWED WORK\n")
            m.verify()

            # NEGATIVE 1: task/problem develops while Paul works -> stale block.
            campus_v2 = update_campus(
                admin, f"{office}/TASK.md", "TASK CAMPUS V2 - NEW DEVELOPMENT\n", "task develops"
            )
            expect_block(m.verify, "STALE_ASSIGNMENT_BLOCKED:SOURCE_CHANGED:" + f"{office}/TASK.md")

            # POSITIVE 3: restart automatically refreshes to newest Campus and can continue.
            m.start()
            capsule2 = json.loads((paul / ".paul-capsule/ASSIGNMENT.json").read_text(encoding="utf-8"))
            assert capsule2["campus_head"] == campus_v2
            cap_task = (
                paul / ".paul-capsule/sources" / office / "TASK.md"
            ).read_text(encoding="utf-8")
            assert cap_task == "TASK CAMPUS V2 - NEW DEVELOPMENT\n"
            m.verify()

            # POSITIVE 4: unrelated WHY change does not falsely stale-block Paul.
            update_campus(
                admin,
                "protocol/PROJECT_MEMORY/AENDERUNGSREGISTER.md",
                "WHY UNRELATED CHANGE\n",
                "unrelated why",
            )
            m.verify()

            # NEGATIVE 2: CURRENT_STATE changes -> stale block.
            update_campus(
                admin, f"{office}/CURRENT_STATE.md", "CURRENT CAMPUS V2\n", "current changes"
            )
            expect_block(
                m.verify,
                "STALE_ASSIGNMENT_BLOCKED:SOURCE_CHANGED:" + f"{office}/CURRENT_STATE.md",
            )

            # Refresh again.
            m.start()
            m.verify()

            # NEGATIVE 3: assignment identity changes -> stale block.
            update_campus(
                admin,
                f"{office}/HOBBYRAUM.md",
                assignment(base_sha, assignment_id="TEXT-PAUL-002"),
                "assignment changes",
            )
            expect_block(m.verify, "STALE_ASSIGNMENT_BLOCKED:ASSIGNMENT_ID")

            # NEGATIVE 4: assignment removed -> Paul must stop.
            update_campus(
                admin,
                f"{office}/HOBBYRAUM.md",
                "# TEXT HOBBYRAUM\nSTATUS: AKTIV / NORMALER ARBEITSCHAT\n",
                "paul unassigned",
            )
            expect_block(m.start, "PAUL_NOT_ASSIGNED")

            # NEGATIVE 5: two simultaneous assignments -> stop.
            update_campus(
                admin,
                f"{office}/HOBBYRAUM.md",
                assignment(base_sha, assignment_id="TEXT-PAUL-003"),
                "paul reassigned",
            )
            other = "protocol/PROJECT_MEMORY/PROJEKTE/PFERDE_ATELIER/BILD"
            update_campus(
                admin,
                f"{other}/HOBBYRAUM.md",
                assignment(base_sha, assignment_id="BILD-PAUL-001"),
                "second paul assignment",
            )
            expect_block(m.start, "PAUL_MULTIPLE_ASSIGNMENTS_BLOCKED")

            print(json.dumps({
                "ok": True,
                "status": "PAUL_CURRENT_CAMPUS_CI_PASS",
                "stale_local_branch_ignored": "PASS",
                "start_reads_latest_official_campus": "PASS",
                "relevant_task_drift_blocks": "PASS",
                "restart_refreshes_latest_campus": "PASS",
                "unrelated_change_does_not_false_block": "PASS",
                "current_state_drift_blocks": "PASS",
                "assignment_change_blocks": "PASS",
                "unassigned_blocks": "PASS",
                "multiple_assignments_block": "PASS"
            }, indent=2))
        finally:
            os.chdir(old_cwd)


if __name__ == "__main__":
    main()
