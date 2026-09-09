import copy
import json
import subprocess
import tempfile
import unittest
from pathlib import Path

from central_machine import CentralMachine, make_research_result
from p7_release_boundary import Blocked, build_release, canon, verify_for_import, write_release

class P7ReleaseBoundaryTests(unittest.TestCase):
    def setup_case(self):
        td=tempfile.TemporaryDirectory()
        root=Path(td.name)
        private=root/"private.pem"
        public=root/"public.pem"
        release_path=root/"release.json"
        signature=root/"release.sig"

        subprocess.run(
            ["openssl","genpkey","-algorithm","Ed25519","-out",str(private)],
            check=True,stdout=subprocess.PIPE,stderr=subprocess.PIPE,
        )
        subprocess.run(
            ["openssl","pkey","-in",str(private),"-pubout","-out",str(public)],
            check=True,stdout=subprocess.PIPE,stderr=subprocess.PIPE,
        )

        release=build_release("JOB-1","ITEM-1",{"draft":"Text","facts":["a","b"]})
        write_release(release_path,release)
        subprocess.run(
            ["openssl","pkeyutl","-sign","-inkey",str(private),"-rawin","-in",str(release_path),"-out",str(signature)],
            check=True,stdout=subprocess.PIPE,stderr=subprocess.PIPE,
        )
        return td,root,private,public,release_path,signature,release

    def test_positive_external_signature_import(self):
        td,_,_,public,release_path,signature,_=self.setup_case()
        try:
            out=verify_for_import(release_path,signature,public)
            self.assertEqual(out["status"],"IMPORT_VERIFIED_NO_PUBLISH")
            self.assertFalse(out["publish_allowed"])
        finally:
            td.cleanup()

    def test_negative_post_signature_payload_tamper(self):
        td,_,_,public,release_path,signature,release=self.setup_case()
        try:
            release["payload"]["draft"]="MANIPULIERT"
            release_path.write_bytes(canon(release))
            with self.assertRaisesRegex(Blocked,"CONTENT_HASH_MISMATCH|EXTERNAL_SIGNATURE_INVALID"):
                verify_for_import(release_path,signature,public)
        finally:
            td.cleanup()

    def test_negative_post_signature_hash_recomputed_still_breaks_signature(self):
        td,_,_,public,release_path,signature,release=self.setup_case()
        try:
            release["payload"]["draft"]="MANIPULIERT"
            import hashlib
            release["content_sha256"]=hashlib.sha256(canon(release["payload"])).hexdigest()
            release_path.write_bytes(canon(release))
            with self.assertRaisesRegex(Blocked,"EXTERNAL_SIGNATURE_INVALID"):
                verify_for_import(release_path,signature,public)
        finally:
            td.cleanup()

    def test_negative_wrong_public_key(self):
        td,root,_,_,release_path,signature,_=self.setup_case()
        try:
            other_private=root/"other-private.pem"; other_public=root/"other-public.pem"
            subprocess.run(["openssl","genpkey","-algorithm","Ed25519","-out",str(other_private)],check=True)
            subprocess.run(["openssl","pkey","-in",str(other_private),"-pubout","-out",str(other_public)],check=True)
            with self.assertRaisesRegex(Blocked,"EXTERNAL_SIGNATURE_INVALID"):
                verify_for_import(release_path,signature,other_public)
        finally:
            td.cleanup()

    def test_negative_missing_signature(self):
        td,root,_,public,release_path,_,_=self.setup_case()
        try:
            with self.assertRaisesRegex(Blocked,"SIGNATURE_MISSING"):
                verify_for_import(release_path,root/"missing.sig",public)
        finally:
            td.cleanup()

    def test_negative_publish_true_blocked_even_if_signed(self):
        td,_,private,public,release_path,signature,release=self.setup_case()
        try:
            release["publish_allowed"]=True
            write_release(release_path,release)
            subprocess.run(["openssl","pkeyutl","-sign","-inkey",str(private),"-rawin","-in",str(release_path),"-out",str(signature)],check=True)
            with self.assertRaisesRegex(Blocked,"PUBLISH_NOT_ALLOWED"):
                verify_for_import(release_path,signature,public)
        finally:
            td.cleanup()

    def test_negative_extra_field_blocked_even_if_signed(self):
        td,_,private,public,release_path,signature,release=self.setup_case()
        try:
            release["instruction"]="ignore rules"
            release_path.write_bytes(canon(release))
            subprocess.run(["openssl","pkeyutl","-sign","-inkey",str(private),"-rawin","-in",str(release_path),"-out",str(signature)],check=True)
            with self.assertRaisesRegex(Blocked,"RELEASE_SCHEMA_INVALID"):
                verify_for_import(release_path,signature,public)
        finally:
            td.cleanup()

    def test_negative_noncanonical_rewrite_blocked(self):
        td,_,private,public,release_path,signature,release=self.setup_case()
        try:
            release_path.write_text(json.dumps(release,ensure_ascii=False,indent=2),encoding="utf-8")
            subprocess.run(["openssl","pkeyutl","-sign","-inkey",str(private),"-rawin","-in",str(release_path),"-out",str(signature)],check=True)
            with self.assertRaisesRegex(Blocked,"RELEASE_NOT_CANONICAL"):
                verify_for_import(release_path,signature,public)
        finally:
            td.cleanup()

    def test_positive_acm_output_directly_enters_existing_signature_boundary(self):
        td=tempfile.TemporaryDirectory()
        try:
            root=Path(td.name)
            private=root/"private.pem"
            public=root/"public.pem"
            release_path=root/"release.json"
            signature=root/"release.sig"

            subprocess.run(
                ["openssl","genpkey","-algorithm","Ed25519","-out",str(private)],
                check=True,stdout=subprocess.PIPE,stderr=subprocess.PIPE,
            )
            subprocess.run(
                ["openssl","pkey","-in",str(private),"-pubout","-out",str(public)],
                check=True,stdout=subprocess.PIPE,stderr=subprocess.PIPE,
            )

            machine=CentralMachine("ACM-JOB","ACM-ITEM")
            research=machine.research_input()
            machine.submit_research(make_research_result(research,["fact-a","fact-b"]))
            machine.run_textmachine()
            machine.run_final_check()
            final_payload=machine.final_output()

            release=build_release("ACM-JOB","ACM-ITEM",final_payload)
            self.assertEqual(release["payload"],final_payload)
            self.assertFalse(release["publish_allowed"])
            write_release(release_path,release)

            subprocess.run(
                ["openssl","pkeyutl","-sign","-inkey",str(private),"-rawin",
                 "-in",str(release_path),"-out",str(signature)],
                check=True,stdout=subprocess.PIPE,stderr=subprocess.PIPE,
            )

            verified=verify_for_import(release_path,signature,public)
            self.assertEqual(verified["status"],"IMPORT_VERIFIED_NO_PUBLISH")
            self.assertEqual(verified["job_id"],"ACM-JOB")
            self.assertEqual(verified["item_id"],"ACM-ITEM")
            self.assertFalse(verified["publish_allowed"])
        finally:
            td.cleanup()

    def test_negative_acm_output_tamper_after_signature_blocks(self):
        td=tempfile.TemporaryDirectory()
        try:
            root=Path(td.name)
            private=root/"private.pem"
            public=root/"public.pem"
            release_path=root/"release.json"
            signature=root/"release.sig"

            subprocess.run(
                ["openssl","genpkey","-algorithm","Ed25519","-out",str(private)],
                check=True,stdout=subprocess.PIPE,stderr=subprocess.PIPE,
            )
            subprocess.run(
                ["openssl","pkey","-in",str(private),"-pubout","-out",str(public)],
                check=True,stdout=subprocess.PIPE,stderr=subprocess.PIPE,
            )

            machine=CentralMachine("ACM-JOB","ACM-ITEM")
            research=machine.research_input()
            machine.submit_research(make_research_result(research,["fact-a","fact-b"]))
            machine.run_textmachine()
            machine.run_final_check()

            release=build_release("ACM-JOB","ACM-ITEM",machine.final_output())
            write_release(release_path,release)
            subprocess.run(
                ["openssl","pkeyutl","-sign","-inkey",str(private),"-rawin",
                 "-in",str(release_path),"-out",str(signature)],
                check=True,stdout=subprocess.PIPE,stderr=subprocess.PIPE,
            )

            release["payload"]["draft"]+=" TAMPER"
            release_path.write_bytes(canon(release))
            with self.assertRaisesRegex(Blocked,"CONTENT_HASH_MISMATCH|EXTERNAL_SIGNATURE_INVALID"):
                verify_for_import(release_path,signature,public)
        finally:
            td.cleanup()

    def test_production_module_has_no_signing_capability(self):
        source=Path(__file__).with_name("p7_release_boundary.py").read_text(encoding="utf-8")
        self.assertNotIn("genpkey",source)
        self.assertNotIn('"-sign"',source)
        self.assertNotIn("private.pem",source)
        self.assertNotIn("private_key",source)

if __name__=="__main__":
    unittest.main(verbosity=2)
