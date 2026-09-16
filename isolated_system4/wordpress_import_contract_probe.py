from __future__ import annotations
import io, re, zipfile
from pathlib import Path

REPO=Path(__file__).resolve().parent.parent
OUTER=REPO/'control/startmaster0107/runtime_packages/PSERC-FIX.zip'
TOKENS=('PSERC_SYSTEM4','SYSTEM4_','CONTRACT_INVALID','contract','ENDSTEMPEL','import')
DIAG_TOKENS=('article_count','item_count','articles','manifest','ENDSTAMP_CONTRACT','PACKAGE_CONTRACT')
EXPECTED_BUILD='0.28.18-endstempel-import-envelope-binding-ppm679'
EXPECTED_ENDSTAMP_CONTRACT='PFERDE_ATELIER_ENDSTEMPEL_RELEASE_V1'
FORBIDDEN_DIRECT_HANDOFF_CONTRACT='SYSTEM4_ARTICLE_BATCH_CHAT_HANDOFF_V2'

def scan_zip(raw:bytes,label:str,evidence:list[str])->None:
    with zipfile.ZipFile(io.BytesIO(raw)) as z:
        for name in z.namelist():
            if name.lower().endswith('.zip'):
                try: scan_zip(z.read(name),label+'!'+name,evidence)
                except zipfile.BadZipFile: pass
                continue
            if not name.lower().endswith(('.php','.json','.md','.txt')): continue
            try: text=z.read(name).decode('utf-8')
            except Exception: continue
            evidence.append(text)
            if not any(t.casefold() in text.casefold() for t in TOKENS+DIAG_TOKENS): continue
            hits=[]
            for n,line in enumerate(text.splitlines(),1):
                folded=line.casefold()
                if any(t.casefold() in folded for t in TOKENS+DIAG_TOKENS):
                    hits.append((n,line.strip()))
            important=[row for row in hits if any(t.casefold() in row[1].casefold() for t in ('PSERC_SYSTEM4','SYSTEM4_','CONTRACT_INVALID','ENDSTEMPEL','article_count','item_count','manifest','PACKAGE_CONTRACT'))]
            if important:
                print('FILE',label+'!'+name)
                for n,line in important[:180]: print(f'{n}: {line[:700]}')

def main()->int:
    if not OUTER.is_file(): raise SystemExit('PSERC_FIX_MISSING')
    evidence=[]
    scan_zip(OUTER.read_bytes(),OUTER.name,evidence)
    joined='\n'.join(evidence)
    if EXPECTED_BUILD not in joined:
        raise SystemExit('WORDPRESS_IMPORT_BUILD_NOT_FOUND:'+EXPECTED_BUILD)
    if re.search(r"ENDSTAMP_CONTRACT\s*=\s*['\"]"+re.escape(EXPECTED_ENDSTAMP_CONTRACT)+r"['\"]",joined) is None:
        raise SystemExit('WORDPRESS_ENDSTAMP_CONTRACT_NOT_FOUND:'+EXPECTED_ENDSTAMP_CONTRACT)
    if FORBIDDEN_DIRECT_HANDOFF_CONTRACT in joined:
        raise SystemExit('WORDPRESS_RAW_SYSTEM4_V2_DIRECT_IMPORT_UNEXPECTED')
    print('SYSTEM4_WORDPRESS_IMPORTER_BUILD_BOUND='+EXPECTED_BUILD)
    print('SYSTEM4_WORDPRESS_ENDSTEMPEL_CONTRACT_BOUND='+EXPECTED_ENDSTAMP_CONTRACT)
    print('SYSTEM4_WORDPRESS_RAW_V2_DIRECT_IMPORT_BLOCK_PROVEN='+FORBIDDEN_DIRECT_HANDOFF_CONTRACT)
    return 0

if __name__=='__main__': raise SystemExit(main())
