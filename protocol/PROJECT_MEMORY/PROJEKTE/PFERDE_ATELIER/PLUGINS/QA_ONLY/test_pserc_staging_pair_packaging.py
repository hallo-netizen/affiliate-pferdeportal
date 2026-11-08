#!/usr/bin/env python3
"""One-time QA original PSERC 0.28.53 vs exact 0.28.54 test copy.
Run with two ORIGINAL ZIP files; no WordPress, K0, plan or production action.
"""
import hashlib
import pathlib
import subprocess
import sys
import tempfile
from zipfile import ZipFile

ORIGINAL_HASH='80340faff2323e5ede86ddd095ac3570a53474ae64771df3bec70fb6f6c6f060'
QA_HASH='2c31ae1bf89613abf456576039f9bd52ef6ed41c1f84c28fd0c57410846033a1'
ROOT='portal-seo-editorial-plan-compiler/'
MODIFIED={ROOT+name for name in (
    'includes/class-pserc-seo-reader.php',
    'includes/class-pserc-compiler.php',
    'includes/class-pserc-plan-compile-job.php',
    'portal-seo-editorial-plan-compiler.php',
    'contracts/compiler-package-binding-v1.json')}

def verify(original: pathlib.Path, qa: pathlib.Path) -> None:
    for f, expected in ((original, ORIGINAL_HASH), (qa, QA_HASH)):
        actual=hashlib.sha256(f.read_bytes()).hexdigest()
        if actual!=expected: raise RuntimeError(f'FAIL {f}: expected {expected}, got {actual}')
        print('PASS exact original/test package SHA256',f.name,actual)
    with ZipFile(original) as before, ZipFile(qa) as after:
        assert before.testzip() is None and after.testzip() is None, 'Damaged ZIP'
        a=set(after.namelist());b=set(before.namelist())
        assert a==b and len(a)==63, ('ORIGINAL_PATHS_CHANGED',len(b),len(a),a^b)
        changed={n for n in a if before.read(n)!=after.read(n)}
        assert changed==MODIFIED, ('UNEXPECTED_PLUGIN_CHANGE',changed^MODIFIED)
        print('PASS 63 original files; only 3 existing PHP classes, main version and package binding differ')
        with tempfile.TemporaryDirectory() as temp:
            after.extractall(temp)
            php=sorted(pathlib.Path(temp).rglob('*.php'))
            assert len(php)==43, ('PHP_SOURCE_COUNT_CHANGED',len(php))
            for f in php:
                run=subprocess.run(['php','-l',str(f)],capture_output=True,text=True)
                if run.returncode: raise RuntimeError('INVALID PHP '+str(f)+run.stderr)
            print('PASS 43/43 PSERC PHP syntax')
    print('REAL_PSERC_EXACT_QA_PAIR_SCOPE_PASS; NOT WORDPRESS_STAGING_PASS')

if __name__=='__main__':
    if len(sys.argv)!=3: raise SystemExit('Usage: test_pserc_staging_pair_packaging.py ORIGINAL_0.28.53.zip QA_0.28.54.zip')
    verify(pathlib.Path(sys.argv[1]),pathlib.Path(sys.argv[2]))
