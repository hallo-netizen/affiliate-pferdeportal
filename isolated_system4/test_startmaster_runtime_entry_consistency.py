from __future__ import annotations

import importlib.util
import unittest
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
GATE = REPO / 'control/output-quarantine/runtime_entry_gate.py'


def load_gate():
    spec = importlib.util.spec_from_file_location('system4_runtime_entry_consistency_gate', GATE)
    if spec is None or spec.loader is None:
        raise RuntimeError('RUNTIME_ENTRY_GATE_LOAD_FAILED')
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


class StartmasterRuntimeEntryConsistencyTest(unittest.TestCase):
    def test_authoritative_current_state_root_and_107007_bundle_are_consistent(self):
        gate = load_gate()
        pointer, state, execution_gate, policy = gate.authority()
        self.assertEqual(pointer['state_ref'], 'control/startmaster0107/CURRENT_STATE.json')
        self.assertEqual(state['next_allowed_step'], 'RUN_NEW_ARTICLE_BATCH_NO_STOP')
        self.assertEqual(execution_gate['step_id'], 'RUN_NEW_ARTICLE_BATCH_NO_STOP')
        self.assertEqual(execution_gate['sequence'], 107007)
        self.assertFalse(state['publish_allowed'])
        self.assertEqual(policy['visible_output_authority'], 'RELEASE_RECEIPT_ONLY')


if __name__ == '__main__':
    unittest.main()
