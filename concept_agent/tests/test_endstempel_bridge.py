import hashlib,json,sys,tempfile,unittest
from pathlib import Path
OFFICE=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(OFFICE))
import endstempel_bridge as bridge

def canon(o): return json.dumps(o,ensure_ascii=False,sort_keys=True,separators=(",",":")).encode("utf-8")
def h(b): return hashlib.sha256(b).hexdigest()

class EndstempelBridgeTest(unittest.TestCase):
    def fixture(self,root):
        slot="1"*64; batch="2"*64; cid="article:test"; body="<p>test</p>"
        env={
          "contract":"PSERC_APPROVED_PRODUCTION_PACKAGE_V1",
          "package_id":"x","package_payload_sha256":"x","source":"TEST",
          "fact_pack_bundle":{},"fact_pack_bundle_sha256":h(canon({})),
          "production_plan":{"items":[{"canonical_article_id":cid,"canonical_article":{"body_html":body}}]},
          "production_plan_sha256":"x",
          "workflow_release":{"contract":"WORKFLOW_SUPERVISOR_RELEASE_V2_SIGNED","status":"PASS","wordpress_write_performed":False,"exact_five_batch_sha256":batch,"items":[{"plan_slot":slot,"canonical_article_id":cid}]},
          "workflow_release_sha256":"x"
        }
        req={"contract":bridge.REQ_CONTRACT,"batch_sha256":batch,"runtime_generation":1,"import_envelope":env,"articles":[{"plan_slot":slot,"content_utf8":body}],"publish_allowed":False,"content_mutation_performed":False}
        p=root/"concept_agent/production_ready/run.json";p.parent.mkdir(parents=True);p.write_text(json.dumps(req),encoding="utf-8")
        return p,slot,batch

    def test_builds_exact_source_and_manifest(self):
        with tempfile.TemporaryDirectory() as td:
            root=Path(td); old=bridge.REPO; bridge.REPO=root
            try:
                p,slot,batch=self.fixture(root)
                ref=bridge.build(str(p.relative_to(root)))
                self.assertEqual(ref,f"control/startmaster0107/recovery_sources/{batch}/generation-000001/MANIFEST.json")
                m=json.loads((root/ref).read_text())
                self.assertEqual(m["item_count"],1)
                self.assertFalse(m["publish_allowed"])
                self.assertTrue((root/m["items"][0]["ref"]).is_file())
                self.assertTrue((root/m["import_envelope_ref"]).is_file())
            finally: bridge.REPO=old

    def test_article_mismatch_blocks_fail_closed(self):
        with tempfile.TemporaryDirectory() as td:
            root=Path(td); old=bridge.REPO; bridge.REPO=root
            try:
                p,_,_=self.fixture(root)
                req=json.loads(p.read_text()); req["articles"][0]["content_utf8"]="tampered"; p.write_text(json.dumps(req))
                with self.assertRaisesRegex(bridge.Blocked,"IMPORT_ENVELOPE_ARTICLE_MISMATCH"):
                    bridge.build(str(p.relative_to(root)))
            finally: bridge.REPO=old

if __name__=="__main__": unittest.main()
