#!/usr/bin/env python3
"""Pferde Atelier content-blind execution gate V3 migration candidate.

Root-cause repair for the static-capsule/dynamic-handoff mismatch.
This module owns only state/action/artifact/test-evidence binding. It has no
editorial, SEO, content, quality, design, plugin or publish authority.
"""
from __future__ import annotations
import argparse, hashlib, json, secrets, shutil, sys, time
from pathlib import Path

class Blocked(RuntimeError):
    pass

TEST_ROLE_TO_KIND = {
    'POSITIVE_TEST_EVIDENCE': 'POSITIVE',
    'NEGATIVE_TEST_EVIDENCE': 'NEGATIVE',
    'FULL_WORKFLOW_REGRESSION_EVIDENCE': 'FULL_WORKFLOW_REGRESSION',
}

def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()

def load(path: Path):
    return json.loads(path.read_text(encoding='utf-8'))

def dump(path: Path, obj) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(obj, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')

def norm(value) -> str:
    return str(value or '').strip()

def rel(value) -> str:
    p = Path(norm(value))
    if not norm(value) or p.is_absolute() or '..' in p.parts:
        raise Blocked('INVALID_RELATIVE_PATH')
    return p.as_posix()

def safe(root: Path, value) -> Path:
    r = root.resolve()
    p = (root / rel(value)).resolve()
    if p != r and r not in p.parents:
        raise Blocked('PATH_ESCAPE')
    return p

def authority(master: Path):
    pointer_path = master / 'control' / 'CURRENT_STARTMASTER.json'
    if not pointer_path.is_file():
        raise Blocked('STARTMASTER_POINTER_MISSING')
    pointer = load(pointer_path)
    rootp = safe(master, pointer.get('root_ref'))
    statep = safe(master, pointer.get('state_ref'))
    if not rootp.is_file() or not statep.is_file():
        raise Blocked('ROOT_OR_STATE_MISSING')
    root, state = load(rootp), load(statep)
    if pointer.get('startmaster') != root.get('startmaster') or root.get('startmaster') != state.get('startmaster'):
        raise Blocked('STARTMASTER_IDENTITY_MISMATCH')
    if sha(statep) != root.get('current_state_sha256'):
        raise Blocked('STATE_HASH_MISMATCH')
    if root.get('next_allowed_step') != state.get('next_allowed_step'):
        raise Blocked('STEP_ROOT_STATE_MISMATCH')
    if state.get('publish_allowed') is not False or root.get('publish_allowed') is not False:
        raise Blocked('AUTO_PUBLISH_FORBIDDEN')
    gate = state.get('execution_gate') or {}
    if gate.get('enforced') is not True:
        raise Blocked('GATE_NOT_ENFORCED')
    if gate.get('step_id') != state.get('next_allowed_step'):
        raise Blocked('GATE_STEP_MISMATCH')
    if gate.get('state_write_authority') != 'ENTRANCE_GATE_ONLY':
        raise Blocked('STATE_WRITE_AUTHORITY_INVALID')
    if gate.get('unknown_step_policy') != 'DENY':
        raise Blocked('UNKNOWN_STEP_POLICY_INVALID')
    if gate.get('free_chat_direct_execution_valid') is not False:
        raise Blocked('FREE_CHAT_MUST_BE_INVALID')
    if gate.get('domain_logic_authority') != 'NONE' or gate.get('content_quality_design_authority') != 'NONE':
        raise Blocked('DOMAIN_AUTHORITY_MUST_BE_NONE')
    if gate.get('worker_context_policy') != 'CAPSULE_ONLY':
        raise Blocked('WORKER_CONTEXT_NOT_CAPSULE_ONLY')
    if gate.get('repeat_or_backtrack_policy') != 'DENY_UNLESS_PREBOUND_NEXT_BINDING':
        raise Blocked('BACKTRACK_POLICY_INVALID')
    if gate.get('api_dependency') != 'NONE':
        raise Blocked('API_DEPENDENCY_FORBIDDEN')
    if gate.get('hard_worker_target') != 'CODEX_CLOUD':
        raise Blocked('HARD_WORKER_NOT_CODEX_CLOUD')
    controller_ref = rel(gate.get('runtime_controller_ref'))
    controller_path = safe(master, controller_ref)
    if not controller_path.is_file():
        raise Blocked('RUNTIME_CONTROLLER_MISSING')
    if sha(controller_path) != gate.get('runtime_controller_sha256'):
        raise Blocked('RUNTIME_CONTROLLER_HASH_MISMATCH')
    bp = safe(master, gate.get('bundle_ref'))
    if not bp.is_file():
        raise Blocked('BUNDLE_MISSING')
    if sha(bp) != gate.get('bundle_sha256'):
        raise Blocked('BUNDLE_HASH_MISMATCH')
    bundle = load(bp)
    if bundle.get('step_id') != gate.get('step_id') or int(bundle.get('sequence', -1)) != int(gate.get('sequence', -2)):
        raise Blocked('BUNDLE_IDENTITY_MISMATCH')
    return pointer, rootp, statep, root, state, gate, bundle, bp

def _validate_role_list(value, token: str):
    if not isinstance(value, list) or any(not norm(v) for v in value) or len(value) != len(set(value)):
        raise Blocked(token)
    return [norm(v) for v in value]

def verify_static_inputs(master: Path, bundle: dict):
    out = []
    rows = bundle.get('authorized_inputs') or []
    if not isinstance(rows, list):
        raise Blocked('STATIC_INPUTS_INVALID')
    for i, row in enumerate(rows):
        if not isinstance(row, dict):
            raise Blocked(f'STATIC_INPUT_INVALID:{i}')
        p = safe(master, row.get('ref'))
        if not p.is_file():
            raise Blocked(f'STATIC_INPUT_MISSING:{i}')
        actual = sha(p)
        if actual != row.get('sha256'):
            raise Blocked(f'STATIC_INPUT_HASH_MISMATCH:{i}')
        out.append({'role': f'STATIC_{i+1:03d}', 'ref': rel(row['ref']), 'sha256': actual, 'size': p.stat().st_size})
    return out

def verify_next_input_manifest(master: Path, manifest_ref: str, expected_hash: str, current_step: str):
    mp = safe(master, manifest_ref)
    if not mp.is_file():
        raise Blocked('NEXT_INPUT_MANIFEST_MISSING')
    if sha(mp) != expected_hash:
        raise Blocked('NEXT_INPUT_MANIFEST_HASH_MISMATCH')
    data = load(mp)
    if data.get('contract') != 'PFERDE_ATELIER_NEXT_INPUT_V1':
        raise Blocked('NEXT_INPUT_CONTRACT_INVALID')
    if data.get('next_step_id') != current_step:
        raise Blocked('NEXT_INPUT_WRONG_TARGET_STEP')
    producer = norm(data.get('producer_step_id'))
    if not producer or int(data.get('producer_sequence', -1)) < 0:
        raise Blocked('NEXT_INPUT_PRODUCER_INVALID')
    rows = data.get('artifacts')
    if not isinstance(rows, list) or not rows:
        raise Blocked('NEXT_INPUT_ARTIFACTS_EMPTY')
    roles, refs = [], []
    payload = []
    for i, row in enumerate(rows):
        if not isinstance(row, dict):
            raise Blocked(f'NEXT_INPUT_ARTIFACT_INVALID:{i}')
        role = norm(row.get('role')); rr = rel(row.get('ref'))
        if not role:
            raise Blocked(f'NEXT_INPUT_ARTIFACT_ROLE_INVALID:{i}')
        roles.append(role); refs.append(rr)
        p = safe(master, rr)
        if not p.is_file():
            raise Blocked(f'NEXT_INPUT_ARTIFACT_MISSING:{i}')
        actual = sha(p)
        if actual != row.get('sha256'):
            raise Blocked(f'NEXT_INPUT_ARTIFACT_HASH_MISMATCH:{i}')
        payload.append({'role': role, 'ref': rr, 'sha256': actual, 'size': p.stat().st_size})
    if len(roles) != len(set(roles)):
        raise Blocked('NEXT_INPUT_DUPLICATE_ARTIFACT_ROLE')
    if len(refs) != len(set(refs)):
        raise Blocked('NEXT_INPUT_DUPLICATE_ARTIFACT_REF')
    return {'manifest': {'role': 'NEXT_INPUT', 'ref': rel(manifest_ref), 'sha256': expected_hash, 'size': mp.stat().st_size}, 'payload': payload, 'producer_step_id': producer, 'producer_sequence': int(data['producer_sequence'])}

def verify_runtime_inputs(master: Path, state: dict, bundle: dict):
    required = _validate_role_list(bundle.get('required_runtime_input_roles') or [], 'REQUIRED_RUNTIME_ROLES_INVALID')
    rows = state.get('runtime_inputs') or []
    if not isinstance(rows, list):
        raise Blocked('RUNTIME_INPUTS_INVALID')
    roles = [norm(x.get('role')) for x in rows if isinstance(x, dict)]
    if roles != required:
        raise Blocked('RUNTIME_INPUT_ROLE_MISMATCH')
    copied = []
    for i, row in enumerate(rows):
        if not isinstance(row, dict):
            raise Blocked(f'RUNTIME_INPUT_INVALID:{i}')
        role = norm(row.get('role'))
        if role == 'NEXT_INPUT':
            verified = verify_next_input_manifest(master, row.get('ref'), row.get('sha256'), state.get('next_allowed_step'))
            copied.append(verified['manifest'])
            copied.extend({'role': f"NEXT_INPUT::{x['role']}", **{k:v for k,v in x.items() if k!='role'}} for x in verified['payload'])
        else:
            p = safe(master, row.get('ref'))
            if not p.is_file():
                raise Blocked(f'RUNTIME_INPUT_MISSING:{i}')
            actual = sha(p)
            if actual != row.get('sha256'):
                raise Blocked(f'RUNTIME_INPUT_HASH_MISMATCH:{i}')
            copied.append({'role': role, 'ref': rel(row['ref']), 'sha256': actual, 'size': p.stat().st_size})
    return copied

def verify_regression_baseline(master: Path, bundle: dict):
    row = bundle.get('regression_baseline')
    if not isinstance(row, dict):
        raise Blocked('REGRESSION_BASELINE_BINDING_MISSING')
    p = safe(master, row.get('ref'))
    if not p.is_file():
        raise Blocked('REGRESSION_BASELINE_MISSING')
    actual = sha(p)
    if actual != row.get('sha256'):
        raise Blocked('REGRESSION_BASELINE_HASH_MISMATCH')
    data = load(p)
    if data.get('contract') != 'PFERDE_ATELIER_FULL_WORKFLOW_REGRESSION_BASELINE_V1':
        raise Blocked('REGRESSION_BASELINE_CONTRACT_INVALID')
    return {'role':'REGRESSION_BASELINE','ref':rel(row['ref']),'sha256':actual,'size':p.stat().st_size}

def build_ticket(statep: Path, bp: Path, state: dict, gate: dict):
    ticket = {
        'contract': 'PFERDE_ATELIER_EXECUTION_TICKET_V3',
        'startmaster': state['startmaster'], 'step_id': state['next_allowed_step'],
        'sequence': int(gate['sequence']), 'state_sha256': sha(statep), 'bundle_sha256': sha(bp),
        'nonce': secrets.token_hex(16), 'issued_at_unix': int(time.time()),
    }
    ticket['ticket_id'] = hashlib.sha256(json.dumps(ticket, sort_keys=True, separators=(',', ':')).encode()).hexdigest()
    return ticket

def issue(master: Path, outdir: Path):
    _, _, statep, _, state, gate, bundle, bp = authority(master)
    static = verify_static_inputs(master, bundle)
    baseline = verify_regression_baseline(master, bundle)
    runtime = verify_runtime_inputs(master, state, bundle)
    if outdir.exists():
        if any(outdir.iterdir()):
            raise Blocked('CAPSULE_OUTPUT_NOT_EMPTY')
    else:
        outdir.mkdir(parents=True)
    (outdir / 'inputs').mkdir()
    copied = []
    for n, row in enumerate(static + [baseline] + runtime, 1):
        src = safe(master, row['ref'])
        dst = outdir / 'inputs' / f'{n:03d}_{src.name}'
        shutil.copyfile(src, dst); dst.chmod(0o444)
        copied.append({'role': row['role'], 'capsule_path': f'inputs/{dst.name}', 'sha256': row['sha256'], 'source_ref': row['ref']})
    ticket = build_ticket(statep, bp, state, gate)
    ins = norm(bundle.get('instruction'))
    if not ins:
        raise Blocked('INSTRUCTION_MISSING')
    required_results = _validate_role_list(bundle.get('required_result_roles') or [], 'REQUIRED_RESULT_ROLES_INVALID')
    handoff_results = _validate_role_list(bundle.get('handoff_result_roles') or [], 'HANDOFF_RESULT_ROLES_INVALID')
    if not set(handoff_results) <= set(required_results):
        raise Blocked('HANDOFF_RESULT_NOT_REQUIRED_RESULT')
    (outdir / 'INSTRUCTION.txt').write_text(ins + '\n', encoding='utf-8')
    dump(outdir / 'TICKET.json', ticket)
    next_binding = bundle.get('next_binding') if isinstance(bundle.get('next_binding'), dict) else None
    dump(outdir / 'WORKER_OUTPUT_CONTRACT.json', {
        'contract':'PFERDE_ATELIER_WORKER_OUTPUT_CONTRACT_V1',
        'receipt_contract':'PFERDE_ATELIER_STEP_RECEIPT_V3',
        'result_manifest_contract':'PFERDE_ATELIER_STEP_RESULT_MANIFEST_V3',
        'test_evidence_contract':'PFERDE_ATELIER_TEST_EVIDENCE_V1',
        'next_input_contract':'PFERDE_ATELIER_NEXT_INPUT_V1',
        'step_id':ticket['step_id'],'sequence':ticket['sequence'],
        'required_result_roles':required_results,'handoff_result_roles':handoff_results,
        'next_step_id': next_binding.get('step_id') if next_binding else None,
        'regression_baseline_sha256':baseline['sha256'],
        'worker_forbidden':{'navigation_decision':True,'state_write_requested':True,'workflow_change_requested':True},
        'test_rule':'ALL_CHECK_ROWS_MUST_HAVE_STATUS_PASS_AND_BASELINE_SHA_MUST_MATCH'
    })
    dump(outdir / 'CAPSULE_MANIFEST.json', {
        'contract': 'PFERDE_ATELIER_EXECUTION_CAPSULE_V3', 'ticket': ticket, 'inputs': copied,
        'isolation_policy': {'context': 'CAPSULE_ONLY', 'master_tree_exposed': False, 'history_exposed': False,
          'navigation_authority_exposed_to_worker': False, 'worker_may_choose_next_step': False,
          'worker_state_write_authority': False, 'workflow_change_authority': False},
        'required_result_roles': required_results, 'handoff_result_roles': handoff_results,
        'regression_baseline_sha256': baseline['sha256'],
    })
    return {'ok': True, 'status': 'CAPSULE_ISSUED', 'step_id': ticket['step_id'], 'sequence': ticket['sequence'], 'input_count': len(copied), 'static_input_count': len(static), 'runtime_materialized_file_count': len(runtime), 'regression_baseline_sha256': baseline['sha256']}

def validate_receipt(ticket: dict, receipt: dict):
    required = {'contract','ticket_id','step_id','sequence','state_sha256','bundle_sha256','status','navigation_decision','state_write_requested','workflow_change_requested','payload','evidence'}
    if set(receipt) != required:
        raise Blocked('RECEIPT_FIELDS_INVALID')
    if receipt.get('contract') != 'PFERDE_ATELIER_STEP_RECEIPT_V3':
        raise Blocked('RECEIPT_CONTRACT_INVALID')
    for key in ['ticket_id','step_id','sequence','state_sha256','bundle_sha256']:
        if receipt.get(key) != ticket.get(key):
            raise Blocked('RECEIPT_BINDING_MISMATCH:' + key)
    if receipt.get('status') not in {'PASS','BLOCKED','USER_ACTION_REQUIRED'}:
        raise Blocked('RECEIPT_STATUS_INVALID')
    if receipt.get('navigation_decision') is not False:
        raise Blocked('WORKER_NAVIGATION_REJECTED')
    if receipt.get('state_write_requested') is not False:
        raise Blocked('WORKER_STATE_WRITE_REJECTED')
    if receipt.get('workflow_change_requested') is not False:
        raise Blocked('WORKER_WORKFLOW_CHANGE_REJECTED')
    if not isinstance(receipt.get('payload'), dict) or not isinstance(receipt.get('evidence'), list):
        raise Blocked('RECEIPT_PAYLOAD_OR_EVIDENCE_INVALID')

def _verify_test_evidence(master: Path, row: dict, ticket: dict, bundle: dict):
    role = norm(row.get('role')); kind = TEST_ROLE_TO_KIND[role]
    p = safe(master, row.get('ref'))
    data = load(p)
    if data.get('contract') != 'PFERDE_ATELIER_TEST_EVIDENCE_V1':
        raise Blocked('TEST_EVIDENCE_CONTRACT_INVALID:' + role)
    if data.get('kind') != kind or data.get('status') != 'PASS':
        raise Blocked('TEST_EVIDENCE_NOT_PASS:' + role)
    if data.get('step_id') != ticket['step_id'] or int(data.get('sequence', -1)) != ticket['sequence']:
        raise Blocked('TEST_EVIDENCE_STEP_BINDING_MISMATCH:' + role)
    if not isinstance(data.get('checks'), list) or not data['checks']:
        raise Blocked('TEST_EVIDENCE_CHECKS_EMPTY:' + role)
    if any(not isinstance(c,dict) or not norm(c.get('name')) or c.get('status')!='PASS' for c in data['checks']):
        raise Blocked('TEST_EVIDENCE_CHECK_NOT_PASS:' + role)
    baseline = bundle.get('regression_baseline') or {}
    if data.get('baseline_sha256') != baseline.get('sha256'):
        raise Blocked('TEST_EVIDENCE_BASELINE_MISMATCH:' + role)

def verify_result_manifest(master: Path, bundle: dict, ticket: dict, manifest: dict):
    if manifest.get('contract') != 'PFERDE_ATELIER_STEP_RESULT_MANIFEST_V3':
        raise Blocked('RESULT_MANIFEST_CONTRACT_INVALID')
    for key in ['ticket_id','step_id','sequence','state_sha256','bundle_sha256']:
        if manifest.get(key) != ticket.get(key):
            raise Blocked('RESULT_MANIFEST_BINDING_MISMATCH:' + key)
    nb = bundle.get('next_binding')
    expected_next = nb.get('step_id') if isinstance(nb, dict) else None
    if manifest.get('next_step_id') != expected_next:
        raise Blocked('RESULT_MANIFEST_NEXT_STEP_MISMATCH')
    rows = manifest.get('artifacts')
    if not isinstance(rows, list):
        raise Blocked('RESULT_ARTIFACTS_INVALID')
    required = _validate_role_list(bundle.get('required_result_roles') or [], 'REQUIRED_RESULT_ROLES_INVALID')
    roles = [norm(x.get('role')) for x in rows if isinstance(x, dict)]
    refs = [rel(x.get('ref')) for x in rows if isinstance(x, dict)]
    if roles != required:
        raise Blocked('RESULT_ROLE_MISMATCH')
    if len(refs) != len(set(refs)):
        raise Blocked('RESULT_DUPLICATE_REF')
    out = []
    for i, row in enumerate(rows):
        p = safe(master, row.get('ref'))
        if not p.is_file():
            raise Blocked(f'RESULT_ARTIFACT_MISSING:{i}')
        actual = sha(p)
        if actual != row.get('sha256'):
            raise Blocked(f'RESULT_ARTIFACT_HASH_MISMATCH:{i}')
        role = row['role']
        if role in TEST_ROLE_TO_KIND:
            _verify_test_evidence(master, row, ticket, bundle)
        elif role == 'NEXT_INPUT':
            data = load(p)
            if data.get('contract') != 'PFERDE_ATELIER_NEXT_INPUT_V1':
                raise Blocked('NEXT_INPUT_RESULT_CONTRACT_INVALID')
            if data.get('producer_step_id') != ticket['step_id'] or int(data.get('producer_sequence', -1)) != ticket['sequence'] or data.get('next_step_id') != expected_next:
                raise Blocked('NEXT_INPUT_RESULT_BINDING_MISMATCH')
            # Validate every payload now, not only at next start.
            verify_next_input_manifest(master, row['ref'], actual, expected_next)
        out.append({'role': role, 'ref': rel(row['ref']), 'sha256': actual})
    return out

def _persist_transition_evidence(master: Path, ticket_path: Path, receipt_path: Path, result_manifest_path: Path, ticket: dict):
    # Entrance-controller-owned evidence copy. Worker never writes state.
    dest = master / 'control' / 'execution-evidence' / f"{ticket['sequence']}_{ticket['ticket_id']}"
    if dest.exists():
        raise Blocked('TRANSITION_EVIDENCE_ALREADY_EXISTS')
    dest.mkdir(parents=True)
    for name, src in [('TICKET.json', ticket_path), ('RECEIPT.json', receipt_path), ('RESULT_MANIFEST.json', result_manifest_path)]:
        shutil.copyfile(src, dest / name)
    return {
        'ticket_ref': str((dest/'TICKET.json').relative_to(master)).replace('\\','/'), 'ticket_sha256': sha(dest/'TICKET.json'),
        'receipt_ref': str((dest/'RECEIPT.json').relative_to(master)).replace('\\','/'), 'receipt_sha256': sha(dest/'RECEIPT.json'),
        'result_manifest_ref': str((dest/'RESULT_MANIFEST.json').relative_to(master)).replace('\\','/'), 'result_manifest_sha256': sha(dest/'RESULT_MANIFEST.json'),
    }

def advance(master: Path, ticket_path: Path, receipt_path: Path, result_manifest_path: Path):
    _, rootp, statep, root, state, gate, bundle, bp = authority(master)
    ticket, receipt = load(ticket_path), load(receipt_path)
    if ticket.get('state_sha256') != sha(statep) or ticket.get('bundle_sha256') != sha(bp) or ticket.get('step_id') != state.get('next_allowed_step'):
        raise Blocked('TICKET_NOT_CURRENT')
    validate_receipt(ticket, receipt)
    if receipt.get('status') != 'PASS':
        raise Blocked('ADVANCE_REQUIRES_PASS')
    if result_manifest_path is None or not result_manifest_path.is_file():
        raise Blocked('RESULT_MANIFEST_REQUIRED')
    results = verify_result_manifest(master, bundle, ticket, load(result_manifest_path))
    if receipt['payload'].get('result_manifest_sha256') != sha(result_manifest_path):
        raise Blocked('RECEIPT_RESULT_MANIFEST_HASH_MISMATCH')
    handoff_roles = _validate_role_list(bundle.get('handoff_result_roles') or [], 'HANDOFF_RESULT_ROLES_INVALID')
    handoff = [x for x in results if x['role'] in handoff_roles]
    nb = bundle.get('next_binding')
    ev = _persist_transition_evidence(master, ticket_path, receipt_path, result_manifest_path, ticket)
    history = state.setdefault('execution_gate_receipts', [])
    history.append({'completed_step_id': ticket['step_id'], 'sequence': ticket['sequence'], 'ticket_id': ticket['ticket_id'], **ev, 'result_artifacts': results})
    if nb is None:
        if handoff:
            raise Blocked('TERMINAL_HANDOFF_FORBIDDEN')
        if state.get('publish_allowed') is not False:
            raise Blocked('AUTO_PUBLISH_FORBIDDEN')
        state['status'] = 'FINAL_REVIEW_COMPLETE_AWAIT_USER_PUBLISH'
        state['runtime_inputs'] = []
        dump(statep, state); root['current_state_sha256'] = sha(statep); dump(rootp, root)
        return {'ok': True, 'status': 'TERMINAL_REVIEW_RECORDED_NO_PUBLISH', 'step_id': ticket['step_id']}
    nextp = safe(master, nb.get('bundle_ref'))
    if not nextp.is_file() or sha(nextp) != nb.get('bundle_sha256'):
        raise Blocked('NEXT_BUNDLE_HASH_MISMATCH')
    nxt = load(nextp)
    if nxt.get('step_id') != nb.get('step_id') or int(nxt.get('sequence', -1)) != int(nb.get('sequence', -2)):
        raise Blocked('NEXT_BUNDLE_IDENTITY_MISMATCH')
    if int(nb['sequence']) <= int(gate['sequence']):
        raise Blocked('NON_MONOTONIC_SEQUENCE')
    expected = _validate_role_list(nxt.get('required_runtime_input_roles') or [], 'NEXT_REQUIRED_RUNTIME_ROLES_INVALID')
    if [x['role'] for x in handoff] != expected:
        raise Blocked('NEXT_RUNTIME_ROLE_CONTRACT_MISMATCH')
    state['next_allowed_step'] = nb['step_id']; state['runtime_inputs'] = handoff; state['generated_at_utc'] = time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime())
    g = state['execution_gate']; g['step_id'] = nb['step_id']; g['sequence'] = nb['sequence']; g['bundle_ref'] = nb['bundle_ref']; g['bundle_sha256'] = nb['bundle_sha256']
    dump(statep, state); root['current_state_sha256'] = sha(statep); root['next_allowed_step'] = nb['step_id']; dump(rootp, root)
    return {'ok': True, 'status': 'STATE_ADVANCED_BY_ENTRANCE_CONTROLLER', 'next_step_id': nb['step_id'], 'sequence': nb['sequence'], 'runtime_input_count': len(handoff), 'evidence_recorded': True}

def verify(master: Path):
    _, _, _, _, state, gate, bundle, _ = authority(master)
    static = verify_static_inputs(master, bundle); baseline=verify_regression_baseline(master,bundle); runtime = verify_runtime_inputs(master, state, bundle)
    return {'ok': True, 'status': 'AUTHORITY_PASS', 'step_id': state['next_allowed_step'], 'sequence': gate['sequence'], 'static_input_count': len(static), 'runtime_materialized_file_count': len(runtime), 'regression_baseline_sha256':baseline['sha256'],'publish_allowed': False}

def main():
    ap = argparse.ArgumentParser(); sub = ap.add_subparsers(dest='cmd', required=True)
    p = sub.add_parser('issue'); p.add_argument('--master', required=True); p.add_argument('--out', required=True)
    p = sub.add_parser('verify'); p.add_argument('--master', required=True)
    p = sub.add_parser('advance'); p.add_argument('--master', required=True); p.add_argument('--ticket', required=True); p.add_argument('--receipt', required=True); p.add_argument('--result-manifest', required=True)
    args = ap.parse_args()
    try:
        if args.cmd == 'issue': out = issue(Path(args.master), Path(args.out))
        elif args.cmd == 'verify': out = verify(Path(args.master))
        else: out = advance(Path(args.master), Path(args.ticket), Path(args.receipt), Path(args.result_manifest))
        print(json.dumps(out, ensure_ascii=False, indent=2)); return 0
    except Blocked as exc:
        print(json.dumps({'ok': False, 'status': 'BLOCKED', 'reason': str(exc)}, ensure_ascii=False, indent=2)); return 2
if __name__ == '__main__':
    raise SystemExit(main())
