import json, subprocess, sys, tempfile, unittest
from pathlib import Path
from full_chain import FullChainSupervisor
from test_full_chain_local import Checks, snapshot

WORKER = r'''import json,sys,hashlib,pathlib
r=json.load(sys.stdin)
for name in ('AGENTS.md','state.json','CURRENT_STATE.json','control','isolated_system4','isolated_system4a'):
    if pathlib.Path(name).exists():
        print(json.dumps({'error':'WORKER_AUTHORITY_SURFACE_VISIBLE:'+name})); raise SystemExit(3)
a=r['article']; i=a['title'].split()[-1]; t=r['task']
def sh(x): return hashlib.sha256(x.encode()).hexdigest()
e1=f'Gesicherter konkreter Beleg A für Artikel {i} mit eindeutiger fachlicher Aussage und sicherer Nutzung.'
e2=f'Gesicherter konkreter Beleg B für Artikel {i} mit einer zweiten fachlichen Aussage zur Auswahl.'
ev=e1+'\\n'+e2+'\\nZusätzlicher gesicherter Quellenkontext.'; sid=f'src-{i}'
src={'source_id':sid,'source_title':f'Fachquelle {i}','source_url':f'https://example.org/source-{i}','retrieved_at':'2026-09-13T08:00:00Z','snapshot_sha256':sh(ev),'evidence':ev}
claims=[{'fact_id':f'f-{i}-a','source_id':sid,'statement':f'Konkrete erste Aussage für Artikel {i}.','evidence_text':e1,'evidence_text_sha256':sh(e1)},{'fact_id':f'f-{i}-b','source_id':sid,'statement':f'Konkrete zweite Aussage für Artikel {i}.','evidence_text':e2,'evidence_text_sha256':sh(e2)}]
if t=='research': c=json.dumps({'contract':'SYSTEM4_RESEARCH_EVIDENCE_V1','sources':[src]},ensure_ascii=False)
elif t=='facts': c=json.dumps({'contract':'SYSTEM4_FACTS_EVIDENCE_V1','claims':claims},ensure_ascii=False)
elif t=='context': c=json.dumps({'fact_pack':{'contract':'canonical_fact_pack_v1','status':'SOURCE_VERIFIED_PRODUCTION_READY','sources':[src],'claims':claims},'production_plan_item':{'article_type':a['article_type'],'topic':a['title'],'target_keyword':a['target_keyword'],'category_binding':{'slug':a['category']}}},ensure_ascii=False)
else:
    unique=' '.join(f'eigen{i}_{n}' for n in range(90))
    c=f'<article class="ppm-generated ppm-type-beratung" data-article-type="Beratung"><h2>{a["title"]}</h2><p data-fact-ids="f-{i}-a f-{i}-b">{unique} eindeutige fachliche Struktur.</p><table class="system-129-table comparison-table"><tr><th>A</th><th>B</th></tr><tr><td>{i}</td><td>Wert</td></tr></table></article>'
json.dump({'content':c},sys.stdout,ensure_ascii=False)
'''

class WorkerIsolationTests(unittest.TestCase):
    def test_full_chain_worker_runs_without_repository_authority_surface(self):
        with tempfile.TemporaryDirectory() as td:
            root=Path(td); worker_room=root/'worker-room'; worker_room.mkdir(); script=worker_room/'worker.py'; script.write_text(WORKER)
            snap=root/'snapshot.json'; snapshot(snap,1); out=root/'handoff.json'
            def worker(req):
                p=subprocess.run([sys.executable,'worker.py'],cwd=worker_room,input=json.dumps(req,ensure_ascii=False),text=True,capture_output=True)
                self.assertEqual(p.returncode,0,p.stdout+p.stderr)
                return json.loads(p.stdout)
            sup=FullChainSupervisor(mode='test',checks=Checks()); result=sup.run_full(snap,worker,out)
            self.assertEqual(result['status'],'SYSTEM4A_FULL_CHAIN_ARCHITECTURE_PASS')
            self.assertEqual(sorted(x.name for x in worker_room.iterdir()),['worker.py'])

    def test_negative_repository_authority_surface_in_worker_room_is_detected(self):
        with tempfile.TemporaryDirectory() as td:
            room=Path(td); (room/'worker.py').write_text(WORKER); (room/'AGENTS.md').write_text('foreign authority')
            req={'task':'research','article':{'title':'Titel 0','target_keyword':'K','category':'c','article_type':'Beratung','plan_slot':'a'*64}}
            p=subprocess.run([sys.executable,'worker.py'],cwd=room,input=json.dumps(req),text=True,capture_output=True)
            self.assertEqual(p.returncode,3); self.assertIn('WORKER_AUTHORITY_SURFACE_VISIBLE:AGENTS.md',p.stdout)

if __name__=='__main__': unittest.main(verbosity=2)
