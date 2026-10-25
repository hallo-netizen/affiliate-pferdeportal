#!/usr/bin/env python3
"""Fail-closed QA guard for the existing Pferdeatelier plugin workbench.

No source generation, no WordPress access, no release.
"""
import argparse
import hashlib
import json
from pathlib import Path
import re
import subprocess
import sys
import tempfile
from zipfile import ZipFile

BEGIN = '<!-- PFERDEATELIER_PLUGIN_WORKBENCH_LOCK_BEGIN -->'
END = '<!-- PFERDEATELIER_PLUGIN_WORKBENCH_LOCK_END -->'
REQUIRED = {
    'contract': 'PFERDEATELIER_SINGLE_WORKBENCH_LOCK_V1',
    'scope': 'PFERDE_ATELIER_PLUGINS',
    'artifact_kind': 'QA_ONLY_NOT_AN_INSTALLER',
    'e2e_status': 'NOT_PASSED',
    'release_allowed': False,
}
ORIGINALS = {
    'PSTE_ORIGINAL_0.57.118.zip': 'pste_sha256',
    'PSERC_ORIGINAL_0.28.42.zip': 'pserc_sha256',
}


def fail(message):
    print('BLOCKED: ' + message, file=sys.stderr)
    raise SystemExit(1)


def digest(data):
    return hashlib.sha256(data).hexdigest()


def load_lock(path):
    body = path.read_text(encoding='utf-8')
    if body.count(BEGIN) != 1 or body.count(END) != 1:
        fail('Aktive Bindung fehlt oder mehrfach vorhanden; keine alte Fassung suchen')
    raw = body.split(BEGIN, 1)[1].split(END, 1)[0].strip()
    if not raw.startswith('```json\n') or not raw.endswith('\n```'):
        fail('Aktive Bindung ist kein eindeutiger JSON-Block')
    try:
        lock = json.loads(raw[len('```json\n'):-len('\n```')])
    except (ValueError, TypeError) as exc:
        fail('Aktive Bindung ungültig: ' + str(exc))
    for key, value in REQUIRED.items():
        if lock.get(key) != value:
            fail('Lock-Vertrag verletzt: ' + key)
    for key in ('artifact_name', 'artifact_sha256', 'pste_sha256', 'pserc_sha256'):
        if not isinstance(lock.get(key), str) or not lock[key]:
            fail('Pflichtbindung fehlt: ' + key)
    if not re.fullmatch('[0-9a-f]{64}', lock['artifact_sha256']):
        fail('QA-Prüfsumme ist ungültig')
    if not all(re.fullmatch('[0-9a-f]{64}', lock[key]) for key in ('pste_sha256','pserc_sha256')):
        fail('Original-Prüfsummen sind ungültig')
    if Path(lock['artifact_name']).name != lock['artifact_name']:
        fail('Arbeitsfassung muss ein einzelner ZIP-Dateiname sein')
    return lock


def main():
    parser = argparse.ArgumentParser(description='Nur die einzige in CURRENT_STATE gebundene QA-Fassung prüfen')
    parser.add_argument('--current', required=True, type=Path)
    parser.add_argument('--artifact', type=Path)
    parser.add_argument('--release', action='store_true', help='Sperre ohne echten Original-Endlauf (kein Installer)')
    parser.add_argument('--metadata-only', action='store_true', help='Nur den eindeutigen Current-Lock für GitHub prüfen')
    args = parser.parse_args()
    lock = load_lock(args.current)
    if args.release:
        fail('Nur QA-Arbeitsfassung; kein vollständiger Original-E2E-/WordPress-Entwurf-PASS')
    if args.metadata_only:
        print('SINGLE_CURRENT_LOCK_OK; RELEASE_BLOCKED')
        return
    if args.artifact is None:
        fail('Genau die aktuelle QA-ZIP muss über --artifact vorliegen')
    if args.artifact.name != lock['artifact_name']:
        fail('Alte oder andere ZIP erkannt: ' + args.artifact.name)
    if not args.artifact.is_file():
        fail('Gebundene aktuelle ZIP physisch nicht vorhanden')
    if digest(args.artifact.read_bytes()) != lock['artifact_sha256']:
        fail('Datei verändert oder veraltet; QA-ZIP-SHA passt nicht zur Current-Autorität')
    with ZipFile(args.artifact) as archive:
        names = archive.namelist()
        if len(names) != len(set(names)):
            fail('Mehrdeutige doppelte ZIP-Einträge')
        if any(name.startswith('/') or '..' in Path(name).parts for name in names):
            fail('Unzulässiger ZIP-Pfad')
        if archive.testzip() is not None:
            fail('ZIP-Inhalt beschädigt')
        for filename, key in ORIGINALS.items():
            name = 'ORIGINAL_ZIPS/' + filename
            if name not in names or digest(archive.read(name)) != lock[key]:
                fail('Originalpaket stimmt nicht: ' + filename)
        if 'ERGEBNIS.json' not in names or 'REPRODUZIEREN.sh' not in names:
            fail('Reproduktionsbeleg fehlt')
        report = json.loads(archive.read('ERGEBNIS.json'))
        if report.get('package_type') != 'QA_BEWEIS_KEIN_INSTALLER':
            fail('Falsche Artefaktrolle')
        deltas = {name.removeprefix('DELTA/') for name in names if name.startswith('DELTA/') and not name.endswith('/')}
        recorded = {entry['path'] for entry in report.get('changed_files', [])}
        if not deltas or deltas != recorded:
            fail('Quelldeltas weichen von der vollständigen Änderungsliste ab')
        with tempfile.TemporaryDirectory(prefix='pferdeatelier-qa-') as tmp:
            archive.extractall(tmp)
            check = subprocess.run(['bash', 'REPRODUZIEREN.sh'], cwd=tmp, text=True,
                                   capture_output=True, timeout=240, check=False)
            if check.returncode:
                print(check.stdout[-2000:], file=sys.stderr)
                print(check.stderr[-2000:], file=sys.stderr)
                fail('Unveränderter Original-QA-Gesamtreplay fehlgeschlagen')
            if 'FULL_K0_PPM_WP_DRAFT_E2E=NOT_EXECUTED; RELEASE=BLOCKED' not in check.stdout:
                fail('Gesamttest-Status wurde nicht korrekt offengelegt')
    print('AKTIVE_QA_KONSISTENT; ORIGINAL_SHA_PASS; REPLAY_PASS; E2E_OFFEN; RELEASE_BLOCKED')


if __name__ == '__main__':
    main()