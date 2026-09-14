import hashlib,json,shutil,subprocess,sys,tempfile,unittest
from pathlib import Path

SOURCE_ROOT=Path(__file__).resolve().parent.parent

def run(argv,*,cwd,check=False):
 return subprocess.run(argv,cwd=cwd,stdout=subprocess.PIPE,stderr=subprocess.PIPE,check=check)

def make_repo():
 td=tempfile.TemporaryDirectory(prefix='system4-root-v4-'); repo=Path(td.name)/'repo'
 shutil.copytree(SOURCE_ROOT,repo,ignore=lambda p,n:[x for x in n if x in {'.git','__pycache__'} or x.endswith('.pyc')])
 run(['git','init','-q'],cwd=repo); run(['git','config','user.email','system4@test.invalid'],cwd=repo); run(['git','config','user.name','System4 Test'],cwd=repo)
 run(['git','add','.'],cwd=repo); run(['git','commit','-qm','snapshot'],cwd=repo); return td,repo

def py(repo,code):
 cp=run([sys.executable,'-c',code],cwd=repo); assert cp.returncode==0,cp.stdout.decode()+cp.stderr.decode(); return cp.stdout.decode().strip()

def manifest(repo): return py(repo,"import sys;sys.path.insert(0,'isolated_system4');import root_entry;print(root_entry._critical_manifest_sha256())")
def head(repo): return run(['git','rev-parse','HEAD'],cwd=repo).stdout.decode().strip()

def make_point0(repo,out):
 m=manifest(repo); raw=json.loads((repo/'isolated_system4/live_fixture/wordpress_snapshot.json').read_text(encoding='utf-8')); raw['system4_root_manifest_sha256']=m
 prod=(json.dumps(raw,ensure_ascii=False,sort_keys=True,separators=(',',':'))).encode()
 ev='Gebundene reale Quellenbeobachtung fuer den Root-Grenztest mit ausreichend langem Evidenztext.'
 src=[{'source_id':'source-root-1','source_url':'https://example.org/root-source','source_title':'Root Source Evidence','retrieved_at':'2026-09-14T00:00:00Z','evidence':ev,'snapshot_sha256':hashlib.sha256(ev.encode()).hexdigest(),'http_status':200,'source_kind':'WEB'}]
 code="import sys,json;sys.path.insert(0,'isolated_system4');import point0_snapshot;from pathlib import Path;prod=Path(%r).read_bytes();src=json.loads(Path(%r).read_text());v=point0_snapshot.build(production_snapshot_bytes=prod,root_manifest_sha256=%r,head_sha=%r,research_provider='BOUND_MACHINE_RESEARCH_RUNTIME',sources=src);Path(%r).write_bytes(point0_snapshot.canon(v))"%(str(out)+'.prod',str(out)+'.src',m,head(repo),str(out))
 Path(str(out)+'.prod').write_bytes(prod); Path(str(out)+'.src').write_text(json.dumps(src),encoding='utf-8'); py(repo,code)
 return out

def entry(repo,p0,workspace): return run([sys.executable,str(repo/'isolated_system4/root_entry.py'),'start-point0',str(p0),str(workspace)],cwd=repo)

class RootEntryV4Tests(unittest.TestCase):
 def prep(self):
  td,repo=make_repo(); self.addCleanup(td.cleanup); p0=make_point0(repo,Path(td.name)/'point0.json'); return td,repo,p0
 def test_positive_only_point0_door(self):
  td,repo,p0=self.prep(); ws=Path(td.name)/'ws'; cp=entry(repo,p0,ws); self.assertEqual(cp.returncode,0,cp.stdout.decode()+cp.stderr.decode()); self.assertIn('SYSTEM4_ROOT_POINT0_PASS:WORKER_DISPATCH_READY',cp.stdout.decode()); self.assertTrue((ws/'worker_dispatch.json').is_file())
 def test_legacy_start_and_stdin_are_hard_blocked(self):
  td,repo,p0=self.prep()
  for cmd in ('start','start-stdin'):
   cp=run([sys.executable,str(repo/'isolated_system4/root_entry.py'),cmd],cwd=repo); self.assertEqual(cp.returncode,2); self.assertIn('ROOT_POINT0_REQUIRED',cp.stdout.decode())
 def test_override_binds_v4_point0_only(self):
  td,repo,p0=self.prep(); text=(repo/'AGENTS.override.md').read_text(); self.assertIn('SYSTEM4_ISOLATED_ROOT_ENTRY_V4_POINT0_ONLY',text); self.assertIn('root_entry.py start-point0',text); self.assertIn('start` and `start-stdin` are forbidden',text)
 def test_internal_workspace_blocks(self):
  td,repo,p0=self.prep(); cp=entry(repo,p0,repo/'isolated_system4/forbidden'); self.assertEqual(cp.returncode,2); self.assertIn('ROOT_ENTRY_WORKSPACE_MUST_BE_OUTSIDE_REPO',cp.stdout.decode())
 def test_internal_point0_blocks(self):
  td,repo,p0=self.prep(); inside=repo/'isolated_system4/point0.json'; inside.write_bytes(p0.read_bytes()); cp=entry(repo,inside,Path(td.name)/'ws'); self.assertEqual(cp.returncode,2); self.assertIn('ROOT_POINT0_FILE_INVALID',cp.stdout.decode())
 def test_dirty_critical_file_blocks(self):
  td,repo,p0=self.prep(); f=repo/'isolated_system4/controller.py'; f.write_text(f.read_text()+'\n# tamper\n'); cp=entry(repo,p0,Path(td.name)/'ws'); self.assertEqual(cp.returncode,2); self.assertIn('ROOT_ENTRY_CRITICAL_FILES_DIRTY',cp.stdout.decode())
 def test_point0_head_mismatch_blocks(self):
  td,repo,p0=self.prep(); v=json.loads(p0.read_text()); v['head_sha']='0'*40; core=dict(v); core.pop('point0_core_sha256',None); v['point0_core_sha256']=hashlib.sha256((json.dumps(core,ensure_ascii=False,sort_keys=True,separators=(',',':'))+'\n').encode()).hexdigest(); p0.write_text(json.dumps(v)); cp=entry(repo,p0,Path(td.name)/'ws'); self.assertEqual(cp.returncode,2); self.assertIn('HEAD_SHA_MISMATCH',cp.stdout.decode())
 def test_point0_source_hash_tamper_blocks(self):
  td,repo,p0=self.prep(); v=json.loads(p0.read_text()); v['research_runtime']['sources'][0]['evidence']+=' TAMPER'; core=dict(v); core.pop('point0_core_sha256',None); v['point0_core_sha256']=hashlib.sha256((json.dumps(core,ensure_ascii=False,sort_keys=True,separators=(',',':'))+'\n').encode()).hexdigest(); p0.write_text(json.dumps(v)); cp=entry(repo,p0,Path(td.name)/'ws'); self.assertEqual(cp.returncode,2); self.assertIn('RESEARCH_SOURCE_HASH_MISMATCH',cp.stdout.decode())

if __name__=='__main__': unittest.main(verbosity=2)
