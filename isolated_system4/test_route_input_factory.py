from __future__ import annotations

import copy
import hashlib
import json
import threading
import zipfile
from http.server import ThreadingHTTPServer, SimpleHTTPRequestHandler
from pathlib import Path
import sys

import chat_start_gate
import production_checks
import source_acquisition

HERE = Path(__file__).resolve().parent
REPO = HERE.parent
PPM = REPO / production_checks.PPM_PACKAGE_REL
TARGET_CATEGORY = 'checklisten-fuer-pferdeanhaenger-faq'
CATEGORY_SOURCE = 'portal-production-machine/contracts/complete-portal-category-source-v1.json'
CATEGORY_HIERARCHY = 'portal-production-machine/contracts/category-hierarchy-snapshot-v1.json'
LINK_SOURCE = 'portal-production-machine/contracts/wordpress-link-target-snapshot-v1.json'
TYPE_SOURCE = 'portal-production-machine/contracts/article-type-templates.json'
STRUCTURE_SOURCE = 'portal-production-machine/contracts/content-structure-language-gate-v2.json'


def stable(value) -> str:
    return hashlib.sha256(json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(',', ':')).encode()).hexdigest()


def writej(path: Path, value) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2, sort_keys=True) + '\n', encoding='utf-8')


class Quiet(SimpleHTTPRequestHandler):
    def log_message(self, format, *args):
        pass


def _ppm_json(archive: zipfile.ZipFile, member: str) -> dict:
    try:
        value = json.loads(archive.read(member).decode('utf-8'))
    except Exception as exc:
        raise RuntimeError('PPM679_PARENT_AUTHORITY_READ_FAILED:' + member) from exc
    if not isinstance(value, dict):
        raise RuntimeError('PPM679_PARENT_AUTHORITY_OBJECT_REQUIRED:' + member)
    return value


def _one(rows: list[dict], label: str) -> dict:
    if len(rows) != 1:
        raise RuntimeError('PPM679_PARENT_AUTHORITY_' + label + '_COUNT:' + str(len(rows)))
    return copy.deepcopy(rows[0])


def _parent_authorities() -> dict:
    with zipfile.ZipFile(PPM) as archive:
        category_source = _ppm_json(archive, CATEGORY_SOURCE)
        hierarchy_source = _ppm_json(archive, CATEGORY_HIERARCHY)
        link_source = _ppm_json(archive, LINK_SOURCE)
        type_source = _ppm_json(archive, TYPE_SOURCE)
        structure_source = _ppm_json(archive, STRUCTURE_SOURCE)

    if structure_source.get('contract') != 'content_structure_language_gate_v2':
        raise RuntimeError('PPM679_STRUCTURE_AUTHORITY_INVALID')
    if link_source.get('contract') != 'WORDPRESS_LINK_TARGET_SNAPSHOT_V1':
        raise RuntimeError('PPM679_LINK_AUTHORITY_INVALID')
    faq = (type_source.get('types') or {}).get('FAQ')
    if not isinstance(faq, dict):
        raise RuntimeError('PPM679_FAQ_TYPE_AUTHORITY_MISSING')

    source_category = _one([
        row for row in (category_source.get('categories') or [])
        if isinstance(row, dict) and row.get('category_slug') == TARGET_CATEGORY
    ], 'CATEGORY_SOURCE')
    hierarchy_category = _one([
        row for row in (hierarchy_source.get('categories') or [])
        if isinstance(row, dict) and row.get('slug') == TARGET_CATEGORY
    ], 'CATEGORY_HIERARCHY')

    if source_category.get('category_name') != hierarchy_category.get('name'):
        raise RuntimeError('PPM679_PARENT_CATEGORY_NAME_MISMATCH')
    if source_category.get('wp_taxonomy') != 'category' or hierarchy_category.get('taxonomy') != 'category':
        raise RuntimeError('PPM679_PARENT_CATEGORY_TAXONOMY_MISMATCH')
    if hierarchy_category.get('assignable') is not True or 'FAQ' not in (hierarchy_category.get('allowed_article_types') or []):
        raise RuntimeError('PPM679_PARENT_CATEGORY_NOT_ASSIGNABLE_FOR_FAQ')

    required_roles = [str(v) for v in (faq.get('required_link_roles') or [])]
    if required_roles != ['parent_category', 'semantic_related', 'further_information']:
        raise RuntimeError('PPM679_PARENT_REQUIRED_LINK_ROLES_CHANGED')
    targets = link_source.get('targets') if isinstance(link_source.get('targets'), list) else []
    by_role = {str(row.get('role')): row for row in targets if isinstance(row, dict)}
    if set(by_role) != set(required_roles):
        raise RuntimeError('PPM679_PARENT_LINK_TARGET_SET_INVALID')

    sections = {
        'parent_category': 'answer',
        'semantic_related': 'details',
        'further_information': 'further_information',
    }
    reasons = {
        'parent_category': 'Übergeordneter Bereich für die grundlegenden Transportthemen.',
        'semantic_related': 'Passender interner Verweis auf das Zugfahrzeug im selben Themenbereich.',
        'further_information': 'Weiterführender interner Verweis auf Pferdeanhänger im Themenbereich Transport.',
    }
    links = []
    for role in required_roles:
        target = by_role[role]
        if target.get('status') != 'publish' or target.get('declared_object_type') != 'page':
            raise RuntimeError('PPM679_PARENT_LINK_TARGET_NOT_PUBLISHED_PAGE:' + role)
        href = str(target.get('relative_url') or '')
        if not href.startswith('/') or href.startswith('//'):
            raise RuntimeError('PPM679_PARENT_LINK_TARGET_NOT_RELATIVE:' + role)
        title = str(target.get('title') or '').strip()
        links.append({
            'active': True,
            'anchor': ('Bereich ' + title) if role == 'parent_category' else title,
            'hierarchy_path': list(target.get('hierarchy_path') or []),
            'href': href,
            'reason': reasons[role],
            'role': role,
            'section_id': sections[role],
            'snapshot_contract': link_source['contract'],
            'target_status': target['status'],
            'target_type': target['declared_object_type'],
        })

    registry = {
        'contract': 'portal_link_registry_snapshot_v2',
        'entries': copy.deepcopy(links),
        'source_snapshot_contract': link_source['contract'],
        'source_snapshot_sha256': str(link_source.get('contract_self_sha256') or stable(link_source)),
    }
    category_binding = {
        'article_type': 'FAQ',
        'category_source_snapshot_hash': stable(category_source),
        'expected_wp_parent_slugs': list(hierarchy_category.get('expected_wp_parent_slugs') or []),
        'expected_wp_taxonomy_depth': int(hierarchy_category.get('expected_wp_taxonomy_depth') or 0),
        'hierarchy_path': str(hierarchy_category.get('hierarchy_path') or hierarchy_category.get('portal_path') or ''),
        'name': str(hierarchy_category.get('name') or ''),
        'portal_level': int(hierarchy_category.get('portal_level') or hierarchy_category.get('level') or 0),
        'portal_node_types': list(hierarchy_category.get('portal_node_types') or []),
        'portal_path': str(hierarchy_category.get('portal_path') or ''),
        'portal_structure_snapshot_hash': str(hierarchy_category.get('portal_structure_snapshot_hash') or ''),
        'slug': TARGET_CATEGORY,
        'taxonomy': 'category',
        'wp_parent_chain_required': bool(hierarchy_category.get('wp_parent_chain_required')),
        'wp_taxonomy_contract_hash': str(hierarchy_category.get('wp_taxonomy_contract_hash') or ''),
        'wp_taxonomy_snapshot_hash': str(hierarchy_category.get('wp_taxonomy_snapshot_hash') or ''),
    }
    wordpress_category = copy.deepcopy(category_binding)
    wordpress_category.pop('article_type', None)
    wordpress_category['semantic_binding_not_numeric_identity'] = True

    marker = 'LT2-FAQ-001'
    marker_regex = str(structure_source.get('visible_test_marker_regex') or '')
    import re
    if not marker_regex or not re.fullmatch(marker_regex, '[' + marker + ']'):
        raise RuntimeError('PPM679_PARENT_INTERNAL_MARKER_CONTRACT_CHANGED')

    cert = faq.get('certification_evidence') if isinstance(faq.get('certification_evidence'), dict) else {}
    return {
        'category_binding': category_binding,
        'wordpress_category': wordpress_category,
        'links': links,
        'registry': registry,
        'marker': marker,
        'search_intent': str(faq.get('search_intent') or ''),
        'gold_core_binding': cert.get('gold_core_binding'),
        'proof': {
            'category_source': CATEGORY_SOURCE,
            'category_source_sha256': stable(category_source),
            'category_hierarchy_source': CATEGORY_HIERARCHY,
            'category_hierarchy_sha256': stable(hierarchy_source),
            'link_source': LINK_SOURCE,
            'link_source_sha256': str(link_source.get('contract_self_sha256') or stable(link_source)),
            'type_source': TYPE_SOURCE,
            'type_source_sha256': stable(type_source),
            'structure_source': STRUCTURE_SOURCE,
            'structure_source_sha256': stable(structure_source),
        },
    }


def _evidence(topic: str, parts: list[str]) -> str:
    rows = []
    for part in parts:
        value = ' '.join(part.split()).strip()
        if value and value[-1] not in '.!?':
            value += '.'
        rows.append(value)
    if len(rows) < 10:
        raise RuntimeError('SCENARIO_SOURCE_TOO_THIN:' + topic)
    return ' '.join(rows)


SCENARIOS = [
    {
        'title': 'Warum sollte der Reifendruck am Pferdeanhänger vor der Fahrt geprüft werden?',
        'keyword': 'Reifendruck am Pferdeanhänger',
        'intent_terms': ['Reifendruck', 'Reifen', 'Pferdeanhänger', 'Fahrt', 'Kontrolle'],
        'direct_answer': 'Der Reifendruck am Pferdeanhänger sollte vor der Fahrt kontrolliert werden, weil der passende Druck und ein unbeschädigter Reifen für einen verlässlichen Zustand des Anhängers wichtig sind. Zusätzlich werden Ventile, Laufflächen und Seitenwände sichtbar geprüft.',
        'table_value': 'Die Tabelle verbindet Reifenzustand, erkennbare Beobachtung und die daraus folgende konkrete Kontrolle vor der Fahrt.',
        'sources': [
            ('Reifendruck und Reifenbelastung', _evidence('Reifendruck', [
                'Der Sollwert für den Reifendruck richtet sich nach dem montierten Reifen und den Vorgaben für den Anhänger',
                'Gemessen wird möglichst am kalten Reifen, damit Erwärmung während der Fahrt den Ausgangswert nicht verfälscht',
                'Ein deutlich zu niedriger Druck vergrößert die Verformung des Reifens unter Last',
                'Stärkere Verformung kann die Erwärmung des Reifens während der Fahrt erhöhen',
                'Linke und rechte Anhängerseite werden unter vergleichbaren Bedingungen gemessen',
                'Ein auffälliger Druckunterschied zwischen den Seiten wird vor der Abfahrt geklärt',
                'Nach einer Korrektur wird der eingestellte Wert erneut mit der Sollvorgabe verglichen',
                'Der Ventilbereich wird nach der Druckkontrolle auf sichtbare Beschädigungen betrachtet',
                'Nach längerer Standzeit wird ein früherer Messwert nicht ungeprüft übernommen',
                'Die aktuelle Messung entscheidet über den heutigen Zustand des Reifens',
                'Die Herstellerangabe bleibt während der Kontrolle die maßgebliche Referenz',
                'Ein geschätzter Druck ersetzt keine Messung am jeweiligen Reifen',
            ])),
            ('Sichtkontrolle der Anhängerreifen', _evidence('Reifensichtkontrolle', [
                'Lauffläche und Seitenwand werden vor der Fahrt auf Schnitte und auffällige Risse geprüft',
                'Beulen oder sichtbare Verformungen werden als eigene Auffälligkeit behandelt',
                'Fremdkörper in der Lauffläche werden nicht durch eine reine Druckmessung ausgeschlossen',
                'Das Profil wird an mehreren Stellen betrachtet, weil Abrieb ungleichmäßig auftreten kann',
                'Innen- und Außenseite eines Reifens können unterschiedliche Verschleißbilder zeigen',
                'Ventilkappen und Ventile werden auf festen Sitz und erkennbare Schäden kontrolliert',
                'Ein Reifen mit sichtbarer Beschädigung wird nicht allein durch Nachfüllen als unauffällig bewertet',
                'Das Reserverad wird einbezogen, wenn es für den Anhänger vorgesehen und einsatzbereit sein soll',
                'Jede Reifenposition wird im Kontrollgang einzeln betrachtet',
                'Die Prüfung wird erst abgeschlossen, wenn keine Position ausgelassen wurde',
                'Eine erkennbare Auffälligkeit wird vor dem Losfahren fachlich geklärt',
                'Der aktuelle Sichtbefund ergänzt die Druckmessung und ersetzt sie nicht',
            ])),
        ],
    },
    {
        'title': 'Warum muss die Beleuchtung am Pferdeanhänger vor der Fahrt kontrolliert werden?',
        'keyword': 'Beleuchtung am Pferdeanhänger',
        'intent_terms': ['Beleuchtung', 'Pferdeanhänger', 'Rücklicht', 'Blinker', 'Kontrolle'],
        'direct_answer': 'Die Beleuchtung am Pferdeanhänger wird vor der Fahrt geprüft, damit Rücklicht, Bremslicht, Blinker und Kennzeichenbeleuchtung zuverlässig funktionieren. Dabei werden auch Stecker, Kabel und Leuchten auf erkennbare Auffälligkeiten kontrolliert.',
        'table_value': 'Die Tabelle ordnet jede Lichtfunktion einer sichtbaren Kontrolle und einer eindeutigen Reaktion bei festgestellten Auffälligkeiten zu.',
        'sources': [
            ('Funktionen der Anhängerbeleuchtung', _evidence('Beleuchtung', [
                'Bremsleuchten müssen beim Betätigen der Bremse eindeutig aufleuchten',
                'Der linke Fahrtrichtungsanzeiger wird getrennt vom rechten Fahrtrichtungsanzeiger geprüft',
                'Rückleuchten kennzeichnen den Anhänger bei eingeschaltetem Fahrlicht nach hinten',
                'Die Kennzeichenbeleuchtung wird als eigene Lichtfunktion kontrolliert',
                'Warnblinklicht kann einen gemeinsamen Blinktest ergänzen',
                'Der gemeinsame Blinktest ersetzt die getrennte Prüfung beider Fahrtrichtungsanzeiger nicht',
                'Beide Rückleuchten werden auf Funktion und auffällige Helligkeitsunterschiede betrachtet',
                'Ein vollständiger Ausfall einer Lichtfunktion wird vor der Fahrt behoben',
                'Nach einer Korrektur wird die betroffene Lichtfunktion erneut geschaltet',
                'Die Funktionskontrolle umfasst mehrere Schaltzustände und nicht nur eine einzelne Lampe',
                'Eine dunkle Kennzeichenleuchte kann trotz funktionierender Rückleuchten auftreten',
                'Der Kontrollgang endet erst nach einer erneuten Prüfung der zuvor auffälligen Funktion',
            ])),
            ('Stecker Kabel und Leuchten', _evidence('Elektrische Verbindung', [
                'Der Anhängerstecker wird vollständig in die vorgesehene Steckverbindung eingesetzt',
                'Eine vorhandene Verriegelung des Steckers muss in der vorgesehenen Stellung sitzen',
                'Sichtbare Kabelabschnitte werden auf Quetschungen und Scheuerstellen geprüft',
                'Das Kabel darf zwischen Zugfahrzeug und Anhänger nicht über den Boden schleifen',
                'Lose Kabelführung kann beim Rangieren oder Lenken zu einer ungünstigen Belastung führen',
                'Feuchtigkeit im Leuchtengehäuse wird als erkennbare Auffälligkeit behandelt',
                'Flackerndes Licht kann auf eine instabile elektrische Verbindung hinweisen',
                'Sichtbare Korrosion an Kontakten wird vor dem Einsatz bewertet',
                'Beschädigte Kabelisolierung bleibt auch bei aktuell leuchtender Lampe eine Auffälligkeit',
                'Die Steckverbindung wird nach einer Korrektur erneut auf festen Sitz kontrolliert',
                'Die Leitung wird abschließend auf freie Führung im Bewegungsbereich geprüft',
                'Alle elektrischen Auffälligkeiten werden vor der Abfahrt geklärt',
            ])),
        ],
    },
    {
        'title': 'Warum sollte die Anhängerkupplung vor dem Losfahren geprüft werden?',
        'keyword': 'Anhängerkupplung',
        'intent_terms': ['Anhängerkupplung', 'Kupplung', 'Pferdeanhänger', 'Sicherung', 'Kontrolle'],
        'direct_answer': 'Die Anhängerkupplung wird vor dem Losfahren kontrolliert, damit der Pferdeanhänger korrekt verbunden und die vorgesehene Sicherung vollständig hergestellt ist. Dazu gehören Verriegelung, Sicherungseinrichtungen, Stützrad und ein abschließender Kontrollgang.',
        'table_value': 'Die Tabelle verbindet Kupplung, Sicherung und Kontrollgang mit dem jeweils sichtbaren Zustand und der notwendigen Handlung vor der Abfahrt.',
        'sources': [
            ('Kupplung vor der Abfahrt', _evidence('Kupplung', [
                'Die Kupplung des Pferdeanhängers muss vollständig auf dem Kugelkopf sitzen',
                'Der vorgesehene Verriegelungsmechanismus wird bis in seine Endstellung gebracht',
                'Eine vorhandene Sicherheitsanzeige wird direkt am Kupplungskopf abgelesen',
                'Eine nur scheinbar geschlossene Verbindung gilt nicht als ausreichende Kontrolle',
                'Das Abreißseil wird an der dafür vorgesehenen Stelle befestigt',
                'Die Sicherung wird nicht lose über ungeeignete Bauteile gelegt',
                'Das Stützrad wird vollständig in die vorgesehene Fahrstellung gebracht',
                'Die Klemmung des Stützrads wird gegen unbeabsichtigtes Absenken gesichert',
                'Der Kupplungsgriff wird nach dem Schließen in seiner Endstellung betrachtet',
                'Eine erkennbare Zwischenstellung verlangt eine erneute Kontrolle der Verriegelung',
                'Die Deichsel bleibt während der Prüfung kontrolliert abgestützt',
                'Erst nach diesen Einzelkontrollen gilt der Kupplungsvorgang als abgeschlossen',
            ])),
            ('Kontrollgang nach dem Ankuppeln', _evidence('Kontrollgang', [
                'Der abschließende Rundgang beginnt erneut an der Deichsel des Anhängers',
                'Kupplung und Sicherung werden aus einer zweiten Blickrichtung kontrolliert',
                'Die elektrische Steckverbindung wird auf festen Sitz betrachtet',
                'Das Stützrad wird auf eingezogene Position und sichere Klemmung geprüft',
                'Der Abstand des Stützrads zum Boden muss für die Fahrt ausreichend sein',
                'Lose Sicherungsteile dürfen nicht im Bewegungsbereich zwischen Fahrzeug und Anhänger liegen',
                'Auch das Anschlusskabel darf im Bewegungsbereich nicht ungünstig eingeklemmt werden',
                'Auffälliges Spiel an der Verbindung führt zurück zur Kupplungskontrolle',
                'Eine unklare Anzeige wird nicht durch Gewohnheit als ausreichend bewertet',
                'Nach einer Korrektur wird der betroffene Punkt erneut geprüft',
                'Der Kontrollgang verbindet die zuvor getrennten Handgriffe zu einer letzten Gesamtprüfung',
                'Erst ein eindeutig bestätigter Zustand beendet den Kupplungsabschnitt',
            ])),
        ],
    },
]


def _dynamic_scenario(index: int) -> dict:
    n = index + 1
    topic = f'Kontrollpunkt {n} am Pferdeanhänger'
    statements_a = [f'{topic} erhält vor der Fahrt eine aktuelle Beobachtung mit der laufenden Position {k}' for k in range(1, 13)]
    statements_b = [f'Nach einer Änderung an {topic} wird die Wirkung in einem getrennten Nachkontrollschritt {k} bestätigt' for k in range(13, 25)]
    return {
        'title': f'Warum sollte {topic} vor der Fahrt geprüft werden?',
        'keyword': topic,
        'intent_terms': ['Kontrollpunkt', 'Pferdeanhänger', 'Fahrt', 'Prüfung', topic],
        'direct_answer': f'{topic} wird vor der Fahrt geprüft, damit sein aktueller Zustand eindeutig festgestellt wird. Eine erkennbare Abweichung wird am betroffenen Kontrollpunkt geklärt und danach erneut kontrolliert.',
        'table_value': f'Die Tabelle verbindet die Beobachtungen zu {topic} mit eindeutigen Handlungen und einer abschließenden Nachkontrolle vor der Fahrt.',
        'sources': [
            (f'Grundlage {topic}', _evidence(topic, statements_a)),
            (f'Nachkontrolle {topic}', _evidence(topic, statements_b)),
        ],
    }


def _scenarios(count: int) -> list[dict]:
    if count < 1:
        raise RuntimeError('TEST_ROUTE_COUNT_MUST_BE_POSITIVE')
    rows = [copy.deepcopy(v) for v in SCENARIOS[:min(count, len(SCENARIOS))]]
    for index in range(len(rows), count):
        rows.append(_dynamic_scenario(index))
    return rows


def _serve_sources(root: Path, scenarios: list[dict]):
    requests = {}
    for i, scenario in enumerate(scenarios):
        rows = []
        for j, (title, evidence) in enumerate(scenario['sources']):
            name = f'item-{i}-source-{j}.html'
            (root / name).write_text(
                f'<!doctype html><html><head><title>{title}</title></head><body><article><h1>{title}</h1><p>{evidence}</p></article></body></html>',
                encoding='utf-8',
            )
            source_id = 'src-' + hashlib.sha256((title + '\n' + evidence).encode()).hexdigest()[:32]
            rows.append({'source_id': source_id, 'source_title': title, 'path': name})
        requests[i] = rows
    handler = lambda *args, **kwargs: Quiet(*args, directory=str(root), **kwargs)
    server = ThreadingHTTPServer(('127.0.0.1', 0), handler)
    threading.Thread(target=server.serve_forever, daemon=True).start()
    return server, requests


def create(out: Path, count: int) -> dict:
    scenarios = _scenarios(count)
    if out.exists() and any(out.iterdir()):
        raise RuntimeError('TEST_FIXTURE_DIR_NOT_EMPTY')
    out.mkdir(parents=True, exist_ok=True)
    authority = _parent_authorities()
    category = authority['category_binding']['slug']

    items = []
    plan_rows = []
    for i, scenario in enumerate(scenarios):
        slot = hashlib.sha256(f'system4a-live-parity-fresh-{count}-{i}-{scenario["title"]}'.encode()).hexdigest()
        items.append({
            'title': scenario['title'],
            'target_keyword': scenario['keyword'],
            'category': category,
            'article_type': 'FAQ',
            'plan_slot': slot,
        })
        quality = {
            'contract': 'content_structure_language_binding_v2',
            'internal_test_marker': authority['marker'],
            'wordpress_category': copy.deepcopy(authority['wordpress_category']),
            'portal_link_registry': copy.deepcopy(authority['registry']),
            'portal_link_registry_hash': stable(authority['registry']),
            'link_bindings': copy.deepcopy(authority['links']),
            'intent_terms': list(scenario['intent_terms']),
            'faq_direct_answer': scenario['direct_answer'],
            'table_value_statement': scenario['table_value'],
        }
        plan = {
            'article_type': 'FAQ',
            'target_keyword': scenario['keyword'],
            'topic': scenario['title'],
            'search_intent': authority['search_intent'],
            'gold_core_binding': authority['gold_core_binding'],
            'category_binding': copy.deepcopy(authority['category_binding']),
            'quality_binding': quality,
            'quality_binding_hash': stable(quality),
            'canonical_article': {'title': scenario['title'], 'article_type': 'FAQ'},
        }
        plan_rows.append({'item_index': i, 'plan_slot': slot, 'production_plan_item': plan})

    batch_sha = stable({'count': count, 'items': items})
    snapshot = {
        'contract': 'SYSTEM4_WORDPRESS_LIVE_INPUT_FIXTURE_V1',
        'next_textmachine_metadata_batch': {
            'contract': 'PSERC_TEXTMACHINE_METADATA_BATCH_V2',
            'status': 'READY_FOR_TEXTMACHINE_METADATA_INTAKE',
            'batch_sha256': batch_sha,
            'item_count': count,
            'items': items,
            'publish_allowed': False,
        },
    }
    event = {
        'contract': chat_start_gate.START_EVENT_CONTRACT,
        'button_id': chat_start_gate.START_BUTTON_ID,
        'action': chat_start_gate.START_ACTION,
        'route': chat_start_gate.START_ROUTE,
        'article_count': count,
        'batch_sha256': batch_sha,
        'publish_allowed': False,
    }
    writej(out / 'snapshot.template.json', snapshot)
    writej(out / 'start_button.json', event)
    writej(out / 'plans.json', {
        'contract': 'SYSTEM4_MACHINE_PREWRITE_PLAN_BATCH_V1',
        'item_count': count,
        'authority': 'PPM679_COMPOSED_FROM_NON_CANDIDATE_AUTHORITIES',
        'authority_components': authority['proof'],
        'items': plan_rows,
    })

    source_root = out / 'source-pages'
    source_root.mkdir()
    server, request_rows = _serve_sources(source_root, scenarios)
    try:
        _, port = server.server_address
        source_items = []
        for i, item in enumerate(items):
            rows = []
            for row in request_rows[i]:
                rows.append({
                    'source_id': row['source_id'],
                    'source_title': row['source_title'],
                    'source_url': f'http://127.0.0.1:{port}/{row["path"]}',
                    'source_kind': 'LOCAL_HASH_BOUND_SOURCE',
                })
            source_items.append({'item_index': i, 'plan_slot': item['plan_slot'], 'sources': rows})
        request_batch = {'contract': source_acquisition.CONTRACT, 'item_count': count, 'items': source_items}
        acquired = source_acquisition.acquire_batch(request_batch, retrieved_at='2026-09-15T08:30:00+00:00')
    finally:
        server.shutdown()
        server.server_close()

    writej(out / 'acquired.json', acquired)
    writej(out / 'source_requests.json', request_batch)
    proof = {
        'contract': 'SYSTEM4_TEST_ROUTE_INPUT_FACTORY_V4',
        'article_count': count,
        'batch_sha256': batch_sha,
        'pre_point0_article_body_count': 0,
        'source_acquisition_contract': acquired['contract'],
        'source_count': sum(len(row['sources']) for row in acquired['items']),
        'count_domain': '1..N',
        'g9_candidate_used': False,
        'prewrite_authority': 'PPM679_COMPOSED_FROM_NON_CANDIDATE_AUTHORITIES',
        'prewrite_authority_components': authority['proof'],
    }
    writej(out / 'input_factory_proof.json', proof)
    return proof


def main(argv: list[str]) -> int:
    if len(argv) != 3:
        raise SystemExit('usage: test_route_input_factory.py <out-dir> <positive-count>')
    print(json.dumps(create(Path(argv[1]), int(argv[2])), ensure_ascii=False, sort_keys=True))
    return 0


if __name__ == '__main__':
    raise SystemExit(main(sys.argv))
