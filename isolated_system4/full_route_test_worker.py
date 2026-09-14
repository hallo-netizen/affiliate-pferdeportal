from __future__ import annotations
import json,re,sys
from pathlib import Path

import authoring_contract,supervisor
from full_route_test_fixture import source_claims_for_article
from real_route_test_support import valid_real_article


def write_json(path:Path,value):
    path.write_text(json.dumps(value,ensure_ascii=False,sort_keys=True),encoding='utf-8')

def _balance_conclusion(body:str,state:dict)->str:
    if state['article']['category'] not in {'pellets-beratung','fliegenmasken-beratung','pferdehaftpflicht-beratung'}: return body
    pattern=re.compile(r'(<section data-block="conclusion">.*?)(</section>)',re.S); match=pattern.search(body)
    if not match: raise RuntimeError('CONCLUSION_BLOCK_MISSING')
    section=match.group(1); last_p=section.rfind('</p>')
    if last_p<0: raise RuntimeError('CONCLUSION_PARAGRAPH_MISSING')
    keyword=state['article']['target_keyword']
    addition=f' Zusätzlich bleibt für {keyword} der gebundene Quellenstand maßgeblich; weitergehende Tatsachen werden im Fazit ausdrücklich nicht ergänzt.'
    section=section[:last_p]+addition+section[last_p:]
    result=body[:match.start(1)]+section+body[match.end(1):]
    authoring_contract.validate_candidate(result,state['authoring_contract']); return result

def main(argv):
    if len(argv)!=5:
        print('FULL_ROUTE_TEST_WORKER_FAIL:BAD_ARGS'); return 2
    mode=argv[1]; workspace=Path(argv[2]); out=Path(argv[3]); index=int(argv[4])
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
        body=_balance_conclusion(valid_real_article(state,index),state)
        out.write_text(body,encoding='utf-8'); return 0
    print('FULL_ROUTE_TEST_WORKER_FAIL:UNKNOWN_MODE'); return 2

if __name__=='__main__': raise SystemExit(main(sys.argv))
