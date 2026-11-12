#!/usr/bin/env python3
"""Rebuild isolated PSTE .25 QA source from original .24 ZIP and the reviewed patch.
No WordPress connection, DB changes, K0 writes or original ZIP mutation.
"""
from pathlib import Path
import hashlib, shutil, subprocess, zipfile
old=Path('/mnt/data/PSTE-0.57.144.24-PARKHAUS-QUELLFIX-NUR-TEST.zip')
patch=Path('/mnt/data/PSTE_05714424_to_05714425_QUELLEN_IDENTITAET_KISS.patch')
root=Path('/mnt/data/work_pste_05714425')
if root.exists():shutil.rmtree(root)
root.mkdir(parents=True)
with zipfile.ZipFile(old) as z:
    if z.testzip() is not None:raise RuntimeError('SOURCE_ZIP_CRC_FAILED')
    z.extractall(root)
# GNU patch requires quoted paths because the established WordPress plugin
# folder contains spaces; this fixes only the patch-file headers, not content.
quoted=[]
for line in patch.read_text(encoding='utf8').splitlines(keepends=True):
    if line.startswith(('--- a/Portal SEO Topic Engine/','+++ b/Portal SEO Topic Engine/')):
        line=line[:4]+'"'+line[4:].rstrip('\n')+'"\n'
    quoted.append(line)
quotedPatch=root/'qa_external.patch'
quotedPatch.write_text(''.join(quoted),encoding='utf8')
proc=subprocess.run(['patch','-p1','--batch','-i',str(quotedPatch)],cwd=root,capture_output=True,text=True)
if proc.returncode:raise RuntimeError(proc.stdout+'\n'+proc.stderr)
quotedPatch.unlink()
php=sorted((root/'Portal SEO Topic Engine').rglob('*.php'))
assert len(php)==83,len(php)
for f in php:
    z=subprocess.run(['php','-l',str(f)],capture_output=True,text=True)
    if z.returncode:raise RuntimeError(z.stdout+'\n'+z.stderr)
assert b'0.57.144.25' in (root/'Portal SEO Topic Engine/portal-seo-topic-engine.php').read_bytes()
print('PASS',len(php),'PHP files rebuilt and linted from exact v24+patch sources')