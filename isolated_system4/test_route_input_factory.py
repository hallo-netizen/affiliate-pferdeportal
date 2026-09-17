from __future__ import annotations

import copy
import hashlib
import json
import os
import re
import sys
import threading
import zipfile
from http.server import ThreadingHTTPServer, SimpleHTTPRequestHandler
from pathlib import Path

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
FRESH_TOKEN_ENV = 'SYSTEM4_FRESH_RUN_TOKEN'


def stable(value) -> str:
    return hashlib.sha256(json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(',', ':')).encode()).hexdigest()


def sha_text(value: str) -> str:
    return hashlib.sha256(value.encode('utf-8')).hexdigest()


def writej(path: Path, value) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2, sort_keys=True) + '\n', encoding='utf-8')


def _fresh_token() -> str:
    token = str(os.environ.get(FRESH_TOKEN_ENV) or '').strip()
    if len(token) < 16:
        raise RuntimeError('SYSTEM4_FRESH_RUN_TOKEN_REQUIRED')
    return token


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


BASE_SCENARIOS = [
    {
        'keyword': 'Verschlusskontrolle am Pferdeanhänger',
        'intent_terms': ['Verschluss', 'Klappe', 'Tür', 'Pferdeanhänger', 'Kontrolle'],
        'direct_answer': 'Die Verschlusskontrolle am Pferdeanhänger prüft Türen, Klappen und Verriegelungen einzeln auf vollständigen Sitz und erkennbare Beschädigungen. Auffällige Verschlüsse werden vor der Abfahrt geklärt und anschließend erneut kontrolliert.',
        'table_value': 'Die Tabelle ordnet Verschluss, sichtbaren Zustand und notwendige Nachkontrolle eindeutig ein.',
        'sources': [
            ('Verriegelungen und Klappen', _evidence('Verschlusskontrolle', [
                'Jede Tür und jede Klappe wird einzeln bis in die vorgesehene Endstellung geschlossen',
                'Verriegelungen werden auf vollständigen Eingriff der vorgesehenen Sicherung geprüft',
                'Ein nur teilweise eingerasteter Verschluss gilt nicht als abgeschlossene Kontrolle',
                'Scharniere werden auf sichtbare Lockerung und ungewöhnliches Spiel betrachtet',
                'Beschädigte oder verbogene Bauteile werden vor der Fahrt fachlich geklärt',
                'Lose Zusatzteile dürfen einen Verschluss nicht am vollständigen Schließen hindern',
                'Nach einer Korrektur wird derselbe Verschluss erneut geöffnet und geschlossen',
                'Die Kontrolle umfasst auch kleinere Serviceklappen und vorhandene Außenfächer',
                'Eine zweite Sichtprüfung bestätigt die Endstellung nach dem ersten Schließen',
                'Der Kontrollgang wird in einer festen Reihenfolge durchgeführt, damit kein Verschluss ausgelassen wird',
                'Die Prüfung endet erst nach eindeutiger Bestätigung aller vorgesehenen Sicherungen',
                'Der aktuelle Sichtbefund entscheidet über die Freigabe des jeweiligen Verschlusses',
            ])),
            ('Abschlusskontrolle der Öffnungen', _evidence('Abschlusskontrolle', [
                'Der abschließende Rundgang beginnt an einer festgelegten Seite des Anhängers',
                'Jede zuvor geprüfte Öffnung wird im Rundgang erneut sichtbar zugeordnet',
                'Überstehende Griffe oder nicht angelegte Sicherungen werden vor der Fahrt korrigiert',
                'Gummidichtungen dürfen den Verriegelungsweg nicht sichtbar behindern',
                'Eine unklare Endstellung wird nicht durch Gewohnheit als ausreichend bewertet',
                'Nach jedem Eingriff wird die betroffene Sicherung erneut vollständig geprüft',
                'Der Rundgang verbindet einzelne Verschlussprüfungen zu einer letzten Gesamtprüfung',
                'Auch von außen schlecht sichtbare Sicherungspunkte werden gezielt betrachtet',
                'Bewegliche Teile werden so gesichert, dass sie während der Fahrt nicht frei aufschwingen können',
                'Die Kontrollreihenfolge bleibt bis zum Ende gleich und nachvollziehbar',
                'Ein festgestellter Mangel führt zurück zum betroffenen Verschluss und nicht zum Überspringen des Punkts',
                'Erst ein eindeutiger Abschlussbefund beendet die Verschlusskontrolle',
            ])),
        ],
    },
    {
        'keyword': 'Bodenprüfung am Pferdeanhänger',
        'intent_terms': ['Boden', 'Pferdeanhänger', 'Oberfläche', 'Feuchtigkeit', 'Kontrolle'],
        'direct_answer': 'Die Bodenprüfung am Pferdeanhänger kontrolliert die sichtbare Oberfläche, Übergänge und zugängliche Randbereiche auf Feuchtigkeit, Beschädigungen und auffällige Verformungen. Unklare Stellen werden vor der Nutzung näher geprüft.',
        'table_value': 'Die Tabelle verbindet sichtbaren Bodenbefund, mögliche Auffälligkeit und die daraus folgende Kontrolle vor der Nutzung.',
        'sources': [
            ('Sichtprüfung der Bodenfläche', _evidence('Bodenprüfung', [
                'Die zugängliche Bodenfläche wird vollständig und nicht nur im mittleren Laufbereich betrachtet',
                'Übergänge zu Wänden und Rampen werden als eigene Kontrollbereiche einbezogen',
                'Feuchte Stellen werden von trockenen Bereichen unterschieden und gezielt nachverfolgt',
                'Abhebungen oder erkennbare Verformungen werden nicht durch eine oberflächliche Reinigung verdeckt',
                'Lose Beläge werden auf ihre Befestigung und den darunter sichtbaren Zustand geprüft',
                'Ein auffälliger Geruch kann Anlass für eine genauere Kontrolle verdeckter Feuchtigkeit sein',
                'Beschädigte Kanten werden vor der Nutzung auf ihre Ursache und Auswirkung bewertet',
                'Nach einer Reinigung wird die zuvor auffällige Stelle erneut betrachtet',
                'Die Kontrolle folgt einer festen Richtung, damit Randbereiche nicht ausgelassen werden',
                'Zugängliche Befestigungspunkte werden auf sichtbare Lockerung oder Korrosion geprüft',
                'Eine unklare Stelle wird nicht allein wegen trockener Oberfläche als unauffällig bewertet',
                'Der aktuelle Gesamtzustand ergibt sich aus Fläche, Übergängen und Randbereichen gemeinsam',
            ])),
            ('Nachkontrolle auffälliger Stellen', _evidence('Bodennachkontrolle', [
                'Eine markierte Auffälligkeit wird nach dem ersten Rundgang gezielt erneut aufgesucht',
                'Die Nachkontrolle vergleicht die Stelle mit unmittelbar angrenzenden unauffälligen Bereichen',
                'Veränderungen nach Belastung oder Reinigung werden getrennt dokumentiert',
                'Eine weiche oder nachgiebige Stelle verlangt eine genauere fachliche Bewertung',
                'Sichtbare Risse werden in Verlauf und Ausdehnung betrachtet statt nur punktuell bewertet',
                'Feuchtigkeit an Übergängen wird auf mögliche Eintrittswege hin kontrolliert',
                'Lose Verbindungsteile werden vor einer erneuten Nutzung fachgerecht geklärt',
                'Nach einer Reparatur wird die betroffene Zone erneut im vollständigen Kontrollgang geprüft',
                'Der Vergleich mit dem Ausgangsbefund verhindert das Übersehen einer unveränderten Auffälligkeit',
                'Die Nachkontrolle ersetzt nicht die vollständige Prüfung der übrigen Bodenbereiche',
                'Alle markierten Stellen müssen vor Abschluss des Rundgangs eindeutig bewertet sein',
                'Erst danach wird der Bodenabschnitt als kontrolliert abgeschlossen',
            ])),
        ],
    },
    {
        'keyword': 'Lüftungskontrolle am Pferdeanhänger',
        'intent_terms': ['Lüftung', 'Öffnung', 'Pferdeanhänger', 'Luftweg', 'Kontrolle'],
        'direct_answer': 'Die Lüftungskontrolle am Pferdeanhänger prüft vorhandene Öffnungen, Schieber und Luftwege auf freie Funktion, sicheren Sitz und erkennbare Blockaden. Veränderungen werden vor der Fahrt beseitigt und danach erneut geprüft.',
        'table_value': 'Die Tabelle ordnet Lüftungselement, sichtbaren Zustand und die erforderliche Funktionskontrolle vor der Fahrt zu.',
        'sources': [
            ('Lüftungsöffnungen und Schieber', _evidence('Lüftungskontrolle', [
                'Vorhandene Lüftungsöffnungen werden einzeln auf freie Durchgänge und sichtbare Blockaden betrachtet',
                'Schieber und Klappen werden in den vorgesehenen Stellungen auf Beweglichkeit geprüft',
                'Lose Abdeckungen dürfen nicht in einen Luftweg hineinragen',
                'Verschmutzungen an Gittern werden als eigene Auffälligkeit behandelt',
                'Beschädigte Gitter oder Halterungen werden vor der Fahrt fachlich geklärt',
                'Ein schwergängiger Schieber wird nicht mit Gewalt in eine scheinbare Endstellung gedrückt',
                'Nach einer Reinigung wird die Beweglichkeit des betroffenen Elements erneut geprüft',
                'Die Kontrollreihenfolge umfasst alle vorhandenen Öffnungen auf beiden Seiten',
                'Ein nur teilweise freier Luftweg wird nicht als vollständig kontrolliert bewertet',
                'Die vorgesehene Fahrstellung jedes verstellbaren Elements wird sichtbar bestätigt',
                'Auffällige Geräusche oder Spiel an beweglichen Teilen führen zu einer Nachkontrolle',
                'Der aktuelle Zustand wird unmittelbar vor der Nutzung erneut bestätigt',
            ])),
            ('Abschlussprüfung der Luftwege', _evidence('Luftwegprüfung', [
                'Der Abschlussrundgang ordnet jede Öffnung erneut ihrer vorgesehenen Funktion zu',
                'Gegenstände im Innenraum dürfen vorgesehene Luftwege nicht sichtbar verdecken',
                'Bewegliche Abdeckungen werden auf sicheren Sitz in der gewählten Stellung geprüft',
                'Eine zuvor gereinigte Öffnung wird auf verbliebene Blockaden kontrolliert',
                'Beschlag oder Feuchtigkeit an einer Öffnung wird als Hinweis für eine zusätzliche Sichtprüfung genutzt',
                'Die Nachkontrolle prüft nicht nur Beweglichkeit, sondern auch die tatsächliche freie Öffnung',
                'Lose Befestigungen werden vor Fahrtbeginn geklärt',
                'Eine unklare Stellung führt zurück zur Bedienung des betroffenen Elements',
                'Alle Öffnungen werden in derselben Reihenfolge wie bei der Erstprüfung erneut betrachtet',
                'Der Kontrollgang endet nicht, solange ein Luftweg ungeklärt bleibt',
                'Nach einem Eingriff wird die betroffene Stelle erneut in den Gesamtgang einbezogen',
                'Erst danach gilt die Lüftungskontrolle als abgeschlossen',
            ])),
        ],
    },
]

CONDITIONS = [
    'nach längerer Standzeit',
    'vor einer frühen Abfahrt',
    'nach einer gründlichen Reinigung',
    'nach einem starken Wetterwechsel',
    'vor einer längeren Strecke',
    'nach einer Wartung',
    'vor der ersten Fahrt des Tages',
    'nach einer Fahrtpause',
    'bei wechselnder Außentemperatur',
    'nach sichtbarer Verschmutzung',
    'nach einem Beladungswechsel',
    'vor einer erneuten Nutzung',
]


def _freshen(base: dict, index: int, token: str) -> dict:
    seed = sha_text(token + '|' + str(index) + '|' + str(base['keyword']))
    condition = CONDITIONS[int(seed[:8], 16) % len(CONDITIONS)]
    keyword = str(base['keyword'])
    scenario = copy.deepcopy(base)
    scenario['title'] = f'Wie wird {keyword} {condition} richtig durchgeführt?'
    scenario['direct_answer'] = str(base['direct_answer']).rstrip() + f' Der konkrete Kontrollfall betrachtet die Prüfung {condition}.'
    scenario['table_value'] = str(base['table_value']).rstrip() + f' Der Vergleich gilt für die Situation {condition}.'
    scenario['fresh_seed_sha256'] = seed
    scenario['condition'] = condition
    return scenario


def _dynamic_scenario(index: int, token: str) -> dict:
    seed = sha_text(token + '|dynamic|' + str(index))
    n = int(seed[:8], 16) % 9000 + 1000
    keyword = f'Kontrollfolge {n} am Pferdeanhänger'
    statements_a = [f'Die {keyword} ordnet vor der Fahrt den Kontrollschritt {k} einem eindeutig sichtbaren Zustand zu' for k in range(1, 13)]
    statements_b = [f'Nach einer Änderung in der {keyword} wird der betroffene Zustand in einem getrennten Nachkontrollschritt {k} erneut bestätigt' for k in range(13, 25)]
    return _freshen({
        'keyword': keyword,
        'intent_terms': ['Kontrollfolge', 'Pferdeanhänger', 'Fahrt', 'Prüfung', keyword],
        'direct_answer': f'Die {keyword} strukturiert die Kontrolle vor der Fahrt in klar getrennte Punkte. Eine erkennbare Abweichung wird am betroffenen Kontrollpunkt geklärt und danach erneut kontrolliert.',
        'table_value': f'Die Tabelle verbindet die Beobachtungen der {keyword} mit eindeutigen Handlungen und einer abschließenden Nachkontrolle.',
        'sources': [
            (f'Grundlage der {keyword}', _evidence(keyword, statements_a)),
            (f'Nachkontrolle der {keyword}', _evidence(keyword, statements_b)),
        ],
    }, index, token)


def _scenarios(count: int, token: str) -> list[dict]:
    if count < 1:
        raise RuntimeError('TEST_ROUTE_COUNT_MUST_BE_POSITIVE')
    rows = [_freshen(copy.deepcopy(v), i, token) for i, v in enumerate(BASE_SCENARIOS[:min(count, len(BASE_SCENARIOS))])]
    for index in range(len(rows), count):
        rows.append(_dynamic_scenario(index, token))
    titles = [row['title'] for row in rows]
    if len(titles) != len(set(titles)):
        raise RuntimeError('SYSTEM4_FRESH_TOPIC_COLLISION')
    return rows


def _serve_sources(root: Path, scenarios: list[dict], fresh_token_sha256: str):
    requests = {}
    for i, scenario in enumerate(scenarios):
        rows = []
        for j, (title, evidence) in enumerate(scenario['sources']):
            name = f'item-{i}-source-{j}.html'
            source_freshness = sha_text(fresh_token_sha256 + '|' + str(i) + '|' + str(j) + '|' + title)
            (root / name).write_text(
                '<!doctype html><html><head>'
                f'<title>{title}</title><meta name="system4-source-snapshot" content="{source_freshness}">'
                f'</head><body><!--system4-source-snapshot:{source_freshness}--><article><h1>{title}</h1><p>{evidence}</p></article></body></html>',
                encoding='utf-8',
            )
            source_id = 'src-' + sha_text(fresh_token_sha256 + '\n' + title + '\n' + evidence)[:32]
            rows.append({'source_id': source_id, 'source_title': title, 'path': name, 'freshness_sha256': source_freshness})
        requests[i] = rows
    handler = lambda *args, **kwargs: Quiet(*args, directory=str(root), **kwargs)
    server = ThreadingHTTPServer(('127.0.0.1', 0), handler)
    threading.Thread(target=server.serve_forever, daemon=True).start()
    return server, requests


def create(out: Path, count: int) -> dict:
    token = _fresh_token()
    token_sha = sha_text(token)
    scenarios = _scenarios(count, token)
    if out.exists() and any(out.iterdir()):
        raise RuntimeError('TEST_FIXTURE_DIR_NOT_EMPTY')
    out.mkdir(parents=True, exist_ok=True)
    authority = _parent_authorities()
    category = authority['category_binding']['slug']

    items = []
    plan_rows = []
    for i, scenario in enumerate(scenarios):
        slot = sha_text(f'system4a-fresh|{token_sha}|{count}|{i}|{scenario["title"]}')
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

    batch_sha = stable({'fresh_run_token_sha256': token_sha, 'count': count, 'items': items})
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
    server, request_rows = _serve_sources(source_root, scenarios, token_sha)
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
    freshness = {
        'contract': 'SYSTEM4_FRESH_ARTICLE_INPUT_V1',
        'fresh_run_token_sha256': token_sha,
        'article_count': count,
        'titles': [row['title'] for row in scenarios],
        'title_sha256': [sha_text(row['title']) for row in scenarios],
        'scenario_seed_sha256': [row['fresh_seed_sha256'] for row in scenarios],
        'plan_slots': [row['plan_slot'] for row in items],
        'source_ids': [[s['source_id'] for s in row['sources']] for row in acquired['items']],
        'pre_point0_article_body_count': 0,
        'article_body_source_allowed': False,
        'old_article_fixture_allowed': False,
        'recovery_article_allowed': False,
        'ppm_candidate_article_allowed': False,
    }
    writej(out / 'freshness.json', freshness)
    proof = {
        'contract': 'SYSTEM4_TEST_ROUTE_INPUT_FACTORY_V5',
        'article_count': count,
        'batch_sha256': batch_sha,
        'pre_point0_article_body_count': 0,
        'source_acquisition_contract': acquired['contract'],
        'source_count': sum(len(row['sources']) for row in acquired['items']),
        'count_domain': '1..N',
        'g9_candidate_used': False,
        'old_article_body_used': False,
        'freshness_required': True,
        'fresh_run_token_sha256': token_sha,
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
