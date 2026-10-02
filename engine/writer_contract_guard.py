from __future__ import annotations
import hashlib, html, json, re, sys
from pathlib import Path

CONTRACT='CANONICAL_WRITER_RECEIPT_V1'
POLICY_CONTRACT='CANONICAL_WRITER_QUALITY_POLICY_V1'

POLICY={
  'contract':POLICY_CONTRACT,
  'total_words_min':750,
  'total_words_max':900,
  'normal_h2_words_min':100,
  'normal_h2_words_max':220,
  'normal_h2_max_ratio':1.50,
  'conclusion_ratio_min':0.10,
  'conclusion_ratio_max':0.15,
  'conclusion_max_paragraphs':3,
  'further_information_required':True,
  'further_information_max_words':60,
  'required_section_blocks':['conclusion','further_information'],
  'special_blocks':['table','conclusion','further_information'],
}

class WriterContractBlocked(RuntimeError):
    pass

def stable(value):
    return hashlib.sha256(json.dumps(value,ensure_ascii=False,sort_keys=True,separators=(',',':')).encode('utf-8')).hexdigest()

def sha_text(value):
    return hashlib.sha256(str(value).encode('utf-8')).hexdigest()

def _plain(value):
    value=re.sub(r'(?is)<[^>]+>',' ',str(value or ''))
    value=html.unescape(value)
    return re.sub(r'\s+',' ',value).strip()

def _word_count(value):
    return len(re.findall(r'\b[\wÄÖÜäöüß-]+\b',_plain(value),re.UNICODE))

def _sections(article_html):
    rows=[]
    for m in re.finditer(r'(?is)<section\b[^>]*data-block\s*=\s*["\']([^"\']+)["\'][^>]*>(.*?)</section>',article_html):
        block=m.group(1)
        inner=m.group(2)
        h2=re.search(r'(?is)<h2\b[^>]*>(.*?)</h2>',inner)
        body=inner[h2.end():] if h2 else inner
        rows.append({
          'block_id':block,
          'heading':_plain(h2.group(1)) if h2 else '',
          'has_h2':h2 is not None,
          'word_count':_word_count(body),
          'paragraph_count':len(re.findall(r'(?is)<p\b[^>]*>',body)),
        })
    return rows

def inspect_html(article_html):
    if not isinstance(article_html,str) or not article_html.strip():
        raise WriterContractBlocked('WRITER_BODY_EMPTY')
    rows=_sections(article_html)
    if not rows:
        raise WriterContractBlocked('WRITER_SECTION_CONTRACT_MISSING')

    ids=[r['block_id'] for r in rows]
    for required in POLICY['required_section_blocks']:
        if ids.count(required)!=1:
            raise WriterContractBlocked('WRITER_REQUIRED_SECTION_COUNT:'+required+':'+str(ids.count(required)))

    total=_word_count(article_html)
    if total<POLICY['total_words_min'] or total>POLICY['total_words_max']:
        raise WriterContractBlocked(f'WRITER_TOTAL_WORD_RANGE:{total}:{POLICY["total_words_min"]}:{POLICY["total_words_max"]}')

    normal=[r for r in rows if r['block_id'] not in POLICY['special_blocks'] and r['has_h2']]
    if not normal:
        raise WriterContractBlocked('WRITER_NORMAL_H2_SECTION_MISSING')
    bad=[r for r in normal if r['word_count']<POLICY['normal_h2_words_min'] or r['word_count']>POLICY['normal_h2_words_max']]
    if bad:
        r=bad[0]
        raise WriterContractBlocked(f'WRITER_H2_WORD_RANGE:{r["word_count"]}:{r["heading"]}')

    counts=[r['word_count'] for r in normal]
    lo=min(counts); hi=max(counts)
    if lo<=0 or hi/lo>POLICY['normal_h2_max_ratio']:
        raise WriterContractBlocked(f'WRITER_H2_IMBALANCE:{lo}:{hi}:{POLICY["normal_h2_max_ratio"]:.2f}')

    conclusion=[r for r in rows if r['block_id']=='conclusion'][0]
    cr=conclusion['word_count']/total
    if cr<POLICY['conclusion_ratio_min']:
        raise WriterContractBlocked(f'WRITER_CONCLUSION_TOO_SHORT:{cr:.6f}:{POLICY["conclusion_ratio_min"]:.6f}')
    if cr>POLICY['conclusion_ratio_max']:
        raise WriterContractBlocked(f'WRITER_CONCLUSION_TOO_LONG:{cr:.6f}:{POLICY["conclusion_ratio_max"]:.6f}')
    if conclusion['paragraph_count']>POLICY['conclusion_max_paragraphs']:
        raise WriterContractBlocked('WRITER_CONCLUSION_TOO_MANY_PARAGRAPHS:'+str(conclusion['paragraph_count']))

    further=[r for r in rows if r['block_id']=='further_information'][0]
    if not further['has_h2'] or further['heading'].casefold()!='weiterführende informationen'.casefold():
        raise WriterContractBlocked('WRITER_FURTHER_INFORMATION_HEADING_INVALID')
    if further['word_count']>POLICY['further_information_max_words']:
        raise WriterContractBlocked('WRITER_FURTHER_INFORMATION_TOO_LONG:'+str(further['word_count']))

    return {
      'status':'PASS',
      'policy_contract':POLICY_CONTRACT,
      'policy_sha256':stable(POLICY),
      'total_words':total,
      'normal_h2_sections':normal,
      'normal_h2_shortest':lo,
      'normal_h2_longest':hi,
      'conclusion_words':conclusion['word_count'],
      'conclusion_ratio':cr,
      'further_information_words':further['word_count'],
    }

def issue_receipt(article):
    body=str(article.get('html') or '')
    metrics=inspect_html(body)
    core={
      'contract':CONTRACT,
      'status':'PASS',
      'route':'CANONICAL_WRITER_CONTRACT_ONLY',
      'article_id':str(article.get('article_id') or ''),
      'visible_text_sha256':sha_text(_plain(body)),
      'section_structure_sha256':stable(metrics['normal_h2_sections']),
      'policy_sha256':metrics['policy_sha256'],
      'section_balance_status':'PASS',
      'conclusion_status':'PASS',
      'further_information_status':'PASS',
      'total_words':metrics['total_words'],
      'conclusion_ratio':round(metrics['conclusion_ratio'],6),
      'publish_allowed':False,
    }
    return {**core,'receipt_sha256':stable(core)}

def bind_receipt(article):
    out=json.loads(json.dumps(article))
    out['final_draft_sha256']=sha_text(str(out.get('html') or ''))
    out['writer_provenance']=issue_receipt(out)
    return out

def verify_package(article):
    actual=article.get('writer_provenance')
    if not isinstance(actual,dict):
        raise WriterContractBlocked('WRITER_PROVENANCE_MISSING')
    expected=issue_receipt(article)
    if actual!=expected:
        raise WriterContractBlocked('WRITER_PROVENANCE_INVALID_OR_STALE')
    return inspect_html(str(article.get('html') or ''))


def main():
    if len(sys.argv)<3:
        raise SystemExit('usage: writer_contract_guard.py stamp IN OUT | verify IN')
    mode=sys.argv[1]
    try:
        if mode=='stamp' and len(sys.argv)==4:
            article=json.loads(Path(sys.argv[2]).read_text(encoding='utf-8'))
            out=bind_receipt(article)
            Path(sys.argv[3]).write_text(json.dumps(out,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
            print(json.dumps({'contract':CONTRACT,'status':'PASS','receipt':out['writer_provenance']},ensure_ascii=False))
            return
        if mode=='verify' and len(sys.argv)==3:
            article=json.loads(Path(sys.argv[2]).read_text(encoding='utf-8'))
            metrics=verify_package(article)
            print(json.dumps({'contract':CONTRACT,'status':'PASS','metrics':metrics},ensure_ascii=False))
            return
        raise WriterContractBlocked('WRITER_GUARD_USAGE_INVALID')
    except Exception as exc:
        print(json.dumps({'contract':CONTRACT,'status':'BLOCKED','reason':str(exc),'publish_allowed':False},ensure_ascii=False))
        raise SystemExit(2)

if __name__=='__main__':
    main()
