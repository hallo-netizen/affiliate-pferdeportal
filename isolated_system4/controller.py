from __future__ import annotations

"""System 4 controller with machine-owned route completeness and repair routing.

The previous controller remains in controller_engine.py.  This public controller is the
only production routing seam.  It binds one canonical article route to the real
Point-0 workspace and owns every legal backward repair transition.  A repairable
worker finding therefore never needs a new article/workspace and never becomes a
terminal parent return merely because its producer is upstream of the draft.
"""

import hashlib
import json
from pathlib import Path
import controller_engine as _engine
import root_entry
import root_supervisor_bridge
import worker_dispatch

# Re-export the existing controller API first so existing callers/tests keep the same surface.
for _name in dir(_engine):
    if not _name.startswith('__') and _name not in {'cmd_fullcheck', 'main', 'load'}:
        globals()[_name] = getattr(_engine, _name)


DRAFT_WORKER = 'DRAFT_WORKER'
RESEARCH_WORKER = 'RESEARCH_WORKER'
FACTS_WORKER = 'FACTS_WORKER'
CONTEXT_WORKER = 'CONTEXT_WORKER'
PARENT_LAUNCH = 'PARENT_LAUNCH'
DRAFT_STAGE = 'DRAFT_STAGE'
RESEARCH_STAGE = 'RESEARCH_STAGE'
FACTS_STAGE = 'FACTS_STAGE'
CONTEXT_STAGE = 'CONTEXT_STAGE'
MULTI_OWNER_RETURN = 'MULTI_OWNER_RETURN'

# ONE machine-readable truth for the article production route.  The same structure
# drives route locking, completeness, and controlled repair rollback.
ROUTE_CONTRACT = 'SYSTEM4_CANONICAL_ARTICLE_ROUTE_V1'
ARTICLE_ROUTE = (
    ('RESEARCH', RESEARCH_WORKER, 'research', 'RESEARCH_REQUIRED'),
    ('FACTS', FACTS_WORKER, 'facts', 'FACT_CHECK_REQUIRED'),
    ('CONTEXT', CONTEXT_WORKER, 'context', 'CONTEXT_REQUIRED'),
    ('DRAFT', DRAFT_WORKER, 'draft', 'DRAFT_REQUIRED'),
)
FULLCHECK_STAGE = 'FULLCHECK'
CANONICAL_COMPLETION_TRACE = tuple(row[0] for row in ARTICLE_ROUTE) + (FULLCHECK_STAGE,)
OWNER_TO_ROUTE = {owner: (name, command, phase) for name, owner, command, phase in ARTICLE_ROUTE}
COMMAND_TO_ROUTE = {command: name for name, owner, command, phase in ARTICLE_ROUTE}
_MACHINE_ROUTE_FILES = (
    'point0.json',
    'root_receipt.json',
    'supervisor_state.json',
    'bound_snapshot.json',
)
_POST_INGRESS_COMMANDS = {
    *(row[2] for row in ARTICLE_ROUTE),
    'repair','check','fullcheck','release','prepare-release','finalize-signed','verify',
}


def _route_contract_digest() -> str:
    value = {
        'contract': ROUTE_CONTRACT,
        'article_route': ARTICLE_ROUTE,
        'completion_trace': CANONICAL_COMPLETION_TRACE,
        'machine_route_files': _MACHINE_ROUTE_FILES,
    }
    raw = json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(',', ':')).encode('utf-8')
    return hashlib.sha256(raw).hexdigest()


def _verify_route_state(state: dict) -> None:
    contract = state.get('route_contract')
    # Direct low-level unit states created outside the production root remain readable;
    # the real root always binds this contract at ingress and is strict from that point.
    if contract is None:
        return
    if contract != ROUTE_CONTRACT:
        raise Fail('ROUTE_CONTRACT_TAMPERED')
    if state.get('route_contract_sha256') != _route_contract_digest():
        raise Fail('ROUTE_CONTRACT_DIGEST_MISMATCH')
    progress = state.get('route_progress')
    if not isinstance(progress, list):
        raise Fail('ROUTE_PROGRESS_INVALID')
    if tuple(progress) != CANONICAL_COMPLETION_TRACE[:len(progress)]:
        raise Fail('ROUTE_PROGRESS_ORDER_INVALID')
    counts = state.get('repair_return_counts')
    if not isinstance(counts, dict):
        raise Fail('REPAIR_RETURN_COUNTS_INVALID')
    for owner, count in counts.items():
        if owner not in OWNER_TO_ROUTE or owner == DRAFT_WORKER:
            raise Fail('REPAIR_RETURN_OWNER_INVALID:' + str(owner))
        if not isinstance(count, int) or isinstance(count, bool) or count < 0:
            raise Fail('REPAIR_RETURN_COUNT_INVALID:' + str(owner))
    history = state.get('repair_history')
    if not isinstance(history, list):
        raise Fail('REPAIR_HISTORY_INVALID')


def load(workspace):
    state, path = _engine.load(workspace)
    _verify_route_state(state)
    return state, path


def _bind_route_contract(workspace: str) -> None:
    state, path = _engine.load(workspace)
    if state.get('route_contract') is not None:
        raise Fail('ROUTE_CONTRACT_ALREADY_BOUND')
    state['route_contract'] = ROUTE_CONTRACT
    state['route_contract_sha256'] = _route_contract_digest()
    state['route_progress'] = []
    state['repair_return_counts'] = {}
    state['repair_history'] = []
    _engine.save(state, path)
    _verify_route_state(state)


def _record_stage_success(workspace: str, command: str) -> None:
    state, path = load(workspace)
    if state.get('route_contract') is None:
        return
    stage = COMMAND_TO_ROUTE.get(command)
    if stage is None:
        raise Fail('ROUTE_STAGE_UNKNOWN:' + command)
    progress = list(state['route_progress'])
    expected_index = len(progress)
    if expected_index >= len(ARTICLE_ROUTE):
        raise Fail('ROUTE_STAGE_AFTER_ARTICLE_COMPLETE:' + stage)
    expected = ARTICLE_ROUTE[expected_index][0]
    if stage != expected:
        raise Fail('ROUTE_STAGE_ORDER_FAIL:EXPECTED_' + expected + ':GOT_' + stage)
    progress.append(stage)
    state['route_progress'] = progress
    _engine.save(state, path)
    _verify_route_state(state)


def _machine_route_lock(command: str, workspace: str) -> None:
    """Fail closed unless the existing Root -> Supervisor route owns this workspace."""
    command = str(command or '').strip()
    w = Path(workspace)
    if not w.is_dir():
        raise Fail('MACHINE_ROUTE_BLOCK:WORKSPACE_MISSING')
    for name in _MACHINE_ROUTE_FILES:
        if not (w / name).is_file():
            raise Fail('MACHINE_ROUTE_BLOCK:' + name.upper().replace('.', '_') + '_MISSING')

    if command == 'ingress':
        if (w / 'state.json').exists():
            raise Fail('MACHINE_ROUTE_BLOCK:INGRESS_STATE_ALREADY_EXISTS')
        try:
            root_supervisor_bridge.dispatch(w)
        except Exception as exc:
            raise Fail('MACHINE_ROUTE_BLOCK:ROOT_SUPERVISOR_BINDING_INVALID:' + str(exc)) from exc
        return

    if command not in _POST_INGRESS_COMMANDS:
        raise Fail('MACHINE_ROUTE_BLOCK:COMMAND_NOT_ALLOWED:' + command)
    if not (w / 'state.json').is_file():
        raise Fail('MACHINE_ROUTE_BLOCK:STATE_MISSING')
    bundle_path = w / 'worker_dispatch.json'
    if not bundle_path.is_file():
        raise Fail('MACHINE_ROUTE_BLOCK:WORKER_DISPATCH_MISSING')
    try:
        bundle = json.loads(bundle_path.read_text(encoding='utf-8'))
        actual_manifest = root_entry._critical_manifest_sha256()
        actual_head = root_entry._git('rev-parse', '--verify', 'HEAD')
        worker_dispatch.verify_bundle(bundle, actual_manifest=actual_manifest, actual_head=actual_head)
        supervisor.verify_controller_binding(w)
        _verify_route_state(json.loads((w / 'state.json').read_text(encoding='utf-8')))
    except Exception as exc:
        if isinstance(exc, Fail):
            raise
        raise Fail('MACHINE_ROUTE_BLOCK:WORKER_DISPATCH_INVALID:' + str(exc)) from exc


def _repair_owners(e) -> tuple[str, ...]:
    """Return every safely classified repair owner; unknown findings fail closed."""
    findings = e.findings if isinstance(getattr(e, 'findings', None), list) else []
    owners = {str(row.get('repair_owner') or '').strip() for row in findings if isinstance(row, dict) and str(row.get('repair_owner') or '').strip()}
    checker = str(getattr(e, 'checker', '') or '')
    if not owners and checker in {'languagetool', 'no_external_links'}:
        owners = {DRAFT_WORKER}
    if not owners:
        raise Fail('REPAIR_OWNER_MISSING:' + checker)
    return tuple(sorted(owners))


def _repair_owner(e):
    owners = _repair_owners(e)
    return owners[0] if len(owners) == 1 else MULTI_OWNER_RETURN


def _stage_owner_route(command: str, message: str):
    """Return only safely repairable producer-stage errors."""
    command = str(command or '').strip().casefold()
    message = str(message or '').strip()

    if command == 'research':
        if message.startswith('RESEARCH_EVIDENCE_FAIL:'):
            return RESEARCH_WORKER, RESEARCH_STAGE
        return None

    if command == 'facts':
        if message.startswith('FACTS_EVIDENCE_FAIL:'):
            return FACTS_WORKER, FACTS_STAGE
        return None

    if command == 'context':
        prefix = 'PRODUCTION_CONTEXT_FAIL:'
        if not message.startswith(prefix):
            return None
        inner = message[len(prefix):]
        if inner.startswith(('FACT_PACK_', 'FACT_ID_', 'FACT_SOURCE_', 'FACT_STATEMENT_', 'FACT_EVIDENCE_')):
            return CONTEXT_WORKER, CONTEXT_STAGE
        return None

    if command == 'draft':
        prefix = 'ARTICLE_AUTHORING_CONTRACT_FAIL:'
        if not message.startswith(prefix):
            return None
        inner = message[len(prefix):]
        if inner.startswith((
            'PREWRITE_BOUND_LINK_MISSING:',
            'PREWRITE_EXTERNAL_LINK_FORBIDDEN',
            'PREWRITE_LINK_COUNT:',
        )):
            return DRAFT_WORKER, DRAFT_STAGE
        return None

    return None


def _stage_owner_call(command: str, fn, workspace: str, *args: str) -> int:
    state_path = Path(workspace) / 'state.json'
    before = state_path.read_bytes() if state_path.is_file() else None
    try:
        fn(workspace, *args)
        _record_stage_success(workspace, command)
        return 0
    except _engine.Fail as exc:
        message = str(exc)
        routed = _stage_owner_route(command, message)
        if routed is None:
            raise
        after = state_path.read_bytes() if state_path.is_file() else None
        if before is None or after != before:
            raise Fail('STAGE_OWNER_RETURN_STATE_MUTATED:' + command) from exc
        owner, route = routed
        print('SYSTEM4_STAGE_OWNER_RETURN:' + owner + ':' + route + ':' + message)
        return 4


def _rollback_upstream_worker(state: dict, path: Path, owners: tuple[str, ...], error: str) -> str | None:
    """Return the SAME article to the earliest responsible worker stage.

    Parent/machine binding owners are deliberately not mutated here: changing sealed
    metadata/links/Point-0 in an article repair would violate authority separation.
    """
    worker_owners = [owner for owner in owners if owner in OWNER_TO_ROUTE]
    parent_owners = [owner for owner in owners if owner not in OWNER_TO_ROUTE]
    if parent_owners:
        return None
    if not worker_owners:
        return None

    order = {owner: index for index, (_, owner, _, _) in enumerate(ARTICLE_ROUTE)}
    target = min(worker_owners, key=lambda owner: order[owner])
    if target == DRAFT_WORKER and set(worker_owners) == {DRAFT_WORKER}:
        return None

    target_index = order[target]
    target_stage, _, _, target_phase = ARTICLE_ROUTE[target_index]
    counts = dict(state.get('repair_return_counts') or {})
    attempt = int(counts.get(target, 0)) + 1
    immutable_before = state.get('immutable_core_sha256')
    article_before = json.loads(json.dumps(state.get('article'), ensure_ascii=False))
    counts[target] = attempt
    history = list(state.get('repair_history') or [])
    history.append({
        'error': error,
        'owners': list(owners),
        'return_owner': target,
        'return_stage': target_stage,
        'attempt': attempt,
        'same_article': True,
    })

    # Invalidate the target producer and every downstream artifact.  No stale evidence
    # may survive a repair return.
    if target_index <= 0:
        state['research'] = None
    if target_index <= 1:
        state['facts'] = None
    if target_index <= 2:
        state['production_context'] = None
        state['authoring_contract'] = None
    state['draft_markdown'] = None
    state['draft_sha256'] = None
    state['checks'] = {}
    state['last_error'] = None
    state['release_prepared'] = None
    state['released'] = False
    state.pop('release_final', None)
    state['repair_return_counts'] = counts
    state['repair_history'] = history
    state['route_progress'] = list(CANONICAL_COMPLETION_TRACE[:target_index])
    state['phase'] = target_phase

    if state.get('immutable_core_sha256') != immutable_before or state.get('article') != article_before:
        raise Fail('REPAIR_RETURN_SAME_ARTICLE_VIOLATION')
    _engine.save(state, path)
    _verify_route_state(state)
    print('SYSTEM4_CONTROLLED_REPAIR_RETURN:' + target + ':' + target_stage + ':ATTEMPT=' + str(attempt))
    return target


def _assert_fullcheck_route_complete(state: dict) -> None:
    if state.get('route_contract') is None:
        return
    _verify_route_state(state)
    expected = tuple(row[0] for row in ARTICLE_ROUTE)
    if tuple(state.get('route_progress') or ()) != expected:
        raise Fail('ROUTE_COMPLETENESS_FAIL:EXPECTED_' + ','.join(expected) + ':GOT_' + ','.join(state.get('route_progress') or []))


def _guard_repair_or_hard_block(state: dict, path: Path, checker: str, error_value: str) -> int:
    finding = production_checks.guard_repair_finding(checker, error_value)
    if finding is None:
        raise Fail('FULL_CHECK_HARD_BLOCK:' + checker.upper() + ':' + error_value)
    owner = str(finding.get('repair_owner') or '').strip()
    if owner != DRAFT_WORKER:
        raise Fail('GUARD_REPAIR_OWNER_INVALID:' + checker + ':' + owner)
    error = 'FULL:' + checker + ':' + str(finding.get('error_code') or error_value)
    state['checks'] = {
        'status': 'FAIL', 'mode': 'FULL_PRODUCTION', 'errors': [error],
        'findings': [finding], 'checker': checker,
        'checked_draft_sha256': state['draft_sha256'],
        'repair_owner': DRAFT_WORKER, 'repair_owners': [DRAFT_WORKER],
    }
    state['last_error'] = error
    state['phase'] = 'REPAIR_REQUIRED'
    _engine.save(state, path)
    print('SYSTEM4_FULL_CHECK_FAIL:' + error + ':REPAIR_OWNER=DRAFT_WORKER:REPAIR_REQUIRED')
    return 3


def cmd_fullcheck(workspace):
    s, p = load(workspace)
    if s['phase'] != 'CHECK_REQUIRED':
        raise Fail('PHASE_FAIL:FULLCHECK')
    _assert_fullcheck_route_complete(s)
    context = s.get('production_context')
    if not isinstance(context, dict):
        raise Fail('PRODUCTION_CONTEXT_MISSING')
    try:
        authoring_contract.validate_bound(Path(__file__).resolve().parent.parent, s)
    except authoring_contract.AuthoringContractError as e:
        raise Fail('AUTHORING_CONTRACT_FAIL:' + str(e)) from e
    text = str(s.get('draft_markdown') or '')
    try:
        content_guard.validate_single_article(text, context['fact_pack'])
        design_guard.validate_design_neutrality(text, s['article']['article_type'])
    except content_guard.ContentGuardError as e:
        return _guard_repair_or_hard_block(s, p, 'content_guard', str(e))
    except design_guard.DesignGuardError as e:
        return _guard_repair_or_hard_block(s, p, 'design_guard', str(e))
    repo = Path(__file__).resolve().parent.parent
    try:
        result = production_checks.run_all(repo, s, context['fact_pack'], context['production_plan_item'])
    except production_checks.RepairRequired as e:
        findings = e.findings
        code = str(findings[0].get('error_code') or e.checker) if findings else e.checker
        owners = _repair_owners(e)
        error = 'FULL:' + e.checker + ':' + code
        owner_value = owners[0] if len(owners) == 1 else MULTI_OWNER_RETURN
        s['checks'] = {
            'status': 'FAIL', 'mode': 'FULL_PRODUCTION', 'errors': [error],
            'findings': findings, 'checker': e.checker,
            'checked_draft_sha256': s['draft_sha256'],
            'repair_owner': owner_value, 'repair_owners': list(owners),
        }
        s['last_error'] = error
        if owners == (DRAFT_WORKER,):
            s['phase'] = 'REPAIR_REQUIRED'
            _engine.save(s, p)
            print('SYSTEM4_FULL_CHECK_FAIL:' + error + ':REPAIR_OWNER=DRAFT_WORKER:REPAIR_REQUIRED')
            return 3

        # Root-cause fix: worker-owned upstream defects are repaired inside the same
        # article/workspace.  Only parent/machine authority defects leave this route.
        repaired_owner = _rollback_upstream_worker(s, p, owners, error)
        if repaired_owner is not None:
            return 0

        s['checks']['return_required'] = True
        s['checks']['return_route'] = PARENT_LAUNCH
        s['phase'] = 'CHECK_REQUIRED'
        _engine.save(s, p)
        print('SYSTEM4_REPAIR_OWNER_RETURN:' + ','.join(owners) + ':' + PARENT_LAUNCH + ':' + error)
        return 4
    except production_checks.ProductionCheckError as e:
        raise Fail('FULL_CHECK_HARD_BLOCK:' + str(e)) from e

    s['checks'] = {
        'status': 'PASS', 'mode': 'FULL_PRODUCTION', 'errors': [],
        'checked_draft_sha256': s['draft_sha256'], 'production_evidence': result,
    }
    s['last_error'] = None
    s['phase'] = 'OUTPUT_GATE_REQUIRED'
    if s.get('route_contract') is not None:
        s['route_progress'] = list(CANONICAL_COMPLETION_TRACE)
    _engine.save(s, p)
    _verify_route_state(s)
    print('SYSTEM4_FULL_CHECK_PASS:OUTPUT_GATE_REQUIRED')
    return 0


_engine.cmd_fullcheck = cmd_fullcheck


def main(argv):
    try:
        if len(argv) < 2:
            raise Fail('BAD_COMMAND')
        cmd = argv[1]
        if cmd == 'ingress':
            if len(argv) not in (4, 5):
                raise Fail('BAD_COMMAND')
            _machine_route_lock(cmd, argv[3])
            rc = _engine.main(argv)
            if rc == 0:
                _bind_route_contract(argv[3])
            return rc
        if cmd in _POST_INGRESS_COMMANDS:
            if len(argv) < 3:
                raise Fail('BAD_COMMAND')
            _machine_route_lock(cmd, argv[2])

        if cmd == 'research':
            if len(argv) != 4: raise Fail('BAD_COMMAND')
            return _stage_owner_call('research', _engine.cmd_research, argv[2], argv[3])
        if cmd == 'facts':
            if len(argv) != 4: raise Fail('BAD_COMMAND')
            return _stage_owner_call('facts', _engine.cmd_facts, argv[2], argv[3])
        if cmd == 'context':
            if len(argv) != 5: raise Fail('BAD_COMMAND')
            return _stage_owner_call('context', _engine.cmd_context, argv[2], argv[3], argv[4])
        if cmd == 'draft':
            if len(argv) != 4: raise Fail('BAD_COMMAND')
            return _stage_owner_call('draft', _engine.cmd_draft, argv[2], argv[3])
        return _engine.main(argv)
    except (Fail, KeyError, IndexError, ValueError, json.JSONDecodeError) as exc:
        print('SYSTEM4_FAIL:' + str(exc))
        return 2


if __name__ == '__main__':
    raise SystemExit(main(_engine.sys.argv))
