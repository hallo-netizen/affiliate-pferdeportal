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



def toolbox_ok():
    return {
        'status':'RUNTIME_TOOLBOX_PASS',
        'php_executable':True,
        'php_version':'8.test',
        'java_executable':True,
        'java_version':'java test',
        'languagetool_real_execution':True,
        'languagetool_engine':m.LT_ENGINE,
        'languagetool_outer_sha256':m.LT_OUTER_SHA256,
        'languagetool_inner_sha256':m.LT_INNER_SHA256,
        'languagetool_jar_sha256':m.LT_JAR_SHA256,
        'ppm679_package_sha256':m.PPM679_PACKAGE_SHA256,
        'pserc_fix_package_sha256':m.PSERC_FIX_PACKAGE_SHA256,
        'agent_network_required':False,
        'content_semantics_inspected':False,
        'quality_authority':'NONE',
        'publish_allowed':False,
    }


def validate(repo, head, *, ed25519=True, toolbox=None, main_sha=None):
    return m.validate(
        repo,
        main_sha_provider=lambda:((main_sha or head),'CODEX_CHECKOUT_REMOTE_TRACKING_MAIN'),
        ed25519_provider=lambda:ed25519,
        runtime_tools_provider=lambda _repo:(toolbox if toolbox is not None else toolbox_ok()),
    )


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
        proof = validate(repo, head)
        assert proof['status']=='CODEX_PRODUCTION_PREFLIGHT_PASS'
        assert proof['content_semantics_inspected'] is False
        assert proof['quality_authority']=='NONE'
        assert proof['workflow_navigation_decision'] is False
        assert proof['publish_allowed'] is False
        detected, source = m.authoritative_main_sha(repo)
        assert detected == head and source == 'CODEX_CHECKOUT_REMOTE_TRACKING_MAIN'

        blocked(lambda:validate(repo, head, main_sha='0'*40), 'CODEX_CHECKOUT_NOT_CURRENT_MAIN')
        blocked(lambda:validate(repo, head, ed25519=False), 'ED25519_RUNTIME_UNAVAILABLE')

        bad=toolbox_ok(); bad['languagetool_jar_sha256']='0'*64
        blocked(lambda:validate(repo, head, toolbox=bad), 'RUNTIME_TOOLBOX_PROOF_INVALID:languagetool_jar_sha256')
        bad=toolbox_ok(); bad['java_executable']=False
        blocked(lambda:validate(repo, head, toolbox=bad), 'RUNTIME_TOOLBOX_PROOF_INVALID:java_executable')
        bad=toolbox_ok(); bad['php_executable']=False
        blocked(lambda:validate(repo, head, toolbox=bad), 'RUNTIME_TOOLBOX_PROOF_INVALID:php_executable')
        bad=toolbox_ok(); bad['ppm679_package_sha256']='0'*64
        blocked(lambda:validate(repo, head, toolbox=bad), 'RUNTIME_TOOLBOX_PROOF_INVALID:ppm679_package_sha256')
        bad=toolbox_ok(); bad['pserc_fix_package_sha256']='0'*64
        blocked(lambda:validate(repo, head, toolbox=bad), 'RUNTIME_TOOLBOX_PROOF_INVALID:pserc_fix_package_sha256')

        runtimep=repo/'control/startmaster0107/runtime_inbox/RUNTIME_INBOX_STATE.json'
        runtime=json.loads(runtimep.read_text()); runtime['status']='BATCH_READY_PACKAGE_PENDING'; dump(runtimep,runtime)
        blocked(lambda:validate(repo, head), 'RUNTIME_NOT_EXECUTION_READY')
        runtime['status']='EXECUTION_READY'; dump(runtimep,runtime)

        ptrp=repo/'control/CURRENT_STARTMASTER.json'; ptr=json.loads(ptrp.read_text()); ptr['free_chat_execution_authority']=True; dump(ptrp,ptr)
        blocked(lambda:validate(repo, head), 'FREE_CHAT_EXECUTION_MUST_BE_FALSE')

    print(json.dumps({'ok':True,'status':'CODEX_ENVIRONMENT_PREFLIGHT_POSITIVE_NEGATIVE_PASS','positive':1,'negative':9,'content_semantics_inspected':False,'quality_authority':'NONE','publish_allowed':False}, indent=2))

if __name__=='__main__':
    main()
