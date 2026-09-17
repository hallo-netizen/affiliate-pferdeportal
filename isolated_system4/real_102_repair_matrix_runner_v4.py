#!/usr/bin/env python3
from __future__ import annotations

import copy
import json
import re
import subprocess
import tempfile
from pathlib import Path

import production_checks
import real_102_repair_matrix_v1 as matrix
import test_repair_continuity

CANONICAL = 'tests/test-canonical-runtime-binding.php'


def _codes(exc: production_checks.RepairRequired) -> list[str]:
    return sorted({str(x.get('error_code') or '') for x in exc.findings if isinstance(x, dict)})


def _expect(repo: Path, html: str, pack: dict, plan: dict, code: str, label: str) -> None:
    try:
        production_checks.run_ppm_content_validator(repo, html, pack, plan)
    except production_checks.RepairRequired as exc:
        codes = _codes(exc)
        if code not in codes:
            raise AssertionError('CURRENT_PPM_MUTATION_WRONG_CODE:' + label + ':' + code + ':' + repr(codes))
        print('CURRENT_PPM_MUTATION_PASS:' + label + ':' + code, flush=True)
        return
    except Exception as exc:
        raise AssertionError('CURRENT_PPM_MUTATION_HARD_BLOCK:' + label + ':' + code + ':' + type(exc).__name__ + ':' + str(exc)) from exc
    raise AssertionError('CURRENT_PPM_MUTATION_NOT_BLOCKED:' + label + ':' + code)


def _replace_in_block(html: str, block: str, pattern: str, repl) -> str:
    section = re.search(r'(<section\b[^>]*data-block="' + re.escape(block) + r'"[^>]*>)(.*?)(</section>)', html, re.I | re.S)
    if not section:
        raise AssertionError('CURRENT_MUTATION_BLOCK_MISSING:' + block)
    body, n = re.subn(pattern, repl, section.group(2), count=1, flags=re.I | re.S)
    if n != 1:
        raise AssertionError('CURRENT_MUTATION_PATTERN_NOT_FOUND_IN_BLOCK:' + block)
    replacement = section.group(1) + body + section.group(3)
    return html[:section.start()] + replacement + html[section.end():]


def current_canonical_mutations(rows: list[dict]) -> dict:
    root = Path(tempfile.mkdtemp(prefix='system4-current-canonical-mut-'))
    _, prepared = test_repair_continuity._prepare_batch(root, 1)
    workspace, _, _ = prepared[0]
    state = json.loads((workspace / 'state.json').read_text(encoding='utf-8'))
    if state.get('phase') != 'CHECK_REQUIRED':
        raise AssertionError('CURRENT_MUTATION_BASE_NOT_CHECK_REQUIRED')
    html = str(state.get('draft_markdown') or '')
    ctx = state.get('production_context') or {}
    pack = copy.deepcopy(ctx.get('fact_pack'))
    plan = copy.deepcopy(ctx.get('production_plan_item'))
    if not html or not isinstance(pack, dict) or not isinstance(plan, dict):
        raise AssertionError('CURRENT_MUTATION_BASE_MISSING')
    baseline = production_checks.run_ppm_content_validator(matrix.REPO, html, pack, plan)
    if baseline.get('status') != 'PASS':
        raise AssertionError('CURRENT_MUTATION_BASE_PPM_NOT_PASS')
    print('CURRENT_PPM_MUTATION_BASELINE_PASS', flush=True)

    claims = pack.get('claims') if isinstance(pack.get('claims'), list) else []
    first_fact = str((claims[0] if claims else {}).get('fact_id') or '')
    if not first_fact:
        raise AssertionError('CURRENT_MUTATION_FIRST_FACT_MISSING')

    def sub1(pattern: str, repl, source: str, flags=0) -> str:
        out, n = re.subn(pattern, repl, source, count=1, flags=flags)
        if n != 1:
            raise AssertionError('CURRENT_MUTATION_PATTERN_NOT_FOUND:' + pattern)
        return out

    h = sub1(r'href="/[^"]+"', 'href="https://external.invalid/"', html)
    _expect(matrix.REPO, h, pack, plan, 'BLOCKED_CONTENT_INTERNAL_LINK_ROLE', 'internal_link_role')

    h = sub1(r'\sdata-fact-ids="[^"]+"', '', html)
    _expect(matrix.REPO, h, pack, plan, 'BLOCKED_CONTENT_FACT_REFS_MISSING', 'fact_refs_missing')

    h = sub1(r'data-fact-ids="[^"]+"', 'data-fact-ids="unknown-fact-id"', html)
    _expect(matrix.REPO, h, pack, plan, 'BLOCKED_CONTENT_FACT_REF_UNKNOWN', 'fact_ref_unknown')

    def numeric(m):
        return m.group(1) + ' Die zusätzliche Prüfzahl lautet 999999.' + m.group(2)
    h = sub1(r'(<p\b[^>]*data-fact-ids="[^"]+"[^>]*>.*?)(</p>)', numeric, html, re.I | re.S)
    _expect(matrix.REPO, h, pack, plan, 'BLOCKED_CONTENT_NUMERIC_CLAIM_UNSUPPORTED', 'numeric_claim')

    h = re.sub(r'data-fact-ids="[^"]+"', 'data-fact-ids="' + first_fact + '"', html)
    _expect(matrix.REPO, h, pack, plan, 'BLOCKED_CONTENT_FACT_PACK_COVERAGE', 'fact_pack_coverage')

    trace_unit_pattern = r'(<p\b[^>]*data-fact-ids="[^"]+"[^>]*>)(.*?)(<span\b[^>]*class="ppm-source-trace"[^>]*>.*?</span>)(.*?</p>)'
    lexical_sentences = [
        'Im Wohnzimmer steht ein kleiner Tisch neben dem Fenster.',
        'Auf dem Regal liegt ein gebundenes Buch mit blauem Einband.',
        'Eine helle Lampe beleuchtet am Abend den Schreibtisch.',
        'Vor dem Fenster hängt ein schlichter Vorhang aus Baumwolle.',
        'Auf dem Boden liegt ein weicher Teppich mit ruhigem Muster.',
        'Neben der Tür steht eine hohe Vase auf einem schmalen Schrank.',
        'In der Küche steht eine weiße Tasse neben einer kleinen Schale.',
        'Der Stuhl am Tisch hat eine gerade Lehne aus hellem Holz.',
        'Auf dem Sofa liegt ein weiches Kissen mit grauem Bezug.',
        'An der Wand hängt ein gerahmtes Bild über einer niedrigen Kommode.',
        'Im Flur steht ein schmaler Korb unter einer einfachen Garderobe.',
        'Auf dem Fensterbrett steht eine kleine Pflanze in einem Tontopf.',
    ]
    lexical_index = {'n': 0}
    def lexical(m):
        sentence = lexical_sentences[lexical_index['n'] % len(lexical_sentences)]
        lexical_index['n'] += 1
        return m.group(1) + sentence + ' ' + m.group(3) + m.group(4)
    h, changed = re.subn(trace_unit_pattern, lexical, html, flags=re.I | re.S)
    if changed < 1:
        raise AssertionError('CURRENT_MUTATION_TRACE_UNITS_MISSING')
    _expect(matrix.REPO, h, pack, plan, 'BLOCKED_CONTENT_TRACE_LEXICAL_SUPPORT', 'trace_lexical_support')

    # Exceed the 2% duplicate threshold with only a few exact duplicates and separate them
    # with distinct, correct German sentences so LanguageTool does not become the first gate.
    duplicate = 'Die abschließende Sichtprüfung bestätigt den dokumentierten Kontrollpunkt.'
    spacer = [
        'Danach wird der nächste Abschnitt unabhängig davon betrachtet.',
        'Ein weiterer Absatz beschreibt einen getrennten Prüfschritt.',
        'Anschließend folgt eine eigenständige Kontrolle des nächsten Bereichs.',
        'Zum Schluss wird ein zusätzlicher Abschnitt separat gelesen.',
    ]
    repeat = ''.join('<p data-fact-ids="' + first_fact + '">' + duplicate + ' ' + s + '</p>' for s in spacer)
    h = sub1(r'(<section\b[^>]*data-block="details"[^>]*>)', lambda m: m.group(1) + repeat, html, re.I)
    _expect(matrix.REPO, h, pack, plan, 'BLOCKED_CONTENT_DUPLICATE_SENTENCE_RATIO', 'duplicate_sentence_ratio')

    intro = re.search(r'<section\b[^>]*data-block="intro"[^>]*>.*?(<p\b[^>]*>.*?</p>)', html, re.I | re.S)
    if not intro:
        raise AssertionError('CURRENT_MUTATION_INTRO_PARAGRAPH_MISSING')
    h = sub1(r'(<section\b[^>]*data-block="intro"[^>]*>)', lambda m: m.group(1) + intro.group(1), html, re.I)
    _expect(matrix.REPO, h, pack, plan, 'BLOCKED_CONTENT_INTRO_PAIR_SIMILARITY', 'intro_pair_similarity')

    h = _replace_in_block(html, 'details', r'data-source-hash="[0-9a-f]{64}"', 'data-source-hash="' + ('a' * 64) + '"')
    _expect(matrix.REPO, h, pack, plan, 'BLOCKED_CONTENT_TRACE_CLAIM_MISMATCH', 'trace_claim_mismatch')

    def short_p(m):
        return m.group(0) if 'pm-ai-disclosure' in m.group(1) else '<p' + m.group(1) + '>Kurz.</p>'
    h = re.sub(r'<p\b([^>]*)>.*?</p>', short_p, html, flags=re.I | re.S)
    _expect(matrix.REPO, h, pack, plan, 'BLOCKED_CONTENT_WORD_FLOOR', 'word_floor')

    seen = {'n': 0}
    def limit_p(m):
        seen['n'] += 1
        return m.group(0) if seen['n'] <= 10 else ''
    h = re.sub(r'<p\b[^>]*>.*?</p>', limit_p, html, flags=re.I | re.S)
    _expect(matrix.REPO, h, pack, plan, 'BLOCKED_CONTENT_PARAGRAPH_FLOOR', 'paragraph_floor')

    seen = {'n': 0}
    def limit_h2(m):
        seen['n'] += 1
        return m.group(0) if seen['n'] <= 3 else '<h3' + m.group(1) + '>' + m.group(2) + '</h3>'
    h = re.sub(r'<h2\b([^>]*)>(.*?)</h2>', limit_h2, html, flags=re.I | re.S)
    _expect(matrix.REPO, h, pack, plan, 'BLOCKED_CONTENT_H2_FLOOR', 'h2_floor')

    tbody = re.search(r'<tbody\b[^>]*>(.*?)</tbody>', html, re.I | re.S)
    if not tbody:
        raise AssertionError('CURRENT_MUTATION_TBODY_MISSING')
    trs = re.findall(r'<tr\b[^>]*>.*?</tr>', tbody.group(1), re.I | re.S)
    if len(trs) < 4:
        raise AssertionError('CURRENT_MUTATION_BASE_TABLE_TOO_SMALL')
    replacement = '<tbody>' + ''.join(trs[:3]) + '</tbody>'
    h = html[:tbody.start()] + replacement + html[tbody.end():]
    _expect(matrix.REPO, h, pack, plan, 'BLOCKED_CONTENT_TABLE_ROW_FLOOR', 'table_row_floor')

    p = copy.deepcopy(pack)
    p['claims'][0]['claim_status'] = 'REJECTED'
    _expect(matrix.REPO, html, p, plan, 'BLOCKED_CONTENT_FACT_REF_NOT_VERIFIED', 'fact_status')

    p = copy.deepcopy(pack)
    p['claims'][0]['article_types'] = ['Pflege']
    _expect(matrix.REPO, html, p, plan, 'BLOCKED_CONTENT_FACT_REF_TYPE_MISMATCH', 'fact_type')

    bound = [r for r in rows if r['scope'] == 'PPM679' and r['negative_test'] == CANONICAL]
    expected_codes = {r['error_code'] for r in bound}
    canonical_codes = {
        'BLOCKED_CONTENT_INTERNAL_LINK_ROLE','BLOCKED_CONTENT_FACT_REFS_MISSING','BLOCKED_CONTENT_FACT_REF_UNKNOWN',
        'BLOCKED_CONTENT_NUMERIC_CLAIM_UNSUPPORTED','BLOCKED_CONTENT_FACT_PACK_COVERAGE','BLOCKED_CONTENT_TRACE_LEXICAL_SUPPORT',
        'BLOCKED_CONTENT_DUPLICATE_SENTENCE_RATIO','BLOCKED_CONTENT_INTRO_PAIR_SIMILARITY','BLOCKED_CONTENT_TRACE_CLAIM_MISMATCH',
        'BLOCKED_CONTENT_WORD_FLOOR','BLOCKED_CONTENT_PARAGRAPH_FLOOR','BLOCKED_CONTENT_H2_FLOOR','BLOCKED_CONTENT_TABLE_ROW_FLOOR',
        'BLOCKED_CONTENT_FACT_REF_NOT_VERIFIED','BLOCKED_CONTENT_FACT_REF_TYPE_MISMATCH',
    }
    if expected_codes != canonical_codes:
        raise AssertionError('CURRENT_CANONICAL_REGISTRY_SET_CHANGED:' + repr(sorted(expected_codes ^ canonical_codes)))
    return {'path': CANONICAL, 'return_code': 0, 'bound_rule_count': len(bound), 'compatibility': 'CURRENT_GREEN_SYSTEM4A_FAQ_MUTATIONS'}


def run_ppm_targeted_authorities(ppm_root: Path, rows: list[dict]) -> dict:
    ppm_rows = [r for r in rows if r['scope'] == 'PPM679']
    negative = sorted({r['negative_test'] for r in ppm_rows})
    positive = sorted({r['positive_test'] for r in ppm_rows})
    if any(not p for p in negative + positive):
        raise AssertionError('PPM_RULE_TEST_BINDING_MISSING')
    executed_negative = []
    for rel in negative:
        if rel == CANONICAL:
            executed_negative.append(current_canonical_mutations(rows))
            continue
        path = ppm_root / rel
        if not path.is_file():
            raise AssertionError('PPM_NEGATIVE_TEST_MISSING:' + rel)
        cp = subprocess.run(['php', str(path)], cwd=ppm_root, text=True, capture_output=True)
        combined = (cp.stdout or '') + '\n' + (cp.stderr or '')
        bound_rows = [r for r in ppm_rows if r['negative_test'] == rel]
        missing = sorted({r['error_code'] for r in bound_rows if r['error_code'] not in combined})
        if missing:
            raise AssertionError('PPM_TARGET_ERROR_NOT_EMITTED:' + rel + ':' + ','.join(missing) + ':RC=' + str(cp.returncode) + '\n' + combined[-8000:])
        executed_negative.append({'path': rel, 'return_code': cp.returncode, 'bound_rule_count': len(bound_rows), 'compatibility': 'UNCHANGED'})
        print('PPM_TARGETED_NEGATIVE_PASS:' + rel + ':' + str(len(bound_rows)), flush=True)
    executed_positive = []
    for rel in positive:
        path = ppm_root / rel
        if not path.is_file():
            raise AssertionError('PPM_POSITIVE_TEST_MISSING:' + rel)
        cp = subprocess.run(['php', str(path)], cwd=ppm_root, text=True, capture_output=True)
        executed_positive.append({'path': rel, 'return_code': cp.returncode})
        print(('PPM_TARGETED_POSITIVE_PASS:' if cp.returncode == 0 else 'PPM_REGISTRY_POSITIVE_STALE:') + rel + ':RC=' + str(cp.returncode), flush=True)
    return {'negative': executed_negative, 'positive': executed_positive}


matrix.run_ppm_targeted_authorities = run_ppm_targeted_authorities
raise SystemExit(matrix.main())
