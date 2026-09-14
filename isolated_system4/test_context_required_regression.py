import hashlib,json,subprocess,sys,tempfile,unittest
from pathlib import Path

HERE=Path(__file__).resolve().parent; ROOT=HERE.parent; CONTROLLER=HERE/'controller.py'; ROOT_ENTRY=HERE/'root_entry.py'; CODEX_ENTRY=HERE/'codex_entry.py'
sys.path.insert(0,str(HERE)); import point0_snapshot,root_entry,supervisor

def h(text): return hashlib.sha256(text.encode()).hexdigest()
def run(argv): return subprocess.run(argv,cwd=ROOT,stdout=subprocess.PIPE,stderr=subprocess.PIPE,check=False)
def head(): return run(['git','rev-parse','HEAD']).stdout.decode().strip()

class ContextRequiredRegressionTests(unittest.TestCase):
 def test_facts_cannot_open_draft_directly(self):
  with tempfile.TemporaryDirectory(prefix='system4-context-required-') as td0:
   td=Path(td0); workspace=td/'workspace'; evidence='Diese reale Testquelle enthält genügend gebundenen Belegtext für zwei unterschiedliche, nachvollziehbare Aussagen im System-4-Test.'
   production={'contract':'SYSTEM4_WORDPRESS_LIVE_INPUT_FIXTURE_V1','source_snapshot_original_sha256':h('context-source'),'system4_root_manifest_sha256':root_entry._critical_manifest_sha256(),'next_textmachine_metadata_batch':{'contract':'PSERC_TEXTMACHINE_METADATA_BATCH_V2','status':'READY_FOR_TEXTMACHINE_METADATA_INTAKE','publish_allowed':False,'batch_sha256':h('context-required-batch'),'item_count':1,'maximum_articles':0,'maximum_articles_per_type':0,'content_or_format_payload_present':False,'items':[{'title':'Das Wichtigste über Hindernisstangen für Pferde','target_keyword':'Hindernisstangen für Pferde','category':'hindernisstangen-beratung','article_type':'Beratung','plan_slot':'9c229b0e6a784a482575e3deb16d105e3b5355becbbbb8ecfc8e1f600b529c56'}]}}
   raw=json.dumps(production,ensure_ascii=False,sort_keys=True,separators=(',',':')).encode()
   src={'source_id':'src-1','source_title':'Reale Testquelle Kontextbindung','source_url':'https://example.org/system4/contextbindung','retrieved_at':'2026-09-14T00:00:00Z','snapshot_sha256':h(evidence),'evidence':evidence,'http_status':200,'source_kind':'WEB'}
   p0=point0_snapshot.build(production_snapshot_bytes=raw,root_manifest_sha256=root_entry._critical_manifest_sha256(),head_sha=head(),research_provider='BOUND_MACHINE_RESEARCH_RUNTIME',sources=[src]); p0p=td/'point0.json'; p0p.write_bytes(point0_snapshot.canon(p0))
   cp=run([sys.executable,str(ROOT_ENTRY),'start-point0',str(p0p),str(workspace)]); self.assertEqual(cp.returncode,0,cp.stdout.decode()+cp.stderr.decode())
   research=td/'research.json'; research.write_text(json.dumps(supervisor.expected_research_document(workspace),ensure_ascii=False),encoding='utf-8')
   ev1='Diese reale Testquelle enthält genügend gebundenen Belegtext'; ev2='für zwei unterschiedliche, nachvollziehbare Aussagen im System-4-Test.'
   facts=td/'facts.json'; facts.write_text(json.dumps({'contract':'SYSTEM4_FACTS_EVIDENCE_V1','claims':[{'fact_id':'fact-1','source_id':'src-1','statement':'Der Kontext muss vor dem Schreiben verbindlich gebunden sein.','evidence_text':ev1,'evidence_text_sha256':h(ev1)},{'fact_id':'fact-2','source_id':'src-1','statement':'Eine spätere bekannte Pflicht darf nicht erst im Fullcheck auftauchen.','evidence_text':ev2,'evidence_text_sha256':h(ev2)}]},ensure_ascii=False),encoding='utf-8')
   for argv in ([sys.executable,str(CONTROLLER),'research',str(workspace),str(research)],[sys.executable,str(CONTROLLER),'facts',str(workspace),str(facts)]):
    cp=run(argv); self.assertEqual(cp.returncode,0,cp.stdout.decode()+cp.stderr.decode())
   state=json.loads((workspace/'state.json').read_text()); self.assertEqual(state['phase'],'CONTEXT_REQUIRED'); self.assertIsNone(state['production_context']); self.assertIsNone(state['authoring_contract'])
   draft=td/'draft.html'; draft.write_text('<article>nicht zulässig vor Context</article>',encoding='utf-8'); blocked=run([sys.executable,str(CONTROLLER),'draft',str(workspace),str(draft)]); self.assertEqual(blocked.returncode,2); self.assertIn('PHASE_FAIL:DRAFT',blocked.stdout.decode())
   state_after=json.loads((workspace/'state.json').read_text()); self.assertEqual(state_after['phase'],'CONTEXT_REQUIRED'); self.assertEqual(state_after['revision'],0)
   entry=run([sys.executable,str(CODEX_ENTRY),'next',str(workspace)]); self.assertEqual(entry.returncode,0,entry.stdout.decode()+entry.stderr.decode()); self.assertIn('SYSTEM4_CODEX_ENTRY_PASS:CONTEXT_REQUIRED',entry.stdout.decode())

if __name__=='__main__': unittest.main(verbosity=2)
