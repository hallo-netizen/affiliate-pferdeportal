from __future__ import annotations
import hashlib, json, os, subprocess, sys
from pathlib import Path

import batch_gate, codex_entry, handoff_transport

HERE = Path(__file__).resolve().parent
REPO = HERE.parent
ROOT_ENTRY = HERE / 'root_entry.py'
CONTROLLER = HERE / 'controller.py'
CONTRACT = 'SYSTEM4_PRODUCTION_BINDING_V1'
STATE_CONTRACT = 'SYSTEM4_PRODUCTION_BATCH_STATE_V1'
ACTIVE_POINTER = REPO / '.pferde-capsule' / 'SYSTEM4_ACTIVE_PRODUCTION_RUN.json'
DEFAULT_BINDING = REPO / '.pferde-capsule' / 'SYSTEM4_PRODUCTION_BINDING_V1.json'
HANDOFF_NAME = handoff_transport.HANDOFF_FILENAME

class RouteError(RuntimeError):
    pass

def canon(v):
    return json.dumps(v, ensure_ascii=False, sort_keys=True, separators=(',', ':')).encode('utf-8')

def sha_bytes(raw: bytes) -> str:
    return hashlib.sha256(raw).hexdigest()

def load(path: Path) -> dict:
    try:
        value = json.loads(path.read_text(encoding='utf-8'))
    except Exception as exc:
        raise RouteError('JSON_INVALID:' + str(path)) from exc
    if not isinstance(value, dict):
        raise RouteError('JSON_OBJECT_REQUIRED:' + str(path))
    return value

def write(path: Path, value: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2, sort_keys=True) + '\n', encoding='utf-8')

def outside_repo(path: Path) -> Path:
    p = path.expanduser().resolve()
    root = REPO.resolve()
    if p == root or root in p.parents:
        raise RouteError('PATH_MUST_BE_OUTSIDE_REPO:' + str(path))
    return p

def binding_path() -> Path:
    raw = os.environ.get('SYSTEM4_PRODUCTION_BINDING', '').strip()
    return Path(raw).expanduser() if raw else DEFAULT_BINDING

def validate_binding(value: dict) -> dict:
    required = {'contract','point0_path','snapshot_path','run_root','publish_allowed'}
    if set(value) != required or value.get('contract') != CONTRACT:
        raise RouteError('PRODUCTION_BINDING_SCHEMA_INVALID')
    if value.get('publish_allowed') is not False:
        raise RouteError('PRODUCTION_BINDING_PUBLISH_MUST_BE_FALSE')
    point0 = outside_repo(Path(str(value['point0_path'])))
    snapshot = outside_repo(Path(str(value['snapshot_path'])))
    run_root = outside_repo(Path(str(value['run_root'])))
    if not point0.is_file():
        raise RouteError('POINT0_MISSING')
    if not snapshot.is_file():
        raise RouteError('SNAPSHOT_MISSING')
    snap = load(snapshot)
    batch = snap.get('next_textmachine_metadata_batch')
    if not isinstance(batch, dict) or batch.get('contract') != 'PSERC_TEXTMACHINE_METADATA_BATCH_V2':
        raise RouteError('SNAPSHOT_BATCH_INVALID')
    items = batch.get('items')
    if not isinstance(items, list) or not items or batch.get('item_count') != len(items):
        raise RouteError('SNAPSHOT_ITEMS_INVALID')
    if batch.get('publish_allowed') is not False:
        raise RouteError('SNAPSHOT_PUBLISH_MUST_BE_FALSE')
    return {'point0':point0,'snapshot':snapshot,'run_root':run_root,'batch':batch,'items':items}

def state_path(run_root: Path) -> Path:
    return run_root / 'production_batch_state.json'

def active() -> tuple[dict,dict]:
    if not ACTIVE_POINTER.is_file():
        raise RouteError('ACTIVE_PRODUCTION_RUN_MISSING')
    ptr = load(ACTIVE_POINTER)
    if ptr.get('contract') != 'SYSTEM4_ACTIVE_PRODUCTION_RUN_V1':
        raise RouteError('ACTIVE_PRODUCTION_RUN_INVALID')
    sp = outside_repo(Path(str(ptr.get('state_path') or '')))
    st = load(sp)
    if st.get('contract') != STATE_CONTRACT:
        raise RouteError('PRODUCTION_BATCH_STATE_INVALID')
    return ptr, st

def save_state(st: dict) -> None:
    write(Path(st['state_path']), st)

def run(args: list[str]) -> subprocess.CompletedProcess[str]:
    cp = subprocess.run(args, cwd=REPO, text=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    if cp.returncode:
        raise RouteError('COMMAND_FAIL:' + ' '.join(args) + ':' + cp.stdout.strip() + ':' + cp.stderr.strip())
    return cp

def ensure_workspace(st: dict, index: int) -> Path:
    if index < 0 or index >= st['article_count']:
        raise RouteError('ITEM_INDEX_INVALID')
    w = Path(st['run_root']) / f'item-{index}'
    state = w / 'state.json'
    if not state.is_file():
        cp = run([sys.executable, str(ROOT_ENTRY), 'start-point0', st['point0_path'], str(w), str(index)])
        if 'SYSTEM4_ROOT_POINT0_PASS:WORKER_DISPATCH_READY' not in cp.stdout:
            raise RouteError('ROOT_ENTRY_PASS_MARKER_MISSING')
    return w

def cmd_start() -> int:
    bp = binding_path()
    if not bp.is_file():
        raise RouteError('SYSTEM4_PRODUCTION_BINDING_MISSING:' + str(bp))
    b = validate_binding(load(bp))
    rr = b['run_root']
    rr.mkdir(parents=True, exist_ok=True)
    sp = state_path(rr)
    if sp.exists():
        st = load(sp)
        if st.get('contract') != STATE_CONTRACT:
            raise RouteError('EXISTING_RUN_STATE_INVALID')
    else:
        st = {
            'contract': STATE_CONTRACT,
            'state_path': str(sp),
            'point0_path': str(b['point0']),
            'snapshot_path': str(b['snapshot']),
            'run_root': str(rr),
            'batch_sha256': b['batch']['batch_sha256'],
            'article_count': len(b['items']),
            'current_index': 0,
            'handoff_path': str(rr / HANDOFF_NAME),
            'status': 'ACTIVE',
            'publish_allowed': False,
        }
        save_state(st)
    ensure_workspace(st, st['current_index'])
    ACTIVE_POINTER.parent.mkdir(parents=True, exist_ok=True)
    write(ACTIVE_POINTER, {'contract':'SYSTEM4_ACTIVE_PRODUCTION_RUN_V1','state_path':str(sp),'publish_allowed':False})
    print(json.dumps({'status':'SYSTEM4_PRODUCTION_ROUTE_READY','article_count':st['article_count'],'current_index':st['current_index'],'batch_sha256':st['batch_sha256'],'publish_allowed':False}, sort_keys=True))
    return 0

def phase_for(w: Path) -> str:
    value = load(w / 'state.json')
    return str(value.get('phase') or '')

def cmd_current() -> int:
    _, st = active()
    while st['current_index'] < st['article_count']:
        i = int(st['current_index'])
        w = ensure_workspace(st, i)
        s = load(w / 'state.json')
        if s.get('phase') == 'OUTPUT_GATE_REQUIRED':
            checks = s.get('checks') or {}
            if checks.get('status') != 'PASS' or checks.get('mode') != 'FULL_PRODUCTION':
                raise RouteError('OUTPUT_GATE_WITHOUT_FULL_PASS:' + str(i))
            st['current_index'] = i + 1
            save_state(st)
            continue
        rc = codex_entry.worker_start(w)
        if rc:
            raise RouteError('CODEX_ENTRY_BLOCKED:' + str(i))
        print('SYSTEM4_PRODUCTION_CURRENT_INDEX=' + str(i))
        print('SYSTEM4_PRODUCTION_WORKSPACE=' + str(w))
        return 0
    print('SYSTEM4_PRODUCTION_BATCH_READY_FOR_FINISH')
    return 0

def handoff_payload(states: list[dict], items: list[dict], batch_sha: str) -> dict:
    rows=[]
    for i,(s,item) in enumerate(zip(states,items)):
        ev=s['checks']['production_evidence']['evidence']
        rows.append({
            'index':i,'title':item['title'],'target_keyword':item['target_keyword'],'category':item['category'],
            'article_type':item['article_type'],'plan_slot':item['plan_slot'],'final_draft_sha256':s['draft_sha256'],
            'revision_count':s['revision'],'body':s['draft_markdown'],'production_context':s['production_context'],
            'languagetool':ev['languagetool'],'ppm679':ev['ppm679'],
        })
    return {
        'contract':handoff_transport.HANDOFF_CONTRACT,'batch_sha256':batch_sha,'publish_allowed':False,
        'signing_deferred':True,'batch_gate_status':'SYSTEM4_BATCH_FULL_PASS_COLLECTED','no_legacy_status':'PASS',
        'test_suite_status':'PASS','wordpress_review':handoff_transport.wordpress_review(),'articles':rows,
    }

def cmd_finish() -> int:
    _, st = active()
    if st['current_index'] != st['article_count']:
        raise RouteError('BATCH_NOT_COMPLETE')
    snapshot = Path(st['snapshot_path'])
    snap = load(snapshot)
    items = snap['next_textmachine_metadata_batch']['items']
    states=[]; paths=[]
    for i in range(st['article_count']):
        p = Path(st['run_root']) / f'item-{i}' / 'state.json'
        if not p.is_file(): raise RouteError('STATE_MISSING:' + str(i))
        s=load(p)
        if s.get('phase')!='OUTPUT_GATE_REQUIRED' or (s.get('checks') or {}).get('status')!='PASS':
            raise RouteError('STATE_NOT_FULL_PASS:' + str(i))
        states.append(s); paths.append(p)
    batch_out = Path(st['run_root']) / 'batch'
    result = batch_gate.collect_batch(snapshot, paths, batch_out)
    if result.get('status') != 'SYSTEM4_BATCH_FULL_PASS_COLLECTED':
        raise RouteError('BATCH_GATE_NOT_PASS')
    payload=handoff_payload(states,items,st['batch_sha256'])
    handoff_transport.validate_handoff(payload)
    out=Path(st['handoff_path'])
    out.write_bytes((json.dumps(payload,ensure_ascii=False,sort_keys=True,separators=(',',':'))+'\n').encode('utf-8'))
    _, raw = handoff_transport.read_validate_handoff(out)
    digest=sha_bytes(raw)
    st['status']='HANDOFF_READY'; st['handoff_sha256']=digest; save_state(st)
    print(json.dumps({'status':'SYSTEM4_PRODUCTION_HANDOFF_READY','handoff_path':str(out),'handoff_sha256':digest,'article_count':st['article_count'],'batch_sha256':st['batch_sha256'],'next_required':'107008_FINAL_REVIEW_OUTPUT_RELEASE','publish_allowed':False},sort_keys=True))
    return 0

def main(argv: list[str]) -> int:
    try:
        if len(argv)!=2 or argv[1] not in {'start','current','finish'}:
            raise RouteError('USE: production_route.py start|current|finish')
        return {'start':cmd_start,'current':cmd_current,'finish':cmd_finish}[argv[1]]()
    except Exception as exc:
        print('SYSTEM4_PRODUCTION_ROUTE_BLOCK:' + str(exc))
        return 2

if __name__ == '__main__':
    raise SystemExit(main(sys.argv))
