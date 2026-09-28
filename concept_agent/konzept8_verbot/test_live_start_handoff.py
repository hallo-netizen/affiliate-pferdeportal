from __future__ import annotations
import copy, json, subprocess, sys, tempfile, unittest
from pathlib import Path

HERE=Path(__file__).resolve().parents[1]
if str(HERE) not in sys.path:
    sys.path.insert(0,str(HERE))

import intake_bridge
from concept_agent.konzept8_verbot import k8_command_gate, k8_entry

class K8LiveStartHandoffTests(unittest.TestCase):
    def setUp(self):
        self.snapshot=json.loads((HERE/"current"/"PSERC_METADATA_SNAPSHOT.json").read_text(encoding="utf-8"))
        self.intake=intake_bridge.prepare(self.snapshot)

    def test_live_receipt_is_k8_single_gate(self):
        receipt=intake_bridge._k8_live_start_receipt(self.snapshot,self.intake)
        self.assertEqual(receipt["status"],"CONCEPT_AGENT_INTAKE_READY")
        self.assertEqual(receipt["bound_worker"],"K8_VERBOT_SINGLE_GATE")
        self.assertNotEqual(receipt["bound_worker"],"BOUND_CHAT_WORKER")
        self.assertIs(receipt["publish_allowed"],False)
        trigger=receipt["process_trigger"]
        boot=receipt["k8_bootstrap"]
        self.assertEqual(trigger["checkpoint_sha256"],boot["checkpoint"]["checkpoint_sha256"])
        self.assertEqual(trigger["allowed_action"],boot["checkpoint"]["allowed_action"])
        self.assertEqual(trigger["required_command"],boot["required_command"])
        self.assertEqual(boot["required_command"]["command"],boot["checkpoint"]["allowed_action"])

    def test_wrong_command_is_inert_and_correct_command_reaches_existing_resume(self):
        receipt=intake_bridge._k8_live_start_receipt(self.snapshot,self.intake)
        boot=receipt["k8_bootstrap"]
        binding=boot["binding"]
        checkpoint=boot["checkpoint"]
        before=copy.deepcopy(checkpoint)

        wrong=copy.deepcopy(boot["required_command"])
        wrong["command"]={"action":"RUN_PSERC","item_count":binding["item_count"]}
        blocked=k8_entry.attempt(binding,checkpoint,wrong)
        self.assertEqual(blocked["status"],k8_command_gate.BLOCKED)
        self.assertEqual(checkpoint,before)
        self.assertEqual(blocked["checkpoint_sha256"],before["checkpoint_sha256"])
        self.assertEqual(blocked["allowed_action"],before["allowed_action"])
        self.assertIs(blocked["state_changed"],False)
        self.assertIsNone(blocked["execution"])

        ok=k8_entry.attempt(binding,checkpoint,boot["required_command"])
        self.assertEqual(ok["status"],k8_entry.EXECUTE)
        self.assertEqual(ok["checkpoint_sha256"],before["checkpoint_sha256"])
        self.assertEqual(ok["allowed_action"],before["allowed_action"])
        self.assertEqual(ok["execution"]["allowed_action"],before["allowed_action"])
        self.assertEqual(checkpoint,before)

    def test_exact_existing_cli_emits_k8_receipt(self):
        with tempfile.TemporaryDirectory() as td:
            out=Path(td)/"INTAKE.json"
            p=subprocess.run(
                [sys.executable,str(HERE/"intake_bridge.py"),"prepare",
                 str(HERE/"current"/"PSERC_METADATA_SNAPSHOT.json"),str(out)],
                check=True,capture_output=True,text=True,
            )
            receipt=json.loads(p.stdout)
            self.assertEqual(receipt["bound_worker"],"K8_VERBOT_SINGLE_GATE")
            self.assertEqual(receipt["process_trigger"]["required_command"]["command"],
                             receipt["process_trigger"]["allowed_action"])
            self.assertTrue(out.is_file())

if __name__=="__main__":
    unittest.main(verbosity=2)
