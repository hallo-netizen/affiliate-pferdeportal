from __future__ import annotations

"""System 4 controller with owner-aware repair and stage-return routing.

The previous controller is retained byte-identically in controller_engine.py. This
public module owns only routing seams: fullcheck repair owners and repairable producer
stage returns. Unknown, binding, integrity and tamper failures remain fail-closed.
"""

import json
from pathlib import Path
import controller_engine as _engine

# Re-export the existing controller API first so existing callers/tests keep the same surface.
for _name in dir(_engine):
    if not _name.startswith('__') and _name not in {'cmd_fullcheck', 'main'}:
        globals()[_name] = getattr(_engine, _name)


DRAFT_WORKER = 'DRAFT_WORKER'
RESEARCH_WORKER = 'RESEARCH_WORKER'
FACTS_WORKER = 'FACTS_WORKER'
CONTEXT_WORKER = 'CONTEXT_WORKER'
PARENT_LAUNCH = 'PARENT_LAUNCH'
RESEARCH_STAGE = 'RESEARCH_STAGE'
FACTS_STAGE = 'FACTS_STAGE'
CONTEXT_STAGE = 'CONTEXT_STAGE'


def _repair_owner(e):
    findings = e.findings if isinstance(getattr(e, 'findings', None), list) else []
    owners = {str(row.get('repair_owner') or '').strip() for row in findings if isinstance(row, dict) and str(row.get('repair_owner') or '').strip()}
    checker = str(getattr(e, 'checker', '') or '')
    if not owners and checker in {'languagetool', 'no_external_links'}:
        return DRAFT_WORKER
    if not owners:
        raise Fail('REPAIR_OWNER_MISSING:'+checker)
    if len(owners) != 1:
        raise Fail('REPAIR_OWNER_CONFLICT:'+','.join(sorted(owners)))
    return next(iter(owners))


def _stage_owner_route(command: str, message: str):
    """Return only safely reparable same-stage producer errors.

    Binding/integrity/tamper failures intentionally return None and remain hard blocks.
    Context routing is deliberately restricted to fact-pack production defects; machine
    prewrite/PPM/binding errors are not context-worker repairs.
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
        # These originate from content_guard.validate_fact_pack. They are defects in the
        # context/fact-pack artifact itself, not in machine-bound plan rails or runtime state.
        if inner.startswith(('FACT_PACK_', 'FACT_ID_', 'FACT_SOURCE_', 'FACT_STATEMENT_', 'FACT_EVIDENCE_')):
            return CONTEXT_WORKER, CONTEXT_STAGE
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
        owner=_repair_owner(e)
        error='FULL:'+e.checker+':'+code
        s['checks']={'status':'FAIL','mode':'FULL_PRODUCTION','errors':[error],'findings':findings,'checker':e.checker,'checked_draft_sha256':s['draft_sha256'],'repair_owner':owner}
        s['last_error']=error
        if owner==DRAFT_WORKER:
            s['phase']='REPAIR_REQUIRED'; save(s,p)
            print('SYSTEM4_FULL_CHECK_FAIL:'+error+':REPAIR_OWNER=DRAFT_WORKER:REPAIR_REQUIRED'); return 3
        s['checks']['return_required']=True
        s['checks']['return_route']=PARENT_LAUNCH
        s['phase']='CHECK_REQUIRED'; save(s,p)
        print('SYSTEM4_REPAIR_OWNER_RETURN:'+owner+':'+PARENT_LAUNCH+':'+error); return 4
    except production_checks.ProductionCheckError as e:
        raise Fail('FULL_CHECK_HARD_BLOCK:'+str(e)) from e
    s['checks']={'status':'PASS','mode':'FULL_PRODUCTION','errors':[],'checked_draft_sha256':s['draft_sha256'],'production_evidence':result}
    s['last_error']=None; s['phase']='OUTPUT_GATE_REQUIRED'; save(s,p)
    print('SYSTEM4_FULL_CHECK_PASS:OUTPUT_GATE_REQUIRED'); return 0


_engine.cmd_fullcheck = cmd_fullcheck


def main(argv):
    try:
        if len(argv) >= 2:
            cmd = argv[1]
            if cmd == 'research':
                if len(argv) != 4: raise Fail('BAD_COMMAND')
                return _stage_owner_call('research', _engine.cmd_research, argv[2], argv[3])
            if cmd == 'facts':
                if len(argv) != 4: raise Fail('BAD_COMMAND')
                return _stage_owner_call('facts', _engine.cmd_facts, argv[2], argv[3])
            if cmd == 'context':
                if len(argv) != 5: raise Fail('BAD_COMMAND')
                return _stage_owner_call('context', _engine.cmd_context, argv[2], argv[3], argv[4])
        return _engine.main(argv)
    except (Fail, KeyError, IndexError, ValueError, json.JSONDecodeError) as exc:
        print('SYSTEM4_FAIL:' + str(exc))
        return 2


if __name__=='__main__':
    raise SystemExit(main(_engine.sys.argv))
