import json
import os
import shutil
import tempfile
import unittest
from pathlib import Path

from external_host import ExternalHostError, PersistentArticleWorkerPool

REQUEST={'task':'research','article':{'plan_slot':'b'*64}}


def write_worker_bundle(root: Path) -> None:
    (root/'payload.txt').write_text('bundle-research-ok',encoding='utf-8')
    (root/'worker.py').write_text(
        "import json,sys\nfrom pathlib import Path\n"
        "payload=Path(__file__).with_name('payload.txt').read_text(encoding='utf-8')\n"
        "for line in sys.stdin:\n"
        " env=json.loads(line)\n"
        " print(json.dumps({'contract':env['contract'],'session_id':env['session_id'],'result':{'content':payload}}),flush=True)\n",
        encoding='utf-8')


@unittest.skipUnless(os.geteuid()==0 and shutil.which('runuser') is not None,'requires root + runuser')
class WorkerBundleStagingTests(unittest.TestCase):
    def test_positive_private_source_bundle_is_supervisor_staged_and_runs_cross_uid(self):
        with tempfile.TemporaryDirectory(prefix='s4a-private-source-') as td:
            private=Path(td)  # 0700 root like Codex temp staging
            write_worker_bundle(private)
            with PersistentArticleWorkerPool.from_python_bundle(private,'worker.py',runtime_processes=1) as pool:
                self.assertEqual(pool.request(REQUEST),{'content':'bundle-research-ok'})
                staging=pool._owned_staging_root
                self.assertIsNotNone(staging)
                self.assertEqual((staging/'bundle'/'worker.py').stat().st_mode & 0o777,0o644)
                self.assertEqual((staging/'bundle').stat().st_mode & 0o777,0o755)
                self.assertEqual(len(pool.runtime_pids()),1)
            self.assertFalse(staging.exists())

    def test_negative_authority_file_in_bundle_is_rejected(self):
        with tempfile.TemporaryDirectory(prefix='s4a-private-source-') as td:
            private=Path(td); write_worker_bundle(private)
            (private/'state.json').write_text('{}',encoding='utf-8')
            with self.assertRaisesRegex(ExternalHostError,'WORKER_AUTHORITY_FILE_FORBIDDEN:state.json'):
                PersistentArticleWorkerPool.from_python_bundle(private,'worker.py')

    def test_negative_symlink_in_bundle_is_rejected(self):
        with tempfile.TemporaryDirectory(prefix='s4a-private-source-') as td:
            private=Path(td); write_worker_bundle(private)
            (private/'link').symlink_to('/etc/passwd')
            with self.assertRaisesRegex(ExternalHostError,'WORKER_BUNDLE_SYMLINK_FORBIDDEN:link'):
                PersistentArticleWorkerPool.from_python_bundle(private,'worker.py')

    def test_negative_missing_entrypoint_is_rejected_and_does_not_leave_worker(self):
        with tempfile.TemporaryDirectory(prefix='s4a-private-source-') as td:
            private=Path(td); write_worker_bundle(private)
            with self.assertRaisesRegex(ExternalHostError,'WORKER_BUNDLE_ENTRYPOINT_MISSING'):
                PersistentArticleWorkerPool.from_python_bundle(private,'missing.py')

if __name__=='__main__': unittest.main(verbosity=2)
