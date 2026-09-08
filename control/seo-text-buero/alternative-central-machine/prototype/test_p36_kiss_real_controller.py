from __future__ import annotations

import json
import subprocess
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

import p36_kiss_real_controller as ctl
from p7_release_boundary import canon
from p10_batch_resume import JOB_CONTRACT, Blocked

class P36KissControllerTests(unittest.TestCase):
    def keypair(self,root:Path):
        priv=root/"private.pem"; pub=root/"public.pem"
        subprocess.run(["openssl","genpkey","-algorithm","Ed25519","-out",str(priv)],check=True,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
        subprocess.run(["openssl","pkey","-in",str(priv),"-pubout","-out",str(pub)],check=True,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
        return priv,pub

    def signed_job(self,root:Path,count:int=3):
        priv,pub=self.keypair(root)
        job={
            "contract":JOB_CONTRACT,
            "job_id":"P36-JOB",
            "items":[{"item_id":f"ITEM-{i}","input":{"source_ref":f"REF-{i}"}} for i in range(count)],
            "publish_allowed":False,
        }
        path=root/"job.json"; sig=root/"job.sig"
        path.write_bytes(canon(job))
        subprocess.run(["openssl","pkeyutl","-sign","-inkey",str(priv),"-rawin","-in",str(path),"-out",str(sig)],check=True,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
        return job,path,sig,pub

    def fake_pass(self,job_id="P36-JOB",item_id="ITEM-0"):
        return {
            "job_id":job_id,
            "item_id":item_id,
            "status":ctl.ITEM_PASS_STATUS,
            "prepare_no_write":True,
            "external_signature_verified":True,
            "exact_one_draft_written":True,
            "publish_count_unchanged":True,
            "post_signature_tamper_blocked":True,
            "post_signature_rehash_tamper_blocked":True,
            "planned_write_fingerprint":"a"*64,
            "release_content_sha256":"b"*64,
        }

    def test_positive_fixed_order_and_count(self):
        with tempfile.TemporaryDirectory() as td:
            root=Path(td)
            job,path,sig,pub=self.signed_job(root,7)
            calls=[]
            def fake(job_id,item_id):
                calls.append((job_id,item_id))
                return self.fake_pass(job_id,item_id)
            with patch.object(ctl,"_run_fixed_item",side_effect=fake):
                out=ctl.execute_signed_job(path,sig,pub)
            self.assertEqual(out["status"],"JOB_PASS_NO_PUBLISH")
            self.assertEqual(out["item_count"],7)
            self.assertEqual(out["completed_count"],7)
            self.assertEqual([x["item_id"] for x in out["items"]],[x["item_id"] for x in job["items"]])
            self.assertEqual(len(calls),7)
            self.assertEqual([item for _,item in calls],[x["item_id"] for x in job["items"]])
            self.assertFalse(out["publish_allowed"])

    def test_negative_tampered_job_blocks_before_worker(self):
        with tempfile.TemporaryDirectory() as td:
            root=Path(td)
            job,path,sig,pub=self.signed_job(root,2)
            job["items"][0]["input"]["source_ref"]="TAMPER"
            path.write_bytes(canon(job))
            with patch.object(ctl,"_run_fixed_item") as worker:
                with self.assertRaises(Blocked):
                    ctl.execute_signed_job(path,sig,pub)
                worker.assert_not_called()

    def test_negative_duplicate_item_blocks_before_worker(self):
        with tempfile.TemporaryDirectory() as td:
            root=Path(td)
            priv,pub=self.keypair(root)
            job={
                "contract":JOB_CONTRACT,
                "job_id":"P36-DUP",
                "items":[{"item_id":"X","input":{}},{"item_id":"X","input":{}}],
                "publish_allowed":False,
            }
            path=root/"job.json"; sig=root/"job.sig"
            path.write_bytes(canon(job))
            subprocess.run(["openssl","pkeyutl","-sign","-inkey",str(priv),"-rawin","-in",str(path),"-out",str(sig)],check=True,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
            with patch.object(ctl,"_run_fixed_item") as worker:
                with self.assertRaises(Blocked):
                    ctl.execute_signed_job(path,sig,pub)
                worker.assert_not_called()

    def test_negative_worker_failure_stops_immediately(self):
        with tempfile.TemporaryDirectory() as td:
            root=Path(td)
            _,path,sig,pub=self.signed_job(root,4)
            counter={"n":0}
            def fake(job_id,item_id):
                counter["n"]+=1
                if counter["n"]==2:
                    raise ctl.ControllerBlocked("TEST_FAILURE")
                return self.fake_pass(job_id,item_id)
            with patch.object(ctl,"_run_fixed_item",side_effect=fake):
                with self.assertRaisesRegex(ctl.ControllerBlocked,"TEST_FAILURE"):
                    ctl.execute_signed_job(path,sig,pub)
            self.assertEqual(counter["n"],2)

    def test_static_no_runtime_selection_api(self):
        text=Path(ctl.__file__).read_text(encoding="utf-8")
        forbidden=(
            "set_next_step",
            "choose_worker",
            "set_validator",
            "set_route",
            "set_engine",
            "alternative_route",
        )
        for token in forbidden:
            self.assertNotIn(token,text)
        self.assertIn('LAB_ITEM_ADAPTER=HERE/"p22_signed_normal_draft_integration.py"',text)

if __name__=="__main__":
    unittest.main(verbosity=2)
