#!/usr/bin/env python3
from __future__ import annotations
import hashlib
import importlib.util
import json
import subprocess
import tempfile
from pathlib import Path

MOD = Path(__file__).resolve().parent / 'codex_environment_preflight.py'
spec = importlib.util.spec_from_file_location('preflight', MOD)
m = importlib.util.module_from_spec(spec)
spec.loader.exec_module(m)


def dump(path: Path, obj) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(obj, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def git(repo: Path, *args: str) -> str:
    return subprocess.run(['git', *args], cwd=repo, check=True, text=True, stdout=subprocess.PIPE).stdout.strip()


def make_repo(root: Path) -> tuple[Path, str]:
    repo = root / 'repo'
    repo.mkdir()
    subprocess.run(['git','init','-b','main'], cwd=repo, check=True, stdout=subprocess.DEVNULL)
    subprocess.run(['git','config','user.email','ci@example.invalid'], cwd=repo, check=True)
    subprocess.run(['git','config','user.name','CI'], cwd=repo, check=True)

    runtime_entry = repo/'control/output-quarantine/runtime_entry_gate.py'
    runtime_entry.parent.mkdir(parents=True, exist_ok=True)
    runtime_entry.write_text('# runtime entry\n', encoding='utf-8')
    policy = {
        'chat_execution_authority':'NONE','chat_output_authority':'NONE',
        'domain_logic_authority':'NONE','content_semantics_authority':'NONE',
        'quality_authority':'NONE','design_authority':'NONE','seo_authority':'NONE',
        'publish_allowed':False,
    }
    policyp = repo/'control/output-quarantine/OUTPUT_VISIBILITY_POLICY.json'; dump(policyp, policy)
    packagep = repo/'control/startmaster0107/runtime_inbox/generations/000001/PRODUCTION_PACKAGE.json'
    packagep.parent.mkdir(parents=True, exist_ok=True); packagep.write_text('{"x":1}\n', encoding='utf-8')
    runtime = {
        'contract':'PFERDE_ATELIER_RUNTIME_BATCH_SLOT_STATE_V1','status':'EXECUTION_READY','generation':1,
        'batch_sha256':'b'*64,'production_package_ref':'control/startmaster0107/runtime_inbox/generations/000001/PRODUCTION_PACKAGE.json',
        'production_package_sha256':sha(packagep),'publish_allowed':False,
    }
    dump(repo/'control/startmaster0107/runtime_inbox/RUNTIME_INBOX_STATE.json', runtime)
    bundlep = repo/'control/startmaster0107/STEP_107007_RUN_NEW_ARTICLE_BATCH_NO_STOP.json'
    dump(bundlep, {'step_id':'RUN_NEW_ARTICLE_BATCH_NO_STOP','sequence':107007})
    state = {
        'startmaster':'STARTMASTER0107','next_allowed_step':'RUN_NEW_ARTICLE_BATCH_NO_STOP',
        'execution_gate':{
            'step_id':'RUN_NEW_ARTICLE_BATCH_NO_STOP','sequence':107007,
            'bundle_ref':'control/startmaster0107/STEP_107007_RUN_NEW_ARTICLE_BATCH_NO_STOP.json',
            'bundle_sha256':sha(bundlep),'domain_logic_authority':'NONE',
            'content_quality_design_authority':'NONE','hard_worker_target':'CODEX_CLOUD',
        },
    }
    statep = repo/'control/startmaster0107/CURRENT_STATE.json'; dump(statep, state)
    root = {'startmaster':'STARTMASTER0107','current_state_sha256':sha(statep),'next_allowed_step':'RUN_NEW_ARTICLE_BATCH_NO_STOP'}
    rootp = repo/'control/startmaster0107/PFERDE_ATELIER_START_HERE.json'; dump(rootp, root)
    ptr = {
        'contract':'PFERDE_ATELIER_CURRENT_STARTMASTER_POINTER_V2','startmaster':'STARTMASTER0107',
        'root_ref':'control/startmaster0107/PFERDE_ATELIER_START_HERE.json','state_ref':'control/startmaster0107/CURRENT_STATE.json',
        'visible_output_policy_ref':'control/output-quarantine/OUTPUT_VISIBILITY_POLICY.json','visible_output_policy_sha256':sha(policyp),
        'execution_entrance_gate_ref':'control/output-quarantine/runtime_entry_gate.py','execution_entrance_gate_sha256':sha(runtime_entry),
        'free_chat_execution_authority':False,'chat_project_result_authority':'NONE','hard_worker':'CODEX_CLOUD',
        'visible_output_authority':'RELEASE_RECEIPT_ONLY',
    }
    dump(repo/'control/CURRENT_STARTMASTER.json', ptr)
    subprocess.run(['git','add','.'], cwd=repo, check=True)
    subprocess.run(['git','commit','-m','fixture'], cwd=repo, check=True, stdout=subprocess.DEVNULL)
    head = git(repo,'rev-parse','HEAD')
    subprocess.run(['git','update-ref','refs/remotes/origin/main',head], cwd=repo, check=True)
    return repo, head


def blocked(fn, token: str):
    try:
        fn()
    except m.PreflightBlocked as exc:
        assert token in str(exc), (token, str(exc))
        return
    raise AssertionError('expected block: '+token)


def main():
    with tempfile.TemporaryDirectory() as td:
        repo, head = make_repo(Path(td))
        proof = m.validate(repo, main_sha_provider=lambda:(head,'CODEX_SETUP_MAINTENANCE_TRACKING_MAIN'), ed25519_provider=lambda:True)
        assert proof['status']=='CODEX_PRODUCTION_PREFLIGHT_PASS'
        assert proof['content_semantics_inspected'] is False
        assert proof['quality_authority']=='NONE'
        assert proof['workflow_navigation_decision'] is False
        assert proof['publish_allowed'] is False
        detected, source = m.authoritative_main_sha(repo)
        assert detected == head and source == 'CODEX_SETUP_MAINTENANCE_TRACKING_MAIN'

        blocked(lambda:m.validate(repo, main_sha_provider=lambda:('0'*40,'CODEX_SETUP_MAINTENANCE_TRACKING_MAIN'), ed25519_provider=lambda:True), 'CODEX_CHECKOUT_NOT_CURRENT_MAIN')
        blocked(lambda:m.validate(repo, main_sha_provider=lambda:(head,'CODEX_SETUP_MAINTENANCE_TRACKING_MAIN'), ed25519_provider=lambda:False), 'ED25519_RUNTIME_UNAVAILABLE')

        runtimep=repo/'control/startmaster0107/runtime_inbox/RUNTIME_INBOX_STATE.json'
        runtime=json.loads(runtimep.read_text()); runtime['status']='BATCH_READY_PACKAGE_PENDING'; dump(runtimep,runtime)
        blocked(lambda:m.validate(repo, main_sha_provider=lambda:(head,'CODEX_SETUP_MAINTENANCE_TRACKING_MAIN'), ed25519_provider=lambda:True), 'RUNTIME_NOT_EXECUTION_READY')
        runtime['status']='EXECUTION_READY'; dump(runtimep,runtime)

        ptrp=repo/'control/CURRENT_STARTMASTER.json'; ptr=json.loads(ptrp.read_text()); ptr['free_chat_execution_authority']=True; dump(ptrp,ptr)
        blocked(lambda:m.validate(repo, main_sha_provider=lambda:(head,'CODEX_SETUP_MAINTENANCE_TRACKING_MAIN'), ed25519_provider=lambda:True), 'FREE_CHAT_EXECUTION_MUST_BE_FALSE')

    print(json.dumps({'ok':True,'status':'CODEX_ENVIRONMENT_PREFLIGHT_POSITIVE_NEGATIVE_PASS','positive':1,'negative':4,'content_semantics_inspected':False,'quality_authority':'NONE','publish_allowed':False}, indent=2))

if __name__=='__main__':
    main()
