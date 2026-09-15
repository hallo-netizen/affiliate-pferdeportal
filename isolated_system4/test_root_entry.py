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


def head(repo:Path)->str:
    return run(['git','rev-parse','--verify','HEAD'],cwd=repo).stdout.decode().strip()


POINT0_BUILDER=r'''
import json,sys
from pathlib import Path
sys.path.insert(0,'isolated_system4')
import point0_snapshot,test_point0_v2
out=Path(sys.argv[1]); manifest=sys.argv[2]; head=sys.argv[3]
base=test_point0_v2.fixture()
raw=point0_snapshot.verify(base)
snap=json.loads(raw.decode('utf-8'))
snap['system4_root_manifest_sha256']=manifest
raw=(json.dumps(snap,ensure_ascii=False,sort_keys=True,separators=(',',':'))+'\n').encode('utf-8')
source_pools=[row['sources'] for row in base['research_runtime']['item_pools']]
prewrite=list(base['machine_prewrite']['items'])
p0=point0_snapshot.build(production_snapshot_bytes=raw,root_manifest_sha256=manifest,head_sha=head,research_provider='TEST_ROOT_ENTRY',source_pools=source_pools,prewrite_bindings=prewrite)
out.write_bytes(point0_snapshot.canon(p0))
'''


def make_point0(repo:Path, path:Path, *, manifest_value=None, head_value=None)->Path:
    path.parent.mkdir(parents=True,exist_ok=True)
    m=manifest_value or manifest(repo)
    h=head_value or head(repo)
    run([sys.executable,'-c',POINT0_BUILDER,str(path),m,h],cwd=repo)
    return path


def run_entry(repo:Path,args):
    return run([sys.executable,str(repo/'isolated_system4'/'root_entry.py'),*args],cwd=repo,check=False)


class RootEntryTests(unittest.TestCase):
    def positive_point0(self, *, branch='system4-sandbox', detached=False, extra_noncritical_commit=False):
        td,repo=make_clean_repo(branch=branch,detached=detached,extra_noncritical_commit=extra_noncritical_commit)
        self.addCleanup(td.cleanup)
        point0=make_point0(repo,Path(td.name)/'point0.json')
        workspace=Path(td.name)/'runtime'
        cp=run_entry(repo,['start-point0',str(point0),str(workspace),'0'])
        self.assertEqual(cp.returncode,0,cp.stdout.decode()+cp.stderr.decode())
        self.assertIn('SYSTEM4_ROOT_POINT0_PASS:WORKER_DISPATCH_READY',cp.stdout.decode())
        for name in ('point0.json','root_receipt.json','supervisor_state.json','bound_snapshot.json','bound_research_sources.json','bound_machine_prewrite.json','worker_dispatch.json','state.json'):
            self.assertTrue((workspace/name).is_file(),name)
        state=json.loads((workspace/'state.json').read_text(encoding='utf-8'))
        self.assertEqual(state['phase'],'RESEARCH_REQUIRED')
        return repo,workspace

    def test_root_override_binds_only_point0_as_executable_route(self):
        td,repo=make_clean_repo(); self.addCleanup(td.cleanup)
        base=(repo/'AGENTS.md').read_text(encoding='utf-8')
        override=(repo/'AGENTS.override.md').read_text(encoding='utf-8')
        self.assertNotIn('SYSTEM4_ISOLATED_ROOT_ENTRY_V3',base)
        self.assertIn('python3 control/cloud-entry-gate/cloud_entry.py start',base)
        self.assertIn('SYSTEM4_ISOLATED_ROOT_ENTRY_V3',override)
        self.assertIn('python3 isolated_system4/root_entry.py start-point0',override)

    def test_positive_point0_canonical_named_branch(self):
        self.positive_point0(branch='hobbyroom/system4-true-single-room-v1')

    def test_positive_point0_arbitrary_symbolic_branch_same_critical_content(self):
        self.positive_point0(branch='codex/pr-238-checkout')

    def test_positive_point0_detached_head_same_critical_content(self):
        repo,_=self.positive_point0(detached=True)
        self.assertEqual(run(['git','branch','--show-current'],cwd=repo).stdout.decode().strip(),'')

    def test_positive_point0_different_commit_same_critical_content(self):
        self.positive_point0(branch='codex/synthetic',extra_noncritical_commit=True)

    def test_negative_legacy_start_is_machine_blocked(self):
        td,repo=make_clean_repo(); self.addCleanup(td.cleanup)
        cp=run_entry(repo,['start','/tmp/input.json',str(Path(td.name)/'runtime')])
        self.assertEqual(cp.returncode,2)
        self.assertIn('MACHINE_ROUTE_BLOCK:POINT0_REQUIRED',cp.stdout.decode())

    def test_negative_legacy_start_stdin_is_machine_blocked(self):
        td,repo=make_clean_repo(); self.addCleanup(td.cleanup)
        cp=run_entry(repo,['start-stdin',str(Path(td.name)/'runtime')])
        self.assertEqual(cp.returncode,2)
        self.assertIn('MACHINE_ROUTE_BLOCK:POINT0_REQUIRED',cp.stdout.decode())

    def test_negative_point0_manifest_mismatch(self):
        td,repo=make_clean_repo(); self.addCleanup(td.cleanup)
        point0=make_point0(repo,Path(td.name)/'point0.json',manifest_value='0'*64)
        cp=run_entry(repo,['start-point0',str(point0),str(Path(td.name)/'runtime'),'0'])
        self.assertEqual(cp.returncode,2)
        self.assertIn('ROOT_POINT0_BIND_FAIL:ROOT_MANIFEST_MISMATCH',cp.stdout.decode())

    def test_negative_point0_head_mismatch(self):
        td,repo=make_clean_repo(); self.addCleanup(td.cleanup)
        point0=make_point0(repo,Path(td.name)/'point0.json',head_value='0'*40)
        cp=run_entry(repo,['start-point0',str(point0),str(Path(td.name)/'runtime'),'0'])
        self.assertEqual(cp.returncode,2)
        self.assertIn('ROOT_POINT0_BIND_FAIL:HEAD_SHA_MISMATCH',cp.stdout.decode())

    def test_negative_dirty_critical_override_is_blocked(self):
        td,repo=make_clean_repo(); self.addCleanup(td.cleanup)
        point0=make_point0(repo,Path(td.name)/'point0.json')
        p=repo/'AGENTS.override.md'; p.write_text(p.read_text(encoding='utf-8')+'\nTAMPER\n',encoding='utf-8')
        cp=run_entry(repo,['start-point0',str(point0),str(Path(td.name)/'runtime'),'0'])
        self.assertEqual(cp.returncode,2)
        self.assertIn('ROOT_ENTRY_CRITICAL_FILES_DIRTY',cp.stdout.decode())

    def test_negative_dirty_controller_is_blocked(self):
        td,repo=make_clean_repo(); self.addCleanup(td.cleanup)
        point0=make_point0(repo,Path(td.name)/'point0.json')
        p=repo/'isolated_system4'/'controller.py'; p.write_text(p.read_text(encoding='utf-8')+'\n# TAMPER\n',encoding='utf-8')
        cp=run_entry(repo,['start-point0',str(point0),str(Path(td.name)/'runtime'),'0'])
        self.assertEqual(cp.returncode,2)
        self.assertIn('ROOT_ENTRY_CRITICAL_FILES_DIRTY',cp.stdout.decode())

    def test_negative_missing_override_is_blocked(self):
        td,repo=make_clean_repo(); self.addCleanup(td.cleanup)
        point0=make_point0(repo,Path(td.name)/'point0.json')
        (repo/'AGENTS.override.md').unlink()
        cp=run_entry(repo,['start-point0',str(point0),str(Path(td.name)/'runtime'),'0'])
        self.assertEqual(cp.returncode,2)
        self.assertIn('ROOT_OVERRIDE_MISSING',cp.stdout.decode())

    def test_negative_repo_internal_point0_is_blocked(self):
        td,repo=make_clean_repo(); self.addCleanup(td.cleanup)
        point0=make_point0(repo,repo/'isolated_system4'/'_forbidden_point0.json')
        cp=run_entry(repo,['start-point0',str(point0),str(Path(td.name)/'runtime'),'0'])
        self.assertEqual(cp.returncode,2)
        self.assertIn('ROOT_POINT0_FILE_INVALID',cp.stdout.decode())

    def test_negative_repo_internal_workspace_is_blocked(self):
        td,repo=make_clean_repo(); self.addCleanup(td.cleanup)
        point0=make_point0(repo,Path(td.name)/'point0.json')
        cp=run_entry(repo,['start-point0',str(point0),str(repo/'isolated_system4'/'_forbidden_workspace'),'0'])
        self.assertEqual(cp.returncode,2)
        self.assertIn('ROOT_ENTRY_WORKSPACE_MUST_BE_OUTSIDE_REPO',cp.stdout.decode())

    def test_negative_nonempty_workspace_is_blocked(self):
        td,repo=make_clean_repo(); self.addCleanup(td.cleanup)
        point0=make_point0(repo,Path(td.name)/'point0.json')
        workspace=Path(td.name)/'runtime'; workspace.mkdir(); (workspace/'junk').write_text('x',encoding='utf-8')
        cp=run_entry(repo,['start-point0',str(point0),str(workspace),'0'])
        self.assertEqual(cp.returncode,2)
        self.assertIn('ROOT_POINT0_BIND_FAIL:WORKSPACE_NOT_EMPTY',cp.stdout.decode())

    def test_negative_invalid_point0_is_blocked_without_state(self):
        td,repo=make_clean_repo(); self.addCleanup(td.cleanup)
        point0=Path(td.name)/'point0.json'; point0.write_text('{not-json',encoding='utf-8')
        workspace=Path(td.name)/'runtime'
        cp=run_entry(repo,['start-point0',str(point0),str(workspace),'0'])
        self.assertEqual(cp.returncode,2)
        self.assertIn('ROOT_CHAT_START_BIND_FAIL:',cp.stdout.decode())
        self.assertFalse((workspace/'state.json').exists())


if __name__=='__main__':
    unittest.main(verbosity=2)
