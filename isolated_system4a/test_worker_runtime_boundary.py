import os
import shutil
import sys
import tempfile
import unittest
from pathlib import Path

from external_host import ExternalHostError, PersistentArticleWorkerPool

REQUEST = {
    'task': 'research',
    'article': {'plan_slot': 'a' * 64},
}


def write_worker(path: Path, mode: str = 'ok') -> None:
    if mode == 'ok':
        code = '''import json,sys\nfor line in sys.stdin:\n    env=json.loads(line)\n    print(json.dumps({'contract':env['contract'],'session_id':env['session_id'],'result':{'content':'research-ok'}}),flush=True)\n'''
    else:
        code = '''import sys\nsys.stderr.write('REALISTIC_WORKER_START_FAILURE\\n')\nsys.stderr.flush()\nraise SystemExit(17)\n'''
    path.write_text(code, encoding='utf-8')
    path.chmod(0o644)


@unittest.skipUnless(os.geteuid() == 0 and shutil.which('runuser') is not None, 'requires root + runuser')
class WorkerRuntimeBoundaryTests(unittest.TestCase):
    def test_negative_codex_like_private_temp_path_blocks_before_worker_start(self):
        with tempfile.TemporaryDirectory(prefix='s4a-neg-inaccessible-') as td:
            root = Path(td)  # tempfile default 0700, reproduces the failed Codex probe staging pattern
            worker = root / 'worker.py'
            write_worker(worker)
            pool = PersistentArticleWorkerPool(
                [sys.executable, str(worker)],
                root / 'workers',
                run_as_user='nobody',
                require_cross_uid=True,
                runtime_processes=1,
            )
            try:
                with self.assertRaisesRegex(ExternalHostError, 'WORKER_COMMAND_PATH_NOT_ACCESSIBLE:'):
                    pool.request(REQUEST)
                self.assertEqual(pool.runtime_pids(), [])
            finally:
                pool.close()

    def test_positive_cross_uid_worker_with_traversable_staging_path(self):
        with tempfile.TemporaryDirectory(prefix='s4a-pos-accessible-') as td:
            root = Path(td)
            root.chmod(0o755)
            worker = root / 'worker.py'
            write_worker(worker)
            pool = PersistentArticleWorkerPool(
                [sys.executable, str(worker)],
                root / 'workers',
                run_as_user='nobody',
                require_cross_uid=True,
                runtime_processes=1,
            )
            try:
                self.assertEqual(pool.request(REQUEST), {'content': 'research-ok'})
                self.assertEqual(len(pool.runtime_pids()), 1)
            finally:
                pool.close()

    def test_negative_real_worker_crash_surfaces_exit_code_and_stderr(self):
        with tempfile.TemporaryDirectory(prefix='s4a-neg-stderr-') as td:
            root = Path(td)
            root.chmod(0o755)
            worker = root / 'worker.py'
            write_worker(worker, 'crash')
            pool = PersistentArticleWorkerPool(
                [sys.executable, str(worker)],
                root / 'workers',
                run_as_user='nobody',
                require_cross_uid=True,
                runtime_processes=1,
            )
            try:
                with self.assertRaisesRegex(
                    ExternalHostError,
                    'WORKER_EXITED_WITHOUT_RESPONSE:RC=17:STDERR=REALISTIC_WORKER_START_FAILURE',
                ):
                    pool.request(REQUEST)
            finally:
                pool.close()


if __name__ == '__main__':
    unittest.main(verbosity=2)
