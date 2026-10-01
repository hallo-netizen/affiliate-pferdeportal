from __future__ import annotations
import re
from . import real_proof as rp

def _slug(value):
    s=str(value or '').strip().casefold()
    for a,b in (('ä','ae'),('ö','oe'),('ü','ue'),('ß','ss')):
        s=s.replace(a,b)
    s=re.sub(r'[^a-z0-9]+','-',s).strip('-')
    return s

def generic_build_wordpress(article,plan_slot):
    slug=_slug(article.get('title') or article.get('target_keyword'))
    row={
      'article_id':article['article_id'],
      'plan_slot':plan_slot,
      'title':article['title'],
      'slug':slug,
      'target_keyword':article['target_keyword'],
      'category':article['wordpress_category']['slug'],
      'article_type':article['article_type'],
      'body':article['html'],
    }
    if any(not str(row[k]).strip() for k in row):
        raise rp.Blocked('WORDPRESS_FIELD_EMPTY')
    return {
      'contract':'PFERDE_ATELIER_WORDPRESS_IMPORT_V1',
      'source':'K10_REAL_PROOF',
      'article_count':1,
      'publish_allowed':False,
      'articles':[row],
    }

rp.build_wordpress=generic_build_wordpress

if __name__=='__main__':
    try:
        rp.main()
    except rp.Blocked as exc:
        import json
        print(json.dumps({'contract':'K10_OPTIMIZATION_REAL_PROOF_V1','status':'BLOCKED','reason':str(exc),'publish_allowed':False},ensure_ascii=False,indent=2))
        raise SystemExit(2)
