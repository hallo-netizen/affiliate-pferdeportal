import os
import shutil
import tempfile
import unittest
from pathlib import Path

from codex_worker_entry import build_codex_production_worker_pool

REQUEST = {'task': 'research', 'article': {'plan_slot': 'a' * 64}}


def write_worker(path: Path) -> None:
    path.write_text(
        "import json,sys\n"
        "for line in sys.stdin:\n"
        " env=json.loads(line)\n"
        " print(json.dumps({'contract':env['contract'],'session_id':env['session_id'],'result':{'content':'research-ok'}}),flush=True)\n",
        encoding='utf-8',
    )
    path.chmod(0o644)


@unittest.skipUnless(os.geteuid() == 0 and shutil.which('runuser') is not None, 'requires root + runuser')
class CodexWorkerEntryTests(unittest.TestCase):
    def test_positive_exact_codex_entry_builds_real_cross_uid_worker(self):
        with tempfile.TemporaryDirectory(prefix='s4a-codex-entry-') as td:
            root = Path(td)
            root.chmod(0o755)
            source = root / 'bundle'
            source.mkdir()
            write_worker(source / 'worker.py')
            pool = build_codex_production_worker_pool(source, 'worker.py', root, runtime_processes=1)
            try:
                self.assertTrue(pool.cross_uid_bound())
                self.assertTrue(pool._command[0].startswith('/usr/'))
                self.assertEqual(pool.request(REQUEST), {'content': 'research-ok'})
            finally:
                pool.close()

    def test_negative_codex_entry_exposes_no_cross_uid_switch(self):
        with tempfile.TemporaryDirectory(prefix='s4a-codex-entry-neg-') as td:
            root = Path(td)
            root.chmod(0o755)
            source = root / 'bundle'
            source.mkdir()
            write_worker(source / 'worker.py')
            with self.assertRaises(TypeError):
                build_codex_production_worker_pool(  # type: ignore[call-arg]
                    source, 'worker.py', root, runtime_processes=1, require_cross_uid=False
                )


if __name__ == '__main__':
    unittest.main(verbosity=2)
