import os, unittest
from pathlib import Path
from central_machine import Blocked, CentralMachine, STEP_ORDER, make_research_result

class P2(unittest.TestCase):
    def good_research(self,m,facts=None):
        i=m.research_input()
        m.submit_research(make_research_result(i,facts or ["fact-a","fact-b"]))

    def full(self,m,facts=None):
        self.good_research(m,facts)
        m.run_textmachine()
        m.run_final_check()
        return m.final_output()

    def test_positive_fixed_three_stage_flow(self):
        m=CentralMachine("J","I")
        out=self.full(m)
        self.assertTrue(m.finished)
        self.assertEqual([x["step_id"] for x in m.snapshot()["history"]],list(STEP_ORDER))
        self.assertIn("Draft:",out["draft"])

    def test_negative_cannot_skip_research(self):
        m=CentralMachine("J","I")
        with self.assertRaisesRegex(Blocked,"STEP_ORDER_VIOLATION"):
            m.run_textmachine()

    def test_negative_no_external_validator_or_step_api(self):
        m=CentralMachine("J","I")
        self.assertFalse(hasattr(m,"submit"))
        self.assertFalse(hasattr(m,"set_validator"))
        self.assertFalse(hasattr(m,"set_next_step"))

    def test_negative_constructor_cannot_choose_engine(self):
        with self.assertRaises(TypeError):
            CentralMachine("J","I",textmachine_path="/tmp/evil")

    def test_negative_environment_cannot_choose_engine(self):
        old=os.environ.get("TEXTMACHINE_PATH")
        os.environ["TEXTMACHINE_PATH"]="/tmp/evil"
        try:
            m=CentralMachine("J","I")
            self.good_research(m)
            m.run_textmachine()
            self.assertEqual(m.current_step,"FINAL_CHECK")
        finally:
            if old is None:
                os.environ.pop("TEXTMACHINE_PATH",None)
            else:
                os.environ["TEXTMACHINE_PATH"]=old

    def test_negative_tampered_engine_hash_blocks(self):
        p=Path(__file__).with_name("frozen_textmachine_stub.py")
        original=p.read_bytes()
        try:
            p.write_bytes(original+b"\n#tamper\n")
            m=CentralMachine("J","I")
            self.good_research(m)
            with self.assertRaisesRegex(Blocked,"TEXTMACHINE_IDENTITY_MISMATCH"):
                m.run_textmachine()
        finally:
            p.write_bytes(original)

    def test_negative_worker_cannot_submit_draft(self):
        m=CentralMachine("J","I")
        i=m.research_input()
        r=make_research_result(i,["f"])
        r["output"]["draft"]="free draft"
        r["output_hash"]="0"*64
        with self.assertRaises(Blocked):
            m.submit_research(r)

    def test_negative_final_pass_cannot_be_self_asserted(self):
        m=CentralMachine("J","I")
        self.good_research(m)
        m.run_textmachine()
        self.assertFalse(hasattr(m,"submit_final_check"))

    def test_negative_fixed_rule_blocks_link_from_textmachine_output(self):
        m=CentralMachine("J","I")
        self.good_research(m,["https://example.org"])
        m.run_textmachine()
        with self.assertRaisesRegex(Blocked,"PROTOTYPE_LINK_RULE_BLOCKED"):
            m.run_final_check()

    def test_positive_theme_independent(self):
        for fact in ["Pferdedecke","Kaffeemühle","Photovoltaik","Steuerrecht"]:
            m=CentralMachine("J-"+fact,"I-"+fact)
            out=self.full(m,[fact])
            self.assertIn(fact,out["draft"])

    def test_positive_repeated_batch_25(self):
        for n in range(25):
            m=CentralMachine(f"J{n}",f"I{n}")
            self.full(m,[f"fact-{n}"])
            self.assertTrue(m.finished)

    def test_negative_wrong_order_after_research(self):
        m=CentralMachine("J","I")
        self.good_research(m)
        with self.assertRaisesRegex(Blocked,"STEP_ORDER_VIOLATION"):
            m.run_final_check()

if __name__=="__main__":
    unittest.main(verbosity=2)
