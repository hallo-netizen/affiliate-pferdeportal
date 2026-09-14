import copy,hashlib,json,subprocess,sys,tempfile,unittest
from pathlib import Path

ROOT=Path(__file__).resolve().parent.parent; S4=ROOT/'isolated_system4'; ENTRY=S4/'root_entry.py'; LIVE=S4/'LIVE_BOUND_INPUT_ONE_ARTICLE.json'
sys.path.insert(0,str(S4)); import point0_snapshot,root_entry

def canon(v): return json.dumps(v,ensure_ascii=False,sort_keys=True,separators=(',',':')).encode()
def manifest(): return root_entry._critical_manifest_sha256()
def head(): return subprocess.run(['git','rev-parse','HEAD'],cwd=ROOT,text=True,capture_output=True,check=True).stdout.strip()
def source():
 ev='Gebundene Quellenbeobachtung fuer den exakten Live-Input-Test mit ausreichendem echten Evidenzumfang.'
 return {'source_id':'live-source-1','source_url':'https://example.org/live-source','source_title':'Live Source Evidence','retrieved_at':'2026-09-14T00:00:00Z','evidence':ev,'snapshot_sha256':hashlib.sha256(ev.encode()).hexdigest(),'http_status':200,'source_kind':'WEB'}
def production(value=None):
 v=copy.deepcopy(value if value is not None else json.loads(LIVE.read_text())); v['system4_root_manifest_sha256']=manifest(); return canon(v)
def build_point0(raw): return point0_snapshot.canon(point0_snapshot.build(production_snapshot_bytes=raw,root_manifest_sha256=manifest(),head_sha=head(),research_provider='BOUND_MACHINE_RESEARCH_RUNTIME',sources=[source()]))
def run_p0(p0,workspace):
 p=Path(workspace).parent/'point0.json'; p.write_bytes(p0); return subprocess.run([sys.executable,str(ENTRY),'start-point0',str(p),str(workspace)],cwd=ROOT,stdout=subprocess.PIPE,stderr=subprocess.PIPE)

class ExactLiveBoundInputV4Tests(unittest.TestCase):
 def test_live_article_metadata_is_still_exact(self):
  v=json.loads(LIVE.read_text()); item=v['next_textmachine_metadata_batch']['items'][0]; self.assertEqual(v['next_textmachine_metadata_batch']['item_count'],1); self.assertEqual(item['article_type'],'Beratung'); self.assertEqual(item['category'],'putzbox-beratung'); self.assertEqual(item['plan_slot'],'88043c35da332d4b2a500d1b61919721aefadf894bc923c841cc849a132c63b5'); self.assertEqual(item['target_keyword'],'Putzbox für Pferde'); self.assertEqual(item['title'],'Putzbox für Pferde richtig auswählen'); self.assertFalse(v['next_textmachine_metadata_batch']['publish_allowed'])
 def test_positive_point0_preserves_production_snapshot_bytes(self):
  raw=production()
  with tempfile.TemporaryDirectory(prefix='s4-live-p0-') as td:
   ws=Path(td)/'ws'; cp=run_p0(build_point0(raw),ws); out=cp.stdout.decode()+cp.stderr.decode(); self.assertEqual(cp.returncode,0,out); self.assertIn('SYSTEM4_ROOT_POINT0_PASS:WORKER_DISPATCH_READY',out); self.assertEqual((ws/'bound_snapshot.json').read_bytes(),raw)
 def test_publish_true_blocks_before_dispatch(self):
  v=json.loads(LIVE.read_text()); v['next_textmachine_metadata_batch']['publish_allowed']=True
  with self.assertRaisesRegex(point0_snapshot.Point0Error,'PUBLISH_AUTHORITY_FAIL'): build_point0(production(v))
 def test_source_hash_tamper_blocks(self):
  raw=production(); p=json.loads(build_point0(raw)); p['research_runtime']['sources'][0]['evidence']+=' tamper'; core=dict(p); core.pop('point0_core_sha256'); p['point0_core_sha256']=hashlib.sha256(point0_snapshot.canon(core)).hexdigest()
  with tempfile.TemporaryDirectory(prefix='s4-live-neg-') as td:
   ws=Path(td)/'ws'; cp=run_p0(point0_snapshot.canon(p),ws); self.assertEqual(cp.returncode,2); self.assertIn('RESEARCH_SOURCE_HASH_MISMATCH',cp.stdout.decode()); self.assertFalse((ws/'worker_dispatch.json').exists())
 def test_repo_internal_workspace_blocks(self):
  raw=production(); p0=build_point0(raw)
  with tempfile.TemporaryDirectory(prefix='s4-live-neg-') as td:
   p=Path(td)/'point0.json'; p.write_bytes(p0); cp=subprocess.run([sys.executable,str(ENTRY),'start-point0',str(p),str(S4/'forbidden-live-workspace')],cwd=ROOT,stdout=subprocess.PIPE,stderr=subprocess.PIPE); self.assertEqual(cp.returncode,2); self.assertIn('ROOT_ENTRY_WORKSPACE_MUST_BE_OUTSIDE_REPO',cp.stdout.decode())

if __name__=='__main__': unittest.main(verbosity=2)
