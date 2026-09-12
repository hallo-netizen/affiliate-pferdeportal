import copy
import hashlib
import unittest
from pathlib import Path
from unittest import mock

import production_checks


def sha(value: str) -> str:
    return hashlib.sha256(value.encode('utf-8')).hexdigest()


def bound_item():
    return {
        'article_type': 'Beratung',
        'target_keyword': 'Testkeyword',
        'topic': 'Testtitel',
        'canonical_article_id': 'article:test',
        'plan_item_key': 'test-key',
        'canonical_article': {
            'title': 'Testtitel',
            'body_html': '<p>ALT</p>',
            'body_html_sha256': sha('<p>ALT</p>'),
            'body_text': 'ALT',
        },
        'quality_binding': {
            'contract': 'content_structure_language_binding_v2',
            'language_review_status': 'LANGUAGETOOL_EVIDENCE_BOUND',
            'language_evidence': {
                'checked_text': 'ALT',
                'checked_text_sha256': sha('ALT'),
                'content_hash': sha('<p>ALT</p>'),
                'engine': production_checks.LT_ENGINE,
                'execution_record': {'input_sha256': sha('ALT'), 'raw_stdout_sha256': 'old', 'return_code': 0},
                'raw_finding_count': 0,
                'raw_report_json': '{"matches":[]}',
                'raw_report_sha256': sha('{"matches":[]}'),
                'return_code': 0,
                'unresolved_finding_count': 0,
            },
        },
    }


class DraftBoundRebindTests(unittest.TestCase):
    def test_rebind_updates_every_draft_bound_hash_without_mutating_bound_input(self):
        item = bound_item()
        item['quality_binding_hash'] = production_checks._canonical_sha(item['quality_binding'])
        original = copy.deepcopy(item)
        body = '<p>NEUER geprüfter Text</p>'
        checked = 'NEUER geprüfter Text'
        lt = {
            'status': 'PASS',
            'engine': production_checks.LT_ENGINE,
            'finding_count': 0,
            'checked_text': checked,
            'checked_text_sha256': sha(checked),
            'raw_report_json': '{"matches":[]}',
            'raw_report_sha256': sha('{"matches":[]}'),
            'return_code': 0,
        }
        rebound = production_checks._rebind_plan_to_checked_draft(item, body, lt)
        self.assertEqual(item, original)
        self.assertEqual(rebound['canonical_article']['body_html'], body)
        self.assertEqual(rebound['canonical_article']['body_html_sha256'], sha(body))
        self.assertEqual(rebound['canonical_article']['body_text'], checked)
        ev = rebound['quality_binding']['language_evidence']
        self.assertEqual(ev['checked_text'], checked)
        self.assertEqual(ev['checked_text_sha256'], sha(checked))
        self.assertEqual(ev['content_hash'], sha(body))
        self.assertEqual(ev['execution_record']['input_sha256'], sha(checked))
        self.assertEqual(ev['raw_finding_count'], 0)
        self.assertEqual(ev['unresolved_finding_count'], 0)
        self.assertEqual(rebound['quality_binding_hash'], production_checks._canonical_sha(rebound['quality_binding']))
        for key in ('article_type', 'target_keyword', 'topic', 'canonical_article_id', 'plan_item_key'):
            self.assertEqual(rebound[key], original[key])

    def test_run_all_runs_lt_once_and_passes_exact_pass_evidence_to_ppm(self):
        body = '<p>Sauberer Text</p>'
        state = {'draft_markdown': body, 'draft_sha256': sha(body)}
        lt = {'status': 'PASS', 'finding_count': 0, 'checked_text': 'Sauberer Text', 'checked_text_sha256': sha('Sauberer Text'), 'raw_report_json': '{"matches":[]}', 'raw_report_sha256': sha('{"matches":[]}'), 'return_code': 0}
        ppm = {'status': 'PASS'}
        with mock.patch.object(production_checks, 'validate_bound_context'), \
             mock.patch.object(production_checks, 'no_legacy_runtime_dependencies', return_value={'status': 'PASS'}), \
             mock.patch.object(production_checks, 'no_external_links', return_value={'status': 'PASS'}), \
             mock.patch.object(production_checks, 'run_languagetool', return_value=lt) as run_lt, \
             mock.patch.object(production_checks, 'run_ppm_content_validator', return_value=ppm) as run_ppm:
            result = production_checks.run_all(Path('.'), state, {}, bound_item())
        self.assertEqual(result['status'], 'PASS')
        self.assertEqual(run_lt.call_count, 1)
        self.assertEqual(run_ppm.call_count, 1)
        self.assertIs(run_ppm.call_args.args[4], lt)

    def test_repairable_lt_finding_short_circuits_ppm(self):
        body = '<p>Fehler</p>'
        state = {'draft_markdown': body, 'draft_sha256': sha(body)}
        repair = production_checks.RepairRequired('languagetool', [{'error_code': 'LANGUAGETOOL_FINDING'}])
        with mock.patch.object(production_checks, 'validate_bound_context'), \
             mock.patch.object(production_checks, 'no_legacy_runtime_dependencies', return_value={'status': 'PASS'}), \
             mock.patch.object(production_checks, 'no_external_links', return_value={'status': 'PASS'}), \
             mock.patch.object(production_checks, 'run_languagetool', side_effect=repair), \
             mock.patch.object(production_checks, 'run_ppm_content_validator') as run_ppm:
            with self.assertRaises(production_checks.RepairRequired):
                production_checks.run_all(Path('.'), state, {}, bound_item())
        run_ppm.assert_not_called()


if __name__ == '__main__':
    unittest.main(verbosity=2)
