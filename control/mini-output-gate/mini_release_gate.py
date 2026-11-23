#!/usr/bin/env python3
"""MINI release gate: ONE technical output checkpoint, with REWORK not reset.

No SEO, category or editorial redecisions. Those remain with their MINI workers.
The existing TITLE repair path now also blocks mechanically obvious filler and punctuation
for NEW titles only; no title is rewritten by this gate.
Every failure produces a repair ticket and leaves the same batch resumable.
"""
from __future__ import annotations
import argparse
import hashlib
import json
import os
import re
import shutil
import sys
from pathlib import Path

STAGES = ('CATEGORY', 'EDITORIAL', 'TITLE')
STAGE_FIELDS = {
    'CATEGORY': ('route', 'category_slug', 'article_type'),
    'EDITORIAL': ('box', 'intent_summary', 'matched_ref', 'reason'),
    'TITLE': ('approved_title',),
}
ORIGINAL = 'ORIGINAL_MINI.json'
RELEASE = 'FREIGABE'
REPAIR = 'REPARATUR.json'
STATUS = 'STAND.json'
ORIGINAL_HASH = 'ORIGINAL_SHA256.txt'


def read(path):
    return json.loads(path.read_text(encoding='utf-8'))


def write(path, data):
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_name('.' + path.name + '.tmp')
    tmp.write_text(json.dumps(data, indent=2, ensure_ascii=False) + '\n', encoding='utf-8')
    os.replace(tmp, path)


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def val(v):
    return isinstance(v, str) and bool(v.strip())


def new_title_rule_error(title, article_type=''):
    """Objective checks for NEW titles; original TITLE worker owns language."""
    if not val(title):
        return 'ENDGUELTIGER_TITEL_FEHLT'
    title = title.strip()
    if len(title) < 8 or len(title) > 110:
        return 'TITEL_LAENGE_UNZULAESSIG'
    # Natural words, spaces, commas and (at most) a terminal question mark.
    if re.search(r'[^\w\s,?]', title, re.UNICODE) or '_' in title:
        return 'TITEL_SONDERZEICHEN_UNZULAESSIG'
    if title.count('?') > 1 or ('?' in title and not title.endswith('?')):
        return 'TITEL_FRAGEZEICHEN_UNZULAESSIG'
    if article_type.strip().casefold() == 'faq' and not title.endswith('?'):
        return 'FAQ_TITEL_FRAGEZEICHEN_FEHLT'
    # Only mechanical, hollow ending patterns. Do not ban verbs globally.
    if re.search(
        r'\b(?:richtig|sachlich|korrekt|passend|gezielt|bedarfsgerecht|sorgfältig)'
        r'\s+(?:(?:dosiert|ausgerichtet)\s+)?(?:einordnen|auswählen)\s*\??def init(original, workspace):
    workspace.mkdir(parents=True, exist_ok=True)
    target = workspace / ORIGINAL
    if target.exists():
        if sha(original) != sha(target):
            raise ValueError('Anderer MINI-Auftrag im Arbeitsraum; alten Auftrag nicht überschreiben.')
    else:
        shutil.copyfile(original, target)
    digest_file = workspace / ORIGINAL_HASH
    if digest_file.exists():
        if digest_file.read_text(encoding='utf-8').strip() != sha(target):
            raise ValueError('Ursprünglicher MINI-Auftrag wurde verändert')
    else:
        digest_file.write_text(sha(target) + '\n', encoding='utf-8')
    return gate(workspace)


def gate(workspace):
    if not (workspace / ORIGINAL).is_file():
        raise ValueError(f'{ORIGINAL} fehlt')
    digest_file = workspace / ORIGINAL_HASH
    if not digest_file.is_file() or digest_file.read_text(encoding='utf-8').strip() != sha(workspace / ORIGINAL):
        raise ValueError('Original ist nicht unverändert hashgebunden; Auftrag nicht freigeben')
    source = read(workspace / ORIGINAL)
    items = source.get('items', [])
    if source.get('contract') != 'TEXTERSTELLUNG_SINGLE_EDITOR_BATCH_V1' or not items:
        raise ValueError('Originalauftrag fehlt oder ist kein MINI-Gesamtauftrag')
    if len(items) != len(source.get('resume_checkpoints', [])):
        raise ValueError('Originalauftrag: Themen/Checkpoints widersprechen sich')
    if source.get('checkpoint_contract') != 'TEXTERSTELLUNG_MINI_CHECKPOINT_V1':
        raise ValueError('Nicht unterstützter Original-MINI-Vertrag')

    problems = []
    loaded = {}
    batch_id, source_hash = source.get('batch_id'), source.get('source_sha256')

    def issue(stage, index, field, code):
        problems.append({'stage': stage, 'item_index': index,
                         'keyword': items[index].get('raw_query', '') if index is not None else '',
                         'field': field, 'code': code})

    # Single technical completeness check, once before release. No subject-matter rechecking.
    for stage in STAGES:
        path = workspace / (stage + '.json')
        if not path.exists():
            continue
        try:
            data = read(path)
        except (json.JSONDecodeError, UnicodeDecodeError) as exc:
            issue(stage, None, 'file', 'JSON_UNLESBAR: ' + str(exc))
            continue
        if (data.get('contract') != source['contract'] or
            data.get('checkpoint_contract') != source['checkpoint_contract'] or
            data.get('batch_id') != batch_id or
            data.get('source_sha256') != source_hash or
            data.get('checkpoint_stage') != stage):
            issue(stage, None, 'header', 'BATCH_ODER_STUFE_FALSCH')
            continue
        rows = data.get('items')
        if not isinstance(rows, list) or len(rows) != len(items):
            issue(stage, None, 'items', 'NICHT_ALLE_ORIGINALTHEMEN')
            continue
        mismatches = []
        for i, (original, actual) in enumerate(zip(items, rows)):
            if not isinstance(actual, dict) or any(actual.get(k) != v for k, v in original.items()):
                issue(stage, i, 'source', 'AUSGANGSDATEN_ODER_REIHENFOLGE_VERAENDERT')
                mismatches.append(i)
        if not mismatches:
            loaded[stage] = rows

    for i, (original, cp) in enumerate(zip(items, source['resume_checkpoints'])):
        next_step = cp.get('next')
        if next_step == 'DONE':
            for st in STAGES:
                if st in loaded and any(val(loaded[st][i].get(k)) for k in STAGE_FIELDS[st]):
                    issue(st, i, 'locked_decision', 'BEREITS_ABGESCHLOSSENE_ENTSCHEIDUNG_WIEDERHOLT')
            continue
        cat = cp.get('category')
        if cat and 'CATEGORY' in loaded:
            if any(val(loaded['CATEGORY'][i].get(k)) for k in STAGE_FIELDS['CATEGORY']):
                issue('CATEGORY', i, 'locked_category', 'ABGESCHLOSSENE_KATEGORIE_ERNEUT_ENTSCHIEDEN')
        if not cat:
            if 'CATEGORY' not in loaded:
                issue('CATEGORY', i, 'file', 'KATEGORIE_DATEI_FEHLT')
                continue
            cat = {k: loaded['CATEGORY'][i].get(k) for k in STAGE_FIELDS['CATEGORY']}
            if cat['route'] not in ('FACH', 'MAGAZIN', 'REDAKTIONSBUERO'):
                issue('CATEGORY', i, 'route', 'KATEGORIE_ENTSCHEIDUNG_FEHLT')
                continue
            if cat['route'] in ('FACH', 'MAGAZIN') and not (val(cat['category_slug']) and val(cat['article_type'])):
                issue('CATEGORY', i, 'category_slug/article_type', 'KATEGORIE_UNVOLLSTAENDIG')
                continue
        if original.get('mode') == 'LEGACY_CATEGORY_ONLY':
            continue  # genuine final stage; no re-decision

        editorial = cp.get('editorial')
        if editorial and 'EDITORIAL' in loaded:
            if any(val(loaded['EDITORIAL'][i].get(k)) for k in STAGE_FIELDS['EDITORIAL']):
                issue('EDITORIAL', i, 'locked_editorial', 'ABGESCHLOSSENE_REDAKTION_ERNEUT_ENTSCHIEDEN')
        if not editorial:
            if 'EDITORIAL' not in loaded:
                issue('EDITORIAL', i, 'file', 'REDAKTION_DATEI_FEHLT')
                continue
            editorial = {k: loaded['EDITORIAL'][i].get(k) for k in STAGE_FIELDS['EDITORIAL']}
            box = editorial['box']
            if box not in ('FREI', 'BELEGT', 'KLAERUNG'):
                issue('EDITORIAL', i, 'box', 'REDAKTIONSENTSCHEIDUNG_FEHLT')
                continue
            if box == 'FREI' and not val(editorial['intent_summary']):
                issue('EDITORIAL', i, 'intent_summary', 'SUCHABSICHT_FEHLT')
                continue
            if box == 'BELEGT' and not val(editorial['matched_ref']):
                issue('EDITORIAL', i, 'matched_ref', 'BESTANDSREFERENZ_FEHLT')
                continue
            if box == 'KLAERUNG' and not val(editorial['reason']):
                issue('EDITORIAL', i, 'reason', 'KLÄRUNGSGRUND_FEHLT')
                continue
        if cp.get('title') and 'TITLE' in loaded:
            if val(loaded['TITLE'][i].get('approved_title')):
                issue('TITLE', i, 'locked_title', 'ABGESCHLOSSENER_TITEL_ERNEUT_ENTSCHIEDEN')
        if editorial.get('box') == 'FREI' and not cp.get('title'):
            if 'TITLE' not in loaded:
                issue('TITLE', i, 'file', 'TITEL_DATEI_FEHLT')
                continue
            title = loaded['TITLE'][i].get('approved_title')
            if not val(title):
                issue('TITLE', i, 'approved_title', 'ENDGUELTIGER_TITEL_FEHLT')
            else:
                fault = new_title_rule_error(title, str(cat.get('article_type') or ''))
                if fault:
                    issue('TITLE', i, 'approved_title', fault)

    release = workspace / RELEASE
    if problems:
        # Rework: keep original and all worker outputs; remove only stale releases.
        if release.exists():
            shutil.rmtree(release)
        problems.sort(key=lambda e: (STAGES.index(e['stage']), e['item_index'] if e['item_index'] is not None else -1))
        ticket = {
            'contract': 'MINI_EINE_ABSCHLUSSPRUEFUNG_REWORK_V1',
            'batch_id': batch_id,
            'status': 'REPARATUR',
            'completed_decisions_are_locked': True,
            'restart_research': False,
            'next_worker': problems[0]['stage'],
            'fix_only': problems,
            'continue_with': 'Korrigierte Worker-Datei am selben Pfad ablegen, danach denselben gate-Befehl erneut ausführen.',
        }
        write(workspace / REPAIR, ticket)
        write(workspace / STATUS, {'status': 'REPARATUR', 'batch_id': batch_id,
                                   'pending': len(problems), 'release_available': False})
        return ticket

    # Publish approved files only after the ONE final technical check passes.
    temp = workspace / ('.' + RELEASE + '.tmp')
    if temp.exists():
        shutil.rmtree(temp)
    temp.mkdir(parents=True)
    released = []
    for stage in STAGES:
        path = workspace / (stage + '.json')
        if stage in loaded:
            dst = temp / path.name
            shutil.copyfile(path, dst)
            released.append({'stage': stage, 'name': dst.name, 'sha256': sha(dst)})
    write(temp / 'NACHWEIS.json', {
        'contract': 'MINI_EINE_ABSCHLUSSPRUEFUNG_REWORK_V1',
        'batch_id': batch_id,
        'status': 'FREIGEGEBEN_FUER_WP_IMPORTE',
        'topic_count': len(items),
        'source_sha256': source_hash,
        'source_file_sha256': sha(workspace / ORIGINAL),
        'checks': 'EIN_MAL_VOR_AUSGABE_TECHNISCHE_VOLLSTAENDIGKEIT',
        'domain_redecision_performed': False,
        'wordpress_import_confirmed': False,
        'files_in_import_order': released,
    })
    if release.exists():
        shutil.rmtree(release)
    os.replace(temp, release)
    (workspace / REPAIR).unlink(missing_ok=True)
    write(workspace / STATUS, {'status': 'FREIGEGEBEN_FUER_WP_IMPORTE', 'batch_id': batch_id,
                               'topic_count': len(items), 'released_count': len(released),
                               'release_available': True, 'wordpress_import_confirmed': False})
    return {'status': 'FREIGEGEBEN_FUER_WP_IMPORTE', 'batch_id': batch_id,
            'topic_count': len(items), 'files': released}


def main():
    ap = argparse.ArgumentParser(description='Ein einziges MINI-Abschlussgate; Fehler => Reparaturschleife')
    ap.add_argument('--workspace', type=Path, required=True)
    ap.add_argument('--original', type=Path, help='Initialer MINI-Export (unveränderlich)')
    args = ap.parse_args()
    try:
        result = init(args.original, args.workspace) if args.original else gate(args.workspace)
        print(json.dumps(result, ensure_ascii=False, indent=2))
        return 0 if result['status'] == 'FREIGEGEBEN_FUER_WP_IMPORTE' else 2
    except (OSError, ValueError, KeyError, TypeError) as exc:
        print(json.dumps({'status': 'UNGUELTIGER_ORIGINALAUFTRAG', 'error': str(exc)}, ensure_ascii=False))
        return 3


if __name__ == '__main__':
    sys.exit(main()),
        title, re.IGNORECASE,
    ):
        return 'TITEL_GENERISCHE_ENDFORMEL'
    return None


def init(original, workspace):
    workspace.mkdir(parents=True, exist_ok=True)
    target = workspace / ORIGINAL
    if target.exists():
        if sha(original) != sha(target):
            raise ValueError('Anderer MINI-Auftrag im Arbeitsraum; alten Auftrag nicht überschreiben.')
    else:
        shutil.copyfile(original, target)
    digest_file = workspace / ORIGINAL_HASH
    if digest_file.exists():
        if digest_file.read_text(encoding='utf-8').strip() != sha(target):
            raise ValueError('Ursprünglicher MINI-Auftrag wurde verändert')
    else:
        digest_file.write_text(sha(target) + '\n', encoding='utf-8')
    return gate(workspace)


def gate(workspace):
    if not (workspace / ORIGINAL).is_file():
        raise ValueError(f'{ORIGINAL} fehlt')
    digest_file = workspace / ORIGINAL_HASH
    if not digest_file.is_file() or digest_file.read_text(encoding='utf-8').strip() != sha(workspace / ORIGINAL):
        raise ValueError('Original ist nicht unverändert hashgebunden; Auftrag nicht freigeben')
    source = read(workspace / ORIGINAL)
    items = source.get('items', [])
    if source.get('contract') != 'TEXTERSTELLUNG_SINGLE_EDITOR_BATCH_V1' or not items:
        raise ValueError('Originalauftrag fehlt oder ist kein MINI-Gesamtauftrag')
    if len(items) != len(source.get('resume_checkpoints', [])):
        raise ValueError('Originalauftrag: Themen/Checkpoints widersprechen sich')
    if source.get('checkpoint_contract') != 'TEXTERSTELLUNG_MINI_CHECKPOINT_V1':
        raise ValueError('Nicht unterstützter Original-MINI-Vertrag')

    problems = []
    loaded = {}
    batch_id, source_hash = source.get('batch_id'), source.get('source_sha256')

    def issue(stage, index, field, code):
        problems.append({'stage': stage, 'item_index': index,
                         'keyword': items[index].get('raw_query', '') if index is not None else '',
                         'field': field, 'code': code})

    # Single technical completeness check, once before release. No subject-matter rechecking.
    for stage in STAGES:
        path = workspace / (stage + '.json')
        if not path.exists():
            continue
        try:
            data = read(path)
        except (json.JSONDecodeError, UnicodeDecodeError) as exc:
            issue(stage, None, 'file', 'JSON_UNLESBAR: ' + str(exc))
            continue
        if (data.get('contract') != source['contract'] or
            data.get('checkpoint_contract') != source['checkpoint_contract'] or
            data.get('batch_id') != batch_id or
            data.get('source_sha256') != source_hash or
            data.get('checkpoint_stage') != stage):
            issue(stage, None, 'header', 'BATCH_ODER_STUFE_FALSCH')
            continue
        rows = data.get('items')
        if not isinstance(rows, list) or len(rows) != len(items):
            issue(stage, None, 'items', 'NICHT_ALLE_ORIGINALTHEMEN')
            continue
        mismatches = []
        for i, (original, actual) in enumerate(zip(items, rows)):
            if not isinstance(actual, dict) or any(actual.get(k) != v for k, v in original.items()):
                issue(stage, i, 'source', 'AUSGANGSDATEN_ODER_REIHENFOLGE_VERAENDERT')
                mismatches.append(i)
        if not mismatches:
            loaded[stage] = rows

    for i, (original, cp) in enumerate(zip(items, source['resume_checkpoints'])):
        next_step = cp.get('next')
        if next_step == 'DONE':
            for st in STAGES:
                if st in loaded and any(val(loaded[st][i].get(k)) for k in STAGE_FIELDS[st]):
                    issue(st, i, 'locked_decision', 'BEREITS_ABGESCHLOSSENE_ENTSCHEIDUNG_WIEDERHOLT')
            continue
        cat = cp.get('category')
        if cat and 'CATEGORY' in loaded:
            if any(val(loaded['CATEGORY'][i].get(k)) for k in STAGE_FIELDS['CATEGORY']):
                issue('CATEGORY', i, 'locked_category', 'ABGESCHLOSSENE_KATEGORIE_ERNEUT_ENTSCHIEDEN')
        if not cat:
            if 'CATEGORY' not in loaded:
                issue('CATEGORY', i, 'file', 'KATEGORIE_DATEI_FEHLT')
                continue
            cat = {k: loaded['CATEGORY'][i].get(k) for k in STAGE_FIELDS['CATEGORY']}
            if cat['route'] not in ('FACH', 'MAGAZIN', 'REDAKTIONSBUERO'):
                issue('CATEGORY', i, 'route', 'KATEGORIE_ENTSCHEIDUNG_FEHLT')
                continue
            if cat['route'] in ('FACH', 'MAGAZIN') and not (val(cat['category_slug']) and val(cat['article_type'])):
                issue('CATEGORY', i, 'category_slug/article_type', 'KATEGORIE_UNVOLLSTAENDIG')
                continue
        if original.get('mode') == 'LEGACY_CATEGORY_ONLY':
            continue  # genuine final stage; no re-decision

        editorial = cp.get('editorial')
        if editorial and 'EDITORIAL' in loaded:
            if any(val(loaded['EDITORIAL'][i].get(k)) for k in STAGE_FIELDS['EDITORIAL']):
                issue('EDITORIAL', i, 'locked_editorial', 'ABGESCHLOSSENE_REDAKTION_ERNEUT_ENTSCHIEDEN')
        if not editorial:
            if 'EDITORIAL' not in loaded:
                issue('EDITORIAL', i, 'file', 'REDAKTION_DATEI_FEHLT')
                continue
            editorial = {k: loaded['EDITORIAL'][i].get(k) for k in STAGE_FIELDS['EDITORIAL']}
            box = editorial['box']
            if box not in ('FREI', 'BELEGT', 'KLAERUNG'):
                issue('EDITORIAL', i, 'box', 'REDAKTIONSENTSCHEIDUNG_FEHLT')
                continue
            if box == 'FREI' and not val(editorial['intent_summary']):
                issue('EDITORIAL', i, 'intent_summary', 'SUCHABSICHT_FEHLT')
                continue
            if box == 'BELEGT' and not val(editorial['matched_ref']):
                issue('EDITORIAL', i, 'matched_ref', 'BESTANDSREFERENZ_FEHLT')
                continue
            if box == 'KLAERUNG' and not val(editorial['reason']):
                issue('EDITORIAL', i, 'reason', 'KLÄRUNGSGRUND_FEHLT')
                continue
        if cp.get('title') and 'TITLE' in loaded:
            if val(loaded['TITLE'][i].get('approved_title')):
                issue('TITLE', i, 'locked_title', 'ABGESCHLOSSENER_TITEL_ERNEUT_ENTSCHIEDEN')
        if editorial.get('box') == 'FREI' and not cp.get('title'):
            if 'TITLE' not in loaded:
                issue('TITLE', i, 'file', 'TITEL_DATEI_FEHLT')
                continue
            if not val(loaded['TITLE'][i].get('approved_title')):
                issue('TITLE', i, 'approved_title', 'ENDGUELTIGER_TITEL_FEHLT')

    release = workspace / RELEASE
    if problems:
        # Rework: keep original and all worker outputs; remove only stale releases.
        if release.exists():
            shutil.rmtree(release)
        problems.sort(key=lambda e: (STAGES.index(e['stage']), e['item_index'] if e['item_index'] is not None else -1))
        ticket = {
            'contract': 'MINI_EINE_ABSCHLUSSPRUEFUNG_REWORK_V1',
            'batch_id': batch_id,
            'status': 'REPARATUR',
            'completed_decisions_are_locked': True,
            'restart_research': False,
            'next_worker': problems[0]['stage'],
            'fix_only': problems,
            'continue_with': 'Korrigierte Worker-Datei am selben Pfad ablegen, danach denselben gate-Befehl erneut ausführen.',
        }
        write(workspace / REPAIR, ticket)
        write(workspace / STATUS, {'status': 'REPARATUR', 'batch_id': batch_id,
                                   'pending': len(problems), 'release_available': False})
        return ticket

    # Publish approved files only after the ONE final technical check passes.
    temp = workspace / ('.' + RELEASE + '.tmp')
    if temp.exists():
        shutil.rmtree(temp)
    temp.mkdir(parents=True)
    released = []
    for stage in STAGES:
        path = workspace / (stage + '.json')
        if stage in loaded:
            dst = temp / path.name
            shutil.copyfile(path, dst)
            released.append({'stage': stage, 'name': dst.name, 'sha256': sha(dst)})
    write(temp / 'NACHWEIS.json', {
        'contract': 'MINI_EINE_ABSCHLUSSPRUEFUNG_REWORK_V1',
        'batch_id': batch_id,
        'status': 'FREIGEGEBEN_FUER_WP_IMPORTE',
        'topic_count': len(items),
        'source_sha256': source_hash,
        'source_file_sha256': sha(workspace / ORIGINAL),
        'checks': 'EIN_MAL_VOR_AUSGABE_TECHNISCHE_VOLLSTAENDIGKEIT',
        'domain_redecision_performed': False,
        'wordpress_import_confirmed': False,
        'files_in_import_order': released,
    })
    if release.exists():
        shutil.rmtree(release)
    os.replace(temp, release)
    (workspace / REPAIR).unlink(missing_ok=True)
    write(workspace / STATUS, {'status': 'FREIGEGEBEN_FUER_WP_IMPORTE', 'batch_id': batch_id,
                               'topic_count': len(items), 'released_count': len(released),
                               'release_available': True, 'wordpress_import_confirmed': False})
    return {'status': 'FREIGEGEBEN_FUER_WP_IMPORTE', 'batch_id': batch_id,
            'topic_count': len(items), 'files': released}


def main():
    ap = argparse.ArgumentParser(description='Ein einziges MINI-Abschlussgate; Fehler => Reparaturschleife')
    ap.add_argument('--workspace', type=Path, required=True)
    ap.add_argument('--original', type=Path, help='Initialer MINI-Export (unveränderlich)')
    args = ap.parse_args()
    try:
        result = init(args.original, args.workspace) if args.original else gate(args.workspace)
        print(json.dumps(result, ensure_ascii=False, indent=2))
        return 0 if result['status'] == 'FREIGEGEBEN_FUER_WP_IMPORTE' else 2
    except (OSError, ValueError, KeyError, TypeError) as exc:
        print(json.dumps({'status': 'UNGUELTIGER_ORIGINALAUFTRAG', 'error': str(exc)}, ensure_ascii=False))
        return 3


if __name__ == '__main__':
    sys.exit(main())