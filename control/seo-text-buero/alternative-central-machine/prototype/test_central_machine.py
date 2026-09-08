import copy
import unittest
from cryptography.exceptions import InvalidSignature
from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PrivateKey
from central_machine import CentralMachine, Blocked, make_result, sha, canon

class CentralMachineTests(unittest.TestCase):
    def build(self):
        return CentralMachine("JOB-1", {"value": 1}, ["S1","S2","S3"])

    def test_positive_full_fixed_sequence(self):
        m=self.build()
        for expected in (2,4,8):
            wi=m.worker_input()
            m.submit(make_result(wi, {"value": expected}), lambda x: set(x)=={"value"} and isinstance(x["value"], int))
        self.assertTrue(m.finished)
        pkg=m.final_package()
        self.assertEqual(pkg["package_hash"], sha(pkg["body"]))

    def test_negative_worker_cannot_choose_next_step(self):
        m=self.build(); wi=m.worker_input(); r=make_result(wi, {"value":2}); r["step_id"]="S3"
        with self.assertRaisesRegex(Blocked,"STEP_ID_MISMATCH"): m.submit(r, lambda x: True)

    def test_negative_injected_next_step_field_rejected(self):
        m=self.build(); wi=m.worker_input(); r=make_result(wi, {"value":2}); r["next_step"]="S3"
        with self.assertRaisesRegex(Blocked,"RESULT_SCHEMA_INVALID"): m.submit(r, lambda x: True)

    def test_negative_wrong_job_rejected(self):
        m=self.build(); wi=m.worker_input(); r=make_result(wi, {"value":2}); r["job_id"]="OTHER"
        with self.assertRaisesRegex(Blocked,"JOB_ID_MISMATCH"): m.submit(r, lambda x: True)

    def test_negative_input_context_forgery_rejected(self):
        m=self.build(); wi=m.worker_input(); r=make_result(wi, {"value":2}); r["input_hash"]="0"*64
        with self.assertRaisesRegex(Blocked,"INPUT_HASH_MISMATCH"): m.submit(r, lambda x: True)

    def test_negative_output_modified_after_worker_rejected(self):
        m=self.build(); wi=m.worker_input(); r=make_result(wi, {"value":2}); r["output"]["value"]=999
        with self.assertRaisesRegex(Blocked,"OUTPUT_HASH_MISMATCH"): m.submit(r, lambda x: True)

    def test_negative_worker_fail_cannot_be_accepted(self):
        m=self.build(); wi=m.worker_input(); r=make_result(wi, {"value":2}, status="FAIL")
        with self.assertRaisesRegex(Blocked,"WORKER_NONPASS"): m.submit(r, lambda x: True)

    def test_negative_validator_fail_blocks(self):
        m=self.build(); wi=m.worker_input(); r=make_result(wi, {"value":2})
        with self.assertRaisesRegex(Blocked,"VALIDATOR_FAIL"): m.submit(r, lambda x: False)

    def test_positive_restart_resumes_exact_next_step(self):
        m=self.build(); wi=m.worker_input(); m.submit(make_result(wi, {"value":2}), lambda x: True)
        r=CentralMachine.restore(m.checkpoint())
        self.assertEqual(r.current_step,"S2")
        self.assertEqual(r.worker_input()["payload"],{"value":2})

    def test_negative_checkpoint_reorder_rejected(self):
        m=self.build(); wi=m.worker_input(); m.submit(make_result(wi, {"value":2}), lambda x: True)
        cp=m.checkpoint(); cp["history"][0]["step_id"]="S3"
        with self.assertRaisesRegex(Blocked,"CHECKPOINT_STEP_ORDER_INVALID"): CentralMachine.restore(cp)

    def test_worker_mutation_of_copy_does_not_mutate_machine(self):
        m=self.build(); wi=m.worker_input(); wi["payload"]["value"]=999
        self.assertEqual(m.worker_input()["payload"],{"value":1})

    def test_negative_final_package_tamper_detectable(self):
        m=self.build()
        for expected in (2,4,8):
            wi=m.worker_input(); m.submit(make_result(wi, {"value":expected}), lambda x: True)
        pkg=m.final_package(); tampered=copy.deepcopy(pkg); tampered["body"]["final_payload"]["value"]=999
        self.assertNotEqual(tampered["package_hash"],sha(tampered["body"]))

    def test_positive_external_signature_verifies_exact_package(self):
        m=CentralMachine("JOB-1",{"value":1},["S1"])
        wi=m.worker_input(); m.submit(make_result(wi,{"value":2}),lambda x: True)
        pkg=m.final_package(); private=Ed25519PrivateKey.generate(); public=private.public_key()
        signed=canon(pkg); sig=private.sign(signed); public.verify(sig,signed)

    def test_negative_post_output_tampering_breaks_signature(self):
        m=CentralMachine("JOB-1",{"value":1},["S1"])
        wi=m.worker_input(); m.submit(make_result(wi,{"value":2}),lambda x: True)
        pkg=m.final_package(); private=Ed25519PrivateKey.generate(); public=private.public_key()
        sig=private.sign(canon(pkg)); tampered=copy.deepcopy(pkg); tampered["body"]["final_payload"]["value"]=999
        with self.assertRaises(InvalidSignature): public.verify(sig, canon(tampered))

if __name__=="__main__":
    unittest.main(verbosity=2)
