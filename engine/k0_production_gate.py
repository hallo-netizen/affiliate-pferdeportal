from __future__ import annotations
import hashlib, html, json, re, sys
from pathlib import Path

from .ppm_parity_guard import verify as verify_ppm

class Blocked(RuntimeError):
    pass

FIVE_FIELDS=('article_type','category','plan_slot','target_keyword','title')
ALLOWED_TABLE_EXCEPTIONS={
    'LINEAR_SEQUENCE',
    'EXISTING_CHECKLIST_EQUIVALENT',
    'INSUFFICIENT_RELATIONAL_DIMENSIONS',
    'NUANCE_LOSS',
}

def _load(path):
    x=json.loads(Path(path).read_text(encoding='utf-8'))
    if not isinstance(x,dict):
        raise Blocked('JSON_OBJECT_REQUIRED:'+str(path))
    return x

def _plain(value):
    value=re.sub(r'(?is)<[^>]+>',' ',str(value or ''))
    value=html.unescape(value)
    return re.sub(r'\s+',' ',value).strip()

def _words(value):
    return re.findall(r'\b[\wÄÖÜäöüß-]+\b',_plain(value),re.UNICODE)

def _sha(value):
    return hashlib.sha256(str(value).encode('utf-8')).hexdigest()

def verify(package, portal):
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

    if portal.get('contract')!='K0_PORTAL_ASSIGNMENT_V1' or portal.get('status')!='PASS':
        raise Blocked('K0_PORTAL_ASSIGNMENT_NOT_PASS')
    rows=portal.get('items') or []
    if len(rows)!=1 or rows[0].get('status')!='AUTO_DETECTED':
        raise Blocked('K0_PORTAL_ASSIGNMENT_NOT_UNIQUE')
    if rows[0].get('job_identity')!=ident:
        raise Blocked('K0_PORTAL_IDENTITY_MISMATCH')

    h2=[_plain(x) for x in re.findall(r'(?is)<h2\b[^>]*>(.*?)</h2>',body)]
    if len(h2)<4 or len(h2)!=len(set(x.casefold() for x in h2)):
        raise Blocked('K0_HEADING_STRUCTURE_INVALID')
    kw=str(ident['target_keyword'])
    if sum(1 for x in h2 if kw.casefold() in x.casefold())>2:
        raise Blocked('K0_HEADING_KEYWORD_OVERUSE')

    table_present=bool(re.search(r'(?is)<table\b',body))
    typ=str(ident['article_type'])
    table_decision=package.get('table_decision') or {}
    if typ=='Vergleich' and not table_present:
        raise Blocked('K0_TABLE_REQUIRED_FOR_VERGLEICH')
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

    return {
      'contract':'K0_PRODUCTION_GATES_V1',
      'status':'PASS',
      'portal_id':rows[0].get('portal_id'),
      'portal_status':'AUTO_DETECTED',
      'article_type':typ,
      'structure_table':'PASS',
      'ppm679_status':'PASS',
      'ppm679_rule_count':104,
      'body_sha256':_sha(body),
      'publish_allowed':False,
    }

def main():
    if len(sys.argv)!=4:
        raise SystemExit('usage: k0_production_gate.py ARTICLE_PACKAGE PORTAL_ASSIGNMENT OUT')
    try:
        out=verify(_load(sys.argv[1]),_load(sys.argv[2]))
    except Blocked as exc:
        out={'contract':'K0_PRODUCTION_GATES_V1','status':'BLOCKED','reason':str(exc),'publish_allowed':False}
        Path(sys.argv[3]).write_text(json.dumps(out,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
        print(json.dumps(out,ensure_ascii=False))
        raise SystemExit(2)
    Path(sys.argv[3]).write_text(json.dumps(out,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    print(json.dumps(out,ensure_ascii=False))

if __name__=='__main__':
    main()
