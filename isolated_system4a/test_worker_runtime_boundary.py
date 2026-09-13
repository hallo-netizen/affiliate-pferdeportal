import os
import shutil
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

import external_host
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
    def worker_python(self) -> str:
        return external_host._resolve_worker_python('nobody')

    def test_negative_codex_like_private_temp_path_blocks_before_worker_start(self):
        with tempfile.TemporaryDirectory(prefix='s4a-neg-inaccessible-') as td:
            root = Path(td)  # tempfile default 0700, reproduces a private worker path
            worker = root / 'worker.py'
            write_worker(worker)
            pool = PersistentArticleWorkerPool(
                [self.worker_python(), str(worker)],
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

    def test_negative_private_interpreter_blocks_even_when_worker_is_accessible(self):
        with tempfile.TemporaryDirectory(prefix='s4a-private-python-') as private_td, tempfile.TemporaryDirectory(prefix='s4a-public-worker-') as public_td:
            private = Path(private_td)  # 0700: Codex-like /root/.pyenv parent condition
            fake_python = private / 'python3'
            fake_python.write_text('#!/bin/sh\nexec /usr/bin/python3 "$@"\n', encoding='utf-8')
            fake_python.chmod(0o700)
            public = Path(public_td)
            public.chmod(0o755)
            worker = public / 'worker.py'
            write_worker(worker)
            pool = PersistentArticleWorkerPool(
                [str(fake_python), str(worker)],
                public / 'workers',
                run_as_user='nobody',
                require_cross_uid=True,
                runtime_processes=1,
            )
            try:
                with self.assertRaisesRegex(ExternalHostError, 'WORKER_COMMAND_PATH_NOT_ACCESSIBLE:' + str(fake_python)):
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
                [self.worker_python(), str(worker)],
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

    def test_positive_worker_environment_does_not_inherit_supervisor_path(self):
        with tempfile.TemporaryDirectory(prefix='s4a-env-') as td:
            root = Path(td)
            root.chmod(0o755)
            with patch.dict(os.environ, {'PATH': '/root/.pyenv/versions/3.11.12/bin:/usr/bin:/bin'}):
                pool = PersistentArticleWorkerPool(
                    [self.worker_python(), '/dev/null'],
                    root / 'workers',
                    run_as_user='nobody',
                    require_cross_uid=True,
                    runtime_processes=1,
                )
                try:
                    workspace = pool._runtime_workspace(0)
                    self.assertEqual(pool._minimal_env(workspace)['PATH'], external_host.WORKER_PATH)
                    self.assertNotIn('/root', pool._minimal_env(workspace)['PATH'])
                    self.assertNotIn('pyenv', pool._minimal_env(workspace)['PATH'])
                finally:
                    pool.close()

    def test_negative_no_accessible_system_python_fails_closed(self):
        with tempfile.TemporaryDirectory(prefix='s4a-private-python-only-') as td:
            private = Path(td)
            fake_python = private / 'python3'
            fake_python.write_text('#!/bin/sh\nexit 0\n', encoding='utf-8')
            fake_python.chmod(0o700)
            with patch.object(external_host, 'WORKER_PATH', str(private)):
                with self.assertRaisesRegex(ExternalHostError, '^WORKER_PYTHON_RUNTIME_UNAVAILABLE$'):
                    external_host._resolve_worker_python('nobody')

    def test_negative_real_worker_crash_surfaces_exit_code_and_stderr(self):
        with tempfile.TemporaryDirectory(prefix='s4a-neg-stderr-') as td:
            root = Path(td)
            root.chmod(0o755)
            worker = root / 'worker.py'
            write_worker(worker, 'crash')
            pool = PersistentArticleWorkerPool(
                [self.worker_python(), str(worker)],
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
