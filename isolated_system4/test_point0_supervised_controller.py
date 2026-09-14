from __future__ import annotations
import hashlib, json, subprocess, tempfile, unittest
from pathlib import Path
import sys

HERE=Path(__file__).resolve().parent
REPO=HERE.parent
sys.path.insert(0,str(HERE))
import controller, point0_snapshot, root_entry


def canon(v): return (json.dumps(v,ensure_ascii=False,sort_keys=True,separators=(',',':'))+'\n').encode()
def h(text): return hashlib.sha256(text.encode()).hexdigest()

class Point0SupervisorControllerTest(unittest.TestCase):
    def production_snapshot(self, manifest):
        value=json.loads((HERE/'LIVE_BOUND_INPUT_ONE_ARTICLE.json').read_text(encoding='utf-8'))
        value['system4_root_manifest_sha256']=manifest
        return canon(value)

    def production_batch_snapshot(self, manifest):
        value=json.loads((HERE/'live_fixture/wordpress_snapshot.json').read_text(encoding='utf-8'))
        value['system4_root_manifest_sha256']=manifest
        return canon(value)

    def source(self):
        evidence='Pferdeputzzeug sollte sauber, trocken und übersichtlich gelagert werden, damit Verschmutzungen früh erkannt werden können.'
        return {'source_id':'source-test-1','source_title':'Fachinformation zur Pferdepflege','source_url':'https://example.org/pferdepflege/fachinformation','retrieved_at':'2026-09-14T10:00:00+02:00','evidence':evidence,'snapshot_sha256':h(evidence),'http_status':200,'source_kind':'test-real-http-contract'}

    def prepare_point0(self, base, batch=False):
        workspace=base/'workspace'; manifest=root_entry._critical_manifest_sha256()
        head=subprocess.run(['git','rev-parse','HEAD'],cwd=REPO,text=True,capture_output=True,check=True).stdout.strip()
        raw=self.production_batch_snapshot(manifest) if batch else self.production_snapshot(manifest)
        p0=point0_snapshot.build(production_snapshot_bytes=raw,root_manifest_sha256=manifest,head_sha=head,research_provider='SYSTEM4_TEST_BOUND_SOURCE_PROVIDER',sources=[self.source()])
        p=base/'point0.json'; p.write_bytes(point0_snapshot.canon(p0)); return p,workspace,p0

    def test_01_direct_controller_ingress_without_supervisor_blocks_and_leaves_no_state(self):
        with tempfile.TemporaryDirectory(prefix='system4-direct-block-') as td:
            base=Path(td); manifest=root_entry._critical_manifest_sha256(); snap=base/'snapshot.json'; snap.write_bytes(self.production_snapshot(manifest)); workspace=base/'workspace'
            rc=controller.main(['controller.py','ingress',str(snap),str(workspace),'0'])
            self.assertEqual(rc,2); self.assertFalse((workspace/'state.json').exists())

    def test_02_root_point0_creates_bound_dispatch_and_controller_state(self):
        with tempfile.TemporaryDirectory(prefix='system4-point0-pass-') as td:
            base=Path(td); p0,workspace,_=self.prepare_point0(base)
            rc=root_entry.main(['root_entry.py','start-point0',str(p0),str(workspace)])
            self.assertEqual(rc,0)
            self.assertTrue((workspace/'supervisor_state.json').is_file())
            self.assertTrue((workspace/'root_receipt.json').is_file())
            self.assertTrue((workspace/'worker_dispatch.json').is_file())
            self.assertTrue((workspace/'state.json').is_file())

    def test_03_exact_bound_research_passes(self):
        with tempfile.TemporaryDirectory(prefix='system4-research-pass-') as td:
            base=Path(td); p0,workspace,p0v=self.prepare_point0(base)
            self.assertEqual(root_entry.main(['root_entry.py','start-point0',str(p0),str(workspace)]),0)
            s=p0v['research_runtime']['sources'][0]
            research={'contract':'SYSTEM4_RESEARCH_EVIDENCE_V1','sources':[{k:s[k] for k in ('source_id','source_title','source_url','retrieved_at','evidence','snapshot_sha256','source_kind')}]}
            rp=base/'research.json'; rp.write_bytes(canon(research))
            self.assertEqual(controller.main(['controller.py','research',str(workspace),str(rp)]),0)
            state=json.loads((workspace/'state.json').read_text(encoding='utf-8')); self.assertEqual(state['phase'],'FACT_CHECK_REQUIRED')

    def test_04_unbound_research_url_blocks_without_state_advance(self):
        with tempfile.TemporaryDirectory(prefix='system4-research-block-') as td:
            base=Path(td); p0,workspace,p0v=self.prepare_point0(base)
            self.assertEqual(root_entry.main(['root_entry.py','start-point0',str(p0),str(workspace)]),0)
            s=p0v['research_runtime']['sources'][0]
            research={'contract':'SYSTEM4_RESEARCH_EVIDENCE_V1','sources':[{k:s[k] for k in ('source_id','source_title','source_url','retrieved_at','evidence','snapshot_sha256','source_kind')}]}
            research['sources'][0]['source_url']='https://example.org/alien-source'
            rp=base/'research-bad.json'; rp.write_bytes(canon(research))
            self.assertEqual(controller.main(['controller.py','research',str(workspace),str(rp)]),2)
            state=json.loads((workspace/'state.json').read_text(encoding='utf-8')); self.assertEqual(state['phase'],'RESEARCH_REQUIRED'); self.assertIsNone(state['research'])

    def test_05_third_article_uses_same_point0_root_door_and_is_index_bound(self):
        with tempfile.TemporaryDirectory(prefix='system4-index-pass-') as td:
            base=Path(td); p0,workspace,_=self.prepare_point0(base,batch=True)
            self.assertEqual(root_entry.main(['root_entry.py','start-point0',str(p0),str(workspace),'2']),0)
            state=json.loads((workspace/'state.json').read_text(encoding='utf-8'))
            supervisor_state=json.loads((workspace/'supervisor_state.json').read_text(encoding='utf-8'))
            dispatch=json.loads((workspace/'worker_dispatch.json').read_text(encoding='utf-8'))
            expected=json.loads((workspace/'bound_snapshot.json').read_text(encoding='utf-8'))['next_textmachine_metadata_batch']['items'][2]
            self.assertEqual(state['article'],expected); self.assertEqual(supervisor_state['article_index'],2); self.assertEqual(dispatch['worker_contract']['article_index'],2)

    def test_06_out_of_range_article_index_blocks_before_controller_state(self):
        with tempfile.TemporaryDirectory(prefix='system4-index-block-') as td:
            base=Path(td); p0,workspace,_=self.prepare_point0(base,batch=True)
            self.assertEqual(root_entry.main(['root_entry.py','start-point0',str(p0),str(workspace),'999']),2)
            self.assertFalse((workspace/'state.json').exists())

if __name__=='__main__': unittest.main(verbosity=2)
