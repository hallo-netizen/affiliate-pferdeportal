import copy,hashlib,json,subprocess,sys,tempfile,unittest
from pathlib import Path

HERE=Path(__file__).resolve().parent; REPO=HERE.parent
sys.path.insert(0,str(HERE))
import point0_snapshot,root_entry

def h(v):return hashlib.sha256(v.encode()).hexdigest()
def head():return subprocess.run(['git','rev-parse','HEAD'],cwd=REPO,text=True,capture_output=True,check=True).stdout.strip()
def production():
 v=json.loads((HERE/'live_fixture/wordpress_snapshot.json').read_text(encoding='utf-8'));v['system4_root_manifest_sha256']=root_entry._critical_manifest_sha256();return json.dumps(v,ensure_ascii=False,sort_keys=True,separators=(',',':')).encode()
def source():
 ev='Reale gebundene Quellenbeobachtung für den zweistufigen Point-0-Test mit ausreichend langem Evidenztext.'
 return {'source_id':'p0-stage-source-1','source_title':'Point0 Stage Source','source_url':'https://example.org/point0-stage','retrieved_at':'2026-09-14T00:00:00Z','evidence':ev,'snapshot_sha256':h(ev),'http_status':200,'source_kind':'WEB'}

class Point0PrepareFinalizeTests(unittest.TestCase):
 def test_prepared_contains_no_sources_and_final_binds_them(self):
  raw=production();p=point0_snapshot.prepare(production_snapshot_bytes=raw,root_manifest_sha256=root_entry._critical_manifest_sha256(),head_sha=head());self.assertEqual(p['contract'],point0_snapshot.PREPARED_CONTRACT);self.assertEqual(p['research_runtime'],{'status':'REQUIRED'});self.assertNotIn('sources',p['research_runtime']);self.assertEqual(point0_snapshot.verify_prepared(p),raw)
  final=point0_snapshot.finalize(p,research_provider='BOUND_MACHINE_RESEARCH_RUNTIME',sources=[source()]);self.assertEqual(final['contract'],point0_snapshot.CONTRACT);self.assertEqual(final['prepared_point0_sha256'],p['point0_prepared_sha256']);self.assertEqual(final['research_runtime']['source_count'],1);self.assertEqual(point0_snapshot.verify(final),raw)
 def test_prepared_tamper_blocks_finalize(self):
  p=point0_snapshot.prepare(production_snapshot_bytes=production(),root_manifest_sha256=root_entry._critical_manifest_sha256(),head_sha=head());p['head_sha']='0'*40
  with self.assertRaisesRegex(point0_snapshot.Point0Error,'POINT0_PREPARED_INTEGRITY_FAIL'):point0_snapshot.finalize(p,research_provider='X',sources=[source()])
 def test_source_hash_tamper_blocks_finalize(self):
  p=point0_snapshot.prepare(production_snapshot_bytes=production(),root_manifest_sha256=root_entry._critical_manifest_sha256(),head_sha=head());s=source();s['evidence']+=' tamper'
  with self.assertRaisesRegex(point0_snapshot.Point0Error,'RESEARCH_SOURCE_HASH_MISMATCH'):point0_snapshot.finalize(p,research_provider='X',sources=[s])
 def test_http_failure_blocks_finalize(self):
  p=point0_snapshot.prepare(production_snapshot_bytes=production(),root_manifest_sha256=root_entry._critical_manifest_sha256(),head_sha=head());s=source();s['http_status']=403
  with self.assertRaisesRegex(point0_snapshot.Point0Error,'RESEARCH_SOURCE_HTTP_FAIL'):point0_snapshot.finalize(p,research_provider='X',sources=[s])
 def test_final_cannot_be_rebound_to_other_prepared_snapshot(self):
  raw=production();p=point0_snapshot.prepare(production_snapshot_bytes=raw,root_manifest_sha256=root_entry._critical_manifest_sha256(),head_sha=head());final=point0_snapshot.finalize(p,research_provider='X',sources=[source()]);final['prepared_point0_sha256']='0'*64;core=dict(final);core.pop('point0_core_sha256');final['point0_core_sha256']=point0_snapshot.sha256(point0_snapshot.canon(core))
  with self.assertRaisesRegex(point0_snapshot.Point0Error,'POINT0_PREPARED_BINDING_MISMATCH'):point0_snapshot.verify(final)

if __name__=='__main__':unittest.main(verbosity=2)
