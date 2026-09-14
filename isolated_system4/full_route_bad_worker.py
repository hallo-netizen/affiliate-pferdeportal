from __future__ import annotations
import json,sys
from pathlib import Path
import supervisor
from full_route_test_fixture import source_claims_for_article


def main(argv):
    if len(argv)!=5:return 2
    mode=argv[1]; ws=Path(argv[2]); out=Path(argv[3])
    state=json.loads((ws/'state.json').read_text(encoding='utf-8'))
    if mode=='research':
        doc=supervisor.expected_research_document(ws)
        doc['sources'][0]['source_url']='https://example.org/forbidden-unbound-research'
        out.write_text(json.dumps(doc,ensure_ascii=False),encoding='utf-8'); return 0
    if mode=='facts':
        _,claims=source_claims_for_article(state['article']); out.write_text(json.dumps({'contract':'SYSTEM4_FACTS_EVIDENCE_V1','claims':claims},ensure_ascii=False),encoding='utf-8'); return 0
    return 2
if __name__=='__main__':raise SystemExit(main(sys.argv))
