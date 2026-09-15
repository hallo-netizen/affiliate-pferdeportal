from __future__ import annotations
import io, re, zipfile
from pathlib import Path

REPO=Path(__file__).resolve().parent.parent
OUTER=REPO/'control/startmaster0107/runtime_packages/PSERC-FIX.zip'
TOKENS=('PSERC_SYSTEM4','SYSTEM4_','CONTRACT_INVALID','contract','ENDSTEMPEL','import')

def scan_zip(raw:bytes,label:str)->None:
    with zipfile.ZipFile(io.BytesIO(raw)) as z:
        for name in z.namelist():
            if name.lower().endswith('.zip'):
                try: scan_zip(z.read(name),label+'!'+name)
                except zipfile.BadZipFile: pass
                continue
            if not name.lower().endswith(('.php','.json','.md','.txt')): continue
            try: text=z.read(name).decode('utf-8')
            except Exception: continue
            if not any(t.casefold() in text.casefold() for t in TOKENS): continue
            hits=[]
            for n,line in enumerate(text.splitlines(),1):
                folded=line.casefold()
                if any(t.casefold() in folded for t in TOKENS):
                    hits.append((n,line.strip()))
            important=[row for row in hits if any(t.casefold() in row[1].casefold() for t in ('PSERC_SYSTEM4','SYSTEM4_','CONTRACT_INVALID','ENDSTEMPEL'))]
            if important:
                print('FILE',label+'!'+name)
                for n,line in important[:120]: print(f'{n}: {line[:500]}')

def main()->int:
    if not OUTER.is_file(): raise SystemExit('PSERC_FIX_MISSING')
    scan_zip(OUTER.read_bytes(),OUTER.name)
    return 0

if __name__=='__main__': raise SystemExit(main())
