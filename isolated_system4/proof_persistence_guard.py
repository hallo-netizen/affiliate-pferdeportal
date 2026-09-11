from __future__ import annotations
import json, re, subprocess, sys
from pathlib import Path

BATCH_SHA='7f2e3290b6ac78ac7df1644395e57ac72f02dc1373e390eb2e532e57a8ce916a'
PROOF_REL=Path('isolated_system4')/'batch_proof'/BATCH_SHA
PLAN_SLOTS=[
'9c229b0e6a784a482575e3deb16d105e3b5355becbbbb8ecfc8e1f600b529c56',
'6ce9a1e47446daf84e85f08e84c33ada214f92612a654d79e68df18ea4e9fa19',
'7b0e8f8b0653eb3a40aee2a68f4b9909df9d8bda374db0ec8c49e7b53ecbee87',
'5999b9b00de2a1756101c5ebfb2b547c6ff2b9360bd9bae0988696a795ff6288',
'7f7a0b4169c19676b3dfe6457ac07c6685ae6ead6c1873a9467d9b6ee32a81da',
'8c8408cebf7f41becc33cdccf04b60387cf75644468a887730a8d18a4a1a7648',
'906ddc4ee72429a8544da018e1f78d63cb2b80c1f11488180f381e2dc16c4af5',
]
EXPECTED_FILES=['system4_batch_evidence.json','SYSTEM4_7_7_FULL_BATCH_PROOF.json']+[f'ARTICLE_{s}.md' for s in PLAN_SLOTS]

class GuardFail(RuntimeError): pass

def run(repo: Path, *args: str) -> str:
    p=subprocess.run(['git','-C',str(repo),*args],text=True,stdout=subprocess.PIPE,stderr=subprocess.PIPE,check=False)
    if p.returncode != 0:
        raise GuardFail('GIT_COMMAND_FAIL:'+args[0]+':'+(p.stderr or p.stdout).strip()[:200])
    return p.stdout.strip()

def verify(repo: Path, branch: str) -> str:
    if not re.fullmatch(r'[A-Za-z0-9._/-]+', branch or '') or '..' in branch:
        raise GuardFail('BRANCH_INVALID')
    head=run(repo,'rev-parse','HEAD')
    if not re.fullmatch(r'[0-9a-f]{40}',head): raise GuardFail('LOCAL_HEAD_INVALID')
    remote=run(repo,'ls-remote','--heads','origin',f'refs/heads/{branch}')
    fields=remote.split()
    if len(fields)!=2 or fields[1] != f'refs/heads/{branch}': raise GuardFail('REMOTE_BRANCH_MISSING')
    if fields[0] != head: raise GuardFail('REMOTE_HEAD_MISMATCH')
    for name in EXPECTED_FILES:
        rel=(PROOF_REL/name).as_posix()
        if not (repo/rel).is_file(): raise GuardFail('PROOF_FILE_MISSING:'+name)
        run(repo,'cat-file','-e',f'HEAD:{rel}')
    proof=json.loads((repo/PROOF_REL/'SYSTEM4_7_7_FULL_BATCH_PROOF.json').read_text(encoding='utf-8'))
    if proof.get('publish_allowed') is not False: raise GuardFail('PROOF_PUBLISH_AUTHORITY_FAIL')
    if proof.get('next_required')!='SIGNED_WORKFLOW_RELEASE': raise GuardFail('PROOF_NEXT_BOUNDARY_FAIL')
    if 'batch_sha256' in proof and proof.get('batch_sha256')!=BATCH_SHA: raise GuardFail('PROOF_BATCH_SHA_FAIL')
    articles=proof.get('articles')
    if not isinstance(articles,list) or len(articles)!=7: raise GuardFail('PROOF_ARTICLE_COUNT_FAIL')
    slots=[str(x.get('plan_slot') or '') for x in articles if isinstance(x,dict)]
    if slots != PLAN_SLOTS: raise GuardFail('PROOF_PLAN_SLOTS_FAIL')
    print('SYSTEM4_PROOF_REMOTE_PASS:'+head)
    return head

def main(argv):
    try:
        if len(argv)!=3 or argv[1]!='verify': raise GuardFail('USAGE:verify <branch>')
        repo=Path(__file__).resolve().parent.parent
        verify(repo,argv[2]); return 0
    except (GuardFail,json.JSONDecodeError) as e:
        print('SYSTEM4_PROOF_PERSISTENCE_FAIL:'+str(e)); return 2

if __name__=='__main__': raise SystemExit(main(sys.argv))
