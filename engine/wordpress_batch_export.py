from __future__ import annotations
import json, re, sys
from pathlib import Path

from .html_design import validate_canonical_html, DesignBlocked
from .k0_wordpress_export import CONTRACT, SOURCE, WORDPRESS_ARTICLE_FIELDS, slug_from_title

class BatchBlocked(RuntimeError): pass

def _load(path: str|Path):
    x=json.loads(Path(path).read_text(encoding="utf-8"))
    if not isinstance(x,dict):
        raise BatchBlocked("JSON_OBJECT_REQUIRED:"+str(path))
    return x

def combine(intake: dict, singles: list[dict]) -> dict:
    items=intake.get("items")
    if intake.get("contract")!="PSERC_TEXTMACHINE_METADATA_BATCH_V2" or not isinstance(items,list) or not items:
        raise BatchBlocked("BATCH_INTAKE_INVALID")
    if intake.get("item_count")!=len(items):
        raise BatchBlocked("BATCH_ITEM_COUNT_MISMATCH")

    rows_by_slot={}
    for doc in singles:
        if doc.get("contract")!=CONTRACT or doc.get("source")!=SOURCE or doc.get("article_count")!=1 or doc.get("publish_allowed") is not False:
            raise BatchBlocked("SINGLE_WORDPRESS_DOCUMENT_INVALID")
        rows=doc.get("articles")
        if not isinstance(rows,list) or len(rows)!=1 or not isinstance(rows[0],dict):
            raise BatchBlocked("SINGLE_WORDPRESS_ARTICLE_INVALID")
        row=rows[0]
        if set(row)!=set(WORDPRESS_ARTICLE_FIELDS):
            raise BatchBlocked("SINGLE_ARTICLE_FIELDS_INVALID")
        slot=str(row.get("plan_slot") or "")
        if not re.fullmatch(r"[0-9a-f]{64}",slot):
            raise BatchBlocked("SINGLE_PLAN_SLOT_INVALID")
        if str(row.get("article_id") or "")!=slot:
            raise BatchBlocked("SINGLE_ARTICLE_ID_MUST_EQUAL_PLAN_SLOT")
        if str(row.get("slug") or "")!=slug_from_title(str(row.get("title") or "")):
            raise BatchBlocked("SINGLE_SLUG_MISMATCH")
        if slot in rows_by_slot:
            raise BatchBlocked("SINGLE_PLAN_SLOT_DUPLICATE:"+slot)
        body=str(row.get("body") or "")
        if not body:
            raise BatchBlocked("SINGLE_BODY_EMPTY:"+slot)
        try:
            validate_canonical_html({"article_type":str(row.get("article_type") or ""),"html":body})
        except DesignBlocked as exc:
            raise BatchBlocked("SINGLE_HTML_INVALID:"+slot+":"+str(exc)) from exc
        rows_by_slot[slot]=row

    ordered=[]
    for item in items:
        if not isinstance(item,dict):
            raise BatchBlocked("BATCH_ITEM_INVALID")
        slot=str(item.get("plan_slot") or "")
        row=rows_by_slot.get(slot)
        if row is None:
            raise BatchBlocked("BATCH_ARTICLE_MISSING:"+slot)
        for key in ("title","target_keyword","category","article_type","plan_slot"):
            if str(row.get(key) or "")!=str(item.get(key) or ""):
                raise BatchBlocked("BATCH_IDENTITY_MISMATCH:"+slot+":"+key)
        ordered.append(dict(row))

    if set(rows_by_slot)!=set(str(x.get("plan_slot") or "") for x in items if isinstance(x,dict)):
        raise BatchBlocked("BATCH_EXTRA_OR_MISSING_ARTICLE")

    return {
        "contract":CONTRACT,
        "source":SOURCE,
        "article_count":len(ordered),
        "publish_allowed":False,
        "articles":ordered,
    }

def main():
    if len(sys.argv)<4:
        raise SystemExit("usage: wordpress_batch_export.py INTAKE OUT SINGLE1 [SINGLE2 ...]")
    try:
        intake=_load(sys.argv[1]); singles=[_load(p) for p in sys.argv[3:]]
        out=combine(intake,singles)
    except (BatchBlocked,DesignBlocked) as exc:
        print(json.dumps({"contract":"K0_WORDPRESS_BATCH_EXPORT_V2","status":"BLOCKED","reason":str(exc),"publish_allowed":False},ensure_ascii=False))
        raise SystemExit(2)
    Path(sys.argv[2]).write_text(json.dumps(out,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
    print(json.dumps({"contract":"K0_WORDPRESS_BATCH_EXPORT_V2","status":"PASS","article_count":out["article_count"],"publish_allowed":False},ensure_ascii=False))

if __name__=="__main__":
    main()
