#!/usr/bin/env python3
from __future__ import annotations
import copy, hashlib, importlib.util, json, shutil, subprocess, tempfile
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
MODPATH = REPO / 'control/cloud-entry-gate/cloud_entry.py'
spec = importlib.util.spec_from_file_location('cloud_entry', MODPATH)
m = importlib.util.module_from_spec(spec)
spec.loader.exec_module(m)

def dump(p, o):
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(json.dumps(o, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')

def sha(p):
    return hashlib.sha256(p.read_bytes()).hexdigest()

def expect_block(fn, token):
    try:
        fn()
    except m.Blocked as e:
        assert token in str(e), (token, str(e))
        return
    raise AssertionError('expected block ' + token)

def current_refs(repo: Path):
    ptr = json.loads((repo / 'control/CURRENT_STARTMASTER.json').read_text())
    root_rel, state_rel = ptr['root_ref'], ptr['state_ref']
    state = json.loads((repo / state_rel).read_text())
    bundle_rel = state['execution_gate']['bundle_ref']
    return ptr, root_rel, state_rel, bundle_rel

def copy_current_repo(td: Path):
    r = td / 'repo'
    ptr, root_rel, state_rel, bundle_rel = current_refs(REPO)
    bundle = json.loads((REPO / bundle_rel).read_text())
    refs = ['control/CURRENT_STARTMASTER.json', root_rel, state_rel, bundle_rel]
    for row in bundle.get('authorized_inputs') or []:
        if isinstance(row, dict) and isinstance(row.get('ref'), str):
            refs.append(row['ref'])
    nb = bundle.get('next_binding')
    if isinstance(nb, dict) and isinstance(nb.get('bundle_ref'), str):
        refs.append(nb['bundle_ref'])
    for rel in dict.fromkeys(refs):
        src, dst = REPO / rel, r / rel
        dst.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(src, dst)
    return r, root_rel, state_rel, bundle_rel

def init_official_git(r: Path, origin='https://github.com/hallo-netizen/affiliate-pferdeportal.git'):
    subprocess.run(['git', 'init', '-q', str(r)], check=True)
    subprocess.run(['git', '-C', str(r), 'remote', 'add', 'origin', origin], check=True)

def bind_root(r: Path, root_rel: str, state_rel: str):
    rp, sp = r / root_rel, r / state_rel
    root = json.loads(rp.read_text())
    root['current_state_sha256'] = sha(sp)
    root['next_allowed_step'] = json.loads(sp.read_text())['next_allowed_step']
    dump(rp, root)

def receipt_from_capsule(r: Path, status='PASS', evidence=None):
    t = json.loads((r / '.pferde-capsule/TICKET.json').read_text())
    return {
        'contract': 'PFERDE_ATELIER_STEP_RECEIPT_V2',
        'ticket_id': t['ticket_id'],
        'step_id': t['step_id'],
        'sequence': t['sequence'],
        'state_sha256': t['state_sha256'],
        'bundle_sha256': t['bundle_sha256'],
        'status': status,
        'navigation_decision': False,
        'state_write_requested': False,
        'workflow_change_requested': False,
        'payload': {'ci': True},
        'evidence': evidence or ['CI_EVIDENCE'],
    }

def use_repo(r: Path):
    old = (m.REPO, m.POINTER, m.CAPSULE)
    m.REPO = r
    m.POINTER = r / 'control/CURRENT_STARTMASTER.json'
    m.CAPSULE = r / '.pferde-capsule'
    return old

def restore(old):
    m.REPO, m.POINTER, m.CAPSULE = old

def main():
    pos = m.verify()
    assert pos['status'] == 'CODEX_CLOUD_GATE_VERIFY_PASS'
    first = m.materialize()
    assert first['status'] == 'CODEX_CLOUD_ENTRANCE_PASS'
    ticket1 = json.loads((REPO / '.pferde-capsule/TICKET.json').read_text())
    first_again = m.materialize()
    ticket2 = json.loads((REPO / '.pferde-capsule/TICKET.json').read_text())
    assert ticket1 == ticket2, 'ticket must be deterministic across chat restart'
    manifest = json.loads((REPO / '.pferde-capsule/CAPSULE_MANIFEST.json').read_text())
    assert manifest['navigation_authority_exposed_to_worker'] is False
    assert manifest['worker_may_choose_next_step'] is False
    assert manifest['worker_state_write_authority'] is False
    assert manifest['workflow_change_authority'] is False
    assert manifest['repo_worktree_available_for_bound_step'] is True
    assert manifest['api_required'] is False
    shutil.rmtree(REPO / '.pferde-capsule')

    low = MODPATH.read_text(encoding='utf-8').lower()
    for token in ['pste', 'pserc', 'ppm', 'languagetool', 'wordpress', 'beratung', 'pflege', 'cannibal', 'api.openai.com', 'openai_api_key', 'requests.post', 'httpx.post', 'urllib.request']:
        assert token not in low, token

    with tempfile.TemporaryDirectory() as t:
        r, root_rel, state_rel, bundle_rel = copy_current_repo(Path(t))
        init_official_git(r)
        old = use_repo(r)
        try:
            assert m.verify()['status'] == 'CODEX_CLOUD_GATE_VERIFY_PASS'
            statep, rootp, bundlep = r / state_rel, r / root_rel, r / bundle_rel
            original_state = json.loads(statep.read_text())
            original_root = json.loads(rootp.read_text())
            original_bundle = json.loads(bundlep.read_text())

            m.materialize()
            before_step = original_state['next_allowed_step']
            rec = receipt_from_capsule(r, 'USER_ACTION_REQUIRED', ['NEEDS_USER'])
            rp = r / '.pferde-capsule/RECEIPT.json'
            dump(rp, rec)
            out = m.complete(rp)
            assert out['status'] == 'STEP_TERMINAL_NONPASS'
            assert out['state_advanced'] is False
            terminal_state = json.loads(statep.read_text())
            assert terminal_state['next_allowed_step'] == before_step
            assert terminal_state['execution_gate_terminal']['status'] == 'USER_ACTION_REQUIRED'
            restart = m.materialize()
            assert restart['status'] == 'STEP_ALREADY_TERMINAL_NONPASS'
            assert restart['step_status'] == 'USER_ACTION_REQUIRED'
            assert not (r / '.pferde-capsule').exists()
            dump(statep, original_state)
            dump(rootp, original_root)

            m.materialize(); rec = receipt_from_capsule(r); rec['navigation_decision'] = True; dump(rp, rec)
            expect_block(lambda: m.complete(rp), 'WORKER_NAVIGATION_DECISION_REJECTED')
            m.materialize(); rec = receipt_from_capsule(r); rec['state_write_requested'] = True; dump(rp, rec)
            expect_block(lambda: m.complete(rp), 'WORKER_STATE_WRITE_REJECTED')
            m.materialize(); rec = receipt_from_capsule(r); rec['workflow_change_requested'] = True; dump(rp, rec)
            expect_block(lambda: m.complete(rp), 'WORKER_WORKFLOW_CHANGE_REJECTED')
            m.materialize(); rec = receipt_from_capsule(r); rec['evidence'] = []; dump(rp, rec)
            expect_block(lambda: m.complete(rp), 'RECEIPT_EVIDENCE_INVALID')
            m.materialize(); rec = receipt_from_capsule(r); rec['step_id'] = 'SIDE_JUMP'; dump(rp, rec)
            expect_block(lambda: m.complete(rp), 'RECEIPT_BINDING_MISMATCH:step_id')

            nb = original_bundle.get('next_binding')
            if isinstance(nb, dict):
                m.materialize()
                rec = receipt_from_capsule(r, 'PASS', ['CURRENT_STEP_PASS'])
                first_pass_receipt = copy.deepcopy(rec)
                dump(rp, rec)
                out = m.complete(rp)
                assert out['status'] == 'STATE_ADVANCED_NEXT_STEP_READY'
                assert out['next_step_id'] == nb['step_id']
                assert out['next_sequence'] == int(nb['sequence'])
                state = json.loads(statep.read_text())
                assert state['next_allowed_step'] == nb['step_id']
                assert int(state['execution_gate']['sequence']) == int(nb['sequence'])
                assert json.loads(rootp.read_text())['current_state_sha256'] == sha(statep)
                dump(rp, first_pass_receipt)
                expect_block(lambda: m.complete(rp), 'RECEIPT_BINDING_MISMATCH')
                dump(statep, original_state)
                dump(rootp, original_root)

            b = copy.deepcopy(original_bundle); b['step_id'] = 'BACKTRACK'; dump(bundlep, b)
            expect_block(m.verify, 'BUNDLE_HASH_MISMATCH')
            dump(bundlep, original_bundle)
            s = copy.deepcopy(original_state); s['next_allowed_step'] = 'SIDE_JUMP'; dump(statep, s); bind_root(r, root_rel, state_rel)
            expect_block(m.verify, 'GATE_STEP_MISMATCH')
            dump(statep, original_state); dump(rootp, original_root)
            p = json.loads((r / 'control/CURRENT_STARTMASTER.json').read_text()); p['root_ref'] = '../escape.json'; dump(r / 'control/CURRENT_STARTMASTER.json', p)
            expect_block(m.verify, 'INVALID_RELATIVE_PATH')
        finally:
            restore(old)

    # Backup/archive execution boundary: hard positive/negative tests.
    with tempfile.TemporaryDirectory() as t:
        normal, _, _, _ = copy_current_repo(Path(t) / 'normal')
        init_official_git(normal)
        old = use_repo(normal)
        try:
            assert m.verify()['status'] == 'CODEX_CLOUD_GATE_VERIFY_PASS'
        finally:
            restore(old)

    for forbidden_name in ('Campus-Tresor', 'Campus-Archiv'):
        with tempfile.TemporaryDirectory() as t:
            r, _, _, _ = copy_current_repo(Path(t) / forbidden_name)
            init_official_git(r)
            old = use_repo(r)
            try:
                expect_block(m.verify, 'BACKUP_WORKSPACE_EXECUTION_BLOCKED')
            finally:
                restore(old)

    with tempfile.TemporaryDirectory() as t:
        r, _, _, _ = copy_current_repo(Path(t) / 'local-origin')
        init_official_git(r, origin='/Campus-Tresor/repository.git')
        old = use_repo(r)
        try:
            expect_block(m.verify, 'OFFICIAL_GITHUB_ORIGIN_REQUIRED')
        finally:
            restore(old)

    with tempfile.TemporaryDirectory() as t:
        r = Path(t) / 'mirror.git'
        subprocess.run(['git', 'init', '--bare', '-q', str(r)], check=True)
        old = use_repo(r)
        try:
            expect_block(m.verify, 'BARE_GIT_MIRROR_EXECUTION_BLOCKED')
        finally:
            restore(old)

    print(json.dumps({
        'ok': True,
        'status': 'CODEX_CLOUD_GATE_CI_PASS',
        'positive_negative': 'PASS',
        'current_startmaster_agnostic': True,
        'current_step_only_no_historical_chain_replay': True,
        'deterministic_chat_restart_ticket': 'PASS',
        'auto_advance_only_on_bound_pass': 'PASS',
        'terminal_nonpass_chat_restart_no_repeat': 'PASS',
        'api_required': False,
        'local_codex_required': False,
        'domain_logic_authority': 'NONE',
        'backup_archive_workspace_execution_blocked': 'PASS',
        'bare_mirror_execution_blocked': 'PASS',
        'local_mirror_origin_execution_blocked': 'PASS'
    }, indent=2))

if __name__ == '__main__':
    main()
