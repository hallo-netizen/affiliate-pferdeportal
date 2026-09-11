import json
import subprocess
import tempfile
import unittest
from pathlib import Path

import proof_persistence_guard as guard


def git(cwd: Path, *args: str) -> str:
    p=subprocess.run(['git','-C',str(cwd),*args],text=True,stdout=subprocess.PIPE,stderr=subprocess.PIPE,check=True)
    return p.stdout.strip()


class ProofPersistenceGuardTest(unittest.TestCase):
    def setUp(self):
        self.tmp=tempfile.TemporaryDirectory()
        root=Path(self.tmp.name)
        self.remote=root/'remote.git'
        self.repo=root/'repo'
        subprocess.run(['git','init','--bare',str(self.remote)],check=True,stdout=subprocess.DEVNULL)
        subprocess.run(['git','init',str(self.repo)],check=True,stdout=subprocess.DEVNULL)
        git(self.repo,'config','user.email','system4@test.invalid')
        git(self.repo,'config','user.name','System4 Test')
        git(self.repo,'remote','add','origin',str(self.remote))
        git(self.repo,'checkout','-b','hobbyroom/system4-true-single-room-v1')
        proof_dir=self.repo/guard.PROOF_REL
        proof_dir.mkdir(parents=True)
        proof={
            'publish_allowed':False,
            'next_required':'SIGNED_WORKFLOW_RELEASE',
            'batch_sha256':guard.BATCH_SHA,
            'articles':[{'plan_slot':slot} for slot in guard.PLAN_SLOTS],
        }
        (proof_dir/'SYSTEM4_7_7_FULL_BATCH_PROOF.json').write_text(json.dumps(proof),encoding='utf-8')
        (proof_dir/'system4_batch_evidence.json').write_text('{}',encoding='utf-8')
        for slot in guard.PLAN_SLOTS:
            (proof_dir/f'ARTICLE_{slot}.md').write_text('# test',encoding='utf-8')
        git(self.repo,'add','.')
        git(self.repo,'commit','-m','proof')

    def tearDown(self):
        self.tmp.cleanup()

    def test_pass_after_real_push(self):
        git(self.repo,'push','-u','origin','hobbyroom/system4-true-single-room-v1')
        self.assertEqual(
            guard.verify(self.repo,'hobbyroom/system4-true-single-room-v1'),
            git(self.repo,'rev-parse','HEAD'),
        )

    def test_blocks_local_only_commit(self):
        with self.assertRaisesRegex(guard.GuardFail,'REMOTE_BRANCH_MISSING|REMOTE_HEAD_MISMATCH'):
            guard.verify(self.repo,'hobbyroom/system4-true-single-room-v1')

    def test_blocks_unpushed_followup_commit(self):
        git(self.repo,'push','-u','origin','hobbyroom/system4-true-single-room-v1')
        article=self.repo/guard.PROOF_REL/f'ARTICLE_{guard.PLAN_SLOTS[0]}.md'
        article.write_text('# locally changed',encoding='utf-8')
        git(self.repo,'add','.')
        git(self.repo,'commit','-m','local-only-followup')
        with self.assertRaisesRegex(guard.GuardFail,'REMOTE_HEAD_MISMATCH'):
            guard.verify(self.repo,'hobbyroom/system4-true-single-room-v1')

    def test_blocks_missing_proof_file(self):
        git(self.repo,'push','-u','origin','hobbyroom/system4-true-single-room-v1')
        (self.repo/guard.PROOF_REL/'system4_batch_evidence.json').unlink()
        with self.assertRaisesRegex(guard.GuardFail,'PROOF_FILE_MISSING'):
            guard.verify(self.repo,'hobbyroom/system4-true-single-room-v1')


if __name__=='__main__':
    unittest.main()
