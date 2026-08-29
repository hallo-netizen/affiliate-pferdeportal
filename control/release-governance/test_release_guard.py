#!/usr/bin/env python3
import copy
import hashlib
import importlib.util
import json
import pathlib
import shutil
import tempfile
import zipfile

HERE = pathlib.Path(__file__).resolve().parent
spec = importlib.util.spec_from_file_location('rg', HERE / 'release_guard.py')
rg = importlib.util.module_from_spec(spec)
spec.loader.exec_module(rg)
TEMPLATE = json.loads((HERE / 'CURRENT_RELEASE.json').read_text(encoding='utf-8'))

def sha(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()

def write(path: pathlib.Path, data):
    path.parent.mkdir(parents=True, exist_ok=True)
    if isinstance(data, str):
        path.write_text(data, encoding='utf-8')
    else:
        path.write_bytes(data)

def build_root(with_source=True):
    td = tempfile.TemporaryDirectory()
    root = pathlib.Path(td.name) / 'repo'
    root.mkdir()
    d = copy.deepcopy(TEMPLATE)
    for key, name in (('released_baseline', 'BASELINE'), ('negative_baseline', 'NEGATIVE')):
        rel = f'{name.lower()}/one.txt'
        content = f'{name}\n'.encode()
        manifest = f'{sha(content)}  {rel}\n'
        mref = f'release/affiliate-zentrale/archive/{name}_MANIFEST.txt'
        write(root / mref, manifest)
        d[key]['source_manifest_ref'] = mref
        d[key]['source_manifest_sha256'] = sha(manifest.encode())
        d[key]['source_file_count'] = 1
    for ref in d['immutable_test_refs'] + d['immutable_governance_refs']:
        write(root / ref, ('immutable:' + ref + '\n').encode())
    files = {
        'affiliate-portal-router/a.php': b'<?php echo "a";\n',
        'affiliate-portal-router/readme.txt': b'fixture\n',
    }
    manifest = ''.join(f'{sha(data)}  {rel}\n' for rel, data in files.items())
    mref = 'release/affiliate-zentrale/CURRENT_SOURCE_SHA256.txt'
    write(root / mref, manifest)
    c = d['active_candidate']
    c['current_source_manifest_ref'] = mref
    c['current_source_manifest_sha256'] = sha(manifest.encode())
    c['source_file_count'] = len(files)
    c['source_container_root'] = 'release/affiliate-zentrale/current'
    c['source_root'] = 'release/affiliate-zentrale/current/affiliate-portal-router'
    d['source_authority']['container_root'] = c['source_container_root']
    d['source_authority']['plugin_root'] = c['source_root']
    d['source_authority']['manifest_ref'] = mref
    d['source_authority']['manifest_sha256'] = c['current_source_manifest_sha256']
    d['source_authority']['source_file_count'] = len(files)
    if with_source:
        for rel, data in files.items():
            write(root / c['source_container_root'] / rel, data)
    write(root / 'control/release-governance/CURRENT_RELEASE.json', json.dumps(d, indent=2) + '\n')
    return td, root, files

def policy(root):
    p = root / 'control/release-governance/CURRENT_RELEASE.json'
    return p, json.loads(p.read_text(encoding='utf-8'))

def save_policy(p, d):
    p.write_text(json.dumps(d, indent=2) + '\n', encoding='utf-8')

def blocked(fn, label):
    try:
        fn()
    except rg.GuardError:
        return
    raise AssertionError('expected block:' + label)

cases = 0
t, r, files = build_root(); rg.governance_check(r); cases += 1; t.cleanup()
t, r, files = build_root(); rg.source_check(r); cases += 1; t.cleanup()
t, r, files = build_root(); rg.tree_check(r); cases += 1; t.cleanup()
t, r, files = build_root(); blocked(lambda: rg.release_check(r), 'premature-release'); cases += 1; t.cleanup()
t, r, files = build_root(); blocked(lambda: rg.start(r, 'v6638-fix'), 'wrong-branch'); cases += 1; t.cleanup()
t, r, files = build_root(with_source=False); blocked(lambda: rg.source_check(r), 'missing-direct-source'); cases += 1; t.cleanup()
t, r, files = build_root(); p = r/'release/affiliate-zentrale/current/affiliate-portal-router/a.php'; p.write_text('tampered'); blocked(lambda: rg.source_check(r), 'tampered-source'); cases += 1; t.cleanup()
t, r, files = build_root(); write(r/'release/affiliate-zentrale/current/affiliate-portal-router/extra.php', 'x'); blocked(lambda: rg.source_check(r), 'extra-source'); cases += 1; t.cleanup()
t, r, files = build_root(); p,d=policy(r); d['no_reconstruction']=False; save_policy(p,d); blocked(lambda: rg.governance_check(r), 'reconstruction-flag'); cases += 1; t.cleanup()
t, r, files = build_root(); p,d=policy(r); d['source_authority']['type']='BASE64_CHUNKS'; save_policy(p,d); blocked(lambda: rg.governance_check(r), 'chunk-authority'); cases += 1; t.cleanup()
t, r, files = build_root(); p,d=policy(r); d['execution_state']['authorized_next_action']='INVESTIGATE_SOMETHING_ELSE'; save_policy(p,d); blocked(lambda: rg.governance_check(r), 'unbound-detour'); cases += 1; t.cleanup()
t, r, files = build_root(); p,d=policy(r); d['objective_control']['max_parallel_workstreams']=2; save_policy(p,d); blocked(lambda: rg.governance_check(r), 'parallel-workstreams'); cases += 1; t.cleanup()

t, r, files = build_root(); p,d=policy(r)
for name, gate in d['required_release_gates'].items():
    eref = f'release/affiliate-zentrale/evidence/{name}.txt'
    payload = ('PASS:' + name + '\n').encode()
    write(r/eref, payload)
    gate.update(status='PASS', evidence_ref=eref, evidence_sha256=sha(payload), source_manifest_sha256=d['active_candidate']['current_source_manifest_sha256'])
final_ref = 'release/affiliate-zentrale/artifacts/final/final.zip'
final_path = r/final_ref
final_path.parent.mkdir(parents=True, exist_ok=True)
with zipfile.ZipFile(final_path, 'w', compression=zipfile.ZIP_DEFLATED) as z:
    for rel,data in files.items(): z.writestr(rel,data)
d['active_candidate'].update(status='RELEASED', release_allowed=True, final_artifact_ref=final_ref, final_artifact_sha256=rg.sha256_file(final_path))
d['execution_state'].update(state='FINAL_RELEASE_BOUND', authorized_next_action='FINALIZE_RELEASE')
save_policy(p,d); rg.release_check(r); cases += 1; t.cleanup()

t, r, files = build_root(); p,d=policy(r)
for name, gate in d['required_release_gates'].items(): gate.update(status='PASS', evidence_ref='protocol/fake.txt', evidence_sha256='0'*64, source_manifest_sha256=d['active_candidate']['current_source_manifest_sha256'])
d['active_candidate'].update(status='RELEASED', release_allowed=True, final_artifact_ref='release/affiliate-zentrale/artifacts/final/no.zip', final_artifact_sha256='0'*64)
d['execution_state']['authorized_next_action']='FINALIZE_RELEASE'; save_policy(p,d)
blocked(lambda: rg.release_check(r), 'evidence-path'); cases += 1; t.cleanup()

a, base, _ = build_root(); b, head, _ = build_root()
shutil.rmtree(head); shutil.copytree(base, head)
q = head/'release/affiliate-zentrale/archive/BASELINE_MANIFEST.txt'; q.write_text(q.read_text()+'\n')
blocked(lambda: rg.pr_check(base, head, 'affiliate-release-current', 'base'), 'archive-scope'); cases += 1
a.cleanup(); b.cleanup()

print('AFFILIATE_RELEASE_GUARD_V4_TESTS_PASS:' + str(cases))
