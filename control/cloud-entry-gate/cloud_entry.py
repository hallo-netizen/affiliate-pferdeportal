#!/usr/bin/env python3
from __future__ import annotations
import hashlib, json, shutil, sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[2]
POINTER = REPO / 'control/CURRENT_STARTMASTER.json'
CAPSULE = REPO / '.pferde-capsule'
RECEIPT_NAME = 'RECEIPT.json'

class Blocked(RuntimeError):
    pass

def sha(p: Path) -> str:
    return hashlib.sha256(p.read_bytes()).hexdigest()

def stable_hash(obj) -> str:
    raw = json.dumps(obj, ensure_ascii=False, sort_keys=True, separators=(',', ':')).encode('utf-8')
    return hashlib.sha256(raw).hexdigest()

def load(p: Path):
    return json.loads(p.read_text(encoding='utf-8'))

def dump_atomic(p: Path, obj) -> None:
    p.parent.mkdir(parents=True, exist_ok=True)
    tmp = p.with_name(p.name + '.tmp')
    tmp.write_text(json.dumps(obj, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    tmp.replace(p)

def rel(v: str) -> Path:
    p = Path(str(v or ''))
    if not str(v or '') or p.is_absolute() or '..' in p.parts:
        raise Blocked('INVALID_RELATIVE_PATH')
    return p

def authority():
    if not POINTER.is_file():
        raise Blocked('STARTMASTER_POINTER_MISSING')
    ptr = load(POINTER)
    rootp = REPO / rel(ptr.get('root_ref'))
    statep = REPO / rel(ptr.get('state_ref'))
    if not rootp.is_file() or not statep.is_file():
        raise Blocked('ROOT_OR_STATE_MISSING')
    root, state = load(rootp), load(statep)
    if ptr.get('startmaster') != root.get('startmaster') or root.get('startmaster') != state.get('startmaster'):
        raise Blocked('STARTMASTER_IDENTITY_MISMATCH')
    state_hash = sha(statep)
    if state_hash != root.get('current_state_sha256'):
        raise Blocked('STATE_HASH_MISMATCH')
    if root.get('next_allowed_step') != state.get('next_allowed_step'):
        raise Blocked('STEP_ROOT_STATE_MISMATCH')
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
    if gate.get('worker_context_policy') not in {'CAPSULE_ONLY', 'CAPSULE_NAVIGATION_REPO_BOUND_STEP'}:
        raise Blocked('WORKER_CONTEXT_POLICY_INVALID')
    if gate.get('hard_worker_target') != 'CODEX_CLOUD':
        raise Blocked('HARD_WORKER_NOT_CODEX_CLOUD')
    if gate.get('api_dependency') != 'NONE':
        raise Blocked('API_DEPENDENCY_FORBIDDEN')
    bp = REPO / rel(gate.get('bundle_ref'))
    if not bp.is_file():
        raise Blocked('BUNDLE_MISSING')
    bundle_hash = sha(bp)
    if bundle_hash != gate.get('bundle_sha256'):
        raise Blocked('BUNDLE_HASH_MISMATCH')
    bundle = load(bp)
    if bundle.get('step_id') != gate.get('step_id') or int(bundle.get('sequence', -1)) != int(gate.get('sequence', -2)):
        raise Blocked('BUNDLE_IDENTITY_MISMATCH')
    return ptr, root, state, gate, bundle, bp, rootp, statep, state_hash, bundle_hash

def verify_inputs(bundle):
    rows = []
    for i, row in enumerate(bundle.get('authorized_inputs') or []):
        if not isinstance(row, dict):
            raise Blocked(f'INPUT_INVALID:{i}')
        p = REPO / rel(row.get('ref'))
        if not p.is_file():
            raise Blocked(f'INPUT_MISSING:{i}:{row.get("ref")}')
        actual = sha(p)
        if actual != row.get('sha256'):
            raise Blocked(f'INPUT_HASH_MISMATCH:{i}:{row.get("ref")}')
        rows.append((p, row))
    return rows

def ticket_for(state, gate, state_hash: str, bundle_hash: str):
    body = {
        'contract': 'PFERDE_ATELIER_EXECUTION_TICKET_V2',
        'startmaster': state['startmaster'],
        'step_id': state['next_allowed_step'],
        'sequence': int(gate['sequence']),
        'state_sha256': state_hash,
        'bundle_sha256': bundle_hash,
    }
    body['ticket_id'] = stable_hash(body)
    return body

def terminal_for_current(state, ticket):
    term = state.get('execution_gate_terminal')
    if not isinstance(term, dict):
        return None
    checks = (
        term.get('step_id') == ticket['step_id'],
        int(term.get('sequence', -1)) == int(ticket['sequence']),
        isinstance(term.get('ticket_id'), str) and len(term.get('ticket_id')) == 64,
        term.get('bundle_sha256') == ticket['bundle_sha256'],
        term.get('status') in {'PASS', 'BLOCKED', 'USER_ACTION_REQUIRED'},
        isinstance(term.get('evidence'), list) and bool(term.get('evidence')),
    )
    if not all(checks):
        raise Blocked('TERMINAL_RECEIPT_BINDING_INVALID')
    return term

def receipt_record(ticket, receipt_hash: str, status: str):
    return {
        'completed_step_id': ticket['step_id'],
        'sequence': ticket['sequence'],
        'ticket_id': ticket['ticket_id'],
        'receipt_sha256': receipt_hash,
        'status': status,
    }

def persist_terminal(state, root, statep: Path, rootp: Path, ticket, receipt, receipt_hash: str):
    hist = state.setdefault('execution_gate_receipts', [])
    hist.append(receipt_record(ticket, receipt_hash, receipt['status']))
    state['execution_gate_terminal'] = {
        'step_id': ticket['step_id'],
        'sequence': ticket['sequence'],
        'ticket_id': ticket['ticket_id'],
        'bundle_sha256': ticket['bundle_sha256'],
        'status': receipt['status'],
        'receipt_sha256': receipt_hash,
        'evidence': list(receipt['evidence']),
    }
    dump_atomic(statep, state)
    root['current_state_sha256'] = sha(statep)
    root['next_allowed_step'] = state['next_allowed_step']
    dump_atomic(rootp, root)

def receipt_schema(ticket):
    return {
        '$schema': 'https://json-schema.org/draft/2020-12/schema',
        'type': 'object',
        'additionalProperties': False,
        'properties': {
            'contract': {'type': 'string', 'const': 'PFERDE_ATELIER_STEP_RECEIPT_V2'},
            'ticket_id': {'type': 'string', 'const': ticket['ticket_id']},
            'step_id': {'type': 'string', 'const': ticket['step_id']},
            'sequence': {'type': 'integer', 'const': ticket['sequence']},
            'state_sha256': {'type': 'string', 'const': ticket['state_sha256']},
            'bundle_sha256': {'type': 'string', 'const': ticket['bundle_sha256']},
            'status': {'type': 'string', 'enum': ['PASS', 'BLOCKED', 'USER_ACTION_REQUIRED']},
            'navigation_decision': {'type': 'boolean', 'const': False},
            'state_write_requested': {'type': 'boolean', 'const': False},
            'workflow_change_requested': {'type': 'boolean', 'const': False},
            'payload': {'type': 'object'},
            'evidence': {'type': 'array', 'items': {'type': 'string'}, 'minItems': 1},
        },
        'required': ['contract', 'ticket_id', 'step_id', 'sequence', 'state_sha256', 'bundle_sha256', 'status', 'navigation_decision', 'state_write_requested', 'workflow_change_requested', 'payload', 'evidence'],
    }

def materialize():
    ptr, root, state, gate, bundle, bp, rootp, statep, state_hash, bundle_hash = authority()
    inputs = verify_inputs(bundle)
    ticket = ticket_for(state, gate, state_hash, bundle_hash)
    terminal = terminal_for_current(state, ticket)
    if terminal is not None:
        if CAPSULE.exists():
            shutil.rmtree(CAPSULE)
        return {
            'ok': True,
            'status': 'FINAL_STEP_ALREADY_PASS' if terminal['status'] == 'PASS' and not isinstance(bundle.get('next_binding'), dict) else 'STEP_ALREADY_TERMINAL_NONPASS',
            'step_id': state['next_allowed_step'],
            'sequence': gate['sequence'],
            'ticket_id': ticket['ticket_id'],
            'step_status': terminal['status'],
            'state_advanced': False,
            'evidence': terminal['evidence'],
            'next_action': 'STOP_AT_BOUND_TERMINAL_STATE',
        }
    if CAPSULE.exists():
        shutil.rmtree(CAPSULE)
    (CAPSULE / 'inputs').mkdir(parents=True)
    copied = []
    for n, (src, row) in enumerate(inputs, 1):
        dst = CAPSULE / 'inputs' / f'{n:03d}_{src.name}'
        shutil.copyfile(src, dst)
        dst.chmod(0o444)
        copied.append({'source_ref': row['ref'], 'sha256': row['sha256'], 'capsule_path': str(dst.relative_to(CAPSULE))})
    instruction = str(bundle.get('instruction') or '').strip()
    if not instruction:
        raise Blocked('INSTRUCTION_MISSING')
    (CAPSULE / 'INSTRUCTION.txt').write_text(instruction + '\n', encoding='utf-8')
    (CAPSULE / 'TICKET.json').write_text(json.dumps(ticket, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    (CAPSULE / 'RECEIPT_SCHEMA.json').write_text(json.dumps(receipt_schema(ticket), ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    manifest = {
        'contract': 'PFERDE_ATELIER_CODEX_CLOUD_CAPSULE_V2',
        'startmaster': state['startmaster'],
        'step_id': state['next_allowed_step'],
        'sequence': gate['sequence'],
        'state_sha256': state_hash,
        'bundle_sha256': bundle_hash,
        'ticket_id': ticket['ticket_id'],
        'inputs': copied,
        'navigation_authority_exposed_to_worker': False,
        'worker_may_choose_next_step': False,
        'worker_state_write_authority': False,
        'workflow_change_authority': False,
        'repo_worktree_available_for_bound_step': gate.get('worker_context_policy') == 'CAPSULE_NAVIGATION_REPO_BOUND_STEP',
        'api_required': False,
        'completion_command': f'python3 control/cloud-entry-gate/cloud_entry.py complete .pferde-capsule/{RECEIPT_NAME}',
    }
    (CAPSULE / 'CAPSULE_MANIFEST.json').write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    return {
        'ok': True,
        'status': 'CODEX_CLOUD_ENTRANCE_PASS',
        'step_id': state['next_allowed_step'],
        'sequence': gate['sequence'],
        'ticket_id': ticket['ticket_id'],
        'capsule': '.pferde-capsule',
        'authorized_input_count': len(copied),
        'repo_worktree_available_for_bound_step': manifest['repo_worktree_available_for_bound_step'],
        'next_action': 'EXECUTE_ONLY_CURRENT_BOUND_STEP_THEN_WRITE_RECEIPT_AND_COMPLETE',
    }

def validate_receipt(receipt_path: Path):
    ptr, root, state, gate, bundle, bp, rootp, statep, state_hash, bundle_hash = authority()
    ticket = ticket_for(state, gate, state_hash, bundle_hash)
    if not receipt_path.is_file():
        raise Blocked('RECEIPT_MISSING')
    receipt = load(receipt_path)
    allowed = {'contract', 'ticket_id', 'step_id', 'sequence', 'state_sha256', 'bundle_sha256', 'status', 'navigation_decision', 'state_write_requested', 'workflow_change_requested', 'payload', 'evidence'}
    if set(receipt) != allowed:
        raise Blocked('RECEIPT_FIELDS_INVALID')
    if receipt.get('contract') != 'PFERDE_ATELIER_STEP_RECEIPT_V2':
        raise Blocked('RECEIPT_CONTRACT_INVALID')
    for key in ('ticket_id', 'step_id', 'sequence', 'state_sha256', 'bundle_sha256'):
        if receipt.get(key) != ticket.get(key):
            raise Blocked('RECEIPT_BINDING_MISMATCH:' + key)
    if receipt.get('status') not in {'PASS', 'BLOCKED', 'USER_ACTION_REQUIRED'}:
        raise Blocked('RECEIPT_STATUS_INVALID')
    if receipt.get('navigation_decision') is not False:
        raise Blocked('WORKER_NAVIGATION_DECISION_REJECTED')
    if receipt.get('state_write_requested') is not False:
        raise Blocked('WORKER_STATE_WRITE_REJECTED')
    if receipt.get('workflow_change_requested') is not False:
        raise Blocked('WORKER_WORKFLOW_CHANGE_REJECTED')
    if not isinstance(receipt.get('payload'), dict):
        raise Blocked('RECEIPT_PAYLOAD_INVALID')
    if not isinstance(receipt.get('evidence'), list) or not receipt.get('evidence') or not all(isinstance(x, str) and x.strip() for x in receipt['evidence']):
        raise Blocked('RECEIPT_EVIDENCE_INVALID')
    return ticket, receipt, hashlib.sha256(receipt_path.read_bytes()).hexdigest()

def complete(receipt_path: Path):
    ticket, receipt, receipt_hash = validate_receipt(receipt_path)
    ptr, root, state, gate, bundle, bp, rootp, statep, state_hash, bundle_hash = authority()
    if receipt['status'] != 'PASS':
        persist_terminal(state, root, statep, rootp, ticket, receipt, receipt_hash)
        if CAPSULE.exists():
            shutil.rmtree(CAPSULE)
        return {
            'ok': True,
            'status': 'STEP_TERMINAL_NONPASS',
            'step_id': ticket['step_id'],
            'sequence': ticket['sequence'],
            'step_status': receipt['status'],
            'state_advanced': False,
            'evidence': receipt['evidence'],
        }
    nb = bundle.get('next_binding')
    if not isinstance(nb, dict):
        persist_terminal(state, root, statep, rootp, ticket, receipt, receipt_hash)
        if CAPSULE.exists():
            shutil.rmtree(CAPSULE)
        return {
            'ok': True,
            'status': 'FINAL_STEP_PASS',
            'step_id': ticket['step_id'],
            'sequence': ticket['sequence'],
            'state_advanced': False,
            'evidence': receipt['evidence'],
        }
    next_step = str(nb.get('step_id') or '').strip()
    next_seq = int(nb.get('sequence', -1))
    next_rel = rel(nb.get('bundle_ref'))
    nextp = REPO / next_rel
    if not nextp.is_file():
        raise Blocked('NEXT_BUNDLE_MISSING')
    next_hash = sha(nextp)
    if next_hash != nb.get('bundle_sha256'):
        raise Blocked('NEXT_BUNDLE_HASH_MISMATCH')
    next_bundle = load(nextp)
    if next_bundle.get('step_id') != next_step or int(next_bundle.get('sequence', -2)) != next_seq:
        raise Blocked('NEXT_BINDING_IDENTITY_MISMATCH')
    if nb.get('startmaster', state['startmaster']) != state['startmaster']:
        raise Blocked('NEXT_STARTMASTER_UNSUPPORTED')
    if next_seq <= int(gate.get('sequence', -1)):
        raise Blocked('NON_MONOTONIC_SEQUENCE_REJECTED')
    state['next_allowed_step'] = next_step
    gate['step_id'] = next_step
    gate['sequence'] = next_seq
    gate['bundle_ref'] = next_rel.as_posix()
    gate['bundle_sha256'] = next_hash
    state.pop('execution_gate_terminal', None)
    hist = state.setdefault('execution_gate_receipts', [])
    hist.append(receipt_record(ticket, receipt_hash, 'PASS'))
    dump_atomic(statep, state)
    root['current_state_sha256'] = sha(statep)
    root['next_allowed_step'] = next_step
    dump_atomic(rootp, root)
    result = materialize()
    return {
        'ok': True,
        'status': 'STATE_ADVANCED_NEXT_STEP_READY',
        'completed_step_id': ticket['step_id'],
        'completed_sequence': ticket['sequence'],
        'next_step_id': result['step_id'],
        'next_sequence': result['sequence'],
        'next_ticket_id': result['ticket_id'],
        'state_advanced': True,
        'next_action': 'CONTINUE_IMMEDIATELY_WITH_NEW_CAPSULE_INSTRUCTION',
    }


def rebind(request_path: Path):
    ptr, root, state, gate, bundle, bp, rootp, statep, state_hash, bundle_hash = authority()
    ticket = ticket_for(state, gate, state_hash, bundle_hash)
    terminal = terminal_for_current(state, ticket)

    if terminal is None:
        raise Blocked('REBIND_REQUIRES_TERMINAL_STEP')
    if terminal.get('status') not in {'PASS', 'BLOCKED', 'USER_ACTION_REQUIRED'}:
        raise Blocked('REBIND_TERMINAL_STATUS_INVALID')

    request_path = request_path.resolve()
    allowed_dir = (REPO / 'control/cloud-entry-gate/rebind-requests').resolve()
    try:
        request_path.relative_to(allowed_dir)
    except ValueError:
        raise Blocked('REBIND_REQUEST_OUTSIDE_AUTHORIZED_DIR')

    if not request_path.is_file():
        raise Blocked('REBIND_REQUEST_MISSING')

    req = load(request_path)
    allowed = {
        'contract',
        'startmaster',
        'current_step_id',
        'current_sequence',
        'current_bundle_sha256',
        'current_terminal_status',
        'next_step_id',
        'next_sequence',
        'next_bundle_ref',
        'next_bundle_sha256',
        'reason',
    }
    if set(req) != allowed:
        raise Blocked('REBIND_REQUEST_FIELDS_INVALID')
    if req.get('contract') != 'PFERDE_ATELIER_EXTERNAL_REBIND_REQUEST_V1':
        raise Blocked('REBIND_REQUEST_CONTRACT_INVALID')
    if req.get('startmaster') != state.get('startmaster'):
        raise Blocked('REBIND_STARTMASTER_MISMATCH')
    if req.get('current_step_id') != ticket.get('step_id'):
        raise Blocked('REBIND_CURRENT_STEP_MISMATCH')
    if int(req.get('current_sequence', -1)) != int(ticket.get('sequence', -2)):
        raise Blocked('REBIND_CURRENT_SEQUENCE_MISMATCH')
    if req.get('current_bundle_sha256') != ticket.get('bundle_sha256'):
        raise Blocked('REBIND_CURRENT_BUNDLE_MISMATCH')
    if req.get('current_terminal_status') != terminal.get('status'):
        raise Blocked('REBIND_TERMINAL_STATUS_MISMATCH')
    if not isinstance(req.get('reason'), str) or not req.get('reason').strip():
        raise Blocked('REBIND_REASON_MISSING')

    next_step = str(req.get('next_step_id') or '').strip()
    if not next_step:
        raise Blocked('REBIND_NEXT_STEP_MISSING')
    try:
        next_seq = int(req.get('next_sequence'))
    except Exception:
        raise Blocked('REBIND_NEXT_SEQUENCE_INVALID')
    if next_seq <= int(gate.get('sequence', -1)):
        raise Blocked('REBIND_NON_MONOTONIC_SEQUENCE_REJECTED')

    next_rel = rel(req.get('next_bundle_ref'))
    nextp = REPO / next_rel
    if not nextp.is_file():
        raise Blocked('REBIND_NEXT_BUNDLE_MISSING')
    next_hash = sha(nextp)
    if next_hash != req.get('next_bundle_sha256'):
        raise Blocked('REBIND_NEXT_BUNDLE_HASH_MISMATCH')

    next_bundle = load(nextp)
    if next_bundle.get('step_id') != next_step:
        raise Blocked('REBIND_NEXT_STEP_IDENTITY_MISMATCH')
    if int(next_bundle.get('sequence', -1)) != next_seq:
        raise Blocked('REBIND_NEXT_SEQUENCE_IDENTITY_MISMATCH')

    hist = state.setdefault('execution_gate_receipts', [])
    hist.append({
        'completed_step_id': ticket['step_id'],
        'sequence': ticket['sequence'],
        'ticket_id': ticket['ticket_id'],
        'receipt_sha256': terminal.get('receipt_sha256'),
        'status': terminal.get('status'),
        'transition': 'EXTERNAL_REBIND',
        'rebind_request_sha256': sha(request_path),
        'rebind_reason': req['reason'].strip(),
    })

    state['next_allowed_step'] = next_step
    gate['step_id'] = next_step
    gate['sequence'] = next_seq
    gate['bundle_ref'] = next_rel.as_posix()
    gate['bundle_sha256'] = next_hash
    state.pop('execution_gate_terminal', None)

    dump_atomic(statep, state)
    root['current_state_sha256'] = sha(statep)
    root['next_allowed_step'] = next_step
    dump_atomic(rootp, root)

    result = materialize()
    return {
        'ok': True,
        'status': 'STATE_REBOUND_NEXT_STEP_READY',
        'previous_step_id': ticket['step_id'],
        'previous_sequence': ticket['sequence'],
        'previous_terminal_status': terminal['status'],
        'next_step_id': result['step_id'],
        'next_sequence': result['sequence'],
        'next_ticket_id': result['ticket_id'],
        'state_advanced': True,
        'rebind_request_sha256': sha(request_path),
        'next_action': 'CONTINUE_IMMEDIATELY_WITH_NEW_CAPSULE_INSTRUCTION',
    }


def verify():
    ptr, root, state, gate, bundle, bp, rootp, statep, state_hash, bundle_hash = authority()
    verify_inputs(bundle)
    ticket = ticket_for(state, gate, state_hash, bundle_hash)
    terminal = terminal_for_current(state, ticket)
    return {
        'ok': True,
        'status': 'CODEX_CLOUD_GATE_VERIFY_PASS',
        'startmaster': state['startmaster'],
        'step_id': state['next_allowed_step'],
        'sequence': gate['sequence'],
        'ticket_id': ticket['ticket_id'],
        'terminal_step_status': terminal['status'] if terminal else None,
        'api_required': False,
        'domain_logic_authority': 'NONE',
    }

def main():
    try:
        cmd = sys.argv[1] if len(sys.argv) > 1 else 'verify'
        if cmd == 'start':
            result = materialize()
        elif cmd == 'verify':
            result = verify()
        elif cmd == 'complete':
            if len(sys.argv) != 3:
                raise Blocked('COMPLETE_REQUIRES_RECEIPT_PATH')
            result = complete(Path(sys.argv[2]))
        elif cmd == 'rebind':
            if len(sys.argv) != 3:
                raise Blocked('REBIND_REQUIRES_REQUEST_PATH')
            result = rebind(Path(sys.argv[2]))
        else:
            raise Blocked('UNKNOWN_COMMAND')
        print(json.dumps(result, ensure_ascii=False, indent=2))
        return 0
    except Blocked as e:
        print(json.dumps({'ok': False, 'status': 'CODEX_CLOUD_ENTRANCE_BLOCKED', 'reason': str(e)}, ensure_ascii=False, indent=2))
        return 2

if __name__ == '__main__':
    raise SystemExit(main())
