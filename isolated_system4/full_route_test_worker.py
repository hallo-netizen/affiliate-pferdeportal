from __future__ import annotations
import hashlib,json,os,re,sys
from pathlib import Path

import authoring_contract,no_codex_test_repair,root_entry,supervisor,worker_dispatch
from full_route_test_fixture import source_claims_for_article
from real_route_test_support import valid_real_article

RUN_NONCE_ENV='SYSTEM4_TEST_RUN_NONCE'
FORCE_REPAIR_INDEX_ENV='SYSTEM4_TEST_FORCE_REPAIR_INDEX'
REPO=Path(__file__).resolve().parent.parent


def write_json(path:Path,value):
    path.write_text(json.dumps(value,ensure_ascii=False,sort_keys=True),encoding='utf-8')

def _balance_conclusion(body:str,state:dict)->str:
    if state['article']['category'] not in {'pellets-beratung','fliegenmasken-beratung','pferdehaftpflicht-beratung'}: return body
    pattern=re.compile(r'(<section data-block="conclusion">.*?)(</section>)',re.S); match=pattern.search(body)
    if not match: raise RuntimeError('CONCLUSION_BLOCK_MISSING')
    section=match.group(1); last_p=section.rfind('</p>')
    if last_p<0: raise RuntimeError('CONCLUSION_PARAGRAPH_MISSING')
    keyword=state['article']['target_keyword']
    addition=(f' Für {keyword} bleibt die Auswahl an den gebundenen Kriterien auszurichten.'
              f' Beim Fazit zu {keyword} setzt der Quellenstand die Grenze.'
              f' Zusätzliche Tatsachen zu {keyword} werden nicht ergänzt.')
    section=section[:last_p]+addition+section[last_p:]
    result=body[:match.start(1)]+section+body[match.end(1):]
    authoring_contract.validate_candidate(result,state['authoring_contract']); return result

def _fresh_variation_index(index:int)->int:
    nonce=os.environ.get(RUN_NONCE_ENV,'').strip()
    if len(nonce)<12:
        raise RuntimeError('TEST_RUN_NONCE_REQUIRED')
    digest=hashlib.sha256((nonce+':'+str(index)).encode('utf-8')).hexdigest()
    return index+31+(int(digest[:8],16)%100003)

def _force_one_repairable_typo(body:str,index:int)->str:
    if os.environ.get(FORCE_REPAIR_INDEX_ENV,'').strip()!=str(index): return body
    replacements=((r'\bPrüfung\b','Prüfungg'),(r'\bEntscheidung\b','Entscheidungg'),(r'\bDokumentation\b','Dokumentationn'))
    for pattern,replacement in replacements:
        changed,count=re.subn(pattern,replacement,body,count=1)
        if count==1: return changed
    raise RuntimeError('FORCED_REPAIR_TOKEN_MISSING')

def main(argv):
    if len(argv)!=5:
        print('FULL_ROUTE_TEST_WORKER_FAIL:BAD_ARGS'); return 2
    mode=argv[1]; workspace=Path(argv[2]); out=Path(argv[3]); index=int(argv[4])
    try:
        manifest=root_entry._critical_manifest_sha256()
        head=root_entry._git('rev-parse','--verify','HEAD')
        wc,_=worker_dispatch.verify_workspace_dispatch(workspace,actual_manifest=manifest,actual_head=head)
        if wc.get('article_index')!=index: raise worker_dispatch.WorkerDispatchError('DISPATCH_TESTWORKER_INDEX_MISMATCH')
    except Exception as exc:
        print('FULL_ROUTE_TEST_WORKER_FAIL:DISPATCH_REQUIRED:'+str(exc)); return 2
    state_path=workspace/'state.json'
    if not state_path.is_file():
        print('FULL_ROUTE_TEST_WORKER_FAIL:STATE_MISSING'); return 2
    state=json.loads(state_path.read_text(encoding='utf-8'))
    if mode=='research':
        write_json(out,supervisor.expected_research_document(workspace)); return 0
    if mode=='facts':
        _,claims=source_claims_for_article(state['article'])
        write_json(out,{'contract':'SYSTEM4_FACTS_EVIDENCE_V1','claims':claims}); return 0
    if mode=='draft':
        if state.get('phase')!='DRAFT_REQUIRED':
            print('FULL_ROUTE_TEST_WORKER_FAIL:DRAFT_PHASE_REQUIRED'); return 2
        try:
            variation_index=_fresh_variation_index(index)
            body=_force_one_repairable_typo(_balance_conclusion(valid_real_article(state,variation_index),state),index)
        except RuntimeError as exc:
            print('FULL_ROUTE_TEST_WORKER_FAIL:'+str(exc)); return 2
        out.write_text(body,encoding='utf-8'); return 0
    if mode=='repair':
        if state.get('phase')!='REPAIR_REQUIRED':
            print('FULL_ROUTE_TEST_WORKER_FAIL:REPAIR_PHASE_REQUIRED'); return 2
        try:
            repaired=no_codex_test_repair.candidate_for_current_failure(REPO,workspace)
        except Exception as exc:
            print('FULL_ROUTE_TEST_WORKER_FAIL:REPAIR_ADAPTER:'+str(exc)); return 2
        out.write_text(repaired,encoding='utf-8'); return 0
    print('FULL_ROUTE_TEST_WORKER_FAIL:UNKNOWN_MODE'); return 2

if __name__=='__main__': raise SystemExit(main(sys.argv))
