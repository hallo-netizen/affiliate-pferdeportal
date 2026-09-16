import hashlib,json,tempfile,unittest,re
from pathlib import Path
from full_chain import FullChainSupervisor
from test_full_chain_local import Checks, evidence

def token(value):
    v=value.strip().casefold().replace('ä','ae').replace('ö','oe').replace('ü','ue').replace('ß','ss')
    return re.sub(r'[^a-z0-9]+','-',v).strip('-')

def make_snapshot(path):
    types=['Beratung','Wissen','Rassen-Porträt']; items=[]
    for i,t in enumerate(types):
        items.append({'title':f'Titel {i}','target_keyword':f'Keyword {i}','category':f'cat-{i}','article_type':t,'plan_slot':hashlib.sha256(f'type-slot-{i}'.encode()).hexdigest()})
    batch={'contract':'PSERC_TEXTMACHINE_METADATA_BATCH_V2','status':'READY_FOR_TEXTMACHINE_METADATA_INTAKE','batch_sha256':hashlib.sha256(b'types').hexdigest(),'item_count':len(items),'items':items,'publish_allowed':False}
    path.write_text(json.dumps({'next_textmachine_metadata_batch':batch},ensure_ascii=False)); return items

def worker(req):
    research,facts,pack,plan=evidence(req); task=req['task']; a=req['article']; idx=a['title'].split()[-1]
    if task=='research': return {'content':json.dumps(research,ensure_ascii=False)}
    if task=='facts': return {'content':json.dumps(facts,ensure_ascii=False)}
    if task=='context': return {'content':json.dumps({'fact_pack':pack,'production_plan_item':plan},ensure_ascii=False)}
    unique=' '.join(f'type{idx}_{n}' for n in range(90)); klass='ppm-type-'+token(a['article_type'])
    body=f'<article class="ppm-generated {klass}" data-article-type="{a["article_type"]}"><h2>{a["title"]}</h2><p data-fact-ids="f-{idx}-a f-{idx}-b">{unique} eigenständiger Inhalt.</p><table class="system-129-table comparison-table"><tr><th>A</th><th>B</th></tr><tr><td>{idx}</td><td>Wert</td></tr></table></article>'
    return {'content':body}

class ArticleTypeFullChainTests(unittest.TestCase):
    def test_mixed_new_article_types_use_same_full_chain(self):
        with tempfile.TemporaryDirectory() as td:
            root=Path(td); snap=root/'s.json'; items=make_snapshot(snap); out=root/'handoff.json'; sup=FullChainSupervisor(mode='test',checks=Checks()); result=sup.run_full(snap,worker,out)
            self.assertEqual(result['article_count'],3); payload=json.loads(out.read_text()); self.assertEqual([r['article_type'] for r in payload['articles']],[i['article_type'] for i in items]); self.assertEqual(sup.verify_output(out)['article_count'],3)

if __name__=='__main__': unittest.main(verbosity=2)
