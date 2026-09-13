import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SYSTEM4 = ROOT / 'isolated_system4'
ENTRY = SYSTEM4 / 'root_entry.py'
FIXTURE = SYSTEM4 / 'live_fixture' / 'wordpress_snapshot.json'


class RootEntryTests(unittest.TestCase):
    def run_entry(self, args, *, stdin=None):
        return subprocess.run(
            [sys.executable, str(ENTRY), *args],
            cwd=ROOT,
            input=stdin,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            check=False,
        )

    def test_root_agents_keeps_old_route_and_binds_system4_route(self):
        text=(ROOT/'AGENTS.md').read_text(encoding='utf-8')
        self.assertIn('SYSTEM4_ISOLATED_ROOT_ENTRY_V2', text)
        self.assertIn('python3 isolated_system4/root_entry.py start-stdin', text)
        self.assertIn('SYSTEM4 branch: DO NOT run control/cloud-entry-gate/cloud_entry.py before or instead of the System-4 root entry.', text)
        self.assertIn('python3 control/cloud-entry-gate/cloud_entry.py start', text)
        self.assertIn('python3 control/cloud-entry-gate/cloud_entry.py complete .pferde-capsule/RECEIPT.json', text)
        self.assertIn('python3 control/cloud-entry-gate/cloud_entry.py verify', text)

    def test_positive_file_entry_from_outside_repo(self):
        raw=FIXTURE.read_bytes()
        with tempfile.TemporaryDirectory(prefix='system4-root-file-') as td:
            td=Path(td); snapshot=td/'snapshot.json'; workspace=td/'workspace'
            snapshot.write_bytes(raw)
            cp=self.run_entry(['start', str(snapshot), str(workspace)])
            self.assertEqual(cp.returncode,0,cp.stdout.decode()+cp.stderr.decode())
            self.assertIn('SYSTEM4_ROOT_ENTRY_PASS:RESEARCH_REQUIRED',cp.stdout.decode())
            state=json.loads((workspace/'state.json').read_text(encoding='utf-8'))
            self.assertEqual(state['phase'],'RESEARCH_REQUIRED')

    def test_positive_stdin_entry_preserves_exact_snapshot_bytes(self):
        raw=FIXTURE.read_bytes()
        with tempfile.TemporaryDirectory(prefix='system4-root-stdin-') as td:
            workspace=Path(td)/'workspace'
            cp=self.run_entry(['start-stdin', str(workspace)], stdin=raw)
            self.assertEqual(cp.returncode,0,cp.stdout.decode()+cp.stderr.decode())
            self.assertIn('SYSTEM4_ROOT_ENTRY_PASS:RESEARCH_REQUIRED',cp.stdout.decode())
            self.assertEqual((workspace/'bound_snapshot.json').read_bytes(),raw)
            state=json.loads((workspace/'state.json').read_text(encoding='utf-8'))
            self.assertEqual(state['phase'],'RESEARCH_REQUIRED')

    def test_negative_repo_internal_snapshot_is_blocked(self):
        with tempfile.TemporaryDirectory(prefix='system4-root-out-') as td:
            cp=self.run_entry(['start', str(FIXTURE), str(Path(td)/'workspace')])
            self.assertEqual(cp.returncode,2)
            self.assertIn('ROOT_ENTRY_SNAPSHOT_MUST_BE_OUTSIDE_REPO',cp.stdout.decode())

    def test_negative_repo_internal_workspace_is_blocked(self):
        raw=FIXTURE.read_bytes()
        with tempfile.TemporaryDirectory(prefix='system4-root-source-') as td:
            snapshot=Path(td)/'snapshot.json'; snapshot.write_bytes(raw)
            cp=self.run_entry(['start', str(snapshot), str(SYSTEM4/'_forbidden_workspace')])
            self.assertEqual(cp.returncode,2)
            self.assertIn('ROOT_ENTRY_WORKSPACE_MUST_BE_OUTSIDE_REPO',cp.stdout.decode())

    def test_negative_invalid_stdin_is_blocked_without_state(self):
        with tempfile.TemporaryDirectory(prefix='system4-root-badstdin-') as td:
            workspace=Path(td)/'workspace'
            cp=self.run_entry(['start-stdin', str(workspace)], stdin=b'{not-json')
            self.assertEqual(cp.returncode,2)
            self.assertIn('ROOT_ENTRY_STDIN_SNAPSHOT_JSON_INVALID',cp.stdout.decode())
            self.assertFalse((workspace/'state.json').exists())


if __name__=='__main__':
    unittest.main(verbosity=2)
