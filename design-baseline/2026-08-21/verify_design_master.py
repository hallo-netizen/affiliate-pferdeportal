#!/usr/bin/env python3
import argparse, hashlib, re, sys, tempfile, zipfile
from pathlib import Path


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open('rb') as f:
        for block in iter(lambda: f.read(1024 * 1024), b''):
            h.update(block)
    return h.hexdigest()


def tree_hashes(root: Path):
    return {str(p.relative_to(root)): sha256(p) for p in root.rglob('*') if p.is_file()}


def verify_manifest(root: Path):
    mf = root / 'MANIFEST_SHA256.txt'
    if not mf.exists():
        return False, ['MANIFEST_SHA256.txt fehlt']
    errors = []
    parsed = 0
    for raw in mf.read_text(errors='replace').splitlines():
        line = raw.strip()
        if not line or line.startswith('#'):
            continue
        m = re.match(r'^([0-9a-fA-F]{64})\s+[* ]?(.+)$', line)
        if not m:
            continue
        parsed += 1
        expected, rel = m.group(1).lower(), m.group(2).strip()
        p = root / rel
        if not p.exists():
            errors.append(f'MISSING {rel}')
        else:
            actual = sha256(p)
            if actual != expected:
                errors.append(f'HASH {rel} expected={expected} actual={actual}')
    if not parsed:
        errors.append('Manifest enthält keine parsebaren SHA-256-Zeilen')
    return not errors, errors


def inspect_zip_root(zip_path: Path):
    with zipfile.ZipFile(zip_path) as z:
        roots = sorted({n.split('/', 1)[0] for n in z.namelist() if n and not n.startswith('__MACOSX/')})
        return roots


def main():
    ap = argparse.ArgumentParser(description='Fail-closed Master/Installer/Source consistency guard')
    ap.add_argument('master_zip')
    args = ap.parse_args()
    master = Path(args.master_zip).resolve()
    if not master.is_file():
        print(f'BLOCKED: Datei fehlt: {master}', file=sys.stderr)
        return 2
    with tempfile.TemporaryDirectory(prefix='design-master-guard-') as td:
        root = Path(td)
        with zipfile.ZipFile(master) as z:
            bad = z.testzip()
            if bad:
                print(f'BLOCKED: ZIP CRC Fehler: {bad}', file=sys.stderr)
                return 2
            z.extractall(root)
        manifest_ok, manifest_errors = verify_manifest(root)
        if not manifest_ok:
            print('BLOCKED: Master-Manifest FAIL')
            for e in manifest_errors[:50]: print(' -', e)
            return 2
        source_parent = root / 'CURRENT_PLUGIN_SOURCE'
        installer_parent = root / 'INSTALLER'
        if not source_parent.is_dir() or not installer_parent.is_dir():
            print('BLOCKED: CURRENT_PLUGIN_SOURCE oder INSTALLER fehlt')
            return 2
        source_dirs = [p for p in source_parent.iterdir() if p.is_dir()]
        if not source_dirs:
            print('BLOCKED: Kein Pluginbaum in CURRENT_PLUGIN_SOURCE')
            return 2
        any_fail = False
        for src in source_dirs:
            candidates = []
            for zpath in installer_parent.glob('*.zip'):
                try:
                    roots = inspect_zip_root(zpath)
                except zipfile.BadZipFile:
                    continue
                if src.name in roots:
                    candidates.append(zpath)
            if len(candidates) != 1:
                print(f'BLOCKED: Für {src.name} wurden {len(candidates)} passende Installer gefunden')
                any_fail = True
                continue
            inst = candidates[0]
            with tempfile.TemporaryDirectory(prefix='design-installer-guard-') as itd:
                ir = Path(itd)
                with zipfile.ZipFile(inst) as z: z.extractall(ir)
                iroot = ir / src.name
                if not iroot.is_dir():
                    print(f'BLOCKED: Installerroot {src.name} fehlt in {inst.name}')
                    any_fail = True
                    continue
                A, B = tree_hashes(src), tree_hashes(iroot)
                only_src = sorted(set(A) - set(B))
                only_inst = sorted(set(B) - set(A))
                changed = sorted(k for k in set(A) & set(B) if A[k] != B[k])
                if only_src or only_inst or changed:
                    any_fail = True
                    print(f'BLOCKED: {src.name} CURRENT_PLUGIN_SOURCE != {inst.name}')
                    print(f'  source_files={len(A)} installer_files={len(B)} same={sum(1 for k in set(A)&set(B) if A[k]==B[k])}')
                    for k in only_src[:30]: print('  ONLY_SOURCE', k)
                    for k in only_inst[:30]: print('  ONLY_INSTALLER', k)
                    for k in changed[:30]: print('  CHANGED', k)
                else:
                    print(f'PASS: {src.name} source == installer ({len(A)}/{len(A)} byte-identisch)')
        if any_fail:
            return 2
        print(f'PASS: Master-Manifest und alle CURRENT_PLUGIN_SOURCE/Installer-Bäume konsistent: {master.name}')
        return 0

if __name__ == '__main__':
    raise SystemExit(main())
