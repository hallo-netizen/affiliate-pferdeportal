import json
import os
import subprocess
import tempfile
import unittest
from pathlib import Path

HERE = Path(__file__).resolve().parent
ENTRY = HERE / 'realcase_production_entry.py'


class RealcaseProductionEntryTests(unittest.TestCase):
    def _payload(self, category: str) -> dict:
        return {
            'contract': 'SYSTEM4_WORDPRESS_LIVE_INPUT_FIXTURE_V1',
            'next_textmachine_metadata_batch': {
                'contract': 'PSERC_TEXTMACHINE_METADATA_BATCH_V2',
                'status': 'READY_FOR_TEXTMACHINE_METADATA_INTAKE',
                'batch_sha256': 'b' * 64,
                'item_count': 1,
                'items': [{
                    'article_type': 'Beratung',
                    'category': category,
                    'plan_slot': 'a' * 64,
                    'target_keyword': 'Checklisten für Pferdeanhänger',
                    'title': 'Checklisten für Pferdeanhänger auswählen die wichtigsten Entscheidungskriterien',
                }],
                'publish_allowed': False,
            },
        }

    def _run(self, category: str, worker_body: str) -> subprocess.CompletedProcess[str]:
        with tempfile.TemporaryDirectory(prefix='s4a-real-entry-', dir='/tmp') as td:
            root = Path(td); root.chmod(0o755)
            source = root / 'worker-source'; source.mkdir(mode=0o700)
            (source / 'worker.py').write_text(worker_body, encoding='utf-8')
            inp = root / 'input.json'
            inp.write_text(json.dumps(self._payload(category), ensure_ascii=False, sort_keys=True, separators=(',', ':')), encoding='utf-8')
            env = dict(os.environ)
            env['PYTHONPATH'] = str(HERE) + ':' + str(HERE.parent / 'isolated_system4')
            return subprocess.run([
                'python3', str(ENTRY),
                '--external-input', str(inp),
                '--worker-source', str(source),
                '--worker-entrypoint', 'worker.py',
                '--runtime-parent', str(root),
                '--authority-root', str(root / 'authority'),
                '--output', str(root / 'out.json'),
                '--parent-chat-dir', str(root / 'parent'),
                '--timeout-seconds', '30',
            ], text=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, env=env, check=False)

    def test_negative_last_real_bad_category_blocks_before_worker(self):
        proc = self._run('pferdeanhaenger-beratung', "raise SystemExit('SHOULD_NOT_START')\n")
        self.assertNotEqual(proc.returncode, 0)
        self.assertIn('PPM679_CATEGORY_NOT_CANONICAL:pferdeanhaenger-beratung', proc.stderr)
        self.assertNotIn('SHOULD_NOT_START', proc.stderr)

    def test_positive_canonical_input_reaches_cross_uid_worker(self):
        proc = self._run(
            'checklisten-fuer-pferdeanhaenger-beratung',
            "import sys\nsys.stderr.write('CANONICAL_ENTRY_WORKER_REACHED\\n');sys.stderr.flush();raise SystemExit(17)\n",
        )
        self.assertNotEqual(proc.returncode, 0)
        self.assertIn('WORKER_EXITED_WITHOUT_RESPONSE:RC=17:STDERR=CANONICAL_ENTRY_WORKER_REACHED', proc.stderr)


if __name__ == '__main__':
    unittest.main(verbosity=2)
