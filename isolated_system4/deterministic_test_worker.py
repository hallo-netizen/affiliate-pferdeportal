from __future__ import annotations

import hashlib
import html
import json
import os
import re
import subprocess
import sys
from pathlib import Path

import block_semantics
import content_guard
import root_entry
import supervisor
import worker_dispatch

HERE = Path(__file__).resolve().parent
REPO = HERE.parent


def canon(value) -> bytes:
    return (json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(',', ':')) + '\n').encode()


def writej(path: Path, value) -> Path:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2, sort_keys=True) + '\n', encoding='utf-8')
    return path


def _head() -> str:
    return subprocess.check_output(['git', 'rev-parse', '--verify', 'HEAD'], cwd=REPO, text=True).strip()


def _gate(workspace: Path) -> dict:
    bundle_path = workspace / 'worker_dispatch.json'
    if not bundle_path.is_file():
        raise RuntimeError('TESTWORKER_DISPATCH_MISSING')
    bundle = json.loads(bundle_path.read_text(encoding='utf-8'))
    manifest = root_entry._critical_manifest_sha256()
    head = _head()
    worker_contract, _ = worker_dispatch.verify_bundle(bundle, actual_manifest=manifest, actual_head=head)
    supervisor.verify_controller_binding(workspace)
    if worker_contract.get('external_web_search_allowed') is not False:
        raise RuntimeError('TESTWORKER_FREE_WEB_NOT_BLOCKED')
    if worker_contract.get('machine_prewrite_mutation_allowed') is not False:
        raise RuntimeError('TESTWORKER_PREWRITE_MUTATION_NOT_BLOCKED')
    return worker_contract


def _state(workspace: Path) -> dict:
    _gate(workspace)
    path = workspace / 'state.json'
    if not path.is_file():
        raise RuntimeError('TESTWORKER_STATE_MISSING')
    return json.loads(path.read_text(encoding='utf-8'))


def _sentences(text: str) -> list[str]:
    rows = []
    for raw in re.split(r'(?<=[.!?])\s+', text.strip()):
        value = ' '.join(raw.split()).strip()
        if len(value) >= 25:
            rows.append(value)
    return rows


def _clean_statement(sentence: str, source_title: str) -> str:
    value = ' '.join(sentence.split()).strip()
    title = ' '.join(str(source_title or '').split()).strip()
    while title and value.casefold().startswith((title + ' ').casefold()):
        value = value[len(title):].lstrip(' :-–—')
    value = value.replace('Walkarbeit', 'Verformung des Reifens')
    value = value.replace('weginterpretiert', 'ignoriert')
    value = value.replace('den Verriegelungsweg', 'die Verriegelung')
    if value and value[-1] not in '.!?':
        value += '.'
    return value


def research(workspace: Path, out: Path) -> dict:
    state = _state(workspace)
    if state.get('phase') != 'RESEARCH_REQUIRED':
        raise RuntimeError('TESTWORKER_PHASE_NOT_RESEARCH')
    value = supervisor.expected_research_document(workspace)
    content_guard.validate_research_document(value)
    writej(out, value)
    return {'status': 'PASS', 'stage': 'RESEARCH', 'sha256': hashlib.sha256(canon(value)).hexdigest()}


def facts(workspace: Path, out: Path) -> dict:
    state = _state(workspace)
    if state.get('phase') != 'FACT_CHECK_REQUIRED':
        raise RuntimeError('TESTWORKER_PHASE_NOT_FACTS')
    research_obj = content_guard.validate_research_document(state['research']['text'])
    claims = []
    number = 0
    for source in research_obj['sources']:
        for sentence in _sentences(source['evidence']):
            statement = _clean_statement(sentence, source.get('source_title', ''))
            if len(statement) < 20:
                continue
            number += 1
            claims.append({
                'fact_id': f'fact-{state["article"]["plan_slot"][:12]}-{number}',
                'source_id': source['source_id'],
                'statement': statement,
                'evidence_text': sentence,
                'evidence_text_sha256': hashlib.sha256(sentence.encode()).hexdigest(),
            })
    if len(claims) < 4:
        raise RuntimeError('TESTWORKER_FACT_SOURCE_TOO_THIN')
    value = {'contract': 'SYSTEM4_FACTS_EVIDENCE_V1', 'claims': claims}
    content_guard.validate_facts_document(value, research_obj)
    writej(out, value)
    return {'status': 'PASS', 'stage': 'FACTS', 'claim_count': len(claims), 'sha256': hashlib.sha256(canon(value)).hexdigest()}


def _slug(text: str) -> str:
    value = text.casefold().replace('ä', 'ae').replace('ö', 'oe').replace('ü', 'ue').replace('ß', 'ss')
    return re.sub(r'[^a-z0-9]+', '-', value).strip('-')[:160] or 'system4-testartikel'


def context(workspace: Path, pack_out: Path, plan_out: Path) -> dict:
    state = _state(workspace)
    if state.get('phase') != 'CONTEXT_REQUIRED':
        raise RuntimeError('TESTWORKER_PHASE_NOT_CONTEXT')
    research_obj = content_guard.validate_research_document(state['research']['text'])
    facts_obj = content_guard.validate_facts_document(state['facts']['text'], research_obj)
    prewrite = json.loads((workspace / 'bound_machine_prewrite.json').read_text(encoding='utf-8'))
    rails = json.loads(json.dumps(prewrite['production_plan_rails'], ensure_ascii=False))
    snapshot_sha = hashlib.sha256((workspace / 'bound_snapshot.json').read_bytes()).hexdigest()
    source_by_id = {row['source_id']: row for row in research_obj['sources']}
    pack_claims = []
    for row in facts_obj['claims']:
        claim = dict(row)
        source = source_by_id[row['source_id']]
        claim['source_url'] = source['source_url']
        claim['claim_status'] = 'FULLY_SUPPORTED'
        claim['article_types'] = [state['article']['article_type']]
        pack_claims.append(claim)
    pack = {
        'contract': 'canonical_fact_pack_v1',
        'status': 'SOURCE_VERIFIED_PRODUCTION_READY',
        'source_snapshot_id': snapshot_sha,
        'fact_pack_id': snapshot_sha,
        'sources': research_obj['sources'],
        'claims': pack_claims,
    }
    quality = rails['quality_binding']
    allowed = [claim['fact_id'] for claim in pack_claims]
    direct = str(quality.get('faq_direct_answer') or '').strip()
    links = quality.get('link_bindings') if isinstance(quality.get('link_bindings'), list) else []
    title = state['article']['title']
    keyword = state['article']['target_keyword']
    article_type = state['article']['article_type']
    runtime = {
        'order_id': 'system4-test-' + state['article']['plan_slot'][:16],
        'article_type': article_type,
        'title': title,
        'slug': _slug(title),
        'subject_scope': title,
        'subject_label': keyword,
        'lead': direct or title,
        'conclusion': 'Die gebundenen Prüfpunkte werden vor der Fahrt vollständig kontrolliert und erkennbare Abweichungen vor dem Start geklärt.',
        'links': links,
        'allowed_fact_ids': allowed,
        'question': title,
        'answer': direct or title,
        'faq_question': title,
        'faq_answer': direct or title,
        'summary': direct or title,
        'search_intent': rails.get('search_intent') or 'informational',
    }
    plan = dict(rails)
    plan['source_snapshot_id'] = snapshot_sha
    plan['runtime_order'] = runtime
    plan['canonical_article'] = {'title': title, 'article_type': article_type, 'slug': runtime['slug']}
    plan['source_hashes'] = [row['snapshot_sha256'] for row in research_obj['sources']]
    writej(pack_out, pack)
    writej(plan_out, plan)
    return {'status': 'PASS', 'stage': 'CONTEXT', 'fact_pack_claims': len(pack_claims), 'allowed_fact_ids': len(allowed)}


def _plain_claim(statement: str) -> str:
    return ' '.join(str(statement or '').strip().rstrip('.!?').split())


def _trace(fact_id: str, authority: dict) -> str:
    meta = authority[fact_id]
    trace_source_title = html.escape(str(meta.get('trace_source_title') or meta.get('source_id') or ''), quote=True)
    source_hash = html.escape(str(meta.get('evidence_text_sha256') or ''), quote=True)
    fact = html.escape(fact_id, quote=True)
    return f'<span class="ppm-source-trace" data-fact-id="{fact}" data-source-title="{trace_source_title}" data-source-hash="{source_hash}"></span>'


def _p(fact_id: str, text: str, authority: dict) -> str:
    return f'<p data-fact-ids="{html.escape(fact_id, quote=True)}">{text}{_trace(fact_id, authority)}</p>'


def _li(fact_id: str, text: str, authority: dict) -> str:
    return f'<li data-fact-ids="{html.escape(fact_id, quote=True)}">{text}{_trace(fact_id, authority)}</li>'


def _td(fact_id: str, text: str, authority: dict) -> str:
    return f'<td data-fact-ids="{html.escape(fact_id, quote=True)}">{text}{_trace(fact_id, authority)}</td>'


TAILS = [
    'Befund wird vorab sorgfältig geprüft',
    'Abweichung wird vorher eindeutig geklärt',
    'Zustand wird aktuell erneut bestätigt',
    'Funktion wird gezielt vollständig kontrolliert',
    'Ergebnis wird neu eindeutig festgestellt',
    'Prüfpunkt bleibt weiterhin klar nachvollziehbar',
    'Kontrolle erfolgt direkt vor Fahrtbeginn',
    'Beobachtung wird anschließend eindeutig bewertet',
]


def _fact_sentence(fact_id: str, claims: dict, index: int) -> str:
    base = html.escape(_plain_claim(claims[fact_id]['statement']))
    tail_index = (index + index // len(TAILS)) % len(TAILS)
    tail = TAILS[tail_index]
    return f'{base}; {tail}.'


def _heading(intent_terms: list[str], index: int) -> str:
    term = html.escape(intent_terms[index % len(intent_terms)] if intent_terms else 'Kontrolle')
    endings = [
        'vor der Fahrt gezielt kontrollieren',
        'im festen Kontrollgang richtig einordnen',
        'bei der Vorbereitung zuverlässig prüfen',
        'vor dem Losfahren eindeutig beurteilen',
        'als aktuellen Zustand sicher feststellen',
        'bei jeder Fahrt erneut kontrollieren',
    ]
    return f'{term} {endings[index % len(endings)]}'


def _link_paragraph(row: dict) -> str:
    href = html.escape(str(row.get('href') or ''), quote=True)
    anchor = html.escape(str(row.get('anchor') or ''))
    role = str(row.get('role') or '')
    introductions = {
        'parent_category': 'Zum übergeordneten Themenbereich gehört',
        'semantic_related': 'Inhaltlich passend ergänzt',
        'further_information': 'Weiterführende Informationen bietet',
    }
    intro = introductions.get(role, 'Ergänzend führt der gebundene interne Verweis zu')
    return f'<p>{intro} <a href="{href}">{anchor}</a>.</p>'


def _required_list_blocks(type_req: dict) -> list[str]:
    raw = type_req.get('required_lists')
    if isinstance(raw, list):
        return [str(v) for v in raw if isinstance(v, str) and v]
    if isinstance(raw, dict):
        values = []
        for key, value in raw.items():
            if value is True or isinstance(value, (dict, list)):
                values.append(str(key))
        return values
    return []


def draft(workspace: Path, out: Path, repair: bool = False) -> dict:
    state = _state(workspace)
    expected = 'REPAIR_REQUIRED' if repair else 'DRAFT_REQUIRED'
    if state.get('phase') != expected:
        raise RuntimeError('TESTWORKER_PHASE_NOT_' + expected)
    contract = state.get('authoring_contract')
    if not isinstance(contract, dict):
        raise RuntimeError('TESTWORKER_AUTHORING_CONTRACT_MISSING')

    identity = contract['article_identity']
    bound = contract['bound_requirements']
    req = contract['global_requirements']
    type_req = contract['type_requirements']
    structure = contract['structure_requirements']
    ids = list(bound['canonical_fact_ids'])
    authority = bound['fact_authority']
    claims = {row['fact_id']: row for row in state['production_context']['fact_pack']['claims']}
    if len(ids) < 4:
        raise RuntimeError('TESTWORKER_FACTS_TOO_LOW_FOR_DRAFT')
    if any(not str(authority[fid].get('trace_source_title') or authority[fid].get('source_id') or '').strip() for fid in ids):
        raise RuntimeError('TESTWORKER_TRACE_SOURCE_AUTHORITY_MISSING')

    intro_name = str((structure.get('intro') or {}).get('required_block') or 'intro')
    direct = html.escape(str(bound.get('faq_direct_answer') or '').strip())
    intro_fact = ids[0]
    sections: dict[str, list[str]] = {
        intro_name: [_p(intro_fact, direct, authority)]
    }
    order = [intro_name]

    required_blocks = [str(v) for v in (type_req.get('required_blocks') or []) if str(v)]
    links = [row for row in (bound.get('link_bindings') or []) if isinstance(row, dict) and row.get('active') is not False]
    for row in links:
        section_id = str(row.get('section_id') or '').strip()
        if section_id and section_id not in required_blocks:
            required_blocks.append(section_id)
    table_cfg = structure.get('table') if isinstance(structure.get('table'), dict) else {}
    table_block = str(table_cfg.get('required_block') or 'table')
    for name in ('answer', 'details', 'further_information', table_block, 'conclusion'):
        if name not in required_blocks:
            required_blocks.append(name)

    cursor = 0
    intent_terms = [str(v) for v in bound.get('intent_terms', []) if str(v).strip()]
    for block in required_blocks:
        if block == intro_name:
            continue
        if block not in sections:
            semantic_heading = block_semantics.canonical_heading(contract, block)
            heading = html.escape(semantic_heading) if semantic_heading else _heading(intent_terms, len(order))
            sections[block] = [f'<h2>{heading}</h2>']
            order.append(block)
        if block in {table_block, 'conclusion'}:
            continue
        for _ in range(2):
            fact_id = ids[cursor % len(ids)]
            sections[block].append(_p(fact_id, _fact_sentence(fact_id, claims, cursor), authority))
            cursor += 1

    for row in links:
        section_id = str(row.get('section_id') or '').strip()
        if not section_id:
            raise RuntimeError('TESTWORKER_LINK_SECTION_ID_MISSING')
        sections[section_id].append(_link_paragraph(row))

    list_blocks = _required_list_blocks(type_req)
    list_block = next((block for block in list_blocks if block in sections), 'details')
    list_items = []
    for offset in range(4):
        fact_id = ids[(cursor + offset) % len(ids)]
        list_items.append(_li(fact_id, _fact_sentence(fact_id, claims, cursor + offset), authority))
    sections[list_block].append('<ul>' + ''.join(list_items) + '</ul>')
    cursor += 4

    min_rows = max(4, int(table_cfg.get('minimum_body_rows') or req.get('min_table_body_rows') or 0))
    row_labels = ['Ausgangslage', 'Sichtprüfung', 'Funktionsprüfung', 'Abschlusskontrolle', 'Nachkontrolle', 'Freigabeprüfung']
    unused_tail = ids[cursor:] if cursor < len(ids) else []
    table_pool = unused_tail if len(unused_tail) >= (min_rows * 2) else ids
    if len(table_pool) < 2:
        raise RuntimeError('TESTWORKER_TABLE_FACT_POOL_TOO_LOW')
    table_rows = []
    table_fact_ids: set[str] = set()
    for row_index in range(min_rows):
        observation_fact = table_pool[(row_index * 2) % len(table_pool)]
        action_fact = table_pool[(row_index * 2 + 1) % len(table_pool)]
        table_fact_ids.update((observation_fact, action_fact))
        table_rows.append(
            '<tr>'
            + _td(observation_fact, html.escape(row_labels[row_index % len(row_labels)]), authority)
            + _td(observation_fact, _fact_sentence(observation_fact, claims, cursor + row_index * 2), authority)
            + _td(action_fact, _fact_sentence(action_fact, claims, cursor + row_index * 2 + 1), authority)
            + '</tr>'
        )
    statement_fact = table_pool[0]
    table_statement = html.escape(str(bound.get('table_value_statement') or '').strip())
    table = (
        _p(statement_fact, table_statement, authority)
        + '<table class="system-129-table comparison-table">'
        + '<thead><tr><th>Prüfbereich</th><th>Beobachtung</th><th>Handlung</th></tr></thead>'
        + '<tbody>' + ''.join(table_rows) + '</tbody></table>'
    )
    sections[table_block].append(table)
    cursor += min_rows * 2 + 1

    post_table_ids = [fact_id for fact_id in ids if fact_id not in table_fact_ids]
    if not post_table_ids:
        raise RuntimeError('TESTWORKER_POST_TABLE_FACT_POOL_EMPTY')

    for _ in range(2):
        fact_id = post_table_ids[cursor % len(post_table_ids)]
        sections['conclusion'].append(_p(fact_id, _fact_sentence(fact_id, claims, cursor), authority))
        cursor += 1

    def render() -> str:
        body = ''.join(f'<section data-block="{html.escape(name, quote=True)}">{"".join(sections[name])}</section>' for name in order)
        return '<article class="ppm-generated ppm-type-faq" data-article-type="FAQ">' + body + '</article>'

    def word_count(value: str) -> int:
        return len(re.findall(r'\b[\wÄÖÜäöüß-]+\b', re.sub(r'<[^>]+>', ' ', value), re.UNICODE))

    target_words = int(req.get('min_words') or 0) + 100
    paragraph_target = int(req.get('min_paragraphs') or 0) + 2
    h2_target = int(req.get('min_h2') or 0)
    extra_index = 0
    while True:
        body = render()
        paragraphs = len(re.findall(r'(?is)<p\b', body))
        h2_count = len(re.findall(r'(?is)<h2\b', body))
        if word_count(body) >= target_words and paragraphs >= paragraph_target and h2_count >= h2_target:
            break
        block = 'details' if extra_index % 2 == 0 else 'further_information'
        fact_id = post_table_ids[cursor % len(post_table_ids)]
        sections[block].append(_p(fact_id, _fact_sentence(fact_id, claims, cursor), authority))
        cursor += 1
        extra_index += 1
        if extra_index > 80:
            raise RuntimeError('TESTWORKER_GLOBAL_FLOOR_UNREACHABLE')

    conclusion_attempts = 0
    while True:
        body = render()
        total_words = word_count(body)
        conclusion_words = word_count(''.join(sections['conclusion']))
        if total_words > 0 and (conclusion_words / total_words) >= 0.09:
            break
        fact_id = post_table_ids[cursor % len(post_table_ids)]
        sections['conclusion'].append(_p(fact_id, _fact_sentence(fact_id, claims, cursor), authority))
        cursor += 1
        conclusion_attempts += 1
        if conclusion_attempts > 12:
            raise RuntimeError('TESTWORKER_CONCLUSION_BALANCE_UNREACHABLE')

    # Test-only reproduction of the four real article-0 PPM finding families.
    # It is opt-in and never active in production. The repair pass rebuilds the
    # article from the bound contract without receiving any prebuilt final body.
    if not repair and os.environ.get('SYSTEM4_TEST_REAL7_PPM_MULTIFINDING', '').strip() == '1':
        duplicate = next(
            (row for row in sections.get('details', []) if row.startswith('<p ') and '<a ' not in row),
            None,
        )
        if duplicate is None:
            raise RuntimeError('TESTWORKER_MULTIFINDING_DUPLICATE_SOURCE_MISSING')
        sections['details'].append(duplicate)

        conclusion_rows = sections.get('conclusion', [])
        conclusion_heading = [row for row in conclusion_rows if row.startswith('<h2>')]
        conclusion_paragraphs = [row for row in conclusion_rows if row.startswith('<p ')]
        if len(conclusion_heading) != 1 or len(conclusion_paragraphs) < 2:
            raise RuntimeError('TESTWORKER_MULTIFINDING_CONCLUSION_SOURCE_MISSING')
        sections['conclusion'] = conclusion_heading + conclusion_paragraphs[:2]

        def _flatten_table_cells(value: str) -> str:
            def repl(match: re.Match[str]) -> str:
                attrs = match.group(1)
                inner = match.group(2)
                trace = ''.join(re.findall(r'(?is)<span\\b[^>]*class="ppm-source-trace"[^>]*></span>', inner))
                return '<td' + attrs + '>Prüfung Kontrolle Zustand.' + trace + '</td>'
            return re.sub(r'(?is)<td([^>]*)>(.*?)</td>', repl, value)

        sections[table_block] = [_flatten_table_cells(row) for row in sections.get(table_block, [])]

    # In the dedicated real7 proof, the first workshop pass intentionally leaves
    # one repairable conclusion defect. This proves that a still-bad article loops
    # back to DRAFT_WORKER again instead of becoming a terminal block.
    if repair and os.environ.get('SYSTEM4_TEST_REAL7_PPM_MULTIFINDING', '').strip() == '1' and int(state.get('revision') or 0) == 1:
        conclusion_rows = sections.get('conclusion', [])
        conclusion_heading = [row for row in conclusion_rows if row.startswith('<h2>')]
        conclusion_paragraphs = [row for row in conclusion_rows if row.startswith('<p ')]
        if len(conclusion_heading) != 1 or len(conclusion_paragraphs) < 2:
            raise RuntimeError('TESTWORKER_WORKSHOP_LOOP_CONCLUSION_SOURCE_MISSING')
        sections['conclusion'] = conclusion_heading + conclusion_paragraphs[:2]

    body = render()
    if not repair and identity['target_keyword'] == 'Bodenprüfung am Pferdeanhänger':
        marker = ' Als belastbares Ergebnis muss dieser Prüfschritt dokumentiert bleiben.'
        body = body.replace('</p>', marker + '</p>', 1)

    out.write_text(body, encoding='utf-8')
    return {
        'status': 'PASS',
        'stage': 'REPAIR' if repair else 'DRAFT',
        'word_count': word_count(body),
        'sha256': hashlib.sha256(body.encode()).hexdigest(),
    }


def main(argv: list[str]) -> int:
    if len(argv) < 3:
        raise SystemExit('usage: deterministic_test_worker.py <gate|research|facts|context|draft|repair> <workspace> [outputs...]')
    cmd = argv[1]
    workspace = Path(argv[2])
    if cmd == 'gate':
        worker_contract = _gate(workspace)
        print(json.dumps({'status': 'PASS', 'stage': 'GATE', 'item_index': worker_contract['item_index']}, sort_keys=True))
        return 0
    if cmd == 'research' and len(argv) == 4:
        result = research(workspace, Path(argv[3]))
    elif cmd == 'facts' and len(argv) == 4:
        result = facts(workspace, Path(argv[3]))
    elif cmd == 'context' and len(argv) == 5:
        result = context(workspace, Path(argv[3]), Path(argv[4]))
    elif cmd == 'draft' and len(argv) == 4:
        result = draft(workspace, Path(argv[3]), False)
    elif cmd == 'repair' and len(argv) == 4:
        result = draft(workspace, Path(argv[3]), True)
    else:
        raise SystemExit('TESTWORKER_BAD_COMMAND')
    print(json.dumps(result, ensure_ascii=False, sort_keys=True))
    return 0


if __name__ == '__main__':
    raise SystemExit(main(sys.argv))