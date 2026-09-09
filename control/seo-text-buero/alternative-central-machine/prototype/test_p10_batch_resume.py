import hashlib
import subprocess
import tempfile
import unittest
from pathlib import Path

from central_machine import CentralMachine
from p7_release_boundary import Blocked, build_release, canon, write_release
from p10_batch_resume import JOB_CONTRACT, next_incomplete_item

class P10BatchResumeTests(unittest.TestCase):
    def keypair(self,root):
        private=root/"private.pem"; public=root/"public.pem"
        subprocess.run(["openssl","genpkey","-algorithm","Ed25519","-out",str(private)],check=True)
        subprocess.run(["openssl","pkey","-in",str(private),"-pubout","-out",str(public)],check=True)
        return private,public

    def sign(self,private,data,sig):
        subprocess.run(["openssl","pkeyutl","-sign","-inkey",str(private),"-rawin","-in",str(data),"-out",str(sig)],check=True)

    def make_job(self,root,private,count=3):
        job={
            "contract":JOB_CONTRACT,
            "job_id":"JOB-R",
            "items":[{"item_id":f"ITEM-{i}","input":{"topic":f"T{i}"}} for i in range(count)],
            "publish_allowed":False,
        }
        path=root/"job.json"; sig=root/"job.sig"
        path.write_bytes(canon(job)); self.sign(private,path,sig)
        return job,path,sig

    def make_release(self,root,private,item_id,job_id="JOB-R"):
        release=build_release(job_id,item_id,{"draft":"done","facts":["x"]})
        path=root/f"{item_id}.json"; sig=root/f"{item_id}.sig"
        write_release(path,release); self.sign(private,path,sig)
        return path,sig

    def test_positive_resume_skips_only_valid_completed_items(self):
        with tempfile.TemporaryDirectory() as td:
            root=Path(td); releases=root/"releases"; releases.mkdir()
            private,public=self.keypair(root)
            _,job,sig=self.make_job(root,private,3)
            self.make_release(releases,private,"ITEM-0")
            nxt=next_incomplete_item(job,sig,public,releases)
            self.assertEqual(nxt["item_id"],"ITEM-1")
            self.assertEqual(nxt["resume_mode"],"RESTART_ITEM_FROM_BEGINNING")

    def test_positive_restarted_item_starts_at_first_step(self):
        with tempfile.TemporaryDirectory() as td:
            root=Path(td); releases=root/"releases"; releases.mkdir()
            private,public=self.keypair(root)
            _,job,sig=self.make_job(root,private,2)
            self.make_release(releases,private,"ITEM-0")
            nxt=next_incomplete_item(job,sig,public,releases)
            m=CentralMachine(nxt["job_id"],nxt["item_id"])
            self.assertEqual(m.current_step,"RESEARCH")

    def test_positive_all_complete_returns_none(self):
        with tempfile.TemporaryDirectory() as td:
            root=Path(td); releases=root/"releases"; releases.mkdir()
            private,public=self.keypair(root)
            _,job,sig=self.make_job(root,private,3)
            for i in range(3): self.make_release(releases,private,f"ITEM-{i}")
            self.assertIsNone(next_incomplete_item(job,sig,public,releases))

    def test_negative_tampered_job_manifest_blocks(self):
        with tempfile.TemporaryDirectory() as td:
            root=Path(td); releases=root/"releases"; releases.mkdir()
            private,public=self.keypair(root)
            job_obj,job,sig=self.make_job(root,private,2)
            job_obj["items"][0]["input"]["topic"]="tampered"
            job.write_bytes(canon(job_obj))
            with self.assertRaisesRegex(Blocked,"EXTERNAL_SIGNATURE_INVALID"):
                next_incomplete_item(job,sig,public,releases)

    def test_negative_duplicate_item_ids_block_even_if_signed(self):
        with tempfile.TemporaryDirectory() as td:
            root=Path(td); releases=root/"releases"; releases.mkdir()
            private,public=self.keypair(root)
            job={
                "contract":JOB_CONTRACT,"job_id":"JOB-R",
                "items":[{"item_id":"X","input":{}},{"item_id":"X","input":{}}],
                "publish_allowed":False,
            }
            path=root/"job.json"; sig=root/"job.sig"
            path.write_bytes(canon(job)); self.sign(private,path,sig)
            with self.assertRaisesRegex(Blocked,"JOB_ITEM_DUPLICATE"):
                next_incomplete_item(path,sig,public,releases)

    def test_negative_partial_final_release_blocks(self):
        with tempfile.TemporaryDirectory() as td:
            root=Path(td); releases=root/"releases"; releases.mkdir()
            private,public=self.keypair(root)
            _,job,sig=self.make_job(root,private,1)
            (releases/"ITEM-0.json").write_text("{}",encoding="utf-8")
            with self.assertRaisesRegex(Blocked,"PARTIAL_FINAL_RELEASE_PRESENT"):
                next_incomplete_item(job,sig,public,releases)

    def test_negative_tampered_completed_release_blocks(self):
        with tempfile.TemporaryDirectory() as td:
            root=Path(td); releases=root/"releases"; releases.mkdir()
            private,public=self.keypair(root)
            _,job,sig=self.make_job(root,private,2)
            path,_=self.make_release(releases,private,"ITEM-0")
            path.write_bytes(path.read_bytes()+b" ")
            with self.assertRaises(Blocked):
                next_incomplete_item(job,sig,public,releases)

    def test_negative_valid_signed_release_for_wrong_job_blocks(self):
        with tempfile.TemporaryDirectory() as td:
            root=Path(td); releases=root/"releases"; releases.mkdir()
            private,public=self.keypair(root)
            _,job,sig=self.make_job(root,private,2)
            self.make_release(releases,private,"ITEM-0",job_id="OTHER")
            with self.assertRaisesRegex(Blocked,"COMPLETED_RELEASE_JOB_MISMATCH"):
                next_incomplete_item(job,sig,public,releases)

    def test_positive_no_artificial_batch_limit_100(self):
        with tempfile.TemporaryDirectory() as td:
            root=Path(td); releases=root/"releases"; releases.mkdir()
            private,public=self.keypair(root)
            _,job,sig=self.make_job(root,private,100)
            nxt=next_incomplete_item(job,sig,public,releases)
            self.assertEqual(nxt["item_id"],"ITEM-0")

if __name__=="__main__":
    unittest.main(verbosity=2)
