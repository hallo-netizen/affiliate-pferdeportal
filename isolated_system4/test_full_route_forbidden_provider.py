from __future__ import annotations
import unittest
from pathlib import Path

HERE=Path(__file__).resolve().parent
REPO=HERE.parent

EXECUTED_PATHS=[
    HERE/'full_route_start.py',
    HERE/'point0_snapshot.py',
    HERE/'root_entry.py',
    HERE/'root_supervisor_bridge.py',
    HERE/'supervisor.py',
    HERE/'worker_dispatch.py',
    HERE/'codex_entry.py',
    HERE/'controller.py',
    HERE/'controller_core.py',
    HERE/'production_binding.py',
    HERE/'authoring_contract.py',
    HERE/'content_guard.py',
    HERE/'design_guard.py',
    HERE/'production_checks.py',
    HERE/'batch_gate.py',
    HERE/'batch_repetition_guard.py',
    HERE/'handoff_transport.py',
    HERE/'full_route_test_fixture.py',
    HERE/'full_route_test_worker.py',
    REPO/'.github/workflows/system4-point0-supervisor-candidate.yml',
]

FORBIDDEN=('dataforseo','data_for_seo','source_acquisition.py','DATAFORSEO_')

class FullRouteForbiddenProviderTests(unittest.TestCase):
    def test_forbidden_provider_absent_from_entire_executed_route(self):
        for path in EXECUTED_PATHS:
            self.assertTrue(path.is_file(),f'MISSING_EXECUTED_PATH:{path}')
            text=path.read_text(encoding='utf-8')
            folded=text.casefold()
            for token in FORBIDDEN:
                self.assertNotIn(token.casefold(),folded,f'FORBIDDEN_PROVIDER_REFERENCE:{path}:{token}')

if __name__=='__main__':
    unittest.main(verbosity=2)
