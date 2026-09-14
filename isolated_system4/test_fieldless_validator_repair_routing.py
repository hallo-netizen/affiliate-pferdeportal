from __future__ import annotations

import unittest

import controller
import production_checks
import repair_router


class FieldlessValidatorRepairRoutingTest(unittest.TestCase):
    def test_fieldless_ppm_validator_rejection_is_repairable(self):
        original = controller._ORIGINAL_RUN_ALL
        try:
            def fail(*args, **kwargs):
                raise production_checks.ProductionCheckError(
                    'PPM679_VALIDATOR_BLOCKED:BLOCKED_KNOWN_REGRESSION_PATTERN'
                )
            controller._ORIGINAL_RUN_ALL = fail
            with self.assertRaises(production_checks.RepairRequired) as ctx:
                controller._run_all_with_validator_routing(None, None, None, None)
            exc = ctx.exception
            self.assertEqual(exc.checker, 'ppm679')
            self.assertEqual(exc.findings[0]['error_code'], 'BLOCKED_KNOWN_REGRESSION_PATTERN')
            self.assertIsNone(exc.findings[0]['field_path'])
        finally:
            controller._ORIGINAL_RUN_ALL = original

    def test_fieldless_ppm_routes_to_body_owner(self):
        state = {
            'last_error': 'FULL:ppm679:BLOCKED_KNOWN_REGRESSION_PATTERN',
            'checks': {
                'findings': [{
                    'error_code': 'BLOCKED_KNOWN_REGRESSION_PATTERN',
                    'validator_id': 'PPM679_Content_Validator',
                }]
            },
        }
        route = repair_router.classify(state)
        self.assertEqual(route['owner'], 'DRAFT_BODY')
        self.assertEqual(route['target'], 'SAME_ARTICLE_BODY')

    def test_technical_ppm_failure_remains_terminal(self):
        original = controller._ORIGINAL_RUN_ALL
        try:
            def fail(*args, **kwargs):
                raise production_checks.ProductionCheckError(
                    'PPM679_VALIDATOR_EXECUTION_FAILED:PHP_CRASH'
                )
            controller._ORIGINAL_RUN_ALL = fail
            with self.assertRaises(production_checks.ProductionCheckError) as ctx:
                controller._run_all_with_validator_routing(None, None, None, None)
            self.assertIn('PPM679_VALIDATOR_EXECUTION_FAILED', str(ctx.exception))
        finally:
            controller._ORIGINAL_RUN_ALL = original

    def test_integrity_failure_remains_terminal(self):
        original = controller._ORIGINAL_RUN_ALL
        try:
            def fail(*args, **kwargs):
                raise production_checks.ProductionCheckError('PPM679_PACKAGE_HASH_MISMATCH')
            controller._ORIGINAL_RUN_ALL = fail
            with self.assertRaises(production_checks.ProductionCheckError):
                controller._run_all_with_validator_routing(None, None, None, None)
        finally:
            controller._ORIGINAL_RUN_ALL = original


if __name__ == '__main__':
    unittest.main()
