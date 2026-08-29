#!/usr/bin/env python3
import argparse, base64, hashlib, io, json, pathlib, sys, zipfile
POLICY_REL=pathlib.Path('control/release-governance/CURRENT_RELEASE.json'); CONTRACT='PFERDE_ATELIER_AFFILIATE_RELEASE_GOVERNANCE_V3'
class GuardError(RuntimeError): pass

def sha256_bytes(b): return hashlib.sha256(b).hexdigest()
def sha256_file(p):
    h=hashlib.sha256()
    with pathlib.Path(p).open('rb') as f:
        for c in iter(lambda:f.read(1024*1024),b''): h.update(c)
    return h.hexdigest()
def load(root):
    p=root/POLICY_REL
    if not p.is_file(): raise GuardError('CURRENT_RELEASE_MISSING')
    try:d=json.loads(p.read_text(encoding='utf-8'))
    except Exception as e: raise GuardError('CURRENT_RELEASE_INVALID_JSON:'+str(e))
    if d.get('contract')!=CONTRACT or d.get('mode')!='ENFORCED' or d.get('workstream')!='AFFILIATE_ZENTRALE': raise GuardError('GOVERNANCE_NOT_ENFORCED')
    for k in ('no_guessing','no_reconstruction','no_side_refactor','no_release_zip_regeneration_before_final_gate'):
        if d.get(k) is not True: raise GuardError('FAIL_CLOSED_FLAG_MISSING:'+k)
    return d
def vf(root,ref,digest,label):
    p=root/ref
    if not p.is_file(): raise GuardError(label+'_MISSING:'+str(ref))
    got=sha256_file(p)
    if got!=digest: raise GuardError(label+'_HASH_MISMATCH:'+got)
    return p
def read_chunks(root,ref,label):
    d=root/ref
    if not d.is_dir(): raise GuardError(label+'_CHUNKS_MISSING:'+str(ref))
    files=sorted(p for p in d.iterdir() if p.is_file())
    if not files: raise GuardError(label+'_CHUNKS_EMPTY')
    if any(p.name!=f'chunk{i:03d}.txt' for i,p in enumerate(files)): raise GuardError(label+'_CHUNK_SEQUENCE_INVALID')
    try:
        text=''.join(''.join(p.read_text(encoding='ascii').split()) for p in files)
        return base64.b64decode(text,validate=True)
    except Exception as e: raise GuardError(label+'_BASE64_INVALID:'+str(e))
def manifest(root,ref,digest,count,label):
    p=vf(root,ref,digest,label+'_MANIFEST'); rows=[]
    for raw in p.read_text(encoding='utf-8').splitlines():
        if not raw.strip(): continue
        a=raw.split(None,1)
        if len(a)!=2 or len(a[0])!=64: raise GuardError(label+'_MANIFEST_FORMAT')
        rows.append((a[0],a[1].strip()))
    if len(rows)!=int(count): raise GuardError(label+'_FILE_COUNT')
    return rows
def zipbytes_vs_manifest(root,ref,zhash,mref,mhash,count,label):
    raw=read_chunks(root,ref,label)
    got=sha256_bytes(raw)
    if got!=zhash: raise GuardError(label+'_ZIP_HASH_MISMATCH:'+got)
    rows=manifest(root,mref,mhash,count,label)
    try:
        with zipfile.ZipFile(io.BytesIO(raw)) as z:
            actual=sorted(n for n in z.namelist() if not n.endswith('/')); expected=sorted(r for _,r in rows)
            if actual!=expected: raise GuardError(label+'_ZIP_FILE_LIST')
            for dig,rel in rows:
                if sha256_bytes(z.read(rel))!=dig: raise GuardError(label+'_ZIP_SOURCE_HASH:'+rel)
    except zipfile.BadZipFile: raise GuardError(label+'_ZIP_INVALID')
def tree_check(root):
    d=load(root); b=d['released_baseline']; n=d['negative_baseline']; c=d['active_candidate']
    zipbytes_vs_manifest(root,b['artifact_chunks_ref'],b['installer_sha256'],b['source_manifest_ref'],b['source_manifest_sha256'],b['source_file_count'],'BASELINE')
    zipbytes_vs_manifest(root,n['artifact_chunks_ref'],n['sha256'],n['source_manifest_ref'],n['source_manifest_sha256'],n['source_file_count'],'NEGATIVE')
    zipbytes_vs_manifest(root,c['working_source_chunks_ref'],c['working_source_sha256'],c['current_source_manifest_ref'],c['current_source_manifest_sha256'],c['source_file_count'],'CURRENT')
    for ref in d.get('immutable_test_refs',[])+d.get('immutable_governance_refs',[]):
        if not (root/ref).is_file(): raise GuardError('IMMUTABLE_REF_MISSING:'+ref)
    if c.get('release_allowed') is True: release_check(root,d)
    print('AFFILIATE_RELEASE_TREE_PASS')
def release_check(root,d=None):
    d=d or load(root); c=d['active_candidate']; bad=[]
    for name,g in (d.get('required_release_gates') or {}).items():
        if not isinstance(g,dict) or g.get('status')!='PASS': bad.append(name); continue
        ref=g.get('evidence_ref'); dig=g.get('evidence_sha256')
        if not ref or not dig: raise GuardError('EVIDENCE_BINDING_MISSING:'+name)
        if not ref.startswith('release/affiliate-zentrale/evidence/'): raise GuardError('EVIDENCE_PATH_INVALID:'+name)
        vf(root,ref,dig,'EVIDENCE_'+name)
    if bad: raise GuardError('RELEASE_GATES_OPEN:'+','.join(bad))
    if c.get('release_allowed') is not True or c.get('status')!='RELEASED': raise GuardError('RELEASE_STATE_NOT_ALLOWED')
    ref=c.get('final_artifact_ref'); dig=c.get('final_artifact_sha256')
    if not ref or not dig or not ref.startswith('release/affiliate-zentrale/artifacts/final/'): raise GuardError('FINAL_ARTIFACT_BINDING_INVALID')
    p=vf(root,ref,dig,'FINAL_ARTIFACT')
    rows=manifest(root,c['current_source_manifest_ref'],c['current_source_manifest_sha256'],c['source_file_count'],'FINAL')
    try:
        with zipfile.ZipFile(p) as z:
            if sorted(n for n in z.namelist() if not n.endswith('/'))!=sorted(r for _,r in rows): raise GuardError('FINAL_ZIP_FILE_LIST')
            for h,r in rows:
                if sha256_bytes(z.read(r))!=h: raise GuardError('FINAL_ZIP_SOURCE_HASH:'+r)
    except zipfile.BadZipFile: raise GuardError('FINAL_ZIP_INVALID')
    print('AFFILIATE_RELEASE_FINAL_GATE_PASS')
def snapshot(root):
    out={}
    for p in root.rglob('*'):
        if p.is_file() and '.git' not in p.parts: out[p.relative_to(root).as_posix()]=sha256_file(p)
    return out
def changes(base,head):
    b=snapshot(base); h=snapshot(head); return sorted(set(b)^set(h)|{k for k in set(b)&set(h) if b[k]!=h[k]})
def starts(p,arr): return any(p.startswith(x) for x in arr)
def pr_check(base,head,head_ref,base_sha):
    bd=load(base); hd=load(head); ch=changes(base,head); sp=hd['scope_policy']; bp=hd['branch_policy']
    if int(hd.get('generation',0))<int(bd.get('generation',0)): raise GuardError('GOVERNANCE_ROLLBACK')
    for key in ('released_baseline','negative_baseline','immutable_snapshot_binding'):
        if hd[key]!=bd[key]: raise GuardError(key.upper()+'_MUTATION_BLOCKED')
    oldrefs=bd.get('immutable_test_refs',[])+bd.get('immutable_governance_refs',[]); newrefs=hd.get('immutable_test_refs',[])+hd.get('immutable_governance_refs',[])
    for ref in oldrefs:
        if ref not in newrefs: raise GuardError('IMMUTABLE_REF_LIST_WEAKENED:'+ref)
        if not (head/ref).is_file(): raise GuardError('IMMUTABLE_REF_REMOVAL_BLOCKED:'+ref)
        if (base/ref).is_file() and sha256_file(base/ref)!=sha256_file(head/ref): raise GuardError('IMMUTABLE_REF_MUTATION_BLOCKED:'+ref)
    scoped=[p for p in ch if starts(p,sp['release_scoped_prefixes']) or p=='control/release-governance/CURRENT_RELEASE.json' or p.startswith('protocol/AFFILIATE_RELEASE_')]
    if scoped and head_ref!=bp['active_work_branch']:
        b=bp['bootstrap']
        if not(head_ref==b['branch'] and base_sha==b['base_sha']): raise GuardError('WRONG_RELEASE_WORK_BRANCH:'+head_ref)
    if head_ref==bp['active_work_branch']:
        bad=[p for p in ch if starts(p,sp['forbidden_prefixes'])]
        if bad: raise GuardError('FORBIDDEN_PATH_CHANGE:'+','.join(bad))
        relevant=[p for p in ch if starts(p,sp['release_scoped_prefixes']) or p.startswith('control/release-governance/') or p.startswith('protocol/AFFILIATE_RELEASE_')]
        bad=[p for p in relevant if not starts(p,sp['allowed_active_branch_prefixes'])]
        if bad: raise GuardError('ACTIVE_BRANCH_SCOPE_VIOLATION:'+','.join(bad))
    tree_check(head); print('AFFILIATE_RELEASE_PR_GUARD_PASS')
def start(root,branch):
    d=load(root); active=d['branch_policy']['active_work_branch']
    if branch!=active: raise GuardError('WORK_BRANCH_REQUIRED:'+active)
    tree_check(root); print('AFFILIATE_RELEASE_START_PASS')
def main():
    ap=argparse.ArgumentParser(); s=ap.add_subparsers(dest='cmd',required=True)
    for n in ('tree-check','release-check'): p=s.add_parser(n); p.add_argument('--root',default='.')
    p=s.add_parser('start'); p.add_argument('--root',default='.'); p.add_argument('--branch',required=True)
    p=s.add_parser('pr-check'); p.add_argument('--base',required=True); p.add_argument('--head',required=True); p.add_argument('--head-ref',required=True); p.add_argument('--base-sha',required=True)
    a=ap.parse_args()
    try:
        if a.cmd=='tree-check': tree_check(pathlib.Path(a.root).resolve())
        elif a.cmd=='release-check': release_check(pathlib.Path(a.root).resolve())
        elif a.cmd=='start': start(pathlib.Path(a.root).resolve(),a.branch)
        else: pr_check(pathlib.Path(a.base).resolve(),pathlib.Path(a.head).resolve(),a.head_ref,a.base_sha)
    except GuardError as e: print('AFFILIATE_RELEASE_GUARD_BLOCKED:'+str(e),file=sys.stderr); return 2
    return 0
if __name__=='__main__': raise SystemExit(main())
