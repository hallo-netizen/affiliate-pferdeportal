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
    'pste_plugin_office_source': '/Campus-Plugins/PFERDE_ATELIER/PPA-005/CURRENT.zip',
    'pste_current_source_version': '0.57.164',
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
    for key in ('pste_current_source_sha256', 'pste_approved_delta_sha256'):
        if not re.fullmatch('[0-9a-f]{64}', str(lock.get(key, ''))):
            fail('Plugin-Buero-Original oder genehmigtes Delta nicht eindeutig gebunden: ' + key)
    return lock



def zip_content(path):
    """One technical integrity reader, never an editorial/worker decision."""
    if not path.is_file():
        fail('Original- oder Kandidaten-ZIP physisch nicht erreichbar: ' + str(path))
    with ZipFile(path) as archive:
        names = archive.namelist()
        if len(names) != len(set(names)):
            fail('Doppelte Datei im Plugin-Archiv')
        if any(name.startswith('/') or '..' in Path(name).parts for name in names):
            fail('Unzulaessige Archivpfade')
        if archive.testzip() is not None:
            fail('Beschaedigte Plugin-ZIP')
        return {name: archive.read(name) for name in names if not name.endswith('/')}


def check_plugin_office_origin(original, candidate, delta, lock):
    """Fail closed: never reconstruct a plugin from older source or a report."""
    if not original.is_file():
        fail('Plugin-Buero-Original fehlt; kein Ersatz aus Altversionen: '
             + lock['pste_plugin_office_source'])
    if digest(original.read_bytes()) != lock['pste_current_source_sha256']:
        fail('Original im Plugin-Buero nicht die gebundene komplette 0.57.164-ZIP')
    if not delta.is_file() or digest(delta.read_bytes()) != lock['pste_approved_delta_sha256']:
        fail('Genehmigter Drei-Dateien-Patch fehlt oder ist veraendert')
    base = zip_content(original)
    final = zip_content(candidate)
    if set(base) != set(final):
        fail('Plugin-Dateisatz geaendert; keine neuen oder fehlenden Dateien erlaubt')
    roots = [name[:-len('portal-seo-topic-engine.php')]
             for name in base if name.endswith('/portal-seo-topic-engine.php')]
    if len(roots) != 1:
        fail('Original-Pluginstruktur nicht eindeutig')
    root = roots[0]
    approved = {
        root + 'includes/class-pste-admin.php',
        root + 'includes/class-pste-planning-readiness-gate.php',
        root + 'includes/class-pste-repository.php',
    }
    main_php = root + 'portal-seo-topic-engine.php'
    if any(name not in base for name in approved):
        fail('Genehmigte Originaldatei fehlt')
    if not (b'0.57.164' in base[main_php]
            and final[main_php] == base[main_php].replace(b'0.57.164', b'0.57.165')):
        fail('Plugin-Versionsdatei nicht ausschliesslich von 0.57.164 auf 0.57.165 geaendert')
    other_changes = [name for name in base if name not in approved and name != main_php
                     and base[name] != final[name]]
    if other_changes:
        fail('Unzulaessige Aenderungen gegenueber Original: ' + ', '.join(other_changes[:5]))
    # Independently apply the one already approved patch to real source bytes.
    # This is a temporary comparison only, not a new plugin build.
    with tempfile.TemporaryDirectory(prefix='pferdeatelier-origin-') as tmp:
        with ZipFile(original) as archive:
            archive.extractall(tmp)
        proc = subprocess.run(
            ['patch', '-p1', '--batch', '--fuzz=0', '--input', str(delta.resolve())],
            cwd=tmp, capture_output=True, text=True, timeout=60, check=False)
        if proc.returncode != 0:
            fail('Delta passt nicht exakt zum 0.57.164-Original: '
                 + (proc.stderr + proc.stdout)[-450:])
        for name in approved:
            expected = (Path(tmp) / name).read_bytes()
            if expected != final[name]:
                fail('Kandidat weicht vom genehmigten Delta ab: ' + name)
    print('PLUGIN_BUERO_ORIGINAL_PASS; GENEHMIGTES_DELTA_PASS; ALLE_DATEIEN_PASS;'
          ' WP_E2E_OFFEN; RELEASE_BLOCKED')

def main():
    parser = argparse.ArgumentParser(description='Nur die einzige in CURRENT_STATE gebundene QA-Fassung prüfen')
    parser.add_argument('--current', required=True, type=Path)
    parser.add_argument('--artifact', type=Path)
    parser.add_argument('--release', action='store_true', help='Sperre ohne echten Original-Endlauf (kein Installer)')
    parser.add_argument('--metadata-only', action='store_true', help='Nur den eindeutigen Current-Lock für GitHub prüfen')
    parser.add_argument('--plugin-original', type=Path, help='Echtes Original aus PPA-005/CURRENT.zip')
    parser.add_argument('--plugin-candidate', type=Path, help='Neues vollstaendiges Staging-Paket')
    parser.add_argument('--plugin-delta', type=Path, help='Eine gebundene Drei-Dateien-Korrektur')
    args = parser.parse_args()
    lock = load_lock(args.current)
    if args.release:
        fail('Nur QA-Arbeitsfassung; kein vollständiger Original-E2E-/WordPress-Entwurf-PASS')
    if args.metadata_only:
        print('SINGLE_CURRENT_METADATA_ONLY_OK; EXTERNAL_ORIGINAL_ZIP_NOT_READ; RELEASE_BLOCKED')
        return
    plugin_flags = (args.plugin_original, args.plugin_candidate, args.plugin_delta)
    if any(item is not None for item in plugin_flags):
        if not all(item is not None for item in plugin_flags) or args.artifact is not None:
            fail('Original, Kandidat und genehmigtes Delta muessen gemeinsam vorliegen')
        check_plugin_office_origin(*plugin_flags, lock)
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