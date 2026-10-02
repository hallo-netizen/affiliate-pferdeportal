from __future__ import annotations
import copy, re

class DesignBlocked(RuntimeError):
    pass

def _require(condition: bool, code: str) -> None:
    if not condition:
        raise DesignBlocked(code)

def article_type_token(article_type: str) -> str:
    value=str(article_type or "").strip().casefold()
    value=value.replace("ä","ae").replace("ö","oe").replace("ü","ue").replace("ß","ss")
    value=re.sub(r"[^a-z0-9]+","-",value).strip("-")
    _require(bool(value),"DESIGN_ARTICLE_TYPE_TOKEN_INVALID")
    return "ppm-type-"+value

def visible_text(value: str) -> str:
    return re.sub(r"\s+"," ",re.sub(r"(?is)<[^>]+>"," ",str(value or ""))).strip()

def _root_match(body: str):
    return re.match(r"(?is)^\s*<article\b([^>]*)>",body)

def _class_tokens(attrs: str) -> set[str]:
    m=re.search(r"(?is)\bclass\s*=\s*([\"'])(.*?)\1",attrs)
    if not m:
        return set()
    return {x for x in re.split(r"\s+",m.group(2).strip()) if x}

def materialize_canonical_root(article: dict) -> tuple[dict,dict]:
    out=copy.deepcopy(article)
    body=str(out.get("html") or "")
    at=str(out.get("article_type") or "").strip()
    _require(bool(body.strip()),"DESIGN_BODY_EMPTY")
    _require(bool(at),"DESIGN_ARTICLE_TYPE_MISSING")

    before_text=visible_text(body)
    m=_root_match(body)
    _require(m is not None,"DESIGN_CANONICAL_ARTICLE_ROOT_MISSING")
    attrs=m.group(1)
    token=article_type_token(at)
    classes=_class_tokens(attrs)
    type_attr=re.search(r"(?is)\bdata-article-type\s*=\s*([\"'])(.*?)\1",attrs)

    # Current K10 historical defect: a completely bare <article> root.
    # Repair only this exact missing-binding case. Conflicting/partial roots fail closed.
    if not attrs.strip():
        replacement=f'<article class="ppm-generated {token}" data-article-type="{at}">'
        body=body[:m.start()]+replacement+body[m.end():]
        repaired=True
    else:
        _require("ppm-generated" in classes,"DESIGN_PPM_GENERATED_CLASS_MISSING")
        _require(token in classes,"DESIGN_ARTICLE_TYPE_CLASS_MISSING:"+token)
        _require(type_attr is not None and type_attr.group(2).strip()==at,"DESIGN_ARTICLE_TYPE_ATTRIBUTE_MISMATCH")
        repaired=False

    _require(len(re.findall(r"(?is)<article\b",body))==1,"DESIGN_NESTED_ARTICLE_FORBIDDEN")
    _require(re.search(r"(?is)<(?:style|script|iframe|form)\b",body) is None,"DESIGN_ACTIVE_OR_GLOBAL_HTML_FORBIDDEN")
    _require(re.search(r"(?is)\sstyle\s*=",body) is None,"DESIGN_INLINE_STYLE_FORBIDDEN")
    _require(re.search(r"(?is)\son[a-z0-9_-]+\s*=",body) is None,"DESIGN_EVENT_HANDLER_FORBIDDEN")
    _require("javascript:" not in body.casefold(),"DESIGN_JAVASCRIPT_URL_FORBIDDEN")

    table_count=0
    for table_count,t in enumerate(re.finditer(r"(?is)<table\b([^>]*)>",body),start=1):
        tclasses=_class_tokens(t.group(1))
        _require("system-129-table" in tclasses,f"DESIGN_TABLE_SYSTEM129_CLASS_MISSING:{table_count-1}")
        _require("comparison-table" in tclasses,f"DESIGN_TABLE_COMPARISON_CLASS_MISSING:{table_count-1}")

    after_text=visible_text(body)
    _require(before_text==after_text,"DESIGN_VISIBLE_TEXT_MUTATION_FORBIDDEN")

    out["html"]=body
    return out,{
        "contract":"K10_CANONICAL_HTML_BINDING_V1",
        "status":"PASS",
        "root_repaired":repaired,
        "required_root_classes":["ppm-generated",token],
        "data_article_type":at,
        "visible_text_changed":False,
        "table_count":table_count,
        "active_html_present":False,
    }

def validate_canonical_html(article: dict) -> dict:
    out,receipt=materialize_canonical_root(article)
    # A validator must never need to repair. It checks already-materialized output.
    if receipt["root_repaired"]:
        raise DesignBlocked("DESIGN_CANONICAL_ROOT_NOT_MATERIALIZED")
    return receipt
