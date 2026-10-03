from __future__ import annotations
import hashlib, html, json, re, sys
from pathlib import Path

from .ppm_parity_guard import verify as verify_ppm
from .writer_contract_guard import verify_package as verify_writer_contract
from .k0_product_property_research import ARTICLE_TYPE as PROPERTY_WINNER_TYPE, SEARCH_INTENT as PROPERTY_WINNER_INTENT, validate_packet as validate_property_packet, Blocked as PropertyResearchBlocked
from .k0_full_rules import verify_pre_lt68 as verify_full_rules_pre_lt68

class Blocked(RuntimeError):
    pass

FIVE_FIELDS=('article_type','category','plan_slot','target_keyword','title')
ALLOWED_TABLE_EXCEPTIONS={
    'LINEAR_SEQUENCE',
    'EXISTING_CHECKLIST_EQUIVALENT',
    'INSUFFICIENT_RELATIONAL_DIMENSIONS',
    'NUANCE_LOSS',
}

# Hard stop against a proven invalid boilerplate family that turned factual FAQ
# into generic purchase/decision copy. These strings are not style preferences;
# they are fingerprints of the proven bad template family.
FORBIDDEN_BOILERPLATE=(
    'für die praxis heißt das: betrachte',
    'trenne muss-kriterien von bloßen zusatzmerkmalen',
    'ein guter vergleich beginnt mit einer klaren reihenfolge',
    'die tabelle ordnet vier praktische prüfpunkte knapp',
    'vor der entscheidung lohnt sich eine bewusste gewichtung',
    'die praktische kontrolle sollte direkt am vorgesehenen einsatz ansetzen',
    'der letzte schritt ist die praktische kontrolle am konkreten fall',
)

INFORMATIONAL_DECISION_TERMS=(
    'muss-kriterien',
    'zusatzmerkmale',
    'passform',
    'größtmögliche ausstattung',
    'vor der entscheidung',
    'praktische kontrolle',
    'zum tatsächlichen bedarf',
    'vorgesehenen einsatz',
)

def _expected_intent(article_type,title):
    typ=str(article_type or '').strip()
    t=_plain(title).casefold()
    if typ==PROPERTY_WINNER_TYPE:
        return PROPERTY_WINNER_INTENT
    if typ=='Beratung':
        return 'DECISION_SUPPORT'
    if typ=='Vergleich':
        return 'COMPARISON_DECISION'
    if typ=='Pflege':
        return 'PROCEDURAL_GUIDANCE'
    if typ=='FAQ':
        if re.search(r'\b(welche|welcher|welches)\b.*\b(besser|geeignet|wählen|auswählen|kaufen)\b',t):
            return 'DECISION_SUPPORT'
        if re.match(r'^(wie (lege|legt|mache|macht|reinige|pflegt|pflege|verwende|nutze|benutze)\b)',t):
            return 'PROCEDURAL_INFORMATIONAL'
        return 'INFORMATIONAL_DIRECT_QUESTION'
    return 'INFORMATIONAL'

def _verify_semantic_intent(package,ident,body):
    profile=package.get('content_profile')
    if not isinstance(profile,dict):
        raise Blocked('K0_CONTENT_PROFILE_MISSING')
    expected=_expected_intent(ident.get('article_type'),ident.get('title'))
    actual=str(profile.get('search_intent') or '').strip()
    if actual!=expected:
        raise Blocked('K0_SEARCH_INTENT_MISMATCH:'+actual+':EXPECTED:'+expected)

    plain=_plain(body).casefold()
    fingerprints=[p for p in FORBIDDEN_BOILERPLATE if p in plain]
    if fingerprints:
        raise Blocked('K0_TEMPLATE_BOILERPLATE_CONTAMINATION:'+','.join(fingerprints))

    if expected=='INFORMATIONAL_DIRECT_QUESTION':
        hits=sorted({term for term in INFORMATIONAL_DECISION_TERMS if term in plain})
        if len(hits)>=3:
            raise Blocked('K0_INFORMATIONAL_FAQ_DECISION_CONTAMINATION:'+','.join(hits))
    return expected

def _load(path):
    x=json.loads(Path(path).read_text(encoding='utf-8'))
    if not isinstance(x,dict):
        raise Blocked('JSON_OBJECT_REQUIRED:'+str(path))
    return x

def _load_category_payload(path):
    x=json.loads(Path(path).read_text(encoding='utf-8'))
    if not isinstance(x,list):
        raise Blocked('CATEGORY_JSON_LIST_REQUIRED:'+str(path))
    return x

def _plain(value):
    value=re.sub(r'(?is)<[^>]+>',' ',str(value or ''))
    value=html.unescape(value)
    return re.sub(r'\s+',' ',value).strip()

def _words(value):
    return re.findall(r'\b[\wÄÖÜäöüß-]+\b',_plain(value),re.UNICODE)

def _sha(value):
    return hashlib.sha256(str(value).encode('utf-8')).hexdigest()

def verify(package, portal, category_payload):
    if package.get('contract')!='K0_ARTICLE_PACKAGE_V1':
        raise Blocked('K0_ARTICLE_PACKAGE_CONTRACT_INVALID')
    ident=package.get('identity')
    if not isinstance(ident,dict) or set(ident)!=set(FIVE_FIELDS):
        raise Blocked('K0_ARTICLE_IDENTITY_INVALID')
    if package.get('publish_allowed') is not False:
        raise Blocked('PUBLISH_ALLOWED_MUST_BE_FALSE')
    body=str(package.get('html') or '')
    if not body:
        raise Blocked('K0_ARTICLE_BODY_EMPTY')
    if package.get('final_draft_sha256')!=_sha(body):
        raise Blocked('K0_ARTICLE_BODY_SHA_MISMATCH')
    try:
        writer_metrics=verify_writer_contract(package)
    except Exception as exc:
        raise Blocked('K0_WRITER_CONTRACT_BLOCKED:'+str(exc))

    if portal.get('contract')!='K0_PORTAL_ASSIGNMENT_V1' or portal.get('status')!='PASS':
        raise Blocked('K0_PORTAL_ASSIGNMENT_NOT_PASS')
    rows=portal.get('items') or []
    if len(rows)!=1 or rows[0].get('status')!='AUTO_DETECTED':
        raise Blocked('K0_PORTAL_ASSIGNMENT_NOT_UNIQUE')
    if rows[0].get('job_identity')!=ident:
        raise Blocked('K0_PORTAL_IDENTITY_MISMATCH')

    semantic_intent=_verify_semantic_intent(package,ident,body)

    property_result=None
    if str(ident.get('article_type') or '')==PROPERTY_WINNER_TYPE:
        pc=package.get('production_context') if isinstance(package.get('production_context'),dict) else {}
        try:
            property_result=validate_property_packet(ident,pc.get('property_research'))
        except PropertyResearchBlocked as exc:
            raise Blocked('K0_PROPERTY_RESEARCH_BLOCKED:'+str(exc)) from exc
        plain=_plain(body)
        first_words=' '.join(_words(body)[:180]).casefold()
        winner=property_result['winner']
        winner_model=str(winner['model']).casefold()
        if winner_model not in first_words:
            raise Blocked('K0_PROPERTY_WINNER_DIRECT_ANSWER_MISSING:'+winner['model'])
        winner_value=('%g' % float(winner['value'])).casefold()
        if winner_value not in plain.casefold():
            raise Blocked('K0_PROPERTY_WINNER_VALUE_MISSING:'+winner_value)
        for row in property_result['candidates']:
            if str(row['model']).casefold() not in plain.casefold():
                raise Blocked('K0_PROPERTY_CANDIDATE_NOT_USED:'+row['model'])

    h2=[_plain(x) for x in re.findall(r'(?is)<h2\b[^>]*>(.*?)</h2>',body)]
    if len(h2)<4 or len(h2)!=len(set(x.casefold() for x in h2)):
        raise Blocked('K0_HEADING_STRUCTURE_INVALID')
    kw=str(ident['target_keyword'])
    if sum(1 for x in h2 if kw.casefold() in x.casefold())>2:
        raise Blocked('K0_HEADING_KEYWORD_OVERUSE')

    table_present=bool(re.search(r'(?is)<table\b',body))
    typ=str(ident['article_type'])
    table_decision=package.get('table_decision') or {}
    if typ in {'Vergleich',PROPERTY_WINNER_TYPE} and not table_present:
        raise Blocked('K0_TABLE_REQUIRED_FOR_PRODUCT_COMPARISON_TYPE')
    if typ in {'Beratung','FAQ','Pflege'} and not table_present:
        if table_decision.get('exception_code') not in ALLOWED_TABLE_EXCEPTIONS:
            raise Blocked('K0_TABLE_REQUIRED_UNLESS_DEFINED_EXCEPTION')
    if table_present:
        th=re.findall(r'(?is)<th\b[^>]*>(.*?)</th>',body)
        if len(th)<3 or any(len(_words(x))>3 for x in th):
            raise Blocked('K0_TABLE_HEADER_INVALID')
        tb=re.search(r'(?is)<tbody\b[^>]*>(.*?)</tbody>',body)
        if not tb:
            raise Blocked('K0_TABLE_BODY_MISSING')
        rows2=re.findall(r'(?is)<tr\b[^>]*>(.*?)</tr>',tb.group(1))
        if len(rows2)<4:
            raise Blocked('K0_TABLE_TOO_FEW_ROWS')
        for row in rows2:
            cells=re.findall(r'(?is)<td\b[^>]*>(.*?)</td>',row)
            if len(cells)<3:
                raise Blocked('K0_TABLE_TOO_FEW_COLUMNS')
            if len(_words(cells[0]))>3:
                raise Blocked('K0_TABLE_FIRST_COLUMN_TOO_LONG')

    ppm=verify_ppm()
    if ppm.get('status')!='PASS' or ppm.get('legacy_rule_count')!=104:
        raise Blocked('K0_PPM679_PARITY_NOT_PASS')

    try:
        full_rules=verify_full_rules_pre_lt68(package,category_payload)
    except Exception as exc:
        raise Blocked('K0_FULL_RULES_BLOCKED:'+str(exc)) from exc
    if full_rules.get('status')!='READY_FOR_LT68':
        raise Blocked('K0_FULL_RULES_NOT_READY_FOR_LT68')

    return {
      'contract':'K0_PRODUCTION_GATES_V1',
      'status':'PASS',
      'portal_id':rows[0].get('portal_id'),
      'portal_status':'AUTO_DETECTED',
      'article_type':typ,
      'structure_table':'PASS',
      'semantic_intent':semantic_intent,
      'semantic_intent_status':'PASS',
      'anti_boilerplate_status':'PASS',
      'writer_contract_status':'PASS',
      'writer_policy_sha256':writer_metrics['policy_sha256'],
      'writer_total_words':writer_metrics['total_words'],
      'writer_conclusion_ratio':writer_metrics['conclusion_ratio'],
      'property_research_status':'PASS' if property_result else 'NOT_REQUIRED',
      'property_winner_product_key':property_result['winner']['product_key'] if property_result else None,
      'ppm679_status':'PASS',
      'ppm679_rule_count':104,
      'all_rules_pre_lt68_status':'PASS',
      'all_rules_required_receipt_count':full_rules.get('required_receipt_count'),
      'all_rules_catalog_sha256':full_rules.get('catalog_sha256'),
      'all_rules_values_sha256':full_rules.get('rule_values_sha256'),
      'body_sha256':_sha(body),
      'publish_allowed':False,
    }

def main():
    if len(sys.argv)!=5:
        raise SystemExit('usage: k0_production_gate.py ARTICLE_PACKAGE PORTAL_ASSIGNMENT CATEGORY_JSON OUT')
    try:
        out=verify(_load(sys.argv[1]),_load(sys.argv[2]),_load_category_payload(sys.argv[3]))
    except Blocked as exc:
        out={'contract':'K0_PRODUCTION_GATES_V1','status':'BLOCKED','reason':str(exc),'publish_allowed':False}
        Path(sys.argv[4]).write_text(json.dumps(out,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
        print(json.dumps(out,ensure_ascii=False))
        raise SystemExit(2)
    Path(sys.argv[4]).write_text(json.dumps(out,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    print(json.dumps(out,ensure_ascii=False))

if __name__=='__main__':
    main()
