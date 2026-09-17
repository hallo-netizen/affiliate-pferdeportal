from __future__ import annotations

import unittest
from pathlib import Path
from unittest import mock

import no_codex_test_repair


class NoCodexTestRepairTests(unittest.TestCase):
    def setUp(self):
        self.repo = Path('/tmp/test-repo')
        self.state = {'authoring_contract': {}}

    @staticmethod
    def _match(offset: int, target: str, replacement: str = 'fixed') -> dict:
        return {
            'offset': offset,
            'length': len(target),
            'message': 'test',
            'shortMessage': 'test',
            'rule': {'id': 'TEST_RULE', 'category': {'id': 'TEST'}},
            'context': {'text': target, 'offset': 0, 'length': len(target)},
            'replacements': [{'value': replacement}],
        }

    def test_repair_tries_other_occurrence_and_requires_strict_lt_progress(self):
        body = '<p>bad good bad</p>'
        checked = 'bad good bad\n'

        def fake_lt(_repo, text):
            # The right-hand literal replacement is intentionally ineffective:
            # it keeps the same LT finding count. Replacing the left occurrence
            # reduces the count, and the remaining finding then reduces to zero.
            if text == 'bad good bad\n':
                matches = [self._match(0, 'bad'), self._match(9, 'bad')]
            elif text == 'bad good fixed\n':
                matches = [self._match(0, 'bad'), self._match(9, 'fixed')]
            elif text == 'fixed good bad\n':
                matches = [self._match(11, 'bad')]
            elif text == 'fixed good fixed\n':
                matches = []
            else:
                raise AssertionError('unexpected LT text: ' + repr(text))
            return {'matches': matches}, '{}', 0

        with mock.patch.object(no_codex_test_repair.production_checks, '_run_languagetool_text', side_effect=fake_lt), \
             mock.patch.object(no_codex_test_repair.authoring_contract, 'validate_candidate', return_value=None):
            repaired = no_codex_test_repair._repair_from_exact_lt_text(
                self.repo, self.state, body, checked, 'LT_REPAIR', False
            )

        self.assertEqual(repaired, '<p>fixed good fixed</p>')

    def test_repair_blocks_when_text_changes_but_lt_finding_count_does_not_improve(self):
        body = '<p>bad</p>'
        checked = 'bad\n'

        def fake_lt(_repo, text):
            if text == 'bad\n':
                matches = [self._match(0, 'bad')]
            elif text == 'fixed\n':
                matches = [self._match(0, 'fixed', 'bad')]
            else:
                raise AssertionError('unexpected LT text: ' + repr(text))
            return {'matches': matches}, '{}', 0

        with mock.patch.object(no_codex_test_repair.production_checks, '_run_languagetool_text', side_effect=fake_lt), \
             mock.patch.object(no_codex_test_repair.authoring_contract, 'validate_candidate', return_value=None):
            with self.assertRaisesRegex(no_codex_test_repair.NoCodexRepairError, 'LT_REPAIR_NO_MONOTONIC_REPAIR'):
                no_codex_test_repair._repair_from_exact_lt_text(
                    self.repo, self.state, body, checked, 'LT_REPAIR', False
                )


if __name__ == '__main__':
    unittest.main(verbosity=2)
