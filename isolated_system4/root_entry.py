from __future__ import annotations
import subprocess, sys
from pathlib import Path

SYSTEM4_ROOT_CONTRACT = 'SYSTEM4_ISOLATED_ROOT_ENTRY_V1'
BRANCH = 'hobbyroom/system4-true-single-room-v1'
HERE = Path(__file__).resolve().parent
REPO = HERE.parent
CODEX_ENTRY = HERE / 'codex_entry.py'
ROOT_AGENTS = REPO / 'AGENTS.md'
MARKER = 'SYSTEM4_ISOLATED_ROOT_ENTRY_V1'

class EntryFail(RuntimeError):
    pass

def _within(child: Path, parent: Path) -> bool:
    child = child.resolve(); parent = parent.resolve()
    return child == parent or parent in child.parents

def _branch() -> str:
    try:
        return subprocess.run(['git','branch','--show-current'],cwd=REPO,text=True,capture_output=True,check=True).stdout.strip()
    except Exception as exc:
        raise EntryFail('ROOT_ENTRY_BRANCH_UNAVAILABLE') from exc

def verify_root_contract(snapshot: Path, workspace: Path) -> None:
    if _branch() != BRANCH:
        raise EntryFail('ROOT_ENTRY_BRANCH_NOT_SYSTEM4')
    if not ROOT_AGENTS.is_file():
        raise EntryFail('ROOT_AGENTS_MISSING')
    text = ROOT_AGENTS.read_text(encoding='utf-8')
    if MARKER not in text:
        raise EntryFail('ROOT_AGENTS_SYSTEM4_ROUTE_MISSING')
    if 'python3 isolated_system4/root_entry.py start' not in text:
        raise EntryFail('ROOT_AGENTS_SYSTEM4_COMMAND_MISSING')
    if 'SYSTEM4 task: DO NOT run control/cloud-entry-gate/cloud_entry.py' not in text:
        raise EntryFail('ROOT_AGENTS_OLD_ENTRY_EXCLUSION_MISSING')
    if not snapshot.is_file() or snapshot.suffix.lower() != '.json':
        raise EntryFail('ROOT_ENTRY_SNAPSHOT_INVALID')
    if _within(snapshot, REPO):
        raise EntryFail('ROOT_ENTRY_SNAPSHOT_MUST_BE_OUTSIDE_REPO')
    if _within(workspace, REPO):
        raise EntryFail('ROOT_ENTRY_WORKSPACE_MUST_BE_OUTSIDE_REPO')

def main(argv: list[str]) -> int:
    try:
        if len(argv) != 4 or argv[1] != 'start':
            raise EntryFail('ROOT_ENTRY_BAD_COMMAND')
        snapshot = Path(argv[2]); workspace = Path(argv[3])
        verify_root_contract(snapshot, workspace)
        p = subprocess.run([sys.executable, str(CODEX_ENTRY), 'start', str(snapshot), str(workspace)], text=True)
        if p.returncode:
            return p.returncode
        print('SYSTEM4_ROOT_ENTRY_PASS:RESEARCH_REQUIRED')
        return 0
    except EntryFail as exc:
        print('SYSTEM4_ROOT_ENTRY_FAIL:' + str(exc))
        return 2

if __name__ == '__main__':
    raise SystemExit(main(sys.argv))
