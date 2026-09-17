import json
import tempfile
import unittest
from pathlib import Path
from unittest import mock
import konzept_null_runner as r

class KonzeptNullIsolationTests(unittest.TestCase):
    def item(self, i):
        return {'title':f'T{i}','target_keyword':f'K{i}','category':'C','article_type':'Beratung','plan_slot':f'S{i}'}

    def test_guard_passes_only_on_bound_branch(self):
        with mock.patch.object(r, 'branch_name', return_value=r.EXPECTED_BRANCH):
            policy, state, start = r.guard()
            self.assertFalse(policy['allow_wordpress_access'])
            self.assertFalse(policy['allow_wordpress_write'])
            self.assertFalse(policy['allow_publish'])
            self.assertFalse(policy['allow_external_write'])
            self.assertFalse(policy['allow_main_write'])
            self.assertEqual(state['terminal_boundary'], 'BEFORE_WORDPRESS')
            self.assertEqual(state['batch_mode'], 'VARIABLE_1_TO_N')
            self.assertEqual(start['batch_mode'], 'VARIABLE_1_TO_N')

    def test_wrong_branch_blocks(self):
        with mock.patch.object(r, 'branch_name', return_value='main'):
            with self.assertRaises(SystemExit):
                r.guard()

    def test_zero_articles_blocks(self):
        with tempfile.TemporaryDirectory() as td:
            p = Path(td)/'input.json'
            p.write_text(json.dumps({'items':[]}), encoding='utf-8')
            with mock.patch.object(r, 'branch_name', return_value=r.EXPECTED_BRANCH):
                with self.assertRaises(SystemExit):
                    r.cmd_init(str(p))

    def test_one_article_allowed(self):
        self._assert_batch_allowed(1)

    def test_seven_articles_allowed(self):
        self._assert_batch_allowed(7)

    def test_twentyfive_articles_allowed(self):
        self._assert_batch_allowed(25)

    def _assert_batch_allowed(self, count):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            p = root/'input.json'
            p.write_text(json.dumps({'items':[self.item(i) for i in range(count)]}), encoding='utf-8')
            with mock.patch.object(r, 'branch_name', return_value=r.EXPECTED_BRANCH), mock.patch.object(r, 'ROOT', root):
                with mock.patch.object(r, 'safe_workdir', side_effect=lambda rid: self._mkwork(root, rid)):
                    r.cmd_init(str(p))
            states=list((root/'work').glob('*/RUN_STATE.json'))
            self.assertEqual(len(states),1)
            data=json.loads(states[0].read_text())
            self.assertEqual(data['article_count'],count)

    def _mkwork(self, root, rid):
        p=root/'work'/rid
        p.mkdir(parents=True, exist_ok=True)
        return p

    def test_duplicate_plan_slot_blocks(self):
        with tempfile.TemporaryDirectory() as td:
            p = Path(td)/'input.json'
            items=[self.item(i) for i in range(2)]
            items[1]['plan_slot']=items[0]['plan_slot']
            p.write_text(json.dumps({'items':items}), encoding='utf-8')
            with mock.patch.object(r, 'branch_name', return_value=r.EXPECTED_BRANCH):
                with self.assertRaises(SystemExit):
                    r.cmd_init(str(p))

    def test_missing_metadata_field_blocks(self):
        with tempfile.TemporaryDirectory() as td:
            p = Path(td)/'input.json'
            item=self.item(1); del item['target_keyword']
            p.write_text(json.dumps({'items':[item]}), encoding='utf-8')
            with mock.patch.object(r, 'branch_name', return_value=r.EXPECTED_BRANCH):
                with self.assertRaises(SystemExit):
                    r.cmd_init(str(p))

if __name__ == '__main__':
    unittest.main()
