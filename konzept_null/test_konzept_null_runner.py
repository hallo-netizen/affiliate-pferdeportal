import json
import tempfile
import unittest
from pathlib import Path
from unittest import mock
import konzept_null_runner as r

class KonzeptNullIsolationTests(unittest.TestCase):
    def test_guard_passes_only_on_bound_branch(self):
        with mock.patch.object(r, 'branch_name', return_value=r.EXPECTED_BRANCH):
            policy, state, start = r.guard()
            self.assertFalse(policy['allow_wordpress_access'])
            self.assertFalse(policy['allow_wordpress_write'])
            self.assertFalse(policy['allow_publish'])
            self.assertFalse(policy['allow_external_write'])
            self.assertFalse(policy['allow_main_write'])
            self.assertEqual(state['terminal_boundary'], 'BEFORE_WORDPRESS')
            self.assertEqual(start['scope'], 'ISOLATED_TEST_ONLY')

    def test_wrong_branch_blocks(self):
        with mock.patch.object(r, 'branch_name', return_value='main'):
            with self.assertRaises(SystemExit): r.guard()

    def test_more_than_one_article_blocks(self):
        with tempfile.TemporaryDirectory() as td:
            p=Path(td)/'input.json'
            item={'title':'T','target_keyword':'K','category':'C','article_type':'Beratung','plan_slot':'S'}
            p.write_text(json.dumps([item,item]), encoding='utf-8')
            with mock.patch.object(r, 'branch_name', return_value=r.EXPECTED_BRANCH):
                with self.assertRaises(SystemExit): r.cmd_init(str(p))

    def test_missing_metadata_field_blocks(self):
        with tempfile.TemporaryDirectory() as td:
            p=Path(td)/'input.json'
            p.write_text(json.dumps({'title':'T'}), encoding='utf-8')
            with mock.patch.object(r, 'branch_name', return_value=r.EXPECTED_BRANCH):
                with self.assertRaises(SystemExit): r.cmd_init(str(p))

    def test_stage_order_blocks(self):
        with tempfile.TemporaryDirectory() as td:
            rs=Path(td)/'RUN_STATE.json'; art=Path(td)/'a.txt'
            rs.write_text(json.dumps({'completed':['METADATA']}), encoding='utf-8'); art.write_text('x')
            with mock.patch.object(r, 'branch_name', return_value=r.EXPECTED_BRANCH), mock.patch.object(r, 'ROOT', Path(td)):
                with self.assertRaises(SystemExit): r.cmd_stage(str(rs), 'PPM_6_7_9', str(art))

if __name__ == '__main__': unittest.main()
