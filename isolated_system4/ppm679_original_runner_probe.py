from __future__ import annotations

import hashlib
import json
import re
import shutil
import sys
import zipfile
from pathlib import Path

PACKAGE_REL=Path('control/startmaster0107/runtime_packages/PORTAL_PRODUCTION_MACHINE_V6.7.9_SIGNED_ARTICLE_TYPE_EXTENSION_ROOTFIX_FINAL.zip')
PACKAGE_SHA256='acbda93bd1c4292de7aaf88db2195631103991ff508b36c88cb694714818abd1'
FAILING=(
    'tests/test-canonical-runtime-binding.php',
    'tests/test-g9-faq-only-live-state-integration.php',
    'tests/test-historical-regressions.php',
    'tests/test-positive-pipeline.php',
    'tests/test-wave1-unsigned-quarantine-blocked.php',
    'tests/three-type-bundled-local/test-beratung-positive.php',
    'tests/three-type-bundled-local/test-bundled-overall-and-no-live.php',
    'tests/three-type-bundled-local/test-pflege-positive.php',
    'tests/three-type-bundled-local/test-release-gate-positive.php',
    'tests/three-type-bundled-local/test-signed-integration-traceability.php',
    'tests/three-type-bundled-local/test-signed-quarantine-boundaries.php',
    'tests/three-type-bundled-local/test-v38-baseline-byte-identity.php',
    'tests/three-type-bundled-local/test-vergleich-positive.php',
)
RUNNER_NAMES=('run','runner','test','tests','suite','phpunit','makefile','composer','readme')
TEXT_SUFFIXES={'.php','.sh','.json','.md','.txt','.yml','.yaml','.xml'}

class ProbeError(RuntimeError): pass

def sha(path:Path)->str:
    h=hashlib.sha256()
    with path.open('rb') as f:
        for block in iter(lambda:f.read(1024*1024),b''): h.update(block)
    return h.hexdigest()

def _read(path:Path,limit:int=24000)->str:
    raw=path.read_bytes()
    if len(raw)>limit: raw=raw[:limit]
    return raw.decode('utf-8','replace')

def _requires(text:str)->list[str]:
    out=[]
    for m in re.finditer(r"(?:require|require_once|include|include_once)\s*(?:\()?\s*([^;\n]+)",text):
        out.append(m.group(1).strip())
    return out

def main()->int:
    repo=Path(__file__).resolve().parent.parent
    package=repo/PACKAGE_REL
    if not package.is_file() or sha(package)!=PACKAGE_SHA256: raise ProbeError('PPM679_PACKAGE_IDENTITY_INVALID')
    root=Path('/tmp/system4-ppm679-runner-probe'); shutil.rmtree(root,ignore_errors=True); root.mkdir()
    with zipfile.ZipFile(package) as zf: zf.extractall(root)
    ppm=root/'portal-production-machine'
    if not ppm.is_dir(): raise ProbeError('PPM679_ROOT_MISSING')

    print('PPM679_RUNNER_PROBE_BEGIN')
    candidates=[]
    for p in ppm.rglob('*'):
        if not p.is_file() or p.suffix.casefold() not in TEXT_SUFFIXES: continue
        rel=p.relative_to(ppm).as_posix()
        folded=rel.casefold()
        if any(token in folded for token in RUNNER_NAMES):
            if p.stat().st_size<=200000:
                candidates.append(rel)
    for rel in sorted(candidates):
        p=ppm/rel
        text=_read(p,12000)
        # Only print files that plausibly orchestrate/bootstrap tests or define signed test state.
        folded=text.casefold()
        if any(token in folded for token in ('bootstrap','test-', 'php ', 'signed', 'baseline', 'manifest', 'preflight')):
            print('PPM679_RUNNER_CANDIDATE_BEGIN='+rel)
            print(text)
            print('PPM679_RUNNER_CANDIDATE_END='+rel)

    for rel in FAILING:
        p=ppm/rel
        if not p.is_file(): raise ProbeError('PPM679_FAILING_TEST_MISSING:'+rel)
        text=_read(p)
        print('PPM679_FAILING_TEST_BEGIN='+rel)
        print(text)
        print('PPM679_REQUIRE_EXPRESSIONS='+json.dumps(_requires(text),ensure_ascii=False))
        print('PPM679_FAILING_TEST_END='+rel)
        # Print nearby bootstrap files from the same directory and parents up to tests/.
        d=p.parent
        seen=set()
        while d!=ppm.parent and ppm in d.parents or d==ppm:
            for name in ('bootstrap-test.php','bootstrap-live-test.php','bootstrap.php','test-bootstrap.php','bootstrap-bundled.php'):
                q=d/name
                if q.is_file() and q not in seen:
                    seen.add(q)
                    qrel=q.relative_to(ppm).as_posix()
                    print('PPM679_BOOTSTRAP_BEGIN='+qrel)
                    print(_read(q))
                    print('PPM679_BOOTSTRAP_END='+qrel)
            if d==ppm or d.name=='tests': break
            d=d.parent
    print('PPM679_RUNNER_PROBE_END')
    return 0

if __name__=='__main__':
    try: raise SystemExit(main())
    except (ProbeError,OSError,ValueError,zipfile.BadZipFile) as exc:
        print('PPM679_RUNNER_PROBE_FAIL:'+str(exc),file=sys.stderr)
        raise SystemExit(2)
