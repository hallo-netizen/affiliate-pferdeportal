import copy
import hashlib
import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SYSTEM4 = ROOT / 'isolated_system4'
ENTRY = SYSTEM4 / 'root_entry.py'
LIVE = SYSTEM4 / 'LIVE_BOUND_INPUT_ONE_ARTICLE.json'
EXPECTED_SHA256 = '58efda5de85ca276829349cbbf6049cc9dca6e2ebbf3a50a94a87caca13e10fd'
EXPECTED_BYTES = 643
EXPECTED_MANIFEST = '3ca3a10c5d2ee37f3932a044b9be9e358bba738205c48fe91ad5c80d154cad7c'


def run_entry(raw: bytes, workspace: Path):
    return subprocess.run(
        [sys.executable, str(ENTRY), 'start-stdin', str(workspace)],
        cwd=ROOT,
        input=raw,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=False,
    )


def canonical(value: dict) -> bytes:
    return (json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(',', ':')) + '\n').encode('utf-8')


class ExactLiveBoundInputTests(unittest.TestCase):
    def setUp(self):
        self.raw = LIVE.read_bytes()
        self.value = json.loads(self.raw)

    def test_live_input_bytes_are_frozen_and_bound(self):
        self.assertEqual(len(self.raw), EXPECTED_BYTES)
        self.assertEqual(hashlib.sha256(self.raw).hexdigest(), EXPECTED_SHA256)
        self.assertEqual(self.value['system4_root_manifest_sha256'], EXPECTED_MANIFEST)
        item = self.value['next_textmachine_metadata_batch']['items'][0]
        self.assertEqual(self.value['next_textmachine_metadata_batch']['item_count'], 1)
        self.assertEqual(item['article_type'], 'Beratung')
        self.assertEqual(item['category'], 'putzbox-beratung')
        self.assertEqual(item['plan_slot'], '88043c35da332d4b2a500d1b61919721aefadf894bc923c841cc849a132c63b5')
        self.assertEqual(item['target_keyword'], 'Putzbox für Pferde')
        self.assertEqual(item['title'], 'Putzbox für Pferde richtig auswählen')
        self.assertFalse(self.value['next_textmachine_metadata_batch']['publish_allowed'])

    def test_positive_exact_live_bytes_reach_research_required_byte_identical(self):
        with tempfile.TemporaryDirectory(prefix='system4-exact-live-pos-') as td:
            workspace = Path(td) / 'runtime'
            cp = run_entry(self.raw, workspace)
            out = cp.stdout.decode(errors='replace') + cp.stderr.decode(errors='replace')
            self.assertEqual(cp.returncode, 0, out)
            self.assertIn('SYSTEM4_ROOT_ENTRY_PASS:RESEARCH_REQUIRED', out)
            self.assertEqual((workspace / 'bound_snapshot.json').read_bytes(), self.raw)
            state = json.loads((workspace / 'state.json').read_text(encoding='utf-8'))
            self.assertEqual(state['phase'], 'RESEARCH_REQUIRED')
            self.assertFalse(state['publish_allowed'])
            self.assertEqual(state['article']['title'], 'Putzbox für Pferde richtig auswählen')

    def test_negative_exact_live_copy_missing_manifest_blocks(self):
        value = copy.deepcopy(self.value); value.pop('system4_root_manifest_sha256')
        with tempfile.TemporaryDirectory(prefix='system4-exact-live-neg-') as td:
            cp = run_entry(canonical(value), Path(td) / 'runtime')
            self.assertEqual(cp.returncode, 2)
            self.assertIn('ROOT_ENTRY_MANIFEST_BINDING_MISSING', cp.stdout.decode())

    def test_negative_exact_live_copy_wrong_manifest_blocks(self):
        value = copy.deepcopy(self.value); value['system4_root_manifest_sha256'] = '0' * 64
        with tempfile.TemporaryDirectory(prefix='system4-exact-live-neg-') as td:
            cp = run_entry(canonical(value), Path(td) / 'runtime')
            self.assertEqual(cp.returncode, 2)
            self.assertIn('ROOT_ENTRY_MANIFEST_MISMATCH', cp.stdout.decode())

    def test_negative_exact_live_copy_publish_true_blocks(self):
        value = copy.deepcopy(self.value); value['next_textmachine_metadata_batch']['publish_allowed'] = True
        with tempfile.TemporaryDirectory(prefix='system4-exact-live-neg-') as td:
            cp = run_entry(canonical(value), Path(td) / 'runtime')
            self.assertEqual(cp.returncode, 2)
            self.assertIn('WORDPRESS_PUBLISH_AUTHORITY_FAIL', cp.stdout.decode())

    def test_negative_exact_live_corrupt_json_blocks(self):
        bad = self.raw[:-2] + b'X\n'
        with tempfile.TemporaryDirectory(prefix='system4-exact-live-neg-') as td:
            cp = run_entry(bad, Path(td) / 'runtime')
            self.assertEqual(cp.returncode, 2)
            self.assertIn('ROOT_ENTRY_STDIN_SNAPSHOT_JSON_INVALID', cp.stdout.decode())

    def test_negative_exact_live_bytes_repo_internal_workspace_blocks(self):
        workspace = SYSTEM4 / '_forbidden_exact_live_workspace'
        cp = run_entry(self.raw, workspace)
        self.assertEqual(cp.returncode, 2)
        self.assertIn('ROOT_ENTRY_WORKSPACE_MUST_BE_OUTSIDE_REPO', cp.stdout.decode())


if __name__ == '__main__':
    unittest.main(verbosity=2)
