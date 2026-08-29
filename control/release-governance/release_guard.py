#!/usr/bin/env python3
import argparse
import hashlib
import json
import pathlib
import sys
import zipfile

POLICY_REL = pathlib.Path('control/release-governance/CURRENT_RELEASE.json')
CONTRACT = 'PFERDE_ATELIER_AFFILIATE_RELEASE_GOVERNANCE_V4'

class GuardError(RuntimeError):
    pass

def sha256_bytes(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()

def sha256_file(path: pathlib.Path) -> str:
    h = hashlib.sha256()
    with path.open('rb') as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b''):
            h.update(chunk)
    return h.hexdigest()

def load(root: pathlib.Path) -> dict:
    p = root / POLICY_REL
    if not p.is_file():
        raise GuardError('CURRENT_RELEASE_MISSING')
    try:
        d = json.loads(p.read_text(encoding='utf-8'))
    except Exception as exc:
        raise GuardError('CURRENT_RELEASE_INVALID_JSON:' + str(exc))
    if d.get('contract') != CONTRACT or d.get('mode') != 'ENFORCED' or d.get('workstream') != 'AFFILIATE_ZENTRALE':
        raise GuardError('GOVERNANCE_NOT_ENFORCED')
    required_true = (
        'no_guessing', 'no_reconstruction', 'no_side_refactor',
        'direct_committed_source_only', 'guard_is_verify_only',
        'no_release_zip_regeneration_before_final_gate'
    )
    for key in required_true:
        if d.get(key) is not True:
            raise GuardError('FAIL_CLOSED_FLAG_MISSING:' + key)
    objective = d.get('objective_control') or {}
    expected_objective = {
        'max_parallel_workstreams': 1,
        'microfix_policy': 'ONLY_IF_REQUIRED_BY_CURRENT_FAILED_BOUND_GATE',
        'new_version_policy': 'FORBIDDEN_UNLESS_CURRENT_BOUND_GATE_REQUIRES_CODE_CHANGE',
        'investigation_policy': 'ONLY_CURRENT_BOUND_GATE_OR_EXPLICIT_USER_SCOPE',
        'pass_reuse_policy': 'REUSE_HASH_IDENTICAL_PASS_EVIDENCE_DO_NOT_RERUN',
        'goal_drift_policy': 'FAIL_CLOSED',
        'optional_detours': 'FORBIDDEN',
    }
    for key, value in expected_objective.items():
        if objective.get(key) != value:
            raise GuardError('OBJECTIVE_CONTROL_WEAKENED:' + key)
    if not objective.get('north_star') or not objective.get('current_milestone'):
        raise GuardError('OBJECTIVE_CONTROL_MISSING')
    authority = d.get('source_authority') or {}
    if authority.get('type') != 'DIRECT_COMMITTED_TREE':
        raise GuardError('SOURCE_AUTHORITY_NOT_DIRECT_TREE')
    if authority.get('reconstruction') != 'FORBIDDEN':
        raise GuardError('RECONSTRUCTION_NOT_FORBIDDEN')
    return d

def verify_file(root: pathlib.Path, ref: str, digest: str, label: str) -> pathlib.Path:
    p = root / ref
    if not p.is_file():
        raise GuardError(label + '_MISSING:' + str(ref))
    got = sha256_file(p)
    if got != digest:
        raise GuardError(label + '_HASH_MISMATCH:' + got)
    return p

def manifest_rows(root: pathlib.Path, ref: str, digest: str, count: int, label: str):
    p = verify_file(root, ref, digest, label + '_MANIFEST')
    rows = []
    seen = set()
    for raw in p.read_text(encoding='utf-8').splitlines():
        if not raw.strip():
            continue
        parts = raw.split(None, 1)
        if len(parts) != 2 or len(parts[0]) != 64:
            raise GuardError(label + '_MANIFEST_FORMAT')
        rel = parts[1].strip().replace('\\', '/')
        if rel.startswith('/') or '..' in pathlib.PurePosixPath(rel).parts:
            raise GuardError(label + '_MANIFEST_PATH_INVALID:' + rel)
        if rel in seen:
            raise GuardError(label + '_MANIFEST_DUPLICATE:' + rel)
        seen.add(rel)
        rows.append((parts[0], rel))
    if len(rows) != int(count):
        raise GuardError(label + '_FILE_COUNT')
    return rows

def source_check(root: pathlib.Path, d=None):
    d = d or load(root)
    c = d['active_candidate']
    container_ref = c['source_container_root'].rstrip('/')
    plugin_ref = c['source_root'].rstrip('/')
    container = root / container_ref
    plugin = root / plugin_ref
    if not container.is_dir() or not plugin.is_dir():
        raise GuardError('CANONICAL_SOURCE_MISSING:' + plugin_ref)
    rows = manifest_rows(
        root,
        c['current_source_manifest_ref'],
        c['current_source_manifest_sha256'],
        c['source_file_count'],
        'CURRENT'
    )
    expected = sorted(rel for _, rel in rows)
    actual = sorted(
        p.relative_to(container).as_posix()
        for p in plugin.rglob('*') if p.is_file()
    )
    if actual != expected:
        missing = sorted(set(expected) - set(actual))
        extra = sorted(set(actual) - set(expected))
        raise GuardError('CURRENT_SOURCE_FILE_LIST:missing=' + ','.join(missing) + ';extra=' + ','.join(extra))
    for digest, rel in rows:
        p = container / rel
        if not p.is_file():
            raise GuardError('CURRENT_SOURCE_FILE_MISSING:' + rel)
        got = sha256_file(p)
        if got != digest:
            raise GuardError('CURRENT_SOURCE_HASH:' + rel + ':' + got)
    print('AFFILIATE_RELEASE_SOURCE_PASS')

def governance_check(root: pathlib.Path, d=None):
    d = d or load(root)
    for key, label in (('released_baseline', 'BASELINE'), ('negative_baseline', 'NEGATIVE')):
        x = d[key]
        manifest_rows(root, x['source_manifest_ref'], x['source_manifest_sha256'], x['source_file_count'], label)
        if x.get('authority') != 'HISTORICAL_EVIDENCE_ONLY':
            raise GuardError(label + '_AUTHORITY_INVALID')
    for ref in d.get('immutable_test_refs', []) + d.get('immutable_governance_refs', []):
        if not (root / ref).is_file():
            raise GuardError('IMMUTABLE_REF_MISSING:' + ref)
    state = d.get('execution_state') or {}
    if state.get('authorized_next_action') not in (
        'COMMIT_EXACT_V6638_21_FILE_SOURCE_TO_CANONICAL_ROOT',
        'RUN_BOUND_RELEASE_GATES',
        'FINALIZE_RELEASE'
    ):
        raise GuardError('AUTHORIZED_NEXT_ACTION_INVALID')
    print('AFFILIATE_RELEASE_GOVERNANCE_PASS')

def tree_check(root: pathlib.Path):
    d = load(root)
    governance_check(root, d)
    source_check(root, d)
    if d['active_candidate'].get('release_allowed') is True:
        release_check(root, d)
    print('AFFILIATE_RELEASE_TREE_PASS')

def release_check(root: pathlib.Path, d=None):
    d = d or load(root)
    governance_check(root, d)
    source_check(root, d)
    c = d['active_candidate']
    bad = []
    for name, gate in (d.get('required_release_gates') or {}).items():
        if not isinstance(gate, dict) or gate.get('status') != 'PASS':
            bad.append(name)
            continue
        ref = gate.get('evidence_ref')
        digest = gate.get('evidence_sha256')
        if gate.get('source_manifest_sha256') != c.get('current_source_manifest_sha256'):
            raise GuardError('EVIDENCE_SOURCE_BINDING_STALE:' + name)
        if not ref or not digest:
            raise GuardError('EVIDENCE_BINDING_MISSING:' + name)
        if not ref.startswith('release/affiliate-zentrale/evidence/'):
            raise GuardError('EVIDENCE_PATH_INVALID:' + name)
        verify_file(root, ref, digest, 'EVIDENCE_' + name)
    if bad:
        raise GuardError('RELEASE_GATES_OPEN:' + ','.join(bad))
    if c.get('release_allowed') is not True or c.get('status') != 'RELEASED':
        raise GuardError('RELEASE_STATE_NOT_ALLOWED')
    if (d.get('execution_state') or {}).get('authorized_next_action') != 'FINALIZE_RELEASE':
        raise GuardError('FINALIZE_STATE_NOT_BOUND')
    ref = c.get('final_artifact_ref')
    digest = c.get('final_artifact_sha256')
    if not ref or not digest or not ref.startswith('release/affiliate-zentrale/artifacts/final/'):
        raise GuardError('FINAL_ARTIFACT_BINDING_INVALID')
    artifact = verify_file(root, ref, digest, 'FINAL_ARTIFACT')
    rows = manifest_rows(root, c['current_source_manifest_ref'], c['current_source_manifest_sha256'], c['source_file_count'], 'FINAL')
    try:
        with zipfile.ZipFile(artifact) as zf:
            names = sorted(n for n in zf.namelist() if not n.endswith('/'))
            expected = sorted(rel for _, rel in rows)
            if names != expected:
                raise GuardError('FINAL_ZIP_FILE_LIST')
            for h, rel in rows:
                if sha256_bytes(zf.read(rel)) != h:
                    raise GuardError('FINAL_ZIP_SOURCE_HASH:' + rel)
    except zipfile.BadZipFile:
        raise GuardError('FINAL_ZIP_INVALID')
    print('AFFILIATE_RELEASE_FINAL_GATE_PASS')

def snapshot(root: pathlib.Path):
    out = {}
    for p in root.rglob('*'):
        if p.is_file() and '.git' not in p.parts:
            out[p.relative_to(root).as_posix()] = sha256_file(p)
    return out

def changes(base: pathlib.Path, head: pathlib.Path):
    b = snapshot(base)
    h = snapshot(head)
    return sorted(set(b) ^ set(h) | {k for k in set(b) & set(h) if b[k] != h[k]})

def starts(path: str, prefixes):
    return any(path.startswith(prefix) for prefix in prefixes)

def pr_check(base: pathlib.Path, head: pathlib.Path, head_ref: str, base_sha: str):
    bd = load(base)
    hd = load(head)
    ch = changes(base, head)
    sp = hd['scope_policy']
    bp = hd['branch_policy']
    if int(hd.get('generation', 0)) < int(bd.get('generation', 0)):
        raise GuardError('GOVERNANCE_ROLLBACK')
    for key in ('released_baseline', 'negative_baseline', 'immutable_snapshot_binding'):
        if hd[key] != bd[key]:
            raise GuardError(key.upper() + '_MUTATION_BLOCKED')
    oldrefs = bd.get('immutable_test_refs', []) + bd.get('immutable_governance_refs', [])
    newrefs = hd.get('immutable_test_refs', []) + hd.get('immutable_governance_refs', [])
    for ref in oldrefs:
        if ref not in newrefs:
            raise GuardError('IMMUTABLE_REF_LIST_WEAKENED:' + ref)
        if not (head / ref).is_file():
            raise GuardError('IMMUTABLE_REF_REMOVAL_BLOCKED:' + ref)
        if (base / ref).is_file() and sha256_file(base / ref) != sha256_file(head / ref):
            raise GuardError('IMMUTABLE_REF_MUTATION_BLOCKED:' + ref)
    scoped = [
        p for p in ch
        if starts(p, sp['release_scoped_prefixes'])
        or p == 'control/release-governance/CURRENT_RELEASE.json'
        or p.startswith('protocol/AFFILIATE_RELEASE_')
    ]
    if scoped and head_ref != bp['active_work_branch']:
        bootstrap = bp['bootstrap']
        if not (head_ref == bootstrap['branch'] and base_sha == bootstrap['base_sha'] and bootstrap.get('one_time_only') is True):
            raise GuardError('WRONG_RELEASE_WORK_BRANCH:' + head_ref)
    if head_ref == bp['active_work_branch']:
        bad = [p for p in ch if starts(p, sp['forbidden_prefixes'])]
        if bad:
            raise GuardError('FORBIDDEN_PATH_CHANGE:' + ','.join(bad))
        relevant = [
            p for p in ch
            if starts(p, sp['release_scoped_prefixes'])
            or p.startswith('control/release-governance/')
            or p.startswith('protocol/AFFILIATE_RELEASE_')
        ]
        bad = [p for p in relevant if not starts(p, sp['allowed_active_branch_prefixes'])]
        if bad:
            raise GuardError('ACTIVE_BRANCH_SCOPE_VIOLATION:' + ','.join(bad))
        state = bd.get('execution_state') or {}
        envelope = state.get('authorized_change_prefixes') or []
        scoped_changes = [p for p in relevant if p != 'protocol/AFFILIATE_RELEASE_']
        bad = [p for p in scoped_changes if not starts(p, envelope) and not p.startswith('protocol/AFFILIATE_RELEASE_')]
        if bad:
            raise GuardError('CURRENT_STEP_SCOPE_VIOLATION:' + ','.join(bad))
        if hd.get('execution_state') != bd.get('execution_state'):
            bound = state.get('next_state_binding') or {}
            hs = hd.get('execution_state') or {}
            for key in ('sequence', 'state', 'authorized_next_action', 'authorized_change_prefixes'):
                if hs.get(key) != bound.get(key):
                    raise GuardError('UNPREBOUND_EXECUTION_STATE_TRANSITION:' + key)
    governance_check(head, hd)
    if head_ref == bp['active_work_branch']:
        source_check(head, hd)
    print('AFFILIATE_RELEASE_PR_GUARD_PASS')

def start(root: pathlib.Path, branch: str):
    d = load(root)
    active = d['branch_policy']['active_work_branch']
    if branch != active:
        raise GuardError('WORK_BRANCH_REQUIRED:' + active)
    tree_check(root)
    print('AFFILIATE_RELEASE_START_PASS')

def main():
    ap = argparse.ArgumentParser()
    sub = ap.add_subparsers(dest='cmd', required=True)
    for name in ('governance-check', 'source-check', 'tree-check', 'release-check'):
        p = sub.add_parser(name)
        p.add_argument('--root', default='.')
    p = sub.add_parser('start')
    p.add_argument('--root', default='.')
    p.add_argument('--branch', required=True)
    p = sub.add_parser('pr-check')
    p.add_argument('--base', required=True)
    p.add_argument('--head', required=True)
    p.add_argument('--head-ref', required=True)
    p.add_argument('--base-sha', required=True)
    args = ap.parse_args()
    try:
        root = pathlib.Path(getattr(args, 'root', '.')).resolve()
        if args.cmd == 'governance-check':
            governance_check(root)
        elif args.cmd == 'source-check':
            source_check(root)
        elif args.cmd == 'tree-check':
            tree_check(root)
        elif args.cmd == 'release-check':
            release_check(root)
        elif args.cmd == 'start':
            start(root, args.branch)
        else:
            pr_check(pathlib.Path(args.base).resolve(), pathlib.Path(args.head).resolve(), args.head_ref, args.base_sha)
    except GuardError as exc:
        print('AFFILIATE_RELEASE_GUARD_BLOCKED:' + str(exc), file=sys.stderr)
        return 2
    return 0

if __name__ == '__main__':
    raise SystemExit(main())
