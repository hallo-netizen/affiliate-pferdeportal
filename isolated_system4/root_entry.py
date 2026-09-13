from __future__ import annotations
import hashlib, json, re, subprocess, sys
from pathlib import Path

SYSTEM4_ROOT_CONTRACT = 'SYSTEM4_ISOLATED_ROOT_ENTRY_V3'
HERE = Path(__file__).resolve().parent
REPO = HERE.parent
CODEX_ENTRY = HERE / 'codex_entry.py'
ROOT_AGENTS = REPO / 'AGENTS.md'
ROOT_OVERRIDE = REPO / 'AGENTS.override.md'
MARKER = 'SYSTEM4_ISOLATED_ROOT_ENTRY_V3'
ROOT_COMMAND_FILE = 'python3 isolated_system4/root_entry.py start'
ROOT_COMMAND_STDIN = 'python3 isolated_system4/root_entry.py start-stdin'
OLD_ENTRY_EXCLUSION = 'SYSTEM4 branch: DO NOT run `control/cloud-entry-gate/cloud_entry.py` before or instead of the System-4 root entry.'
MANIFEST_FIELD = 'system4_root_manifest_sha256'
CRITICAL_PATHS = (
    'AGENTS.md',
    'AGENTS.override.md',
    'isolated_system4/root_entry.py',
    'isolated_system4/codex_entry.py',
    'isolated_system4/controller.py',
    'isolated_system4/content_guard.py',
    'isolated_system4/design_guard.py',
    'isolated_system4/production_checks.py',
    'isolated_system4/batch_gate.py',
    'isolated_system4/batch_repetition_guard.py',
    'isolated_system4/handoff_transport.py',
    'isolated_system4/LT68Worker.java',
)

class EntryFail(RuntimeError):
    pass

def _within(child: Path, parent: Path) -> bool:
    child = child.resolve(); parent = parent.resolve()
    return child == parent or parent in child.parents

def _git(*args: str) -> str:
    try:
        cp = subprocess.run(['git', *args], cwd=REPO, text=True, capture_output=True, check=True)
        return cp.stdout.strip()
    except Exception as exc:
        raise EntryFail('ROOT_ENTRY_GIT_IDENTITY_UNAVAILABLE') from exc

def _critical_manifest_sha256() -> str:
    root = Path(_git('rev-parse','--show-toplevel')).resolve()
    if root != REPO.resolve():
        raise EntryFail('ROOT_ENTRY_GIT_ROOT_MISMATCH')
    _git('rev-parse','--verify','HEAD')
    tracked=set(_git('ls-files','--',*CRITICAL_PATHS).splitlines())
    missing_tracked=[rel for rel in CRITICAL_PATHS if rel not in tracked]
    if missing_tracked:
        raise EntryFail('ROOT_ENTRY_CRITICAL_FILE_UNTRACKED:'+missing_tracked[0])
    dirty=_git('status','--porcelain=v1','--untracked-files=no','--',*CRITICAL_PATHS)
    if dirty:
        raise EntryFail('ROOT_ENTRY_CRITICAL_FILES_DIRTY')
    rows=[]
    for rel in CRITICAL_PATHS:
        path=REPO/rel
        if not path.is_file():
            raise EntryFail('ROOT_ENTRY_CRITICAL_FILE_MISSING:'+rel)
        digest=hashlib.sha256(path.read_bytes()).hexdigest()
        rows.append(rel+'\0'+digest+'\n')
    return hashlib.sha256(''.join(rows).encode('utf-8')).hexdigest()

def _verify_common(workspace: Path) -> str:
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
    return _critical_manifest_sha256()

def _verify_snapshot_binding(value: dict, actual_manifest: str) -> None:
    expected=value.get(MANIFEST_FIELD)
    if expected is None:
        raise EntryFail('ROOT_ENTRY_MANIFEST_BINDING_MISSING')
    if not isinstance(expected,str) or not re.fullmatch(r'[0-9a-f]{64}',expected):
        raise EntryFail('ROOT_ENTRY_MANIFEST_BINDING_INVALID')
    if expected != actual_manifest:
        raise EntryFail('ROOT_ENTRY_MANIFEST_MISMATCH')

def _validate_snapshot_file(snapshot: Path, actual_manifest: str) -> dict:
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
    _verify_snapshot_binding(value,actual_manifest)
    return value

def _materialize_stdin_snapshot(workspace: Path, actual_manifest: str) -> Path:
    raw=sys.stdin.buffer.read()
    if not raw:
        raise EntryFail('ROOT_ENTRY_STDIN_SNAPSHOT_MISSING')
    try:
        value=json.loads(raw.decode('utf-8'))
    except Exception as exc:
        raise EntryFail('ROOT_ENTRY_STDIN_SNAPSHOT_JSON_INVALID') from exc
    if not isinstance(value,dict):
        raise EntryFail('ROOT_ENTRY_STDIN_SNAPSHOT_OBJECT_REQUIRED')
    _verify_snapshot_binding(value,actual_manifest)
    workspace.mkdir(parents=True,exist_ok=True)
    snapshot=workspace/'bound_snapshot.json'
    snapshot.write_bytes(raw)
    _validate_snapshot_file(snapshot,actual_manifest)
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
            manifest=_verify_common(workspace); _validate_snapshot_file(snapshot,manifest)
            return _start(snapshot,workspace)
        if command=='start-stdin':
            if len(argv)!=3:
                raise EntryFail('ROOT_ENTRY_BAD_COMMAND')
            workspace=Path(argv[2])
            manifest=_verify_common(workspace)
            snapshot=_materialize_stdin_snapshot(workspace,manifest)
            return _start(snapshot,workspace)
        raise EntryFail('ROOT_ENTRY_BAD_COMMAND')
    except EntryFail as exc:
        print('SYSTEM4_ROOT_ENTRY_FAIL:' + str(exc))
        return 2

if __name__ == '__main__':
    raise SystemExit(main(sys.argv))
