from __future__ import annotations
import hashlib, json, tempfile, unittest
from pathlib import Path
import slimline_controller as m

def dump(p:Path,o): p.parent.mkdir(parents=True,exist_ok=True); p.write_text(json.dumps(o,indent=2)+"\n",encoding="utf-8")
def sha(p:Path): return hashlib.sha256(p.read_bytes()).hexdigest()

class T(unittest.TestCase):
    def setUp(self):
        self.t=tempfile.TemporaryDirectory(); self.repo=Path(self.t.name); self.contract=self.repo/'PLAN_B_CONTRACT.json'; self.contract.write_text(Path(__file__).with_name('PLAN_B_CONTRACT.json').read_text(),encoding='utf-8')
        self.batch=self.repo/'batch.json'; self.state=self.repo/'state.json'; self.slot='a'*64; dump(self.batch,{"batch_sha256":'b'*64,"items":[{"canonical_article_id":"article:test","plan_slot":self.slot}]})
        self.s=m.init_state(self.repo,self.contract,self.batch,self.state,'.shadow')
    def tearDown(self): self.t.cleanup()
    def build_item_pass(self):
        root=self.repo/f'.shadow/items/{self.slot}'; root.mkdir(parents=True,exist_ok=True); rows=[]
        final=root/'ARTICLE.html'; final.write_text('<p>x</p>',encoding='utf-8'); final_sha=sha(final)
        report=root/'PPM_REPORT.json'; dump(report,{"ok":True,"technical_status":"TECHNICAL_CHECK_OK","content_quality_status":"CONTENT_QUALITY_CHECK_OK","content_hash":final_sha,"checks":{"content_hash":final_sha,"fail_closed_aggregate_status":"PASS"}})
        for stage in m.REQUIRED_STAGES:
            art=root/f'{stage}.artifact'; art.write_text(stage,encoding='utf-8')
            proof={"contract":m.STAGE_PROOF,"status":"PASS","batch_sha256":'b'*64,"canonical_article_id":"article:test","plan_slot":self.slot,"stage":stage,"execution_performed":True,"input_sha256":'1'*64,"execution_evidence":["executed"],"artifacts":[{"ref":art.relative_to(self.repo).as_posix(),"sha256":sha(art)}],"content_or_quality_rules_changed":False,"publish_allowed":False}
            if stage=='ppm': proof['ppm679_binding']={"ppm_version":"6.7.9","ppm_package_sha256":'2'*64,"article_type_templates_sha256":'3'*64,"final_article_ref":final.relative_to(self.repo).as_posix(),"final_article_sha256":final_sha,"ppm_report_ref":report.relative_to(self.repo).as_posix(),"ppm_report_sha256":sha(report)}
            pp=root/f'{stage}.json'; dump(pp,proof); rows.append({"stage":stage,"ref":pp.relative_to(self.repo).as_posix(),"sha256":sha(pp)})
        fp=root/'FACH_PASS.json'; dump(fp,{"contract":m.FACH_PASS,"status":"PASS","batch_sha256":'b'*64,"canonical_article_id":"article:test","plan_slot":self.slot,"required_stage_proofs":rows,"content_or_quality_rules_changed":False,"publish_allowed":False})
        out=root/'out.json'; dump(out,{"x":1})
        receipt={"contract":m.ITEM_RECEIPT,"ticket_id":m.ticket_body(self.s)['ticket_id'],"batch_sha256":'b'*64,"canonical_article_id":"article:test","plan_slot":self.slot,"status":"PASS","workflow_pass":True,"navigation_decision":False,"state_write_requested":False,"workflow_change_requested":False,"content_or_quality_rules_changed":False,"outputs":[{"ref":out.relative_to(self.repo).as_posix(),"sha256":sha(out)},{"ref":fp.relative_to(self.repo).as_posix(),"sha256":sha(fp)}],"evidence":["PASS"],"fachworkflow_pass_ref":fp.relative_to(self.repo).as_posix(),"fachworkflow_pass_sha256":sha(fp),"publish_allowed":False}
        rp=self.repo/'r.json'; dump(rp,receipt); return rp
    def test_pass_auto_advances(self):
        rp=self.build_item_pass(); out=m.submit(self.repo,self.contract,self.state,rp); self.assertEqual(out['next']['phase'],'FINAL_REVIEW'); self.assertTrue((self.repo/'.shadow/PREPARED_BATCH.json').is_file())
    def test_chat_navigation_blocked(self):
        rp=self.build_item_pass(); x=json.loads(rp.read_text()); x['navigation_decision']=True; dump(rp,x)
        with self.assertRaisesRegex(m.Blocked,'FORBIDDEN_AUTHORITY'): m.submit(self.repo,self.contract,self.state,rp)
    def test_stage_missing_blocks(self):
        rp=self.build_item_pass(); rec=json.loads(rp.read_text()); fp=self.repo/rec['fachworkflow_pass_ref']; x=json.loads(fp.read_text()); x['required_stage_proofs']=x['required_stage_proofs'][:-1]; dump(fp,x); rec['fachworkflow_pass_sha256']=sha(fp); rec['outputs'][1]['sha256']=sha(fp); dump(rp,rec)
        with self.assertRaisesRegex(m.Blocked,'STAGE_PROOF_COUNT_INVALID'): m.submit(self.repo,self.contract,self.state,rp)
    def test_unknown_quality_change_blocks(self):
        rp=self.build_item_pass(); rec=json.loads(rp.read_text()); rec['content_or_quality_rules_changed']=True; dump(rp,rec)
        with self.assertRaisesRegex(m.Blocked,'FORBIDDEN_AUTHORITY'): m.submit(self.repo,self.contract,self.state,rp)
    def test_ppm_hash_mismatch_blocks(self):
        rp=self.build_item_pass(); rec=json.loads(rp.read_text()); fp=self.repo/rec['fachworkflow_pass_ref']; f=json.loads(fp.read_text()); row=next(x for x in f['required_stage_proofs'] if x['stage']=='ppm'); pp=self.repo/row['ref']; p=json.loads(pp.read_text()); p['ppm679_binding']['final_article_sha256']='0'*64; dump(pp,p); row['sha256']=sha(pp); dump(fp,f); rec['fachworkflow_pass_sha256']=sha(fp); rec['outputs'][1]['sha256']=sha(fp); dump(rp,rec)
        with self.assertRaisesRegex(m.Blocked,'PPM_BOUND_FILE_HASH_MISMATCH'): m.submit(self.repo,self.contract,self.state,rp)

if __name__=='__main__': unittest.main()
