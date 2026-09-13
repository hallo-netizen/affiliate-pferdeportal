from __future__ import annotations
import json, subprocess, sys
from pathlib import Path

SYSTEM4_ROOT_CONTRACT = 'SYSTEM4_ISOLATED_ROOT_ENTRY_V3'
BRANCH = 'hobbyroom/system4-true-single-room-v1'
HERE = Path(__file__).resolve().parent
REPO = HERE.parent
CODEX_ENTRY = HERE / 'codex_entry.py'
ROOT_AGENTS = REPO / 'AGENTS.md'
ROOT_OVERRIDE = REPO / 'AGENTS.override.md'
MARKER = 'SYSTEM4_ISOLATED_ROOT_ENTRY_V3'
ROOT_COMMAND_FILE = 'python3 isolated_system4/root_entry.py start'
ROOT_COMMAND_STDIN = 'python3 isolated_system4/root_entry.py start-stdin'
OLD_ENTRY_EXCLUSION = 'SYSTEM4 branch: DO NOT run `control/cloud-entry-gate/cloud_entry.py` before or instead of the System-4 root entry.'

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

def _verify_common(workspace: Path) -> None:
    if _branch() != BRANCH:
        raise EntryFail('ROOT_ENTRY_BRANCH_NOT_SYSTEM4')
    if not ROOT_AGENTS.is_file():
        raise EntryFail('ROOT_AGENTS_MISSING')
    if not ROOT_OVERRIDE.is_file():
        raise EntryFail('ROOT_OVERRIDE_MISSING')
    base = ROOT_AGENTS.read_text(encoding='utf-8')
    text = ROOT_OVERRIDE.read_text(encoding='utf-8')
    if 'python3 control/cloud-entry-gate/cloud_entry.py start' not in base:
        raise EntryFail('ROOT_AGENTS_IMMUTABLE_GATE_MISSING')
    if MARKER not in text:
        raise EntryFail('ROOT_OVERRIDE_SYSTEM4_ROUTE_MISSING')
    if ROOT_COMMAND_FILE not in text or ROOT_COMMAND_STDIN not in text:
        raise EntryFail('ROOT_OVERRIDE_SYSTEM4_COMMAND_MISSING')
    if OLD_ENTRY_EXCLUSION not in text:
        raise EntryFail('ROOT_OVERRIDE_OLD_ENTRY_EXCLUSION_MISSING')
    if _within(workspace, REPO):
        raise EntryFail('ROOT_ENTRY_WORKSPACE_MUST_BE_OUTSIDE_REPO')

def _validate_snapshot_file(snapshot: Path) -> None:
    if not snapshot.is_file() or snapshot.suffix.lower() != '.json':
        raise EntryFail('ROOT_ENTRY_SNAPSHOT_INVALID')
    if _within(snapshot, REPO):
        raise EntryFail('ROOT_ENTRY_SNAPSHOT_MUST_BE_OUTSIDE_REPO')
    try:
        value=json.loads(snapshot.read_text(encoding='utf-8'))
    except Exception as exc:
        raise EntryFail('ROOT_ENTRY_SNAPSHOT_JSON_INVALID') from exc
    if not isinstance(value,dict):
        raise EntryFail('ROOT_ENTRY_SNAPSHOT_OBJECT_REQUIRED')

def _materialize_stdin_snapshot(workspace: Path) -> Path:
    raw=sys.stdin.buffer.read()
    if not raw:
        raise EntryFail('ROOT_ENTRY_STDIN_SNAPSHOT_MISSING')
    try:
        value=json.loads(raw.decode('utf-8'))
    except Exception as exc:
        raise EntryFail('ROOT_ENTRY_STDIN_SNAPSHOT_JSON_INVALID') from exc
    if not isinstance(value,dict):
        raise EntryFail('ROOT_ENTRY_STDIN_SNAPSHOT_OBJECT_REQUIRED')
    workspace.mkdir(parents=True,exist_ok=True)
    snapshot=workspace/'bound_snapshot.json'
    snapshot.write_bytes(raw)
    _validate_snapshot_file(snapshot)
    return snapshot

def _start(snapshot: Path, workspace: Path) -> int:
    p = subprocess.run([sys.executable, str(CODEX_ENTRY), 'start', str(snapshot), str(workspace)], text=True)
    if p.returncode:
        return p.returncode
    print('SYSTEM4_ROOT_ENTRY_PASS:RESEARCH_REQUIRED')
    return 0

def main(argv: list[str]) -> int:
    try:
        if len(argv) < 2:
            raise EntryFail('ROOT_ENTRY_BAD_COMMAND')
        command=argv[1]
        if command=='start':
            if len(argv)!=4:
                raise EntryFail('ROOT_ENTRY_BAD_COMMAND')
            snapshot=Path(argv[2]); workspace=Path(argv[3])
            _verify_common(workspace); _validate_snapshot_file(snapshot)
            return _start(snapshot,workspace)
        if command=='start-stdin':
            if len(argv)!=3:
                raise EntryFail('ROOT_ENTRY_BAD_COMMAND')
            workspace=Path(argv[2])
            _verify_common(workspace)
            snapshot=_materialize_stdin_snapshot(workspace)
            return _start(snapshot,workspace)
        raise EntryFail('ROOT_ENTRY_BAD_COMMAND')
    except EntryFail as exc:
        print('SYSTEM4_ROOT_ENTRY_FAIL:' + str(exc))
        return 2

if __name__ == '__main__':
    raise SystemExit(main(sys.argv))
