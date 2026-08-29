#!/usr/bin/env python3
from __future__ import annotations
import copy, hashlib, importlib.util, json, shutil, tempfile
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

def copy_current_repo(td: Path):
    r = td / 'repo'
    ptr = json.loads((REPO / 'control/CURRENT_STARTMASTER.json').read_text())
    root_rel, state_rel = ptr['root_ref'], ptr['state_ref']
    refs = ['control/CURRENT_STARTMASTER.json', root_rel, state_rel]
    refs += [str(p.relative_to(REPO)) for p in (REPO / 'control/startmaster0107').glob('STEP_107*.json')]
    refs += ['control/startmaster0106/rootfix_input/ROOTFIX_40_40_EVIDENCE_SOURCE_V1.txt']
    for rel in refs:
        src, dst = REPO / rel, r / rel
        dst.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(src, dst)
    return r, root_rel, state_rel

def bind_root(r: Path, root_rel: str, state_rel: str):
    rp, sp = r / root_rel, r / state_rel
    root = json.loads(rp.read_text())
    root['current_state_sha256'] = sha(sp)
    root['next_allowed_step'] = json.loads(sp.read_text())['next_allowed_step']
    dump(rp, root)

def bind_current_bundle(r: Path, root_rel: str, state_rel: str):
    sp = r / state_rel
    state = json.loads(sp.read_text())
    bp = r / state['execution_gate']['bundle_ref']
    state['execution_gate']['bundle_sha256'] = sha(bp)
    dump(sp, state)
    bind_root(r, root_rel, state_rel)

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
        r, root_rel, state_rel = copy_current_repo(Path(t))
        old = use_repo(r)
        try:
            assert m.verify()['status'] == 'CODEX_CLOUD_GATE_VERIFY_PASS'
            statep, rootp = r / state_rel, r / root_rel
            original_state = json.loads(statep.read_text())
            original_root = json.loads(rootp.read_text())

            # Negative terminal: USER_ACTION_REQUIRED never advances and survives chat restart without rerunning the worker.
            m.materialize()
            before_step = json.loads(statep.read_text())['next_allowed_step']
            rec = receipt_from_capsule(r, 'USER_ACTION_REQUIRED', ['NEEDS_USER'])
            rp = r / '.pferde-capsule/RECEIPT.json'; dump(rp, rec)
            out = m.complete(rp)
            assert out['status'] == 'STEP_TERMINAL_NONPASS' and out['state_advanced'] is False
            terminal_state = json.loads(statep.read_text())
            assert terminal_state['next_allowed_step'] == before_step
            assert terminal_state['execution_gate_terminal']['status'] == 'USER_ACTION_REQUIRED'
            restart = m.materialize()
            assert restart['status'] == 'STEP_ALREADY_TERMINAL_NONPASS'
            assert restart['step_status'] == 'USER_ACTION_REQUIRED'
            assert not (r / '.pferde-capsule').exists()
            # Reset for independent receipt-authority negatives.
            dump(statep, original_state); dump(rootp, original_root)

            # Negative: fake navigation/state/workflow authority is rejected.
            m.materialize(); rec = receipt_from_capsule(r); rec['navigation_decision'] = True; dump(rp, rec)
            expect_block(lambda: m.complete(rp), 'WORKER_NAVIGATION_DECISION_REJECTED')
            m.materialize(); rec = receipt_from_capsule(r); rec['state_write_requested'] = True; dump(rp, rec)
            expect_block(lambda: m.complete(rp), 'WORKER_STATE_WRITE_REJECTED')
            m.materialize(); rec = receipt_from_capsule(r); rec['workflow_change_requested'] = True; dump(rp, rec)
            expect_block(lambda: m.complete(rp), 'WORKER_WORKFLOW_CHANGE_REJECTED')

            # Negative: empty evidence cannot PASS.
            m.materialize(); rec = receipt_from_capsule(r); rec['evidence'] = []; dump(rp, rec)
            expect_block(lambda: m.complete(rp), 'RECEIPT_EVIDENCE_INVALID')

            # Negative: ticket/step tampering cannot advance.
            m.materialize(); rec = receipt_from_capsule(r); rec['step_id'] = 'SIDE_JUMP'; dump(rp, rec)
            expect_block(lambda: m.complete(rp), 'RECEIPT_BINDING_MISMATCH:step_id')

            # Positive + anti-repeat: exact PASS advances one bound hop and stale receipt is rejected.
            m.materialize(); rec = receipt_from_capsule(r, 'PASS', ['ROOTFIX_TEST_PASS']); dump(rp, rec)
            first_pass_receipt = copy.deepcopy(rec)
            out = m.complete(rp)
            assert out['status'] == 'STATE_ADVANCED_NEXT_STEP_READY'
            assert out['next_sequence'] == 107002
            state = json.loads(statep.read_text())
            assert state['next_allowed_step'] == 'SAFE_SANDBOX_AUTO_REENTRY_AFTER_40_40_ROOTFIX'
            assert json.loads(rootp.read_text())['current_state_sha256'] == sha(statep)
            dump(rp, first_pass_receipt)
            expect_block(lambda: m.complete(rp), 'RECEIPT_BINDING_MISMATCH')

            # Reset and execute the complete real prebound 107001->107008 chain.
            dump(statep, original_state); dump(rootp, original_root)
            seen = []
            for expected_seq in range(107001, 107009):
                mat = m.materialize()
                assert mat['sequence'] == expected_seq
                seen.append(mat['step_id'])
                rec = receipt_from_capsule(r, 'PASS', [f'CHAIN_PASS_{expected_seq}']); dump(rp, rec)
                out = m.complete(rp)
                if expected_seq < 107008:
                    assert out['status'] == 'STATE_ADVANCED_NEXT_STEP_READY'
                    assert out['next_sequence'] == expected_seq + 1
                else:
                    assert out['status'] == 'FINAL_STEP_PASS'
                    assert out['state_advanced'] is False
            assert len(seen) == 8 and len(set(seen)) == 8
            final_state = json.loads(statep.read_text())
            assert final_state['next_allowed_step'] == 'FINAL_NEW_ARTICLE_BATCH_REVIEW_AWAIT_USER_PUBLISH'
            assert final_state['execution_gate']['sequence'] == 107008
            assert len(final_state.get('execution_gate_receipts', [])) == 8
            assert final_state['execution_gate_terminal']['status'] == 'PASS'
            final_restart = m.materialize()
            assert final_restart['status'] == 'FINAL_STEP_ALREADY_PASS'
            assert not (r / '.pferde-capsule').exists()

            # Negative: bundle tamper and side-jump state fail closed.
            dump(statep, original_state); dump(rootp, original_root)
            bundlep = r / original_state['execution_gate']['bundle_ref']
            b = json.loads(bundlep.read_text()); b['step_id'] = 'BACKTRACK'; dump(bundlep, b)
            expect_block(m.verify, 'BUNDLE_HASH_MISMATCH')
            shutil.copyfile(REPO / original_state['execution_gate']['bundle_ref'], bundlep)
            s = copy.deepcopy(original_state); s['next_allowed_step'] = 'SIDE_JUMP'; dump(statep, s); bind_root(r, root_rel, state_rel)
            expect_block(m.verify, 'GATE_STEP_MISMATCH')

            # Negative: path escape.
            dump(statep, original_state); dump(rootp, original_root)
            p = json.loads((r / 'control/CURRENT_STARTMASTER.json').read_text()); p['root_ref'] = '../escape.json'; dump(r / 'control/CURRENT_STARTMASTER.json', p)
            expect_block(m.verify, 'INVALID_RELATIVE_PATH')
        finally:
            restore(old)

    print(json.dumps({
        'ok': True,
        'status': 'CODEX_CLOUD_GATE_CI_PASS',
        'positive_negative': 'PASS',
        'full_prebound_chain_107001_107008': 'PASS',
        'deterministic_chat_restart_ticket': 'PASS',
        'auto_advance_only_on_bound_pass': 'PASS',
        'terminal_nonpass_chat_restart_no_repeat': 'PASS',
        'final_pass_chat_restart_no_repeat': 'PASS',
        'api_required': False,
        'local_codex_required': False,
        'domain_logic_authority': 'NONE'
    }, indent=2))

if __name__ == '__main__':
    main()
