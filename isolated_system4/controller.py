from __future__ import annotations

"""System 4 controller with owner-aware repair return routing.

The previous controller is retained byte-identically in controller_engine.py.  This
public module changes only the fullcheck repair-routing seam: DRAFT_WORKER keeps the
existing same-article repair path; parent/machine owners return RC=4 without mutating
the bound article or draft. Unknown/missing/conflicting owner data remains fail-closed.
"""

import controller_engine as _engine

# Re-export the existing controller API first so existing callers/tests keep the same surface.
for _name in dir(_engine):
    if not _name.startswith('__') and _name not in {'cmd_fullcheck', 'main'}:
        globals()[_name] = getattr(_engine, _name)


DRAFT_WORKER = 'DRAFT_WORKER'
PARENT_LAUNCH = 'PARENT_LAUNCH'


def _repair_owner(e):
    findings = e.findings if isinstance(getattr(e, 'findings', None), list) else []
    owners = {str(row.get('repair_owner') or '').strip() for row in findings if isinstance(row, dict) and str(row.get('repair_owner') or '').strip()}
    checker = str(getattr(e, 'checker', '') or '')
    # LT and the explicit external-link checker operate on the current article draft.
    if not owners and checker in {'languagetool', 'no_external_links'}:
        return DRAFT_WORKER
    if not owners:
        raise Fail('REPAIR_OWNER_MISSING:'+checker)
    if len(owners) != 1:
        raise Fail('REPAIR_OWNER_CONFLICT:'+','.join(sorted(owners)))
    return next(iter(owners))


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
        # Parent/machine return is not PASS and not a draft repair. Keep CHECK_REQUIRED so
        # the exact same bound draft remains frozen until the owning upstream stage repairs.
        s['checks']['return_required']=True
        s['checks']['return_route']=PARENT_LAUNCH
        s['phase']='CHECK_REQUIRED'; save(s,p)
        print('SYSTEM4_REPAIR_OWNER_RETURN:'+owner+':'+PARENT_LAUNCH+':'+error); return 4
    except production_checks.ProductionCheckError as e:
        raise Fail('FULL_CHECK_HARD_BLOCK:'+str(e)) from e
    s['checks']={'status':'PASS','mode':'FULL_PRODUCTION','errors':[],'checked_draft_sha256':s['draft_sha256'],'production_evidence':result}
    s['last_error']=None; s['phase']='OUTPUT_GATE_REQUIRED'; save(s,p)
    print('SYSTEM4_FULL_CHECK_PASS:OUTPUT_GATE_REQUIRED'); return 0


# The preserved engine's main resolves cmd_fullcheck from its own module globals.
_engine.cmd_fullcheck = cmd_fullcheck


def main(argv):
    return _engine.main(argv)


if __name__=='__main__':
    raise SystemExit(main(_engine.sys.argv))
