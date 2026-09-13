import json
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

SOURCE_ROOT = Path(__file__).resolve().parent.parent


def run(argv, *, cwd, stdin=None, check=True):
    cp=subprocess.run(argv,cwd=cwd,input=stdin,stdout=subprocess.PIPE,stderr=subprocess.PIPE,check=False)
    if check and cp.returncode:
        raise AssertionError(cp.stdout.decode(errors='replace')+cp.stderr.decode(errors='replace'))
    return cp


def make_clean_repo(*, branch='system4-sandbox', detached=False, extra_noncritical_commit=False):
    td=tempfile.TemporaryDirectory(prefix='system4-root-repo-')
    repo=Path(td.name)/'repo'
    def ignore(path,names):
        ignored={'.git','__pycache__'}
        return [n for n in names if n in ignored or n.endswith('.pyc')]
    shutil.copytree(SOURCE_ROOT,repo,ignore=ignore)
    run(['git','init','-q'],cwd=repo)
    run(['git','config','user.email','system4@test.invalid'],cwd=repo)
    run(['git','config','user.name','System4 Test'],cwd=repo)
    run(['git','add','.'],cwd=repo)
    run(['git','commit','-qm','system4 test snapshot'],cwd=repo)
    run(['git','branch','-M',branch],cwd=repo)
    if extra_noncritical_commit:
        marker=repo/'isolated_system4'/'_noncritical_checkout_marker.txt'
        marker.write_text('noncritical commit identity test\n',encoding='utf-8')
        run(['git','add',str(marker.relative_to(repo))],cwd=repo)
        run(['git','commit','-qm','noncritical commit'],cwd=repo)
    if detached:
        run(['git','checkout','--detach','-q'],cwd=repo)
    return td,repo


def manifest(repo:Path)->str:
    cp=run([sys.executable,'-c',"import sys;sys.path.insert(0,'isolated_system4');import root_entry;print(root_entry._critical_manifest_sha256())"],cwd=repo)
    return cp.stdout.decode().strip()


def bound_snapshot(repo:Path, *, manifest_value=None, include_manifest=True)->bytes:
    raw=json.loads((repo/'isolated_system4'/'live_fixture'/'wordpress_snapshot.json').read_text(encoding='utf-8'))
    if include_manifest:
        raw['system4_root_manifest_sha256']=manifest_value or manifest(repo)
    return json.dumps(raw,ensure_ascii=False,sort_keys=True,separators=(',',':')).encode('utf-8')


def run_entry(repo:Path,args,*,stdin=None):
    return run([sys.executable,str(repo/'isolated_system4'/'root_entry.py'),*args],cwd=repo,stdin=stdin,check=False)


class RootEntryTests(unittest.TestCase):
    def positive_stdin(self, *, branch='system4-sandbox', detached=False, extra_noncritical_commit=False):
        td,repo=make_clean_repo(branch=branch,detached=detached,extra_noncritical_commit=extra_noncritical_commit)
        self.addCleanup(td.cleanup)
        raw=bound_snapshot(repo)
        workspace=Path(td.name)/'runtime'
        cp=run_entry(repo,['start-stdin',str(workspace)],stdin=raw)
        self.assertEqual(cp.returncode,0,cp.stdout.decode()+cp.stderr.decode())
        self.assertIn('SYSTEM4_ROOT_ENTRY_PASS:RESEARCH_REQUIRED',cp.stdout.decode())
        self.assertEqual((workspace/'bound_snapshot.json').read_bytes(),raw)
        state=json.loads((workspace/'state.json').read_text(encoding='utf-8'))
        self.assertEqual(state['phase'],'RESEARCH_REQUIRED')
        return repo,workspace

    def test_root_override_binds_system4_without_mutating_base_agents(self):
        td,repo=make_clean_repo(); self.addCleanup(td.cleanup)
        base=(repo/'AGENTS.md').read_text(encoding='utf-8')
        override=(repo/'AGENTS.override.md').read_text(encoding='utf-8')
        self.assertNotIn('SYSTEM4_ISOLATED_ROOT_ENTRY_V3',base)
        self.assertIn('python3 control/cloud-entry-gate/cloud_entry.py start',base)
        self.assertIn('SYSTEM4_ISOLATED_ROOT_ENTRY_V3',override)
        self.assertIn('python3 isolated_system4/root_entry.py start-stdin',override)

    def test_positive_canonical_named_branch(self):
        self.positive_stdin(branch='hobbyroom/system4-true-single-room-v1')

    def test_positive_arbitrary_symbolic_branch_same_critical_content(self):
        self.positive_stdin(branch='codex/pr-238-checkout')

    def test_positive_detached_head_same_critical_content(self):
        repo,_=self.positive_stdin(detached=True)
        current=run(['git','branch','--show-current'],cwd=repo).stdout.decode().strip()
        self.assertEqual(current,'')

    def test_positive_different_commit_same_critical_content(self):
        self.positive_stdin(branch='codex/synthetic',extra_noncritical_commit=True)

    def test_positive_file_entry_from_outside_repo(self):
        td,repo=make_clean_repo(); self.addCleanup(td.cleanup)
        runtime=Path(td.name)/'runtime'; runtime.mkdir()
        snapshot=runtime/'snapshot.json'; snapshot.write_bytes(bound_snapshot(repo))
        workspace=runtime/'workspace'
        cp=run_entry(repo,['start',str(snapshot),str(workspace)])
        self.assertEqual(cp.returncode,0,cp.stdout.decode()+cp.stderr.decode())
        self.assertIn('SYSTEM4_ROOT_ENTRY_PASS:RESEARCH_REQUIRED',cp.stdout.decode())

    def test_negative_manifest_missing(self):
        td,repo=make_clean_repo(); self.addCleanup(td.cleanup)
        cp=run_entry(repo,['start-stdin',str(Path(td.name)/'runtime')],stdin=bound_snapshot(repo,include_manifest=False))
        self.assertEqual(cp.returncode,2)
        self.assertIn('ROOT_ENTRY_MANIFEST_BINDING_MISSING',cp.stdout.decode())

    def test_negative_manifest_mismatch(self):
        td,repo=make_clean_repo(); self.addCleanup(td.cleanup)
        cp=run_entry(repo,['start-stdin',str(Path(td.name)/'runtime')],stdin=bound_snapshot(repo,manifest_value='0'*64))
        self.assertEqual(cp.returncode,2)
        self.assertIn('ROOT_ENTRY_MANIFEST_MISMATCH',cp.stdout.decode())

    def test_negative_dirty_critical_override_is_blocked(self):
        td,repo=make_clean_repo(); self.addCleanup(td.cleanup)
        old=manifest(repo)
        (repo/'AGENTS.override.md').write_text((repo/'AGENTS.override.md').read_text(encoding='utf-8')+'\nTAMPER\n',encoding='utf-8')
        cp=run_entry(repo,['start-stdin',str(Path(td.name)/'runtime')],stdin=bound_snapshot(repo,manifest_value=old))
        self.assertEqual(cp.returncode,2)
        self.assertIn('ROOT_ENTRY_CRITICAL_FILES_DIRTY',cp.stdout.decode())

    def test_negative_dirty_controller_is_blocked(self):
        td,repo=make_clean_repo(); self.addCleanup(td.cleanup)
        old=manifest(repo)
        p=repo/'isolated_system4'/'controller.py'; p.write_text(p.read_text(encoding='utf-8')+'\n# TAMPER\n',encoding='utf-8')
        cp=run_entry(repo,['start-stdin',str(Path(td.name)/'runtime')],stdin=bound_snapshot(repo,manifest_value=old))
        self.assertEqual(cp.returncode,2)
        self.assertIn('ROOT_ENTRY_CRITICAL_FILES_DIRTY',cp.stdout.decode())

    def test_negative_missing_override_is_blocked(self):
        td,repo=make_clean_repo(); self.addCleanup(td.cleanup)
        (repo/'AGENTS.override.md').unlink()
        cp=run_entry(repo,['start-stdin',str(Path(td.name)/'runtime')],stdin=b'{}')
        self.assertEqual(cp.returncode,2)
        self.assertIn('ROOT_OVERRIDE_MISSING',cp.stdout.decode())

    def test_negative_repo_internal_snapshot_is_blocked(self):
        td,repo=make_clean_repo(); self.addCleanup(td.cleanup)
        fixture=repo/'isolated_system4'/'live_fixture'/'wordpress_snapshot.json'
        cp=run_entry(repo,['start',str(fixture),str(Path(td.name)/'runtime')])
        self.assertEqual(cp.returncode,2)
        self.assertIn('ROOT_ENTRY_SNAPSHOT_MUST_BE_OUTSIDE_REPO',cp.stdout.decode())

    def test_negative_repo_internal_workspace_is_blocked(self):
        td,repo=make_clean_repo(); self.addCleanup(td.cleanup)
        external=Path(td.name)/'snapshot.json'; external.write_bytes(bound_snapshot(repo))
        cp=run_entry(repo,['start',str(external),str(repo/'isolated_system4'/'_forbidden_workspace')])
        self.assertEqual(cp.returncode,2)
        self.assertIn('ROOT_ENTRY_WORKSPACE_MUST_BE_OUTSIDE_REPO',cp.stdout.decode())

    def test_negative_invalid_stdin_is_blocked_without_state(self):
        td,repo=make_clean_repo(); self.addCleanup(td.cleanup)
        workspace=Path(td.name)/'runtime'
        cp=run_entry(repo,['start-stdin',str(workspace)],stdin=b'{not-json')
        self.assertEqual(cp.returncode,2)
        self.assertIn('ROOT_ENTRY_STDIN_SNAPSHOT_JSON_INVALID',cp.stdout.decode())
        self.assertFalse((workspace/'state.json').exists())


if __name__=='__main__':
    unittest.main(verbosity=2)
