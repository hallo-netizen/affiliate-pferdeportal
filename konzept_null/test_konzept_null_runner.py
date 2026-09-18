import io, json, tempfile, unittest
from contextlib import redirect_stdout
from pathlib import Path
from unittest import mock

import konzept_null_runner as r

class KonzeptNullIsolationTests(unittest.TestCase):
    def metadata(self, n):
        return {
            "items":[
                {
                    "title":f"T{i}",
                    "target_keyword":f"K{i}",
                    "category":"C",
                    "article_type":"Beratung",
                    "plan_slot":f"S{i}",
                }
                for i in range(n)
            ]
        }

    def init_in_temp(self,n):
        td=tempfile.TemporaryDirectory()
        root=Path(td.name)
        src=root/"input.json"
        src.write_text(json.dumps(self.metadata(n)),encoding="utf-8")
        p_branch=mock.patch.object(r,"branch_name",return_value=r.EXPECTED_BRANCH)
        p_root=mock.patch.object(r,"ROOT",root)
        p_work=mock.patch.object(r,"safe_workdir",side_effect=lambda rid,root=root: ((root/"work"/rid).mkdir(parents=True,exist_ok=True) or (root/"work"/rid)))
        with p_branch,p_root,p_work:
            r.cmd_init(str(src))
        state=next((root/"work").glob("*/RUN_STATE.json"))
        return td,root,state

    def test_guard_passes_only_on_bound_branch(self):
        with mock.patch.object(r,"branch_name",return_value=r.EXPECTED_BRANCH):
            r.guard()

    def test_wrong_branch_blocks(self):
        with self.assertRaises(SystemExit):
            with mock.patch.object(r,"branch_name",return_value="main"):
                r.guard()

    def test_zero_articles_blocks(self):
        with tempfile.TemporaryDirectory() as td:
            p=Path(td)/"input.json"; p.write_text(json.dumps({"items":[]}),encoding="utf-8")
            with self.assertRaises(SystemExit):
                with mock.patch.object(r,"branch_name",return_value=r.EXPECTED_BRANCH):
                    r.cmd_init(str(p))

    def test_missing_metadata_field_blocks(self):
        with tempfile.TemporaryDirectory() as td:
            p=Path(td)/"input.json"; p.write_text(json.dumps({"items":[{"title":"x"}]}),encoding="utf-8")
            with self.assertRaises(SystemExit):
                with mock.patch.object(r,"branch_name",return_value=r.EXPECTED_BRANCH):
                    r.cmd_init(str(p))

    def test_duplicate_plan_slot_blocks(self):
        x=self.metadata(2)
        x["items"][1]["plan_slot"]=x["items"][0]["plan_slot"]
        with tempfile.TemporaryDirectory() as td:
            p=Path(td)/"input.json"; p.write_text(json.dumps(x),encoding="utf-8")
            with self.assertRaises(SystemExit):
                with mock.patch.object(r,"branch_name",return_value=r.EXPECTED_BRANCH):
                    r.cmd_init(str(p))

    def test_one_article_allowed(self):
        td,root,state=self.init_in_temp(1); td.cleanup()

    def test_seven_articles_allowed(self):
        td,root,state=self.init_in_temp(7); td.cleanup()

    def test_twentyfive_articles_allowed(self):
        td,root,state=self.init_in_temp(25); td.cleanup()

    def test_initial_next_step_is_source_order(self):
        td,root,state=self.init_in_temp(1)
        rs=json.loads(state.read_text())
        self.assertEqual(rs["completed"],["METADATA"])
        self.assertEqual(rs["next_allowed_step"],"CREATE_SOURCE_ORDER")
        td.cleanup()

    def test_skip_stage_blocks(self):
        td,root,state=self.init_in_temp(1)
        art=root/"a"; art.write_text("x")
        with self.assertRaises(SystemExit):
            with mock.patch.object(r,"branch_name",return_value=r.EXPECTED_BRANCH), mock.patch.object(r,"ROOT",root):
                r.cmd_stage(str(state),"RESEARCH",str(art))
        td.cleanup()

    def test_full_stepwise_chain_and_terminal_boundary(self):
        td,root,state=self.init_in_temp(1)
        with mock.patch.object(r,"branch_name",return_value=r.EXPECTED_BRANCH), mock.patch.object(r,"ROOT",root):
            for stage in r.STAGES[1:]:
                rs=json.loads(state.read_text())
                self.assertEqual(rs["next_allowed_step"],r.NEXT[rs["completed"][-1]])
                art=root/f"{stage}.json"
                art.write_text(json.dumps({"stage":stage,"proof":"test"}),encoding="utf-8")
                r.cmd_stage(str(state),stage,str(art))
            rs=json.loads(state.read_text())
            self.assertEqual(rs["completed"],r.STAGES)
            self.assertEqual(rs["next_allowed_step"],"COMPLETE_BEFORE_WORDPRESS")
            r.cmd_finalize(str(state))
        pkg=next((root/"work").glob("*/KONZEPT_NULL_LOCAL_TEST_PACKAGE.json"))
        d=json.loads(pkg.read_text())
        self.assertEqual(d["terminal_boundary"],"BEFORE_WORDPRESS")
        self.assertFalse(d["publish_allowed"])
        self.assertFalse(d["wordpress_access_allowed"])
        td.cleanup()

    def test_next_reports_exactly_one_action(self):
        td,root,state=self.init_in_temp(1)
        buf=io.StringIO()
        with redirect_stdout(buf):
            with mock.patch.object(r,"branch_name",return_value=r.EXPECTED_BRANCH), mock.patch.object(r,"ROOT",root):
                r.cmd_next(str(state))
        out=json.loads(buf.getvalue())
        self.assertEqual(out["next_allowed_step"],"CREATE_SOURCE_ORDER")
        self.assertTrue(out["no_other_step_allowed"])
        td.cleanup()

if __name__=="__main__":
    unittest.main()
