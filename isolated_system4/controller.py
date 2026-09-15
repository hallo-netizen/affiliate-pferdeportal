from __future__ import annotations

"""System 4 controller with owner-aware repair and stage-return routing.

The previous controller is retained byte-identically in controller_engine.py. This
public module owns only routing seams: fullcheck repair owners and repairable producer
stage returns. Unknown, binding, integrity and tamper failures remain fail-closed.
"""

import json
from pathlib import Path
import controller_engine as _engine
import root_entry
import root_supervisor_bridge
import worker_dispatch

# Re-export the existing controller API first so existing callers/tests keep the same surface.
for _name in dir(_engine):
    if not _name.startswith('__') and _name not in {'cmd_fullcheck', 'main'}:
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

_MACHINE_ROUTE_FILES = (
    'point0.json',
    'root_receipt.json',
    'supervisor_state.json',
    'bound_snapshot.json',
)
_POST_INGRESS_COMMANDS = {
    'research','facts','context','draft','repair','check','fullcheck',
    'release','prepare-release','finalize-signed','verify',
}


def _machine_route_lock(command: str, workspace: str) -> None:
    """Fail closed unless the existing Root -> Supervisor route owns this workspace.

    This is deliberately not another workflow. It only prevents callers from bypassing
    the already existing workflow by invoking controller stages directly.
    """
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
    except Exception as exc:
        raise Fail('MACHINE_ROUTE_BLOCK:WORKER_DISPATCH_INVALID:' + str(exc)) from exc


def _repair_owners(e) -> tuple[str, ...]:
    """Return every safely classified repair owner.

    Historical failure mode: two simultaneously repairable findings with different
    owners were converted into ``REPAIR_OWNER_CONFLICT`` and the route stopped. That is
    forbidden. Multiple repairable owners are an upstream-return condition, not an
    integrity failure. Unknown/unclassified findings still fail closed.
    """
    findings = e.findings if isinstance(getattr(e, 'findings', None), list) else []
    owners = {str(row.get('repair_owner') or '').strip() for row in findings if isinstance(row, dict) and str(row.get('repair_owner') or '').strip()}
    checker = str(getattr(e, 'checker', '') or '')
    if not owners and checker in {'languagetool', 'no_external_links'}:
        owners = {DRAFT_WORKER}
    if not owners:
        raise Fail('REPAIR_OWNER_MISSING:'+checker)
    return tuple(sorted(owners))


def _repair_owner(e):
    owners = _repair_owners(e)
    return owners[0] if len(owners) == 1 else MULTI_OWNER_RETURN


def _stage_owner_route(command: str, message: str):
    """Return only safely reparable producer-stage errors.

    Binding/integrity/tamper failures intentionally return None and remain hard blocks.
    Draft routing is limited to defects created in the candidate article itself after
    valid machine bindings already exist. It must never repair the bindings.
    """
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
        # These are candidate-realization defects. The bound link registry/plan remains
        # untouched; only the draft worker may rewrite the current article candidate.
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


def cmd_fullcheck(workspace):
    s,p=load(workspace)
    if s['phase']!='CHECK_REQUIRED': raise Fail('PHASE_FAIL:FULLCHECK')
    context=s.get('production_context')
    if not isinstance(context,dict): raise Fail('PRODUCTION_CONTEXT_MISSING')
    try: authoring_contract.validate_bound(Path(__file__).resolve().parent.parent,s)
    except authoring_contract.AuthoringContractError as e: raise Fail('AUTHORING_CONTRACT_FAIL:'+str(e)) from e
    text=str(s.get('draft_markdown') or '')
    try:
        content_guard.validate_single_article(text,context['fact_pack'])
        design_guard.validate_design_neutrality(text,s['article']['article_type'])
    except content_guard.ContentGuardError as e: raise Fail('FULL_CHECK_HARD_BLOCK:CONTENT_GUARD:'+str(e)) from e
    except design_guard.DesignGuardError as e: raise Fail('FULL_CHECK_HARD_BLOCK:DESIGN_GUARD:'+str(e)) from e
    repo=Path(__file__).resolve().parent.parent
    try:
        result=production_checks.run_all(repo,s,context['fact_pack'],context['production_plan_item'])
    except production_checks.RepairRequired as e:
        findings=e.findings
        code=str(findings[0].get('error_code') or e.checker) if findings else e.checker
        owners=_repair_owners(e)
        error='FULL:'+e.checker+':'+code
        owner_value=owners[0] if len(owners)==1 else MULTI_OWNER_RETURN
        s['checks']={'status':'FAIL','mode':'FULL_PRODUCTION','errors':[error],'findings':findings,'checker':e.checker,'checked_draft_sha256':s['draft_sha256'],'repair_owner':owner_value,'repair_owners':list(owners)}
        s['last_error']=error
        if owners==(DRAFT_WORKER,):
            s['phase']='REPAIR_REQUIRED'; save(s,p)
            print('SYSTEM4_FULL_CHECK_FAIL:'+error+':REPAIR_OWNER=DRAFT_WORKER:REPAIR_REQUIRED'); return 3
        # Any repairable upstream/mixed-owner set MUST be returned. It must never become
        # a terminal conflict. The upstream launch receives every owner/finding and may
        # only use the real producing authority for repair/rebuild.
        s['checks']['return_required']=True
        s['checks']['return_route']=PARENT_LAUNCH
        s['phase']='CHECK_REQUIRED'; save(s,p)
        print('SYSTEM4_REPAIR_OWNER_RETURN:'+','.join(owners)+':'+PARENT_LAUNCH+':'+error); return 4
    except production_checks.ProductionCheckError as e:
        raise Fail('FULL_CHECK_HARD_BLOCK:'+str(e)) from e
    s['checks']={'status':'PASS','mode':'FULL_PRODUCTION','errors':[],'checked_draft_sha256':s['draft_sha256'],'production_evidence':result}
    s['last_error']=None; s['phase']='OUTPUT_GATE_REQUIRED'; save(s,p)
    print('SYSTEM4_FULL_CHECK_PASS:OUTPUT_GATE_REQUIRED'); return 0


_engine.cmd_fullcheck = cmd_fullcheck


def main(argv):
    try:
        if len(argv) < 2:
            raise Fail('BAD_COMMAND')
        cmd = argv[1]
        if cmd == 'ingress':
            if len(argv) not in (4,5): raise Fail('BAD_COMMAND')
            _machine_route_lock(cmd, argv[3])
        elif cmd in _POST_INGRESS_COMMANDS:
            if len(argv) < 3: raise Fail('BAD_COMMAND')
            _machine_route_lock(cmd, argv[2])

        if len(argv) >= 2:
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


if __name__=='__main__':
    raise SystemExit(main(_engine.sys.argv))
